# Provenance

## Origin

The taxonomy is the owner's own, started some time before this experiment, after studying published classification guides and teaching material, among them Michael Edwards' Fragrance Wheel and wine aroma wheels that run from general terms at the centre to specific ones at the edge. No single guide was copied. Conversations with an LLM then extended the table with things those guides don't carry: texture and tactile words, and reference materials for each scent. The result was a 48-row table and an unfinished chart, set aside because making the imagery by hand was too slow.

The experiment picked it up on 2026-10-03 with GPT-6 Astra (High) in Codex and its built-in image-generation tool. `data/taxonomy.json` records that 48-row table as it stood at the start of the experiment; everything after it is the experiment's work. Early studies and the unfinished chart are not part of this final-product package.

## Accepted screen exhibit

The owner accepted the spacious Olfactory Atlas on 2026-10-04: a 9,216-pixel wheel with a compact title centre, shorter curved realm headings, 20 families, 48 source characters, 82 scent possibilities and 318 editable labels.

## Language and structure

`data/print-editorial.json` records editorial wording and ordering separately from the source transcription. The three `data/hierarchy-review-*.json` files retain the curated scent possibilities, primary-source material references and facet-specific notes. `data/cells.json` describes the accepted 318 cells. TOBACCO remains scoped by realm.

The source characters expand to 82 useful scent possibilities. Angular widths reflect the number of included possibilities, not measured olfactory distance, prevalence or importance. This is intentionally a selective recognition guide for an amateur. Texture terms suggest optional impressions; reference materials illustrate facets rather than establish the ingredients of a perfume. Review used several AI-agent perspectives and visual checks; it does not constitute independent human-perfumer certification or experimental sensory validation.

## Photographic assets

All 130 selected compositions were generated or edited by GPT-6 Astra through Codex's built-in image-generation tool (GPT Image 2) during the experiment. No alternative image-generation API workflow was used. Parent images mix the cues from their descendants; a continuous photograph spans each outer scent route. Ice, mist and related visual cues are sensory metaphors. Botanical and chemical identities are illustrative, not certified specimen depictions.

`source/artwork.json` records each selected original's identity, original project path, generation identifier, date, dimensions, exact prompt path, assigned cells and SHA-256 checksum. `source/prompts/` contains those prompts. Historical reference-input paths document ancestry only. Fresh-generation briefs for the six selected edit results are provided in `source/generation-briefs.json`, so new images can be planned without earlier inputs. Selected originals are preserved byte-for-byte as PNGs in the downloadable working-source archive. The assembly uses relative paths and separately editable vector labels, boundaries and geometry.

Baskerville and Avenir are system fonts referenced by the authoring master. Font files are not distributed. Raster exhibit tiles include the approved lettering and do not require visitors to install either font.

## Delivery and quality

The approved screen render was rasterized in the browser using the project's established image delivery copies and vector glyph filters. A lossless copy of this flattened PNG is included in the GitHub release. It is not described as an uncompressed-source photographic master: `source/master.svg` with the original PNG assets is the full-quality working version.

The public viewer uses two pre-rendered WebP tile pyramids at quality 94 (512-pixel tiles, one-pixel overlap), preserving the approved labelled and image-only views. The standalone AVIF uses quality 65, 4:4:4 chroma and the full 9,216 × 9,216 dimensions. It was selected over a larger WebP after checking lettering and photographic detail in rendered crops. It is a compact derivative, not a replacement for either the source photographs or the approved PNG.

The accepted centre uses radius 220 in a 6,144-unit coordinate system. Four realm images extend inward with their original pixel mapping; other cell geometry and image crops remain unchanged. Realm headings remain 96 physical pixels, with two-line arcs for the long names. Source style settings and fit records are retained. Screen checks are not a production-print verification.

## Cleanup and preservation

The package retains the accepted `source/master.svg`, final content data, selected prompts, self-contained generation briefs, reusable skills and the supported export/validation tools. Historical artwork variants, prototype snapshots and process archives are excluded. The checked-in files contain no dependency on the original workstation, temporary browser downloads or another experiment. Source archives and release checksums preserve the original selected artwork for future editing.

## Full exploration tool — 2026-10-18

The standalone exhibit now adapts the full scent exploration experience from the bottom of the owner’s article at https://ryannel.dev/projects/olfactory-atlas/. It offers free zoom/pan and question-led selection with highlighted routes, examples, breadcrumbs and study references; it does not include the article’s scripted Citrus tour. The implementation lives in this repo and derives its 154 interactive nodes from the final cell and editorial data. It uses the existing tile pyramids and preserves the accepted photographic artwork and typography. The article is linked as the narrative account; this repository holds the finished product and its authoring specification.
