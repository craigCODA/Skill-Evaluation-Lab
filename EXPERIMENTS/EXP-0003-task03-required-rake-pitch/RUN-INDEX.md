# EXP-0003 Run Index

The experiment begins when global run `0020` is cut. These rows define the frozen first-model block; they are not evidence until each run is actually preserved.

| Run | Model | Version | Evidence class | Condition | Status |
| --- | --- | --- | --- | --- | --- |
| `0020` | Grok 4.6 High | 00-SUPPLIED | primary | supplied original, forced | planned |
| `0021` | Grok 4.6 High | NO-SKILL | primary | no explicit architecture skill | planned |
| `0022` | Grok 4.6 High | 01-V1-CANDIDATE | primary | V1, forced | planned |
| `0023` | Grok 4.6 High | 02-V2-GRAPH | primary | V2, forced | planned |

## Run-order rule

Run in numerical order from a fresh clone and fresh conversation each time.

A failed, incomplete, contaminated, or state-only specimen still consumes its global run ID and must be preserved before any rerun receives a new ID.

Do not add another model block until the Grok four-arm EXP-0003 block is scored and there is a reason to spend the additional runs.
