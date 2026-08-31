# EXP-0004 Baseline

Repository: ShingleFile

Baseline commit: `cd393ddd60548823dabd6875060247693a22c1be`

Use this pinned fact pattern for scoring. Do not infer the baseline from memory, current Active, later runs, or model claims.

The subject model must not receive this file, the scorecard, prior experiment conclusions, expected authority notes, or likely solution shape.

## Premise Verification Summary

The premise is true at the frozen baseline.

Open-valley footage produces a positive `valleyMetal.cost`, but baseline customer totals and proposal pricing do not include that cost. Open valley appears in proposal scope text. Closed/non-open valley behavior produces no valley-metal customer charge.

## 1. Existing Valley-Metal Option Record

`shared/options/valleyMetal.ts` defines the valley-metal option and marks it unbilled:

```ts
36: export const valleyMetalOption: JobOption<ValleyMetalBreakdown> = {
37:   id: "valleyMetal",
38:   title: "Valley Metal",
39:   summary:
40:     "Open-valley metal computed for visibility. NOT billed to the customer; it only informs materials counts.",
41:   phase: "job",
42:   billed: false,
43:   pricingPlain:
44:     "Only open valleys are figured: open-valley feet times the per-foot rate. This is shown for reference and is NOT added to the customer total.",
45:   example: "30 ft of open valley at $3/ft = $90 (reference only — not billed).",
```

The same file states that closed-valley feet are tracked, not billed:

```ts
49:     { name: "Valley style", description: "'open' or 'closed'. Only 'open' is computed for billing visibility." },
50:     { name: "Open valley LF", description: "Linear feet of open valley." },
51:     { name: "Closed valley LF", description: "Linear feet of closed valley (tracked, not billed)." },
```

## 2. Open-Valley Footage Produces `valleyMetal.cost`

`shared/options/valleyMetal.ts` computes `billableLf` from open-valley footage and multiplies by the valley-metal rate:

```ts
28:   const row = (cat.valleyMetalRates as ValleyMetalRate[]).find(
29:     (r) => r.key === "open-valley",
30:   );
31:   const pricePerFoot = row?.pricePerFoot ?? 0;
32:   const billableLf = valleys.style === "open" ? valleys.openLf : 0;
33:   return { pricePerFoot, billableLf, cost: billableLf * pricePerFoot };
```

The estimate calculator computes the option:

```ts
131:   const valleyMetal = valleyMetalOption.compute(jobCtx);
```

The UI displays that computed amount while describing it as not billed:

```vue
405:     <h2>Valley metal</h2>
406:     <p class="v2-note">Computed for visibility only; not added to the customer total.</p>
...
426:         <dt>{{ totals.valleyMetal.billableLf }} ft @ {{ formatMoney(totals.valleyMetal.pricePerFoot) }}/ft (not billed)</dt>
427:         <dd>{{ formatMoney(totals.valleyMetal.cost) }}</dd>
```

## 3. Customer Total Excludes `valleyMetal.cost`

`shared/calculator/calculateEstimate.ts` computes `valleyMetal`, then explicitly excludes it from `grandTotal`:

```ts
131:   const valleyMetal = valleyMetalOption.compute(jobCtx);
132:   const materials = materialsCounts(roofing, catalog);
133:
134:   // valleyMetal is intentionally excluded — it is not billed.
135:   const grandTotal =
136:     areaCosts.reduce((sum, area) => sum + area.total, 0) +
137:     ridge.total +
138:     warranty.cost +
139:     stepFlash.cost +
140:     chimney.cost +
141:     chimneyKit.cost +
142:     accessories.total +
143:     satellite.cost +
144:     antenna.cost +
145:     lightning.cost +
146:     skylights.total +
147:     noAccess.total +
148:     gutterRemoval.cost +
149:     lowSlope.cost +
150:     permit +
151:     extras.amount;
```

There is no `valleyMetal.cost` term in this customer-facing total.

## 4. Proposal And Contract Path

Open valley appears in proposal scope output through `shared/contracts/roofProposalScope.ts`:

```ts
102:   const valleyLf =
103:     roofing.valleys.style === "open"
104:       ? roofing.valleys.openLf
105:       : roofing.valleys.closedLf;
106:   const valleyLine =
107:     valleyLf > 0
108:       ? line(
109:           "Valleys",
110:           `${valleyLf} LF — ${roofing.valleys.style === "open" ? "Open valley" : "Half lace valley"}`,
111:         )
112:       : line("Valleys", "None on this roof");
```

The roof proposal customer price uses `roofingTotals.grandTotal` and `buildRoofPricingLines(...)` in `shared/contracts/roofProposalDocument.ts`:

```ts
63:           {
64:             label:
65:               "I / We the Owner(s) agree to pay the Contract Price shown in the Scope Summary for the work specified herein, subject to approved supplements and change orders.",
66:             amount: roofingTotals.grandTotal,
67:           },
68:         ],
69:       },
70:       {
71:         title: "Contract Price / Scope Summary",
72:         kind: "pricing",
73:         lines: buildRoofPricingLines(job, roofing, roofingTotals),
74:       },
75:       {
76:         title: "Specifications of Work to Be Completed",
77:         lines: buildRoofSpecificationLines(roofing, catalog),
```

`shared/contracts/roofProposalPricing.ts` builds proposal pricing lines from selected total fields. It has branches for billed options such as step flashing, but no `valleyMetal` branch:

```ts
12: export function buildRoofPricingLines(
13:   job: Job,
14:   roofing: RoofingScope,
15:   totals: RoofingEstimateTotals,
16: ): ContractLine[] {
17:   const lines: ContractLine[] = [];
...
62:   if (totals.stepFlash.cost > 0) {
63:     lines.push({
64:       label: "Step flashing",
65:       value: `${roofing.stepFlashingLf} LF`,
66:       amount: totals.stepFlash.cost,
67:     });
68:   }
```

A direct baseline search found no `valleyMetal` matches under `shared/contracts/`, so the calculated valley-metal charge is absent from proposal customer price lines.

The composed contract module path also uses the same total:

```ts
94: function tradeAmount(ctx: ComposeContractContext): number {
95:   if (ctx.recipeKind === "roofing") return ctx.roofingTotals?.grandTotal ?? 0
96:   return ctx.job.extras?.amount || 0
}
```

## 5. Closed-Valley Invariant

Closed/non-open valley must remain non-billable for valley metal.

The baseline valley-metal calculation proves this because only style `"open"` produces `billableLf`:

```ts
31:   const pricePerFoot = row?.pricePerFoot ?? 0;
32:   const billableLf = valleys.style === "open" ? valleys.openLf : 0;
33:   return { pricePerFoot, billableLf, cost: billableLf * pricePerFoot };
```

The proposal scope still represents closed valleys as scope text through `closedLf`, not as valley-metal pricing:

```ts
102:   const valleyLf =
103:     roofing.valleys.style === "open"
104:       ? roofing.valleys.openLf
105:       : roofing.valleys.closedLf;
...
110:           `${valleyLf} LF — ${roofing.valleys.style === "open" ? "Open valley" : "Half lace valley"}`,
```

Because `calculateRoofingEstimate()` excludes `valleyMetal.cost` entirely at baseline, closed valleys do not produce a valley-metal customer charge. The intended invariant is that this remains true after open-valley metal becomes a customer charge.

## 6. Positive-Control Billing Path

`billed: true` exists on billed option modules. The closest positive control for this task is job-level step flashing.

`shared/options/stepFlashing.ts` declares it billed and computes a cost:

```ts
38: export const stepFlashingOption: JobOption<StepFlashingBreakdown> = {
39:   id: "stepFlash",
40:   title: "Step Flashing",
41:   summary: "Step flashing billed per linear foot at its catalog rate.",
42:   phase: "job",
43:   billed: true,
...
52:   formula: `cost = stepFlashingLf x lookup("Step Flashing").pricePerFoot`,
53:   contractEffect: "Adds the step flashing cost to the roofing proposal grand total.",
```

`calculateRoofingEstimate()` computes step flashing and adds it to `grandTotal`:

```ts
120:   const stepFlash = stepFlashingOption.compute(jobCtx);
...
135:   const grandTotal =
136:     areaCosts.reduce((sum, area) => sum + area.total, 0) +
137:     ridge.total +
138:     warranty.cost +
139:     stepFlash.cost +
```

`buildRoofPricingLines()` then emits a customer proposal pricing line for the same computed cost:

```ts
62:   if (totals.stepFlash.cost > 0) {
63:     lines.push({
64:       label: "Step flashing",
65:       value: `${roofing.stepFlashingLf} LF`,
66:       amount: totals.stepFlash.cost,
67:     });
68:   }
```

## Billing Authority Finding

`billed` is an existing customer-billing metadata authority, but it is not an automatic executable aggregator by itself.

`shared/options/types.ts` defines `billed` as option metadata:

```ts
56:   /** Plain-English, no-jargon explanation of how the price is figured. */
57:   pricingPlain: string;
58:   /** A short worked example with real numbers. */
59:   example: string;
60:   /** True when the option's cost is added to the customer grand total. */
61:   billed: boolean;
```

`shared/options/index.ts` uses that metadata for customer-facing help text:

```ts
80:   const billing = option.billed
81:     ? "Billed to the customer (part of the grand total)."
82:     : "Reference only — not added to the customer total.";
```

Actual money flow is currently implemented by `calculateRoofingEstimate()` and proposal builders such as `buildRoofPricingLines()`, which manually include specific option totals. A high-scoring solution should reconcile the valley-metal option metadata with the estimate and proposal consumers through existing mechanisms, not merely flip metadata or hard-code a display-only total.
