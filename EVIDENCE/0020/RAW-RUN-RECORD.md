# Run 0020 - supplied original forced EXP-0003 required rake pitch, Grok 4.6 High

- Date/time: 2026-08-31 CDT; exact archive timestamp is recorded in EVIDENCE/0020/archive-manifest.json
- Operator: Codex workplace operator
- Mode: supplied-original skill run
- Subject model + exact version: Grok 4.6 High from operator selection; the exported Cursor transcript does not independently encode the model identifier
- Model settings / tools: Cursor harness; raw internal agent transcript exported from the Cursor project store; exact reasoning/effort setting was not independently captured in the transcript
- Target repository: ShingleFile
- Target starting commit: cd393ddd60548823dabd6875060247693a22c1be
- Skill: layered-codebase-architecture
- Skill condition: supplied original (00-SUPPLIED)
- Skill invocation: forced
- Skill runtime path: %USERPROFILE%/.cursor/skills-cursor/layered-codebase-architecture/
- Skill version / SHA-256:

~~~text
SKILL_DIR=C:\Users\NeverAMoment\.cursor\skills-cursor\layered-codebase-architecture
093d1a371b695a8bdcf6bb2ae6bdd4c28b582ecd51ed1e4600db2630c7ae5221  conventions.md
0cd727e9ea67ed5410c07bde1ab5c19f50f09d71f6ae643b9ce19f91b487a969  MANIFEST.txt
306676f83773c6c1fb5c057113d0f0b67e61a31eaa05badf4730bd4de35ffb1c  RATIONALE.md
0cb645117d1916616bc0474a049820a1a833c60f82b38d7a2f209510436fe4d0  SKILL.md

~~~

## Change Request

Planned prompt from PROMPT.txt:

~~~text
In the roof quick calculator, a drawn rake can be put back on “Plan only,” and it still contributes to the totals like that is valid. Rake pitch is required; hip and valley pitch are optional.

Make an unpitched rake clearly incomplete and keep it out of the quick calculator totals until a pitch is selected. Do not change the line-drawing workflow or proposal/report behavior.


~~~

Cursor prompt as exported:

~~~text
/layered-codebase-architecture  In the roof quick calculator, a drawn rake can be put back on “Plan only,” and it still contributes to the totals like that is valid. Rake pitch is required; hip and valley pitch are optional.

Make an unpitched rake clearly incomplete and keep it out of the quick calculator totals until a pitch is selected. Do not change the line-drawing workflow or proposal/report behavior.

~~~

## Result Asset

- Archive filename: run-0020-grok46-original-exp0003-supplied.zip
- Archive SHA-256: d98b643a796532d9e147fd69d4a1931aeb0165250cf017dce391721b5c981f0c
- Archive location: ARCHIVES/local/run-0020-grok46-original-exp0003-supplied.zip
- Archive durability: local-only, publication pending; do not treat this ZIP as retrievable from a fresh clone until it is attached to a durable release/artifact store.

## Transcript/Trace

- EVIDENCE/0020/cursor-agent-transcript.raw.jsonl
- EVIDENCE/0020/cursor-agent-transcript.md
- EVIDENCE/0020/cursor-subagent-c261c7c6-30a8-4cef-88fa-fbb7afaeb1d4.raw.jsonl
- EVIDENCE/0020/cursor-subagent-c261c7c6-30a8-4cef-88fa-fbb7afaeb1d4.md
- EVIDENCE/0020/cursor-terminal-112313.txt
- EVIDENCE/0020/cursor-terminal-11506.txt
- EVIDENCE/0020/cursor-terminal-11507.txt
- EVIDENCE/0020/cursor-terminal-11508.txt
- EVIDENCE/0020/cursor-terminal-11509.txt

Transcript SHA-256:

~~~text
5c300b7f70a8df85d05c328c152efe20c2723ac1b50139de9b670c01f0011f3d  cursor-agent-transcript.raw.jsonl
85dbacba4f90668762a443f5ae623170e9a9835ff805e1ca1e6f9b354a6613ad  cursor-agent-transcript.md
0eac3b83a14bba24b87b9da587df9440662f97deeffde30de49e3803e5cc9fe5  cursor-subagent-c261c7c6-30a8-4cef-88fa-fbb7afaeb1d4.raw.jsonl
1dc8b77ce4845cebd0f7d0ba560f71286c472dbc9a5a4e267f8585a96c0912ac  cursor-subagent-c261c7c6-30a8-4cef-88fa-fbb7afaeb1d4.md
~~~

## Expected Pressure

Task 03 from EXP-0003-task03-required-rake-pitch: make an unpitched drawn rake clearly incomplete and keep it out of quick-calculator totals until a pitch is selected, while preserving the line-drawing workflow and proposal/report behavior.

## Outcome

The Active working tree at preservation contained two tracked modifications and two untracked paths:

~~~text
 M components/roof/RoofQuickLinearCalculator.vue
 M shared/roofLineMeasurements.ts
?? .cursor/
?? shared/roofLineMeasurements.test.ts
~~~

Tracked changed files before preservation:

~~~text
M	components/roof/RoofQuickLinearCalculator.vue
M	shared/roofLineMeasurements.ts
~~~

git diff --stat HEAD before preservation:

~~~text
 components/roof/RoofQuickLinearCalculator.vue | 67 +++++++++++++++++++++++++--
 shared/roofLineMeasurements.ts                | 17 ++++++-
 2 files changed, 80 insertions(+), 4 deletions(-)
~~~

Untracked files before preservation:

~~~text
.cursor/noun-map.md
shared/roofLineMeasurements.test.ts
~~~

git diff --check before preservation:

~~~text
(no whitespace errors)
~~~

## Verification

Archive verification completed before cleanup:

~~~text
testzip=OK
entry_count=679
has_git=True
archive_size=3484789
~~~

The archive was checked for transcript-related entries:

~~~text
matching_entries=0
~~~

The transcript is not inside the archive ZIP. It is preserved in EVIDENCE/0020 beside the archive evidence.

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
tests: 8 passed, 0 failed
~~~

No independent browser/runtime click-through verification was preserved by Codex.

Active HEAD before preservation:

~~~text
cd393ddd60548823dabd6875060247693a22c1be
~~~

diff.patch contains tracked changes only. untracked-files.txt records .cursor/noun-map.md and shared/roofLineMeasurements.test.ts; both are included in the full archive ZIP.

## Observed Trace Events

Observed transcript events only, without architecture-quality scoring:

- Cursor began with the forced /layered-codebase-architecture invocation and inlined supplied-original skill content.
- Cursor used an explore subagent to map rake pitch flow, totals, and affected consumers.
- Cursor created .cursor/noun-map.md in the subject repository.
- Cursor changed shared/roofLineMeasurements.ts and components/roof/RoofQuickLinearCalculator.vue.
- Cursor added shared/roofLineMeasurements.test.ts.
- Cursor ran npx tsx --test shared/roofLineMeasurements.test.ts, which passed eight tests.
- Cursor did not preserve browser/runtime manual verification.

## Suspected Skill Gap (Hypothesis)

Not evaluated in this preservation step. This run is preserved as the supplied-original EXP-0003 first arm for later scoring against the rubric.

## Next Experiment

Clear Active and recreate it from Mother, then run 0021 as the no-skill control with no layered-codebase-architecture folder present in Cursor global skills-cursor directory.
