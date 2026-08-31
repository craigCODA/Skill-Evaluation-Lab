# Release Evidence

Binary evidence for canonical runs `0001` through `0015` is stored on this repository's release tag `evidence-0001-0015`.

Runs `0016` through `0019` are preserved as checked-in evidence plus local-only archives under `ARCHIVES/local/`. Those ZIPs are intentionally not committed to normal Git history and are not retrievable from a fresh clone until published to a durable external artifact store.

The release includes one result package per canonical run plus `SHA256SUMS.txt`.

Raw import packages are not part of the current public release surface unless `CURRENT-STATE.md` explicitly says otherwise.
