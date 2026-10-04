# Accepted assembly and rebuild

The accepted screen edition is `source/master.svg`, displayed at 9216 × 9216 with viewBox 0 0 6144 6144. `data/cells.json` records its 318 cells and exact angular/radial extents. The title centre has radius 220. Source geometry and lettering remain separate from generated photographs.

For existing edits, work directly in the master and update relevant content/asset metadata. For new images, record the full ancestral scent path, target cell IDs, original asset and exact prompt. Review the actual crop; source image aspect ratio alone does not predict whether a cue will survive in a narrow wedge.

The working-source archive installs 130 original PNGs. `npm run prepare:render` embeds them without recompression and prepares a browser export. With the matching fonts installed, export labelled and image-only PNGs to `build/labels.png` and `build/image.png`. `npm run build:tiles` generates the two tile pyramids, compact AVIF and overview image. `npm run build` updates just the viewer HTML.

Validate taxonomy, cells, local links, complete tile coverage, image signatures and optional original checksums using the README commands. Inspect the actual landing page and viewer: full wheel, inner headings, longest references and light/dark imagery; also check family focus, zoom/pan and text toggle. Screen review is not print verification.

Keep original assets and full-resolution PNG exports in release archives; keep the compact exhibit in Git. Retired proofs are development history under ignored build/development-archive, not runtime requirements. Publish only when the user requests it.
