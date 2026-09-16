# Tool reference

Run `python scripts/mapkit.py --help` from the experiment root. All commands are local; none calls an image API, commits files or publishes. Use one writer at a time: this small helper does not provide multi-process locking.

| Command | Purpose |
| --- | --- |
| `new --output work/NAME [--world FILE] [--base PNG]` | Create a new project from the example or a supplied model; refuse an existing output. Base image must match model dimensions. |
| `validate WORLD_JSON` | Check structural types, dimensions, IDs, references, coordinates and basic river graph consistency. |
| `guide PROJECT` | Write a labelled schematic JPEG preview, at most 1600 px in each dimension. |
| `prepare PROJECT ID --rect X Y W H [--mask PNG]` | Freeze current input hashes, target rectangle, prior pixels, guide, context and optional local L-mode mask. IDs cannot be reused. |
| `ingest PROJECT ID --image PNG --provenance JSON` | Retain an opaque RGB/RGBA lossless returned PNG; require exact target dimensions and provenance; make the integrated candidate. |
| `inspect PROJECT ID` | Write the assembled overview and overlapping native crops covering the region plus a 96 px collar; create review.json if missing. |
| `accept PROJECT ID [--review FILE]` | Verify freshness, retained hashes and completed visual-review records, then atomically replace the project state file. |
| `export PROJECT RELEASE [--allow-partial]` | Write clean PNG, preview, editable label SVG and manifest from the accepted state. Partial coverage needs the explicit flag. |

## Project layout

```text
work/my-world/
  world.json                 Intended geography and public site register
  style.json                 Style contract and guide colors
  planning/                  Brief, societies, decisions and unresolved work
  assets/masters/            Imported source art
  iterations/CANDIDATE/      Prepared inputs, exact output, provenance and review
  metadata/state.json        Current accepted patch list and revision
  previews/                  Safe schematic overview
  private/                   Ignored, never part of public packaging
  releases/RELEASE/          Explicit local deliverables
```

Candidate IDs allow lowercase letters, digits, underscores and hyphens. Use `pilot-v1`, `pilot-v2`, `ford-repair-v1`, etc. Prepared inputs are immutable. Each candidate retains snapshots of world.json, style.json and the style reference files, alongside their hashes. Put reference paths in `style.reference_files` as project-relative strings (for example `assets/masters/style-selected-v1.png`). If geography, style or accepted state changes, prepare a new candidate; the old one becomes stale. The submitted prompt may expand on prompt.md; save that final prompt in provenance.json without changing the sealed preparation.

Accepted reviews are retained with their own hashes and evidence file hashes. Acceptance requires `pass` and nonempty observations/evidence for seven checks: style, geography, routes, structures, joins, required sites and mask perimeter. If a check is inapplicable, explain why in its observation and point to the inspected image; do not leave it blank. Required sites need painted, moved (with destination) or deferred (with reason) records. Deferral is explicit accounting, not evidence of release completeness. Open candidate defects must be resolved; model limitations stay documented in planning and release notes.

Evidence paths are relative to the working project, for example `iterations/pilot-v1/evidence/native-204-124.png`. Add whole-route crops when the supplied target crops are insufficient. The tool cannot establish visual truth, detect fabricated reviews or replace user judgment.

## Refinement masks

Use a native grayscale PNG exactly as large as the local rectangle. Black preserves prior pixels, white takes generated pixels, intermediate values blend. Ingestion retains the model's full returned PNG and the separate composite. This guarantees exact preservation where the mask is black; it does not guarantee the mask boundary avoids a shifted tree or bank. Review the whole perimeter. Do not use broad feathering across incompatible roof or channel geometry.

## Recovery

There is no destructive cleanup command. State points only to accepted inputs; unaccepted attempts remain on disk. Retrying an accepted ID leaves state unchanged. A failed ingestion without ingested.json can be retried; once ingested, use a new candidate for changes. Keep backups/version control for work you care about. The helper does not replace a full transactional database, automatically roll back versions or maintain remote backups.

For publication, use the explicit kit packager, or select artwork release files manually. Never ZIP an entire working world with private writing and production prompts.
