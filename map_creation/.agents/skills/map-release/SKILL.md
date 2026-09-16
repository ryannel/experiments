---
name: map-release
description: Prepare a reviewed fantasy map for sharing with separate labels, native masters, provenance, public-safe previews and explicit reuse terms.
---

# Prepare a map release

Read [releasing](../../../docs/releasing.md). Confirm the intended audience and deliverables from the saved brief. Do not equate preparing a release with permission to upload or publish it.

Review the exact accepted revision. Check whole-map hierarchy, regional relationships, native structures, all required sites and open issues. User approval and reviewer acceptance remain separate. Do not silently relabel unresolved defects as complete.

Use `mapkit.py export` for a small-map local release. It requires accepted artwork and records the source state and hashes. Keep clean terrain PNG, editable label SVG and a safe JPEG preview. Inspect labels against actual painted anchors before sharing; planned JSON coordinates may be stale. The helper copies existing planned anchors and does not perform collision avoidance.

Prepare labelled versions in an editor if requested, while retaining the clean master. Keep source resolution explicit; any enlarged display or resampled delivery must be described honestly.

Select public files explicitly. Remove private lore from filenames, prompts, logs, provenance, layers and metadata, not just visible labels. Keep exact production records locally, and create a sanitized public summary if they contain sensitive material. Never distribute a working project's entire directory by default.

Use [release-notes.md](../../../templates/release-notes.md) and record actual reuse terms for artwork and external sources. Bundle editable dependencies needed for the promised kind of reuse; a preview alone is not a reconstruction package.

Report saved locations, what was visually checked, native dimensions, known limits and whether publication occurred. For sharing the kit itself, use `scripts/package_experiment.py` and test the extracted standalone folder.
