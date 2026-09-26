"""由 data/*.yaml 生成 README.md 与 docs/ 下的按类型、按雷达视图。

用法：
  python scripts/render.py          # 校验并生成
  python scripts/render.py --check  # 只校验，并检查生成结果是否已提交（CI 用）
"""
import argparse
import sys
from datetime import date, timedelta

from lib import ROOT, load_meta, load_projects, validate

STALE_DAYS = 365
RING_ORDER = ("adopt", "trial", "assess", "hold")


def fmt_stars(n):
    if n is None:
        return "-"
    return f"{n / 1000:.1f}k" if n >= 1000 else str(n)


def row(p, meta, show_category=False, link_prefix=""):
    flags = ""
    if p.get("archived"):
        flags += " ⚠️已归档"
    if p.get("missing"):
        flags += " ❌失效"
    elif p.get("pushed_at") and date.fromisoformat(p["pushed_at"]) < date.today() - timedelta(days=STALE_DAYS):
        flags += " 💤一年未更新"
    kind = meta["kinds"][p["kind"]]
    cells = [f"[{p['repo']}](https://github.com/{p['repo']}){flags}"]
    if show_category:
        top, sub = meta["index"][p["category"]]
        cells.append(f"{top['name']} / {sub['name']}")
    cells += [f"{kind['emoji']} {kind['name']}", meta["rings"][p["ring"]]["name"], p["why"],
              fmt_stars(p.get("stars")), p.get("pushed_at") or "-"]
    return "| " + " | ".join(c.replace("|", "\\|") for c in cells) + " |"


def sort_key(p):
    return (RING_ORDER.index(p["ring"]), -(p.get("stars") or 0))


def table(items, meta, show_category=False):
    head = ["项目"] + (["分类"] if show_category else []) + ["类型", "雷达", "为什么关注", "⭐", "最近推送"]
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += [row(p, meta, show_category) for p in sorted(items, key=sort_key)]
    return "\n".join(out)


def legend(meta):
    kinds = " · ".join(f"{k['emoji']} **{k['name']}**：{k['desc']}" for k in meta["kinds"].values())
    rings = " · ".join(f"**{r['name']}**（{rid}）：{r['desc']}" for rid, r in meta["rings"].items())
    return f"- 类型：{kinds}\n- 雷达：{rings}"


def render_readme(projects, meta):
    by_cat = {}
    for p in projects:
        by_cat.setdefault(p["category"], []).append(p)
    counts = {k: sum(p["kind"] == k for p in projects) for k in meta["kinds"]}

    out = [
        "<!-- 本文件由 scripts/render.py 自动生成，请修改 data/*.yaml，不要直接编辑 -->",
        "# Awesome Origen",
        "",
        "Origen 关注的前沿技术、工程实践与工具精选。每一项都写明了**我们为什么关注它**，并用技术雷达标注团队态度。",
        "",
        f"共 **{len(projects)}** 个项目：" + " · ".join(
            f"[{meta['kinds'][k]['emoji']} {meta['kinds'][k]['name']} {n}](docs/{k}.md)" for k, n in counts.items()
        ) + " · [🎯 按雷达查看](docs/radar.md)",
        "",
        legend(meta),
        "",
        "## 目录",
        "",
    ]
    for top in meta["categories"]:
        n = sum(len(by_cat.get(f"{top['id']}/{s['id']}", [])) for s in top["children"])
        out.append(f"- [{top['name']}](#{top['id']})（{n}）— {top['desc']}")
    for top in meta["categories"]:
        out += ["", f'<a id="{top["id"]}"></a>', "", f"## {top['name']}", "", f"> {top['desc']}"]
        for sub in top["children"]:
            items = by_cat.get(f"{top['id']}/{sub['id']}")
            if items:
                out += ["", f"### {sub['name']}", "", table(items, meta)]
    out += ["", "## 贡献", "", "见 [CONTRIBUTING.md](CONTRIBUTING.md)。推荐在本仓库中使用 Claude Code 的 `/curate add <url>` 添加项目。", ""]
    return "\n".join(out)


def render_view(title, groups, meta):
    out = ["<!-- 自动生成，请勿直接编辑 -->", f"# {title}", "", "[← 返回总览](../README.md)", ""]
    for heading, items in groups:
        if items:
            out += [f"## {heading}（{len(items)}）", "", table(items, meta, show_category=True), ""]
    return "\n".join(out)


def outputs(projects, meta):
    files = {ROOT / "README.md": render_readme(projects, meta)}
    for kid, k in meta["kinds"].items():
        groups = [(r["name"], [p for p in projects if p["kind"] == kid and p["ring"] == rid])
                  for rid, r in meta["rings"].items()]
        files[ROOT / "docs" / f"{kid}.md"] = render_view(f"{k['emoji']} {k['name']}：{k['desc']}", groups, meta)
    groups = [(f"{r['name']}（{rid}）— {r['desc']}", [p for p in projects if p["ring"] == rid])
              for rid, r in meta["rings"].items()]
    files[ROOT / "docs" / "radar.md"] = render_view("🎯 技术雷达", groups, meta)
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    meta, projects = load_meta(), load_projects()
    errors = validate(projects, meta)
    if errors:
        print("数据校验失败：\n  " + "\n  ".join(errors), file=sys.stderr)
        sys.exit(1)

    stale = []
    for path, content in outputs(projects, meta).items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
    if stale:
        print(f"以下文件与数据不一致，请运行 python scripts/render.py 后提交：{stale}", file=sys.stderr)
        sys.exit(1)
    print(f"OK：{len(projects)} 个项目")


if __name__ == "__main__":
    main()
