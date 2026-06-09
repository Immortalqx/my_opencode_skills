# mmx-cli

English | [中文](./README.zh-CN.md)

`mmx-cli` is a Claude Code skill that wraps the local `mmx` command-line interface from the [MiniMax CLI](https://github.com/MiniMax-AI/cli) project. It lets Claude use `mmx` for text, image, video, speech, music, web search, vision, quota, file, and schema-export workflows.

Use this skill when you want Claude to operate through the local `mmx` command-line interface:

```text
Use the mmx-cli skill to run a MiniMax CLI dry run for an image generation request and show me the request JSON.
```

For token-sensitive checks, ask Claude to use `--dry-run`, `--quiet`, `--output json`, and `--non-interactive`.

## Installable Directory

The installable Claude skill is:

```text
mmx-cli/mmx-cli/
```

Do not install the outer `mmx-cli/` folder. It contains repository README files only.

## Contents

- `mmx-cli/SKILL.md`: Claude skill definition, kept aligned with the upstream MiniMax CLI skill.

## Prerequisite

Install and configure the MiniMax CLI before using the skill:

```bash
npm install -g mmx-cli
mmx auth status
```

## Install

```bash
cp -r mmx-cli/mmx-cli/* ~/.claude/skills/mmx-cli/
```

The skill is then available as `/mmx-cli`.
