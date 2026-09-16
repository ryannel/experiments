---
name: map-director
description: Coordinate a complete fantasy map project, including scope, style exploration, world planning, regional painting and delivery. Use for new maps or resuming a multi-stage map project.
---

# Direct a map project

Locate this kit's root by walking three directories up from this skill folder. Read [the workflow](../../../docs/workflow.md) and project AGENTS.md. Run tools from that root. Keep the bundle intact; it needs no private library.

## Begin or resume

For a new map, use [start-here](../../../docs/start-here.md) to identify purpose, representation scale, mood, available references and budget. Ask a small number of material questions, proposing concrete choices when helpful. Use `scripts/mapkit.py new --output work/<slug>` for the runnable example, then replace its world and planning records with the user's intent. Do not quietly adopt the example's canon.

For existing work, read `planning/brief.md`, `planning/decisions.md`, `world.json`, `style.json` and `metadata/state.json`. Summarize the accepted state and open questions before the next action. Never regenerate a good scene just because it is easier than understanding it.

## Route the work

- Compare art directions with [map-art-direction](../map-art-direction/SKILL.md).
- Plan geographic room, populations and factions with [map-world-planning](../map-world-planning/SKILL.md).
- Use [lantern-forest](../lantern-forest/SKILL.md) or [lantern-village](../lantern-village/SKILL.md) when those components need design, assets or repair.
- Produce a pilot, then expand with [map-render](../map-render/SKILL.md).
- Prepare a public delivery with [map-release](../map-release/SKILL.md).

Load only the guidance needed for the current stage. A local village request does not require inventing a continent. A style change does not authorize changing established canon.

## Maintain continuity

Save choices, assumptions, review results and next steps in `planning/decisions.md`. Keep canon, planned positions, observed painted geometry and user approval separate. Reconcile required sites after every region; missing content must be explicitly moved, deferred or unresolved.

Show style comparisons and the first integrated pilot before broad expansion unless the user has already delegated those choices. Continue within existing authorization without inserting a new permission ritual at every stage. If a tool, budget or essential decision prevents painting, complete independent planning and state precisely what remains unavailable.

## Completion

Deliver the agreed scope with honest native resolution, editable sources, safe previews and known limitations. A painted rectangle is not proof of functional rivers or a coherent population. Read [review](../../../docs/review.md) before claiming those checks.
