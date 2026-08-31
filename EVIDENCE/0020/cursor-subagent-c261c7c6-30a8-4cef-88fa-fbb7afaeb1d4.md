# Cursor Subagent Transcript - Run 0020

Full-fidelity source is preserved in the paired raw JSONL file. This Markdown view records message/tool sequence and the exported user query without inlining the full skill body.

## Event 1 - user

User query exported by Cursor:

~~~text
Explore the ShingleFile codebase at D:\Downloads\Skill-Evaluation-Lab\ACTIVE\ShingleFile-main thoroughly.

Goal: understand how roof "rake" lines work in the "roof quick calculator", specifically pitch requirement vs hip/valley.

Context from user:
- In the roof quick calculator, a drawn rake can be put back on "Plan only," and it still contributes to the totals like that is valid.
- Rake pitch is required; hip and valley pitch are optional.
- We need to make an unpitched rake clearly incomplete and keep it out of the quick calculator totals until a pitch is selected.
- Do NOT change the line-drawing workflow or proposal/report behavior.

Please find:
1. Overall repo structure (top-level folders, layers)
2. Roof quick calculator UI, domain, adapters related to rakes, hips, valleys, pitch
3. How "Plan only" pitch works
4. How totals are calculated for rakes vs hips/valleys
5. Any existing completeness/validation logic for pitch
6. Relevant file paths with brief description
7. How capabilities are currently named (for noun-map)

Return:
- File paths and key functions/types
- How rake pitch currently flows from UI → totals
- Hip/valley pitch handling for contrast
- Suggested domain vs UI vs adapter placement for the fix
- Any existing tests

Be very thorough. Search for: rake, pitch, "Plan only", planOnly, plan-only, hip, valley, quick calculator, roof calculator.
~~~

## Event 2 - assistant

Text:

~~~text
I'll map the repo structure and search for rake/pitch/quick-calculator paths so we can trace how plan-only rakes reach totals.
~~~

Tool use: UpdateCurrentStep

~~~json
{
  "current_step": "Exploring roof rake pitch"
}
~~~

Tool use: Shell

~~~json
{
  "command": "Get-ChildItem -Force | Select-Object Mode, Name; Write-Host \"---\"; Get-ChildItem -Directory -Recurse -Depth 2 | Select-Object FullName | ForEach-Object { $_.FullName.Replace((Get-Location).Path + '\\', '') }",
  "working_directory": "D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main",
  "description": "List top-level and nested folders"
}
~~~

Tool use: Grep

~~~json
{
  "pattern": "rake|planOnly|plan-only|Plan only|Plan Only",
  "path": "D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main",
  "-i": true,
  "glob": "*.{ts,tsx,js,jsx,cs,py,md,json}",
  "head_limit": 80
}
~~~

Tool use: Grep

~~~json
{
  "pattern": "quick.?calc|roof.?calc|RoofQuick|QuickCalc",
  "path": "D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main",
  "-i": true,
  "glob": "*.{ts,tsx,js,jsx,cs,py,md}",
  "head_limit": 60
}
~~~

Tool use: Glob

~~~json
{
  "glob_pattern": "**/*.{ts,tsx,cs,py}",
  "target_directory": "D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main"
}
~~~

Tool use: Read

~~~json
{
  "path": "C:\\Users\\NeverAMoment\\.cursor\\skills-cursor\\layered-codebase-architecture\\SKILL.md",
  "limit": 80
}
~~~

## Event 3 - assistant

Text:

~~~text
The first search came up empty — checking what this repo actually contains.
~~~

Tool use: AwaitShell

~~~json
{
  "shell_id": "11506",
  "block_until_ms": 15000
}
~~~

Tool use: Glob

~~~json
{
  "glob_pattern": "**/*",
  "target_directory": "D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main"
}
~~~

Tool use: Shell

~~~json
{
  "command": "dir; Write-Host \"====\"; Get-ChildItem -Force | Format-Table Name, Mode, Length -AutoSize",
  "description": "List root directory contents",
  "working_directory": "D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main"
}
~~~

## Event 4 - assistant

Text:

~~~text
Nuxt/Vue project confirmed. Digging into roof calculator, rake, and pitch next.
~~~

Tool use: UpdateCurrentStep

~~~json
{
  "current_step": "Searching rake and pitch"
}
~~~

Tool use: Read

~~~json
{
  "path": "C:\\Users\\NeverAMoment\\.cursor\\projects\\d-Downloads-Skill-Evaluation-Lab-ACTIVE-ShingleFile-main\\terminals\\11506.txt",
  "limit": 80
}
~~~

Tool use: Grep

~~~json
{
  "path": "D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main",
  "pattern": "rake|Rake|RAKE",
  "head_limit": 100
}
~~~

Tool use: Grep

~~~json
{
  "path": "D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main",
  "pattern": "planOnly|plan-only|Plan only|Plan Only|plan_only",
  "head_limit": 80
}
~~~

Tool use: Grep

~~~json
{
  "path": "D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main",
  "pattern": "pitch|Pitch|hip|Hip|valley|Valley",
  "head_limit": 120
}
~~~

Tool use: Grep

~~~json
{
  "path": "D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main",
  "pattern": "quick.?calc|QuickCalc|roof.?calc|RoofCalc|roof calculator",
  "-i": true,
  "head_limit": 80
}
~~~

Tool use: Shell

~~~json
{
  "command": "Get-ChildItem -Directory -Recurse -Depth 2 | ForEach-Object { $_.FullName.Replace('D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main\\', '') } | Sort-Object",
  "description": "List folders depth 2"
}
~~~

## Event 5 - assistant

Text:

~~~text
Grep isn't matching source; switching to shell search under `components/roof` and `shared/calculator`.
~~~

Tool use: Shell

~~~json
{
  "command": "rg -i -n \"rake|planOnly|plan-only|Plan only|pitch|hip|valley|quick.?calc\" --glob \"!node_modules\" --glob \"!package-lock.json\" -g \"*.{ts,tsx,vue,js,md}\" . 2>&1 | Select-Object -First 150",
  "description": "Ripgrep rake pitch hip valley"
}
~~~

Tool use: Shell

~~~json
{
  "command": "Get-ChildItem -Recurse -File -Include *.ts,*.vue,*.js,*.md | Where-Object { $_.FullName -notmatch 'node_modules' } | Select-Object -First 200 FullName | ForEach-Object { $_.FullName.Replace('D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main\\', '') }",
  "description": "List source files in repo"
}
~~~

Tool use: Shell

~~~json
{
  "command": "Get-ChildItem -Recurse components\\roof, shared\\calculator, pages\\calculator, composables | Select-Object FullName, Length | ForEach-Object { \"$($_.Length) $($_.FullName.Replace('D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main\\', ''))\" }",
  "description": "List roof and calculator files"
}
~~~

## Event 6 - assistant

Text:

~~~text
Core files identified. Tracing rake pitch from measurements through the quick calculator.
~~~

Tool use: UpdateCurrentStep

~~~json
{
  "current_step": "Reading rake pitch flow"
}
~~~

Tool use: Read

~~~json
{
  "path": "D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main\\shared\\roofLineMeasurements.ts"
}
~~~

Tool use: Read

~~~json
{
  "path": "D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main\\components\\roof\\RoofQuickLinearCalculator.vue"
}
~~~

Tool use: Shell

~~~json
{
  "command": "rg -n -i \"plan.?only|planOnly|roofLineUsesPitch|pitchRise|incomplete|required.*pitch|usesPitch|rake|hip|valley\" shared/roofLineMeasurements.ts composables/useRoofMeasurements.ts components/roof/RoofQuickLinearCalculator.vue components/roof/RoofImageMeasurePanel.vue utils docs .cursor 2>&1; Write-Host \"====FILES====\"; Get-ChildItem -Recurse -File shared,utils,composables,.cursor -ErrorAction SilentlyContinue | ForEach-Object { $_.FullName.Replace('D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main\\', '') }",
  "description": "Search pitch/plan-only in key files"
}
~~~

## Event 7 - assistant

Text:

~~~text
Found the bug surface: `required` pitch is metadata only—totals still count plan feet. Tracing measurement wiring, validation, and tests.
~~~

Tool use: Shell

~~~json
{
  "command": "rg -n \"roofLineAdjustedFeet|roofLineMeasurementTotals|pitchAdjustment|measuredLines|RoofQuickLinear|plan only|Plan only|countsTowardRoofTotal\" --glob \"!package-lock.json\" . 2>&1 | Select-Object -First 120; Write-Host \"====TESTS====\"; Get-ChildItem -Recurse -File -Include *test*,*spec*,*.test.*,*.spec.* -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch 'node_modules' } | ForEach-Object { $_.FullName.Replace('D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main\\', '') }; Write-Host \"====NOUN====\"; if (Test-Path .cursor) { Get-ChildItem -Recurse .cursor | ForEach-Object { $_.FullName } } else { \"no .cursor\" }; Write-Host \"====PKG====\"; Select-String -Path package.json -Pattern \"test|vitest|jest|playwright\"",
  "description": "Find usages, tests, noun-map"
}
~~~

Tool use: Read

~~~json
{
  "path": "D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main\\composables\\useRoofMeasurements.ts",
  "limit": 200
}
~~~

Tool use: Read

~~~json
{
  "path": "D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main\\components\\roof\\RoofImageMeasurePanel.vue",
  "offset": 160,
  "limit": 220
}
~~~

Tool use: Read

~~~json
{
  "path": "D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main\\components\\roof\\RoofMeasurementWorkspaceSection.vue",
  "limit": 150
}
~~~

Tool use: Read

~~~json
{
  "path": "D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main\\shared\\roofMeasurement.ts"
}
~~~

## Event 8 - assistant

Tool use: Read

~~~json
{
  "path": "D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main\\shared\\roofProbeReport.ts"
}
~~~

Tool use: Read

~~~json
{
  "path": "D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main\\components\\roof\\RoofImageMeasurePanel.vue",
  "offset": 620,
  "limit": 80
}
~~~

Tool use: Read

~~~json
{
  "path": "D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main\\package.json"
}
~~~

Tool use: Read

~~~json
{
  "path": "D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main\\README.md"
}
~~~

Tool use: Shell

~~~json
{
  "command": "rg -n -i \"pitchAdjustment|roofLineAdjusted|incomplete|missing.?pitch|required.?pitch|Plan only|plan only|countsToward\" --glob \"!package-lock.json\" . 2>&1; Write-Host \"====\"; rg -n \"roofLineMeasurement|measuredLines|pitchRiseOver12\" shared server utils composables pages --glob \"!node_modules\" 2>&1 | Select-Object -First 80; Write-Host \"====DOCS====\"; Get-ChildItem docs -Recurse | ForEach-Object { $_.Name }",
  "description": "Find validation and report pitch usage"
}
~~~

## Event 9 - assistant

Tool use: Shell

~~~json
{
  "command": "rg -n \"adjustedFeet|pitchRise|label|feet|Plan\" components/roof/RoofImageMeasurePanel.vue utils/captureRoofDrawingScreenshot.ts 2>&1 | Select-Object -First 60; Write-Host \"====\"; rg -n \"RoofQuickLinear|quick.?calc|measuredLines|rakeDrip\" components pages composables shared --glob \"!node_modules\" 2>&1 | Select-Object -First 40; Write-Host \"====VALIDATION====\"; rg -n -i \"pitch|rake|complete|valid\" shared/validation.ts server/utils/estimateValidation.ts 2>&1 | Select-Object -First 40; Write-Host \"====GROK====\"; rg -n -i \"rake|hip|valley|pitch\" server/utils/grokRoofLines.ts 2>&1 | Select-Object -First 40",
  "description": "Check canvas labels, validation, AI lines"
}
~~~

Tool use: Read

~~~json
{
  "path": "D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main\\utils\\captureRoofDrawingScreenshot.ts",
  "limit": 80
}
~~~

Tool use: Read

~~~json
{
  "path": "D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main\\composables\\useRoofProbeReport.ts"
}
~~~

Tool use: Read

~~~json
{
  "path": "D:\\Downloads\\Skill-Evaluation-Lab\\ACTIVE\\ShingleFile-main\\pages\\roof-probe.vue",
  "limit": 100
}
~~~

Tool use: Read

~~~json
{
  "path": "C:\\Users\\NeverAMoment\\.cursor\\skills-cursor\\layered-codebase-architecture\\conventions.md",
  "limit": 80
}
~~~

## Event 10 - assistant

Tool use: Shell

~~~json
{
  "command": "rg -n \"RoofMeasurementWorkspaceSection|RoofQuickLinear|latestMeasuredLines\" pages components 2>&1; Write-Host \"====\"; Get-ChildItem components\\roof | ForEach-Object { $_.Name }; Write-Host \"====APPNAV====\"; rg -n \"roof-probe|ShingleScope|calculator\" shared/appNav.ts pages/index.vue 2>&1 | Select-Object -First 30",
  "description": "Confirm quick calc page wiring"
}
~~~

Tool use: UpdateCurrentStep

~~~json
{
  "current_step": "Summarizing rake pitch findings",
  "final_summary": "Rake pitch is marked `required` in `shared/roofLineMeasurements.ts`, but totals ignore that: `roofLineAdjustedFeet` still counts plan feet when pitch is missing, so Quick Calculator “Plan only” rakes inflate totals. Hip/valley stay optional and correctly may stay unpitched. Fix belongs in domain totals + Quick Calculator UI incompleteness—not drawing or proposal flows. No tests cover this today.",
  "completed_subtitle": "Mapped rake pitch totals gap"
}
~~~

## Event 11 - assistant

Text:

~~~text
## Verdict

Rake is already declared `pitchAdjustment: "required"` in domain metadata, but **totals never enforce it**. Choosing **Plan only** clears `pitchRiseOver12` and `roofLineAdjustedFeet` still returns plan feet, so the rake stays in Quick Calculator totals. Hip/valley are `optional` and the same plan-foot fallback is intentional for them.

---

## 1. Repo structure

Nuxt 4 Vue app (`roof-calc-nuxt`). Stated goal: business logic in `shared/`.

| Layer | Path | Role |
|---|---|---|
| Routes / UI pages | `pages/` | Workflow routes; ShingleScope = `pages/roof-probe.vue` |
| UI components | `components/`, `components/roof/` | Forms, probe workspace, Quick Calculator |
| UI state | `composables/` | `useRoofMeasurements`, `useRoofProbeReport`, etc. |
| Domain / shared | `shared/` | Line measurements, probe report, estimate calc, contracts, pricebook |
| Server / adapters | `server/api/`, `server/utils/` | Nitro APIs, stores, Solar/Grok helpers |
| Infra / DB | `infra/`, `drizzle/` | AWS + Postgres |
| Utils | `utils/` | Client helpers (e.g. drawing screenshot) |

No `.cursor/noun-map.md`. No unit/integration test runner or `*.test.ts` files.

---

## 2. Quick Calculator wiring (rake / hip / valley / pitch)

**Page flow**

`pages/roof-probe.vue`
→ `useRoofMeasurements()` (`latestMeasuredLines`)
→ `RoofMeasurementWorkspaceSection` (`v-model:lines`)
→ `RoofImageMeasurePanel` (draw) + `RoofQuickLinearCalculator` (`v-model:measured-lines`)

Both panels share the same `RoofLineMeasurement[]`.

**Domain types / metadata** — `D:\Downloads\Skill-Evaluation-Lab\ACTIVE\ShingleFile-main\shared\roofLineMeasurements.ts`

| Type | `pitchAdjustment` | `countsTowardRoofTotal` |
|---|---|---|
| ridge, eave | `none` | true |
| hip, valley | `optional` | true |
| **rake** | **`required`** | true |
| measurement, caution-tape | `none` | false |

Key APIs:
- `RoofLineMeasurement` — `pitchRiseOver12?: number`, `feet`
- `roofLineUsesPitch(type)` — true if adjustment ≠ `"none"` (required **and** optional)
- `roofLinePitchFactor(rise)` — `√(rise²+12²)/12`
- `roofLineAdjustedFeet(line)` — apply factor **or** return plan feet
- `roofLineMeasurementTotals(lines)` — sum adjusted feet per type

**Drawing UI** — `components/roof/RoofImageMeasurePanel.vue`
- Pitch picker only when `activeTypeUsesPitch()` (hip/valley/rake).
- Options are **3:12–12:12 only** — no Plan only.
- On commit: `pitchRiseOver12: activeTypeUsesPitch() ? activePitchRiseOver12 : undefined` (default rise `6`).
- Canvas labels show **plan** `line.feet` only.

**Quick Calculator UI** — `components/roof/RoofQuickLinearCalculator.vue`
- Manual LF inputs + measured totals.
- Drawn-line pitch `<select>` with **`<option value="">Plan only</option>`**.
- `onPitchChange` → `updateLinePitch` sets `pitchRiseOver12` to a number or `undefined`.

---

## 3. How “Plan only” works

UI: empty select value → `pitchRiseOver12 = undefined`.

Display helper:
```ts
if (line.pitchRiseOver12 === undefined) return "plan";
```
→ subtitle like `12.0 plan - plan`.

Domain fallback (the bug for required rake):
```188:194:shared/roofLineMeasurements.ts
export function roofLineAdjustedFeet(line: RoofLineMeasurement): number {
  const meta = roofLineTypeMeta(line.type);
  if (meta.pitchAdjustment === "none" || line.pitchRiseOver12 === undefined) {
    return line.feet;
  }
  return line.feet * roofLinePitchFactor(line.pitchRiseOver12);
}
```

`pitchAdjustment: "required"` is **never read** for completeness or exclusion—only `"none"` vs not-none via `roofLineUsesPitch`.

---

## 4. Totals: rake vs hip/valley

```ts
// Quick Calculator
measuredTotals = roofLineMeasurementTotals(measuredLines)
combinedTotals[key] = manualInput[key] + measuredTotals[key]
dripEdgeFt = eave + rake
totalLinearFt = sum of ridge/hip/valley/eave/rake
```

| Scenario | Behavior today |
|---|---|
| Rake with pitch | plan × pitch factor → totals |
| Rake Plan only | **plan feet still counted** |
| Hip/valley with pitch | plan × factor |
| Hip/valley Plan only | plan feet counted (intended for optional) |

Probe report (`shared/roofProbeReport.ts`) uses `roofLineMeasurementTotals(...).ridge` only for ventilation. Proposal/estimate rake uses **separate** `area.rakeDripLf` on the job form—not Quick Calculator lines.

---

## 5. Completeness / validation today

- **None** for line pitch completeness.
- `shared/validation.ts` / `server/utils/estimateValidation.ts` are estimate-job fields only.
- Metadata already encodes intent (`required` vs `optional`) but is unused for gating.

---

## 6. Relevant paths

| Path | Role |
|---|---|
| `shared/roofLineMeasurements.ts` | Line types, pitch rules, adjusted feet, totals |
| `components/roof/RoofQuickLinearCalculator.vue` | Quick Calculator UI + Plan only pitch edits |
| `components/roof/RoofImageMeasurePanel.vue` | Drawing; always assigns pitch for pitched types |
| `components/roof/RoofMeasurementWorkspaceSection.vue` | Layout: draw + calculator |
| `composables/useRoofMeasurements.ts` | Persist `lines` in IndexedDB history |
| `composables/useRoofProbeReport.ts` | Builds probe report from measurement + lines |
| `shared/roofProbeReport.ts` | Report stats; ridge LF from line totals |
| `pages/roof-probe.vue` | ShingleScope page |
| `utils/captureRoofDrawingScreenshot.ts` | Export image (plan feet labels) |
| `components/roof/RoofPlaneEdgesSection.vue` | Estimate form rake LF (separate path) |
| `shared/options/dripEdge.ts` | Billed drip from estimate area LF |

---

## 7. Capability naming (noun-map sketch)

No noun map in repo. Live naming is inconsistent:

| Concern | Route | UI | Composable | Domain | Alias |
|---|---|---|---|---|---|
| ShingleScope / probe | `/roof-probe` | `RoofProbe*`, workspace | `useRoofMeasurements` | `roofMeasurement`, `roofProbeReport` | ShingleScope |
| Drawn linears / Quick Calc | (same page) | `RoofQuickLinearCalculator`, `RoofImageMeasurePanel` | (state in `useRoofMeasurements`) | **`roofLineMeasurements`** | Quick calculator |
| Estimate roof scope | `/estimates/...`, `/calculator` | `RoofingScopeForm`, `RoofPlane*` | `useEstimates` | `roofArea`, `calculator`, `options` | |

Best noun for this fix: **`RoofLineMeasurements`** (already the domain module name).

---

## UI → totals flow (rake)

1. Draw rake → panel stores `feet` + `pitchRiseOver12` (default 6).
2. Quick Calculator lists line; pitch select can clear to Plan only → `undefined`.
3. `roofLineMeasurementTotals` → `roofLineAdjustedFeet` → **plan feet** when undefined.
4. That sum feeds measured badge, type totals, drip edge, total linear.

Hip/valley: same pipeline; Plan only is valid because `optional`.

---

## Suggested placement for the fix

**Domain (`shared/roofLineMeasurements.ts`) — primary**
- Honor `pitchAdjustment === "required"`:
  - e.g. `roofLineIsPitchComplete(line)` / `roofLineCountsInQuickTotals(line)`
  - In `roofLineMeasurementTotals` (or a dedicated quick-totals helper), **exclude** incomplete required lines (or contribute `0`).
- Keep `roofLineAdjustedFeet` useful for “plan length” display, or split “display feet” vs “billable/total feet” so Plan-only rakes can still show plan LF while totals ignore them.
- Hip/valley unchanged (optional + undefined → plan feet OK).

**UI (`RoofQuickLinearCalculator.vue`) — secondary**
- Incomplete rake styling / copy (“needs pitch”).
- Optionally relabel Plan only for required types (e.g. “Select pitch”) without removing the empty value—user asked not to change **drawing** workflow; calculator pitch editing is in scope.
- Drive off domain predicates; don’t re-encode required/optional in the Vue file.

**Adapter / composables / drawing / proposal**
- **No change** to `RoofImageMeasurePanel` draw path, screenshot, estimate/proposal, or report ridge logic (ridge is `none`; rake exclusion doesn’t affect ventilation).
- Prefer changing shared totals carefully; if report must stay byte-identical for other types, add a quick-calc-specific totals function and use it only in the calculator—but excluding incomplete **rakes** from the shared totals function is safe for current report usage.

---

## Tests

**None** for pitch/totals/Quick Calculator. `package.json` has no `test` script (only `typecheck` / `build`). Closest place for new coverage: `shared/roofLineMeasurements.test.ts` next to the domain module.
~~~

## Event 12 - 

