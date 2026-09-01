# Run 0031 - V2 candidate forced EXP-0004 open valley metal charge, Opus

- Date/time: 2026-09-01 CDT; exact archive timestamp is recorded in EVIDENCE/0031/archive-manifest.json
- Operator: Codex workplace operator
- Mode: V2 candidate skill run
- Subject model + exact version: Opus from operator selection; the exported Cursor transcript does not independently encode the model identifier
- Model settings / tools: Cursor harness; raw internal agent transcript exported from the Cursor project store; exact reasoning/effort setting was not independently captured in the transcript
- Target repository: ShingleFile
- Target starting commit: cd393ddd60548823dabd6875060247693a22c1be
- Skill: layered-codebase-architecture
- Skill condition: V2 candidate (02-V2-GRAPH)
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

- Archive filename: run-0031-opus-v2-exp0004-candidate.zip
- Archive SHA-256: 25022cb8fe3309c51bbb7389fc7d168c2a65ea5abc711358bec8e12355dd49f8
- Archive location: ARCHIVES/local/run-0031-opus-v2-exp0004-candidate.zip
- Archive durability: local-only, publication pending; do not treat this ZIP as retrievable from a fresh clone until it is attached to a durable release/artifact store.

## Transcript/Trace

- EVIDENCE/0031/cursor-agent-transcript.raw.jsonl
- EVIDENCE/0031/cursor-agent-transcript.md
- EVIDENCE/0031/cursor-subagent-57d86e3f-2e27-4280-a360-c011f54e6852.raw.jsonl
- EVIDENCE/0031/cursor-subagent-57d86e3f-2e27-4280-a360-c011f54e6852.md
- EVIDENCE/0031/cursor-subagent-17249b51-dac2-4e4a-ba34-48ca853bf505.raw.jsonl
- EVIDENCE/0031/cursor-subagent-17249b51-dac2-4e4a-ba34-48ca853bf505.md
- EVIDENCE/0031/cursor-terminal-557724.txt
- EVIDENCE/0031/cursor-terminal-448088.txt
- EVIDENCE/0031/cursor-terminal-448089.txt
- EVIDENCE/0031/cursor-terminal-322495.txt

Transcript SHA-256:

~~~text
415828dbe8620de973e1cdc4f49d8c8e511b6c40007a704f9ae7a2896fa06726  cursor-agent-transcript.raw.jsonl
37ec611942ec0001d3330c4b6af8838978034fa882a361298a1a2f50b07b11db  cursor-agent-transcript.md
d0d36ca048be953520ea4d4d27ff941af473f8c223eca91c84c062843b1f8b34  cursor-subagent-57d86e3f-2e27-4280-a360-c011f54e6852.raw.jsonl
cf3ef382ab8fe07f017de768ee37a314f4fc06eec4bc6b91f08185bf48f7bb8b  cursor-subagent-57d86e3f-2e27-4280-a360-c011f54e6852.md
70d67be0510790ea7a331f8f6ca79ef39468fd96237d44a4b7ea835d6f1ab84b  cursor-subagent-17249b51-dac2-4e4a-ba34-48ca853bf505.raw.jsonl
9f07565e7cbccd46f447cfdd994dce9192454c5de8140ce9e21a96fcb21ddb43  cursor-subagent-17249b51-dac2-4e4a-ba34-48ca853bf505.md
~~~

## Expected Pressure

Task 04 from EXP-0004-task04-open-valley-metal-charge: make open valley metal a customer charge where the product failure is observed across estimate totals and roofing proposal pricing, without exposing implementation hints, expected authority, or closed-valley invariants to the subject model.

## Outcome

The Active working tree at preservation contained 4 tracked modifications and 0 untracked subject-repository paths:

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

Untracked subject-repository files before preservation:

~~~text
(none)
~~~

Ignored files/directories visible before preservation:

~~~text
!! .nuxt/
!! node_modules/
~~~

git diff --stat HEAD before preservation:

~~~text
 components/RoofingScopeForm.vue         |  4 ++--
 shared/calculator/calculateEstimate.ts  |  2 +-
 shared/contracts/roofProposalPricing.ts |  8 ++++++++
 shared/options/valleyMetal.ts           | 19 +++++++++----------
 4 files changed, 20 insertions(+), 13 deletions(-)
~~~

git diff --check before preservation:

~~~text
(no whitespace errors)
~~~

## Verification

Archive verification completed before cleanup:

~~~text
testzip=OK
entry_count=24068
has_git=True
archive_size=104623855
~~~

The archive was checked for transcript/terminal-named entries:

~~~text
matching_entries=9
all matches are dependency files under node_modules/
~~~

The lab transcript and terminal evidence are not inside the archive ZIP. They are preserved in EVIDENCE/0031 beside the archive evidence.

The archive was checked for generated dependency/build directories:

~~~text
node_modules=True
.nuxt=True
.output=False
~~~

The archive includes ignored dependency/build state created during the run: node_modules=True, .nuxt=True, .output=False.

Cursor terminal evidence preserved for this run includes file/directory listing attempts and a contract snapshot persistence search. Some listing terminal outputs are empty despite succeeded metadata; another listing terminal output records PowerShell `dir ... /b` parameter errors while succeeded metadata is present.

The transcript records `npm install`, `npm run typecheck`, ReadLints, repository exploration, and final typecheck/lint claims, but no separate terminal file containing npm install output or successful typecheck output was found under the Cursor terminal exports. Treat those as transcript/process evidence, not independently preserved command-output verification.

Active HEAD before preservation:

~~~text
cd393ddd60548823dabd6875060247693a22c1be
~~~

diff.patch contains tracked changes only. untracked-files.txt is `(none)` because no untracked subject files were present at preservation. ignored-files.txt records ignored generated/dependency directories that are present in the full Active archive.

## Observed Trace Events

Observed transcript events only, without architecture-quality scoring:

- Cursor began with the forced /layered-codebase-architecture invocation and inlined V2 skill content.
- Cursor launched two repository exploration subagents, then inspected valley metal, estimate totals, proposal pricing, UI, material counts, contract store, docs, and persistence paths.
- Cursor changed shared/options/valleyMetal.ts, shared/calculator/calculateEstimate.ts, shared/contracts/roofProposalPricing.ts, and components/RoofingScopeForm.vue.
- Cursor did not create untracked subject-repository files, but it did create ignored dependency/build directories node_modules/ and .nuxt/ while attempting verification.
- Cursor did not change shared/pricebook/types.ts.
- Cursor did not preserve a standalone executable behavior check proving proposal pricing inclusion, open valley customer-charge propagation, closed-valley preservation, or absence of double-counting.

## Suspected Skill Gap (Hypothesis)

Not evaluated in this preservation step. This run is preserved as the V2 candidate EXP-0004 second-model arm for later scoring against the rubric.

## Next Experiment

The planned EXP-0004 Opus block is complete through run 0031. Next useful action is to score the second-model Opus block and then compare it with the GPT-5.1 block.
