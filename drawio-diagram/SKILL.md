---
name: drawio-diagram
description: Use when creating research figures, paper posters, academic presentation visuals, or conceptual diagrams as an editable draw.io/diagrams.net draft plus PNG export that passes strict visual QA. Especially for paper figures or posters where the user wants the agent to read source materials, reuse extracted paper images or plots, and produce an editable draw.io draft + PNG export the user can keep editing directly in draw.io. Cross-platform (Windows, macOS, Linux). PNG export has a hard 60s timeout.
---

# Draw.io Research Figure Pipeline

## Purpose

This skill produces research visuals as a single deliverable:

1. An editable, readable `.drawio` draft plus one PNG export that passes strict visual QA. SVG/PDF are not exported (they cause unpredictable hangs in headless drawio).

The draw.io draft is not disposable. It must be good enough for the user to keep editing directly in draw.io and to use as a paper or poster figure on its own.

## Non-Negotiable Gates

Do not declare a figure ready until all gates pass:

1. **Asset gate:** If the task is based on a paper, poster, PDF, slides, Markdown notes, or experiment folder, inspect available figures/images/tables first and reuse useful visual assets instead of redrawing everything from scratch. This is mandatory, not optional.
2. **Editable draft gate:** Produce a `.drawio` that is meaningful and editable by itself. The user must be able to continue editing it in draw.io.
3. **Discovery gate:** Verify the drawio CLI is installed and locatable on this host. If not found, run the discovery script and surface install instructions (do not silently fail).
4. **Export gate:** Export PNG from the `.drawio` with a hard 60s timeout. SVG/PDF exports are intentionally skipped — headless drawio frequently hangs on those, and the PNG is sufficient for visual QA.
5. **Visual QA gate:** Open the exported PNG and inspect it visually. If text is clipped, occluded, distorted, overlapped, unreadable, misaligned, too small, or blocked by icons/shapes, fix the `.drawio`, re-export, and inspect again.
6. **No-blind-export gate:** Never say the PNG is ready just because files exist. The visual preview must be checked.

If any gate fails, repair the draw.io draft first. Do not declare the figure ready.

For research posters and paper figures, the asset gate must produce an `asset_manifest.md` before drawing begins. If relevant visual assets exist but are not used, `qa_notes.md` must explain why each was rejected.

## Privacy Rule

Never store API keys, tokens, auth JSON contents, private URLs, or user secrets inside the skill or generated figure files. Scripts may read credentials at runtime from environment variables or existing local auth files, but must not print them.

## Discovery & Setup

The drawio CLI must be present on the host before any export. This skill is cross-platform: Windows uses PowerShell scripts, macOS and Linux use bash scripts. The skill ships two discovery helpers and two exporters that share the same lookup logic.

### Mandatory preflight

Before invoking the exporter, run the discovery script for this host. If it returns a non-zero status, surface the install hint to the user — do not silently fall back to other skills, and do not hand back a stub PNG.

| Host | Discovery | Exporter |
|---|---|---|
| Windows | `@@SKILL_DIR@@/scripts/find_drawio.ps1` | `@@SKILL_DIR@@/scripts/export_drawio.ps1` |
| macOS / Linux | `bash @@SKILL_DIR@@/scripts/find_drawio.sh` | `bash @@SKILL_DIR@@/scripts/export_drawio.sh` |

### Lookup order (all scripts)

1. `$DRAWIO_EXE` environment variable (absolute path to the drawio binary).
2. `PATH` lookup via the platform-native command (`Get-Command` / `command -v`).
3. Per-OS common install locations (see script sources for the full list).
4. For Linux, a best-effort AppImage scan under `$HOME` and `/opt`.
5. For Windows, a best-effort scan under `%LOCALAPPDATA%\Microsoft\WinGet\Packages`.

### Installing drawio

If the discovery script exits non-zero, install drawio via the host's package manager and re-run discovery:

| Platform | Install command | Notes |
|---|---|---|
| Windows | `winget install drawio` or `choco install drawio` or download from https://www.drawio.com/ | Installer places `draw.io.exe` in `%LOCALAPPDATA%\Programs\draw.io\`. |
| macOS | `brew install --cask drawio` or download `.dmg` from https://www.drawio.com/ | Binary lives inside the `.app` bundle; the discovery script handles it. |
| Ubuntu / Debian | Download AppImage from https://www.drawio.com/ and `chmod +x`, **or** `sudo snap install drawio` | Recommended path: put the AppImage in `~/.local/bin/` and symlink as `drawio`. |
| Other Linux | `yay -S drawio` (Arch), `flatpak install drawio` | Same logic — the script's PATH and AppImage scan will pick them up. |

If installation is impossible, ask the user to confirm an alternative path or hand back the editable `.drawio` only (no PNG, no claim of completion).

## Default Output Folder

Use `image_draft/` by default. Never choose a generic test folder unless the user explicitly names it.

Recommended structure:

```text
image_draft/
  assets/                  # extracted paper images, plots, screenshots
  asset_manifest.md        # inventory of usable source visuals
  sketch.drawio            # editable semantic draft
  sketch.png               # visual QA preview (the only raster export)
  qa_notes.md              # visual QA checklist and fixes
```

If `image_draft/` already exists, create a versioned subfolder such as `image_draft/run_002/` unless the user asks to overwrite.

## Source Material Workflow

For research tasks, first build content from source materials:

- Read the paper/PDF/slides/notes enough to identify the actual method, problem setting, main claim, experimental evidence, and available figures.
- Treat user-provided screenshots/images in the conversation as source assets too: inspect them and reuse them when they contain useful paper figures, layouts, plots, or visual examples.
- Search local folders for `.pdf`, `.pptx`, `.md`, `.png`, `.jpg`, `.jpeg`, `.svg`, `.webp`, and figure asset folders.
- Run or manually create an asset inventory before sketching. Use `@@SKILL_DIR@@/scripts/inventory_assets.py` when possible.
- Extract or reuse relevant visual material:
  - method diagrams
  - robot/camera setup images
  - pipeline screenshots
  - result plots/tables
  - qualitative examples
  - ablation charts
- Put reused assets under `image_draft/assets/`.
- Insert useful assets into draw.io when they improve fidelity. Do not replace real paper figures with weak hand-drawn substitutes.
- For a paper poster, at least one relevant method/result/setup/qualitative asset should be inserted when such assets exist. If none are inserted, justify this explicitly in `qa_notes.md`.
- If the source paper includes figures that communicate the method, robot/camera setup, dataset, results, ablations, or qualitative examples, those figures have priority over newly invented icons or generic boxes.
- Keep figure assets as movable draw.io image objects where possible. If programmatic insertion is unreliable, use draw.io desktop or the draw.io browser editor to insert the images, then re-export and inspect.
- Use `@@SKILL_DIR@@/scripts/render_pdf_pages.py` when possible.

## Draw.io Draft Requirements

The draft must be clean:

- Fixed canvas size appropriate to the task, usually 16:9 for posters or `1536x1024`-like landscape.
- Stable grid: columns, rows, and section titles must align.
- No text under shapes, arrows, image crops, icons, badges, or panel borders.
- No text clipping or overflow.
- No ambiguous arrows.
- No title/body/media collisions.
- All panels must have enough internal padding.
- All labels must be concise and editable.
- Use real extracted paper figures/images where useful; embed or reference them in draw.io so the user can move/replace them.
- Do not create a generic diagram if the paper already provides relevant visual evidence. Use the paper's method figure, setup figure, result chart, or qualitative examples as visual anchors.
- Keep the draft independent: no "according to the paper", "from PDF", or "adapted from notes" in the visible figure.

For academic posters, prefer:

- A strong title band.
- 3-4 main sections.
- Method/architecture in the center.
- Real result numbers/plots on the right or bottom.
- Key takeaways in a dedicated strip.
- Paper images/robot setup/qualitative examples as visual anchors when available.

## Mandatory Visual QA Loop

After every draw.io export:

1. Open `sketch.png` with an image viewer or `view_image`.
2. Check at full-image scale and zoomed into dense regions.
3. Record pass/fail in `qa_notes.md`.
4. If fail, fix the `.drawio`, re-export, and inspect again.

QA checklist:

```text
- [ ] Title is readable and not clipped.
- [ ] Every panel title has a fixed area and does not overlap body text.
- [ ] Body text fits inside its box with padding.
- [ ] No image, icon, arrow, badge, or crop covers text.
- [ ] No text extends outside panel boundaries.
- [ ] All arrows point in the intended direction.
- [ ] Extracted figures/images are visible and not distorted.
- [ ] Relevant source assets were inserted, or each unused relevant asset is justified in `qa_notes.md`.
- [ ] Result numbers/axis labels are readable when included.
- [ ] The draft is useful as a standalone editable draw.io artifact, with all labels and structure understandable without external context.
```

Only after every item passes may the figure be declared ready.

## Export

Exports **PNG only**, with a **hard 60s timeout**. SVG and PDF exports are deliberately omitted — headless drawio frequently hangs on those, and the PNG is sufficient for visual QA of the raster preview. The editable `.drawio` stays the source of truth. Override the timeout via `-TimeoutSeconds` (PowerShell) or `-t` (bash) when justified.

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy Bypass -File "@@SKILL_DIR@@/scripts/export_drawio.ps1" `
  -DrawioPath "<image_draft>/sketch.drawio" `
  -OutDir "<image_draft>"
```

Flags:

| Flag | Default | Notes |
|---|---|---|
| `-DrawioPath` | required | Input `.drawio` file. |
| `-OutDir` | input's directory | Where the PNG is written. |
| `-Scale` | `1.5` | PNG render scale. |
| `-TimeoutSeconds` | `60` | Hard kill after this many seconds. Exit code `5` on timeout. |
| `-DrawioExe` | auto-discovered | Explicit path to `draw.io.exe`. |
| `-EmbedPngDiagram` | off | Embed diagram XML inside the PNG (large output). |

### macOS / Linux (bash)

```bash
bash "@@SKILL_DIR@@/scripts/export_drawio.sh" \
  -i "<image_draft>/sketch.drawio" \
  -o "<image_draft>"
```

Flags:

| Flag | Default | Notes |
|---|---|---|
| `-i` | required | Input `.drawio` file. |
| `-o` | input's directory | Where the PNG is written. |
| `-s` | `1.5` | PNG render scale. |
| `-t` | `60` | Hard timeout in seconds. Exit code `5` on timeout. Uses GNU `timeout` when available; otherwise runs an internal watchdog. |

### Behavior on timeout

If the export exceeds the timeout, the exporter kills the drawio process, deletes any partial PNG, and exits with code `5`. The agent should report timeout as a hard failure and either re-export with `-TimeoutSeconds` / `-t` raised, or hand back the editable `.drawio` only and explicitly flag that visual QA could not run.

### Discovered locations

Both exporters read `$DRAWIO_EXE` first, then search PATH and common install locations (see "Discovery & Setup" above). On Linux the AppImage is auto-discovered under `$HOME` and `/opt`.

## Final Response

Report:

- `.drawio`, `.png`, and `qa_notes.md` paths.
- Whether source figures/images were reused.
- Whether visual QA passed.
- Whether the PNG export completed within the 60s timeout budget (if it timed out, say so explicitly).

If visual QA did not pass, stop and report that the figure is not ready and describe what was fixed in the latest iteration.
