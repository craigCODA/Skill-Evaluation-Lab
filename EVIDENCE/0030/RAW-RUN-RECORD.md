# Run 0030 - V1 candidate forced EXP-0004 open valley metal charge, Opus

- Date/time: 2026-08-31 CDT; exact archive timestamp is recorded in EVIDENCE/0030/archive-manifest.json
- Operator: Codex workplace operator
- Mode: V1 candidate skill run
- Subject model + exact version: Opus from operator selection; the exported Cursor transcript does not independently encode the model identifier
- Model settings / tools: Cursor harness; raw internal agent transcript exported from the Cursor project store; exact reasoning/effort setting was not independently captured in the transcript
- Target repository: ShingleFile
- Target starting commit: cd393ddd60548823dabd6875060247693a22c1be
- Skill: layered-codebase-architecture
- Skill condition: V1 candidate (01-V1-CANDIDATE)
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
When I choose an open valley and enter the footage, the estimate shows a valley metal amount but the customer total and roofing proposal ignore it. Open valley metal is a customer charge.
~~~

Cursor prompt as exported:

~~~text
/layered-codebase-architecture 
When I choose an open valley and enter the footage, the estimate shows a valley metal amount but the customer total and roofing proposal ignore it. Open valley metal is a customer charge.
~~~

## Result Asset

- Archive filename: run-0030-opus-v1-exp0004-candidate.zip
- Archive SHA-256: 261a5fb55cbeaa5c51afb44b9d288c16b2c2ea93b49368fe8a4ffec1b7b107d4
- Archive location: ARCHIVES/local/run-0030-opus-v1-exp0004-candidate.zip
- Archive durability: local-only, publication pending; do not treat this ZIP as retrievable from a fresh clone until it is attached to a durable release/artifact store.

## Transcript/Trace

- EVIDENCE/0030/cursor-agent-transcript.raw.jsonl
- EVIDENCE/0030/cursor-agent-transcript.md
- EVIDENCE/0030/cursor-subagent-d3251467-2110-4679-b60d-74f39dad34cc.raw.jsonl
- EVIDENCE/0030/cursor-subagent-d3251467-2110-4679-b60d-74f39dad34cc.md
- EVIDENCE/0030/cursor-terminal-795077.txt
- EVIDENCE/0030/cursor-terminal-795078.txt
- EVIDENCE/0030/cursor-terminal-647875.txt
- EVIDENCE/0030/cursor-terminal-647876.txt

Transcript SHA-256:

~~~text
c11a48c7b540161e5c37d65949c0fcc738f7d59fb9c9539e6ba3ac2f4a3ba875  cursor-agent-transcript.raw.jsonl
f931ef02dd6d63eb8ea8e785487b169f721e825ff06b4f273ef6105142a684d0  cursor-agent-transcript.md
0a151c8d4a73ccae02c44b16108f6673fe6de9ca62d4be442df594713f3daca5  cursor-subagent-d3251467-2110-4679-b60d-74f39dad34cc.raw.jsonl
4d4f7d400b112b1c35a79d025fdc90d37d7f855ba5c4241d3158ea606ccf32e7  cursor-subagent-d3251467-2110-4679-b60d-74f39dad34cc.md
~~~

## Expected Pressure

Task 04 from EXP-0004-task04-open-valley-metal-charge: make open valley metal a customer charge where the product failure is observed across estimate totals and roofing proposal pricing, without exposing implementation hints, expected authority, or closed-valley invariants to the subject model.

## Outcome

The Active working tree at preservation contained 5 tracked modifications and 0 untracked paths:

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
 components/RoofingScopeForm.vue         |  4 ++--
 shared/calculator/calculateEstimate.ts  |  2 +-
 shared/contracts/roofProposalPricing.ts |  8 ++++++++
 shared/options/valleyMetal.ts           | 22 +++++++++++-----------
 shared/pricebook/types.ts               |  5 ++---
 5 files changed, 24 insertions(+), 17 deletions(-)
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
archive_size=3483075
~~~

The archive was checked for transcript-related entries:

~~~text
matching_entries=0
~~~

The transcript is not inside the archive ZIP. It is preserved in EVIDENCE/0030 beside the archive evidence.

The archive was checked for generated dependency/build directories:

~~~text
node_modules=False
.nuxt=False
.output=False
~~~

Cursor terminal evidence preserved for this run includes root/key-folder listing output. One terminal output shows a PowerShell `dir ... /b` command ending with an error message while the exported metadata reports exit_code 0.

The transcript records repository exploration, direct reads, and grep activity, but no independent successful typecheck, test, build, browser/runtime verification, proposal-pricing behavior check, explicit open/closed-valley behavior check, or no-double-counting check was preserved.

Active HEAD before preservation:

~~~text
cd393ddd60548823dabd6875060247693a22c1be
~~~

diff.patch contains tracked changes only. untracked-files.txt is `(none)` because no untracked subject files were present at preservation.

## Observed Trace Events

Observed transcript events only, without architecture-quality scoring:

- Cursor began with the forced /layered-codebase-architecture invocation and inlined V1 skill content.
- Cursor delegated a repository exploration subagent, then inspected estimate, proposal, option, type, UI, material-count, docs, and contract paths.
- Cursor changed shared/options/valleyMetal.ts, shared/calculator/calculateEstimate.ts, shared/contracts/roofProposalPricing.ts, shared/pricebook/types.ts, and components/RoofingScopeForm.vue.
- Cursor did not create untracked subject-repository files.
- Cursor did not preserve an executable behavior check proving proposal pricing inclusion, open valley customer-charge propagation, closed-valley preservation, or absence of double-counting.

## Suspected Skill Gap (Hypothesis)

Not evaluated in this preservation step. This run is preserved as the V1 candidate EXP-0004 second-model arm for later scoring against the rubric.

## Next Experiment

Continue EXP-0004 with run 0031: Opus V2 candidate, fresh Mother-to-Active clone, fresh Cursor conversation, V2 installed in Cursor global skills-cursor directory, and forced /layered-codebase-architecture invocation.
