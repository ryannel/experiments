# Growing beyond the demo

The bundled helper composes the full small-map canvas in memory and enforces a **16,000,000-pixel** limit. It is not the production renderer used for the showcase and is not suitable for large atlas masters. Do not remove the limit and call that scaling.

For a larger implementation, keep one global pixel coordinate system and immutable accepted patches. Render local context from a baseline plus intersecting patches, with bounded caches. Retain exact source masters, per-region prompts, masks, origins and decisions. Choose crop sizes from measured tool support and needed detail, not from an arbitrary tile count.

Use overlapping regions so painters can see accepted neighbours. Context overlap and output ownership are different: copying a neighbour into a prompt does not force preservation. Inspect every affected side, including east and south on backfills, and inspect the final seam and its surrounding terrain. Feathering is useful on compatible ground; averaging a bridge, roof or riverbank creates ghosts. Repair structural seams in a coherent corridor or use a deliberate hard boundary along compatible features.

A large continent should not contain one landmark per rectangle. Start from catchments, journeys and territorial needs; choose painting rectangles afterward. Measure both painted area and the content ledger. A fully covered canvas can still omit a faction's capital.

Native dimensions are a budget for detail. Enlarging a finished small image does not create resolved houses or trees. If a model returns a smaller size, retain it honestly, prepare smaller native regions or change the release size. Never stretch a region into a larger slot without documenting a deliberate change in representation.

A 12,000 × 8,000 RGBA buffer alone is about 366 MiB; multiple layers and copies multiply that. A tiled viewer built from one huge in-memory render does not demonstrate bounded-memory rendering. Test actual peak memory, reconstruction and local update behavior before promising a larger atlas.

Present JPEG overviews no wider than 1600 pixels and native local crops. Keep full lossless masters and editable SVG/Blender layers on disk. Generate a zoom pyramid only when needed, from accepted native artwork, with explicit public data selection.
