# research-wiki

[English](./README.md) | 中文

`research-wiki` 是一个独立的 Claude Code skill，用于维护持久化科研知识库，覆盖论文、想法、实验、主张以及它们之间的有类型关系。它的目标是把研究上下文沉淀下来，避免每个 session 都重新搭一遍同一张领域地图。

当你希望 Claude 初始化、查询或更新项目级 research wiki 时，可以使用 `research-wiki` skill：

```text
使用 research-wiki skill 为本项目初始化一个 research wiki，并导入我们之前讨论过的 arXiv 论文。
```

查询时可以这样说：

```text
使用 research-wiki skill 总结当前 research-wiki/ 目录里最重要的 gap 和失败想法。
```

## 工作流程

1. Claude 在当前项目中初始化或复用已有的 `research-wiki/` 目录。
2. Claude 把论文、想法、实验和主张分别保存为 Markdown 页面。
3. Claude 把关系保存在 `graph/edges.jsonl`，并从图自动重建紧凑视图。
4. Claude 使用随 skill 打包的 `research_wiki.py` 辅助脚本（在 `SKILL.md` 中通过 `${CLAUDE_SKILL_DIR}` 解析路径），负责初始化、论文导入、边更新、索引重建、query pack 生成和同步。
5. Claude 可以运行 `verify_wiki_coverage.sh` 做非阻塞的本地诊断。

## 输出

- 项目中的持久化 `research-wiki/` 目录。
- 论文、想法、实验和主张页面。
- `index.md`、`log.md`、`gap_map.md`、`query_pack.md` 和 `graph/edges.jsonl`。
- 可选的论文导入覆盖率诊断结果。

## 辅助脚本

- [research-wiki/scripts/research_wiki.py](./research-wiki/scripts/research_wiki.py)：wiki 变更和重建操作的辅助脚本。
- [research-wiki/scripts/verify_wiki_coverage.sh](./research-wiki/scripts/verify_wiki_coverage.sh)：非阻塞覆盖率诊断脚本。

## 可安装目录

真正可安装的 Claude skill 是：

```text
research-wiki/research-wiki/
```

不要安装外层 `research-wiki/` 文件夹。外层只放这个仓库的说明文档。

## 内容

- `research-wiki/SKILL.md`：持久化 research wiki 工作流。
- `research-wiki/scripts/`：确定性的 wiki 辅助脚本。

## 安装

```bash
cp -r research-wiki/research-wiki/* ~/.claude/skills/research-wiki/
```

之后就可以用 `/research-wiki` 调用。
