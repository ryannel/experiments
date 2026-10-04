# Provenance

## Accepted screen exhibit

The user accepted the spacious Olfactory Atlas on 2026-10-04: a 9,216-pixel wheel with a compact title centre, shorter curved realm headings, 20 families, 48 source characters, 82 scent possibilities and 318 editable labels. The four broad areas, family memberships and image compositions come from the iterative olfactory-taxonomy experiment.

`data/taxonomy.json` preserves the original 48-row table transcription. The original reference table and early Citrus study were part of the development process and remain in the earlier Git history/local development archive; neither is needed to operate this exhibit. Their third-party image rights were not documented. They are not republished in the cleaned exhibit.

## Language and structure

`data/print-editorial.json` records editorial wording and ordering separately from the source transcription. The three `data/hierarchy-review-*.json` files retain the curated scent possibilities, primary-source material references and facet-specific notes. `data/cells.json` describes the accepted 318 cells. TOBACCO remains scoped by realm.

The source characters expand to 82 useful scent possibilities. Angular widths reflect the number of included possibilities, not measured olfactory distance, prevalence or importance. This is intentionally a selective recognition guide for an amateur. Texture terms suggest optional impressions; reference materials illustrate facets rather than establish the ingredients of a perfume. Review used several AI-agent perspectives and visual checks; it does not constitute independent human-perfumer certification or experimental sensory validation.

## Photographic assets

All 130 selected compositions were generated or edited with the built-in OpenAI image-generation tool during the experiment. No alternative image-generation API workflow was used. Parent images mix the cues from their descendants; a continuous photograph spans each outer scent route. Ice, mist and related visual cues are sensory metaphors. Botanical and chemical identities are illustrative, not certified specimen depictions.

`source/artwork.json` records each selected original's identity, original project path, generation identifier, date, dimensions, exact prompt path, assigned cells and SHA-256 checksum. `source/prompts/` contains those prompts. Historical reference-input paths document ancestry; superseded inputs remain in the local development archive and are not required to use the selected original. Selected originals are preserved byte-for-byte as PNGs in the downloadable working-source archive. The assembly uses relative paths and separately editable vector labels, boundaries and geometry.

Baskerville and Avenir are system fonts referenced by the authoring master. Font files are not distributed. Raster exhibit tiles include the approved lettering and do not require visitors to install either font.

## Delivery and quality

The approved screen render was rasterized in the browser using the project's established image delivery copies and vector glyph filters. A lossless copy of this flattened PNG is included in the GitHub release. It is not described as an uncompressed-source photographic master: `source/master.svg` with the original PNG assets is the full-quality working version.

The public viewer uses two pre-rendered WebP tile pyramids at quality 94 (512-pixel tiles, one-pixel overlap), preserving the approved labelled and image-only views. The standalone AVIF uses quality 65, 4:4:4 chroma and the full 9,216 × 9,216 dimensions. It was selected over a larger WebP after checking lettering and photographic detail in rendered crops. It is a compact derivative, not a replacement for either the source photographs or the approved PNG.

The accepted centre uses radius 220 in a 6,144-unit coordinate system. Four realm images extend inward with their original pixel mapping; other cell geometry and image crops remain unchanged. Realm headings remain 96 physical pixels, with two-line arcs for the long names. Source style settings and fit records are retained. Screen checks are not a production-print verification.

## Cleanup and preservation

The exhibit consolidates many prototype builders into the accepted `source/master.svg`, a portable tile/export builder and a validator. Superseded drafts, assets and development documents are archived locally under ignored `build/development-archive/`; visitors do not need them. The checked-in files contain no dependency on the original workstation, temporary browser downloads or another experiment. Source archives and release checksums preserve the original selected artwork for future editing.
