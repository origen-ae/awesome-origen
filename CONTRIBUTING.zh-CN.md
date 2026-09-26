# 贡献指南

[English](CONTRIBUTING.md)

## 添加项目

**最简单的做法**：在本仓库新建 issue，选择 **Recommend a project / 推荐项目** 模板，贴上 GitHub 链接。定时任务每天会处理一次：自动分类后开 PR，PR 合并后 issue 会自动关闭。

**本地做法**：在本仓库中打开 Claude Code，执行 `/curate add https://github.com/owner/repo`。它会自动查重、分类，生成中英文说明，回填数据并重新生成 README。

**手工做法**：

1. 在 `data/projects.yaml` 末尾追加一行：
   ```yaml
   - {repo: owner/name, category: 一级/二级, kind: tool, ring: assess, why: Why we care in English, why_zh: 我们为什么关注它, added_at: 2026-09-26}
   ```
   - `category` 的可选值见 `data/categories.yaml`
   - `kind`：`frontier` 前沿 / `practice` 实践 / `tool` 工具
   - `ring`：新项目一律填 `assess`；团队实际用过后再改为 `trial` / `adopt`
   - `why` 写英文，`why_zh` 写中文，两者都必填
2. 运行 `pip install -r requirements.txt`，然后：
   ```
   python scripts/refresh.py --only owner/name
   python scripts/render.py
   ```
3. 提交 `data/`、`README*.md`、`docs/` 并开 PR。CI 会校验数据，并检查 README 是否已重新生成。

## 收录标准

- 与我们的方向相关：前沿技术、工程实践、工具
- 说明要写出我们自己的判断，不要照抄项目简介。中文不超过 30 个字，英文不超过 12 个词
- 不 fork 到组织里。只有需要二次开发、要给上游提 PR，或者需要备份生产依赖时才 fork 或 mirror

## 修改分类

编辑 `data/categories.yaml`，每个分类都要填英文（`name` / `desc`）和中文（`name_zh` / `desc_zh`）。一级分类尽量不超过 8 个。给已有分类改 id 时，要同步修改 projects.yaml 中引用它的项目。

## 自动化

| 任务 | 时间 | 作用 |
|---|---|---|
| Claude Code 定时任务（`/curate routine`） | 每天 | 处理推荐 issue；周一额外按 `data/sources.yaml` 发现新项目；有变化时开 PR |
| `refresh` workflow | 每周一 | 刷新 stars、活跃度、归档状态 |
| `validate` workflow | PR / push | 校验数据，并检查 README 是否已重新生成 |

`discover` 和 `add-from-issue` 两个 workflow 默认是禁用的。配置了 `ANTHROPIC_API_KEY` 或 `CLAUDE_CODE_OAUTH_TOKEN` 这两个 secret 之后可以启用，作为定时任务的替代方案。
