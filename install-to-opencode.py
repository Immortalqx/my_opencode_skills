#!/usr/bin/env python3
"""install-to-opencode.py — two-stage migration tool for my_opencode_skills.

Stage 1 (--rewrite): turn specific source strings into @@SKILL_DIR@@ placeholders.
Stage 2 (--install, default): copy each skill to the opencode skills dir and
                              substitute placeholders with absolute paths.

Both stages are dry-run by default; pass --apply to actually write.

Examples
--------
    # Dry-run: show what would be installed.
    python install-to-opencode.py

    # Actually install to ~/.config/opencode/skills/.
    python install-to-opencode.py --apply

    # Install one skill to a custom target.
    python install-to-opencode.py --skill arxiv --target D:/my-skills --apply

    # Rewrite the source in place (committable).
    python install-to-opencode.py --rewrite --apply

    # Run the unit tests.
    python install-to-opencode.py --test
"""

from __future__ import annotations

import argparse
import dataclasses
import re
import shutil
import sys
import unittest
from collections.abc import Iterable
from pathlib import Path

try:
    import yaml
except ImportError:
    print("error: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


REPO_ROOT = Path(__file__).resolve().parent
RULES_PATH = REPO_ROOT / "migration-rules.yaml"

PLACEHOLDER_SINGLE = "@@SKILL_DIR@@"
PLACEHOLDER_CROSS = re.compile(r"@@SKILL_DIR:(?P<skill>[\w-]+)@@")


# =============================================================================
# Data classes
# =============================================================================


@dataclasses.dataclass
class RewriteRule:
    id: str
    find: str | None
    regex: str | None
    replace: str
    apply_to: tuple[str, ...]
    multiline: bool = False

    def matches(self, suffix: str) -> bool:
        # suffix like ".md", ".py"
        for pat in self.apply_to:
            # simple glob: "*.md" -> endswith ".md"
            if pat.startswith("*."):
                if suffix.endswith(pat[1:]):
                    return True
        return False

    def apply(self, text: str) -> tuple[str, int]:
        if self.regex:
            flags = re.MULTILINE if self.multiline else 0
            new, n = re.subn(self.regex, self.replace, text, flags=flags)
            return new, n
        if self.find is None:
            return text, 0
        return text.replace(self.find, self.replace), text.count(self.find)


@dataclasses.dataclass
class Rules:
    rewrite_rules: list[RewriteRule]
    install_target: str
    in_skill_subdirs: tuple[str, ...]
    cross_skill_pattern: re.Pattern
    single_skill_pattern: str
    validation: dict
    exclude_skills: tuple[str, ...]
    modes: dict[str, dict]

    @classmethod
    def load(cls, path: Path) -> Rules:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        install = data.get("install", {})
        rewrite = data.get("rewrite_rules", [])
        validation = data.get("validation", {})

        rules = []
        for r in rewrite:
            rules.append(
                RewriteRule(
                    id=r["id"],
                    find=r.get("find"),
                    regex=r.get("regex"),
                    replace=r.get("replace", ""),
                    apply_to=tuple(r.get("apply_to", ["*.md"])),
                    multiline=r.get("multiline", False),
                )
            )

        cross_pat = re.compile(install["cross_skill_pattern"])
        modes_raw = data.get("modes", {})
        # Normalize: ensure every mode has the 5 required keys
        modes: dict[str, dict] = {}
        for name, cfg in modes_raw.items():
            modes[name] = {
                "description": cfg.get("description", ""),
                "target": cfg.get("target"),
                "skills": cfg.get("skills"),
                "require_target": bool(cfg.get("require_target", False)),
                "allow_skill": bool(cfg.get("allow_skill", False)),
                "requires_skill": bool(cfg.get("requires_skill", False)),
            }
        return cls(
            rewrite_rules=rules,
            install_target=install["default_target"],
            in_skill_subdirs=tuple(install["in_skill_subdirs"]),
            cross_skill_pattern=cross_pat,
            single_skill_pattern=install["single_skill_pattern"],
            validation=validation,
            exclude_skills=tuple(data.get("exclude_skills", [])),
            modes=modes,
        )


# =============================================================================
# Source scanning
# =============================================================================


@dataclasses.dataclass
class Skill:
    name: str
    path: Path

    def find_files(self) -> dict[str, Path]:
        """Map relative path (POSIX) to absolute path for every file in the skill."""
        out: dict[str, Path] = {}
        for p in self.path.rglob("*"):
            if p.is_file():
                out[p.relative_to(self.path).as_posix()] = p
        return out


def discover_skills(source: Path, exclude: Iterable[str]) -> list[Skill]:
    out: list[Skill] = []
    excluded = set(exclude)
    for p in sorted(source.iterdir()):
        if not p.is_dir():
            continue
        if p.name in excluded:
            continue
        if not (p / "SKILL.md").exists():
            continue
        out.append(Skill(name=p.name, path=p))
    return out


# =============================================================================
# Stage 1 — REWRITE
# =============================================================================


@dataclasses.dataclass
class RewriteResult:
    files_changed: int
    replacements: dict[str, int] = dataclasses.field(default_factory=dict)
    details: list[tuple[str, str, int]] = dataclasses.field(default_factory=list)

    def total(self) -> int:
        return sum(self.replacements.values())


def rewrite_skill(skill: Skill, rules: Rules, apply: bool, verbose: bool) -> RewriteResult:
    result = RewriteResult(files_changed=0)
    errors: list[str] = []

    for path in skill.path.rglob("*"):
        if not path.is_file():
            continue
        if not path.suffix:
            continue
        rel = path.relative_to(skill.path).as_posix()
        suffix = path.suffix

        # Only process text-like suffixes
        if suffix.lower() not in (".md", ".markdown", ".py", ".sh", ".ps1", ".js", ".ts", ".txt", ".yaml", ".yml", ".toml", ".json"):
            continue

        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"  skip (non-UTF-8): {rel}")
            continue

        new = original
        rule_counts: dict[str, int] = {}
        for rule in rules.rewrite_rules:
            if not rule.matches(suffix):
                continue
            new, n = rule.apply(new)
            if n:
                rule_counts[rule.id] = n

        if not rule_counts:
            continue

        result.files_changed += 1
        result.details.append((rel, " ".join(f"{k}={v}" for k, v in rule_counts.items()),
                               sum(rule_counts.values())))
        for k, v in rule_counts.items():
            result.replacements[k] = result.replacements.get(k, 0) + v

        if apply:
            path.write_text(new, encoding="utf-8")

    if errors:
        result.details.append(("--- encoding errors ---", "", 0))
        result.details.extend((e, "", 0) for e in errors)
    return result


# =============================================================================
# Stage 2 — INSTALL
# =============================================================================


@dataclasses.dataclass
class InstallResult:
    skills_installed: list[str] = dataclasses.field(default_factory=list)
    skills_skipped: list[str] = dataclasses.field(default_factory=list)
    skills_failed: list[tuple[str, str]] = dataclasses.field(default_factory=list)
    substitutions: dict[str, int] = dataclasses.field(default_factory=dict)
    warnings: list[str] = dataclasses.field(default_factory=list)

    def total_subs(self) -> int:
        return sum(self.substitutions.values())


def _apply_rewrite_rules_to_text(text: str, suffix: str, rules: Rules) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    for rule in rules.rewrite_rules:
        if not rule.matches(suffix):
            continue
        text, n = rule.apply(text)
        if n:
            counts[rule.id] = n
    return text, counts


def _substitute_in_skill_paths(text: str, skill: Skill, suffix: str) -> tuple[str, int]:
    """Replace bare `scripts/<file>`, `references/<file>`, `assets/<file>` with
    `@@SKILL_DIR@@/<that path>` for every file that actually exists in the skill.

    Only operates on .md / .markdown files. Python and other code files might
    contain the string `scripts/<file>` inside docstring examples (e.g.,
    `python scripts/foo.py`) and substituting those would produce nonsense
    in code comments.

    Skips occurrences that are part of a cross-skill reference (e.g.,
    `@@SKILL_DIR:other@@/scripts/foo.py`) — those are resolved by the cross-skill
    stage, and double-substitution would produce a path with two prefixes.

    Returns (new_text, num_replacements).
    """
    if suffix.lower() not in (".md", ".markdown"):
        return text, 0
    files = skill.find_files()
    n_total = 0

    # Sort by path length DESC so longer matches win (e.g.,
    # "scripts/office/unpack.py" before "scripts/unpack.py" — both are real files).
    for rel in sorted(files, key=len, reverse=True):
        if "/" not in rel:
            continue
        sub, _, fname = rel.partition("/")
        if sub not in ("scripts", "references", "assets"):
            continue
        placeholder = f"{PLACEHOLDER_SINGLE}/{rel}"
        if placeholder in text:
            continue  # already substituted
        # Replace each occurrence but skip those preceded by @@SKILL_DIR:<name>@@/
        # (i.e. a cross-skill reference where the path is appended after a `@@/`
        # separator).
        new_text = text
        i = 0
        while True:
            j = new_text.find(rel, i)
            if j < 0:
                break
            # Look at the text right before the path: it must end with
            # `@@SKILL_DIR:<name>@@/` for this to be a cross-skill reference.
            preceding = new_text[max(0, j - 64):j]
            if re.search(r"@@SKILL_DIR:[\w-]+@@/$", preceding):
                i = j + 1
                continue
            new_text = new_text[:j] + placeholder + new_text[j + len(rel):]
            n_total += 1
            i = j + len(placeholder)
        text = new_text
    return text, n_total


def _substitute_cross_skill_refs(text: str, all_skill_names: set[str], target_root: Path) -> tuple[str, int]:
    """Replace @@SKILL_DIR:<name>@@ with the absolute path of that skill in target.

    Names not in all_skill_names are left as-is and a warning is recorded by
    the caller (cross_skill_strategy: soft).
    """
    n = 0
    unknown: list[str] = []

    def _replace(m: re.Match) -> str:
        nonlocal n
        name = m.group("skill")
        if name not in all_skill_names:
            unknown.append(name)
            return m.group(0)
        n += 1
        return (target_root / name).as_posix()

    new = PLACEHOLDER_CROSS.sub(_replace, text)
    if unknown:
        # surface unknown names via a sentinel substring; caller scans for it
        new += f"\n<!-- opencode-migration-warn: unknown-skills={','.join(sorted(set(unknown)))} -->\n"
    return new, n


def _substitute_single(text: str, target_skill_dir: Path) -> tuple[str, int]:
    n = text.count(PLACEHOLDER_SINGLE)
    new = text.replace(PLACEHOLDER_SINGLE, target_skill_dir.as_posix())
    return new, n


def _preview_skill(args: argparse.Namespace) -> int:
    """Print what <SKILL>/SKILL.md would look like after install substitutions."""
    rules = Rules.load(args.rules)
    target_root = Path(args.target).expanduser() if args.target else Path(rules.install_target).expanduser()
    skills = discover_skills(args.source, rules.exclude_skills)
    skill = next((s for s in skills if s.name == args.preview), None)
    if not skill:
        print(f"error: skill {args.preview!r} not found in {args.source}", file=sys.stderr)
        return 2

    all_names = {s.name for s in skills}
    skill_md = skill.path / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    text, _ = _apply_rewrite_rules_to_text(text, ".md", rules)
    text, _ = _substitute_in_skill_paths(text, skill, ".md")
    text, _ = _substitute_cross_skill_refs(text, all_names, target_root)
    text, _ = _substitute_single(text, target_root / skill.name)
    text = re.sub(r"\n?<!-- opencode-migration-warn:.*?-->\n?", "\n", text)
    print(text)
    return 0


def _validate_skill_text(
    name: str,
    text: str,
    rules: Rules,
    warnings: list[str],
    in_skill_subs: int = 0,
) -> None:
    for s in rules.validation.get("must_be_zero_per_skill_md", []):
        # Use word-boundary regex to avoid substring false positives
        # e.g. "x_temp_claude" should not match "temp_claude"
        if re.search(rf"\b{re.escape(s)}\b", text):
            warnings.append(f"[{name}] SKILL.md still contains {s!r}")
    # If the SKILL.md uses scripts/references/assets references but neither
    # in-skill substitution ran nor a SKILL_DIR placeholder exists, something
    # was missed. (Cross-skill references like @@SKILL_DIR:other@@/... count
    # as "handled" since they will be resolved by the cross-skill stage.)
    uses_subresources = any(p in text for p in ("scripts/", "references/", "assets/"))
    has_placeholder = PLACEHOLDER_SINGLE in text or "@@SKILL_DIR:" in text
    if uses_subresources and in_skill_subs == 0 and not has_placeholder:
        warnings.append(
            f"[{name}] SKILL.md references scripts/references/assets "
            f"but no @@SKILL_DIR marker was added"
        )


def _process_skill(
    skill: Skill,
    target_root: Path,
    all_skill_names: set[str],
    rules: Rules,
    apply: bool,
    force: bool,
    warnings: list[str],
) -> tuple[str, int, int, int]:
    """Returns (status, in_skill_subs, cross_skill_subs, single_subs).
    status is one of: 'installed', 'skipped', 'failed'.
    """
    target = target_root / skill.name
    if target.exists():
        if not force:
            return "skipped", 0, 0, 0
        if apply:
            shutil.rmtree(target)
    if apply:
        target.mkdir(parents=True, exist_ok=True)

    in_subs = cross_subs = single_subs = 0
    try:
        for src_file in skill.path.rglob("*"):
            if not src_file.is_file():
                continue
            rel = src_file.relative_to(skill.path)
            dst_file = target / rel
            if apply:
                dst_file.parent.mkdir(parents=True, exist_ok=True)

            # Only process text-like files; copy binary as-is
            if src_file.suffix.lower() not in (
                ".md", ".markdown", ".py", ".sh", ".ps1", ".js", ".ts", ".txt",
                ".yaml", ".yml", ".toml", ".json", ".html", ".css", ".svg",
            ):
                if apply:
                    shutil.copy2(src_file, dst_file)
                continue

            try:
                text = src_file.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                warnings.append(f"[{skill.name}] non-UTF-8 file copied as binary: {rel}")
                if apply:
                    shutil.copy2(src_file, dst_file)
                continue

            suffix = src_file.suffix

            # Stage 1 (in-memory): apply rewrite rules (so unrewritten sources work)
            text, _ = _apply_rewrite_rules_to_text(text, suffix, rules)

            # Stage 2a: substitute in-skill file references
            text, n = _substitute_in_skill_paths(text, skill, suffix)
            in_subs += n

            # Validate SKILL.md BEFORE cross-skill substitution so the
            # @@SKILL_DIR:<name>@@ marker is still present in the text.
            if src_file.name == "SKILL.md":
                _validate_skill_text(skill.name, text, rules, warnings, in_subs)

            # Stage 2b: substitute cross-skill references
            text, n = _substitute_cross_skill_refs(text, all_skill_names, target_root)
            cross_subs += n

            # Stage 2c: substitute the @@SKILL_DIR@@ placeholder with absolute path.
            # `target` is already target_root / skill.name, so we use `target` directly.
            text, n = _substitute_single(text, target)
            single_subs += n

            # Strip sentinel comments that may have been added
            text = re.sub(r"\n?<!-- opencode-migration-warn:.*?-->\n?", "\n", text)

            if apply:
                # Compare against the source: if nothing changed, just copy
                # (preserves original line endings, encoding, and timestamps).
                # Otherwise write the substituted text with `newline=""` to
                # avoid Windows CRLF translation of LF-normalized input.
                src_text = src_file.read_text(encoding="utf-8")
                if text == src_text:
                    shutil.copy2(src_file, dst_file)
                else:
                    dst_file.write_text(text, encoding="utf-8", newline="")
            # In dry-run we do NOT create any files; the summary tells the user
            # what would change.

        return "installed", in_subs, cross_subs, single_subs

    except Exception as e:
        warnings.append(f"[{skill.name}] install failed: {e}")
        return "failed", in_subs, cross_subs, single_subs


def install_all(
    source: Path,
    target_arg: str | None,
    rules: Rules,
    apply: bool,
    force: bool,
    skill_filter: list[str] | None,
    verbose: bool,
) -> InstallResult:
    target_root = Path(target_arg).expanduser() if target_arg else Path(rules.install_target).expanduser()
    skills = discover_skills(source, rules.exclude_skills)
    if skill_filter:
        wanted = set(skill_filter)
        skills = [s for s in skills if s.name in wanted]

    all_names = {s.name for s in skills}
    result = InstallResult()

    if not skills:
        result.warnings.append("no skills found in source")
        return result

    if not apply and not target_root.exists():
        # dry-run: don't create target_root
        pass
    elif apply:
        target_root.mkdir(parents=True, exist_ok=True)

    for skill in skills:
        status, in_n, cross_n, single_n = _process_skill(
            skill, target_root, all_names, rules, apply, force, result.warnings
        )
        if status == "installed":
            result.skills_installed.append(skill.name)
            result.substitutions[f"{skill.name}:in_skill"] = in_n
            result.substitutions[f"{skill.name}:cross_skill"] = cross_n
            result.substitutions[f"{skill.name}:placeholder"] = single_n
        elif status == "skipped":
            result.skills_skipped.append(skill.name)
        else:
            result.skills_failed.append((skill.name, status))

    return result


# =============================================================================
# CLI
# =============================================================================


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="install-to-opencode",
        description="Migrate my_opencode_skills to opencode. Default mode is install.",
    )
    p.add_argument("--source", type=Path, default=REPO_ROOT,
                   help="source repo root (default: script's parent dir)")
    p.add_argument("--target", type=str, default=None,
                   help="install root (default: mode-dependent, usually ~/.config/opencode/skills)")
    p.add_argument("--rules", type=Path, default=RULES_PATH,
                   help="path to migration-rules.yaml")
    p.add_argument("--rewrite", action="store_true",
                   help="rewrite source files in place instead of installing")
    p.add_argument("--install", dest="do_install", action="store_true",
                   help="install mode (default; explicit for clarity)")
    p.add_argument("--skill", action="append", default=None,
                   help="restrict to one skill (can repeat). Only valid with --mode select.")
    p.add_argument("--force", action="store_true",
                   help="overwrite existing target skill dir")
    p.add_argument("--apply", action="store_true",
                   help="actually write files (default: dry-run)")
    p.add_argument("--verbose", "-v", action="store_true",
                   help="verbose output")
    p.add_argument("--test", action="store_true",
                   help="run self-tests and exit")
    p.add_argument("--preview", metavar="SKILL", default=None,
                   help="print the post-substitution SKILL.md of <SKILL> to stdout and exit")
    p.add_argument("--mode", choices=["default", "all", "select", "literature-survey", "mock-review"],
                   default="default",
                   help="install mode preset (default: default = only install mmx-cli to global)")
    return p.parse_args(argv)


def print_rewrite_summary(results: dict[str, RewriteResult], apply: bool) -> None:
    print(f"\n{'==' * 30}")
    print(f"REWRITE {'(applied)' if apply else '(dry-run)'}")
    print(f"{'==' * 30}")
    total_files = 0
    total_subs = 0
    by_rule: dict[str, int] = {}
    for skill, r in results.items():
        if r.files_changed == 0:
            continue
        total_files += r.files_changed
        total_subs += r.total()
        for k, v in r.replacements.items():
            by_rule[k] = by_rule.get(k, 0) + v
        print(f"  {skill}: {r.files_changed} files, {r.total()} replacements")
        if r.total() <= 6:
            for f, rule_summary, n in r.details:
                print(f"      {f}  ({rule_summary})")
    print()
    print(f"Total: {total_files} files changed, {total_subs} replacements")
    if by_rule:
        print("By rule:")
        for k, v in sorted(by_rule.items()):
            print(f"  {k}: {v}")


def print_install_summary(
    result: InstallResult,
    apply: bool,
    target_root: Path,
    mode_name: str,
    skill_filter: list[str] | None,
) -> None:
    skills_desc = (
        "all" if skill_filter is None
        else f"{len(skill_filter)} selected: {', '.join(skill_filter)}"
    )
    print(f"\n{'==' * 30}")
    print(f"INSTALL  mode={mode_name}  target={target_root}  skills={skills_desc}  {'(applied)' if apply else '(dry-run)'}")
    print(f"{'==' * 30}")
    print(f"Installed: {len(result.skills_installed)}")
    for s in result.skills_installed:
        subs = sum(v for k, v in result.substitutions.items() if k.startswith(f"{s}:"))
        print(f"  {s}: {subs} substitutions")
    if result.skills_skipped:
        print(f"Skipped (already exists, use --force to overwrite): {len(result.skills_skipped)}")
        for s in result.skills_skipped:
            print(f"  {s}")
    if result.skills_failed:
        print(f"Failed: {len(result.skills_failed)}")
        for s, why in result.skills_failed:
            print(f"  {s}: {why}")
    if result.warnings:
        print(f"\nWarnings ({len(result.warnings)}):")
        for w in result.warnings:
            print(f"  {w}")


# =============================================================================
# Self-tests
# =============================================================================


class TestSubstitution(unittest.TestCase):
    def setUp(self) -> None:
        self.rules = Rules.load(RULES_PATH)

    def test_rewrite_claude_var(self) -> None:
        text = "run python ${CLAUDE_SKILL_DIR}/scripts/foo.py"
        new, n = _apply_rewrite_rules_to_text(text, ".md", self.rules)
        self.assertEqual(n, {"claude-skill-dir-var": 1})
        self.assertIn("@@SKILL_DIR@@", new)
        self.assertNotIn("${CLAUDE_SKILL_DIR}", new)

    def test_rewrite_idempotent(self) -> None:
        text = "use @@SKILL_DIR@@/scripts/foo.py"
        new, n = _apply_rewrite_rules_to_text(text, ".md", self.rules)
        self.assertEqual(n, {})
        self.assertEqual(new, text)

    def test_rename_temp_claude(self) -> None:
        text = "save to temp_claude/scans and x_temp_*"
        new, n = _apply_rewrite_rules_to_text(text, ".md", self.rules)
        self.assertIn("x_temp", new)
        self.assertNotIn("temp_claude", new)
        # x_temp_* should NOT be re-substituted
        self.assertIn("x_temp_*", new)

    def test_drop_argument_hint(self) -> None:
        text = "argument-hint: <foo>\nname: x\n"
        new, n = _apply_rewrite_rules_to_text(text, ".md", self.rules)
        self.assertNotIn("argument-hint", new)
        self.assertIn("name: x", new)

    def test_drop_arguments(self) -> None:
        text = "Search: $ARGUMENTS"
        new, n = _apply_rewrite_rules_to_text(text, ".md", self.rules)
        self.assertNotIn("$ARGUMENTS", new)
        self.assertIn("user's most recent request", new)

    def test_in_skill_substitution(self) -> None:
        # Create a fake skill with a scripts/ subdir
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            skill_path = Path(tmp) / "fake-skill"
            (skill_path / "scripts").mkdir(parents=True)
            (skill_path / "scripts" / "foo.py").write_text("# foo")
            (skill_path / "references").mkdir(parents=True)
            (skill_path / "references" / "bar.md").write_text("# bar")
            skill = Skill(name="fake-skill", path=skill_path)
            text = "use scripts/foo.py and references/bar.md"
            new, n = _substitute_in_skill_paths(text, skill, ".md")
            self.assertEqual(n, 2)
            self.assertIn("@@SKILL_DIR@@/scripts/foo.py", new)
            self.assertIn("@@SKILL_DIR@@/references/bar.md", new)

    def test_in_skill_substitution_skips_cross_skill(self) -> None:
        """Bare `scripts/foo.py` that is part of a `@@SKILL_DIR:other@@/...`
        reference must NOT be substituted to the current skill's path."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            skill_path = Path(tmp) / "fake-skill"
            (skill_path / "scripts").mkdir(parents=True)
            (skill_path / "scripts" / "foo.py").write_text("# foo")
            skill = Skill(name="fake-skill", path=skill_path)
            # The `scripts/foo.py` is preceded by @@SKILL_DIR:other@@
            text = "use @@SKILL_DIR:other@@/scripts/foo.py but also scripts/foo.py alone"
            new, n = _substitute_in_skill_paths(text, skill, ".md")
            # Only the standalone one should be substituted; the cross-skill one is left alone
            self.assertEqual(n, 1)
            self.assertIn("@@SKILL_DIR:other@@/scripts/foo.py", new)
            self.assertIn("@@SKILL_DIR@@/scripts/foo.py", new)

    def test_cross_skill_substitution(self) -> None:
        all_names = {"arxiv", "mock-review"}
        with _temp_skill_root() as root:
            text = "see @@SKILL_DIR:arxiv@@/scripts/foo.py and @@SKILL_DIR:unknown@@/x.py"
            new, n = _substitute_cross_skill_refs(text, all_names, root)
            self.assertIn("arxiv", new)  # known
            self.assertIn("unknown", new)  # unknown kept
            self.assertIn("opencode-migration-warn", new)

    def test_single_substitution(self) -> None:
        with _temp_skill_root() as root:
            target = root / "arxiv"
            text = "scripts path is @@SKILL_DIR@@/scripts/x.py"
            new, n = _substitute_single(text, target)
            self.assertEqual(n, 1)
            self.assertIn(str(target.as_posix()), new)


from contextlib import contextmanager  # noqa: E402


@contextmanager
def _temp_skill_root():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)


# =============================================================================
# main
# =============================================================================


# =============================================================================
# main
# =============================================================================


def _resolve_mode(
    args: argparse.Namespace, rules: Rules
) -> tuple[str, list[str] | None, str]:
    """Apply --mode preset and run the 5 validation rules. Return (target_str,
    skill_filter, mode_name) for install_all() to consume.

    Validation rules (in order):
      1. --skill requires --mode select (no implicit promotion)
      2. mode does not allow --skill  (catches --mode all --skill foo etc.)
      3. mode requires --skill         (catches --mode select without --skill)
      4. mode requires --target        (catches --mode literature-survey w/o --target)
      5. target resolution: --target > mode preset > rules.install_target
      6. skill filter resolution: --skill > mode preset; '~' / null handled
    """
    # Rule 1: --skill must be paired with --mode select
    if args.skill and args.mode != "select":
        print(
            f"error: --skill 仅在 --mode select 下有效（当前 --mode {args.mode}）",
            file=sys.stderr,
        )
        sys.exit(2)

    if args.mode not in rules.modes:
        # Defensive: argparse already constrains this, but YAML could be edited
        print(f"error: unknown --mode {args.mode!r}", file=sys.stderr)
        sys.exit(2)

    mode_cfg = rules.modes[args.mode]

    # Rule 2: mode forbids --skill
    if not mode_cfg["allow_skill"] and args.skill:
        print(
            f"error: --mode {args.mode} 不允许 --skill", file=sys.stderr
        )
        sys.exit(2)

    # Rule 3: mode requires --skill
    if mode_cfg["requires_skill"] and not args.skill:
        print(
            f"error: --mode {args.mode} 必须配合 --skill <name>（可重复）",
            file=sys.stderr,
        )
        sys.exit(2)

    # Rule 4: mode requires --target
    if mode_cfg["require_target"] and not args.target:
        print(
            f"error: --mode {args.mode} 必须配合 --target <path> 指定项目目录",
            file=sys.stderr,
        )
        sys.exit(2)

    # Rule 5: target resolution
    if args.target:
        target_str = args.target
    elif mode_cfg["target"]:
        target_str = mode_cfg["target"]
    else:
        # Should be unreachable given rule 4
        target_str = rules.install_target

    # Rule 6: skill filter resolution
    if mode_cfg["skills"] is None:
        # Skills come from --skill (select mode); args.skill is guaranteed non-empty
        # by rule 3, but keep a defensive fallback.
        skill_filter = list(args.skill) if args.skill else None
    elif mode_cfg["skills"] == "~":
        # '~' = all discovered skills
        skill_filter = None
    else:
        skill_filter = list(mode_cfg["skills"])

    return target_str, skill_filter, args.mode


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.preview:
        return _preview_skill(args)

    if args.test:
        # Configure argv to skip pytest discovery quirks
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(TestSubstitution)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        return 0 if result.wasSuccessful() else 1

    rules = Rules.load(args.rules)

    if args.rewrite and args.do_install:
        print("error: --rewrite and --install are mutually exclusive", file=sys.stderr)
        return 2

    if args.rewrite:
        skills = discover_skills(args.source, rules.exclude_skills)
        if args.skill:
            wanted = set(args.skill)
            skills = [s for s in skills if s.name in wanted]
        results: dict[str, RewriteResult] = {}
        for skill in skills:
            results[skill.name] = rewrite_skill(skill, rules, args.apply, args.verbose)
        print_rewrite_summary(results, args.apply)
        return 0

    # Resolve mode preset (5 validation rules + target/skills resolution)
    target_str, skill_filter, mode_name = _resolve_mode(args, rules)

    # default: install
    result = install_all(
        source=args.source,
        target_arg=target_str,
        rules=rules,
        apply=args.apply,
        force=args.force,
        skill_filter=skill_filter,
        verbose=args.verbose,
    )
    target_root = Path(target_str).expanduser()
    print_install_summary(result, args.apply, target_root, mode_name, skill_filter)
    return 0 if not result.skills_failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
