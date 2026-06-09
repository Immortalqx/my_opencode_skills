# figure-description

[English](./README.md) | 中文

`figure-description` 是一个专利用途的附图处理 skill，用于处理用户提供的技术图，并生成带附图标记的正式附图说明。

当你已有专利附图，希望 Claude 识别部件、分配附图标记并撰写附图说明时，可以使用 `figure-description` skill：

```text
使用 figure-description skill 处理 patent/figures/ 下的附图，撰写 CN 发明专利附图说明。
```

## 依赖说明

这个 skill 本身不需要 API key。它主要读取本地图像文件和专利草稿材料，例如 `patent/INVENTION_DISCLOSURE.md` 与 `patent/CLAIMS.md`。

## 工作流程

1. 在 `patent/figures/`、`figures/` 或项目根目录中发现附图文件。
2. 检查每张图，识别部件、连接关系和流程。
3. 按图号系列分配附图标记。
4. 按 CN、US 或 EP 风格生成正式附图说明。
5. 生成附图标记索引和一致性检查清单。

## 内容

- `figure-description/SKILL.md`：Claude skill 定义。
- 外层 `README.md` 和 `README.zh-CN.md` 只是仓库说明，不会被安装到 Claude skills 目录。

## 安装

```bash
cp -r figure-description/figure-description/* ~/.claude/skills/figure-description/
```

之后就可以用 `/figure-description` 调用。
