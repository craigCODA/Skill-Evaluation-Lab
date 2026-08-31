# Run 0021 - no-skill control EXP-0003 required rake pitch, Grok 4.6 High

- Date/time: 2026-08-31 CDT; exact archive timestamp is recorded in EVIDENCE/0021/archive-manifest.json
- Operator: Codex workplace operator
- Mode: no-skill control run
- Subject model + exact version: Grok 4.6 High from operator selection; the exported Cursor transcript does not independently encode the model identifier
- Model settings / tools: Cursor harness; raw internal agent transcript exported from the Cursor project store; exact reasoning/effort setting was not independently captured in the transcript
- Target repository: ShingleFile
- Target starting commit: cd393ddd60548823dabd6875060247693a22c1be
- Skill: layered-codebase-architecture
- Skill condition: no-skill control (NO-SKILL)
- Skill invocation: none
- Skill runtime path: absent from %USERPROFILE%/.cursor/skills-cursor/layered-codebase-architecture/
- Skill version / SHA-256: not applicable; the global skill folder was absent

## Change Request

Planned prompt from PROMPT.txt:

~~~text
In the roof quick calculator, a drawn rake can be put back on “Plan only,” and it still contributes to the totals like that is valid. Rake pitch is required; hip and valley pitch are optional.

Make an unpitched rake clearly incomplete and keep it out of the quick calculator totals until a pitch is selected. Do not change the line-drawing workflow or proposal/report behavior.


~~~

Cursor prompt as exported:

~~~text
In the roof quick calculator, a drawn rake can be put back on “Plan only,” and it still contributes to the totals like that is valid. Rake pitch is required; hip and valley pitch are optional.

Make an unpitched rake clearly incomplete and keep it out of the quick calculator totals until a pitch is selected. Do not change the line-drawing workflow or proposal/report behavior.

~~~

## Result Asset

- Archive filename: run-0021-grok46-no-skill-exp0003-control.zip
- Archive SHA-256: 1633e40e65901604f105bb2d66ad7c7fa2cabf502216a9a66a7cbd650a6959ac
- Archive location: ARCHIVES/local/run-0021-grok46-no-skill-exp0003-control.zip
- Archive durability: local-only, publication pending; do not treat this ZIP as retrievable from a fresh clone until it is attached to a durable release/artifact store.

## Transcript/Trace

- EVIDENCE/0021/cursor-agent-transcript.raw.jsonl
- EVIDENCE/0021/cursor-agent-transcript.md
- EVIDENCE/0021/cursor-terminal-998129.txt
- EVIDENCE/0021/cursor-terminal-998130.txt
- EVIDENCE/0021/cursor-terminal-998131.txt
- EVIDENCE/0021/cursor-terminal-998132.txt
- EVIDENCE/0021/cursor-terminal-998133.txt

Transcript SHA-256:

~~~text
8d9c4031dbde4b2ae22ca02c6d3cb7a34fe6b2d03447e35dcd7adb1e5c0009dc  cursor-agent-transcript.raw.jsonl
09de917ec67eb9aad100237df3b00d187a4cffe06444cf536713ec76ee688fd9  cursor-agent-transcript.md
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

git diff --stat HEAD before preservation:

~~~text
 components/roof/RoofQuickLinearCalculator.vue | 48 ++++++++++++++++++++++++---
 shared/roofLineMeasurements.ts                | 10 ++++++
 2 files changed, 53 insertions(+), 5 deletions(-)
~~~

Untracked files before preservation:

~~~text
(none)
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
archive_size=3483216
~~~

The archive was checked for transcript-related entries:

~~~text
matching_entries=0
~~~

The transcript is not inside the archive ZIP. It is preserved in EVIDENCE/0021 beside the archive evidence.

The archive was checked for generated dependency/build directories:

~~~text
node_modules=False
.nuxt=False
.output=False
~~~

Cursor terminal verification preserved for this run includes an environment check only:

~~~text
node_modules: absent
.nuxt: absent
exit_code: 0
~~~

No independent test, typecheck, build, or browser/runtime verification was preserved by Codex for this run.

Active HEAD before preservation:

~~~text
cd393ddd60548823dabd6875060247693a22c1be
~~~

diff.patch contains tracked changes only. untracked-files.txt is empty because no untracked subject files were present at preservation.

## Observed Trace Events

Observed transcript events only, without architecture-quality scoring:

- Cursor began with the plain EXP-0003 prompt and no /layered-codebase-architecture invocation.
- Cursor searched the repository for rake pitch, plan-only, quick calculator totals, and shared measurement logic.
- Cursor changed shared/roofLineMeasurements.ts and components/roof/RoofQuickLinearCalculator.vue.
- Cursor did not create untracked subject-repository files.
- Cursor did not preserve an independent test, typecheck, build, or browser verification command.

## Suspected Skill Gap (Hypothesis)

Not evaluated in this preservation step. This run is preserved as the no-skill EXP-0003 control arm for later scoring against the rubric.

## Next Experiment

Clear Active and recreate it from Mother, then run 0022 with V1 installed in Cursor global skills-cursor directory and a forced /layered-codebase-architecture invocation.
