# Run 0018 - candidate V1 forced Task 02 quick calculator clear label, Grok 4.6 High

- Date/time: 2026-08-31 CDT; exact archive timestamp is recorded in `EVIDENCE/0018/archive-manifest.json`
- Operator: Codex workplace operator
- Mode: candidate-skill V1 run
- Subject model + exact version: `Grok 4.6 High` from operator selection; the exported Cursor transcript does not independently encode the model identifier
- Model settings / tools: Cursor harness; raw internal agent transcript exported from the Cursor project store; exact reasoning/effort setting was not independently captured in the transcript
- Target repository: ShingleFile
- Target starting commit: `cd393ddd60548823dabd6875060247693a22c1be`
- Skill: `layered-codebase-architecture`
- Skill condition: candidate V1 (`01-V1-CANDIDATE`)
- Skill invocation: forced
- Skill runtime path: `%USERPROFILE%/.cursor/skills-cursor/layered-codebase-architecture/`
- Skill version / SHA-256:

```text
SKILL_DIR=C:\Users\NeverAMoment\.cursor\skills-cursor\layered-codebase-architecture
c997e0659a92f00671a4931523b038f34357a6121012a8f88f4bb53c3bbda2b7  conventions.md
ef50b3c6a661e01ed761df5815fa90f263c032c8d6f38da6eeb14413f6a9844d  FROM-00.diff
f76b8a0326f0d00b099e322f8ae12ca367cf7551747397d648599bc4e0525f11  MANIFEST.txt
ca59bf6ac18818ecf3977c389d521f8b99f46d0cd663fd538ae4335351aa4e7c  RATIONALE.md
7f760abe7228a62d1a7abf37b20f5b87a2b9ea0711431260300231bd0f630414  SKILL.md
```

## Change Request

Planned prompt from `PROMPT.txt`:

```text
In the roof quick calculator, the bottom button says “Clear entries,” but it only clears the manually entered ridge, hip, valley, eave, and rake values. Rename it to “Clear manual entries” so the label matches what it actually does. Don’t change the behavior. Do not restructure surrounding files.
```

Cursor initial prompt as exported:

```text
/layered-codebase-architecture  In the roof quick calculator, the bottom button says “Clear entries,” but it only clears the manually entered ridge, hip, valley, eave, and rake values. Rename it to “Clear manual entries” so the label matches what it actually does. Don’t change the behavior. Do not restructure surrounding files.
```

Prompt note: The exported initial user query differs from `PROMPT.txt`; this record preserves the exported query exactly and does not rewrite the specimen.

## Result Asset

- Archive filename: `run-0018-grok46-v1-exp0002-candidate.zip`
- Archive SHA-256: `0171d05a2dda3aa15bce8424e3996fb2e18f8eeebf2cde7b64bcee8d98dba944`
- Archive location: `ARCHIVES/local/run-0018-grok46-v1-exp0002-candidate.zip`
- Archive durability: local-only, publication pending; do not treat this ZIP as retrievable from a fresh clone until it is attached to a durable release/artifact store.

## Transcript/Trace

- `EVIDENCE/0018/cursor-agent-transcript.raw.jsonl`
- `EVIDENCE/0018/cursor-agent-transcript.md`
  - `EVIDENCE/0018/cursor-terminal-290920.txt`
  - `EVIDENCE/0018/cursor-terminal-290921.txt`
  - `EVIDENCE/0018/cursor-terminal-290922.txt`

Transcript SHA-256:

```text
6eed9e97074311879b9210ec0e1a7c7e4ecb9bcfa40bcc482e03a362ca43f8c4  cursor-agent-transcript.raw.jsonl
874aba434cb843648cb96e74660072e72988271a212cbe08c2e54ba383c061cf  cursor-agent-transcript.md
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
archive_size=3482428
```

The archive was checked for transcript-related entries:

```text
matching_entries=0
```

The transcript is not inside the archive ZIP. It is preserved in `EVIDENCE/0018` beside the archive evidence.

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

- Cursor began with the forced `/layered-codebase-architecture` invocation and inlined V1 skill content.
- Cursor searched for the clear-label text and located the quick calculator.
- Cursor edited only `components/roof/RoofQuickLinearCalculator.vue`.
- Cursor changed `Clear entries` to `Clear manual entries`.
- Cursor did not create, rename, or restructure surrounding files.
- Cursor ended with `status: success`.

## Suspected Skill Gap (Hypothesis)

Not evaluated in this preservation step. The result is useful as the V1 candidate cell for the Grok 4.6 High EXP-0002 holdout block.

## Next Experiment

Clear Active and recreate it from Mother, install `02-V2-GRAPH` into Cursor global `skills-cursor`, then run `0019` as the forced V2 arm.
