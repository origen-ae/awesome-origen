"""数据读写与校验的公共逻辑。"""
import sys
from datetime import date
from pathlib import Path

import yaml

# Windows 控制台默认 GBK，统一输出 UTF-8
sys.stdout.reconfigure(encoding="utf-8", newline="\n")
sys.stderr.reconfigure(encoding="utf-8", newline="\n")

ROOT = Path(__file__).resolve().parent.parent
CATEGORIES_FILE = ROOT / "data" / "categories.yaml"
PROJECTS_FILE = ROOT / "data" / "projects.yaml"

REQUIRED = ("repo", "category", "kind", "ring", "why")
# 人工维护字段在前，脚本回填字段在后
FIELD_ORDER = ("repo", "category", "kind", "ring", "why", "tags", "added_at", "source",
               "stars", "pushed_at", "language", "license", "archived", "missing", "desc")


def load_meta():
    meta = yaml.safe_load(CATEGORIES_FILE.read_text(encoding="utf-8"))
    # "一级/二级" -> (一级分类, 二级分类)
    meta["index"] = {
        f"{top['id']}/{sub['id']}": (top, sub)
        for top in meta["categories"] for sub in top.get("children", [])
    }
    return meta


def load_yaml_list(path):
    """读取列表型 YAML；YAML 会把 2026-01-01 解析成 date，这里统一转回字符串。"""
    items = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    for it in items:
        for k, v in it.items():
            if isinstance(v, date):
                it[k] = v.isoformat()
    return items


def load_projects():
    return load_yaml_list(PROJECTS_FILE)


def validate(projects, meta):
    errors, seen = [], {}
    for i, p in enumerate(projects, 1):
        where = f"#{i} {p.get('repo', '?')}"
        for f in REQUIRED:
            if not p.get(f):
                errors.append(f"{where}: 缺少字段 {f}")
        if p.get("category") and p["category"] not in meta["index"]:
            errors.append(f"{where}: 未定义的分类 {p['category']}（见 categories.yaml）")
        if p.get("kind") and p["kind"] not in meta["kinds"]:
            errors.append(f"{where}: kind 只能是 {list(meta['kinds'])}")
        if p.get("ring") and p["ring"] not in meta["rings"]:
            errors.append(f"{where}: ring 只能是 {list(meta['rings'])}")
        key = str(p.get("repo", "")).lower()
        if key in seen:
            errors.append(f"{where}: 与 #{seen[key]} 重复")
        seen[key] = i
    return errors


def save_projects(projects, meta):
    """按 categories.yaml 的顺序分组写回，每个项目一行，分组间空一行，便于 diff 与审阅。"""
    order = {cid: n for n, cid in enumerate(meta["index"])}
    projects = sorted(projects, key=lambda p: order.get(p.get("category"), len(order)))  # 稳定排序，组内保持原顺序
    lines, last_top = [], None
    for p in projects:
        top = str(p.get("category", "")).split("/")[0]
        if last_top is not None and top != last_top:
            lines.append("")
        last_top = top
        item = {k: p[k] for k in FIELD_ORDER if k in p and p[k] is not None}
        item.update({k: v for k, v in p.items() if k not in item and v is not None})
        lines.append(yaml.safe_dump([item], default_flow_style=None, allow_unicode=True,
                                    sort_keys=False, width=100000).rstrip())
    PROJECTS_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
