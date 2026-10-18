# Returning to the project

Start with the [project skill](../skills/olfactory-sunburst/SKILL.md), then use this guide for the particular change. To generate a fresh wheel from the final specification, follow the [from-scratch recipe](../skills/olfactory-sunburst/references/from-scratch.md) and run `python3 scripts/plan_artwork.py`. It needs no previous images.

## Restore original images safely

From the experiment root:

```sh
python3 scripts/restore_sources.py
python3 scripts/validate_exhibit.py --originals
```

The restore command downloads the pinned working-source archive and verifies its checksum, then installs only missing original PNGs. It does **not** extract the archive over your SVG, prompts or metadata. It preserves matching existing images and refuses to overwrite a changed one. To use an existing download:

```sh
python3 scripts/restore_sources.py --archive /path/to/olfactory-atlas-working-source.zip
```

Matching Baskerville and Avenir fonts are required for matching new exports. They are not bundled; the existing viewer does not need them.

## Which file to change

| Change | Edit | Keep aligned |
| --- | --- | --- |
| A label or line break | The matching `data-cell` text element in `source/master.svg` | `data/cells.json` text; typography fit/readability |
| Type size, contrast, arc placement | SVG text/filter/path definitions | `data/spacious-typography.json` and relevant skill reference |
| Replace a photograph | Original PNG and its SVG image placement | `source/artwork.json`: path, dimensions, SHA-256, prompt, generation identity and target cells |
| Reframe an existing image | Image rectangle/transform within the SVG sector clip | Existing source image remains unchanged; inspect its defining recognition cue |
| Geometry or a route's structure | SVG geometry, clips, boundaries and labels together | Cell IDs/extents in `data/cells.json`; family extents in `data/explorer.json`; related editorial data |
| Landing page | `index.html` | Its links and preview |
| Exploration layout, zoom/pan and question interaction | `templates/explorer.html` and `templates/viewer.js` | Run `npm run build` to regenerate `exhibit/index.html` and `exhibit/viewer.js` |
| Scent choices, hints and reference details | `data/cells.json`, final editorial data and `scripts/exploration-data.cjs` | Build the viewer; all choices must resolve to the correct realm-scoped parents |

`data/taxonomy.json` is the original 48-row transcription. Preserve it when revising the display; editorial changes belong in the separate editorial files. Family names are scoped by realm.

The SVG has independent `geometry`, `artwork`, `boundaries`, `labels` and `central-title` groups. Realm names use circular text paths; the two longest names have two lines. Individual outer routes share a continuous photograph across comparison, feel and reference bands.

For a label-only change, preserve the full wording in `data/cells.json` while using separate SVG spans/text paths to wrap it. The validator compares normalized rendered text. If the source SVG `data-source` attribute repeats the displayed wording, update it as well. Content changes affecting references should also update the curated possibility and its source/facet note.

For an intentional image edit, retain the new original and calculate its SHA-256 with `shasum -a 256 source/images/NAME.png` (or Python's hashlib), then update its manifest entry. The restore command and export preparation will correctly refuse an unexpected checksum change. The old release is a backup of v1, not a replacement for your newer work.

## Export the revised wheel

```sh
npm ci
npm run prepare:render
python3 -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000/build/render.html` with the matching fonts installed. Export the labelled and image-only PNGs. Save the downloads as `build/labels.png` and `build/image.png`, then run:

```sh
npm run build:tiles
python3 scripts/build_layout.py
python3 scripts/validate_exhibit.py --originals
python3 scripts/plan_artwork.py
```

This rebuilds the tiles, AVIF and preview. The original image pixels remain in `source/images/` and the editable lettering remains in the SVG. Preparing the original-image render uses significant memory; visitors can simply use the checked-in tiles.

Review the actual viewer: whole wheel for balance; native detail for pale/busy images, long labels and narrow families. Check family selection, zoom/pan and image-only mode after interface changes. Mathematical fit and structural validation do not establish visual legibility.

## Save the work

Commit source SVG, manifests, prompts, data and refreshed exhibit together. Original PNGs are ignored by Git: a new or modified image must also be backed up in a new checksum-verified source archive before publishing that revision. Document the change in provenance and retain v1 as the accepted baseline. A text/geometry-only edit does not require replacing the original PNG archive. Publishing is a separate, explicit action.

## Exploration and article

The standalone tool adapts the full exploration experience at the bottom of the ryannel.dev article; it has no scripted-tour mode. This repo owns its renderer, question logic and data generation. The article remains the linked narrative; the landing page links the finished product, skill, prompts and source. No runtime/build access to the ryannel.dev checkout is required.

`npm run build` derives 154 interactive nodes (4 realms, 20 families, 48 characters and 82 comparisons) from the final cell/editorial data. Each comparison combines its feel and reference bands for selection, preserving the photographic route. Stable cell IDs identify selections, including the two Tobacco branches. The fast tile cache remains independent of the question panel.

The responsive viewer keeps the illustration above independently scrolling questions on phones and beside them in landscape. Secondary controls live in Tools. Wheel only hides the panel; Show questions restores it without resetting the scent path. Test at 320px and 390px portrait, short landscape and tablet widths, plus desktop. The build adds a content hash to the viewer script URL so updated interactions are loaded alongside updated markup.
