# Finding a visual language

Use the same small scene across candidate styles: a wooded rise, bridge, cultivated edge and modest settlement. Hold geography and content constant so the comparison is about visual treatment. Try two or three plausible directions within the agreed budget, such as restrained ink and wash, layered painterly relief, or clear graphic symbols. These are options, not a required aesthetic.

Compare at both intended overview size and 100% native pixels:

- Can someone distinguish inhabited places, forest, high ground and water immediately?
- Do house roofs and tree crowns share a camera angle, light direction and scale language?
- Are ordinary terrain textures quiet enough for landmarks and labels?
- Does a village remain a village when shrunk, and a capital have a recognizable silhouette?
- Can a neighbouring region be painted without a noticeable shift in palette or brushwork?

Record the selected reference's file and hash, medium, palette, projection/camera, light, edge treatment, detail density, icon exaggeration and rejected traits in [style.json](../templates/style.json). Selection is a decision, not a claim that all content in a trial is correct.

## Build only the assets the pilot needs

First decide whether you are painting terrain directly, assembling sprites, or using a hybrid. Direct atlas painting needs structural guides and references; it does not require a continent-sized sprite collection. A local village assembly benefits from individual buildings and plants with real alpha, ground anchors and footprints.

For a reusable asset, record native dimensions, occupied bounds, doorway/root anchor, footprint, intended placement size, lighting and review status. Request transparent output when needed, then inspect the alpha channel; a painted checkerboard is not transparency. Review the asset against actual ground beside an accepted reference building. Avoid mirroring or rotating baked lighting.

Start with a few useful roles: mature broad crown, narrow evergreen, younger edge tree, ordinary home, shared store, local landmark and one ground treatment. Expand after the integrated pilot passes. Distinct filenames do not guarantee distinct silhouettes. Keep rejected sources out of default selection while retaining inputs needed to reconstruct earlier work.

## Prompt starter

Use the user's own references and choices. The [prompt library](prompts.md) supplies reusable structures for style trials, generation, extension and repair. Record the exact submitted text; a later summary is not the original prompt. Never promise that a style reference or preservation instruction forces exact output geometry.
