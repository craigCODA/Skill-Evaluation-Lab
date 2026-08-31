---
name: layered-codebase-architecture
description: >-
  Places and reviews code on the noun chain: one capability name through UI,
  contract, adapter, and domain, with import law and security placement. Use
  when placing a file, reviewing an import, renaming a capability, auditing
  architecture drift, or revamping a messy repo.
---

# Layered codebase architecture

Laws for **shape**, **names**, and **security placement**. Procedures for placing files and revamping a messy tree. Stack-specific case and folder spelling live in [conventions.md](conventions.md) — apply them after the laws, never instead of them. If the repo under edit has `.cursor/architecture-conventions.md`, that file wins over [conventions.md](conventions.md).

**Noun chain** (the findability test, stated once): a newcomer walks route → UI → contract → adapter → domain → definitions on **one name**. If a hop needs a translation dictionary, rename or record an alias (see When you cannot comply). Every other “walk the chain” line in this skill means this test.

The filled noun map is the committed file `.cursor/noun-map.md` in the repo under edit (create it from the template below if missing).

This skill is the source of truth for placement, naming, generated vs source, and frozen vs editable. A repo `FileRules` cursor rule should point here by skill name, not copy these laws.

---

## When invoked

| Branch | Do this |
| --- | --- |
| Placing a file | Procedure: Place a file |
| Reviewing an import | Check: Import matrix |
| Renaming a capability | Fill the noun map, then Check: Noun-chain walk |
| Auditing drift | Noun map for live routes, then both named checks |
| Revamping | Procedure: Revamp |

Greenfield: apply the laws before the first feature folder exists. Legacy: do not boil the ocean. The next change obeys the laws and moves the **touched** capability onto the noun chain.

---

## Procedure: Place a file

1. Name the layer (Shape #9). If you cannot, stop.
2. Name the capability noun (Names #2). Search the repo for that noun first (Shape #10).
3. Put the file on that row of `.cursor/noun-map.md` (Language).
4. Name the file as a **thing** (noun) or an **action** (verb) (Language).
5. Check: Sentence test on the full path.
6. Check: Import matrix on the new file’s imports.
7. Update or mark N/A every hop on the noun chain (Feature hops).
8. Add tests at the same layer.
9. Apply [conventions.md](conventions.md) (or the repo overlay if present).

**Done:** Check: Noun-chain walk passes for that noun, or the skip is explicit.

---

## Language

**Noun** — a capability (`Patients`) and the types inside it (`Patient`).  
**Verb** — an operation (`getPatient`, `validateEntry`, `mapErrors`).  
**Role** — adapter agent noun (`QueryExecutor`, `EventProcessor`, `Authorizer`).  
**Noun map** — `.cursor/noun-map.md`; one row per capability; every hop uses that row’s name (or N/A, or a recorded alias).  
**Sentence test** — the path, read left to right, is a speakable sentence: layer, then noun, then a narrowing job or type.

1. Folders, packages, classes, types, interfaces, components, and schemas are **nouns**.
2. Functions, methods, and handler bodies are **verbs**. Adapter *roles* are agent nouns (`{Noun}-{Role}`), not chores.
3. A file that *is* a type is named for the type (`Patient.ts`). A file that *does* one job may take the verb (`transformation.ts`) only inside an adapter whose folder already supplied the noun.
4. Empty **capability** nouns fail: `Manager`, `Helper`, `Util`, `Common`, `Data` as the only name of a *capability* (a layer or shared package named `Data/`, `data`, or `@org/data` is not a capability noun — do not flag it on that rule). Pair an empty capability name with a real noun or delete it. Do not name a type as a verb (`ProcessPatient` is a function; `PatientProcessor` is a role).
5. Interfaces are roles (`PatientRepository`), not `IDo…`. Boolean identifiers are predicates (`isReady`, `hasError`). Events are happened (`PatientCreated`).

### Noun map template

The durable record is `.cursor/noun-map.md` in the repo under edit. Fill it before renaming a capability, auditing drift, or revamping. Collapse synonyms into one noun per row. Persist aliases there so they survive across sessions.

| Noun | Route | UI | Contract | Adapter | Domain | Definitions | Alias (if any) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Patients | `/patients` | UI tree named `Patients` | `Patients` schema/types | `{Patients}-{Role}` | `Patients` / `Patient` | tree named `Patients` | |
| Reporting | `/reporting` | UI tree named `Reporting` | `Reporting` | `{Reporting}-{Role}` | `Reporting` / `Report` | tree named `Reporting` | |
| _…_ | | | | | | | |

**Done (map):** every live route has a row in `.cursor/noun-map.md`; each cell is the map noun, N/A, or an alias.

---

## Check: Noun-chain walk

Start at the user-visible route (or the file under edit). Walk the noun chain against `.cursor/noun-map.md`. Each hop uses the map noun or is marked N/A.

**Fail** if any hop uses a synonym (`analytics` vs `reporting`) not listed as Alias on that file.

---

## Check: Sentence test

Read the path left to right.

**Pass:** layer, then noun, then narrowing job/type (`Frontend/pages/patients/details` → “frontend pages for patient details”).  
**Fail:** verb first (`process/patients`), missing subject, or the noun repeated as noise.

Call sites should match the path (`loadDetails` lives with patient details, not in a `misc` folder).

---

## Check: Import matrix

A violation is a placement bug, not a style nit. Do not except the import; move the code.

1. List every **new or changed import** in the diff.
2. Classify the importing file: Definitions | Domain | Contracts | Adapters | UI.
3. Each import must land in **May import**.
4. Generated contracts: import **public** names from the generated package. Do not reach into generated internals. Do not hand-edit generated files.

| From | May import | Must not import |
| --- | --- | --- |
| Definitions | Other definition files in definition trees | Domain, adapters, UI, generated artifacts |
| Domain | Domain internals, language stdlib | UI, adapters, vendor SDKs, frozen trees, definitions-as-runtime-I/O |
| Contracts (authored + generated) | Other contracts as the schema requires | UI, adapters, domain rules |
| Adapters | Domain, public contract names, vendor SDKs | UI |
| UI | Domain, public contract names, other UI, UI state modules | Adapter internals, vendor cloud SDKs, generated internals |

Inward dependencies are also a **taint boundary**: domain cannot import a vendor SDK, so it cannot call the cloud or leak through one. That is a security control, not only a style rule.

---

## Shape (10)

1. **Domain is the core.** Business rules, invariants, and transformations live in portable code. That code does not know about HTTP, UI, or a vendor SDK.
2. **The edges are adapters.** Network, storage, auth, messaging, and other I/O only translate. They parse input, call domain, and map errors. They do not own the rules.
3. **The UI is another edge.** Screens compose existing primitives. Presentation stays in views; application behavior lives in UI state modules that call domain or adapters.
4. **Declare what varies; code what is stable.** Product variants, forms, workflows, and report shapes are authored as data. Code interprets those definitions instead of growing a special case for each one.
5. **Generated artifacts are not source.** Types, clients, and derived files come from definitions. You edit the definition. You never hand-edit the generated output.
6. **Dependencies point inward.** UI and adapters may depend on domain and generated contracts. Domain depends on neither UI, adapters, nor vendor SDKs.
7. **Share contracts, not platforms.** Front and back agree on names and types from a single schema (or equivalent contract). They do not share UI kits, cloud SDKs, or handler code.
8. **Separate frozen from editable.** Vendor/template trees, generated files, and build output are off-limits. Application code lives only in designated trees.
9. **One concern, one home.** A new thing belongs in exactly one layer: a rule in domain, a definition in data, I/O in an adapter, a screen in UI. If you cannot name the layer, do not add the file.
10. **Extend before inventing.** Prefer an existing package, module, or definition shape. A new top-level concept is last resort, not the default.

---

## Names (10)

One capability name, reused everywhere. If the user is on `/patients`, you find `Patients` on the page, the UI tree, the contract, the adapter, and the domain package.

1. **Root folders are layers, not features.** Top level is UI, adapters, domain, contracts/clients, and definition data. A feature never gets its own root folder; it appears as the **same name** under each layer that needs it.
2. **The capability name is the index.** Pick one noun (`Patients`, `Reporting`, `Auditing`). That noun is the folder, the schema, the adapter prefix, the domain package, and the UI route segment. Do not invent a second word for the same thing.
3. **The URL is the frontend key.** The route segment is the noun. UI for that screen lives under the same noun. UI state modules are named from that noun ([conventions.md](conventions.md) for spelling).
4. **The adapter folder is `{Noun}-{Role}`.** Examples: `API-Patients`, `Reporting-QueryExecutor`, `Auditing-EventProcessor`. Role prefixes say *what kind of edge*, not a new domain. Entry-file spelling is in [conventions.md](conventions.md).
5. **Domain packages are the noun; files are the type.** `Patients/Patient`, `Reporting/ReportDefinition`. Subfolders are kinds of work (`Definitions/`, `Factories/`, `Tables/`), not a second naming scheme. Tests sit next to the module they prove.
6. **Definition data mirrors the noun.** Authored YAML/JSON/GraphQL for a capability lives in a tree named for that capability, not dumped in the adapter that loads it.
7. **Contracts use the same noun.** Schema files, generated types, and client modules are named for the capability. Front and back import that public name; they do not each invent a DTO alias.
8. **Case follows [conventions.md](conventions.md)** (or the repo overlay / siblings if that overlay is silent). Do not invent a second case regime.
9. **UI nests by noun, then by job.** Route and component trees under the noun, then the screen or widget (`details`, `List`, `Form`). Do not scatter one capability across unrelated UI folders. Frozen trees stay off the map.
10. **Findability is Check: Noun-chain walk.** On a messy repo, fixing the walk is the first refactor.

---

## Security placement

This skill owns **where** security lives. Whether a change is *safe* is a separate vulnerability review — run one; this skill is not that review.

1. **Trust boundary is the adapter.** Authenticate and authorize in adapters before calling domain. UI may hide controls; it is never the enforcement point. Domain may hold **pure policy functions** that adapters call (`canEdit(patient, actor)`). Domain never reads tokens, sessions, cookies, or HTTP.
2. **Untrusted input stops at the edge.** Parse and validate in adapters. Domain assumes validated values. Do not re-parse transport payloads in domain or trust UI-only checks.
3. **Secrets stay at the edge.** Keys, tokens, and connection strings are injected into adapters (environment/config). They do not live in domain, UI bundles, or definition files as live secrets, and they are not committed.
4. **Sensitive data has a home per hop.** Domain may *model* PII. Adapters persist, transmit, and emit **audit events** for sensitive operations. UI displays what the adapter authorized. Do not log secrets or raw PII in UI state modules.
5. **Vendor SDKs only in adapters.** New supply-chain dependencies attach at the edge (taint boundary). Domain stays free of them.

---

## Feature hops

A user-visible change is not done until every hop for that noun is updated or marked N/A:

1. Definition data (if the shape varies)
2. Contract / schema
3. Generated artifacts (regenerate; do not hand-edit)
4. Domain
5. Adapter (`{Noun}-{Role}`)
6. UI route, views, UI state modules

**Done:** each hop exists under the same noun, or the skip is explicit.

---

## Tests by layer

- **Domain:** rules, transformations, pure policy. No network, disk, or UI.
- **Adapters:** parse, authenticate, authorize, map errors, call domain, emit audit events. No duplicated rules.
- **UI:** composition and screen state. No business rules and no authz enforcement.

Tests live next to the code they prove.

---

## Procedure: Revamp

**Done:** every live capability has one name and one home per layer, or is marked N/A (`.cursor/noun-map.md` complete; Check: Noun-chain walk passes per row).

1. Fill `.cursor/noun-map.md` from live routes and folders. Collapse synonyms.
2. For one noun, Check: Noun-chain walk. Note missing hops and extra names.
3. Stop the bleeding: new files for that noun follow this skill. Do not add a second name.
4. Move rules inward. Leave parse/map/render/authz at the edges.
5. Thin adapters: parse, authorize, call domain, map errors, audit.
6. Restore source of truth: hand-edited generated files go back to the definition; regenerate.
7. Fix the noun chain (aliases if you cannot rename — below).
8. Repeat for the next noun. Do not start a parallel architecture.

---

## When you cannot comply

- **Published name vs noun chain.** Do not break external consumers in the same change unless asked. Keep an **Alias** on `.cursor/noun-map.md` at the published edge; map to the noun internally. The noun-chain walk may pass through that alias only if it is recorded there.
- **Extend vs one home.** If the existing module is the **wrong layer**, one home wins: extract into the correct layer rather than extend the misplaced file.
- **Hops that do not apply.** Mark N/A on the map. Do not invent a hop.

---

## Out of scope

Cloud, IaC, table keys, deploy scripts, UI-kit style, definition-format authoring, and vulnerability scoring. When a blob needs a smaller interface, split it at a seam; do not invent a new layer to avoid the split.
