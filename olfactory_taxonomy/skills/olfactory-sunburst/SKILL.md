---
name: olfactory-sunburst
description: Build or revise the Olfactory Atlas photographic scent wheel from its taxonomy, editorial data and generation briefs, with exact vector geometry, editable labels and a portable exhibit.
---

# Olfactory Atlas

Work from this standalone project root. Read README.md, PROVENANCE.md and AGENTS.md. This skill covers both creating fresh artwork from the final specification and editing the accepted wheel.

The goal is useful scent descriptions for an amateur: broad impression → family → character → familiar comparison, with optional feel words and material references. Leading recognition prompts and a selective hierarchy are intentional. Learners can stop at any tier. A reference illustrates a scent facet, not an ingredient identified in a perfume. Longevity is outside scope.

## Choose the starting point

- **Edit the accepted work:** `source/master.svg` is the assembly. Restore original PNGs with `python3 scripts/restore_sources.py`; it preserves current SVG and metadata edits. Follow [the editing guide](../../docs/EDITING.md).
- **Start fresh from the final design:** follow [the from-scratch recipe](references/from-scratch.md). Run `python3 scripts/plan_artwork.py` to create 130 self-contained generation jobs with scent context, target cells and exact sector clips. This requires neither original pictures nor earlier drafts.

The final content is 4 realms, 20 realm-scoped families, 48 source characters, 82 scent possibilities and 318 cell labels. `data/taxonomy.json` preserves the source transcription. The editorial overlay and three `data/hierarchy-review-*.json` files define the selected possibilities and material references; `data/cells.json` is the final cell specification. Scope TOBACCO by realm. Sector width represents included possibilities, not measured scent distance or prevalence.

Read [assembly guidance](references/assembly-plan.md) for geometry, layers and export; [imagery guidance](references/background-imagery.md) before generating; and [typography guidance](references/typography.md) before placing lettering. Current settings and the editable master hold exact accepted values.

Build imagery from the outer scent routes inward. One photograph continues through a route's comparison, feel and reference bands. Parents mix representative cues from their descendants organically, without mirroring the child columns. Compose for the actual wedge: generous partial leaf tips, gum corners and petal curls may read better than tiny complete objects.

Use built-in image generation for photographic creation and edits. Keep original PNGs, prompts, dimensions, generation IDs, assigned cells and SHA-256 in the artwork manifest. `source/prompts/` preserves the selected original calls; six edit-only calls have self-contained fresh-generation replacements in `source/generation-briefs.json`. Never replace an original with its lossy export. Stage fresh generations under `build/regeneration/` until reviewed.

Keep photography, exact geometry, boundaries and editable lettering in separate SVG layers. Review actual crops with and without labels, at overview and native reading size, including narrow families and long text over pale/busy imagery. Fit calculations alone do not establish readability.

Run the documented validators, restoration tests when changing source handling, and the artwork planner when changing generation inputs. Rebuild delivery tiles after artwork or lettering changes. The exhibit must work after cloning without custom fonts, Node or online services; those are authoring requirements only. Publishing needs explicit user authorization. Screen review does not establish print readiness.

For small screens, keep the wheel visible while the question panel scrolls independently. Keep the primary toolbar compact, put secondary actions in Tools, and offer a reversible Wheel only / Show questions view. Preserve the scent path and manually panned camera when resizing or toggling panels. Use generous touch targets and check narrow portrait, short landscape and tablet layouts in the actual browser, including question navigation and image-only mode.
