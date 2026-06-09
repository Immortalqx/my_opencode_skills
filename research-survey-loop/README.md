# research-survey-loop

Chinese version: [README.zh-CN.md](./README.zh-CN.md)

`research-survey-loop` is a standalone Claude Code skill repository for long-running, multi-round survey workflows. It is mainly tuned for Robotics, Embodied AI, computer vision, world models, navigation, manipulation, and nearby topics.

## How It Works

1. The user sends a prompt with a survey topic and optional local materials.
2. Claude creates or resumes a persistent survey task.
3. Claude works round by round. Different rounds may search sources, read papers, absorb local materials, refine categories, and expand the survey.
4. The user later tells Claude which round to continue, or asks it to continue the next round.

Example follow-up:

```text
Continue round 2 for the same topic based on current_task.md and round_log.md.
```

## Source Strategy

The skill combines:

- task-local and workspace-local PDFs,
- public web search and official venue / publisher pages,
- bundled helper scripts for task initialization, source normalization, and chunked PDF reading (resolved via `${CLAUDE_SKILL_DIR}` from `SKILL.md`),
- public Semantic Scholar and arXiv APIs for normalized metadata when needed.

The default path stays within one agent plus bundled local scripts and public web sources.

## Output

The skill maintains a persistent workflow under `survey_tasks/<topic-slug>/` and updates:

- `task.md`
- `round_log.md`
- `current_task.md`
- `survey.md`

## Repository Layout

- `README.md` and `README.zh-CN.md`: repository docs
- `research-survey-loop/`: installable Claude skill directory
- `research-survey-loop/scripts/`: bundled helper scripts (init, fetch, chunked PDF reader)
- `research-survey-loop/references/`: source priority and writing rules
- `research-survey-loop/assets/`: task, round log, current task, and survey templates

## Install

```bash
cp -r research-survey-loop/research-survey-loop/* ~/.claude/skills/research-survey-loop/
```

The skill is then available as `/research-survey-loop`.
