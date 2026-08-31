# EXP-0002 Run Index

The experiment begins when global run `0016` is cut. These rows define the frozen first-model block; they are not evidence until each run is actually preserved.

| Run | Model | Version | Evidence class | Condition | Status |
| --- | --- | --- | --- | --- | --- |
| `0016` | Grok 4.6 High | 00-SUPPLIED | primary | supplied original, forced | preserved |
| `0017` | Grok 4.6 High | NO-SKILL | primary | no explicit architecture skill | preserved |
| `0018` | Grok 4.6 High | 01-V1-CANDIDATE | primary | V1, forced | preserved |
| `0019` | Grok 4.6 High | 02-V2-GRAPH | primary | V2, forced | preserved |

## Run-order rule

Run in numerical order from a fresh clone and fresh conversation each time.

A failed, incomplete, contaminated, or state-only specimen still consumes its global run ID and must be preserved before any rerun receives a new ID.

Do not add another model block until the Grok four-arm holdout is scored and there is a reason to spend the additional runs.
