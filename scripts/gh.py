"""GitHub REST API 的最小封装（仅用标准库）。环境变量 GITHUB_TOKEN 可选。"""
import base64
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import date

API = "https://api.github.com"
REPO_RE = re.compile(r"github\.com/([\w.-]+)/([\w.-]+)", re.I)


class RateLimited(Exception):
    pass


def _get(path, params=None):
    url = API + path + ("?" + urllib.parse.urlencode(params) if params else "")
    token = os.environ.get("GITHUB_TOKEN")
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "origen-ae-awesome",
        **({"Authorization": f"Bearer {token}"} if token else {}),
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        if e.code in (403, 429):
            raise RateLimited(path) from e
        raise


def parse_repo(text):
    """从 URL 或 owner/name 中解析出 owner/name。"""
    m = REPO_RE.search(text)
    if m:
        owner, name = m.groups()
    elif re.fullmatch(r"[\w.-]+/[\w.-]+", text.strip()):
        owner, name = text.strip().split("/")
    else:
        return None
    return f"{owner}/{name.removesuffix('.git')}"


def repo(full_name):
    """返回仓库信息；仓库不存在时返回 None。"""
    try:
        return _get(f"/repos/{full_name}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def readme(full_name, limit=4000):
    """README 前 limit 个字符，用作分类依据；没有 README 时返回空字符串。"""
    try:
        d = _get(f"/repos/{full_name}/readme")
    except urllib.error.HTTPError:
        return ""
    return base64.b64decode(d["content"]).decode("utf-8", "replace")[:limit]


def search(query, per_page=10):
    return _get("/search/repositories", {"q": query, "sort": "stars", "order": "desc", "per_page": per_page})["items"]


def apply_meta(p, d):
    """把 API 返回的仓库信息写入项目记录的自动字段。"""
    p["repo"] = d["full_name"]
    p.pop("missing", None)
    p["stars"] = d["stargazers_count"]
    p["pushed_at"] = d["pushed_at"][:10]
    p["language"] = d.get("language")
    p["license"] = (d.get("license") or {}).get("spdx_id")
    p["archived"] = d["archived"] or None  # 只在归档时写出该字段
    p["desc"] = d.get("description")


def today():
    return date.today().isoformat()
