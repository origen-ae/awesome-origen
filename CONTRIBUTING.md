# 贡献指南

## 添加项目

**最简单的做法**：在本仓库新建 issue，选择 **推荐项目** 模板，贴上 GitHub 链接。机器人会自动分类收录：组织成员提交的直接进入 main，其他人提交的会开 PR 等待审核。

**本地做法**：在本仓库中打开 Claude Code，执行 `/curate add https://github.com/owner/repo`，它会自动完成分类、查重、回填数据和生成 README。

**手工做法**：

1. 在 `data/projects.yaml` 末尾追加一行：
   ```yaml
   - {repo: owner/name, category: 一级/二级, kind: tool, ring: assess, why: 我们为什么关注它, added_at: 2026-09-26}
   ```
   - `category` 的可选值见 `data/categories.yaml`
   - `kind`：`frontier` 前沿 / `practice` 实践 / `tool` 工具
   - `ring`：新项目一律填 `assess`；团队实际用过后再改为 `trial` / `adopt`
2. 运行 `pip install -r requirements.txt`，然后：
   ```
   python scripts/refresh.py --only owner/name
   python scripts/render.py
   ```
3. 提交 `data/`、`README.md`、`docs/` 并开 PR。CI 会校验数据，并检查 README 是否已重新生成。

## 收录标准

- 与我们的方向相关：前沿技术、工程实践、工具
- `why` 要写出我们自己的判断，不要照抄项目简介
- 不 fork 到组织里。只有需要二次开发、要给上游提 PR，或者需要备份生产依赖时才 fork 或 mirror

## 修改分类

编辑 `data/categories.yaml`。一级分类尽量不超过 8 个。给已有分类改 id 时，要同步修改 projects.yaml 中引用它的项目。

## 自动化一览

| Workflow | 触发时机 | 作用 |
|---|---|---|
| `add-from-issue` | 提交"推荐项目" issue，或手动运行 | 链接 → 模型分类 → 收录 |
| `discover` | 每周一 | 按 `data/sources.yaml` 搜索 → 模型筛选 → 开 PR，合并即表示接受 |
| `refresh` | 每周一 | 刷新 stars、活跃度、归档状态 |
| `validate` | PR / push | 校验数据，并检查 README 是否已重新生成 |

需要在仓库的 Settings → Secrets 中配置 `ANTHROPIC_API_KEY`。
