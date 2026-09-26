# Contributing

[简体中文](CONTRIBUTING.zh-CN.md)

## Adding a project

**Easiest:** open an issue in this repo with the **Recommend a project / 推荐项目** template and paste GitHub links. A scheduled job processes these daily: it categorizes the projects and opens a PR, and the issue closes automatically when the PR is merged.

**Locally:** open Claude Code in this repo and run `/curate add https://github.com/owner/repo`. It checks for duplicates, categorizes, writes the English and Chinese descriptions, fills in metadata and regenerates the README.

**By hand:**

1. Append a line to `data/projects.yaml`:
   ```yaml
   - {repo: owner/name, category: top/child, kind: tool, ring: assess, why: Why we care in English, why_zh: 中文说明, added_at: 2026-09-26}
   ```
   - Valid `category` values are listed in `data/categories.yaml`
   - `kind`: `frontier` / `practice` / `tool`
   - `ring`: always `assess` for new projects; change to `trial` / `adopt` once the team has actually used it
   - `why` is English, `why_zh` is Chinese; both are required
2. Run `pip install -r requirements.txt`, then:
   ```
   python scripts/refresh.py --only owner/name
   python scripts/render.py
   ```
3. Commit `data/`, `README*.md` and `docs/`, then open a PR. CI validates the data and checks that the README was regenerated.

## Inclusion criteria

- Relevant to our focus areas: frontier technologies, engineering practices, tools
- The description states our own judgment, not the project's tagline. Keep it to 12 English words and 30 Chinese characters
- Don't fork projects into the org. Fork or mirror only when we modify the code, contribute upstream, or need a backup of a production dependency

## Changing categories

Edit `data/categories.yaml`. Every category needs English (`name` / `desc`) and Chinese (`name_zh` / `desc_zh`) text. Keep top-level categories to 8 or fewer. When renaming a category id, update the projects in projects.yaml that reference it.

## Automation

| Job | When | What it does |
|---|---|---|
| Claude Code routine (`/curate routine`) | Daily | Processes recommendation issues; on Mondays also discovers new projects via `data/sources.yaml`; opens a PR when something changed |
| `refresh` workflow | Mondays | Refreshes stars, activity and archived status |
| `validate` workflow | PR / push | Validates data and checks the README is regenerated |

The `discover` and `add-from-issue` workflows are disabled by default. You can enable them as an alternative to the routine once the `ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN` secret is configured.
