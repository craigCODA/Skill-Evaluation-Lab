# Run 0029 - no-skill control EXP-0004 open valley metal charge, Opus

- Date/time: 2026-08-31 CDT; exact archive timestamp is recorded in EVIDENCE/0029/archive-manifest.json
- Operator: Codex workplace operator
- Mode: no-skill control run
- Subject model + exact version: Opus from operator selection; the exported Cursor transcript does not independently encode the model identifier
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

- Archive filename: run-0029-opus-no-skill-exp0004-control.zip
- Archive SHA-256: 15bc9a836497ed16106ad10449bed5e7fa47ee0d2df2df8d4aed2973111c6192
- Archive location: ARCHIVES/local/run-0029-opus-no-skill-exp0004-control.zip
- Archive durability: local-only, publication pending; do not treat this ZIP as retrievable from a fresh clone until it is attached to a durable release/artifact store.

## Transcript/Trace

- EVIDENCE/0029/cursor-agent-transcript.raw.jsonl
- EVIDENCE/0029/cursor-agent-transcript.md
- EVIDENCE/0029/cursor-subagent-04e0b478-24dc-4ee4-87a6-931cecd25046.raw.jsonl
- EVIDENCE/0029/cursor-subagent-04e0b478-24dc-4ee4-87a6-931cecd25046.md
- EVIDENCE/0029/cursor-terminal-527835.txt
- EVIDENCE/0029/cursor-terminal-527836.txt
- EVIDENCE/0029/cursor-terminal-527837.txt
- EVIDENCE/0029/cursor-terminal-527838.txt
- EVIDENCE/0029/cursor-terminal-527839.txt
- EVIDENCE/0029/cursor-terminal-286269.txt

Transcript SHA-256:

~~~text
e2d02796f4f7149656822efff721a9658e2690f81adb1a0d05734207b8b0cba8  cursor-agent-transcript.raw.jsonl
3a449f130a4cd397a3922d91ee4a67e356e59f628361e8c66413c909041684db  cursor-agent-transcript.md
06460c1236a0c50b7a24cc2333e75b51684f005dfba6a8535d733ad96fdd1d82  cursor-subagent-04e0b478-24dc-4ee4-87a6-931cecd25046.raw.jsonl
f75e7e2d90b12d00470b2322294390991ab065a99e225fe845ab43a211b27b4c  cursor-subagent-04e0b478-24dc-4ee4-87a6-931cecd25046.md
~~~

## Expected Pressure

Task 04 from EXP-0004-task04-open-valley-metal-charge: make open valley metal a customer charge where the product failure is observed across estimate totals and roofing proposal pricing, without exposing implementation hints, expected authority, or closed-valley invariants to the subject model.

## Outcome

The Active working tree at preservation contained 4 tracked modifications and 0 untracked paths:

~~~text
 M components/RoofingScopeForm.vue
 M shared/calculator/calculateEstimate.ts
 M shared/contracts/roofProposalPricing.ts
 M shared/options/valleyMetal.ts
~~~

Tracked changed files before preservation:

~~~text
M	components/RoofingScopeForm.vue
M	shared/calculator/calculateEstimate.ts
M	shared/contracts/roofProposalPricing.ts
M	shared/options/valleyMetal.ts
~~~

Untracked files before preservation:

~~~text
(none)
~~~

git diff --stat HEAD before preservation:

~~~text
 components/RoofingScopeForm.vue         |  4 ++--
 shared/calculator/calculateEstimate.ts  |  2 +-
 shared/contracts/roofProposalPricing.ts |  8 ++++++++
 shared/options/valleyMetal.ts           | 22 +++++++++++-----------
 4 files changed, 22 insertions(+), 14 deletions(-)
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
archive_size=3482997
~~~

The archive was checked for transcript-related entries:

~~~text
matching_entries=0
~~~

The transcript is not inside the archive ZIP. It is preserved in EVIDENCE/0029 beside the archive evidence.

The archive was checked for generated dependency/build directories:

~~~text
node_modules=False
.nuxt=False
.output=False
~~~

Cursor terminal evidence preserved for this run includes repository listing/search output, proposal/contract search output, and package/test discovery output. The preserved terminal evidence includes a command that returned failed status while emitting matching output because a later search in the command found no test/spec files.

The transcript records a ReadLints call on changed files and an attempted dependency-gated typecheck command, but no independently preserved successful typecheck, test, build, browser/runtime verification, proposal-pricing behavior check, or explicit open/closed-valley behavior check was preserved.

Active HEAD before preservation:

~~~text
cd393ddd60548823dabd6875060247693a22c1be
~~~

diff.patch contains tracked changes only. untracked-files.txt is `(none)` because no untracked subject files were present at preservation.

## Observed Trace Events

Observed transcript events only, without architecture-quality scoring:

- Cursor began with the plain EXP-0004 prompt and no /layered-codebase-architecture invocation.
- Cursor delegated a repository exploration subagent and then cross-checked the subagent's findings with direct file reads and shell search.
- Cursor searched valley metal, billing metadata, estimate totals, proposal/contract pricing, material counts, and contract document paths.
- Cursor changed shared/options/valleyMetal.ts, shared/calculator/calculateEstimate.ts, shared/contracts/roofProposalPricing.ts, and components/RoofingScopeForm.vue.
- Cursor did not create untracked subject-repository files.
- Cursor did not change shared/pricebook/types.ts.
- Cursor did not preserve an executable behavior check proving proposal pricing inclusion, open valley customer-charge propagation, closed-valley preservation, or absence of double-counting.

## Suspected Skill Gap (Hypothesis)

Not evaluated in this preservation step. This run is preserved as the no-skill EXP-0004 second-model control arm for later scoring against the rubric.

## Next Experiment

Continue EXP-0004 with run 0030: Opus V1 candidate, fresh Mother-to-Active clone, fresh Cursor conversation, V1 installed in Cursor global skills-cursor directory, and forced /layered-codebase-architecture invocation.
