# Run 0027 - V2 candidate forced EXP-0004 open valley metal charge, GPT-5.1

- Date/time: 2026-08-31 CDT; exact archive timestamp is recorded in EVIDENCE/0027/archive-manifest.json
- Operator: Codex workplace operator
- Mode: V2 candidate skill run
- Subject model + exact version: GPT-5.1 from operator selection; the exported Cursor transcript does not independently encode the model identifier
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
When I choose an open valley and enter the footage, the estimate shows a valley metal amount but the customer total and roofing proposal ignore it. Open valley metal is a customer charge.
~~~

Cursor prompt as exported:

~~~text
/layered-codebase-architecture 

When I choose an open valley and enter the footage, the estimate shows a valley metal amount but the customer total and roofing proposal ignore it. Open valley metal is a customer charge.
~~~

## Result Asset

- Archive filename: run-0027-gpt51-v2-exp0004-candidate.zip
- Archive SHA-256: 44d5876deb6f0ff0577518e5fd1ba9984616c1ea32864f87323f76afc990b791
- Archive location: ARCHIVES/local/run-0027-gpt51-v2-exp0004-candidate.zip
- Archive durability: local-only, publication pending; do not treat this ZIP as retrievable from a fresh clone until it is attached to a durable release/artifact store.

## Transcript/Trace

- EVIDENCE/0027/cursor-agent-transcript.raw.jsonl
- EVIDENCE/0027/cursor-agent-transcript.md
- EVIDENCE/0027/cursor-terminal-869165.txt
- EVIDENCE/0027/cursor-terminal-869166.txt
- EVIDENCE/0027/cursor-terminal-869167.txt
- EVIDENCE/0027/cursor-terminal-869168.txt
- EVIDENCE/0027/cursor-terminal-869169.txt
- EVIDENCE/0027/cursor-terminal-869170.txt
- EVIDENCE/0027/cursor-terminal-869171.txt

Transcript SHA-256:

~~~text
018387e4e4be11a47ad58290e2f4c38b64e7b2e4ac75573a8fca9f24d3413b17  cursor-agent-transcript.raw.jsonl
78aa7e5ab6c2fbf9fca16e628d6e5f29dd455ea6e96e0d774b09e7b9ed8aed74  cursor-agent-transcript.md
~~~

## Expected Pressure

Task 04 from EXP-0004-task04-open-valley-metal-charge: make open valley metal a customer charge where the product failure is observed across estimate totals and roofing proposal pricing, without exposing implementation hints, expected authority, or closed-valley invariants to the subject model.

## Outcome

The Active working tree at preservation contained three tracked modifications and no untracked paths:

~~~text
 M shared/calculator/calculateEstimate.ts
 M shared/contracts/roofProposalPricing.ts
 M shared/options/valleyMetal.ts
~~~

Tracked changed files before preservation:

~~~text
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
 shared/calculator/calculateEstimate.ts  |  3 ++-
 shared/contracts/roofProposalPricing.ts |  8 ++++++++
 shared/options/valleyMetal.ts           | 20 ++++++++++++--------
 3 files changed, 22 insertions(+), 9 deletions(-)
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
archive_size=3482835
~~~

The archive was checked for transcript-related entries:

~~~text
matching_entries=0
~~~

The transcript is not inside the archive ZIP. It is preserved in EVIDENCE/0027 beside the archive evidence.

The archive was checked for generated dependency/build directories:

~~~text
node_modules=False
.nuxt=False
.output=False
~~~

Cursor terminal evidence preserved for this run includes successful directory listings and a failed `npm run typecheck` command:

~~~text
'nuxt' is not recognized as an internal or external command,
operable program or batch file.

exit_code: 1
~~~

No successful typecheck, test, build, browser/runtime verification, proposal-pricing behavior check, or explicit open/closed-valley behavior check was independently preserved.

Active HEAD before preservation:

~~~text
cd393ddd60548823dabd6875060247693a22c1be
~~~

diff.patch contains tracked changes only. untracked-files.txt is `(none)` because no untracked subject files were present at preservation.

## Observed Trace Events

Observed transcript events only, without architecture-quality scoring:

- Cursor began with the forced /layered-codebase-architecture invocation and inlined V2 candidate skill content.
- Cursor had initial Grep/Glob path trouble and used shell directory listings plus direct reads to locate estimate, option, and proposal-pricing files.
- Cursor changed shared/options/valleyMetal.ts, shared/calculator/calculateEstimate.ts, and shared/contracts/roofProposalPricing.ts.
- Cursor set the valley-metal option metadata to billed, added valleyMetal.cost directly into calculateRoofingEstimate grandTotal, and added a valley metal pricing line in roofProposalPricing when cost is greater than zero.
- Cursor did not create untracked subject-repository files.
- Cursor attempted `npm run typecheck`; the preserved terminal output records failure because `nuxt` was not recognized.
- Cursor did not preserve an executable behavior check proving proposal pricing inclusion, open valley customer-charge propagation, closed-valley preservation, or absence of double-counting.

## Suspected Skill Gap (Hypothesis)

Not evaluated in this preservation step. This run is preserved as the V2 candidate EXP-0004 first-model arm for later scoring against the rubric.

## Next Experiment

EXP-0004 first-model block `0024` through `0027` is now ready for scoring before any further run block is cut.
