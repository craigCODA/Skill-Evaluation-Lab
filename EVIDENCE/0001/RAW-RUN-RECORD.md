# Run 0001 - supplied-original forced Task 01 roof image measure
- Date/time: 2026-08-28 UTC; exact archive timestamp is recorded in `EVIDENCE/0001/archive-manifest.json`
- Operator: Codex workplace operator
- Mode: supplied-skill
- Subject model + exact version: Grok 4.6 High
- Model settings / tools: Cursor harness; transcript export identifies Cursor `3.17.21`
- Target repository: ShingleFile
- Target starting commit: `cd393ddd60548823dabd6875060247693a22c1be`
- Skill: `layered-codebase-architecture`
- Skill condition: supplied-original
- Skill invocation: forced
- Skill runtime path: `%USERPROFILE%/.cursor/skills-cursor/layered-codebase-architecture/`
- Skill version / commit / SHA-256:
  - `SKILL.md`: `d2fedfdcb0f4bd055b8605c00fc98ae0b99036e1a0fbfa3d34a458be876998c7`
  - `conventions.md`: `912b9274ea5f829c1082b8ad40b1fd5bfdd96aa603b307c4f0c79d863c4fa5da`
- Skill hash provenance: actual Cursor-installed runtime files reverified byte-for-byte before retirement at `%USERPROFILE%/.cursor/skills-cursor/layered-codebase-architecture/`
- Change request:

```text
this roof image measure panel has gotten ridiculous. clean it up and structure it in a way that makes sense without changing how it works.
```

- Archive filename: `0001-supplied-original-forced-task01-roof-image-measure.zip`
- Transcript/trace: `EVIDENCE/0001/cursor_roof_image_measure_panel.md`
- Transcript SHA-256: `206b936cc141af4a146d55e588bd9b4c62f92137c5734177b944b9b0b6751c00`
- Operator intervention during agent run: transcript shows one user task prompt and one Cursor response; no in-run operator correction/intervention is visible in the supplied transcript

## Expected pressure

Task 01 from `EXPLORATORY-BATCH.md`: `components/roof/RoofImageMeasurePanel.vue` was the target pressure component, described there as approximately 800 lines.

## Outcome

Cursor reported that the aerial measure editor was split around the capability name `ImageMeasure`.

Cursor reported this structure:

```text
shared/roofImageMeasure.ts
- crop
- scale
- georef fallback
- pointer math
- pitch snapping

composables/useRoofImageMeasure.ts
- tool tabs
- drafts
- pointer handlers
- markup mutations

components/roof/ImageMeasure/
- RoofImageMeasurePanel
- RoofImageMeasureCanvas
- RoofImageMeasureToolbar
- LinesPanel
- IconsPanel
- AreasPanel
```

Cursor also reported:

```text
- RoofDrawingActionsPanel unchanged
- existing CSS classes preserved
- existing RoofImageMeasurePanel usage preserved
- runtime verification was NOT completed because node_modules was missing
- it recommended manually exercising /roof-probe after dependencies are installed
```

These are Cursor's reported claims, not operator-verified product findings.

## Verification

Runtime verification was unavailable because `ACTIVE/ShingleFile-main/node_modules` was absent. `Test-Path ACTIVE/ShingleFile-main/node_modules` returned `False`.

Transcript provenance:

```text
file: EVIDENCE/0001/cursor_roof_image_measure_panel.md
exported: 2026-08-27 23:50:22 CDT
source: Cursor 3.17.21
sha256: 206b936cc141af4a146d55e588bd9b4c62f92137c5734177b944b9b0b6751c00
visible interaction pattern: one user prompt with /layered-codebase-architecture, followed by one Cursor response
```

Installed skill provenance was reverified before retirement:

```text
USERPROFILE=C:\Users\NeverAMoment
SKILL_DIR=C:\Users\NeverAMoment\.cursor\skills-cursor\layered-codebase-architecture
SKILL.md       d2fedfdcb0f4bd055b8605c00fc98ae0b99036e1a0fbfa3d34a458be876998c7
conventions.md 912b9274ea5f829c1082b8ad40b1fd5bfdd96aa603b307c4f0c79d863c4fa5da
```

Active HEAD before retirement:

```text
cd393ddd60548823dabd6875060247693a22c1be
```

Exact pre-retirement `git status --porcelain=v1 -uall`:

```text
 D components/roof/RoofImageMeasurePanel.vue
?? .cursor/noun-map.md
?? components/roof/ImageMeasure/RoofImageMeasureAreasPanel.vue
?? components/roof/ImageMeasure/RoofImageMeasureCanvas.vue
?? components/roof/ImageMeasure/RoofImageMeasureIconsPanel.vue
?? components/roof/ImageMeasure/RoofImageMeasureLinesPanel.vue
?? components/roof/ImageMeasure/RoofImageMeasurePanel.vue
?? components/roof/ImageMeasure/RoofImageMeasureToolbar.vue
?? composables/useRoofImageMeasure.ts
?? shared/roofImageMeasure.ts
```

Tracked diff before retirement:

```text
D	components/roof/RoofImageMeasurePanel.vue
```

`git diff --stat HEAD` before retirement:

```text
components/roof/RoofImageMeasurePanel.vue | 800 ------------------------------
1 file changed, 800 deletions(-)
```

Untracked file list before retirement:

```text
.cursor/noun-map.md
components/roof/ImageMeasure/RoofImageMeasureAreasPanel.vue
components/roof/ImageMeasure/RoofImageMeasureCanvas.vue
components/roof/ImageMeasure/RoofImageMeasureIconsPanel.vue
components/roof/ImageMeasure/RoofImageMeasureLinesPanel.vue
components/roof/ImageMeasure/RoofImageMeasurePanel.vue
components/roof/ImageMeasure/RoofImageMeasureToolbar.vue
composables/useRoofImageMeasure.ts
shared/roofImageMeasure.ts
```

Relevant resulting file tree before retirement:

```text
ACTIVE/ShingleFile-main/.cursor/noun-map.md
ACTIVE/ShingleFile-main/components/roof/ImageMeasure/RoofImageMeasureAreasPanel.vue
ACTIVE/ShingleFile-main/components/roof/ImageMeasure/RoofImageMeasureCanvas.vue
ACTIVE/ShingleFile-main/components/roof/ImageMeasure/RoofImageMeasureIconsPanel.vue
ACTIVE/ShingleFile-main/components/roof/ImageMeasure/RoofImageMeasureLinesPanel.vue
ACTIVE/ShingleFile-main/components/roof/ImageMeasure/RoofImageMeasurePanel.vue
ACTIVE/ShingleFile-main/components/roof/ImageMeasure/RoofImageMeasureToolbar.vue
ACTIVE/ShingleFile-main/composables/useRoofImageMeasure.ts
ACTIVE/ShingleFile-main/shared/roofImageMeasure.ts
```

Important evidence caveat: the workplace helper's `EVIDENCE/0001/diff.patch` is generated with `git diff --binary HEAD`, so it records tracked changes but does not include untracked file contents. The full Active archive ZIP preserves untracked files and `.git` metadata.

## Observed failures / strengths

UNKNOWN. Not evaluated in this preservation step.

## Suspected skill gap (hypothesis)

Not evaluated in this preservation step.

## Next experiment

Run 0002 is intended as the no-skill control with the same repository, baseline, Cursor harness, Grok 4.6 High model, and exact Task 01 prompt, after Active is retired and freshly cloned from Mother.
