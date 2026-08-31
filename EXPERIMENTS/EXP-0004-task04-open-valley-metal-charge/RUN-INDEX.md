# EXP-0004 Run Index

The experiment begins when global run `0024` is cut. These rows define the frozen GPT-5.1 first-model block; they are not evidence until each run is actually preserved.

| Run | Model | Version | Evidence class | Condition | Status |
| --- | --- | --- | --- | --- | --- |
| `0024` | GPT-5.1 | 00-SUPPLIED | primary | supplied original, forced | preserved |
| `0025` | GPT-5.1 | NO-SKILL | primary | no explicit architecture skill | preserved |
| `0026` | GPT-5.1 | 01-V1-CANDIDATE | primary | V1, forced | planned |
| `0027` | GPT-5.1 | 02-V2-GRAPH | primary | V2, forced | planned |

## Run-Order Rule

Run in numerical order from a fresh clone and fresh conversation each time.

A failed, incomplete, contaminated, or state-only specimen still consumes its global run ID and must be preserved before any rerun receives a new ID.

Do not add another model block until the GPT-5.1 four-arm EXP-0004 block is preserved and scored.
