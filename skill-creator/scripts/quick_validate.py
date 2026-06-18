#!/usr/bin/env python3
"""
Quick validation script for opencode skills - minimal version.

Validates the SKILL.md frontmatter against opencode's published rules:
https://opencode.ai/docs/skills/

opencode-recognized frontmatter fields are: name, description, license,
compatibility, metadata. Unknown fields are silently ignored by opencode, but
this script flags them so authors do not carry over fields from Codex
(`allowed-tools`, `display_name`, `default_prompt`, `icon_small`, `brand_color`,
etc.) or other ecosystems by accident.

This script is a smoke test, not a quality gate. It does not check the body
for accuracy, the description for trigger quality, or the bundled resources
for correctness.
"""

import re
import sys
from pathlib import Path

import yaml

MAX_SKILL_NAME_LENGTH = 64

# Fields opencode actually reads from SKILL.md frontmatter. Anything else
# (e.g. `allowed-tools`, `display_name`, `default_prompt`, `icon_small`,
# `brand_color`, `short-description`) is a leak from Codex / Claude Code and
# should be removed on port.
OPENCODE_FRONTMATTER_FIELDS = {"name", "description", "license", "compatibility", "metadata"}


def validate_skill(skill_path):
    """Basic validation of an opencode skill."""
    skill_path = Path(skill_path)

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    unexpected_keys = set(frontmatter.keys()) - OPENCODE_FRONTMATTER_FIELDS
    if unexpected_keys:
        allowed = ", ".join(sorted(OPENCODE_FRONTMATTER_FIELDS))
        unexpected = ", ".join(sorted(unexpected_keys))
        return (
            False,
            f"Unexpected key(s) in SKILL.md frontmatter: {unexpected}. "
            f"opencode-recognized fields are: {allowed}. "
            f"Strip Codex/Claude Code fields like `allowed-tools`, `display_name`, "
            f"`default_prompt`, `icon_small`, `brand_color` on port.",
        )

    if "name" not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if "description" not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    name = frontmatter.get("name", "")
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name):
            return (
                False,
                f"Name '{name}' should be hyphen-case "
                f"(lowercase letters, digits, and hyphens; "
                f"regex ^[a-z0-9]+(-[a-z0-9]+)*$)",
            )
        if len(name) > MAX_SKILL_NAME_LENGTH:
            return (
                False,
                f"Name is too long ({len(name)} characters). "
                f"Maximum is {MAX_SKILL_NAME_LENGTH} characters.",
            )

    description = frontmatter.get("description", "")
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        if "<" in description or ">" in description:
            return False, "Description cannot contain angle brackets (< or >)"
        if len(description) > 1024:
            return (
                False,
                f"Description is too long ({len(description)} characters). "
                f"Maximum is 1024 characters.",
            )

    return True, "Skill is valid!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)
    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
