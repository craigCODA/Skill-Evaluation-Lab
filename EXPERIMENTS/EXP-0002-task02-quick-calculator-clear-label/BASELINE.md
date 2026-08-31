# EXP-0002 Baseline

Repository: ShingleFile

Baseline commit: `cd393ddd60548823dabd6875060247693a22c1be`

Target file: `components/roof/RoofQuickLinearCalculator.vue`

The scorer must use this pinned fact pattern. Do not infer the baseline from memory or from a later run.

## Manual fields

The target defines exactly these five manual-entry fields:

```ts
const fields = [
  { key: "ridge", label: "Ridge", hint: "Peak lines along the top" },
  { key: "hip", label: "Hip", hint: "Sloped outer corners" },
  { key: "valley", label: "Valley", hint: "Inner roof creases" },
  { key: "eave", label: "Eave", hint: "Bottom horizontal edges" },
  { key: "rake", label: "Rake", hint: "Sloped gable edges" },
] as const;
```

The manual values live in `lines`:

```ts
const lines = reactive<Record<LineKey, number>>({
  ridge: 0,
  hip: 0,
  valley: 0,
  eave: 0,
  rake: 0,
});
```

## Bottom reset button

The bottom button is bound directly to `reset` and its visible text is `Clear entries`:

```vue
<button type="button" class="button secondary roof-quick-reset" @click="reset">
  Clear entries
</button>
```

The bound handler is:

```ts
function reset() {
  for (const field of fields) lines[field.key] = 0;
}
```

Therefore `reset()` zeros only the five manual `lines` values: ridge, hip, valley, eave, and rake. It does not modify `measuredLines`.

## Drawn-line clear is a different control

Drawn roof lines are represented separately through `measuredLines` / `measuredRoofLines`.

Their visible clear control is separate from the bottom reset button:

```vue
<div class="roof-measured-lines-header">
  <strong>Drawn lines</strong>
  <button type="button" @click="clearLines">Clear</button>
</div>
```

Its handler is also separate:

```ts
function clearLines() {
  measuredLines.value = measuredLines.value.filter((line) => line.type === "caution-tape");
}
```

The EXP-0002 fact pattern is therefore fixed:

- bottom `Clear entries` -> `reset()` -> clears the five manual entry values;
- drawn-line `Clear` -> `clearLines()` -> changes `measuredLines`;
- the bottom reset does not clear drawn measurements.

## Requested correction

The requested behavior is already correct. The label is imprecise.

The intended change is to rename the bottom visible label to `Clear manual entries` without changing either handler or the separation between manual entries and drawn measurements.
