# research-survey-loop

English version: [README.md](./README.md)

`research-survey-loop` 是一个独立的 Claude Code skill 仓库，用于长期、多轮调研流程。它主要面向 Robotics、Embodied AI、计算机视觉、world models、navigation、manipulation 及其相邻方向。

## 快速开始

给 Claude 发消息，要求它使用 `research-survey-loop` skill 调研某个主题；如果你本地已经有笔记、PDF 或初步结果，也可以一起提供。

```text
使用 research-survey-loop skill 调研近期关于 embodied navigation 中 world model 的工作。
我本地也有一些笔记和 PDF，开始 round 1。
```

## 工作方式

1. 用户发送调研主题，并可附带本地已有资料。
2. Claude 创建或继续一个持久化的 survey task。
3. Claude 按多个 round 推进。不同 round 可能分别负责检索资料、阅读论文、吸收本地材料、整理分类、扩写综述。
4. 后续用户再告诉 Claude 当前继续哪个 round，或者直接让它继续下一轮。

示例后续消息：

```text
根据 current_task.md 和 round_log.md 继续 round 2。
```

## 来源策略

这个 skill 会结合：

- 工作区和 task 本地已有的 PDF，
- 公共网页检索与官方 venue / publisher 页面，
- 随 skill 打包的任务初始化、资料归档和分块读 PDF 脚本（在 `SKILL.md` 中通过 `${CLAUDE_SKILL_DIR}` 解析），
- 公共 Semantic Scholar 与 arXiv API 提供的规范化元数据。

默认路径只依赖当前 agent、skill 自带脚本和公共网页来源。

## 输出

这个 skill 会在 `survey_tasks/<topic-slug>/` 下维护一个持续演进的流程，并持续更新：

- `task.md`
- `round_log.md`
- `current_task.md`
- `survey.md`

## 仓库结构

- `README.md` 和 `README.zh-CN.md`：仓库说明文档
- `research-survey-loop/`：可安装的 Claude skill 目录
- `research-survey-loop/scripts/`：随 skill 打包的辅助脚本（init、fetch、分块读 PDF）
- `research-survey-loop/references/`：来源优先级与写作规则
- `research-survey-loop/assets/`：task、round log、current task、survey 模板

## 安装

```bash
cp -r research-survey-loop/research-survey-loop/* ~/.claude/skills/research-survey-loop/
```

之后就可以用 `/research-survey-loop` 调用。
