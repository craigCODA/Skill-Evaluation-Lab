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

The verifier checks:

- no excluded provider references in current text files or paths
- contiguous canonical run IDs
- matching evidence, development-history, experiment, and JSON records
- result asset names and hashes
- canonical skill file hashes
- optional release asset names
