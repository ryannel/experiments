# Olfactory Atlas

Read README.md and PROVENANCE.md before editing. This is a standalone exhibit inside a collection; scope changes to this folder.

- The accepted assembly is `source/master.svg`; keep its photographic artwork, exact geometry, boundaries and editable text separate. Do not rebuild from archived prototypes.
- Preserve the 48-row transcription in `data/taxonomy.json`. Deliberate editorial changes belong in the separate editorial data and `data/cells.json`. Scope family identities by realm; TOBACCO occurs twice.
- Use `skills/olfactory-sunburst/SKILL.md` for design work and keep it current with accepted decisions.
- `source/images/` contains full-quality original PNGs, installed from the GitHub working-source archive. Never overwrite them with export encodings. Update artwork hashes only for intentional source revisions.
- New photographic assets use the built-in image-generation tool; retain the originals, prompts and provenance.
- The viewer and AVIF are delivery artifacts. Keep them self-contained, relative-path based and usable after cloning without Node, fonts, external CDNs or API keys.
- For image/label changes, prepare and render the master, rebuild both tile modes as needed, then inspect actual browser output. Match Baskerville and Avenir for exports; do not silently accept changed font metrics.
- Run `python3 scripts/build_layout.py` and `python3 scripts/validate_exhibit.py`. Use `--originals` when source assets are installed. Check the landing page, family zoom, pan and image-only mode after viewer changes.
- Large authoring rasters, dependencies, retired experiments and temporary renders belong under ignored `build/`; original assets are distributed through the working-source release rather than Git history.
- Do not claim scientific completeness, professional certification or production-print readiness. Do not publish new releases or push merely because files are prepared; explicit user authorization is required.
