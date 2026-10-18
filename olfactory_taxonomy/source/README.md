# Working source

`master.svg` is the editable 9,216-pixel assembly. Run `python3 scripts/restore_sources.py` from the experiment root to install and verify the original images from the [working-source archive](https://github.com/ryannel/experiments/releases/download/olfactory-atlas-v1/olfactory-atlas-working-source.zip). It installs only missing PNGs and preserves your current SVG and metadata.

All 130 original PNGs are byte-preserved. `artwork.json` records SHA-256 hashes, dimensions, target cells and provenance; `prompts/` contains their generation prompts. Use Baskerville and Avenir for matching typography. Fonts are not included.

Geometry, artwork, boundaries and editable labels are independent SVG layers. No retired prototype builder is required. See the root README for exports and verification.

[Editing guide](../docs/EDITING.md) · [From-scratch recipe](../skills/olfactory-sunburst/references/from-scratch.md)

`generation-briefs.json` supplies self-contained fresh-generation replacements for the six selected images whose original prompts were edits. `python3 scripts/plan_artwork.py` combines these with the other saved prompts and the final geometry to plan every composition.
