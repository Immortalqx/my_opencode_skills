# my_claude_skills

English | [Chinese](./README.zh-CN.md)

Personal Claude Code skills for reusable research, writing, and document workflows.

Each skill is a top-level directory. A valid skill directory contains `SKILL.md` at its root and may also include `scripts/`, `references/`, or `assets/`. There is no nested installable directory and no per-skill README in this repository.

All 29 skills are auto-invocable. Claude Code picks them up by their `description` triggers, and the user can also invoke any skill explicitly with `/<skill>`. Inside a skill's body, bundled scripts are referenced through the `${CLAUDE_SKILL_DIR}` path resolver so the path works regardless of install location (per-skill `~/.claude/skills/<skill>/` or repo-level copy).

Unless a skill explicitly says otherwise, these skills are designed for standalone, single-agent use: bundled local scripts, local files, and public web access are normal; notification hooks, reviewer-agent chains, and hidden cross-skill hooks are not part of the default path.

## Skills

| Skill | Summary | Typical use |
| --- | --- | --- |
| [`alphaxiv`](./alphaxiv/) | Quick single-paper lookup using public AlphaXiv Markdown first, with AlphaXiv Markdown and arXiv LaTeX source fallback when needed. | Explaining one arXiv paper from an ID or URL without running a broad literature survey. |
| [`arxiv`](./arxiv/) | Search arXiv, fetch metadata for specific arXiv IDs, and download PDFs into local paper libraries using the bundled arXiv Atom API helper. | Finding preprints, downloading arXiv PDFs by query or ID, and building local `papers/` or `literature/` collections. |
| [`doc-coauthoring`](./doc-coauthoring/) | Three-stage co-authoring workflow (Context Gathering → Refinement → Reader Testing) for collaborative document writing. | User asks to write a doc, proposal, spec, or similar structured content and wants structured guidance. |
| [`docx`](./docx/) | Create, read, edit, and manipulate Word documents via the bundled docx-js helpers and unpack/pack scripts. | Any task involving .docx files: reports, memos, letters, tracked changes, comments, or extracted content. |
| [`drawio-diagram`](./drawio-diagram/) | Draw.io research-figure workflow that builds an editable `.drawio` draft, exports PNG/SVG/PDF, and runs visual QA on the exported PNG. | Paper figures, posters, slide visuals, and concept diagrams that need an editable draw.io artifact. |
| [`figure-description`](./figure-description/) | Patent figure workflow that identifies components, assigns reference numerals, and generates formal drawing descriptions. | Preparing CN/US/EP patent drawing descriptions and reference numeral indexes from local technical figures. |
| [`phd-figure-designer`](./phd-figure-designer/) | Design advisor for the three load-bearing figures of a technical paper: Motivated Example, Solution Overview, and Experimental Results. | User wants feedback on Figure 1 design, a Solution Overview diagram, or experimental-results chart layout. |
| [`formula-derivation`](./formula-derivation/) | Research-formula derivation workflow that clarifies assumptions and separates identities, propositions, approximations, and interpretations. | Turning messy theory notes into an internal derivation note, paper-style theory draft, or blocker report. |
| [`grant-proposal`](./grant-proposal/) | Structured grant-proposal drafting from research ideas and literature, with agency-specific and generic formats. | Turning a research direction into a funding application with aims, milestones, feasibility, and outputs. |
| [`help-me-read`](./help-me-read/) | Deep-read a user-provided PDF and produce a story-driven close-read note with page screenshots, figure explanations, and background context. | Detailed study notes, tutor-style breakdowns, or close reads of lecture decks and academic papers. |
| [`mmx-cli`](./mmx-cli/) | MiniMax CLI skill for operating the local `mmx` command for text, search, vision, quota, file, and media tasks. | Running an installed local MiniMax CLI directly, especially for bilingual multi-query search and non-interactive JSON workflows. |
| [`mock-review`](./mock-review/) | Mock peer-review workflow for manuscript authors that studies venue requirements, inspects PDFs, researches related work, and writes simulated reviews. | Pre-submission risk checks, rebuttal preparation, and reviewer-style critique before revising a manuscript. |
| [`novelty-check`](./novelty-check/) | Research-idea novelty checker that extracts core claims, searches literature, compares closest prior work, and reports novelty risk. | Checking whether a method appears to have already been done before investing implementation time. |
| [`pdf`](./pdf/) | Read, merge, split, rotate, watermark, encrypt, OCR, and fill forms on PDF files using pypdf, pdfplumber, reportlab, and poppler. | Any .pdf-related task, including reading tables, redacting pages, and creating new PDFs from scratch. |
| [`phd-benchmark-paper-template`](./phd-benchmark-paper-template/) | Benchmark / Evaluation paper scaffolding around five pillars (Research Gap, Construction Pipeline, Evaluation Framework, Empirical Findings, optional Companion Method). | User is writing a benchmark paper and needs a stage-aware workflow from gap analysis to pre-submission checklist. |
| [`phd-idea-evaluator`](./phd-idea-evaluator/) | Reviewer-style idea evaluation using a five-dimension framework (Higher, Faster, Stronger, Cheaper, Broader), lifecycle matching, paradigm-shift probing, and fatal-flaws audit. | User has a draft research idea and asks whether it is worth pursuing before committing to a paper scope. |
| [`phd-intro-drafter`](./phd-intro-drafter/) | Six-paragraph Introduction outline (Background → Limitations → Goal → Challenges → Solution → Contributions) with challenge-to-module and contribution-to-section mapping. | User wants to draft or restructure the Introduction of a technical paper before writing prose. |
| [`phd-pre-submission-reviewer`](./phd-pre-submission-reviewer/) | Pre-submission review across five dimensions (macro logic, writing details, English grammar, LaTeX formatting, figure quality) with CRITICAL/MAJOR/MINOR severity tagging. | User asks for a final-pass review within the last 3-5 days before a submission deadline. |
| [`phd-tech-paper-template`](./phd-tech-paper-template/) | Structures a technical paper's logical skeleton with a thinking-template table and runs a four-point self-consistency check. | User is brainstorming a paper, planning before drafting, or auditing a half-written paper's logic chain. |
| [`phd-vibe-research-workflow`](./phd-vibe-research-workflow/) | AI-assisted research workflow covering Vibe Coding, Vibe Figure, and Vibe Writing, with behavioural rules and tool selection. | User wants to start a new AI-assisted work block or needs guidance on which AI tool fits the current stage. |
| [`pptx`](./pptx/) | Read, create, and edit PowerPoint presentations using markitdown, pptxgenjs, and the bundled unpack/pack/QA scripts. | Building or editing slide decks, parsing content out of .pptx files, or running visual QA on rendered slides. |
| [`proof-writer`](./proof-writer/) | Rigorous proof-writing workflow for theorem, lemma, proposition, and corollary statements. | Turning a rough mathematical claim or proof sketch into a defensible proof package. |
| [`research-lit`](./research-lit/) | Standalone literature-review workflow across local PDFs, public web search, and structured arXiv metadata. | Finding related work, mapping a paper landscape, and comparing paper clusters around a research topic. |
| [`research-survey-loop`](./research-survey-loop/) | Long-running literature survey workflow that maintains stable task documents, searches prioritized sources, reads papers in chunks, and incrementally writes a Chinese survey. | Sustained literature surveys for robotics, embodied AI, computer vision, world models, navigation, manipulation, 3D perception, and adjacent topics. |
| [`research-wiki`](./research-wiki/) | Persistent project-level research knowledge base for papers, ideas, experiments, claims, and typed relationships. | Building reusable project memory instead of rediscovering the same field map in every session. |
| [`skill-creator`](./skill-creator/) | End-to-end workflow to create new skills, iterate on existing ones, run evals, and optimize description triggers. | User wants to author a new skill, refine an existing one, or measure skill performance with variance analysis. |
| [`theme-factory`](./theme-factory/) | Ten pre-curated color and font themes (Ocean Depths, Sunset Boulevard, etc.) that can be applied to any artifact. | Applying consistent professional styling to slide decks, documents, reports, or HTML landing pages. |
| [`update-source-map`](./update-source-map/) | Create or update an agent-readable source map for any project directory while preserving hand-curated per-file summaries across regenerations. | Starting work in an unfamiliar workspace, refreshing a stale index, or handing a project to another agent. |
| [`xlsx`](./xlsx/) | Create, read, edit, and analyze spreadsheets with openpyxl and pandas, including formula recalculation and error scanning. | Any .xlsx / .xlsm / .csv / .tsv task such as adding columns, computing formulas, or cleaning messy tabular data. |

## Install

Each top-level directory is a skill. Copy it into `~/.claude/skills/`:

```bash
cp -r <skill> ~/.claude/skills/<skill>
```

To install all 29 skills at once:

```bash
for s in alphaxiv arxiv doc-coauthoring docx drawio-diagram figure-description \
         phd-figure-designer formula-derivation grant-proposal help-me-read \
         mmx-cli mock-review novelty-check pdf phd-benchmark-paper-template \
         phd-idea-evaluator phd-intro-drafter phd-pre-submission-reviewer \
         phd-tech-paper-template phd-vibe-research-workflow pptx proof-writer \
         research-lit research-survey-loop research-wiki skill-creator \
         theme-factory update-source-map xlsx; do
  cp -r "$s" ~/.claude/skills/"$s"/
done
```

After installing or updating skills, restart Claude Code so the new skill metadata is picked up.

## Notes

- All 29 skills are auto-invocable. Claude Code matches user requests to skill descriptions, and the user can also invoke a skill explicitly with `/<skill-name>`. There is no `disable-model-invocation` flag on any skill in this repository.
- Inside each `SKILL.md`, bundled scripts are referenced through `${CLAUDE_SKILL_DIR}` so paths work whether the skill is installed at `~/.claude/skills/<skill>/` or copied to a different location.
- These skills encode personal research workflows and do not represent official processes of any venue, journal, or institution.
- Skills sourced from external repositories keep their original names or use a `phd-` prefix to namespace them: Anthropic skills (no prefix) come from `anthropics/skills`, and the `phd-*` skills come from `HKUSTDial/Supervisor-Skills`. See each skill's `LICENSE.txt` or SKILL.md frontmatter for upstream license terms.
- `mmx-cli` requires a configured local `mmx` command.
- `drawio-diagram` is intended for editable figure workflows and declares a figure ready only after the visual QA loop passes.
- Outputs from `mock-review` should be clearly labeled as simulated/mock reviews and must not impersonate official reviewer reports.
- Literature retrieval should prioritize legally accessible sources such as official open-access pages, arXiv, OpenReview, and author pages.
