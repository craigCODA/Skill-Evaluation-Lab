# Run 0014 - candidate V2 forced Task 01 roof image measure, Kimi 2.7
- Date/time: 2026-08-30 CDT; exact archive timestamp is recorded in `EVIDENCE/0014/archive-manifest.json`
- Operator: Codex workplace operator
- Mode: candidate-skill V2 graph run
- Subject model + exact version: `Kimi 2.7` from user correction; the exported Cursor transcript does not independently include the model identifier
- Model settings / tools: Cursor harness; raw internal agent transcript exported from the Cursor project store; exact reasoning/effort setting was not independently captured in the transcript
- Target repository: ShingleFile
- Target starting commit: `cd393ddd60548823dabd6875060247693a22c1be`
- Skill: `layered-codebase-architecture`
- Skill condition: candidate-v2
- Skill invocation: forced
- Skill runtime path: `%USERPROFILE%/.cursor/skills-cursor/layered-codebase-architecture/`
- Skill version / commit / SHA-256:
  - `SKILL.md`: `c183d335cf06102f2d66ac716fc8d1d6e33b85d96f23dd014298d6bdd79e5cd1`
  - `conventions.md`: `5a1dc4af63c8605ee2998c7fba0f1c98506fbbba49abb8bf7a084e9c03be5255`
- Change request:

```text
this roof image measure panel has gotten ridiculous. clean it up and structure it in a way that makes sense without changing how it works.
```

- Cursor prompt as exported:

```text
/layered-codebase-architecture  this roof image measure panel has gotten ridiculous. clean it up and structure it in a way that makes sense without changing how it works.
```

- Archive filename: `0014-candidate-v2-forced-task01-roof-image-measure-kimi27code.zip`
- Archive SHA-256: `19a4b5bcebfdc820172780022ab6771c086a7a69a1c43fd06062f923f3fbfe7a`
- Archive source: `ACTIVE_NEXT/ShingleFile-main-0014`
- Archive method: manual archive equivalent to `workplace.py archive`
- Archive note: official `ACTIVE/ShingleFile-main` was locked and could not be swapped into the lifecycle helper path, so this run was preserved from the parallel ActiveNext clone.
- Transcript/trace:
  - `EVIDENCE/0014/cursor-agent-transcript.raw.jsonl`
  - `EVIDENCE/0014/cursor-agent-transcript.md`
  - `EVIDENCE/0014/cursor-terminal-711493.txt`
- Transcript SHA-256:
  - raw JSONL: `bb53ea27414c1e15b0d93382df72dd36a5270abc1f2350c986d353a563cc410c`
  - markdown: `12d0e649d1e70906238a3dae1c1ed617f663846b48e14920f36b3d4bc852711e`
  - terminal log: `a22c42271665aa97e2417c163d9049c7e9c59f2d4547c0ebc0f51881e5a1a6a5`

## Expected pressure

Task 01 from `EXPLORATORY-BATCH.md`: `components/roof/RoofImageMeasurePanel.vue` was the target pressure component.

## Outcome

The preserved working tree contained three tracked modifications and five untracked files:

```text
 M components/roof/RoofImageMeasurePanel.vue
 M shared/roofImageryScale.ts
 M shared/roofLineMeasurements.ts
?? components/roof/RoofImageMeasureAreaPanel.vue
?? components/roof/RoofImageMeasureCanvas.vue
?? components/roof/RoofImageMeasureIconPanel.vue
?? components/roof/RoofImageMeasureLinePanel.vue
?? components/roof/RoofImageMeasureToolbar.vue
```

Tracked diff before preservation:

```text
M	components/roof/RoofImageMeasurePanel.vue
M	shared/roofImageryScale.ts
M	shared/roofLineMeasurements.ts
```

`git diff --stat HEAD` before preservation:

```text
components/roof/RoofImageMeasurePanel.vue | 721 +++++-------------------------
shared/roofImageryScale.ts                |  78 +++-
shared/roofLineMeasurements.ts            |  10 +
3 files changed, 190 insertions(+), 619 deletions(-)
```

Ignored generated/dependency directories were present in the archived source:

```text
!! .nuxt/
!! .output/
!! node_modules/
```

## Verification

Archive verification completed after preservation:

```text
testzip=OK
entry_count=24963
has_git=True
archive_size=108527837
```

The archive was verified to contain the full source clone, including `.git`, tracked changes, untracked files, and the ignored `.nuxt`, `.output`, and `node_modules` directories. This differs from earlier helper-created archives that excluded generated dependency output.

The archive was also checked for transcript-related entries:

```text
matching_entries=0
```

The transcript is not inside the archive ZIP. It is preserved in `EVIDENCE/0014` beside the archive evidence.

Runtime verification was not completed by Codex. The preserved terminal log is the initial failed `npx nuxt typecheck` run:

```text
ERROR Cannot resolve module "@nuxt/kit"
exit_code=1
```

The exported Cursor transcript later states that `npm run typecheck` passed and `npm run build` completed successfully. No separate successful terminal log for those later commands was found during preservation, so those remain transcript claims rather than independently preserved build evidence.

Installed skill provenance was reverified before preservation:

```text
SKILL_DIR=C:\Users\NeverAMoment\.cursor\skills-cursor\layered-codebase-architecture
SKILL.md        c183d335cf06102f2d66ac716fc8d1d6e33b85d96f23dd014298d6bdd79e5cd1
conventions.md 5a1dc4af63c8605ee2998c7fba0f1c98506fbbba49abb8bf7a084e9c03be5255
```

ActiveNext HEAD before preservation:

```text
cd393ddd60548823dabd6875060247693a22c1be
```

`diff.patch` contains tracked changes only. The five untracked components are listed in `git-status.txt` and `untracked-files.txt`, and are preserved in the full archive ZIP.

## Observed failures / strengths

Observed transcript events only, without architecture-quality evaluation:

- Cursor began with the forced `/layered-codebase-architecture` invocation and inlined skill content.
- Cursor located and mapped the roof image measure capability before editing.
- Cursor discussed seam proof and chose UI component extraction plus shared helper extraction.
- Cursor created `RoofImageMeasureCanvas`, `RoofImageMeasureToolbar`, `RoofImageMeasureLinePanel`, `RoofImageMeasureIconPanel`, and `RoofImageMeasureAreaPanel`.
- Cursor moved geometry and pitch helpers into shared files.
- Cursor caught and repaired tab reset behavior during the run.
- Cursor reported typecheck and build success after the initial failed `npx nuxt typecheck`.

## Suspected skill gap (hypothesis)

Not evaluated in this preservation step.

## Next experiment

Official `ACTIVE/ShingleFile-main` was a clean Mother clone before preservation but remained locked by another process during the attempted swap. The 0014 specimen remains at `ACTIVE_NEXT/ShingleFile-main-0014` unless it is retired after Cursor releases the lock. Proceed to the next workflow from a clean Mother clone, not from this preserved 0014 specimen.
