# Run 0028 - supplied original forced EXP-0004 open valley metal charge, Opus

- Date/time: 2026-08-31 CDT; exact archive timestamp is recorded in EVIDENCE/0028/archive-manifest.json
- Operator: Codex workplace operator
- Mode: supplied original skill run
- Subject model + exact version: Opus from operator selection; the exported Cursor transcript does not independently encode the model identifier
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
When I choose an open valley and enter the footage, the estimate shows a valley metal amount but the customer total and roofing proposal ignore it. Open valley metal is a customer charge.
~~~

Cursor prompt as exported:

~~~text
/layered-codebase-architecture
When I choose an open valley and enter the footage, the estimate shows a valley metal amount but the customer total and roofing proposal ignore it. Open valley metal is a customer charge.
~~~

## Result Asset

- Archive filename: run-0028-opus-original-exp0004-supplied.zip
- Archive SHA-256: b28330a211146241ccc68a23f1f4706b3fccb9fcfa5cf1726b6dff78e3fa3ac9
- Archive location: ARCHIVES/local/run-0028-opus-original-exp0004-supplied.zip
- Archive durability: local-only, publication pending; do not treat this ZIP as retrievable from a fresh clone until it is attached to a durable release/artifact store.

## Transcript/Trace

- EVIDENCE/0028/cursor-agent-transcript.raw.jsonl
- EVIDENCE/0028/cursor-agent-transcript.md
- EVIDENCE/0028/cursor-terminal-152611.txt
- EVIDENCE/0028/cursor-terminal-152612.txt

Transcript SHA-256:

~~~text
0b4e6ecb08a13124915449ac483a43b52093d950e6a7b3c2249cd09a820343a5  cursor-agent-transcript.raw.jsonl
d501436e2e95dada6c14ce930eb6750f73e807cfce1acb59903f6d08b2055538  cursor-agent-transcript.md
~~~

## Expected Pressure

Task 04 from EXP-0004-task04-open-valley-metal-charge: make open valley metal a customer charge where the product failure is observed across estimate totals and roofing proposal pricing, without exposing implementation hints, expected authority, or closed-valley invariants to the subject model.

## Outcome

The Active working tree at preservation contained five tracked modifications and no untracked paths:

~~~text
 M components/RoofingScopeForm.vue
 M shared/calculator/calculateEstimate.ts
 M shared/contracts/roofProposalPricing.ts
 M shared/options/valleyMetal.ts
 M shared/pricebook/types.ts
~~~

Tracked changed files before preservation:

~~~text
M	components/RoofingScopeForm.vue
M	shared/calculator/calculateEstimate.ts
M	shared/contracts/roofProposalPricing.ts
M	shared/options/valleyMetal.ts
M	shared/pricebook/types.ts
~~~

Untracked files before preservation:

~~~text
(none)
~~~

git diff --stat HEAD before preservation:

~~~text
 components/RoofingScopeForm.vue         |  3 +--
 shared/calculator/calculateEstimate.ts  |  2 +-
 shared/contracts/roofProposalPricing.ts |  8 ++++++++
 shared/options/valleyMetal.ts           | 22 +++++++++++-----------
 shared/pricebook/types.ts               |  5 ++---
 5 files changed, 23 insertions(+), 17 deletions(-)
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
archive_size=3483497
~~~

The archive was checked for transcript-related entries:

~~~text
matching_entries=0
~~~

The transcript is not inside the archive ZIP. It is preserved in EVIDENCE/0028 beside the archive evidence.

The archive was checked for generated dependency/build directories:

~~~text
node_modules=False
.nuxt=False
.output=False
~~~

Cursor terminal evidence preserved for this run includes a successful root `ls` command and a later repo-wide valley search command that returned a failed status while emitting matching output. The transcript records an attempted `npm run typecheck` command and later states dependencies were not installed, but no separate successful typecheck, test, build, or browser/runtime terminal output was independently preserved.

No targeted open/closed-valley behavior check, proposal-pricing behavior check, or no-double-counting check was independently preserved.

Active HEAD before preservation:

~~~text
cd393ddd60548823dabd6875060247693a22c1be
~~~

diff.patch contains tracked changes only. untracked-files.txt is `(none)` because no untracked subject files were present at preservation.

## Observed Trace Events

Observed transcript events only, without architecture-quality scoring:

- Cursor began with the forced /layered-codebase-architecture invocation and inlined supplied original skill content.
- Cursor traced the valley-metal rule across option metadata, pricebook type comments, estimate totals, proposal pricing, UI copy, contract document usage, and server contract routes.
- Cursor explicitly decided not to create `.cursor/noun-map.md` for this bounded change.
- Cursor changed shared/options/valleyMetal.ts, shared/calculator/calculateEstimate.ts, shared/contracts/roofProposalPricing.ts, components/RoofingScopeForm.vue, and shared/pricebook/types.ts.
- Cursor did not create untracked subject-repository files.
- Cursor attempted `npm run typecheck`, but no independent terminal output for a successful typecheck was preserved.
- Cursor did not preserve an executable behavior check proving proposal pricing inclusion, open valley customer-charge propagation, closed-valley preservation, or absence of double-counting.

## Suspected Skill Gap (Hypothesis)

Not evaluated in this preservation step. This run is preserved as the supplied original EXP-0004 second-model arm for later scoring against the rubric.

## Next Experiment

Continue EXP-0004 with run 0029: Opus no-skill control, fresh Mother-to-Active clone, fresh Cursor conversation, no global layered-codebase-architecture skill present, and no slash invocation.
