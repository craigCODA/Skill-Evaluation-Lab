# Release Evidence

Binary evidence for canonical runs `0001` through `0015` is stored on this repository's release tag `evidence-0001-0015`.

The release includes one result package per canonical run plus `SHA256SUMS.txt`.

Runs `0016` through `0027` currently have local-only ZIP archives under `ARCHIVES/local/`. Their archive names and SHA-256 hashes are recorded in canonical evidence, but those ZIPs are ignored by Git and are not durable release assets until uploaded to a GitHub Release or another external artifact store.

Raw import packages are not part of the current public release surface unless `CURRENT-STATE.md` explicitly says otherwise.
