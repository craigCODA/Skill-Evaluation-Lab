# Run 0025 - no-skill control EXP-0004 open valley metal charge, GPT-5.1

- Date/time: 2026-08-31 CDT; exact archive timestamp is recorded in EVIDENCE/0025/archive-manifest.json
- Operator: Codex workplace operator
- Mode: no-skill control run
- Subject model + exact version: GPT-5.1 from operator selection; the exported Cursor transcript does not independently encode the model identifier
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
When I choose an open valley and enter the footage, the estimate shows a valley metal amount but the customer total and roofing proposal ignore it. Open valley metal is a customer charge.
~~~

Cursor prompt as exported:

~~~text
When I choose an open valley and enter the footage, the estimate shows a valley metal amount but the customer total and roofing proposal ignore it. Open valley metal is a customer charge.
~~~

## Result Asset

- Archive filename: run-0025-gpt51-no-skill-exp0004-control.zip
- Archive SHA-256: 06a229d17b2eb6bb18e56c214191e74701b5881fd89de2026a1de490177f05c0
- Archive location: ARCHIVES/local/run-0025-gpt51-no-skill-exp0004-control.zip
- Archive durability: local-only, publication pending; do not treat this ZIP as retrievable from a fresh clone until it is attached to a durable release/artifact store.

## Transcript/Trace

- EVIDENCE/0025/cursor-agent-transcript.raw.jsonl
- EVIDENCE/0025/cursor-agent-transcript.md
- EVIDENCE/0025/cursor-terminal-629480.txt
- EVIDENCE/0025/cursor-terminal-629481.txt
- EVIDENCE/0025/cursor-terminal-629482.txt
- EVIDENCE/0025/cursor-terminal-629483.txt

Transcript SHA-256:

~~~text
9741745046318a3937504b3fe8ca5357dd78073a3b7272fd79b045d29f853202  cursor-agent-transcript.raw.jsonl
626a3c25a31e875088780bfb7cd70415616371728399d362724629360c65d79e  cursor-agent-transcript.md
~~~

## Expected Pressure

Task 04 from EXP-0004-task04-open-valley-metal-charge: make open valley metal a customer charge where the product failure is observed across estimate totals and roofing proposal pricing, without exposing implementation hints, expected authority, or closed-valley invariants to the subject model.

## Outcome

The Active working tree at preservation contained three tracked modifications and no untracked paths:

~~~text
 M components/RoofingScopeForm.vue
 M shared/calculator/calculateEstimate.ts
 M shared/options/valleyMetal.ts
~~~

Tracked changed files before preservation:

~~~text
M	components/RoofingScopeForm.vue
M	shared/calculator/calculateEstimate.ts
M	shared/options/valleyMetal.ts
~~~

Untracked files before preservation:

~~~text
(none)
~~~

git diff --stat HEAD before preservation:

~~~text
 components/RoofingScopeForm.vue        |  6 ++++--
 shared/calculator/calculateEstimate.ts |  2 +-
 shared/options/valleyMetal.ts          | 14 +++++++-------
 3 files changed, 12 insertions(+), 10 deletions(-)
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
archive_size=3483061
~~~

The archive was checked for transcript-related entries:

~~~text
matching_entries=0
~~~

The transcript is not inside the archive ZIP. It is preserved in EVIDENCE/0025 beside the archive evidence.

The archive was checked for generated dependency/build directories:

~~~text
node_modules=False
.nuxt=False
.output=False
~~~

Cursor terminal evidence preserved for this run includes repository searches:

~~~text
dir
rg -n "valley"
rg -n "contractEffect"
rg -n "grandTotal"
all recorded as status: succeeded
~~~

The transcript records a ReadLints call on changed files, but no successful typecheck, test, build, browser runtime check, or explicit open/closed-valley behavior check was independently preserved.

Active HEAD before preservation:

~~~text
cd393ddd60548823dabd6875060247693a22c1be
~~~

diff.patch contains tracked changes only. untracked-files.txt is `(none)` because no untracked subject files were present at preservation.

## Observed Trace Events

Observed transcript events only, without architecture-quality scoring:

- Cursor began with the plain EXP-0004 prompt and no /layered-codebase-architecture invocation.
- Cursor searched for valley, proposal/contract effects, and grandTotal usage.
- Cursor changed shared/options/valleyMetal.ts, shared/calculator/calculateEstimate.ts, and components/RoofingScopeForm.vue.
- Cursor did not create untracked subject-repository files.
- Cursor did not change shared/contracts/roofProposalPricing.ts.
- Cursor did not preserve an executable behavior check proving proposal pricing inclusion, open valley customer-charge propagation, or closed-valley preservation.

## Suspected Skill Gap (Hypothesis)

Not evaluated in this preservation step. This run is preserved as the no-skill EXP-0004 first-model control arm for later scoring against the rubric.

## Next Experiment

Continue EXP-0004 with run 0026: GPT-5.1 V1 candidate, fresh Mother-to-Active clone, fresh Cursor conversation, V1 installed in Cursor global skills-cursor directory, and forced /layered-codebase-architecture invocation.
