# Skill Evaluation Lab

## Purpose

This repository is the canonical working environment for empirical evaluation and refinement of coding-agent skills.

Skills are treated as executable behavioral instructions, not documents to improve by intuition.

Every retained change must be traceable to preserved evidence.

## Core laws

1. Current state may change. Preserved evidence does not.
2. A later conclusion may supersede an earlier conclusion. It does not rewrite what was known when the earlier conclusion was recorded.
3. Unpreserved run state is not evidence.
4. Failed runs are evidence. Preserve them before cleanup or reset.
5. `CANONICAL/` answers what should be used now.
6. `SKILLS/` preserves how a skill evolved.
7. `EXPERIMENTS/` defines controlled questions and conditions.
8. `EVIDENCE/` records what happened.
9. `DEVELOPMENT-HISTORY/` records what was concluded at that point in time.
10. `REPORTS/` are derived communication artifacts, never the source of truth.
11. Run numbers are global across every skill in this repository.
12. Experiment numbers are global. Skill version numbers are local to the skill.
13. Canonical public history may exclude imported material that is not accepted as preserved run evidence.
14. Excluded material is not referenced by current-state docs, run indexes, release assets, or checksum manifests.
15. If canonical material is removed, run numbers are collapsed so current public numbering remains contiguous.

## Source Of Truth

`CURRENT-STATE.md` states the operational truth right now.

`CANONICAL/` contains the current skill artifact to use.

`SKILLS/` preserves skill version history and version rationale.

`EXPERIMENTS/` defines research questions, conditions, run indexes, and scoring rubrics.

`EVIDENCE/` contains factual run records.

`DEVELOPMENT-HISTORY/` contains time-local interpretation.

`REPORTS/` contains derived human-facing summaries.

`RESEARCH/` contains outside references and unresolved research questions.

No report, transcript claim, or model summary replaces preserved evidence.

## Coordinates

A result is identified by three independent coordinates: Skill, Experiment, Run.

## New-agent start sequence

Read `CURRENT-STATE.md`, then the current artifact under `CANONICAL/`, then the active experiment, then only the evidence needed for the question being answered.

Do not reconstruct current state by reading history backward if `CURRENT-STATE.md` already states it.
