"""输入 GitHub 链接，自动分类后收录。

用法：
  python scripts/add.py https://github.com/a/b https://github.com/c/d
  python scripts/add.py "任意文本，里面的 GitHub 链接都会被识别"
  python scripts/add.py a/b --category vlm/models --kind frontier --why "..."   # 全部手工指定时不调用模型
参数：
  --why      覆盖模型写的"为什么关注"（只在添加单个项目时使用）
  --summary  把结果写成 Markdown，供 PR 描述或 issue 评论使用
  --issue    输入是"推荐项目" issue 表单的正文：从"项目链接"一节取链接，从"为什么关注"一节取 why
Agent 模式（由会话里的 Claude 自己判断，不再调用模型；格式与 discover.py 相同）：
  --export work.json      写出评审标准和候选资料后退出
  --apply verdicts.json   用 verdicts.json 里的判断代替模型调用
退出码：有新增为 0；没有任何新增为 2。
"""
import argparse
import json
import re
import sys
from pathlib import Path

import gh
from lib import load_meta, load_projects, save_projects, validate


def parse_issue_form(body):
    """issue 表单正文由若干 "### 标题" 小节组成，未填写的字段内容为 _No response_。"""
    sections = dict(re.findall(r"^###\s*(.+?)\s*\n(.*?)(?=^###|\Z)", body, re.M | re.S))
    get = lambda prefix: next((v.strip() for k, v in sections.items() if k.startswith(prefix)), "")
    why = get("为什么关注")
    return get("项目链接") or body, (None if why in ("", "_No response_") else why)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--category")
    ap.add_argument("--kind", choices=["frontier", "practice", "tool"])
    ap.add_argument("--why")
    ap.add_argument("--summary")
    ap.add_argument("--issue", action="store_true")
    ap.add_argument("--export")
    ap.add_argument("--apply")
    args = ap.parse_args()
    if args.issue:
        links, why = parse_issue_form("\n".join(args.inputs))
        args.inputs, args.why = [links], args.why or why

    meta, projects = load_meta(), load_projects()
    existing = {p["repo"].lower(): p for p in projects}

    repos = []
    for text in args.inputs:
        found = [f"{o}/{n.removesuffix('.git')}" for o, n in gh.REPO_RE.findall(text)] or [gh.parse_repo(text)]
        repos += [r for r in found if r and r.lower() not in {x.lower() for x in repos}]
    if not repos:
        print("没有识别到 GitHub 仓库链接", file=sys.stderr)
        sys.exit(2)

    lines, fetched = [], []
    for r in repos:
        d = gh.repo(r)
        if d is None:
            lines.append(f"- ❌ `{r}`：仓库不存在或是私有仓库")
        elif d["full_name"].lower() in existing:
            p = existing[d["full_name"].lower()]
            lines.append(f"- ⏭ [{d['full_name']}](https://github.com/{d['full_name']})：已收录在 `{p['category']}`")
        else:
            fetched.append(d)

    manual = args.category and args.kind and args.why
    if fetched and args.export:
        from classify import system_prompt, to_candidate
        Path(args.export).write_text(json.dumps({
            "instructions": system_prompt(meta) + "\n\n这些链接是用户主动推荐的，除非明显和收录方向无关，否则应判为相关。",
            "output_format": '写一个 JSON 文件：{"items": [{"repo", "relevant", "category", "kind", "why", "reason"}, ...]}，每个候选一条',
            "candidates": [to_candidate(d, gh.readme(d["full_name"])) for d in fetched],
        }, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
        print("\n".join(lines + [f"已写出 {args.export}（{len(fetched)} 个待判断）"]))
        return
    if fetched and args.apply:
        from classify import Verdicts, check
        verdicts = {v.repo.lower(): check(v, meta) for v in
                    Verdicts.model_validate_json(Path(args.apply).read_text(encoding="utf-8")).items}
    elif fetched and not manual:
        from classify import classify, to_candidate
        verdicts = classify([to_candidate(d, gh.readme(d["full_name"])) for d in fetched], meta)
    else:
        verdicts = {}

    added = []
    for d in fetched:
        name = d["full_name"]
        v = verdicts.get(name.lower())
        category = args.category or (v.category if v else "")
        kind = args.kind or (v.kind if v else None)
        why = (args.why if len(fetched) == 1 else None) or (v.why if v else None)
        if v and not v.relevant and not args.category:
            lines.append(f"- 🚫 `{name}`：模型判断不在收录方向内（{v.reason}）；确实需要收录的话，用 --category / --kind / --why 手工指定")
            continue
        if category not in meta["index"] or not kind or not why:
            lines.append(f"- ❓ `{name}`：无法自动分类（{v.reason if v else '模型未返回结果'}），请用 --category / --kind / --why 手工指定")
            continue
        p = {"repo": name, "category": category, "kind": kind, "ring": "assess", "why": why,
             "added_at": gh.today(), "source": "manual"}
        gh.apply_meta(p, d)
        projects.append(p)
        added.append(p)
        top, sub = meta["index"][category]
        warn = f"\n  - ⚠️ 模型认为相关性不足：{v.reason}" if v and not v.relevant else ""
        lines.append(f"- ✅ [{name}](https://github.com/{name}) → **{top['name']} / {sub['name']}** · "
                     f"{meta['kinds'][kind]['name']} · {why}{warn}")

    errors = validate(projects, meta)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)
    if added:
        save_projects(projects, meta)

    summary = "\n".join(lines)
    print(summary)
    if args.summary:
        Path(args.summary).write_text(summary + "\n", encoding="utf-8", newline="\n")
    sys.exit(0 if added else 2)


if __name__ == "__main__":
    main()
