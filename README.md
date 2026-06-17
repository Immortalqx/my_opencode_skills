# my_opencode_skills

[English](./README.md) | [中文](./README.zh-CN.md)

Personal opencode skills for reusable research, writing, and document workflows.

Each skill is a top-level directory. A valid skill directory contains `SKILL.md` at its root and may also include `scripts/`, `references/`, or `assets/`. There is no nested installable directory and no per-skill README in this repository.

All 27 skills are auto-invocable. opencode picks them up by their `description` triggers, and the user can also invoke any skill explicitly via the `skill` tool. Inside a skill's body, bundled scripts and resources are referenced through the `@@SKILL_DIR@@` and `@@SKILL_DIR:<other-skill>@@` placeholders; the install script substitutes these with absolute install paths.

Unless a skill explicitly says otherwise, these skills are designed for standalone, single-agent use: bundled local scripts, local files, and public web access are normal; notification hooks, reviewer-agent chains, and hidden cross-skill hooks are not part of the default path.

## Install

Requires **Python 3.10+** with `pyyaml` (`pip install pyyaml`) and **opencode 1.1+** (for `external_directory` auto-allow on skill directories).

### Install modes

Five `--mode` presets are supported:

| Mode | Default | Skills | Target |
|------|---------|--------|--------|
| `default` (when no `--mode` given) | ✅ | `mmx-cli` only | `~/.config/opencode/skills/` |
| `all` | | All 27 skills | `~/.config/opencode/skills/` |
| `select` | | Those given by `--skill` | `--target` (defaults to global) |
| `literature-survey` | | Literature survey bundle (5) | **`--target` required** |
| `mock-review` | | Mock review bundle (4) | **`--target` required** |

#### Quick reference

```bash
# 1. Default: install mmx-cli to global only (compensates for MiniMax M3's missing web search)
python install-to-opencode.py --apply

# 2. Install all to global
python install-to-opencode.py --mode all --apply

# 3. Literature survey project (5 skills)
python install-to-opencode.py --mode literature-survey --target /path/to/proj/.opencode/skills --apply

# 4. Mock review project (4 skills)
python install-to-opencode.py --mode mock-review --target /path/to/proj/.opencode/skills --apply

# 5. Install specific skill to global
python install-to-opencode.py --mode select --skill arxiv --apply

# 6. Install specific skill to project
python install-to-opencode.py --mode select --skill arxiv --target /path/to/proj/.opencode/skills --apply
```

#### Argument resolution

```
--target  :  CLI  >  mode.target  >  YAML default_target
--skill   :  CLI  >  mode.skills
--mode    :  CLI  >  default
```

CLI values always win over mode presets.

#### Five mode validations (error messages)

| Trigger | Behavior |
|---------|----------|
| `--skill` but `--mode` is not `select` | ❌ ERROR |
| `--mode <preset>` with `--skill` | ❌ ERROR (`default` / `all` / `literature-survey` / `mock-review` do not accept `--skill`) |
| `--mode select` without `--skill` | ❌ ERROR (`select` requires `--skill`) |
| `--mode literature-survey` or `--mode mock-review` without `--target` | ❌ ERROR (these modes require a project path) |

### Common options

| Option | Description |
|--------|-------------|
| `--apply` | Actually write to disk (default is dry-run) |
| `--force` | `rmtree` target dir and rebuild (**deletes everything in target, including files you added manually**) |
| `--preview <SKILL>` | Print the post-substitution `SKILL.md` of `<SKILL>` to stdout |
| `--test` | Run the built-in unit tests |
| `--skill <name>` | Only valid with `--mode select` (repeatable) |
| `--target <path>` | Install to given path (default depends on mode) |
| `--source <path>` | Source repo path (default: script's parent dir) |
| `--verbose` / `-v` | Verbose output |

### `--force` behavior

- **Without `--force`**: If the skill already exists in the target, the **whole skill is skipped**. Safe but stale — changes in source are not reflected in target.
- **With `--force`**: `rmtree` the target dir and rebuild. Equivalent to `rsync --delete` — files you added manually in target (not in source) **will be deleted**.
- **Daily suggestion**: Run without `--force` first to inspect the summary; add `--force` only when you confirm a clean reinstall is wanted.

### Test checklist (after deleting all skills)

```bash
# 1. Unit tests (no side effects)
python install-to-opencode.py --test
# Expected: Ran 9 tests in ... OK

# 2. Default dry-run
python install-to-opencode.py
# Expected: mode=default  skills=1 selected: mmx-cli

# 3. Default apply
python install-to-opencode.py --apply
# Expected: ~/.config/opencode/skills/ contains mmx-cli/ only

# 4. --mode all
python install-to-opencode.py --mode all --apply
# Expected: ~/.config/opencode/skills/ contains 27 skill directories

# 5. --mode literature-survey
python install-to-opencode.py --mode literature-survey --target <project/.opencode/skills> --apply
# Expected: 5 skills in project

# 6. --mode mock-review
python install-to-opencode.py --mode mock-review --target <project/.opencode/skills> --apply
# Expected: 4 skills in project

# 7. --mode select custom
python install-to-opencode.py --mode select --skill arxiv --apply
# Expected: arxiv/ in global

# 8. Re-run same mode
python install-to-opencode.py --mode all --apply
# Expected: 27 Skipped (already exists, use --force to overwrite)

# 9. --force reinstall
python install-to-opencode.py --mode all --apply --force
# Expected: 27 Installed

# 10. Error validations
python install-to-opencode.py --mode all --skill arxiv
# Expected: ERROR: --skill 仅在 --mode select 下有效

python install-to-opencode.py --mode select
# Expected: ERROR: --mode select 必须配合 --skill

python install-to-opencode.py --mode literature-survey
# Expected: ERROR: --mode literature-survey 必须配合 --target
```

### Custom install location

opencode scans 6 default locations (3 project + 3 global), but installing elsewhere requires adding to `opencode.json`:

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

### Dry-run

All commands are dry-run by default. Drop `--apply` to see what would change without writing anything.

```bash
python install-to-opencode.py                          # show default-mode install plan
python install-to-opencode.py --mode all               # dry-run all
python install-to-opencode.py --preview arxiv          # show arxiv's post-install SKILL.md
python install-to-opencode.py --test                   # run unit tests
```

## Path convention

This repo never contains user-specific paths. It uses two placeholders that the install script resolves:

| Placeholder | Meaning | Example after install |
| --- | --- | --- |
| `@@SKILL_DIR@@` | The current skill's install directory | `C:/Users/<you>/.config/opencode/skills/arxiv` |
| `@@SKILL_DIR:<name>@@` | Another skill's install directory (cross-skill reference) | `C:/Users/<you>/.config/opencode/skills/arxiv` |

Bare `scripts/<file>`, `references/<file>`, and `assets/<file>` paths inside `SKILL.md` are also substituted automatically when the file actually exists in the skill.

## Scratch directories

All skills follow one convention: any intermediate output the skill writes to a user's project lives under **`x_temp/`** at the project root. The leading `x_` sorts `x_temp` to the bottom of any directory listing, making it easy to spot and clean up. The legacy `temp_claude/`, `claude_temp/`, `x_temp_claude/`, etc. naming is gone.

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
| [`theme-factory`](./theme-factory/) | Ten pre-curated color and font themes (Ocean Depths, Sunset Boulevard, etc.) that can be applied to any artifact. | Applying consistent professional styling to slide decks, documents, reports, or HTML landing pages. |
| [`update-source-map`](./update-source-map/) | Create or update an agent-readable source map for any project directory while preserving hand-curated per-file summaries across regenerations. | Starting work in an unfamiliar workspace, refreshing a stale index, or handing a project to another agent. |
| [`xlsx`](./xlsx/) | Create, read, edit, and analyze spreadsheets with openpyxl and pandas, including formula recalculation and error scanning. | Any .xlsx / .xlsm / .csv / .tsv task such as adding columns, computing formulas, or cleaning messy tabular data. |

## Notes

- All 27 skills are auto-invocable. opencode matches user requests to skill descriptions; the user can also invoke a skill explicitly with the `skill` tool.
- Inside each `SKILL.md`, bundled scripts and resources are referenced through `@@SKILL_DIR@@` (or `@@SKILL_DIR:<other>@@` for cross-skill). The install script substitutes these with the absolute install path so the same source tree works regardless of where it gets installed. **This is intentional**: some LLM clients (e.g., MiniMax M3) cannot resolve `@@SKILL_DIR@@`-style relative placeholders, so the installed `SKILL.md` must embed absolute paths for the skill's bundled scripts and resources to be locatable.
- These skills encode personal research workflows and do not represent official processes of any venue, journal, or institution.
- Skills sourced from external repositories keep their original names or use a `phd-` prefix to namespace them: Anthropic skills (no prefix) come from `anthropics/skills`, and the `phd-*` skills come from `HKUSTDial/Supervisor-Skills`. See each skill's `LICENSE.txt` or SKILL.md frontmatter for upstream license terms.
- `mmx-cli` requires a configured local `mmx` command.
- `drawio-diagram` is intended for editable figure workflows and declares a figure ready only after the visual QA loop passes.
- Outputs from `mock-review` should be clearly labeled as simulated/mock reviews and must not impersonate official reviewer reports.
- Literature retrieval should prioritize legally accessible sources such as official open-access pages, arXiv, OpenReview, and author pages.
- The install script automatically strips Claude-Code-specific frontmatter fields (`allowed-tools: ...`, `argument-hint: ...`, `$ARGUMENTS`, `${CLAUDE_SKILL_DIR}`). opencode does not recognize these fields, and keeping them is just noise; stripping them is invisible to opencode behavior.
