# arxiv

[English](./README.md) | 中文

`arxiv` 是一个用于搜索 arXiv、按 arXiv ID 获取论文元数据、并把论文 PDF 下载到本地 paper library 的 Claude Code skill。

当你希望 Claude 查找预印本、根据 arXiv ID 获取 PDF，或者把相关 arXiv 论文保存到 `papers/` 或指定目录时，可以使用 `arxiv` skill：

```text
使用 arxiv skill 搜索近期关于 test-time scaling 的论文，并把最相关的一篇 PDF 下载到 papers/。
```

如果已经知道论文 ID，也可以这样说：

```text
使用 arxiv skill 拉取 2301.07041 并把 PDF 下载到 literature/。
```

## 工作流程

1. Claude 解析查询词、arXiv ID、结果数量、输出目录和下载模式。
2. Claude 运行安装好的 skill 内置脚本 `${CLAUDE_SKILL_DIR}/scripts/arxiv_fetch.py`。路径用 `${CLAUDE_SKILL_DIR}` 变量解析，因此无论装在 `~/.claude/skills/arxiv/` 还是 `.claude/skills/arxiv/` 都能找到。
3. 搜索结果会以结构化元数据返回，包括 arXiv ID、标题、作者、摘要、日期、分类、PDF 链接和 abstract 链接。
4. 如果用户要求下载，PDF 默认保存到 `papers/`，也可以保存到用户指定目录。
5. 如果目标 PDF 已存在，skill 会跳过而不是覆盖；如果下载到的文件过小，会按错误页面处理。

## 输出

- 在对话中打印搜索结果。
- 可选地把下载的 PDF 保存到 `papers/` 或用户指定目录。

这个 skill 不会把搜索日志、调试 JSON 或缓存文件作为任务结果持久化。

## 辅助脚本

- [arxiv/scripts/arxiv_fetch.py](./arxiv/scripts/arxiv_fetch.py)：用于 arXiv Atom API 搜索和 PDF 下载的小型 CLI。

在已安装的 skill 目录内、SKILL.md 中调用时这样写：

```bash
python "${CLAUDE_SKILL_DIR}/scripts/arxiv_fetch.py" search "diffusion policy" --max 10
python "${CLAUDE_SKILL_DIR}/scripts/arxiv_fetch.py" search "id:2301.07041" --max 1
python "${CLAUDE_SKILL_DIR}/scripts/arxiv_fetch.py" download 2301.07041 --dir papers
```

## 仓库结构

- `README.md` 和 `README.zh-CN.md`：仓库说明文档。
- `arxiv/`：可安装的 Claude skill 目录。
- `arxiv/SKILL.md`：Claude skill 定义。
- `arxiv/scripts/`：确定性的辅助脚本。

## 安装

```bash
cp -r arxiv/arxiv/* ~/.claude/skills/arxiv/
```

之后就可以用 `/arxiv` 调用。
