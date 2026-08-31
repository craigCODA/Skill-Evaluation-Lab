# Methodology

Skills are treatments. The experiment is not whether the Markdown looks better. The experiment is whether a changed instruction changes agent behavior under controlled conditions.

## Default loop

1. Freeze the skill artifact.
2. Freeze task, model, harness, tools, budget, baseline repository, and scorer where possible.
3. Run clean-context conditions.
4. Preserve the result before cleanup.
5. Read traces and changed code.
6. Classify failures and questions.
7. Research only the questions surfaced by evidence.
8. Make the smallest justified skill change.
9. Re-run old versus new under matched conditions.
10. Use holdouts before generalizing.

Separate trigger accuracy from body quality. One run does not prove universal behavior.

## Promotion Rule

A skill change is promoted only when the evidence shows a behavior change worth preserving.

Prefer the smallest skill edit that explains the observed failure.

Use matched reruns before claiming improvement.

Use a holdout task before claiming generality.

## Research Boundary

Evidence records say what happened.

Development history says what was concluded at that time.

Current state says what to do next.
