# Run 0026 - V1 candidate forced EXP-0004 open valley metal charge, GPT-5.1

- Date/time: 2026-08-31 CDT; exact archive timestamp is recorded in EVIDENCE/0026/archive-manifest.json
- Operator: Codex workplace operator
- Mode: V1 candidate skill run
- Subject model + exact version: GPT-5.1 from operator selection; the exported Cursor transcript does not independently encode the model identifier
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
When I choose an open valley and enter the footage, the estimate shows a valley metal amount but the customer total and roofing proposal ignore it. Open valley metal is a customer charge.
~~~

Cursor prompt as exported:

~~~text
/layered-codebase-architecture  

When I choose an open valley and enter the footage, the estimate shows a valley metal amount but the customer total and roofing proposal ignore it. Open valley metal is a customer charge.
~~~

## Result Asset

- Archive filename: run-0026-gpt51-v1-exp0004-candidate.zip
- Archive SHA-256: 7bfa93f2bcedf9272cef43f1427a1a820f0921cc78cc0a86b10c00ec88135f3a
- Archive location: ARCHIVES/local/run-0026-gpt51-v1-exp0004-candidate.zip
- Archive durability: local-only, publication pending; do not treat this ZIP as retrievable from a fresh clone until it is attached to a durable release/artifact store.

## Transcript/Trace

- EVIDENCE/0026/cursor-agent-transcript.raw.jsonl
- EVIDENCE/0026/cursor-agent-transcript.md
- EVIDENCE/0026/cursor-terminal-1.txt
- EVIDENCE/0026/cursor-terminal-985130.txt

Transcript SHA-256:

~~~text
e0ecb3c0bd364798a08c83c0fc2ebdd27a189b871728864fa834848d77b3d907  cursor-agent-transcript.raw.jsonl
03467eb56541a67a66d5aa0ee982619ecfe4cd1b9dc561c0b512fbdec4e5ff8c  cursor-agent-transcript.md
~~~

## Expected Pressure

Task 04 from EXP-0004-task04-open-valley-metal-charge: make open valley metal a customer charge where the product failure is observed across estimate totals and roofing proposal pricing, without exposing implementation hints, expected authority, or closed-valley invariants to the subject model.

## Outcome

The Active working tree at preservation contained one tracked modification and no untracked paths:

~~~text
 M shared/options/valleyMetal.ts
~~~

Tracked changed files before preservation:

~~~text
M	shared/options/valleyMetal.ts
~~~

Untracked files before preservation:

~~~text
(none)
~~~

git diff --stat HEAD before preservation:

~~~text
 shared/options/valleyMetal.ts | 18 +++++++++---------
 1 file changed, 9 insertions(+), 9 deletions(-)
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
archive_size=3482042
~~~

The archive was checked for transcript-related entries:

~~~text
matching_entries=0
~~~

The transcript is not inside the archive ZIP. It is preserved in EVIDENCE/0026 beside the archive evidence.

The archive was checked for generated dependency/build directories:

~~~text
node_modules=False
.nuxt=False
.output=False
~~~

Cursor terminal evidence preserved for this run includes a successful `pwd; ls` shell command record, but the preserved terminal output does not include an actual file listing.

The transcript records a ReadLints call on shared/options/valleyMetal.ts, but no successful typecheck, test, build, browser runtime check, proposal-pricing behavior check, or explicit open/closed-valley behavior check was independently preserved.

Active HEAD before preservation:

~~~text
cd393ddd60548823dabd6875060247693a22c1be
~~~

diff.patch contains tracked changes only. untracked-files.txt is `(none)` because no untracked subject files were present at preservation.

## Observed Trace Events

Observed transcript events only, without architecture-quality scoring:

- Cursor began with the forced /layered-codebase-architecture invocation and inlined V1 candidate skill content.
- Cursor had repeated Grep/Glob path trouble and used direct Read operations on likely files.
- Cursor inferred that setting valleyMetalOption.billed to true should make estimate/proposal mechanisms include the charge.
- Cursor changed only shared/options/valleyMetal.ts.
- Cursor did not create untracked subject-repository files.
- Cursor did not preserve an executable behavior check proving proposal pricing inclusion, open valley customer-charge propagation, or closed-valley preservation.

## Suspected Skill Gap (Hypothesis)

Not evaluated in this preservation step. This run is preserved as the V1 candidate EXP-0004 first-model arm for later scoring against the rubric.

## Next Experiment

Continue EXP-0004 with run 0027: GPT-5.1 V2 candidate, fresh Mother-to-Active clone, fresh Cursor conversation, V2 installed in Cursor global skills-cursor directory, and forced /layered-codebase-architecture invocation.
