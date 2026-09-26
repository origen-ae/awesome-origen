"""从 GitHub API 回填 stars / 最近推送 / 归档状态等元数据。

用法：
  python scripts/refresh.py                 # 刷新全部
  python scripts/refresh.py --only a/b c/d  # 只刷新指定仓库
环境变量 GITHUB_TOKEN 可选；不设置时匿名访问，每小时限 60 次请求。
"""
import argparse
import sys

import gh
from lib import load_meta, load_projects, save_projects


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="只刷新这些仓库")
    args = ap.parse_args()

    meta, projects = load_meta(), load_projects()
    only = {r.lower() for r in args.only} if args.only else None
    updated = failed = 0

    for p in projects:
        if only and p["repo"].lower() not in only:
            continue
        try:
            d = gh.repo(p["repo"])
        except gh.RateLimited:
            print(f"[限流] 在 {p['repo']} 处停止，已完成 {updated} 个；请设置 GITHUB_TOKEN", file=sys.stderr)
            break
        if d is None:
            p["missing"] = True
            print(f"[404] {p['repo']} 已不存在或转为私有", file=sys.stderr)
            failed += 1
            continue
        if d["full_name"] != p["repo"]:  # 仓库改名或转移后 API 会跟随重定向
            print(f"[改名] {p['repo']} -> {d['full_name']}")
        gh.apply_meta(p, d)
        updated += 1

    save_projects(projects, meta)
    print(f"刷新完成：{updated} 个成功，{failed} 个失效")


if __name__ == "__main__":
    main()
