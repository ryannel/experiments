# Assembly and export

The final screen edition is `source/master.svg`, displayed at 9216 × 9216 with viewBox 0 0 6144 6144. `data/cells.json` records its 318 cells and exact extents. Ring edges are `[220, 700, 1120, 1600, 2260, 2580, 2880]`. The title opening has radius 220. Photographs, sector geometry, boundaries and editable text stay separate.

To create fresh artwork and construct the wheel from the final specification, follow [the from-scratch recipe](from-scratch.md). `python3 scripts/plan_artwork.py` produces 130 self-contained jobs, with full scent context and exact combined clips. It needs no original pictures or prior drafts.

To edit the accepted work, use the current master and update relevant metadata. `python3 scripts/restore_sources.py` safely installs the 130 selected original PNGs without replacing the current SVG or metadata. For a new image, record its full ancestral scent path, target cells, original asset and exact prompt. Review its actual wedge crop before selection.

`npm run prepare:render` embeds original PNGs without recompression and prepares a browser export. With Baskerville and Avenir installed, export labelled and image-only PNGs to `build/labels.png` and `build/image.png`. `npm run build:tiles` generates the two tile pyramids, compact AVIF and preview. `npm run build` updates only the viewer HTML.

Validate taxonomy, cells, local links, complete tile coverage, image signatures and original checksums using the README commands. Inspect actual browser output at overview and native detail: long labels, pale/busy imagery, narrow families, family focus, zoom/pan and text toggle. These are screen checks, not print verification.

Keep the final product, current generation prompts/briefs and reusable skills in the repo. Full-quality selected PNGs and the approved flattened PNG remain separately downloadable to keep clones manageable. Do not add historical variants, prototype snapshots or process archives. Publish only when the user requests it.

The finished exploration tool supports free navigation and question-led scent choices, without a scripted tour. Its hierarchy is derived from the final repo data by scripts/exploration-data.cjs; templates/explorer.html and templates/viewer.js own the interface. Rebuild with npm run build after changing content or interaction, without regenerating image tiles. Keep the article linked as the narrative, and the repo as the product/source of truth.
