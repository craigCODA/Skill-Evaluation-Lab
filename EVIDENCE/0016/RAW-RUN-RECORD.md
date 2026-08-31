# Run 0016 - supplied original forced Task 02 quick calculator clear label, Grok 4.6 High

- Date/time: 2026-08-31 CDT; exact archive timestamp is recorded in `EVIDENCE/0016/archive-manifest.json`
- Operator: Codex workplace operator
- Mode: supplied-original skill run
- Subject model + exact version: `Grok 4.6 High` from operator selection; the exported Cursor transcript does not independently encode the model identifier
- Model settings / tools: Cursor harness; raw internal agent transcript exported from the Cursor project store; exact reasoning/effort setting was not independently captured in the transcript
- Target repository: ShingleFile
- Target starting commit: `cd393ddd60548823dabd6875060247693a22c1be`
- Skill: `layered-codebase-architecture`
- Skill condition: supplied original (`00-SUPPLIED`)
- Skill invocation: forced
- Skill runtime path: `%USERPROFILE%/.cursor/skills-cursor/layered-codebase-architecture/`
- Skill version / SHA-256:

```text
SKILL_DIR=C:\Users\NeverAMoment\.cursor\skills-cursor\layered-codebase-architecture
093d1a371b695a8bdcf6bb2ae6bdd4c28b582ecd51ed1e4600db2630c7ae5221  conventions.md
0cd727e9ea67ed5410c07bde1ab5c19f50f09d71f6ae643b9ce19f91b487a969  MANIFEST.txt
306676f83773c6c1fb5c057113d0f0b67e61a31eaa05badf4730bd4de35ffb1c  RATIONALE.md
0cb645117d1916616bc0474a049820a1a833c60f82b38d7a2f209510436fe4d0  SKILL.md
```

## Change Request

Planned prompt from `PROMPT.txt`:

```text
In the roof quick calculator, the bottom button says “Clear entries,” but it only clears the manually entered ridge, hip, valley, eave, and rake values. Rename it to “Clear manual entries” so the label matches what it actually does. Don’t change the behavior. Do not restructure surrounding files.
```

Cursor prompt as exported:

```text
/layered-codebase-architecture  the roof quick calculator, the bottom button says “Clear entries,” but it only clears the manually entered ridge, hip, valley, eave, and rake values. Rename it to “Clear manual entries” so the label matches what it actually does. Don’t change the behavior. Do not restructure surrounding files.
```

Prompt note: The exported Cursor user query omitted the leading word `In` from `PROMPT.txt`; this record preserves the exported query exactly and does not rewrite the specimen.

## Result Asset

- Archive filename: `run-0016-grok46-original-exp0002-supplied.zip`
- Archive SHA-256: `fb8a13bda7dc6f8fe14f30e5ef554ccfbe3652ef43bdef9ddad49195accd3efe`
- Archive location: `ARCHIVES/local/run-0016-grok46-original-exp0002-supplied.zip`
- Archive durability: local-only, publication pending; do not treat this ZIP as retrievable from a fresh clone until it is attached to a durable release/artifact store.

## Transcript/Trace

- `EVIDENCE/0016/cursor-agent-transcript.raw.jsonl`
- `EVIDENCE/0016/cursor-agent-transcript.md`
  - `EVIDENCE/0016/cursor-terminal-671231.txt`

Transcript SHA-256:

```text
bab240dd1fd36ec80e7cb7155ca1bf461ef7ccf47a4ac4b28c164be7120ea38f  cursor-agent-transcript.raw.jsonl
4c18b8aedf2bacd82d6f84b54e08112f7ff69aaee253dee9b1c33a3e3c471108  cursor-agent-transcript.md
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
archive_size=3484466
```

The archive was checked for transcript-related entries:

```text
matching_entries=0
```

The transcript is not inside the archive ZIP. It is preserved in `EVIDENCE/0016` beside the archive evidence.

The archive was checked for generated dependency/build directories:

```text
node_modules=False
.nuxt=False
.output=False
```

Runtime verification was not completed by Codex. The exported Cursor transcript reports the exact one-line label change and says browser clicking was not available. No preserved typecheck/build/browser verification output exists for this run.

Active HEAD before preservation:

```text
cd393ddd60548823dabd6875060247693a22c1be
```

`diff.patch` contains tracked changes only. `untracked-files.txt` is empty.

## Observed Failures / Strengths

Observed transcript events only, without architecture-quality scoring:

- Cursor began with the forced `/layered-codebase-architecture` invocation and inlined skill content.
- Cursor searched for the clear-label text and then used the Active workspace path directly.
- Cursor edited only `components/roof/RoofQuickLinearCalculator.vue`.
- Cursor changed `Clear entries` to `Clear manual entries`.
- Cursor did not create, rename, or restructure surrounding files.
- Cursor reported that no browser/app verification was available in its tool context.
- Cursor ended with `status: success`.

## Suspected Skill Gap (Hypothesis)

Not evaluated in this preservation step. The result is useful as a holdout cell for whether the supplied original skill causes overreach on a label-only task.

## Next Experiment

Clear Active and recreate it from Mother, then run `0017` as the no-skill control with no `layered-codebase-architecture` folder present in Cursor global `skills-cursor` directory.
