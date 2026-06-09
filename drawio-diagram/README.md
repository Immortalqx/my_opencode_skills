# drawio-diagram

Chinese version: [README.zh-CN.md](./README.zh-CN.md)

`drawio-diagram` is a Claude Code skill for research-figure workflows. The deliverable is an editable `draw.io` / `diagrams.net` draft plus PNG/SVG/PDF exports that have passed strict visual QA. The draw.io draft is meant to be reused and edited by the user directly, not discarded as an intermediate artifact.

Use the `drawio-diagram` skill when you want Claude to create a research figure:

```text
Use the drawio-diagram skill to create a research figure from the current workspace.
Read the available paper assets first, reuse useful figures or plots, create an editable draw.io draft under image_draft/,
export PNG/SVG/PDF, and run visual QA on the PNG. Iterate on the .drawio until the QA loop passes.
Style target: clean technical poster figure.
```

If you already have a `.drawio` and want to refine it on top of the existing file:

```text
Use the drawio-diagram skill on this existing .drawio file.
Keep the structure editable, tighten the layout, re-export, and re-run the QA loop.
```

## How It Works

1. Claude reads the local paper, poster, slides, notes, or experiment materials and checks for reusable visual assets.
2. Claude creates or refines an editable `sketch.drawio` draft.
3. Claude exports PNG/SVG/PDF versions for review.
4. Claude runs the visual QA loop on the PNG, fixes the `.drawio`, and re-exports until the QA checklist passes.

## Output

By default, the skill writes to `image_draft/` and typically produces:

- `assets/`
- `asset_manifest.md`
- `sketch.drawio`
- `sketch.png`
- `sketch.svg`
- `sketch.pdf`
- `qa_notes.md`

## Helper Scripts

- [drawio-diagram/scripts/inventory_assets.py](./drawio-diagram/scripts/inventory_assets.py): inventory reusable local assets
- [drawio-diagram/scripts/render_pdf_pages.py](./drawio-diagram/scripts/render_pdf_pages.py): render PDF pages into reusable image assets
- [drawio-diagram/scripts/export_drawio.ps1](./drawio-diagram/scripts/export_drawio.ps1): export PNG/SVG/PDF from a `.drawio` file

The skill resolves these scripts via `${CLAUDE_SKILL_DIR}` from inside `SKILL.md`, so they work no matter where the skill is installed.

## Repository Layout

- `README.md` and `README.zh-CN.md`: repository docs
- `drawio-diagram/`: installable Claude skill directory
- `drawio-diagram/SKILL.md`: Claude skill definition
- `drawio-diagram/scripts/`: deterministic helper scripts (Python + PowerShell)

## Install

```bash
cp -r drawio-diagram/drawio-diagram/* ~/.claude/skills/drawio-diagram/
```

The skill is then available as `/drawio-diagram`.
