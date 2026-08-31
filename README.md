# Skill Evaluation Lab

A persistent, reproducible working environment for empirical testing and refinement of coding-agent skills.

Start here:

1. `00-SKILL-EVALUATION-LAB.md`
2. `CURRENT-STATE.md`
3. `CANONICAL/`
4. `EXPERIMENTS/`
5. `EVIDENCE/`
6. `DATA/runs.json`
7. `TOOLING/verification/`

The repository is organized around evidence, not polished outcomes. Supplied skills, candidate versions, failed runs, model limitations, preserved run records, hashes, analysis, and external research stay connected without being collapsed into one narrative.

The first study is `layered-codebase-architecture`, with canonical global runs `0001` through `0027` preserved. The current V2 artifact is experimental. EXP-0003 has a scored Grok 4.6 High responsibility-boundary holdout block. EXP-0004 has its GPT-5.1 first-model block preserved through `0027` and ready for scoring; the next unused global run is `0028`.

Run `py -3 TOOLING/verification/verify_lab.py` before trusting a changed current-state record.
