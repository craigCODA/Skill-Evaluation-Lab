# Run 0017 - no-skill control Task 02 quick calculator clear label, Grok 4.6 High

- Date/time: 2026-08-31 CDT; exact archive timestamp is recorded in `EVIDENCE/0017/archive-manifest.json`
- Operator: Codex workplace operator
- Mode: no-skill control run
- Subject model + exact version: `Grok 4.6 High` from operator selection; the exported Cursor transcript does not independently encode the model identifier
- Model settings / tools: Cursor harness; raw internal agent transcript exported from the Cursor project store; exact reasoning/effort setting was not independently captured in the transcript
- Target repository: ShingleFile
- Target starting commit: `cd393ddd60548823dabd6875060247693a22c1be`
- Skill: `layered-codebase-architecture`
- Skill condition: no skill (`NO-SKILL`)
- Skill invocation: none
- Skill runtime path: `%USERPROFILE%/.cursor/skills-cursor/layered-codebase-architecture/` absent before run

## Skill State

```text
SKILL_DIR=
C:\Users\NeverAMoment\.cursor\skills-cursor\layered-codebase-architecture
present=false
condition=NO-SKILL
```

## Change Request

Planned prompt from `PROMPT.txt`:

```text
In the roof quick calculator, the bottom button says “Clear entries,” but it only clears the manually entered ridge, hip, valley, eave, and rake values. Rename it to “Clear manual entries” so the label matches what it actually does. Don’t change the behavior. Do not restructure surrounding files.
```

Cursor initial prompt as exported:

```text
In the roof quick calculator, the bottom button says “Clear entries,” but it only clears the manually entered ridge, hip, valley, eave, and rake values. Rename it to “Clear manual entries” so the label matches what it actually does. Don’t change the behavior. Do not restructure surrounding files.
```

Prompt note: No prompt-text deviation observed between planned prompt and exported initial user query.

## Result Asset

- Archive filename: `run-0017-grok46-no-skill-exp0002-control.zip`
- Archive SHA-256: `9fb60ed3b6f0d22a60a4a8c08a2e3aadbd17c5101e2d3386bd1b60ed633f0897`
- Archive location: `ARCHIVES/local/run-0017-grok46-no-skill-exp0002-control.zip`
- Archive durability: local-only, publication pending; do not treat this ZIP as retrievable from a fresh clone until it is attached to a durable release/artifact store.

## Transcript/Trace

- `EVIDENCE/0017/cursor-agent-transcript.raw.jsonl`
- `EVIDENCE/0017/cursor-agent-transcript.md`
  - `EVIDENCE/0017/cursor-terminal-1.txt`
  - `EVIDENCE/0017/cursor-terminal-822755.txt`
  - `EVIDENCE/0017/cursor-terminal-822756.txt`
  - `EVIDENCE/0017/cursor-terminal-822757.txt`
  - `EVIDENCE/0017/cursor-terminal-822758.txt`
  - `EVIDENCE/0017/cursor-terminal-822759.txt`

Transcript SHA-256:

```text
473083d93510c805cd16aa7b78ced82881ab480fbdf6462426f4c9fe7527fa31  cursor-agent-transcript.raw.jsonl
ad12634585dee1f5cc3286e7025f5c9cbd3e096fa9e03161ce4fff6175280f88  cursor-agent-transcript.md
```

## Expected Pressure

Task 02 from `EXP-0002-task02-quick-calculator-clear-label`: rename the roof quick calculator clear button label while preserving behavior and avoiding surrounding-file restructuring.

## Outcome

The Active working tree at preservation contained one tracked modification and no untracked files:

```text
 M components/roof/RoofQuickLinearCalculator.vue
```

Tracked diff before preservation:

```text
M	components/roof/RoofQuickLinearCalculator.vue
```

`git diff --stat HEAD` before preservation:

```text
 components/roof/RoofQuickLinearCalculator.vue | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

Untracked files before preservation:

```text
(none)
```

`git diff --check` before preservation:

```text
(no whitespace errors)
```

## Verification

Archive verification completed before cleanup:

```text
testzip=OK
entry_count=678
has_git=True
archive_size=3481899
```

The archive was checked for transcript-related entries:

```text
matching_entries=0
```

The transcript is not inside the archive ZIP. It is preserved in `EVIDENCE/0017` beside the archive evidence.

The archive was checked for generated dependency/build directories:

```text
node_modules=False
.nuxt=False
.output=False
```

Runtime verification was not completed by Codex. The exported Cursor transcript reports the exact one-line label change. No preserved typecheck/build/browser verification output exists for this run.

Active HEAD before preservation:

```text
cd393ddd60548823dabd6875060247693a22c1be
```

`diff.patch` contains tracked changes only. `untracked-files.txt` is empty.

## Observed Failures / Strengths

Observed transcript events only, without architecture-quality scoring:

- Cursor began without a `/layered-codebase-architecture` invocation and without manually attached skill content.
- Cursor searched for the clear-label text and located the quick calculator.
- Cursor edited only `components/roof/RoofQuickLinearCalculator.vue`.
- Cursor changed `Clear entries` to `Clear manual entries`.
- Cursor did not create, rename, or restructure surrounding files.
- Cursor ended with `status: success`.

## Suspected Skill Gap (Hypothesis)

Not evaluated in this preservation step. The result is useful as the no-skill control cell for the Grok 4.6 High EXP-0002 holdout block.

## Next Experiment

Clear Active and recreate it from Mother, install `01-V1-CANDIDATE` into Cursor global `skills-cursor`, then run `0018` as the forced V1 arm.
