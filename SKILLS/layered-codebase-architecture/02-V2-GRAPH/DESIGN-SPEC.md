# Layered Codebase Architecture V2 Graph Design Spec

Status: DESIGN ONLY. DO NOT IMPLEMENT YET.
Date: 2026-08-30
Source candidate: frozen V1 candidate
Source SKILL.md SHA-256: 4a2082288c161b6a43cc6c0d0e7bb05961c1f8fc7edcd1647e4ebf8f0322432a
Source conventions.md SHA-256: dd84c0acff48472b52b9f29d01db5b7ff6157c70e0e7dca872b3a42c5353cc3d

## 1. Purpose

V2 changes the skill's architectural model from a fixed noun chain to a discovered capability graph.

The noun is not removed. The noun becomes the index used to find and name the capability. The graph describes how that capability actually exists in the repository.

The design must preserve the improvements already supported by V1 evidence:

- Repository reality comes before a prescribed folder tree.
- A permanent repository-wide noun map is not created for every bounded task.
- Purity or reuse alone does not make code Domain.
- Mechanism-dependent behavior stays with the boundary whose concepts give it meaning.
- One responsibility has one authority.
- Existing structures are extended before new structures are invented.
- Published or framework-owned names may differ when the mapping is explicit.
- Physical TypeScript/Vue/Nuxt conventions are conditional defaults, not universal laws.

V2 adds a second goal: safe and useful behavior when the model cannot reliably perform a large architectural refactor.

The desired failure mode is not a half-built architecture. The desired failure mode is a bounded stop with an accurate explanation of what was found and what could not be completed safely.

## 2. Design thesis

V2 is built around five ideas.

1. Capability noun
   - Answers: what part of the product or system is this work about?
   - Example: Roof Measurement, Patients, Reporting.

2. Node
   - A meaningful architectural thing in the touched capability.
   - Examples: component, module, state owner, contract, domain rule set, adapter, entry point, generated artifact.
   - A node is not automatically a file.

3. Edge
   - A real relationship between nodes.
   - Canonical V2 edge vocabulary is intentionally small:
     - depends on
     - owns
     - reads
     - writes
     - calls
     - adapts
   - More specific prose is allowed, but these six terms are enough for the skill's reasoning model.

4. Authority
   - The node that owns the meaning of a responsibility.
   - A responsibility can have many consumers and representations.
   - Only one node owns its meaning.

5. Boundary
   - A point where mechanism-specific concerns enter or leave the capability.
   - Examples: UI, browser, network, database, filesystem, auth, messaging, vendor SDK.

The central sentence for V2 is:

"The capability noun is the index. The capability graph is the architecture. Authority tells where a responsibility belongs. Edges tell what depends on what."

## 3. V2 behavioral contract

A model using V2 should do the following in order.

1. Locate the target.
2. Read the target and its immediate relationships.
3. Name the capability noun.
4. Map the smallest useful graph.
5. Identify the authority for each responsibility relevant to the task.
6. Diagnose one actual architecture problem.
7. Make one justified structural change.
8. Verify that change at the strongest evidence level available.
9. Expand one graph hop only if the original task still requires it.
10. Stop instead of guessing when the graph, file state, or verification state is uncertain.

V2 must not reward architecture for its own sake.

A long file is not automatically an architecture violation.
A pure helper is not automatically Domain.
A reusable helper is not automatically shared code.
A missing conceptual layer is not automatically a reason to create a folder.
A model that cannot justify a new authority must not create one.

## 4. Weak-model survivability requirements

V2 must degrade safely.

This section exists because the evaluation exposed two different failure classes:

- Inconsistent execution that can begin a valid refactor but lose state and leave broken partial architecture.
- Stable low-capability execution that may not be able to perform the architecture task at all.

V2 cannot make a weak model strong. It can reduce the damage caused by weak execution.

### 4.1 Locate ladder

Before asking the user for a file path, the model must attempt these steps in order:

1. Search the exact symbol or phrase from the request.
2. Search meaningful fragments of the phrase.
3. Inspect likely framework or project directories.
4. Search callers, imports, routes, references, or consumers.
5. Broaden to a repository listing or wider search.
6. Ask the user only after those methods fail.

The model must not infer architecture from filenames before it has read the target and at least one immediate relationship when available.

### 4.2 One seam at a time

V2 must prohibit multiple structural extractions from being in flight at once.

Required loop:

1. Choose one responsibility.
2. Move or clarify that one responsibility.
3. Re-read the changed node and its immediate neighbors.
4. Check the changed dependency edges.
5. Run the cheapest available verification that can detect breakage.
6. Decide whether another structural change is still required.

A second structural extraction cannot begin until the first one is integrated and checked.

### 4.3 Edit failure recovery

If a structural edit fails once:

- Re-read the affected file before trying again.

If the same structural edit fails twice:

- Stop expanding the refactor.
- Preserve the current state.
- Report the blocker.
- Do not reconstruct a large file from memory.

### 4.4 Safe stop

A valid V2 result can be a safe stop.

A safe stop is better than a broken multi-file refactor when the model cannot continue reliably.

A safe stop must state:

- What target was located.
- What immediate graph was observed.
- What architecture problem was identified, if any.
- What prevented a safe edit or verification.
- What was left unchanged.

### 4.5 Verification honesty

The skill must distinguish these evidence levels:

- Read-only/static inspection.
- Lint.
- Typecheck.
- Unit/integration test.
- Build.
- Runtime/manual behavior verification.

The model must not say "behavior preserved" when it only has lint, typecheck, or build evidence.

## 5. New section order for SKILL.md

V2 should use this order:

1. Frontmatter
2. Overview and source-of-truth rules
3. Core model: capability graph
4. When invoked
5. Procedure: Work a capability change
6. Language
7. Check: Capability graph
8. Check: Name continuity
9. Check: Sentence test
10. Check: Import matrix
11. Shape
12. Names
13. Security placement
14. Affected graph
15. Tests by responsibility
16. Recovery and safe stop
17. Procedure: Revamp
18. When you cannot comply
19. Out of scope

This order puts the execution model before detailed laws. It also separates architecture reasoning from naming reasoning.

## 6. Exact section mapping from V1 to V2

The following subsections define what stays, moves, changes, or disappears.

### 6.1 Frontmatter

V1 status: REWRITE.

Current V1 problem:

The description summarizes the skill's workflow with language such as "noun chain" and "one capability name through UI, contract, adapter, and domain." That gives the agent a shortcut and encodes the chain before the skill body is read.

V2 requirement:

The description must contain triggers only.

Proposed V2 description:

"Use when placing a file, reviewing an import, renaming a capability, auditing architecture drift, or restructuring a codebase whose responsibilities and dependencies are unclear."

Keep:

- name: layered-codebase-architecture

Remove from description:

- noun chain
- one capability name through UI, contract, adapter, and domain
- security-placement workflow summary

### 6.2 Opening overview

V1 status: KEEP MOST, ADD CORE GRAPH LAW.

Keep with minor wording cleanup:

- Shape, names, and security placement are still the major law groups.
- Stack-specific spelling stays in conventions.md.
- .cursor/architecture-conventions.md still overrides conventions.md.
- Repository reality first stays unchanged in meaning.

Remove:

- The fixed "Noun chain" paragraph.
- The statement that every later chain reference means route to UI to contract to adapter to domain to definitions.

Replace with a short "Core model" paragraph:

"The capability noun is the index. The capability graph is the architecture. Start with the touched capability, discover the nodes and relationships that actually exist, identify the authority for each relevant responsibility, and change only a demonstrated responsibility or dependency seam. Do not invent nodes or edges to complete a preferred architecture shape."

The durable-map paragraph also changes. See section 6.7.

### 6.3 When invoked

V1 status: REWRITE TABLE.

Replace branches as follows:

Placing a file:
- Use Procedure: Work a capability change.
- Focus on responsibility, existing authority, and dependency edge.

Reviewing an import:
- Treat the import as a graph edge.
- Run Check: Import matrix.

Renaming a capability:
- Map affected graph nodes and aliases.
- Run Check: Name continuity.

Auditing drift:
- Map entry points, authorities, dependencies, and boundary crossings.
- Run Check: Capability graph and Check: Import matrix.

Revamping:
- Use Procedure: Revamp.

Greenfield/legacy paragraph:

Keep the "do not boil the ocean" idea.
Rewrite the legacy clause so it no longer says "moves the touched capability onto the noun chain."

Proposed meaning:

"Legacy: do not boil the ocean. The next change obeys the laws and repairs only the touched capability subgraph required by the task."

### 6.4 Procedure: Place a file

V1 status: REMOVE AS A STANDALONE PROCEDURE.

Reason:

The current procedure begins by naming a layer and placing the file into a fixed noun-chain model. V2 needs one general procedure that works for placing, moving, splitting, and reviewing code.

Replace with a section titled `Procedure: Work a capability change`.


Step 1: Locate
- Find the exact target using the locate ladder.
- Do not edit yet.

Step 2: Observe
- Read the target.
- Read its immediate parent/caller when available.
- Read direct imports and direct consumers relevant to the task.
- Read existing tests and sibling patterns when they affect placement.

Step 3: Name the capability
- Name one canonical capability noun.
- Search for existing names and aliases before inventing a new one.

Step 4: Map the smallest useful graph
- Start with the target plus one relationship hop.
- Record nodes, authorities, boundaries, and important edges temporarily.
- Expand only if the proposed change crosses that edge.

Step 5: Diagnose
- Identify one real architecture problem using the allowed diagnosis list.
- If no architecture problem is demonstrated, prefer an in-place cleanup.

Step 6: Prove a new seam when needed
- Before creating a new file/module/component/composable, answer the seam-proof fields.

Step 7: Change one seam
- Perform one structural change only.

Step 8: Verify
- Re-read changed nodes and immediate neighbors.
- Check imports.
- Run the strongest available verification.
- State the evidence level accurately.

Step 9: Stop or expand
- Stop when the requested problem is solved.
- Expand one hop only if the original task still requires it.

Done condition:

"The requested behavior is preserved at the evidence level actually verified, each changed responsibility has one authority, and no unnecessary graph node or dependency edge was introduced."

### 6.5 Language

V1 status: KEEP NOUN/VERB/ROLE, REPLACE NOUN MAP DEFINITION, ADD GRAPH TERMS.

Keep:

- Noun
- Verb
- Role
- Sentence test
- Language rules 1 through 5, with only wording edits needed for graph terminology.

Remove:

- Noun map as a required language primitive.

Add:

Node:
"A meaningful architectural thing in the touched capability: component, module, state owner, contract, domain rule set, adapter, entry point, generated artifact, or equivalent repository concept. A node is not automatically a file."

Edge:
"A meaningful relationship between nodes. Use the small canonical vocabulary: depends on, owns, reads, writes, calls, adapts."

Capability graph:
"The smallest useful set of nodes and edges needed to explain the touched capability. It describes the repository that exists instead of assuming a fixed sequence of layers."

Authority:
"The node that owns the meaning of a responsibility. Many nodes may consume or represent a responsibility. One node owns it."

Boundary:
"A point where mechanism-specific behavior enters or leaves the capability, such as UI, browser, network, storage, auth, messaging, filesystem, or vendor SDK."

### 6.6 New seam proof

V1 status: ADD NEW REQUIRED CHECK.

Before creating a new structural node, the model must state:

Responsibility:
Current authority:
Proposed authority:
Why the existing authority cannot remain:

Additional rule:

"If the last field cannot be answered with a demonstrated responsibility or dependency seam, do not create the node."

This is required before any new module, component, composable, adapter, contract package, or domain package created primarily for architectural separation.

### 6.7 Noun map template

V1 status: REMOVE FIXED TABLE, REPLACE WITH OPTIONAL DURABLE CAPABILITY MAP.

Remove entirely:

- Fixed columns: Noun, Route, UI, Contract, Adapter, Domain, Definitions, Alias.
- Done condition requiring every live route to have a row.

V2 default:

Graph traces are temporary working notes.

Do not create repository documentation for a bounded task unless one of these is true:

- The user explicitly asks for it.
- The repository already maintains architecture maps.
- A repository-wide audit is the task.
- A large rename requires persistent alias tracking.
- The same ambiguity has recurred enough that durable documentation is justified.

If durable documentation is justified, preferred default path is:

.cursor/capability-map.md

Recommended format:

Nodes table:
| Node | Kind | Capability | Authority | Location | Alias |

Edges table:
| From | Relationship | To | Boundary/Reason |

Legacy rule:

"If .cursor/noun-map.md already exists, read it as legacy naming evidence. Do not delete, rewrite, or automatically migrate it during unrelated work."

### 6.8 Check: Noun-chain walk

V1 status: REMOVE.

Replace with two separate checks.

#### Check: Capability graph

Required questions:

1. What nodes are involved in the touched behavior?
2. Which node owns each relevant responsibility?
3. What are the important dependency edges?
4. Where are mechanism boundaries crossed?
5. Did the change create duplicate authority?
6. Did the change create an unnecessary node or edge?
7. Are dependencies pointing in allowed directions?
8. Is any node present only because a taxonomy expected it?

Fail conditions:

- Two nodes claim authority for the same rule.
- Mechanism code owns domain/policy meaning.
- A new node has no seam proof.
- A new dependency violates the import matrix.
- The graph had to be invented to justify the refactor.

#### Check: Name continuity

Required questions:

1. What is the canonical capability noun?
2. Which nodes reuse it coherently?
3. Which published, framework-owned, or boundary-specific names intentionally differ?
4. Is each intentional alias or mapping obvious?
5. Did the change introduce a new unexplained synonym?

Fail condition:

- The same capability is given unrelated names without an explicit reason or mapping.

### 6.9 Check: Sentence test

V1 status: KEEP.

Only change examples if needed to avoid implying universal physical layers.

Keep the central rule:

- The path should read as a speakable sentence from repository-owned structure to capability to narrowing job/type.

Add:

"Sentence test is a naming/findability check. It does not prove architectural correctness."

This prevents the naming check from being used as a substitute for graph reasoning.

### 6.10 Check: Import matrix

V1 status: KEEP CORE, ADD APPLICATION/USE CASE, REFRAME IMPORTS AS EDGES.

Opening change:

Current idea:
"List every new or changed import."

V2:
"Treat every new or changed import as a dependency edge in the capability graph."

Add one classification:

Definitions | Domain/Policy | Contracts | Application/Use Case | Adapters | UI

Proposed matrix intent:

Definitions:
- May import other definitions.
- Must not import Domain/Policy, Application, adapters, UI, or generated runtime artifacts.

Domain/Policy:
- May import domain internals and language/runtime basics.
- Must not import UI, Application orchestration, concrete adapters, vendor SDKs, transport/session objects, or frozen trees.

Contracts:
- May import other contracts as schema requires.
- Must not own business rules or depend on UI/adapters.

Application/Use Case:
- May import Domain/Policy and abstract/public ports/contracts.
- Coordinates business sequencing, authorization decisions, transaction scope, and side effects through ports.
- Must not depend on UI or concrete adapter internals.

Adapters:
- May depend inward on Application/Use Case, Domain/Policy, public contracts, and outward on vendor SDKs.
- Must not depend on UI.
- Do not own business rules.

UI:
- May depend on UI state, Application/Use Case, Domain/Policy, and public contracts.
- Must not depend on adapter internals, vendor infrastructure SDKs, or generated internals.

Keep:

- Generated contracts use public names only.
- Generated internals are not imported directly.
- Taint-boundary/security explanation stays.

### 6.11 Shape (10)

V1 status: KEEP MOST, TIGHTEN 1, 3, 9, 10.

Shape 1 Domain is the core:
- Keep current V1 meaning.
- Rename mental category to Domain/Policy where useful.
- Keep the statement that purity/reuse alone does not make code Domain.

Shape 2 Edges are adapters:
- Keep.

Shape 3 UI is another edge:
- Keep current Application/Use Case distinction.
- Align it with the new import-matrix row.

Shape 4 Declare what varies:
- Keep.

Shape 5 Generated artifacts are not source:
- Keep.

Shape 6 Dependencies point inward:
- Keep, updated for Application/Use Case.

Shape 7 Share contracts, not platforms:
- Keep.

Shape 8 Separate frozen from editable:
- Keep.

Shape 9 One responsibility, one authority:
- Rewrite for graph language:

"A responsibility has one authority. Many nodes may consume or represent that responsibility. Only one node owns its meaning. Do not create a new authority unless a demonstrated responsibility or dependency seam requires one."

Add:

"A long file is not enough evidence for a split."

Shape 10 Extend before inventing:
- Keep.
- Add:

"A new node requires seam proof."

### 6.12 Names (10)

V1 status: KEEP MOST, REMOVE CHAIN DEPENDENCY.

Opening sentence rewrite:

Current idea:
"One capability name, reused everywhere."

V2:
"One canonical capability noun, reused wherever the repository can do so coherently. Published, framework-owned, generated, or boundary-specific names may differ when the mapping is explicit."

Name 1 Root folders follow repository reality:
- Keep.

Name 2 Capability name is the index:
- Keep and make it the bridge to the graph.

Name 3 Repository entry point as boundary key:
- Keep.

Name 4 Adapter naming:
- Keep.

Name 5 Domain packages are noun/files are type:
- Keep as a compatible pattern, but do not make it imply every repository needs a Domain folder.

Name 6 Definition data mirrors noun:
- Keep.

Name 7 Contracts use same noun:
- Keep with alias language.

Name 8 Case follows conventions:
- Keep.

Name 9 UI nests by noun then job:
- Keep as a repository-compatible default, not an architecture proof.

Name 10 Findability:
- Replace "Findability is Check: Noun-chain walk."
- Proposed V2:

"Findability means a newcomer can enter through an obvious node or public entry point and follow meaningful graph relationships to the code that owns the behavior. Use Check: Name continuity for naming and Check: Capability graph for architecture."

### 6.13 Security placement

V1 status: KEEP ALMOST ENTIRELY.

Reason:

The section already reasons about boundaries and dependency direction. It fits the graph model naturally.

Minor wording changes:

- Treat trust boundary, vendor SDK, data flow, and auth placement as graph boundary/edge checks.
- Keep pure policy in Domain/Policy.
- Keep token/session/cookie handling out of Domain/Policy.

No new security scope is added.

### 6.14 Feature hops

V1 status: REMOVE FIXED HOP LIST.

Reason:

The list Definition, Contract, Generated, Domain, Adapter, UI assumes a topology that may not exist.

Replace the section title with `Affected graph`.

Proposed rule:

"A change is complete when every affected relationship from the changed responsibility has been updated, verified unchanged, or explicitly ruled out. Do not invent a category that does not exist in the repository."

Inspect applicable relationships:

- inbound callers/consumers
- owned state
- authoritative rules
- contracts/types
- generated derivatives
- outbound adapters/side effects
- persistence
- events/messages
- UI representations
- tests

Done condition:

"The touched responsibility has one authority, its affected edges are accounted for, and no new unrelated graph branch was introduced."

### 6.15 Tests by layer

V1 status: REWRITE AS TESTS BY RESPONSIBILITY.

Reason:

V2 adds Application/Use Case and does not assume physical layer folders.

Proposed categories:

Domain/Policy:
- rules, invariants, transformations, pure policy
- no network, disk, UI, session, vendor SDK

Application/Use Case:
- sequencing, orchestration, transaction/auth decisions, port coordination
- fake or test ports allowed
- no concrete vendor SDK requirement

Adapters:
- parse, authenticate, authorize boundary input, map errors, call inward, emit boundary/audit effects
- no duplicated business rules

UI:
- composition, presentation state, interaction state
- no business-rule authority
- no auth enforcement authority

Generated/Contracts:
- generator/schema tests or compatibility tests when repository practice supports them

General rule:

"Tests follow the responsibility they prove. Follow repository placement conventions."

### 6.16 Recovery and safe stop

V1 status: ADD NEW SECTION.

This section is intentionally short and procedural.

Proposed wording:

"If an edit fails, re-read the affected file before another structural edit. If the same structural change fails twice, stop expanding the refactor and report the blocker. Do not reconstruct large files from memory."

"If the target, graph, or verification state is uncertain, stop rather than guess. A bounded safe stop is better than a broken architecture."

"Do not claim behavior preservation above the evidence actually verified."

### 6.17 Procedure: Revamp

V1 status: REWRITE AROUND GRAPH REPAIR.

Proposed V2 procedure:

1. Locate the touched capability.
2. Map the smallest useful subgraph.
3. Identify duplicate authority, invalid dependency edges, mechanism/policy mixing, unexplained aliases, or unnecessary intermediary nodes.
4. Choose the highest-value real seam required by the task.
5. State seam proof if creating a new node.
6. Change one seam.
7. Re-read and verify the changed local graph.
8. Stop if the requested problem is solved.
9. Expand one hop only when the remaining task requires it.
10. Repeat for another capability only when the user request explicitly includes it.

Keep from V1 in adapted form:

- Stop the bleeding.
- Move rules inward.
- Thin adapters.
- Restore source of truth for generated artifacts.
- Do not widen the task to normalize the repository.

Remove:

- "For one noun, Check: Noun-chain walk."
- "Fix the noun chain."

Replace with graph and name-continuity checks.

### 6.18 When you cannot comply

V1 status: REWRITE.

Published name:

"Do not break external consumers unless asked. Keep the published name at its boundary node and record the mapping to the canonical capability noun when a durable map is already justified."

Existing module in wrong responsibility:

Keep the current one-home idea but express it as authority:

"If an existing node is the wrong authority for the responsibility, do not extend the mistake. Move the responsibility to the correct authority at one verified seam."

Missing conceptual category:

Replace N/A-hop language with:

"If a conceptual category does not exist in the repository, do not create a node for it."

Legacy noun map:

"Existing .cursor/noun-map.md is evidence, not a migration command. Preserve it unless the task explicitly includes architecture-document migration."

### 6.19 Out of scope

V1 status: KEEP.

Keep:

- Cloud
- IaC
- table keys
- deploy scripts
- UI-kit style
- definition-format authoring
- vulnerability scoring

Rewrite final sentence so it uses authority/seam language instead of layer language:

"When a blob needs a smaller interface, split only at a demonstrated responsibility or dependency seam."

### 6.20 V1 to V2 change ledger

| V1 section | V2 action | V2 destination |
| --- | --- | --- |
| Frontmatter description | Rewrite | Frontmatter |
| Opening overview | Keep most, rewrite chain model | Overview and Core model |
| Noun chain paragraph | Remove | Replaced by Capability graph |
| Durable noun-map paragraph | Rewrite | Optional durable capability map |
| When invoked | Rewrite | When invoked |
| Procedure: Place a file | Remove as standalone | Procedure: Work a capability change |
| Language noun/verb/role | Keep | Language |
| Language noun-map definition | Remove | Node, Edge, Capability graph, Authority, Boundary |
| Noun map template | Remove fixed chain table | Optional durable capability map |
| Check: Noun-chain walk | Remove | Check: Capability graph + Check: Name continuity |
| Check: Sentence test | Keep, narrow scope | Check: Sentence test |
| Check: Import matrix | Keep and expand | Add Application/Use Case and graph-edge framing |
| Shape 1-8 | Keep with small alignment edits | Shape |
| Shape 9 | Rewrite | Graph authority law |
| Shape 10 | Keep, add seam proof | Shape |
| Names 1-9 | Keep with small graph alignment | Names |
| Names 10 | Rewrite | Graph findability + name continuity |
| Security placement | Keep | Security placement |
| Feature hops | Remove | Affected graph |
| Tests by layer | Rewrite | Tests by responsibility |
| Procedure: Revamp | Rewrite | Graph repair procedure |
| When you cannot comply | Rewrite | Boundary aliases, wrong authority, missing categories, legacy map |
| Out of scope | Keep | Out of scope |
| conventions.md | Minimal wording only | conventions.md |

## 7. conventions.md design

V1 conventions status: MINIMAL CHANGE.

The physical conventions overlay already has a compatibility gate and repository-first rule. V2 should not turn the graph concept into a new folder scheme.

Keep:

- Compatibility gate.
- Repo/framework conventions win.
- .cursor/architecture-conventions.md override.
- Case table.
- UI tree defaults.
- Adapter tree defaults.
- Tests follow repo placement.

Potential wording changes only:

1. Header sentence:
   - Replace any reference to "laws" that could imply physical graph folders with "architecture laws live in SKILL.md."

2. Layer and capability folder example:
   - Keep as compatible TypeScript/Vue/Nuxt spelling, not as a requirement that all graph node kinds become folders.

3. Adapter tree:
   - Keep `{Noun}-{Role}` as a compatible-stack default.

No graph-map file format belongs in conventions.md.

## 8. Diagnosis rules

V2 must force a diagnosis before structural work.

A structural change is justified only when at least one of these is demonstrated:

1. Two nodes own the same responsibility.
2. One node owns unrelated responsibilities that have independent dependency seams.
3. A dependency edge crosses a forbidden boundary.
4. Mechanism-specific code owns policy/domain meaning.
5. A rule has been duplicated.
6. A public contract and its implementation have become incoherent.
7. The requested change cannot be made safely without separating an existing seam.

These are not sufficient reasons by themselves:

- The file is long.
- The code looks messy.
- A helper is pure.
- A helper could be reused.
- A folder is missing from an architecture diagram.
- A new abstraction would look cleaner.
- A taxonomy has an empty category.

If no real architecture problem is demonstrated, the model should prefer an in-place cleanup.

## 9. Graph depth rule

V2 must explicitly bound graph exploration.

Default depth:

- Target plus one relationship hop.

Expand one more hop only when:

- The responsibility being moved crosses that edge.
- A changed node has an external/public consumer that can be affected.
- The dependency law cannot be evaluated locally.
- A public rename or repository audit explicitly requires broader tracing.

Repository-wide graphing is only appropriate for an explicit audit, migration, or rename scope.

This rule exists to control context size and prevent architecture expansion.

## 10. Generated and frozen as node properties

V2 should stop treating generated/frozen status as if they are always separate architecture layers.

Graph representation can record:

- Kind
- Status: authored, generated, frozen, vendor, build output
- Editable: yes/no

Rules remain:

- Edit definitions, not generated output.
- Do not hand-edit frozen/vendor/build output.
- Public generated contracts can be graph nodes without becoming editable authorities.

## 11. Expected behavior on previously excluded model classes

This section is a design target, not a claim that V2 will achieve it.

### 11.1 Inconsistent model target

Desired V2 improvement:

- Fewer parallel structural changes.
- Re-read after edit failure.
- Stop after repeated failure.
- Preserve a coherent partial result or make no structural edit.
- Avoid leaving unwired components/composables.

Success is not "complete the whole refactor."
Success can be "complete one verified seam and stop."

### 11.2 Low-capability model target

Desired V2 improvement:

- Locate target through the ladder before asking for help.
- Read target before proposing architecture.
- Map at least one meaningful local graph.
- Avoid rename proposals based only on filenames.
- Avoid creating files when seam proof cannot be stated.
- Stop safely when the task exceeds capability.

Success can be "no change, but correct diagnosis and safe stop."

## 12. Non-goals

V2 will not attempt to:

- Make every model capable of large refactors.
- Create a universal architecture graph format.
- Require repository-wide architecture documentation.
- Replace framework conventions.
- Force DDD, Clean Architecture, Hexagonal Architecture, or any named architecture.
- Turn every import into a permanent graph artifact.
- Increase the number of layers.
- Automatically migrate existing .cursor/noun-map.md files.
- Claim runtime behavior preservation from static checks.

## 13. V2 evaluation plan

The current V1 candidate remains frozen and is not edited in place.

V2 receives a new identity and hash only after the pre-implementation RED evidence is preserved.

### 13.0 Pre-implementation RED gate

V2 changes behavior, so the new pressure cases must exist before the skill is rewritten.

Task 01 already provides RED evidence for several targeted failures:

- V1 can still permit model-specific over-splitting or coordination mistakes.
- V1 does not reliably control edit/recovery behavior on inconsistent models.
- V1 does not reliably help a low-capability model complete or safely stop the task.
- V1 still contains a chain model that assumes expected hops rather than discovered relationships.

Before writing V2, add at least one new graph-specific pressure prompt and run the frozen V1 candidate on it. Preserve the run before any V2 wording exists.

Recommended graph-specific RED prompt:

"A few places in this project seem to be doing the same thing differently. Figure out what actually owns the behavior, clean up the duplication, and do not change how it works."

Minimum recommended RED models:

- One competent model that already produced coherent V1 work.
- Gemini 2.5 diagnostic if available, to observe whether it starts multiple structural changes or loses edit state.

The RED run is not required to fail catastrophically. It must simply show what V1 currently does under the new pressure so V2 is written against observed behavior rather than imagined behavior.

Do not edit V1 or create V2 until the RED prompt, run metadata, transcript, and result archive are frozen.

### 13.1 Phase A: Task 01 regression gate

Use the exact original Task 01 prompt:

"this roof image measure panel has gotten ridiculous. clean it up and structure it in a way that makes sense without changing how it works."

Run V2 against the same baseline repository and lifecycle.

Models:

- Grok 4.6 High
- Kimi K2.7 Code
- GPT-5.1
- Gemini 2.5 diagnostic

Primary question:

Does V2 preserve or improve the useful V1 behavior on competent models while producing safer failure behavior on the diagnostic models?

### 13.2 Task 01 regression assertions

For Grok:

- No mandatory noun-map creation.
- No false Domain bucket for DOM/presentation code.
- Architectural pressure remains.
- New files require seam proof.

For Kimi:

- No false Domain bucket.
- Coupled session state is not split across authorities without explicit coordination.
- Clear/reset behavior does not regress.
- One structural seam is completed before another begins.

For GPT-5.1:

- Candidate can still change architectural strategy when a real seam is demonstrated.
- No noun map.
- No generic Domain dumping ground.
- Prop/reactivity relationships are traced before extraction.
- Verification claims remain bounded to evidence.

For Gemini diagnostic:

- Reads target before architecture proposal.
- Does not begin multiple parallel extractions before verification.
- Re-reads after edit failure.
- Stops expansion after repeated failure.
- Does not leave a larger broken graph than it started with.

### 13.3 Phase B: Graph-pressure task

After Task 01 passes the regression gate, use a new prompt that pressures authority and duplication rather than file size.

Proposed prompt:

"A few places in this project seem to be doing the same thing differently. Figure out what actually owns the behavior, clean up the duplication, and do not change how it works."

This tests:

- authority discovery
- duplicate-rule detection
- graph traversal
- existing-home preference
- boundary reasoning
- name continuity

Use the same original/no-skill/V1/V2 comparison strategy as budget allows.

### 13.4 Phase C: Fresh paired confirmation

Historical V1 results are useful, but a fresh paired V1 vs V2 confirmation reduces time/harness drift.

Minimum recommended paired models:

- Grok 4.6 High
- Kimi K2.7 Code
- GPT-5.1

Each pair uses:

- same baseline
- same prompt
- same harness
- fresh context
- V1 frozen candidate
- V2 graph candidate

Diagnostic models can be repeated after primary paired results if they remain available.

### 13.5 Phase D: Ablation

If V2 outperforms V1, do not assume every new rule matters.

Ablate these groups independently:

A. Capability graph replaces noun chain.
B. One-seam-at-a-time execution.
C. Seam proof before new node.
D. Locate and recovery ladder.
E. Application/Use Case dependency category.
F. Depth-limited graph traversal.
G. Verification-honesty wording.

Remove one group at a time and rerun a pressure case.

A rule group is load-bearing only when its removal repeatedly causes the targeted behavior to regress.

## 14. Scoring changes for V2

Keep the existing architecture/behavior scoring, but add these rows:

- Target located without human path assistance.
- Target read before structural proposal.
- Immediate graph mapped coherently.
- Authority explicitly identified.
- New node seam proof present.
- Number of simultaneous unfinished structural extractions.
- Re-read after failed edit.
- Safe stop after repeated failure.
- Verification level stated accurately.
- Unnecessary durable architecture file created.
- New dependency edge justified.
- Broken/unwired node left behind.

Correctness gate:

Source reduction or elegance does not count as a positive architecture result when the implementation is statically broken or behaviorally regressed.

Safe-stop rule:

For a diagnostic weak model, a coherent safe stop scores above an incomplete broken refactor even if the safe stop changes no product code.

## 15. Acceptance criteria for implementing V2

Do not implement V2 until this design is approved.

When implementation begins, the V2 SKILL.md must satisfy all of these:

1. No fixed noun chain remains as the architecture model.
2. Capability noun remains as naming/index concept.
3. Graph is temporary by default.
4. Durable capability map is conditional, not automatic.
5. Noun-chain walk is removed.
6. Capability graph check and name-continuity check are separate.
7. Application/Use Case exists in the import matrix.
8. One-seam-at-a-time loop is explicit.
9. Seam proof is required before a new structural node.
10. Locate ladder is explicit.
11. Edit failure recovery is explicit.
12. Safe stop is explicitly valid.
13. Graph depth is bounded by default.
14. Verification claims are limited to evidence level.
15. Existing noun maps are treated as legacy evidence, not auto-migrated.
16. conventions.md remains a compatibility overlay, not a graph folder schema.
17. Security-placement laws remain intact.
18. Generated/frozen source rules remain intact.
19. The skill does not mention specific tested models.
20. The skill is shorter or no more cognitively dense than necessary to express these laws.

## 16. Implementation strategy after approval

Approval of this spec does not immediately authorize rewriting the skill. Skill changes use the same RED, GREEN, REFACTOR discipline as the existing evaluation method.

Recommended sequence:

1. Preserve V1 hashes and files unchanged.
2. Freeze the new graph-specific RED prompt and scoring assertions.
3. Run the frozen V1 candidate on the RED pressure case and preserve transcript/result evidence.
4. Review the RED trace for the exact behavior V2 must change.
5. Copy frozen V1 candidate to a new V2 working directory.
6. Rewrite frontmatter and opening model.
7. Replace Place a file with Work a capability change.
8. Replace noun-map/chain sections with graph/name checks.
9. Update import matrix with Application/Use Case.
10. Rewrite Shape 9/10 and Names 10.
11. Replace Feature hops with Affected graph.
12. Add Recovery and safe stop.
13. Rewrite Revamp.
14. Make minimal conventions.md wording changes only if needed.
15. Run structural self-review against the 20 acceptance criteria.
16. Hash V2 artifacts.
17. Preregister Task 01 V2 assertions before executing the first V2 run.
18. Run Task 01 regression gate.
19. Run the same graph-pressure prompt used for the RED baseline.
20. Keep, revise, or reject V2 from the observed comparison.

No V1 evidence, report, or handoff package is edited retroactively when V2 is created.

## 17. Open design questions requiring approval

These are the only choices that should be resolved before implementation.

1. Durable map filename
   Recommended: `.cursor/capability-map.md`
   Alternative: keep `.cursor/noun-map.md` only when already present and never define a new default durable map filename.

2. Canonical edge vocabulary
   Recommended six: depends on, owns, reads, writes, calls, adapts.
   Question: should "renders" and "emits" be official edge words, or remain descriptive prose?

3. Edit failure threshold
   Recommended: one failure triggers re-read; second failure on the same structural change triggers safe stop.

4. Application/Use Case naming
   Recommended label: `Application/Use Case` so repositories do not need an `Application/` folder.

5. Safe-stop result language
   Recommended: explicitly say a safe stop is a valid outcome when the model cannot establish a safe next edit.

## 18. Recommended decisions

For implementation, use these defaults unless changed during review:

- Durable map filename: `.cursor/capability-map.md` only when durability is justified.
- Edge vocabulary: six canonical terms only. Keep "renders" and "emits" as normal prose.
- Edit failure threshold: re-read after first failure, safe stop after second failure on the same structural change.
- Application label: `Application/Use Case`.
- Safe stop: explicitly valid.

## 19. Final design statement

V1 asks the model to reason about architecture primarily through a capability noun and a sequence of expected hops.

V2 keeps the capability noun but replaces the expected sequence with discovered relationships.

The V2 operating model is:

"Find the thing. Read the thing and its immediate relationships. Name the capability. Map the smallest useful graph. Identify authority. Diagnose one real seam. Change one seam. Verify it. Expand only if the original problem still requires it. Stop rather than guess."

This is the behavior the implementation must encode and the evaluation must test.
