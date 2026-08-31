# Verification Tooling

Run the local lab verifier before committing research-record changes.

```powershell
py -3 TOOLING/verification/verify_lab.py
```

To verify a GitHub release response, save release JSON and pass it in:

```powershell
gh release view evidence-0001-0015 --json tagName,name,body,assets > release.json
py -3 TOOLING/verification/verify_lab.py --release-json release.json
```

Runs whose `release_tag` is `local-unreleased` only have ignored local archives under `ARCHIVES/local/`. They are hash-recorded evidence but are not durable release assets until uploaded to a GitHub Release or another external artifact store.

The verifier checks:

- no excluded provider references in current text files or paths
- contiguous canonical run IDs
- matching evidence, development-history, experiment, and JSON records
- result asset names and hashes
- canonical skill file hashes
- optional release asset names
