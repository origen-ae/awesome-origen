"""输入 GitHub 链接，自动分类后收录。

用法：
  python scripts/add.py https://github.com/a/b https://github.com/c/d
  python scripts/add.py "任意文本，里面的 GitHub 链接都会被识别"
  python scripts/add.py a/b --category vlm/models --kind frontier --why "..." --why-zh "..."   # 全部手工指定时不调用模型
参数：
  --why / --why-zh  覆盖模型写的英文 / 中文"为什么关注"（只在添加单个项目时使用）
  --summary  把结果写成 Markdown，供 PR 描述或 issue 评论使用
  --issue    输入是"推荐项目" issue 表单的正文：从"项目链接"一节取链接，从"为什么关注"一节取说明（含中文则作为 why_zh，否则作为 why）
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
    get = lambda *keys: next((v.strip() for k, v in sections.items() if any(x in k for x in keys)), "")
    why = get("为什么关注", "Why")
    return get("项目链接", "Project links") or body, (None if why in ("", "_No response_") else why)


def has_cjk(text):
    return any("\u4e00" <= ch <= "\u9fff" for ch in text)


def candidates(fetched, args, to_candidate):
    """整理分类输入；只加一个项目且用户写了说明时，附上 user_note，让模型以它为准并补齐另一种语言。"""
    out = [to_candidate(d, gh.readme(d["full_name"])) for d in fetched]
    note = args.why or args.why_zh
    if len(out) == 1 and note:
        out[0]["user_note"] = note
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--category")
    ap.add_argument("--kind", choices=["frontier", "practice", "tool"])
    ap.add_argument("--why")
    ap.add_argument("--why-zh")
    ap.add_argument("--summary")
    ap.add_argument("--issue", action="store_true")
    ap.add_argument("--export")
    ap.add_argument("--apply")
    args = ap.parse_args()
    if args.issue:
        links, note = parse_issue_form("\n".join(args.inputs))
        args.inputs = [links]
        if note:  # 用户写的说明按语言放进 why_zh 或 why，另一种语言由模型补齐
            if has_cjk(note):
                args.why_zh = args.why_zh or note
            else:
                args.why = args.why or note

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

    manual = args.category and args.kind and args.why and args.why_zh
    if fetched and args.export:
        from classify import OUTPUT_FORMAT, system_prompt, to_candidate
        Path(args.export).write_text(json.dumps({
            "instructions": system_prompt(meta) + "\n\n这些链接是用户主动推荐的，除非明显和收录方向无关，否则应判为相关。",
            "output_format": OUTPUT_FORMAT,
            "candidates": candidates(fetched, args, to_candidate),
        }, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
        print("\n".join(lines + [f"已写出 {args.export}（{len(fetched)} 个待判断）"]))
        return
    if fetched and args.apply:
        from classify import Verdicts, check
        verdicts = {v.repo.lower(): check(v, meta) for v in
                    Verdicts.model_validate_json(Path(args.apply).read_text(encoding="utf-8")).items}
    elif fetched and not manual:
        from classify import classify, to_candidate
        verdicts = classify(candidates(fetched, args, to_candidate), meta)
    else:
        verdicts = {}

    added = []
    for d in fetched:
        name = d["full_name"]
        v = verdicts.get(name.lower())
        category = args.category or (v.category if v else "")
        kind = args.kind or (v.kind if v else None)
        single = len(fetched) == 1
        why = (args.why if single else None) or (v.why if v else None)
        why_zh = (args.why_zh if single else None) or (v.why_zh if v else None)
        if v and not v.relevant and not args.category:
            lines.append(f"- 🚫 `{name}`：模型判断不在收录方向内（{v.reason}）；确实需要收录的话，用 --category / --kind / --why / --why-zh 手工指定")
            continue
        if category not in meta["index"] or not kind or not why or not why_zh:
            lines.append(f"- ❓ `{name}`：无法自动分类（{v.reason if v else '模型未返回结果'}），请用 --category / --kind / --why / --why-zh 手工指定")
            continue
        p = {"repo": name, "category": category, "kind": kind, "ring": "assess", "why": why,
             "why_zh": why_zh, "added_at": gh.today(), "source": "manual"}
        gh.apply_meta(p, d)
        projects.append(p)
        added.append(p)
        top, sub = meta["index"][category]
        warn = f"\n  - ⚠️ 模型认为相关性不足：{v.reason}" if v and not v.relevant else ""
        lines.append(f"- ✅ [{name}](https://github.com/{name}) → **{top['name']} / {sub['name']}** · "
                     f"{meta['kinds'][kind]['name']} · {why}｜{why_zh}{warn}")

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
