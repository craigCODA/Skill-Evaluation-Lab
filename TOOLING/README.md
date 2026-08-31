# Tooling

Tooling exists to make preservation repeatable, not to become another source of experimental truth. Any automation that mutates a run must preserve the pre-mutation state first.

Use `verification/verify_lab.py` before committing changes to current lab metadata.

The verifier reads `DATA/runs.json`, `EVIDENCE/`, `EXPERIMENTS/`, and canonical skill hashes.
