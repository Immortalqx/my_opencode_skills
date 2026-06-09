# mmx-cli

[English](./README.md) | 中文

`mmx-cli` 是一个 Claude Code skill，封装了 [MiniMax CLI](https://github.com/MiniMax-AI/cli) 项目的本地 `mmx` 命令行工具。它让 Claude 可以通过 `mmx` 处理文本、图片、视频、语音、音乐、网页搜索、视觉理解、额度查询、文件管理和 schema 导出等流程。

当你希望 Claude 通过本地 MiniMax CLI 执行任务时使用这个 skill：

```text
使用 mmx-cli skill 跑一次 MiniMax CLI 的图片生成 dry run，并把请求 JSON 给我。
```

如果只是做低成本能力检查，要求 Claude 使用 `--dry-run`、`--quiet`、`--output json` 和 `--non-interactive`。

## 可安装目录

真正可安装的 Claude skill 是：

```text
mmx-cli/mmx-cli/
```

不要安装外层 `mmx-cli/` 文件夹。外层只放这个仓库的说明文档。

## 内容

- `mmx-cli/SKILL.md`：Claude skill 定义，与上游 MiniMax CLI skill 保持同步。

## 前置条件

使用前需要先安装并配置 MiniMax CLI：

```bash
npm install -g mmx-cli
mmx auth status
```

## 安装

```bash
cp -r mmx-cli/mmx-cli/* ~/.claude/skills/mmx-cli/
```

之后就可以用 `/mmx-cli` 调用。
