# Jarrod — Read This First

## 01-V1-CANDIDATE: why it differs from the supplied original

This file is the decision record for the first targeted revision of `layered-codebase-architecture`.

It explains **why** I changed the supplied skill, not just what changed. The exact textual change is preserved separately in `FROM-00.diff`.

V1 is not presented here as a universally proven improvement. It was the first candidate justified by the controlled evidence available at that point.

## The evidence sequence that justified editing the skill

### Run 0001 — supplied original, forced

With the supplied skill active, Grok 4.6 High treated the roof image measure task as an architecture problem rather than only a UI cleanup. That was useful. The skill created real architectural pressure.

It also exposed several behaviors I did not want to accept without testing:

- broad decomposition beyond the immediate request;
- creation of a persistent repository noun map;
- a generic shared helper that grouped mixed concerns because the code looked pure or reusable;
- physical structure decisions that appeared to come from the skill's taxonomy rather than from the repository;
- pressure toward globally consistent naming and folder shapes even where a framework or boundary could legitimately use different vocabulary.

I did **not** change the skill after 0001. I first needed to know which behaviors came from the skill and which Grok would have produced naturally.

### Run 0002 — no-skill control

With the same repository baseline, task, harness, and model but without the architecture skill, Grok mostly treated the problem as a local UI/layout cleanup. It did not reproduce the architectural decomposition from 0001.

That control established the main thing I wanted to preserve: the supplied skill was materially changing how the model framed the task. It made the model see responsibility structure that the no-skill run mostly ignored.

The decision was therefore **not** to make the skill less architectural.

The decision was to keep that architectural pressure while removing places where the skill appeared to prescribe too much of the repository's physical answer before reading the repository closely enough.

## The changes I made from the supplied original to V1

### 1. Tightened what counts as Domain

**Problem:** The original wording made it too easy to classify pure or reusable calculations as Domain simply because they were portable.

**Change:** V1 makes domain ownership depend on business meaning and invariants, not purity or reuse alone. Mechanism-dependent calculations stay with the boundary whose concepts give them meaning.

**Why:** In 0001, crop, scale, pointer, formatting, and related helpers were pulled into a generic shared/domain-style module even though several of them were presentation or mechanism concerns.

**Intent:** Preserve real domain extraction without turning every clean helper into domain logic.

### 2. Made application/use-case responsibility conceptual instead of requiring a physical layer

**Problem:** A responsibility taxonomy can accidentally become a folder-generation instruction.

**Change:** V1 recognizes application/use-case responsibility when behavior coordinates rules, ports, side effects, authorization/transaction scope, or business sequencing, even when the repository has no `Application/` folder.

**Why:** The architecture concept is useful; requiring a physical layer with that name is not universally valid.

**Intent:** Let the model identify orchestration responsibility without inventing repository structure just to satisfy the taxonomy.

### 3. Changed "one concern, one home" into "one responsibility, one authority"

**Problem:** "One concern, one home" can be interpreted physically: one concern becomes one new file, folder, or layer.

**Change:** V1 uses **one responsibility, one authority**. A rule or responsibility should have one authoritative owner, while representations and supporting operations may legitimately exist at more than one boundary.

**Why:** Architectural ownership is the important invariant. Physical singularity is not.

**Intent:** Prevent taxonomy-driven file creation while still preventing duplicated authority.

### 4. Made repository structure follow repository reality

**Problem:** Universal statements such as root folders being layers can conflict with valid feature packages, crates, plugins, framework-owned directories, modules, or other repository shapes.

**Change:** V1 keeps the conceptual responsibility rules but makes physical placement follow the language, framework, project, and existing repository conventions unless a real responsibility or dependency violation justifies restructuring.

**Why:** An any-repository skill cannot treat one physical layout as the definition of good architecture.

**Intent:** Make the skill portable across codebases instead of teaching every codebase to look like the examples in the skill.

### 5. Allowed explicit boundary vocabulary mappings

**Problem:** Requiring one exact canonical word everywhere can force unnecessary renames across APIs, protocols, legacy surfaces, framework-owned names, or external contracts.

**Change:** V1 allows boundary-specific vocabulary when the mapping back to the canonical capability is explicit.

**Why:** The real failure is unexplained translation, not the existence of two legitimate names at different boundaries.

**Intent:** Preserve findability and conceptual consistency without forcing destructive or cosmetic renaming.

### 6. Kept adapter responsibility, relaxed exact adapter spelling

**Problem:** The original `{Noun}-{Role}` style is useful in a compatible stack but too specific to be a universal architecture law.

**Change:** V1 keeps the requirement that edge/boundary responsibility be understandable while allowing actual folder and file spelling to follow the repository.

**Why:** An adapter should still be recognizable as an adapter whether the codebase is TypeScript, Python, Rust, Go, Java, C, or something else.

**Intent:** Preserve the architectural boundary without prescribing one naming dialect.

### 7. Bounded Revamp to the requested capability

**Problem:** The original Revamp flow could build momentum beyond the user's request by filling a broad noun map and continuing into the next noun/capability.

**Change:** V1 starts with the touched capability and its immediate dependencies, defines completion around the requested capability, and only proceeds to another capability when the task actually includes it.

**Why:** 0001 showed that a local request could trigger persistent repository-wide architecture work.

**Intent:** Keep the skill willing to clean architecture aggressively where needed while giving it a real stopping condition.

### 8. Removed the automatic repository-wide noun-map obligation

**Problem:** A persistent repository artifact appeared in 0001 even though the user asked to clean up one panel.

**Change:** V1 makes local architectural inspection the starting point instead of requiring the repository noun map to be populated as a prerequisite.

**Why:** A repo-level architecture artifact should exist because the task needs it, not because the skill always demands one.

**Intent:** Reduce scope expansion and permanent artifacts that do not directly support the requested work.

### 9. Added an explicit compatibility gate to `conventions.md`

**Problem:** `conventions.md` contains TypeScript/Vue/Nuxt-oriented physical naming and placement examples that could be mistaken for universal laws.

**Change:** V1 explicitly limits those defaults to compatible repositories and states that repository-local and framework conventions win.

**Why:** The skill is intended to operate across arbitrary codebases.

**Intent:** Keep useful concrete examples without allowing them to overwrite a different ecosystem's native structure.

### 10. Changed test placement from a universal location to repository-following placement

**Problem:** A fixed co-location rule for tests is not valid across all repositories and frameworks.

**Change:** V1 tells the model to follow the repository's existing test-placement convention; co-located `*.test.ts` is only a compatible default.

**Why:** Test architecture is part of repository reality too.

**Intent:** Avoid creating a second test-layout convention inside an existing project.

## What I deliberately did not remove

I did not remove the parts of the supplied skill that made the model recognize architecture as architecture.

The no-skill control showed that this pressure was doing useful work. V1 still expects the model to identify responsibility boundaries, dependency direction, domain ownership, adapters, UI boundaries, contracts, generated artifacts, and authority.

The revision was targeted: **preserve the useful architectural framing, reduce premature physical prescription.**

## What happened when V1 was run

Run 0003 used this candidate against the same task and baseline.

Compared with 0001, V1 avoided the persistent noun map and generic shared bucket, extended existing related modules instead of inventing one broad new domain bucket, kept browser pointer mechanics at the UI edge, used more explicit component interfaces, and performed stronger verification including extracted-rule tests and typecheck.

That result was promising, but it was not treated as universal proof. The candidate was carried forward for additional model evaluation rather than declared finished from one run.

## How to audit this decision

Use these files together:

- `../00-SUPPLIED/` — the exact supplied original;
- `FROM-00.diff` — the exact original → V1 textual change;
- `SKILL.md` and `conventions.md` — the V1 artifact actually evaluated;
- `../../../DEVELOPMENT-HISTORY/0001.md` — what the original run supported at that point;
- `../../../DEVELOPMENT-HISTORY/0002.md` — what the no-skill control established;
- `../../../DEVELOPMENT-HISTORY/0003.md` — what the first V1 run supported;
- `../../../EXPERIMENTS/EXP-0001-task01-roof-image-measure/` — controlled experiment definition, conditions, run index, and scorecard;
- `../../../EVIDENCE/` — preserved run evidence;
- `../../../REPORTS/layered-codebase-architecture/full-working-evaluation.docx` — the long-form working record.

The diff answers **what changed**.

This file answers **why I changed it**.

The experiment and evidence answer **what actually happened when it was tested**.
