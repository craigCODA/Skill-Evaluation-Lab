# EXP-0004 Run Index

The experiment begins when global run `0024` is cut. These rows define the frozen first-model GPT-5.1 block and the second-model Opus block; they are not evidence until each run is actually preserved.

| Run | Model | Version | Evidence class | Condition | Status |
| --- | --- | --- | --- | --- | --- |
| `0024` | GPT-5.1 | 00-SUPPLIED | primary | supplied original, forced | preserved |
| `0025` | GPT-5.1 | NO-SKILL | primary | no explicit architecture skill | preserved |
| `0026` | GPT-5.1 | 01-V1-CANDIDATE | primary | V1, forced | preserved |
| `0027` | GPT-5.1 | 02-V2-GRAPH | primary | V2, forced | preserved |
| `0028` | Opus | 00-SUPPLIED | primary | supplied original, forced | preserved |
| `0029` | Opus | NO-SKILL | primary | no explicit architecture skill | planned |
| `0030` | Opus | 01-V1-CANDIDATE | primary | V1, forced | planned |
| `0031` | Opus | 02-V2-GRAPH | primary | V2, forced | planned |

## Run-Order Rule

Run in numerical order from a fresh clone and fresh conversation each time.

A failed, incomplete, contaminated, or state-only specimen still consumes its global run ID and must be preserved before any rerun receives a new ID.

Do not add another model block until the GPT-5.1 four-arm EXP-0004 block is preserved and scored.
