# figure-description

Chinese version: [README.zh-CN.md](./README.zh-CN.md)

`figure-description` is a patent drafting skill for processing user-provided technical figures and producing formal drawing descriptions with reference numerals.

Use the `figure-description` skill when you have patent figures and want Claude to identify components, assign numerals, and generate drawing descriptions:

```text
Use the figure-description skill to process the figures under patent/figures/ for a CN invention patent.
```

## Dependency Note

No API key is required by the skill itself. It works from local figure files and patent drafting artifacts such as `patent/INVENTION_DISCLOSURE.md` and `patent/CLAIMS.md`.

## Workflow

1. Discover figure files in `patent/figures/`, `figures/`, or the workspace root.
2. Inspect each figure and identify components, connections, and flow.
3. Assign reference numerals by figure series.
4. Generate formal drawing descriptions for CN, US, or EP style.
5. Create a reference numeral index and consistency checklist.

## Contents

- `figure-description/SKILL.md`: Claude skill definition.
- The outer `README.md` and `README.zh-CN.md` are repository docs only and are not installed.

## Install

```bash
cp -r figure-description/figure-description/* ~/.claude/skills/figure-description/
```

The skill is then available as `/figure-description`.
