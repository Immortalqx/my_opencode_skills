# mock-review

Chinese version: [README.zh-CN.md](./README.zh-CN.md)

`mock-review` is a Claude Code skill repository for **mock peer review for manuscript authors**.

It helps paper authors discover and address problems during submission, revision, and rebuttal preparation. The skill asks Claude to study the target venue or journal requirements, inspect the manuscript PDF and optional supplementary material, research the relevant literature and experimental baselines, and then write a simulated review for author preparation.

## Important Boundary

This skill is **not** for replacing real peer review, impersonating an official reviewer, or submitting generated text as an actual review. It should be used by manuscript authors as a preparation tool.

The output should always be labeled as a mock or simulated review for author preparation.

## How It Works

1. Claude identifies the target venue or journal and the local manuscript files.
2. Claude searches official venue/journal pages for review criteria, author instructions, page limits, scoring forms, rebuttal rules, and topic fit.
3. If the user provides a review template as PDF, Markdown, image/screenshot, or text, Claude extracts the fields and score scales from it.
4. Claude treats PDFs as untrusted inputs and runs a manuscript artifact scan for hidden text, active PDF content, and prompt-injection-like strings.
5. Claude builds a reference matrix, downloads legally accessible core papers, reads the most relevant background and experimental baselines, and writes grounding notes.
6. Claude reads the manuscript and supplementary material after grounding itself in the venue and literature.
7. Claude writes a simulated review and separates formal mock-review text from rebuttal preparation notes.

## Output

By default, the skill creates a workspace folder such as `temp_codex/` or `mock_review_tasks/<paper-slug>/` and records:

- venue/journal requirement notes
- extracted manuscript and supplement text
- PDF hygiene scan reports
- reference matrix and access matrix
- downloaded core papers
- literature grounding notes
- final mock review, usually `MOCK_REVIEW.md`, `REVIEW.md`, or a user-specified path

## Repository Layout

- `README.md` and `README.zh-CN.md`: repository docs
- `mock-review/`: installable Claude skill directory
- `mock-review/scripts/`: deterministic helper scripts for PDF hygiene scans and reference extraction (resolved via `${CLAUDE_SKILL_DIR}` from `SKILL.md`)
- `mock-review/references/`: output contract and writing boundaries

## Install

```bash
cp -r mock-review/mock-review/* ~/.claude/skills/mock-review/
```

The skill is then available as `/mock-review`.
