# EXP-0002 Run Index

The experiment begins when global run `0016` is cut. These rows define the frozen three-model block; they are not evidence until each run is actually preserved.

| Run | Model | Version | Evidence class | Condition | Status |
| --- | --- | --- | --- | --- | --- |
| `0016` | Grok 4.6 High | NO-SKILL | primary | no explicit architecture skill | planned |
| `0017` | Grok 4.6 High | 00-SUPPLIED | primary | supplied original, forced | planned |
| `0018` | Grok 4.6 High | 01-V1-CANDIDATE | primary | V1, forced | planned |
| `0019` | Grok 4.6 High | 02-V2-GRAPH | primary | V2, forced | planned |
| `0020` | Kimi K2.7 Code | NO-SKILL | primary | no explicit architecture skill | planned |
| `0021` | Kimi K2.7 Code | 00-SUPPLIED | primary | supplied original, forced | planned |
| `0022` | Kimi K2.7 Code | 01-V1-CANDIDATE | primary | V1, forced | planned |
| `0023` | Kimi K2.7 Code | 02-V2-GRAPH | primary | V2, forced | planned |
| `0024` | GPT-5.1 | NO-SKILL | primary | no explicit architecture skill | planned |
| `0025` | GPT-5.1 | 00-SUPPLIED | primary | supplied original, forced | planned |
| `0026` | GPT-5.1 | 01-V1-CANDIDATE | primary | V1, forced | planned |
| `0027` | GPT-5.1 | 02-V2-GRAPH | primary | V2, forced | planned |

## Run-order rule

Run in numerical order from a fresh clone and fresh conversation each time.

A failed, incomplete, contaminated, or state-only specimen still consumes its global run ID and must be preserved before any rerun receives a new ID.

The full three-model holdout may be run in one lifecycle block once the workplace preflight is clean.
