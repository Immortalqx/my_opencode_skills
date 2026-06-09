# figure-spec

Chinese version: [README.zh-CN.md](./README.zh-CN.md)

`figure-spec` generates deterministic, editable SVG diagrams from structured FigureSpec JSON. It is intended for publication-quality architecture, workflow, pipeline, audit cascade, and topology figures.

Use the `figure-spec` skill when you need a precise vector diagram whose layout should be reproducible:

```text
Use the figure-spec skill to create an editable SVG workflow diagram for this method.
```

## Dependency Note

No API key is required. The renderer runs locally from the bundled Python script.

## Workflow

1. Convert the diagram goal into structured FigureSpec JSON.
2. Validate the spec with the bundled renderer (`${CLAUDE_SKILL_DIR}/scripts/figure_renderer.py`).
3. Render SVG from the spec.
4. Inspect the SVG/PDF and revise the JSON, not the generated SVG.

## Helper Scripts

- `figure-spec/scripts/figure_renderer.py`: validates and renders FigureSpec JSON.

The skill resolves the script via `${CLAUDE_SKILL_DIR}` from inside `SKILL.md`, so it works no matter where the skill is installed.

## Contents

- `figure-spec/SKILL.md`: Claude skill definition.
- `figure-spec/scripts/`: deterministic renderer.
- The outer `README.md` and `README.zh-CN.md` are repository docs only and are not installed.

## Install

```bash
cp -r figure-spec/figure-spec/* ~/.claude/skills/figure-spec/
```

The skill is then available as `/figure-spec`.
