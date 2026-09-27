"""每日任务（无需 Claude 管理员权限的 routine 替代方案）：处理推荐 issue；周一额外做定时发现；有变化时开 PR。

本机（Windows 计划任务）或 GitHub Actions 都可以运行：
  python scripts/daily.py              # 周一自动包含发现
  python scripts/daily.py --discover   # 强制执行发现
  python scripts/daily.py --dry-run    # 只处理、不推送不开 PR（改动留在工作区，便于检查）
分类用 classify.py 的后端：有 ANTHROPIC_API_KEY 走 API，否则调用本机 `claude -p`（Team 订阅）。
GitHub token：环境变量 GITHUB_TOKEN；本机没有时从 git 凭证管理器读取 levin-zhou 的凭证。
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request
from datetime import datetime
from pathlib import Path

from lib import ROOT

REPO = os.environ.get("CURATE_REPO", "origen-ae/awesome-origen")
GIT_USER = os.environ.get("CURATE_GIT_USER", "levin-zhou")
PATHS = ["data/", "README.md", "README.zh-CN.md", "docs/"]


def run(*cmd, check=True, **kw):
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", **kw)
    if check and r.returncode != 0:
        sys.exit(f"命令失败：{' '.join(cmd)}\n{r.stdout}\n{r.stderr}")
    return r


def github_token():
    if os.environ.get("GITHUB_TOKEN"):
        return os.environ["GITHUB_TOKEN"]
    r = subprocess.run(["git", "credential", "fill"], input=f"protocol=https\nhost=github.com\nusername={GIT_USER}\n\n",
                       capture_output=True, text=True, env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
    m = re.search(r"^password=(.+)$", r.stdout, re.M)
    if not m:
        sys.exit("找不到 GitHub token：请设置 GITHUB_TOKEN，或先用 git credential-manager github login 登录")
    return m.group(1).strip()


def api(method, path, token, body=None):
    req = urllib.request.Request(f"https://api.github.com{path}", method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
                                          "User-Agent": "origen-ae-daily", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp) if resp.length != 0 else None


def pending_in_open_prs(token):
    """已被尚未合并的机器人 PR 处理过的 issue，避免重复处理。"""
    nums = set()
    for pr in api("GET", f"/repos/{REPO}/pulls?state=open&per_page=50", token):
        if pr["head"]["ref"].startswith("bot/curate-"):
            nums |= {int(n) for n in re.findall(r"Closes #(\d+)", pr.get("body") or "")}
    return nums


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--discover", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    os.environ["GITHUB_TOKEN"] = token = github_token()  # 子进程（add.py / discover.py）调 GitHub API 也用它

    if run("git", "status", "--porcelain", "--", *PATHS).stdout.strip():
        sys.exit("data/、README 或 docs/ 有未提交的改动，先处理干净再运行")
    run("git", "checkout", "-q", "main")
    run("git", "pull", "-q", "--ff-only")

    tmp = Path(tempfile.mkdtemp(prefix="curate-"))
    sections, closes, no_change = [], [], []

    skip = pending_in_open_prs(token)
    issues = [i for i in api("GET", f"/repos/{REPO}/issues?labels=add-project&state=open&per_page=50", token)
              if "pull_request" not in i and i["number"] not in skip]
    for i in issues:
        out = tmp / f"issue-{i['number']}.md"
        r = run(sys.executable, "scripts/add.py", "--issue", "--summary", str(out), i["body"] or "", check=False)
        summary = out.read_text(encoding="utf-8").strip() if out.exists() else (r.stdout + r.stderr).strip()
        print(f"#{i['number']} exit={r.returncode}\n{summary}")
        if r.returncode == 0:
            sections.append(f"### #{i['number']}\n\n{summary}")
            closes.append(i["number"])
        elif r.returncode == 2:
            no_change.append((i["number"], summary))
        else:
            print(f"[跳过] #{i['number']} 处理出错，下次再试", file=sys.stderr)

    if args.discover or datetime.now().weekday() == 0:
        out = tmp / "discover.md"
        run(sys.executable, "scripts/discover.py", "--summary", str(out))
        if out.exists():
            sections.append("### Weekly discovery / 每周发现\n\n" + out.read_text(encoding="utf-8").strip())

    changed = run("git", "status", "--porcelain", "--", "data/").stdout.strip()
    if changed:
        run(sys.executable, "scripts/render.py")

    if args.dry_run:
        print("\n[dry-run] 不推送、不开 PR；改动保留在工作区")
        return

    for num, summary in no_change:  # 没有可收录内容的 issue：说明原因后关闭
        api("POST", f"/repos/{REPO}/issues/{num}/comments", token,
            {"body": f"{summary}\n\nNothing new to add, closing this issue. 没有新增项目，关闭此 issue。"})
        api("PATCH", f"/repos/{REPO}/issues/{num}", token, {"state": "closed", "state_reason": "not_planned"})

    if not changed:
        print("今日无新增")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    branch = f"bot/curate-{datetime.now():%Y%m%d-%H%M}"
    run("git", "checkout", "-q", "-b", branch)
    run("git", "add", "--", *PATHS)
    run("git", "-c", "user.name=origen-curate-bot", "-c", "user.email=levin.zhou@origen.ae",
        "commit", "-q", "-m", f"curate: {today}\n\nCo-Authored-By: Claude <noreply@anthropic.com>")
    run("git", "push", "-q", "-u", "origin", branch, env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
    run("git", "checkout", "-q", "main")

    added = run("git", "diff", "--numstat", f"main...{branch}", "--", "data/projects.yaml").stdout.split()
    n_added = int(added[0]) - int(added[1]) if len(added) >= 2 else 0
    body = "\n\n".join(sections + [
        "Review: delete any unwanted line in `data/projects.yaml`, run `python scripts/render.py`, then commit. "
        "审阅方式：不想要的项目，删掉 projects.yaml 中对应的行，运行 render.py 后提交。",
        "\n".join(f"Closes #{n}" for n in closes),
        "🤖 Generated with [Claude Code](https://claude.com/claude-code)",
    ]).strip()
    pr = api("POST", f"/repos/{REPO}/pulls", token,
             {"title": f"curate: {today} 收录 {max(n_added, 0)} 个项目 / add {max(n_added, 0)} projects",
              "head": branch, "base": "main", "body": body})
    print(f"已创建 PR：{pr['html_url']}")


if __name__ == "__main__":
    main()
