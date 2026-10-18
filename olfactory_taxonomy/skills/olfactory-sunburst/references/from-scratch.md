# Build fresh from the final specification

This is the reusable recipe for making the wheel without keeping past experiments. A fresh generation will vary photographically; exact recovery of the accepted images uses the selected original PNGs instead.

## 1. Establish the content

For this wheel, reuse `data/cells.json` and the final editorial data. The source transcription is `data/taxonomy.json`; `data/print-editorial.json` and the three `data/hierarchy-review-*.json` files retain display ordering, curated choices, feel words, material-reference sources and facet notes. `data/cells.json` supplies the final IDs, wording, spans, radii and source identities. The review-named files are the final content specification, not an archive of discarded alternatives.

For a new version, preserve original source identities and make editorial changes separately. Each route should contain a useful comparison, contextually applicable feel words and an identifiable material reference. A single continuation is fine; do not manufacture splits to fill space. Verify substantive new perfumery terms against primary material/manufacturer sources. Do not invent ingredients, unnamed comparison accords or obligatory texture associations.

## 2. Derive the vector layout

Use a 6144-unit square coordinate system with centre `(3072, 3072)` and 9216-pixel screen export. The output-to-vector scale is 1.5. The ring edges are `[220, 700, 1120, 1600, 2260, 2580, 2880]`: broad area, family, character, comparison, feel, reference. The title occupies the central opening.

The current 82 possibilities have equal `360 / 82` angular width. Follow the final clockwise order; merge each parent's span across its own descendants. Identify families by realm plus name. All three outer bands align to the possibility. Counts are `4 + 20 + 48 + 3 × 82 = 318` cells. The original 48-row validation output has 7.5° sectors and is not the current wheel's angular manifest.

Angles run clockwise from twelve o'clock. A point at radius `r`, angle `a` is `(3072 + r sin(a), 3072 − r cos(a))`. Construct an annular sector from its outer start/end points, radial edge, reverse inner arc and closing edge. Set the SVG large-arc flag when a span exceeds 180°. Derive the geometry and clip paths from the same cell extents. The artwork planner emits exact clip path strings for every composition; keep cell boundaries separately so shared route photographs still show ring divisions.

Build named `geometry`, `artwork`, `boundaries`, `labels` and `central-title` groups. Keep text, paths and original photographs editable. `source/master.svg` is the accepted reference/template if matching the final design; it is not required to plan new images.

## 3. Plan all compositions

```sh
python3 scripts/plan_artwork.py
```

`build/artwork-plan.json` contains 130 jobs in generation order: outer routes, character summaries, family summaries, broad-area summaries. Jobs include target IDs/labels, full scent context, descendant comparisons, a self-contained prompt, suggested dimensions and the combined sector clip. The planner verifies that all 318 cells are covered exactly once and that each shared image occupies contiguous cells with a single angular span.

Use the suggested dimensions/aspect ratio as an authoring target, not an assumption about the generator's returned size. Record actual dimensions. The six fresh briefs in `source/generation-briefs.json` replace edit-only prompts that would otherwise require discarded input images. All remaining jobs use their saved standalone prompt. No historical image bundle is needed.

## 4. Generate and review artwork

Use the built-in image-generation tool with the planned prompt and [imagery recipe](background-imagery.md). Generate a representative route and parent first to establish the visual treatment; then complete the plan outside-in. Save candidates at each job's staged image path under `build/regeneration/images/`.

Prefer a few large, tactile recognition cues with calmer supporting material. Keep the defined tip/corner/curl inside the visible tapered crop. Avoid tabletop, decorative props and dense scattered objects. A parent should evoke its children as one interwoven concept, not a series of narrow child bands. Parent job prompts include descendant comparisons; select representative cues rather than trying to depict every literal object.

Keep original PNGs unchanged. Record the actual prompt, generation identity/date, target cells, dimensions, any edit inputs and SHA-256. `source/artwork.json` describes the accepted originals; use a separate candidate manifest for fresh work until it is selected. Do not reuse an old checksum for a new photograph.

## 5. Assemble and label

Clip each image to its combined target sector once. Preserve aspect ratio, use the actual returned dimensions and inspect the crop. For a radial route, rotate its composition around the chart centre so the height follows the radial direction; position/crop its recognition cues within the target wedge. Adjust placement based on the actual silhouette, not solely rectangular source bounds. Do not apply a different crop to each ring of a shared route.

Use [the typography recipe](typography.md). Convert native font/filter distances to SVG units by dividing by 1.5. Fit measured word advances and line boxes within both radial and angular bounds. Outer labels generally run radially; flip those on the left half to remain upright. Broad family headings can run tangentially when they fit, with a radial fallback for narrow cells. Use the current master and style settings as the reference for exact positions and narrow-family exceptions.

Realm headings follow centred circular text paths, with reversed lower arcs. Long realm names use the accepted two-line breaks. Keep consistent ivory lettering, the specified dark glyph edge and glyph-following fades; no label panels. Place the compact descriptive title in the centre. Preserve readable outer text rather than shrinking everything to exaggerate hierarchy.

Update `data/cells.json`, `data/explorer.json` and the artwork manifest if the structure changes. The final master and current data should agree before export.

## 6. Export and check

Follow the supported steps in [the editing guide](../../../docs/EDITING.md): install matching fonts and the pinned Sharp dependency, prepare the original-image SVG, export labelled and image-only PNGs in the browser, then build tiles/AVIF/preview.

Run `python3 scripts/build_layout.py`, `python3 scripts/validate_exhibit.py --originals` and `python3 scripts/plan_artwork.py`. Review the actual whole wheel and native family views; check narrow sectors, pale/busy images, long references, boundaries, continuity, zoom/pan and text toggle. Keep the original full-quality assets distinct from compact delivery files. A fresh generation is not expected to reproduce the previous raster byte-for-byte.
