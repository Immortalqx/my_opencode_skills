# research-lit

[English](./README.md) | 中文

`research-lit` 是一个独立的 Claude Code skill，用于检索、对比和综合研究论文。默认路径只依赖本地 PDF、公共网页检索和随 skill 打包的 arXiv 元数据脚本。

当你希望 Claude 查找相关工作、总结某个研究方向，或者理解一组论文在讲什么时，可以使用 `research-lit` skill：

```text
使用 research-lit skill 查找关于机器人操作中 diffusion policy 的近期论文，并总结主要方法族。
```

如果想限制信息来源，也可以这样说：

```text
使用 research-lit skill 调研 VLM agent 的 test-time scaling，sources: local, web, arxiv download: true。
```

## 工作流程

1. Claude 解析研究主题、信息来源、本地论文库路径和可选的 arXiv 下载设置。
2. Claude 扫描本地 `papers/`、`literature/` 或用户显式指定的论文目录。
3. Claude 使用公共网页检索补充近期论文和官方页面。
4. Claude 使用内置 arXiv 辅助脚本获取结构化元数据，并在用户要求时下载 PDF。
5. Claude 按 arXiv ID、URL 或规范化标题去重。
6. Claude 按问题、方法、结果、相关性和来源分析每篇论文，并输出综合结果。

## 输出

- 带引用元数据、方法摘要、关键结果、相关性和来源的文献表格。
- 对领域格局的简短叙述性总结。
- 可选地把 arXiv PDF 下载到 `papers/`、`literature/` 或用户指定目录。

## 辅助脚本

- [research-lit/scripts/arxiv_fetch.py](./research-lit/scripts/arxiv_fetch.py)：随 skill 打包的 arXiv Atom API 搜索和 PDF 下载辅助脚本。在 `SKILL.md` 中通过 `${CLAUDE_SKILL_DIR}` 解析路径。

## 可安装目录

真正可安装的 Claude skill 是：

```text
research-lit/research-lit/
```

不要安装外层 `research-lit/` 文件夹。外层只放这个仓库的说明文档。

## 内容

- `research-lit/SKILL.md`：文献调研工作流。
- `research-lit/scripts/`：skill 自带的确定性辅助脚本。

## 安装

```bash
cp -r research-lit/research-lit/* ~/.claude/skills/research-lit/
```

之后就可以用 `/research-lit` 调用。
