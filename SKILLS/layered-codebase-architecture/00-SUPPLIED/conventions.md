# Conventions overlay

Default TypeScript / Vue spelling. Laws live in [SKILL.md](SKILL.md). If a convention here fights a law, the law wins and this overlay should be fixed.

If the repo under edit has `.cursor/architecture-conventions.md`, that file wins. Match siblings in the same folder when both overlays are silent.

## Case by kind of file

| Kind | Case | Example |
| --- | --- | --- |
| Layer and capability folders | `PascalCase`; adapters may hyphenate | `Patients`, `API-Patients` |
| Adapter entry file | kebab-case of the folder name | `api-patients.ts`, `reporting-queryexecutor.ts` |
| Domain modules, types, Vue components | `PascalCase` | `Patient.ts`, `PatientList.vue` |
| Route folders | lowercase noun | `pages/patients/` |
| UI state modules (composables) | `use` + noun | `usePatients.ts` |
| Tests | next to the module, `*.test.ts` | `PatientKeys.test.ts` |

## UI tree

- Routes: `pages/{noun}/` then job (`details`, `index`).
- Components: `components/{Noun}/` then widget (`List`, `Form`).
- Composables: `use{Noun}` / `use{Noun}{Job}`.

## Adapter tree

- Folder: `{Noun}-{Role}` with a role prefix that names the edge (`API-`, `Reporting-`, `Auditing-`).
- Entry file: kebab-case of that folder.
- One-job helpers inside the adapter may be verb files (`transformation.ts`, `user-lookup.ts`).
