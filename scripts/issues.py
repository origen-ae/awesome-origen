"""列出待处理的"推荐项目" issue（open，且带 add-project 标签），输出 JSON，供 routine / 本地 Agent 使用。

用法：python scripts/issues.py [owner/repo]   # 默认 origen-ae/awesome-origen，也可用环境变量 CURATE_REPO 指定
公开仓库匿名即可读取。
"""
import json
import os
import sys

import gh


def main():
    repo = (sys.argv[1] if len(sys.argv) > 1 else None) or os.environ.get("CURATE_REPO", "origen-ae/awesome-origen")
    items = gh._get(f"/repos/{repo}/issues", {"labels": "add-project", "state": "open", "per_page": 50})
    print(json.dumps([
        {"number": i["number"], "author": i["user"]["login"], "association": i["author_association"], "body": i["body"] or ""}
        for i in items if "pull_request" not in i
    ], ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
