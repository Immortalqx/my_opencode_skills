---
name: novelty-check
description: "Verify research idea novelty against recent literature. Use when user says \"查新\", \"novelty check\", \"有没有人做过\", \"check novelty\", or wants to verify a research idea is novel before implementing."
argument-hint: <method-idea-description>
allowed-tools: WebSearch WebFetch
---

# Novelty Check Skill

Check whether a proposed method/idea has already been done in the literature: **$ARGUMENTS**

## Instructions

Given a method description, systematically verify its novelty:

### Phase A: Extract Key Claims

### Phase B: Multi-Source Literature Search

1. **Web Search** (via `WebSearch`):
   - Search arXiv, Google Scholar, Semantic Scholar
   - Use specific technical terms from the claim
   - Try at least 3 different query formulations per claim
   - Include year filters for 2024-2026

2. **Known paper databases**: Check against:
   - ICLR 2025/2026, NeurIPS 2025, ICML 2025/2026
   - Recent arXiv preprints (2025-2026)

3. **Read abstracts**: For each potentially overlapping paper, WebFetch its abstract and related work section

### Phase C: Evidence Synthesis

For each close paper, identify: - Which claim(s) it overlaps - Whether the overlap is in the method, problem setting, objective, data, or empirical finding - Whether the proposed difference is technical, experimental, or only a framing difference - What evidence supports the difference: abstract, method section, figures, experiments, or claims

### Phase D: Novelty Report

```markdown
## Novelty Check Report

### Proposed Method
[1-2 sentence description]

### Core Claims
1. [Claim 1] — Novelty: HIGH/MEDIUM/LOW — Closest: [paper]
2. [Claim 2] — Novelty: HIGH/MEDIUM/LOW — Closest: [paper]
...

### Closest Prior Work
| Paper | Year | Venue | Overlap | Key Difference |
|-------|------|-------|---------|----------------|

### Overall Novelty Assessment
- Score: X/10
- Recommendation: PROCEED / PROCEED WITH CAUTION / ABANDON
- Key differentiator: [what makes this unique, if anything]
- Risk: [closest prior-work threat]

### Suggested Positioning
[How to frame the contribution to maximize novelty perception]
```

### Important Rules
