# drawio-diagram

[English](./README.md) | 中文

`drawio-diagram` 是一个独立的 Claude Code skill，面向科研图示工作流。核心交付物是可编辑的 `draw.io` / `diagrams.net` 草稿，以及通过严格视觉 QA 的 PNG/SVG/PDF 导出；草图本身就要足够好，用户可以直接在 draw.io 里继续编辑并作为最终配图使用。

让 Claude 对论文、海报或概念图任务使用 `drawio-diagram` skill：

```text
使用 drawio-diagram skill 从当前工作区生成一张科研配图。
先读取已有的论文素材、复用有用的图或图表，在 image_draft/ 下创建可编辑的 draw.io 草稿，
导出 PNG/SVG/PDF，并在 PNG 上跑视觉 QA。迭代修改 .drawio 直到 QA 全部通过。
风格目标：清爽的技术海报配图。
```

如果你已经有一个 `.drawio` 文件，希望在原图基础上继续细化，也可以这样说：

```text
对当前这个 .drawio 文件使用 drawio-diagram skill。
保持结构可编辑、收紧布局、重新导出，再跑一次 QA 循环。
```

## 工作流程

1. Claude 先读取本地论文、海报、幻灯片、笔记或实验材料，并检查可复用的视觉素材。
2. Claude 创建或继续完善可编辑的 `sketch.drawio` 草稿。
3. Claude 导出 PNG/SVG/PDF，供用户检查和继续编辑。
4. Claude 在 PNG 上跑视觉 QA 循环，修复 `.drawio` 并重新导出，直到 QA 清单全部通过。

## 输出

默认输出目录为 `image_draft/`，通常会包含：

- `assets/`
- `asset_manifest.md`
- `sketch.drawio`
- `sketch.png`
- `sketch.svg`
- `sketch.pdf`
- `qa_notes.md`

## 辅助脚本

- [drawio-diagram/scripts/inventory_assets.py](./drawio-diagram/scripts/inventory_assets.py)：盘点本地可复用素材
- [drawio-diagram/scripts/render_pdf_pages.py](./drawio-diagram/scripts/render_pdf_pages.py)：把 PDF 页面渲染成可复用图片资产
- [drawio-diagram/scripts/export_drawio.ps1](./drawio-diagram/scripts/export_drawio.ps1)：从 `.drawio` 导出 PNG/SVG/PDF

在 `SKILL.md` 中调用时用 `${CLAUDE_SKILL_DIR}` 解析这些脚本路径，无论装在哪里都能找到。

## 仓库结构

- `README.md` 和 `README.zh-CN.md`：仓库说明文档
- `drawio-diagram/`：可安装的 Claude skill 目录
- `drawio-diagram/SKILL.md`：Claude skill 定义
- `drawio-diagram/scripts/`：确定性的辅助脚本（Python + PowerShell）

## 安装

```bash
cp -r drawio-diagram/drawio-diagram/* ~/.claude/skills/drawio-diagram/
```

之后就可以用 `/drawio-diagram` 调用。
