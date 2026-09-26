"""定时发现：按 data/sources.yaml 搜索 GitHub，由模型筛选、分类后收录。

用法：
  python scripts/discover.py --dry-run          # 只列出候选，不调用模型、不写文件
  python scripts/discover.py --summary out.md   # 评估并收录（调用 classify.py 的后端），结果写成 PR 描述
Agent 模式（在 Claude Code 会话或云端 routine 中运行，由会话里的 Claude 自己判断，不再调用模型）：
  python scripts/discover.py --export work.json # 写出评审标准和候选资料（含 README 节选）
  #   ……Claude 按 work.json 里的 instructions 写出 verdicts.json：{"items": [Verdict, ...]}
  python scripts/discover.py --apply verdicts.json --summary out.md
所有评估过的候选都会记入 data/seen.yaml，seen_ttl_days 天内不再重复评估。
审阅 PR 时，删掉 projects.yaml 中不想要的行即可；这些项目仍留在 seen.yaml 中，不会再被推荐。
"""
import argparse
import json
import os
import re
import sys
import time
from datetime import date, timedelta
from itertools import zip_longest
from pathlib import Path

import yaml

import gh
from lib import ROOT, load_meta, load_projects, load_yaml_list, save_projects

SOURCES_FILE = ROOT / "data" / "sources.yaml"
SEEN_FILE = ROOT / "data" / "seen.yaml"


def expand(query):
    return re.sub(r"\{(\d+)d\}", lambda m: (date.today() - timedelta(days=int(m[1]))).isoformat(), query)


def load_seen():
    if not SEEN_FILE.exists():
        return {}
    return {s["repo"].lower(): s for s in load_yaml_list(SEEN_FILE)}


def save_seen(seen):
    lines = [yaml.safe_dump([s], default_flow_style=None, allow_unicode=True, sort_keys=False, width=100000).rstrip()
             for s in sorted(seen.values(), key=lambda s: s["repo"].lower())]
    SEEN_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def collect(cfg, skip):
    """按领域搜索，并在各领域之间轮流取候选，避免某一个领域占满名额。"""
    pause = 2 if os.environ.get("GITHUB_TOKEN") else 7  # 搜索 API 限速：登录 30 次/分钟，匿名 10 次/分钟
    per_domain = {}
    for domain, queries in cfg["queries"].items():
        bucket = per_domain.setdefault(domain, [])
        for q in queries:
            try:
                items = gh.search(expand(q), cfg["per_query"])
            except gh.RateLimited:
                print(f"[限流] 跳过查询：{q}", file=sys.stderr)
                continue
            for d in items:
                key = d["full_name"].lower()
                if d["fork"] or d["archived"] or key in skip:
                    continue
                skip.add(key)
                bucket.append(d)
            time.sleep(pause)
    ordered = [d for group in zip_longest(*per_domain.values()) for d in group if d]
    return ordered[:cfg["max_candidates"]]


def apply(candidates, verdicts, meta, projects, seen):
    added, rejected = [], []
    for d in candidates:
        name = d["full_name"] if "full_name" in d else d["repo"]
        v = verdicts.get(name.lower())
        if v is None:
            continue  # 本次没拿到结果，下次再评估
        seen[name.lower()] = {"repo": name, "at": gh.today(), "relevant": v.relevant, "reason": v.reason}
        if not v.relevant:
            rejected.append((name, v.reason))
            continue
        p = {"repo": name, "category": v.category, "kind": v.kind, "ring": "assess", "why": v.why,
             "added_at": gh.today(), "source": "auto"}
        if "full_name" in d:
            gh.apply_meta(p, d)
        projects.append(p)
        added.append(p)
    return added, rejected


def summarize(n, added, rejected, meta):
    lines = [f"本次评估 {n} 个候选，建议收录 **{len(added)}** 个。",
             "", "审阅方式：不想要的项目，直接在本 PR 中删掉 `data/projects.yaml` 里对应的行（它们仍记在 seen.yaml 中，不会再被推荐），然后运行 `python scripts/render.py` 并提交。", ""]
    if added:
        lines += ["| 项目 | 分类 | 类型 | 为什么关注 | ⭐ |", "|---|---|---|---|---|"]
        for p in sorted(added, key=lambda p: p["category"]):
            top, sub = meta["index"][p["category"]]
            lines.append(f"| [{p['repo']}](https://github.com/{p['repo']}) | {top['name']} / {sub['name']} | "
                         f"{meta['kinds'][p['kind']]['name']} | {p['why']} | {p.get('stars', '-')} |")
    if rejected:
        lines += ["", f"<details><summary>未收录 {len(rejected)} 个</summary>", ""]
        lines += [f"- [{n}](https://github.com/{n})：{r}" for n, r in rejected]
        lines += ["", "</details>"]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--export", help="Agent 模式：写出评审标准和候选到此 JSON 文件")
    ap.add_argument("--apply", help="Agent 模式：读取 verdicts JSON 并收录")
    ap.add_argument("--summary")
    args = ap.parse_args()

    from classify import Verdicts, check, classify, system_prompt, to_candidate
    meta, projects, seen = load_meta(), load_projects(), load_seen()

    if args.apply:
        work_file = Path(args.apply).with_name("work.json")
        verdicts = {v.repo.lower(): check(v, meta) for v in
                    Verdicts.model_validate_json(Path(args.apply).read_text(encoding="utf-8")).items}
        # 优先用 --export 时保存的候选（含完整元数据）；找不到时只按 verdicts 收录，元数据留给 refresh 回填
        candidates = (json.loads(work_file.read_text(encoding="utf-8"))["raw"] if work_file.exists()
                      else [{"repo": v.repo} for v in verdicts.values()])
    else:
        cfg = yaml.safe_load(SOURCES_FILE.read_text(encoding="utf-8"))
        cutoff = (date.today() - timedelta(days=cfg["seen_ttl_days"])).isoformat()
        skip = {p["repo"].lower() for p in projects} | {k for k, s in seen.items() if s["at"] >= cutoff}
        candidates = collect(cfg, skip)
        print(f"候选 {len(candidates)} 个")
        if args.dry_run:
            for d in candidates:
                print(f"  {d['full_name']:<50} ⭐{d['stargazers_count']:<7} {(d.get('description') or '')[:60]}")
            return
        inputs = [to_candidate(d, gh.readme(d["full_name"])) for d in candidates]
        if args.export:
            Path(args.export).write_text(json.dumps({
                "instructions": system_prompt(meta),
                "output_format": '写一个 JSON 文件：{"items": [{"repo", "relevant", "category", "kind", "why", "reason"}, ...]}，每个候选一条',
                "candidates": inputs,
                "raw": candidates,
            }, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
            print(f"已写出 {args.export}")
            return
        verdicts = classify(inputs, meta)

    added, rejected = apply(candidates, verdicts, meta, projects, seen)
    save_projects(projects, meta)
    save_seen(seen)
    summary = summarize(len(verdicts), added, rejected, meta)
    print(summary)
    if args.summary:
        Path(args.summary).write_text(summary + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
