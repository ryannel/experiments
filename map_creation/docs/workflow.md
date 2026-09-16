# The production arc

A map combines three records: **what the world means**, **where features are intended to go**, and **what the painting actually shows**. Keep them separate and reconcile them after changes.

| Stage | Produce | Review before expansion |
| --- | --- | --- |
| 1. Brief | Purpose, scale, audience, constraints, budget and open decisions | Is this an atlas, region or local illustration? |
| 2. Art direction | A few comparable style trials, chosen reference and style contract | Do terrain, houses and trees belong together at the intended size? |
| 3. Whole-world allocation | Land, high ground, catchments, habitats, political room and major journeys | Can rivers reach their outlets, and does every realm have geographic space? |
| 4. Population and factions | Settlement roles, population assumptions, providers, dependencies and effective control | Does ordinary life explain the settlements and routes? |
| 5. Pilot | One region painted at its intended pixel budget | Does the complete method work across terrain, forest, settlement and joins? |
| 6. Expansion | Sequential accepted regions, explicit content ledger and updated observed geometry | Are all affected neighbours, routes and required sites accounted for? |
| 7. Refinement | Bounded repairs with masks and exact input records | Did the repair solve the defect without creating a new one? |
| 8. Release | Clean master, separate labels, safe previews, provenance and limitations | Are public files complete, legible and free of hidden setting material? |

## The repeatable rendering loop

**Prepare → paint → ingest → inspect → accept.** Use `mapkit.py` for the small-map implementation; the [walkthrough](walkthrough.md) shows each command.

A prepared candidate freezes the world/style hashes, current accepted revision, native rectangle, guide/context and any edit mask. Painting is an explicit external step. Ingestion keeps the returned original and, for refinements, composites through the mask. Inspection produces small overviews and overlapping native crops. Acceptance requires completed review records tied to the exact candidate and rejects stale inputs.

Review and acceptance in this helper mean **recorded reviewer selection**. They never imply user approval, demographic validity or geographic simulation. Name the reviewer honestly. If the user has authorized continued production, record agent review and keep going within that authorization; do not invent extra permission gates.

After acceptance, prepare the next region from the current assembled artwork. Old briefs become stale when the accepted baseline or world/style changes. Use a new ID. Record moved, painted, deferred and unresolved sites explicitly; rectangle coverage is not content completeness.

## Useful checkpoints

Show comparisons at decisions that change downstream work: initial style, crowded political allocation, the first complete pilot and final release. Avoid asking the user to approve every reversible file operation. If an artistic decision is unresolved, offer a concrete comparison and continue with unrelated preparation.

Budget in measured pilot attempts, including rejected generations and repair calls. A successful single tile does not establish full-world cost or throughput. Count source generation, human/agent review and manual masks separately.
