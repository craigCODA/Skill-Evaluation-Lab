# Workplace Lifecycle Checkpoints

These checkpoints capture issues that have repeated across the Shingle workplace runs. Run them at the phase boundary instead of waiting for a failed preserve/cleanup attempt to reveal the problem.

The script is read-only. It does not clone, archive, delete, move, edit skills, or touch `ACTIVE/`.

## Repeated Issues

- Cursor can keep `ACTIVE/ShingleFile-main` locked after a run completes.
- PowerShell `Move-Item` can partially move a checkout that contains hidden `.git` metadata.
- Cursor skill retirement must stay on the same drive when using `.NET Directory.Move`.
- Empty command-output captures, especially `git diff --check`, must still become explicit evidence files.
- `diff.patch` only captures tracked changes; untracked files must be listed and preserved through the full archive.
- Cursor can leave multiple project/transcript folders for the same Active path; choose the current trace before preservation.
- `ARCHIVES/local/*.zip` is local-only evidence until published to durable artifact storage.

## Checkpoints

Before opening Cursor for a run:

```powershell
powershell -ExecutionPolicy Bypass -File TOOLING\workplace\checkpoints.ps1 -Phase FreshReady -RunId 0021 -SkillVersion NO-SKILL
```

After the model finishes, before any cleanup:

```powershell
powershell -ExecutionPolicy Bypass -File TOOLING\workplace\checkpoints.ps1 -Phase PreserveReady -RunId 0021 -SkillVersion NO-SKILL
```

Before clearing Active after evidence and archive are preserved:

```powershell
powershell -ExecutionPolicy Bypass -File TOOLING\workplace\checkpoints.ps1 -Phase CleanupReady -RunId 0021 -SkillVersion NO-SKILL
```

After fresh-cloning the next arm, run `FreshReady` again with the next run ID and expected skill condition.

## Cleanup Rules

Archive first, then clear Active.

Do not use `Move-Item` for a complete Active checkout. Close the Cursor window for `ShingleFile-main`, then move the directory with `[System.IO.Directory]::Move()` to an ignored same-drive location under `ARCHIVES/local/`.

Do not move `%USERPROFILE%/.cursor/skills-cursor/layered-codebase-architecture` to `D:` with `[System.IO.Directory]::Move()`. Move it to a same-drive retired folder under `%USERPROFILE%/.cursor/retired-skills-cursor/`, or remove it only when the run plan explicitly allows deletion.

For no-skill arms, the global skill folder must be absent before Cursor opens.

For skill arms, the global skill folder must match the selected frozen artifact hashes before Cursor opens.
