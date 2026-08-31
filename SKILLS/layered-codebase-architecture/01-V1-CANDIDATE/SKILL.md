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

**Repository reality first.** Treat layers as responsibilities before treating them as folders. Discover the repository's framework-, language-, and project-owned structure before prescribing a physical tree; preserve coherent existing structure unless a responsibility or dependency violation requires change.

**Noun chain** (the findability test, stated once): a newcomer walks route → UI → contract → adapter → domain → definitions on **one name**. If a hop needs a translation dictionary, rename or record an alias (see When you cannot comply). Every other “walk the chain” line in this skill means this test.

Use an existing `.cursor/noun-map.md` as the durable noun/alias record. For a bounded task, do not create or expand a repository-wide noun map unless the user, repo rules, or a recurring ambiguity requires one; otherwise keep the touched capability trace temporary.

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
3. If a durable noun map is already in scope, put the file on that row; otherwise keep the noun trace temporary (Language).
4. Name the file as a **thing** (noun) or an **action** (verb) (Language).
5. Check: Sentence test on the full path.
6. Check: Import matrix on the new file’s imports.
7. Update, verify, or mark N/A every **touched and applicable** hop on the noun chain (Feature hops).
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

When a durable noun map already exists or is explicitly required, use it before renaming a capability, auditing drift, or revamping. Collapse synonyms into one noun per row. Otherwise use the same mapping temporarily for the touched capability and do not create repository-wide documentation solely for the task.

| Noun | Route | UI | Contract | Adapter | Domain | Definitions | Alias (if any) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Patients | `/patients` | UI tree named `Patients` | `Patients` schema/types | `{Patients}-{Role}` | `Patients` / `Patient` | tree named `Patients` | |
| Reporting | `/reporting` | UI tree named `Reporting` | `Reporting` | `{Reporting}-{Role}` | `Reporting` / `Report` | tree named `Reporting` | |
| _…_ | | | | | | | |

**Done (map):** every live route has a row in `.cursor/noun-map.md`; each cell is the map noun, N/A, or an alias.

---

## Check: Noun-chain walk

Start at the relevant entry point (or the file under edit). Walk the noun chain against the durable noun map when one is in scope; otherwise use a temporary trace. Each relevant hop uses the canonical noun, an explicit alias/mapping, or N/A.

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

1. **Domain is the core.** Business rules, invariants, and transformations whose meaning is independent of a delivery mechanism live in portable code. Purity or reuse alone does not make code domain logic: mechanism-dependent calculations remain with the boundary whose concepts give them meaning.
2. **The edges are adapters.** Network, storage, auth, messaging, and other I/O only translate. They parse input, call domain, and map errors. They do not own the rules.
3. **The UI is another edge.** Presentation and presentation state stay at the UI boundary. When behavior coordinates multiple rules, ports, side effects, authorization/transaction scope, or business sequencing, treat that as an application/use-case responsibility even if the repository has no `Application/` folder.
4. **Declare what varies; code what is stable.** Product variants, forms, workflows, and report shapes are authored as data. Code interprets those definitions instead of growing a special case for each one.
5. **Generated artifacts are not source.** Types, clients, and derived files come from definitions. You edit the definition. You never hand-edit the generated output.
6. **Dependencies point inward.** UI and adapters may depend on domain and generated contracts. Domain depends on neither UI, adapters, nor vendor SDKs.
7. **Share contracts, not platforms.** Front and back agree on names and types from a single schema (or equivalent contract). They do not share UI kits, cloud SDKs, or handler code.
8. **Separate frozen from editable.** Vendor/template trees, generated files, and build output are off-limits. Application code lives only in designated trees.
9. **One responsibility, one authority.** A rule or responsibility has one authoritative owner, but representations and supporting operations may exist at multiple boundaries. Do not create files, folders, or layers merely to satisfy the taxonomy; split only at a real responsibility or dependency seam.
10. **Extend before inventing.** Prefer an existing package, module, or definition shape. A new top-level concept is last resort, not the default.

---

## Names (10)

One capability name, reused everywhere. If the user is on `/patients`, you find `Patients` on the page, the UI tree, the contract, the adapter, and the domain package.

1. **Root folders follow repository reality.** Conceptual responsibilities do not require universal physical roots. Respect framework-, language-, and project-owned top-level structure; reorganize it only when a demonstrated responsibility or dependency violation requires change.
2. **The capability name is the index.** Pick one canonical noun (`Patients`, `Reporting`, `Auditing`) and reuse it where the repository can do so coherently. Published, framework-owned, or boundary-specific names may differ when the mapping is explicit; do not invent unexplained synonyms.
3. **Use the repository's entry point as the boundary key.** In a routed UI this may be the URL segment; in another system it may be a command, endpoint, message, job, device interface, or other public entry. Keep its mapping to the canonical capability explicit.
4. **Adapter naming exposes the boundary role.** Follow the repository's existing physical naming. `{Noun}-{Role}` is a compatible-stack default from [conventions.md](conventions.md), not a universal folder law; the role still says *what kind of edge*, not a new domain.
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

A user-visible change is not done until every **touched and applicable** hop for that capability is updated, verified unchanged, or marked N/A. Do not invent missing layers just to complete this list:

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

**Done:** the touched capability has a coherent responsibility path and the requested behavior is preserved at the evidence level actually verified. Do not treat bounded work as permission to normalize unrelated capabilities.

1. Inspect the touched capability and its immediate dependencies. Use an existing noun map when one is already in scope; otherwise keep the trace temporary unless a durable map is explicitly justified.
2. For one noun, Check: Noun-chain walk. Note missing hops and extra names.
3. Stop the bleeding: new files for that noun follow this skill. Do not add a second name.
4. Move rules inward. Leave parse/map/render/authz at the edges.
5. Thin adapters: parse, authorize, call domain, map errors, audit.
6. Restore source of truth: hand-edited generated files go back to the definition; regenerate.
7. Fix the noun chain (aliases if you cannot rename — below).
8. Repeat for another noun only when the task scope actually includes it. Do not widen the task just to normalize the repository or start a parallel architecture.

---

## When you cannot comply

- **Published name vs noun chain.** Do not break external consumers in the same change unless asked. Keep an **Alias** on `.cursor/noun-map.md` at the published edge; map to the noun internally. The noun-chain walk may pass through that alias only if it is recorded there.
- **Extend vs one home.** If the existing module is the **wrong layer**, one home wins: extract into the correct layer rather than extend the misplaced file.
- **Hops that do not apply.** Mark N/A on the map. Do not invent a hop.

---

## Out of scope

Cloud, IaC, table keys, deploy scripts, UI-kit style, definition-format authoring, and vulnerability scoring. When a blob needs a smaller interface, split it at a seam; do not invent a new layer to avoid the split.
