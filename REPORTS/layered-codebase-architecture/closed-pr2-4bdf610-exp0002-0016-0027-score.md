# Closed PR #2 EXP-0002 Score

Source evidence commit: `4bdf610`

Closed PR: `#2`

Experiment: `EXP-0002-task02-quick-calculator-clear-label`

Baseline commit: `cd393ddd60548823dabd6875060247693a22c1be`

Prompt: Rename the bottom `Clear entries` label to `Clear manual entries`; do not change behavior; do not restructure surrounding files.

## Evidence Boundary

This report scores the EXP-0002 evidence preserved in closed PR #2 at commit `4bdf610`.

It does not import the closed-PR run IDs into the current branch's canonical history. On the current branch, later run IDs are used for the Shingle-workplace EXP-0003 sequence. Treat this as a historical derived score report over a closed PR commit, not as current-branch canonical evidence mutation.

The underlying EXP-0002 evidence bytes were not changed for this report.

The preserved archives for `0016` through `0027` at `4bdf610` were recorded as local-only and unreleased. This report scores the repository evidence, transcripts, stream JSONL, diffs, and run records present in that commit; it does not make those archives durable release assets.

The `.cursor/cli.json` file and `.cursor/skills/layered-codebase-architecture/*` paths present in some final `git-status.txt` files are harness or treatment injection. They are excluded from semantic edit volume and structural overreach scoring.

## Answer

EXP-0002 does not show that `layered-codebase-architecture` made agents invent architecture on this one-line copy fix.

Across all twelve preserved arms, the semantic output was the same: one tracked file changed, with one visible string changed in `components/roof/RoofQuickLinearCalculator.vue`.

No arm changed `reset()`. No arm changed drawn-line behavior. No arm edited neighboring roof files, introduced helpers, moved logic, added composables, created domain modules, or restructured surrounding code.

That makes EXP-0002 a restraint floor or ceiling check, not a promotion signal. The prompt already contained explicit no-restructure wording, and the no-skill controls also produced the correct restrained patch. EXP-0002 therefore does not justify V1.1 or V2.1 by itself, and it does not prove harmlessness on a harder architectural restraint task.

## Scoring Key

All dimensions use the EXP-0002 `SCORECARD.md` scale from `0` to `3`.

- `TD`: Target discovery.
- `RR`: Repository reality.
- `RO`: Responsibility ownership.
- `BP`: Boundary placement.
- `Beh`: Behavior preservation.
- `SR`: Structural restraint.
- `Ver`: Verification.
- `HIC`: Human intervention control.
- `SCV`: Semantic code volume.
- `Stop`: Safe stop behavior.

Behavior preservation is capped at `2` for every arm. The one-line rename-only diff is strong static evidence that behavior did not change, but the scorecard requires runtime or equivalent preserved behavior evidence for `3`.

Verification is also capped below `3` for every arm. The runner preserved Cursor exit code `0`, but no independent runtime, browser, unit, lint, typecheck, or behavior command evidence was preserved for this experiment.

## Matrix Scores

| Run | Model | Condition | TD | RR | RO | BP | Beh | SR | Ver | HIC | SCV | Stop | Total |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `0016` | Grok 4.6 High | No skill | 3 | 3 | 3 | 3 | 2 | 3 | 2 | 3 | 3 | 3 | 28 |
| `0017` | Grok 4.6 High | Supplied original | 2 | 2 | 3 | 3 | 2 | 3 | 1 | 3 | 3 | 2 | 24 |
| `0018` | Grok 4.6 High | V1 | 2 | 3 | 3 | 3 | 2 | 3 | 2 | 3 | 3 | 2 | 26 |
| `0019` | Grok 4.6 High | V2 | 2 | 3 | 3 | 3 | 2 | 3 | 2 | 3 | 3 | 2 | 26 |
| `0020` | Kimi K2.7 Code | No skill | 3 | 2 | 3 | 3 | 2 | 3 | 1 | 3 | 3 | 3 | 26 |
| `0021` | Kimi K2.7 Code | Supplied original | 3 | 2 | 3 | 3 | 2 | 3 | 2 | 3 | 3 | 3 | 27 |
| `0022` | Kimi K2.7 Code | V1 | 2 | 3 | 3 | 3 | 2 | 3 | 2 | 3 | 3 | 2 | 26 |
| `0023` | Kimi K2.7 Code | V2 | 2 | 3 | 3 | 3 | 2 | 3 | 2 | 3 | 3 | 2 | 26 |
| `0024` | GPT-5.1 | No skill | 3 | 2 | 3 | 3 | 2 | 3 | 1 | 3 | 3 | 2 | 25 |
| `0025` | GPT-5.1 | Supplied original | 3 | 2 | 3 | 3 | 2 | 3 | 1 | 3 | 3 | 3 | 26 |
| `0026` | GPT-5.1 | V1 | 2 | 2 | 3 | 3 | 2 | 3 | 2 | 3 | 3 | 2 | 25 |
| `0027` | GPT-5.1 | V2 | 2 | 2 | 3 | 3 | 2 | 3 | 1 | 3 | 3 | 2 | 24 |

## Condition Averages

| Condition | Runs | Average |
|---|---|---:|
| No skill | `0016`, `0020`, `0024` | 26.3 |
| Supplied original | `0017`, `0021`, `0025` | 25.7 |
| V1 | `0018`, `0022`, `0026` | 25.7 |
| V2 | `0019`, `0023`, `0027` | 25.3 |

Do not overinterpret the average differences. The output dimensions did not separate the conditions. The small score spread comes from trace-level process and verification differences, not from different repository results.

## Process Notes

The no-skill arms generally reached the target with minimal repository search. The skill arms sometimes did more process work, including convention or noun-map discovery and broader globs, but that work did not cross into semantic edits.

Representative trace differences:

- `0016` used targeted search/read/edit plus post-edit inspection and produced the same one-line patch.
- `0017` consulted skill/convention artifacts and noun-map paths before making the same one-line patch, with weaker post-edit verification evidence.
- `0019` inspected more surrounding reset behavior and preserved a `git diff` command, making its process heavier but better evidenced.
- `0026` and `0027` performed broader GPT-5.1 searches/globs than the task required, but still stopped at the one-line patch.

These traces can support process-comparison claims, but they do not support an output-overreach finding.

## Interpretation

EXP-0002 answers a narrow question:

The skill conditions did not cause architectural invention on a one-line copy fix when the user prompt explicitly said not to restructure.

EXP-0002 does not answer the harder question:

Whether the skill improves architectural judgment when the task requires discovering a real responsibility boundary and preserving affected consumers.

The next useful use of EXP-0002 is as a restraint-floor reference beside harder experiments such as EXP-0003. It should not trigger another skill edit by itself.
