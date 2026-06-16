# my_opencode_skills

[English](./README.md) | [中文](./README.zh-CN.md)

个人维护的 opencode skills 集合，用于沉淀可复用的科研、写作和文档处理工作流。

每个 skill 都是一个顶层目录。合法的 skill 目录会在根部包含 `SKILL.md`，并可以按需附带 `scripts/`、`references/` 或 `assets/`。本仓库不再使用嵌套的可安装目录，也不再保留每个 skill 自己的 README。

所有 28 个 skills 都是 auto-invocable。opencode 会根据 `description` 触发词自动匹配，用户也可以通过 `skill` 工具显式调用。在每个 skill 内部，附带脚本和资源通过 `@@SKILL_DIR@@` 和 `@@SKILL_DIR:<other-skill>@@` 占位符引用；安装脚本会把这些占位符替换成绝对安装路径。

除非某个 skill 明确说明，否则这些 skills 默认面向独立、单 agent 使用：可以使用 skill 自带脚本、本地文件和公共网页来源；通知钩子、reviewer agent 链路或隐藏的跨 skill 钩子都不是默认路径。

## 安装

依赖：**Python 3.10+**（需要 `pyyaml`，`pip install pyyaml`）和 **opencode 1.1+**（1.1+ 起会对 skill 目录自动放行 `external_directory`）。

### 默认安装（全部 28 个 skills 到 `~/.config/opencode/skills/`）

```bash
git clone <repo-url> my_opencode_skills
cd my_opencode_skills
python install-to-opencode.py --apply
```

首次安装或更新后，重启 opencode 让新 skill 的 metadata 生效。

### 自定义安装位置

opencode 默认还会扫描 `~/.claude/skills/` 和 `~/.agents/skills/`，你也可以装到任意位置并把路径加到 `opencode.json`：

```bash
python install-to-opencode.py --target D:/my-skills --apply
```

```jsonc
// opencode.json
{
  "skills": {
    "paths": ["D:/my-skills"]
  }
}
```

### 只装部分 skill

```bash
python install-to-opencode.py --skill arxiv --skill drawio-diagram --apply
```

### 覆盖重装

```bash
python install-to-opencode.py --force --apply
```

### 预览

所有命令默认是 dry-run。去掉 `--apply` 就只会打印计划、不写盘。

```bash
python install-to-opencode.py                       # 打印安装计划
python install-to-opencode.py --preview arxiv      # 预览某个 skill 装好后的 SKILL.md
python install-to-opencode.py --test               # 跑内置单元测试
```

## 路径约定

本仓库绝不包含用户特定路径。使用两种占位符，由安装脚本在落地时替换：

| 占位符 | 含义 | 装好后示例 |
| --- | --- | --- |
| `@@SKILL_DIR@@` | 当前 skill 的安装目录 | `C:/Users/<你>/.config/opencode/skills/arxiv` |
| `@@SKILL_DIR:<name>@@` | 另一个 skill 的安装目录（跨 skill 引用） | `C:/Users/<你>/.config/opencode/skills/arxiv` |

`SKILL.md` 内的裸 `scripts/<file>`、`references/<file>`、`assets/<file>` 路径，只要对应的文件实际存在于该 skill 目录中，也会被自动替换。

## 临时目录约定

所有 skill 写到**用户项目**的中间产物统一放在项目根的 **`x_temp/`** 目录。前导 `x_` 让 `x_temp` 排在任何目录列表的底部，便于一眼找到和清理。`temp_claude/`、`claude_temp/`、`x_temp_claude/` 等历史命名已全部清掉。

## Skills

| Skill | 简介 | 典型用途 |
| --- | --- | --- |
| [`alphaxiv`](./alphaxiv/) | 使用公开 AlphaXiv Markdown 快速查询单篇 arXiv 论文，必要时降级读取完整 AlphaXiv Markdown 或 arXiv LaTeX 源码。 | 根据 arXiv ID 或 URL 快速解释单篇论文，而不是做大范围文献综述。 |
| [`arxiv`](./arxiv/) | 搜索 arXiv、按 arXiv ID 获取论文元数据，并通过内置 arXiv Atom API 辅助脚本把 PDF 下载到本地论文库。 | 查找预印本、按查询词或 arXiv ID 下载 PDF，以及维护本地 `papers/` 或 `literature/` 论文集合。 |
| [`doc-coauthoring`](./doc-coauthoring/) | 三阶段协作式文档写作工作流：上下文收集 → 结构打磨 → 读者测试。 | 用户要写文档、提案、PRD、设计文档等结构化内容，并希望有结构化引导。 |
| [`docx`](./docx/) | 通过内置 docx-js helpers 和 unpack/pack 脚本创建、读取、编辑和操作 Word 文档。 | 任何 .docx 相关任务：报告、备忘录、信函、tracked changes、评论，或从中抽取内容。 |
| [`drawio-diagram`](./drawio-diagram/) | 面向科研图示的 draw.io 工作流：生成可编辑 `.drawio` 草稿，导出 PNG/SVG/PDF，并在 PNG 上执行视觉 QA。 | 论文配图、海报、演示文稿视觉稿、概念图，尤其适合需要保留可编辑 draw.io 文件的场景。 |
| [`figure-description`](./figure-description/) | 专利附图处理工作流：识别图中部件、分配附图标记，并生成正式附图说明。 | 根据本地技术图准备 CN/US/EP 专利附图说明和附图标记索引。 |
| [`phd-figure-designer`](./phd-figure-designer/) | 技术论文三张承重图（Motivated Example、Solution Overview、Experimental Results）的设计顾问。 | 用户想要对 Figure 1 设计、Solution Overview 框图或实验结果图的布局给出反馈。 |
| [`formula-derivation`](./formula-derivation/) | 研究公式推导工作流：澄清假设，并区分恒等式、命题、近似和解释。 | 把杂乱理论笔记整理成内部推导笔记、论文风格理论草稿或 blocker report。 |
| [`grant-proposal`](./grant-proposal/) | 从研究 idea 和文献材料撰写结构化基金申请书，支持机构特定格式和通用格式。 | 把研究方向转成包含研究目标、里程碑、可行性和预期成果的 funding application。 |
| [`help-me-read`](./help-me-read/) | 深读用户提供的 PDF，生成带页面截图、图表解释和背景补充的故事化精读笔记。 | 生成 lecture slides 或论文的精读笔记、深入解析和 tutor-style breakdown。 |
| [`mmx-cli`](./mmx-cli/) | MiniMax CLI skill，用本地 `mmx` 命令执行文本、搜索、视觉、额度、文件和多媒体任务。 | 直接调用本地已配置好的 MiniMax CLI，尤其适合中英文混合多次搜索，以及 `--quiet`、`--output json`、`--non-interactive` 的非交互式工作流。 |
| [`mock-review`](./mock-review/) | 给论文作者使用的模拟审稿工作流：调研 venue 要求、检查稿件 PDF、研究相关工作并生成模拟审稿意见。 | 投稿前风险排查、rebuttal 准备、论文修改前的 reviewer-style critique。 |
| [`novelty-check`](./novelty-check/) | 研究 idea 查新工具：抽取核心 claim，检索文献，对比 closest prior work，并报告 novelty 风险。 | 在投入实现时间前检查一个方法是否看起来已经被做过。 |
| [`pdf`](./pdf/) | 用 pypdf、pdfplumber、reportlab 和 poppler 进行 PDF 合并、拆分、旋转、水印、加密、OCR 和表单填写。 | 任何 .pdf 相关任务，包括读取表格、页面处理和从零创建新 PDF。 |
| [`phd-benchmark-paper-template`](./phd-benchmark-paper-template/) | 围绕五大支柱（Research Gap、Construction Pipeline、Evaluation Framework、Empirical Findings、可选 Companion Method）的 Benchmark / Evaluation 论文骨架。 | 用户正在写一篇 benchmark 论文，需要从 gap analysis 到 pre-submission checklist 的阶段化工作流。 |
| [`phd-idea-evaluator`](./phd-idea-evaluator/) | 用五维框架（更高更快更强更省更广）、生命周期匹配、范式跃迁探测和致命缺陷审计给出 reviewer-style 评估。 | 用户有一个 draft idea，想在投入几个月之前知道值不值得做。 |
| [`phd-intro-drafter`](./phd-intro-drafter/) | 六段式 Introduction 大纲（背景→局限→目标→挑战→方案→贡献），并强制挑战-模块、贡献-章节一一对应。 | 用户想在写正文前起草或重构技术论文的 Introduction。 |
| [`phd-pre-submission-reviewer`](./phd-pre-submission-reviewer/) | 跨 5 个维度（宏观逻辑、写作细节、英语语法、LaTeX 排版、图表质量）的预投稿审核，含 CRITICAL/MAJOR/MINOR 严重性分级。 | 用户在投稿截止前 3-5 天要求做 final pass 复审。 |
| [`phd-tech-paper-template`](./phd-tech-paper-template/) | 用 thinking-template 表格搭出技术论文的完整逻辑骨架，并跑 4 项自洽性检查。 | 用户正在头脑风暴一篇论文、动笔前规划，或对半成品论文的逻辑链做审计。 |
| [`phd-vibe-research-workflow`](./phd-vibe-research-workflow/) | 覆盖 Vibe Coding、Vibe Figure、Vibe Writing 的 AI 辅助科研工作流，含行为守则和工具选型。 | 用户要开启一个 AI 辅助工作块，或需要指导当前阶段该用哪个 AI 工具。 |
| [`pptx`](./pptx/) | 用 markitdown、pptxgenjs 和内置 unpack/pack/QA 脚本读取、创建和编辑 PowerPoint 演示文稿。 | 构建或编辑幻灯片、从 .pptx 抽取内容，或对渲染出的幻灯片做视觉 QA。 |
| [`proof-writer`](./proof-writer/) | 面向 theorem、lemma、proposition、corollary 等命题的严谨证明写作工作流。 | 把粗糙命题或证明草稿整理成可辩护的证明包。 |
| [`research-lit`](./research-lit/) | 独立文献调研工作流：结合本地 PDF、公共网页检索和结构化 arXiv 元数据进行相关工作检索、比较和综合。 | 围绕某个研究主题查找相关工作、梳理论文版图并比较不同方法簇。 |
| [`research-survey-loop`](./research-survey-loop/) | 长周期文献综述工作流：维护稳定任务文档、按来源优先级搜索论文、分块阅读论文，并逐轮扩展中文综述。 | 机器人、具身智能、计算机视觉、世界模型、导航、操作、3D 感知等方向的持续文献调研。 |
| [`research-wiki`](./research-wiki/) | 持久化项目级科研知识库，用于沉淀论文、想法、实验、主张以及它们之间的有类型关系。 | 把项目研究记忆固定下来，避免每个 session 都重新搭一遍同一张领域地图。 |
| [`theme-factory`](./theme-factory/) | 10 套精选的配色与字体主题（Ocean Depths、Sunset Boulevard 等），可套用到任何 artifact。 | 给幻灯片、文档、报告或 HTML 着陆页应用统一专业样式。 |
| [`update-source-map`](./update-source-map/) | 为任意项目目录创建或更新 agent 可读的 source map，并在刷新时保留手写的 per-file 摘要。 | 处理新的或不熟悉的 workspace、刷新过期索引，或把项目交给另一个 agent。 |
| [`xlsx`](./xlsx/) | 用 openpyxl 和 pandas 创建、读取、编辑和分析电子表格，含公式重算和错误扫描。 | 任何 .xlsx / .xlsm / .csv / .tsv 任务，例如加列、计算公式、清洗脏表格数据。 |

## 说明

- 所有 28 个 skills 都是 auto-invocable。opencode 根据 `description` 触发词自动匹配；用户也可以用 `skill` 工具显式调用。本仓库没有任何一个 skill 带有 `disable-model-invocation` 标记。
- 每个 `SKILL.md` 内部，附带脚本和资源都通过 `@@SKILL_DIR@@`（跨 skill 用 `@@SKILL_DIR:<other>@@`）引用。安装脚本在落地时把这些占位符替换为绝对安装路径，所以同一份源码无论装到 `~/.config/opencode/skills/<skill>/` 还是别的位置都能正常工作。
- 这些 skills 是个人科研工作流沉淀，不代表任何会议、期刊或机构的官方流程。
- 从外部仓库引入的 skills 保持原名或加 `phd-` 前缀以标记来源：Anthropic 官方 skills（无前缀）来自 `anthropics/skills` 仓库；`phd-*` 系列来自 `HKUSTDial/Supervisor-Skills` 仓库。各 skill 的上游许可条款见其 `LICENSE.txt` 或 SKILL.md frontmatter。
- `mmx-cli` 需要本地已经配置好 `mmx` 命令。
- `drawio-diagram` 面向需要保留可编辑 draw.io 草稿的图示工作流；只有视觉 QA 循环通过后才应宣布图已完成。
- 使用 `mock-review` 生成的内容应明确标注为 simulated/mock review，不能冒充官方审稿意见。
- 文献下载和调研应优先使用官方开放页面、arXiv、OpenReview、作者主页等合法可访问来源。
