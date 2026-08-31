# Run 0022 - candidate V1 forced EXP-0003 required rake pitch, Grok 4.6 High

- Date/time: 2026-08-31 CDT; exact archive timestamp is recorded in EVIDENCE/0022/archive-manifest.json
- Operator: Codex workplace operator
- Mode: candidate V1 skill run
- Subject model + exact version: Grok 4.6 High from operator selection; the exported Cursor transcript does not independently encode the model identifier
- Model settings / tools: Cursor harness; raw internal agent transcript exported from the Cursor project store; exact reasoning/effort setting was not independently captured in the transcript
- Target repository: ShingleFile
- Target starting commit: cd393ddd60548823dabd6875060247693a22c1be
- Skill: layered-codebase-architecture
- Skill condition: candidate V1 (01-V1-CANDIDATE)
- Skill invocation: forced
- Skill runtime path: %USERPROFILE%/.cursor/skills-cursor/layered-codebase-architecture/
- Skill version / SHA-256:

~~~text
SKILL_DIR=C:\Users\NeverAMoment\.cursor\skills-cursor\layered-codebase-architecture
c997e0659a92f00671a4931523b038f34357a6121012a8f88f4bb53c3bbda2b7  conventions.md
ef50b3c6a661e01ed761df5815fa90f263c032c8d6f38da6eeb14413f6a9844d  FROM-00.diff
f76b8a0326f0d00b099e322f8ae12ca367cf7551747397d648599bc4e0525f11  MANIFEST.txt
ca59bf6ac18818ecf3977c389d521f8b99f46d0cd663fd538ae4335351aa4e7c  RATIONALE.md
7f760abe7228a62d1a7abf37b20f5b87a2b9ea0711431260300231bd0f630414  SKILL.md
~~~

## Change Request

Planned prompt from PROMPT.txt:

~~~text
In the roof quick calculator, a drawn rake can be put back on “Plan only,” and it still contributes to the totals like that is valid. Rake pitch is required; hip and valley pitch are optional.

Make an unpitched rake clearly incomplete and keep it out of the quick calculator totals until a pitch is selected. Do not change the line-drawing workflow or proposal/report behavior.

~~~

Cursor prompt as exported:

~~~text
\n/layered-codebase-architecture  the roof quick calculator, a drawn rake can be put back on “Plan only,” and it still contributes to the totals like that is valid. Rake pitch is required; hip and valley pitch are optional.\n\nMake an unpitched rake clearly incomplete and keep it out of the quick calculator totals until a pitch is selected. Do not change the line-drawing workflow or proposal/report behavior.\n
~~~

## Result Asset

- Archive filename: run-0022-grok46-v1-exp0003-candidate.zip
- Archive SHA-256: 0e6e419c2621a0bdb95b5e34ea0c7215884c6b78737e874b7f747b4298dfc0de
- Archive location: ARCHIVES/local/run-0022-grok46-v1-exp0003-candidate.zip
- Archive durability: local-only, publication pending; do not treat this ZIP as retrievable from a fresh clone until it is attached to a durable release/artifact store.

## Transcript/Trace

- EVIDENCE/0022/cursor-agent-transcript.raw.jsonl
- EVIDENCE/0022/cursor-agent-transcript.md
- EVIDENCE/0022/cursor-terminal-711261.txt
- EVIDENCE/0022/cursor-terminal-711262.txt
- EVIDENCE/0022/cursor-terminal-711263.txt
- EVIDENCE/0022/cursor-terminal-711264.txt
- EVIDENCE/0022/cursor-terminal-711265.txt
- EVIDENCE/0022/cursor-terminal-711266.txt
- EVIDENCE/0022/cursor-terminal-711267.txt
- EVIDENCE/0022/cursor-terminal-711268.txt
- EVIDENCE/0022/cursor-terminal-711269.txt
- EVIDENCE/0022/cursor-terminal-711270.txt

Transcript SHA-256:

~~~text
e3a6c627f8c1efe7b706726a4e69231a7cd86a5cc7ef9fd58a4471413303fc10  cursor-agent-transcript.raw.jsonl
3ae92ab0c5e99360fc90dd561a27dfd379bf3b98dded93f44e9e131bd571e1c1  cursor-agent-transcript.md
~~~

## Expected Pressure

Task 03 from EXP-0003-task03-required-rake-pitch: make an unpitched drawn rake clearly incomplete and keep it out of quick-calculator totals until a pitch is selected, while preserving the line-drawing workflow and proposal/report behavior.

## Outcome

The Active working tree at preservation contained two tracked modifications and one untracked path:

~~~text
 M components/roof/RoofQuickLinearCalculator.vue
 M shared/roofLineMeasurements.ts
?? shared/roofLineMeasurements.test.ts
~~~

Tracked changed files before preservation:

~~~text
M	components/roof/RoofQuickLinearCalculator.vue
M	shared/roofLineMeasurements.ts
~~~

Untracked files before preservation:

~~~text
shared/roofLineMeasurements.test.ts
~~~

git diff --stat HEAD before preservation:

~~~text
 components/roof/RoofQuickLinearCalculator.vue | 51 ++++++++++++++++++++++++---
 shared/roofLineMeasurements.ts                | 18 +++++++++-
 2 files changed, 64 insertions(+), 5 deletions(-)
~~~

git diff --check before preservation:

~~~text
(no whitespace errors)
~~~

## Verification

Archive verification completed before cleanup:

~~~text
testzip=OK
entry_count=678
has_git=True
archive_size=3483249
~~~

The archive was checked for transcript-related entries:

~~~text
matching_entries=0
~~~

The transcript is not inside the archive ZIP. It is preserved in EVIDENCE/0022 beside the archive evidence.

The archive was checked for generated dependency/build directories:

~~~text
node_modules=False
.nuxt=False
.output=False
~~~

Cursor terminal verification preserved for this run includes:

~~~text
npx tsx --test shared/roofLineMeasurements.test.ts
exit_code: 0
tests: 4 passed, 0 failed
~~~

A second preserved terminal run also records the same domain test command passing four tests.

The transcript records an attempted npx nuxt typecheck command, but the separately preserved terminal evidence does not contain a successful typecheck result. Preserved terminal evidence instead records node_modules missing and nuxt not installed. No independent browser/runtime click-through verification was preserved by Codex.

Active HEAD before preservation:

~~~text
cd393ddd60548823dabd6875060247693a22c1be
~~~

diff.patch contains tracked changes only. untracked-files.txt records shared/roofLineMeasurements.test.ts; it is included in the full archive ZIP.

## Observed Trace Events

Observed transcript events only, without architecture-quality scoring:

- Cursor began with the forced /layered-codebase-architecture invocation and inlined V1 skill content.
- Cursor read the V1 conventions file and searched for rake pitch, plan-only, totals, and pitch-helper consumers.
- Cursor changed shared/roofLineMeasurements.ts and components/roof/RoofQuickLinearCalculator.vue.
- Cursor added shared/roofLineMeasurements.test.ts.
- Cursor ran npx tsx --test shared/roofLineMeasurements.test.ts twice, with the preserved logs showing four passing tests each time.
- Cursor attempted to typecheck the Nuxt project, but no successful typecheck terminal log was preserved and local node_modules/nuxt were absent.
- Cursor did not preserve browser/runtime manual verification.

## Suspected Skill Gap (Hypothesis)

Not evaluated in this preservation step. This run is preserved as the candidate V1 EXP-0003 first-model arm for later scoring against the rubric.

## Next Experiment

Clear Active and recreate it from Mother, then run 0023 with V2 installed in Cursor global skills-cursor directory and a forced /layered-codebase-architecture invocation.
