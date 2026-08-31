# Run Naming

Global run IDs are four digits and never reset when the skill changes.

`0001` through `0015` belong to the first study. The current completed run and next planned run are recorded in `CURRENT-STATE.md`.

Run IDs describe canonical preserved runs in the current public lab record. If imported material is excluded from canonical history, later runs are renumbered so the public run sequence remains contiguous.

Do not reuse IDs present in `EVIDENCE/`, `DATA/runs.json`, `DEVELOPMENT-HISTORY/`, already-cut experiment run indexes, archives, or prep files. Treat explicit current-state reservations as unavailable unless they are explicitly superseded before any run is cut. Existing run IDs are immutable.

Experiment IDs use `EXP-0001`, `EXP-0002`, and so on.

Skill versions are local to each skill, for example `00-SUPPLIED`, `01-V1-CANDIDATE`, `02-V2-GRAPH`.
