# formula-derivation

Chinese version: [README.zh-CN.md](./README.zh-CN.md)

`formula-derivation` helps turn loose research-theory notes into a coherent derivation line. It is for building and structuring formulas, not for checking a finished theorem-proof package.

Use the `formula-derivation` skill when you need to clarify assumptions, define the right object, separate identities from approximations, or write a paper-ready derivation skeleton:

```text
Use the formula-derivation skill to organize these notes into a paper-style derivation.
```

## Dependency Note

No API key is required.

## Workflow

1. Freeze the target phenomenon and claim.
2. Choose the invariant object that the derivation should revolve around.
3. Put assumptions and notation first.
4. Classify each step as identity, proposition, approximation, or interpretation.
5. Produce either an internal derivation note, a paper-style theory draft, or a blocker report.

## Contents

- `formula-derivation/SKILL.md`: Claude skill definition.
- The outer `README.md` and `README.zh-CN.md` are repository docs only and are not installed.

## Install

```bash
cp -r formula-derivation/formula-derivation/* ~/.claude/skills/formula-derivation/
```

The skill is then available as `/formula-derivation`.
