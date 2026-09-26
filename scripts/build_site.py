"""由 data/*.yaml 生成 GitHub Pages 站点的数据文件 site/data.json（页面本身是 site/index.html）。

用法：python scripts/build_site.py
"""
import json

from lib import ROOT, load_meta, load_projects, validate


def main():
    meta, projects = load_meta(), load_projects()
    errors = validate(projects, meta)
    if errors:
        raise SystemExit("数据校验失败：\n  " + "\n  ".join(errors))

    bi = lambda o, f: {"en": o[f], "zh": o.get(f"{f}_zh") or o[f]}
    data = {
        "areas": [
            {"id": top["id"], "name": bi(top, "name"), "short": bi(top, "short"), "desc": bi(top, "desc"),
             "children": [{"id": f"{top['id']}/{s['id']}", "name": bi(s, "name")} for s in top["children"]]}
            for top in meta["categories"]
        ],
        "kinds": {k: {"name": bi(v, "name"), "desc": bi(v, "desc"), "emoji": v["emoji"]} for k, v in meta["kinds"].items()},
        "rings": {k: {"name": bi(v, "name"), "desc": bi(v, "desc")} for k, v in meta["rings"].items()},
        "projects": [
            {
                "repo": p["repo"], "category": p["category"], "area": p["category"].split("/")[0],
                "kind": p["kind"], "ring": p["ring"], "why": {"en": p["why"], "zh": p["why_zh"]},
                "desc": p.get("desc"), "stars": p.get("stars"), "pushed_at": p.get("pushed_at"),
                "language": p.get("language"), "license": p.get("license"), "added_at": p.get("added_at"),
                "archived": bool(p.get("archived")), "missing": bool(p.get("missing")),
            }
            for p in projects
        ],
    }
    out = ROOT / "site" / "data.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8", newline="\n")
    print(f"已生成 {out.relative_to(ROOT).as_posix()}：{len(projects)} 个项目")


if __name__ == "__main__":
    main()
