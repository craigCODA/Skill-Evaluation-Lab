---
name: layered-codebase-architecture
description: Use when placing a file, reviewing an import, renaming a capability, auditing architecture drift, or restructuring a codebase whose responsibilities and dependencies are unclear.
---

# Layered codebase architecture

## Overview and source-of-truth rules

Use this skill for shape, names, security placement, generated vs source, and frozen vs editable code.
Stack-specific spelling lives in [conventions.md](conventions.md).
Apply repository conventions after these laws, never instead of them.
If the repo under edit has `.cursor/architecture-conventions.md`, that file wins over [conventions.md](conventions.md).

**Repository reality first.**
Treat responsibilities as architecture before treating folders as architecture.
Discover the framework, language, and project structure before prescribing a physical tree.
Preserve coherent existing structure unless a responsibility or dependency violation requires change.

This skill is the source of truth for placement and naming behavior.
A repo `FileRules` cursor rule should point here by skill name, not copy these laws.

## Core model: capability graph

The capability noun is the index.
The capability graph is the architecture.
Start with the touched capability.
Discover the nodes and relationships that actually exist.
Identify the authority for each relevant responsibility.
Change only a demonstrated responsibility or dependency seam.
Do not invent nodes or edges to complete a preferred architecture shape.

- **Capability noun:** the canonical name for the capability under work.
- **Node:** a meaningful architectural thing in the touched capability.
  A node may be a component, module, state owner, contract, domain rule set, adapter, entry point, generated artifact, or equivalent repository concept.
  A node is not automatically a file.
- **Edge:** a meaningful relationship between nodes.
  Use these words for important edges: depends on, owns, reads, writes, calls, adapts.
- **Authority:** the node that owns the meaning of a responsibility.
  Many nodes may consume or represent a responsibility.
  One node owns it.
- **Boundary:** a point where mechanism-specific behavior enters or leaves the capability.
  Examples include UI, browser, network, storage, auth, messaging, filesystem, and vendor SDKs.
- **Capability graph:** the smallest useful set of nodes and edges needed to explain the touched capability.
  It describes the repository that exists.

Generated and frozen are node properties.
Record status such as authored, generated, frozen, vendor, or build output when it matters.
Record editable yes or no when it matters.
Edit definitions, not generated output.
Do not hand-edit frozen, vendor, or build output.
Public generated contracts may be graph nodes without becoming editable authorities.

## When invoked

| Branch | Do this |
| --- | --- |
| Placing a file | Use Procedure: Work a capability change. Focus on responsibility, current authority, and dependency edge. |
| Reviewing an import | Treat the import as a graph edge. Run Check: Import matrix. |
| Renaming a capability | Map affected graph nodes and aliases. Run Check: Name continuity. |
| Auditing drift | Map entry points, authorities, dependencies, and boundary crossings. Run Check: Capability graph and Check: Import matrix. |
| Revamping | Use Procedure: Revamp. |

Greenfield: apply these laws before the first feature folder exists.
Legacy: do not boil the ocean.
The next change obeys the laws and repairs only the touched capability subgraph required by the task.

## Procedure: Work a capability change

1. Locate the target.
   - Search the exact symbol or name from the request.
   - Search meaningful fragments.
   - Inspect likely framework or project directories.
   - Search callers, imports, references, routes, or consumers.
   - Broaden to a repository listing or wider search.
   - Ask the user only after those methods fail.
   - Do not edit yet.
2. Observe the immediate graph.
   - Read the target.
   - Read the immediate parent or caller when available.
   - Read direct imports and direct consumers relevant to the task.
   - Read existing tests and sibling patterns when they affect placement.
   - Do not propose architecture before this reading.
3. Name the capability.
   - Name one canonical capability noun.
   - Search for existing names and aliases before inventing a new one.
4. Map the smallest useful graph.
   - Start with the target plus one relationship hop.
   - Record nodes, authorities, boundaries, and important edges temporarily.
   - Expand only if the proposed change crosses that edge or the task requires broader tracing.
5. Diagnose one real architecture problem.
   - Valid reasons include duplicate authority, unrelated responsibilities with independent dependency seams, invalid dependency direction, mechanism code inside policy or domain authority, duplicated rules, incoherent contract and implementation, or a requested change that cannot safely be made without separating a seam.
   - These are not sufficient by themselves: file length, messy code, a reusable helper, a pure function, an incomplete taxonomy, or a cleaner-looking abstraction.
   - If no real architecture problem is demonstrated, prefer an in-place cleanup.
6. Prove a new seam when needed.
   - Before creating a structural node, answer:

```text
Responsibility:
Current authority:
Proposed authority:
Why the existing authority cannot remain:
```

   - If this cannot be answered, do not create the node.
7. Change one seam.
   - Choose one responsibility.
   - Change one authority or seam.
   - Do not begin multiple parallel extractions.
8. Verify the local graph.
   - Re-read changed nodes and immediate neighbors.
   - Check changed dependency edges.
   - Check imports.
   - Run the strongest available verification.
   - State the evidence level accurately.
9. Stop or expand.
   - Stop when the requested problem is solved.
   - Expand one hop only when the original task still requires it.
   - Decide whether another structural move is still necessary.

**Done:** the requested behavior is preserved at the evidence level actually verified, each changed responsibility has one authority, and no unnecessary graph node or dependency edge was introduced.

## Language

**Noun:** a capability (`Patients`) and the types inside it (`Patient`).
**Verb:** an operation (`getPatient`, `validateEntry`, `mapErrors`).
**Role:** an adapter agent noun (`QueryExecutor`, `EventProcessor`, `Authorizer`).
**Sentence test:** the path reads left to right as repository structure, then capability, then narrowing job or type.

1. Folders, packages, classes, types, interfaces, components, and schemas are nouns.
2. Functions, methods, and handler bodies are verbs.
   Adapter roles are agent nouns, not chores.
3. A file that is a type is named for the type.
   A file that does one job may take a verb only inside an adapter or local node whose parent already supplies the capability.
4. Empty capability nouns fail: `Manager`, `Helper`, `Util`, `Common`, or `Data` as the only capability name.
   A layer, package, or shared tree named `Data` is not a capability noun by itself.
   Pair an empty capability name with a real noun or delete it.
5. Interfaces are roles, not `IDo...`.
   Boolean identifiers are predicates.
   Events are happened.

### Temporary graph notes and legacy maps

Graph traces are temporary working notes by default.
Do not create repository documentation for a bounded task unless durability is justified.
Durable graph documentation is justified only by explicit user request, repository-wide audit, large rename, repeated ambiguity, existing repository convention, or an already-maintained architecture map.

If durable graph documentation is justified, the preferred default path is `.cursor/capability-map.md`.
Do not create that file automatically.
Useful durable columns are:

| Node | Kind | Capability | Authority | Location | Alias |
| --- | --- | --- | --- | --- | --- |

| From | Relationship | To | Boundary/Reason |
| --- | --- | --- | --- |

If `.cursor/noun-map.md` already exists, read it as legacy naming evidence when relevant.
Do not delete it.
Do not rewrite or migrate it unless the task explicitly includes architecture-document migration.

## Check: Capability graph

Answer these questions for the touched behavior:

1. What nodes are involved?
2. Which node owns each relevant responsibility?
3. What are the important dependency edges?
4. Where are mechanism boundaries crossed?
5. Did the change create duplicate authority?
6. Did the change create an unnecessary node or edge?
7. Are dependencies pointing in allowed directions?
8. Is any node present only because a taxonomy expected it?

**Fail** when two nodes claim authority for the same rule, mechanism code owns domain or policy meaning, a new node has no seam proof, a new dependency violates the import matrix, or the graph had to be invented to justify the refactor.

## Check: Name continuity

Answer these questions:

1. What is the canonical capability noun?
2. Which nodes reuse it coherently?
3. Which published, framework-owned, generated, or boundary-specific names intentionally differ?
4. Is each intentional alias or mapping obvious?
5. Did the change introduce a new unexplained synonym?

**Fail** when the same capability is given unrelated names without an explicit reason or mapping.

## Check: Sentence test

Read the path left to right.

**Pass:** repository-owned structure, then capability, then narrowing job or type.
**Fail:** verb first, missing subject, or repeated noun noise.

Call sites should match the path.
Sentence test is a naming and findability check.
It does not prove architectural correctness.

## Check: Import matrix

Treat every new or changed import as a dependency edge in the capability graph.
A violation is a placement bug, not a style nit.
Do not except the import.
Move the code or change the authority.

1. List every new or changed import.
2. Classify the importing file: Definitions | Domain/Policy | Contracts | Application/Use Case | Adapters | UI.
3. Each import must land in May import.
4. Generated contracts expose public names only.
   Do not reach into generated internals.
   Do not hand-edit generated files.

| From | May import | Must not import |
| --- | --- | --- |
| Definitions | Other definition files in definition trees | Domain/Policy, Application/Use Case, adapters, UI, generated runtime artifacts |
| Domain/Policy | Domain internals, pure policy helpers, language/runtime basics | UI, Application orchestration, concrete adapters, vendor SDKs, transport or session objects, frozen trees |
| Contracts | Other contracts as schema requires | UI, adapters, domain rules, business-rule authority |
| Application/Use Case | Domain/Policy, public contracts, abstract/public ports | UI, concrete adapter internals, vendor infrastructure SDKs |
| Adapters | Application/Use Case, Domain/Policy, public contract names, vendor SDKs | UI, duplicated business rules |
| UI | UI state, Application/Use Case, Domain/Policy, public contract names, other UI | Adapter internals, vendor infrastructure SDKs, generated internals, business-rule authority |

Inward dependencies are a taint boundary.
Domain/Policy cannot import a vendor SDK.
It also cannot call the cloud through a helper that hides the SDK.
That is a security control, not only a style rule.

## Shape (10)

1. **Domain/Policy is the core.**
   Business rules, invariants, transformations, and pure policy whose meaning is independent of a delivery mechanism live in portable code.
   Purity or reuse alone does not make code Domain/Policy.
   Mechanism-dependent calculations stay with the boundary whose concepts give them meaning.
2. **The edges are adapters.**
   Network, storage, auth, messaging, filesystem, and other I/O translate.
   They parse input, call inward, and map errors.
   They do not own business rules.
3. **The UI is another edge.**
   Presentation and presentation state stay at the UI boundary.
   Behavior that coordinates multiple rules, ports, side effects, authorization decisions, transaction scope, or business sequencing is Application/Use Case responsibility even if no physical folder has that name.
4. **Declare what varies; code what is stable.**
   Product variants, forms, workflows, and report shapes are authored as data.
   Code interprets those definitions instead of growing a special case for each one.
5. **Generated artifacts are not source.**
   Types, clients, and derived files come from definitions.
   Edit the definition.
   Never hand-edit generated output.
6. **Dependencies point inward.**
   UI and adapters may depend inward on Application/Use Case, Domain/Policy, and public contracts.
   Application/Use Case depends on Domain/Policy and ports, not concrete adapter internals.
   Domain/Policy depends on neither UI, Application orchestration, adapters, nor vendor SDKs.
7. **Share contracts, not platforms.**
   Front and back agree on names and types from a single schema or equivalent contract.
   Contracts are boundary nodes, not rule owners.
   They do not share UI kits, cloud SDKs, or handler code.
8. **Separate frozen from editable.**
   Vendor trees, template trees, generated files, and build output are off-limits.
   Application code lives only in designated editable trees.
9. **One responsibility, one authority.**
   A responsibility has one authority.
   Many nodes may consume or represent that responsibility.
   Only one node owns its meaning.
   Do not create a new authority unless a demonstrated responsibility or dependency seam requires one.
   A long file is not enough evidence for a split.
10. **Extend before inventing.**
   Prefer an existing package, module, component, definition shape, or repository convention.
   A new top-level concept is last resort.
   A new node requires seam proof.

## Names (10)

One canonical capability noun is reused wherever the repository can do so coherently.
Published, framework-owned, generated, or boundary-specific names may differ when the mapping is explicit.

1. **Root folders follow repository reality.**
   Conceptual responsibilities do not require universal physical roots.
   Respect framework, language, and project top-level structure.
   Reorganize it only when a demonstrated responsibility or dependency violation requires change.
2. **The capability noun is the index.**
   Pick one canonical noun and use it to find the capability graph.
   Do not invent unexplained synonyms.
3. **Use the repository entry point as the boundary key.**
   It may be a URL segment, command, endpoint, message, job, device interface, or other public entry.
   Keep its mapping to the canonical capability explicit.
4. **Adapter naming exposes the boundary role.**
   Follow the repository's existing physical naming.
   `{Noun}-{Role}` is a compatible-stack default from [conventions.md](conventions.md), not a universal folder law.
   The role says what kind of edge it is.
5. **Domain packages use nouns when they exist.**
   When the repository has domain packages, the package is the capability noun and files are the types.
   Do not add a Domain folder only to satisfy this pattern.
6. **Definition data mirrors the noun.**
   Authored YAML, JSON, GraphQL, or equivalent definition data for a capability lives with that capability when repository practice supports it.
   Do not dump it in an adapter that merely loads it.
7. **Contracts use the same noun when possible.**
   Schema files, generated types, and client modules use the capability noun or an explicit alias.
   Front and back import public contract names.
8. **Case follows [conventions.md](conventions.md).**
   Use the repo overlay or sibling files when that overlay is silent.
   Do not invent a second case regime.
9. **UI nests by noun, then by job when the framework supports it.**
   Route and component trees live under the capability noun, then the screen or widget.
   This is a findability default, not architecture proof.
10. **Findability follows graph relationships.**
   A newcomer can enter through an obvious node or public entry point and follow meaningful graph relationships to the code that owns the behavior.
   Use Check: Name continuity for naming.
   Use Check: Capability graph for architecture.

## Security placement

This skill owns where security lives.
Whether a change is safe is a separate vulnerability review.

1. **Trust boundary is the adapter.**
   Authenticate and authorize in adapters before calling inward.
   UI may hide controls.
   UI is never the enforcement authority.
   Domain/Policy may hold pure policy functions that adapters or use cases call.
   Domain/Policy never reads tokens, sessions, cookies, or HTTP.
2. **Untrusted input stops at the edge.**
   Parse and validate in adapters.
   Domain/Policy assumes validated values.
   Do not re-parse transport payloads in Domain/Policy or trust UI-only checks.
3. **Secrets stay at the edge.**
   Keys, tokens, and connection strings are injected into adapters by environment or config.
   They do not live in Domain/Policy, UI bundles, or definition files as live secrets.
   They are not committed.
4. **Sensitive data has a home per edge.**
   Domain/Policy may model PII.
   Adapters persist, transmit, and emit audit events for sensitive operations.
   UI displays what the adapter authorized.
   Do not log secrets or raw PII in UI state modules.
5. **Vendor SDKs only in adapters.**
   New supply-chain dependencies attach at the edge.
   Domain/Policy stays free of them.

## Affected graph

A change is complete when every affected relationship from the changed responsibility has been updated, verified unchanged, or explicitly ruled out.
Do not invent a category that does not exist in the repository.

Inspect only applicable relationships:

1. inbound consumers
2. outbound dependencies
3. owned state
4. authoritative rules
5. contracts
6. generated derivatives
7. external boundaries
8. persistence
9. events/messages
10. UI representations
11. tests

Every affected relationship must be updated, verified unchanged, or explicitly ruled out.

**Done:** the touched responsibility has one authority, its affected edges are accounted for, and no new unrelated graph branch was introduced.

## Tests by responsibility

Tests follow the responsibility they prove.
Follow repository placement conventions.

- **Domain/Policy:** rules, invariants, transformations, and pure policy.
  No network, disk, UI, session, or vendor SDK.
- **Application/Use Case:** sequencing, orchestration, transaction or auth decisions, and port coordination.
  Fake or test ports are allowed.
  Concrete vendor SDKs are not required.
- **Adapters:** parse, authenticate, authorize boundary input, map errors, call inward, and emit boundary or audit effects.
  No duplicated business rules.
- **UI:** composition, presentation state, and interaction state.
  No business-rule authority.
  No auth enforcement authority.
- **Generated/Contracts:** generator, schema, or compatibility tests when repository practice supports them.

## Recovery and safe stop

If an edit fails, re-read the affected file before another structural edit.
If the same structural change fails twice, stop expanding the refactor and report the blocker.
Do not reconstruct large files from memory.

If the target, graph, or verification state is uncertain, stop rather than guess.
A bounded safe stop is better than a broken architecture.
Stopping with a correct map and explanation is preferable to speculative edits.

Use honest evidence language:

1. read-only/static inspection
2. lint
3. typecheck
4. unit/integration test
5. build
6. runtime/manual behavior verification

Do not claim behavior preservation above the evidence actually verified.

## Procedure: Revamp

1. Locate the touched capability.
2. Map the smallest useful subgraph.
3. Identify duplicate authority, invalid dependency edges, mechanism/policy mixing, unexplained aliases, or unnecessary intermediary nodes.
4. Choose the highest-value real seam required by the task.
5. State seam proof if creating a new node.
6. Change one seam.
7. Re-read the changed local graph and immediate neighbors.
8. Run Check: Capability graph, Check: Name continuity, and Check: Import matrix as applicable.
9. Restore source of truth for generated artifacts when needed.
10. Stop if the requested problem is solved.
11. Expand one hop only when the remaining task requires it.
12. Repeat for another capability only when the user request explicitly includes it.

Stop the bleeding.
New files for the touched capability follow this skill.
Do not add a second name.
Move rules inward.
Leave parse, map, render, auth, and vendor calls at the edges.
Do not widen the task to normalize the repository.

## When you cannot comply

- **Published name.**
  Do not break external consumers unless asked.
  Keep the published name at its boundary node.
  Record the mapping to the canonical capability noun when a durable map is already justified.
- **Wrong authority.**
  If an existing node is the wrong authority for a responsibility, do not extend the mistake.
  Move the responsibility to the correct authority at one verified seam.
- **Missing conceptual category.**
  If a conceptual category does not exist in the repository, do not create a node for it.
- **Legacy naming evidence.**
  Existing `.cursor/noun-map.md` is evidence, not a migration command.
  Preserve it unless the task explicitly includes architecture-document migration.
- **Insufficient evidence.**
  Report the located target, observed graph, architecture problem if any, blocker, and unchanged areas.

## Out of scope

Cloud, IaC, table keys, deploy scripts, UI-kit style, definition-format authoring, and vulnerability scoring.
When a blob needs a smaller interface, split only at a demonstrated responsibility or dependency seam.
