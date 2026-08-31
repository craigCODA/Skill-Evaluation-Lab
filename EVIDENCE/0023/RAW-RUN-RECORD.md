# Run 0023 - candidate V2 forced EXP-0003 required rake pitch, Grok 4.6 High

- Date/time: 2026-08-31 CDT; exact archive timestamp is recorded in EVIDENCE/0023/archive-manifest.json
- Operator: Codex workplace operator
- Mode: candidate V2 skill run
- Subject model + exact version: Grok 4.6 High from operator selection; the exported Cursor transcript does not independently encode the model identifier
- Model settings / tools: Cursor harness; raw internal agent transcript exported from the Cursor project store; exact reasoning/effort setting was not independently captured in the transcript
- Target repository: ShingleFile
- Target starting commit: cd393ddd60548823dabd6875060247693a22c1be
- Skill: layered-codebase-architecture
- Skill condition: candidate V2 (02-V2-GRAPH)
- Skill invocation: forced
- Skill runtime path: %USERPROFILE%/.cursor/skills-cursor/layered-codebase-architecture/
- Skill version / SHA-256:

~~~text
SKILL_DIR=C:\Users\NeverAMoment\.cursor\skills-cursor\layered-codebase-architecture
80c872938a34e4b2eb12c7b8c071fdd38ea9f131881d5961d7a2543bc2355507  conventions.md
5952129d23b4c8e8e3a0324db2aa5088b84da50a044413828b563b2790f94f86  DESIGN-SPEC.md
67431e25df154c67a36ae05f1791d16315dde114a0cb09435a6a5b58926f6578  FROM-01.diff
65d0f7c542b853db8c5d22b0eafc1aac34f447e8370a9352d502aca1cd8ef6ed  MANIFEST.txt
38e3d9066aa1d3ca692764136035743a243ea4bc50acf484567f72b687ea42cd  RATIONALE.md
339d9e8a57e302dea561b6dccea44a56f6228f48c2d26c4629f7f7ba1be03ae0  SKILL.md
c82a4e82f37b9f1b67a532a21e7659c0f48e197f45f08e62aa111202f0c49b67  SOURCE-MANIFEST.txt
~~~

## Change Request

Planned prompt from PROMPT.txt:

~~~text
In the roof quick calculator, a drawn rake can be put back on “Plan only,” and it still contributes to the totals like that is valid. Rake pitch is required; hip and valley pitch are optional.

Make an unpitched rake clearly incomplete and keep it out of the quick calculator totals until a pitch is selected. Do not change the line-drawing workflow or proposal/report behavior.

~~~

Cursor prompt as exported:

~~~text
\n/layered-codebase-architecture  In the roof quick calculator, a drawn rake can be put back on “Plan only,” and it still contributes to the totals like that is valid. Rake pitch is required; hip and valley pitch are optional.\n\nMake an unpitched rake clearly incomplete and keep it out of the quick calculator totals until a pitch is selected. Do not change the line-drawing workflow or proposal/report behavior.\n
~~~

## Result Asset

- Archive filename: run-0023-grok46-v2-exp0003-candidate.zip
- Archive SHA-256: eeb536453f088a4ab2357d1c8d02248bf880332ac14be85f08916229a7fc6975
- Archive location: ARCHIVES/local/run-0023-grok46-v2-exp0003-candidate.zip
- Archive durability: local-only, publication pending; do not treat this ZIP as retrievable from a fresh clone until it is attached to a durable release/artifact store.

## Transcript/Trace

- EVIDENCE/0023/cursor-agent-transcript.raw.jsonl
- EVIDENCE/0023/cursor-agent-transcript.md
- EVIDENCE/0023/cursor-terminal-1.txt
- EVIDENCE/0023/cursor-terminal-879171.txt
- EVIDENCE/0023/cursor-terminal-879172.txt
- EVIDENCE/0023/cursor-terminal-879173.txt
- EVIDENCE/0023/cursor-terminal-879174.txt
- EVIDENCE/0023/cursor-terminal-879175.txt
- EVIDENCE/0023/cursor-terminal-879176.txt
- EVIDENCE/0023/cursor-terminal-879177.txt
- EVIDENCE/0023/cursor-terminal-879178.txt

Transcript SHA-256:

~~~text
605859ff7845c51c0b79e5d1542a63a24ce232ba39bd5eeff8f673ec744a521b  cursor-agent-transcript.raw.jsonl
e1b6d44596de0782188edc28175d6477f95491cc33be25193a4fcde40cc8726e  cursor-agent-transcript.md
~~~

## Expected Pressure

Task 03 from EXP-0003-task03-required-rake-pitch: make an unpitched drawn rake clearly incomplete and keep it out of quick-calculator totals until a pitch is selected, while preserving the line-drawing workflow and proposal/report behavior.

## Outcome

The Active working tree at preservation contained two tracked modifications and no untracked paths:

~~~text
 M components/roof/RoofQuickLinearCalculator.vue
 M shared/roofLineMeasurements.ts
~~~

Tracked changed files before preservation:

~~~text
M	components/roof/RoofQuickLinearCalculator.vue
M	shared/roofLineMeasurements.ts
~~~

Untracked files before preservation:

~~~text
(none)
~~~

git diff --stat HEAD before preservation:

~~~text
 components/roof/RoofQuickLinearCalculator.vue | 32 ++++++++++++++++++++++++---
 shared/roofLineMeasurements.ts                |  8 ++++++-
 2 files changed, 36 insertions(+), 4 deletions(-)
~~~

git diff --check before preservation:

~~~text
(no whitespace errors)
~~~

## Verification

Archive verification completed before cleanup:

~~~text
testzip=OK
entry_count=677
has_git=True
archive_size=3483205
~~~

The archive was checked for transcript-related entries:

~~~text
matching_entries=0
~~~

The transcript is not inside the archive ZIP. It is preserved in EVIDENCE/0023 beside the archive evidence.

The archive was checked for generated dependency/build directories:

~~~text
node_modules=False
.nuxt=False
.output=False
~~~

Cursor terminal verification preserved for this run includes an inline domain check:

~~~text
npx tsx -e "...roofLineMeasurementTotals..."
exit_code: 0
rakeNoPitchComplete: false
rakePitchedComplete: true
hipNoPitchComplete: true
rakeNoPitchAdjusted: 10
rake total: 11.180339887498949
~~~

The transcript records an attempted npm run typecheck command, but no successful typecheck terminal log was preserved. Preserved terminal evidence records nuxt missing and no node_modules. No independent browser/runtime click-through verification was preserved by Codex.

Active HEAD before preservation:

~~~text
cd393ddd60548823dabd6875060247693a22c1be
~~~

diff.patch contains tracked changes only. untracked-files.txt is empty because no untracked subject files were present at preservation.

## Observed Trace Events

Observed transcript events only, without architecture-quality scoring:

- Cursor began with the forced /layered-codebase-architecture invocation and inlined V2 skill content.
- Cursor searched for rake, plan-only, pitch, totals, related consumers, and style tokens.
- Cursor changed shared/roofLineMeasurements.ts and components/roof/RoofQuickLinearCalculator.vue.
- Cursor did not create untracked subject-repository files.
- Cursor ran an inline npx tsx domain check that the preserved terminal log shows exited 0.
- Cursor attempted npm run typecheck, but no successful typecheck terminal log was preserved and local node_modules/nuxt were absent.
- Cursor did not preserve browser/runtime manual verification.

## Suspected Skill Gap (Hypothesis)

Not evaluated in this preservation step. This run is preserved as the candidate V2 EXP-0003 first-model arm for later scoring against the rubric.

## Next Experiment

The Grok 4.6 High four-arm EXP-0003 block is now ready for scoring. Do not add another model block until this block is scored and there is a reason to spend the additional runs.
