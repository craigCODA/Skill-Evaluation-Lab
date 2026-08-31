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

The first study is `layered-codebase-architecture`, with canonical global runs `0001` through `0027` preserved. The current V2 artifact is experimental. Future skills and variants continue the same global run sequence.

Binary result archives for runs `0001` through `0015` are durable release assets. Runs `0016` through `0027` currently have hash-recorded local archives only; their ZIPs are intentionally ignored under `ARCHIVES/local/` until published to a release or external artifact store.

Run `py -3 TOOLING/verification/verify_lab.py` before trusting a changed current-state record.
