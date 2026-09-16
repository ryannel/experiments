# World JSON format, version 1

Use [Bracken Reach](../examples/bracken-reach/world.json) as the complete runnable example. The helper uses explicit data rather than inferring geometry from prose. Coordinates are **world pixels**, origin top-left, x rightward, y downward. Values must lie inside the canvas (`0 <= x < width`, `0 <= y < height`).

| Field | Contents |
| --- | --- |
| `version` | Integer `1`. |
| `name` | Nonempty display name. |
| `canvas` | Positive integer `width`, `height`; at most 16,000,000 pixels total. |
| `scale_note` | Human-readable distance/representation assumptions. |
| `land` | One or more `{id, polygon: [[x,y], ...]}` records. Minimum three vertices. |
| `regions` | `{id, kind, polygon}`; kind is `forest`, `upland`, `farmland` or `wetland`. |
| `rivers` | `{id, points, width, downstream}` plus optional name. Points are ordered upstream to downstream. Width is in pixels, greater than zero and at most 128. |
| `roads` | `{id, from, to, points}`. Endpoints reference settlement IDs; first/last points equal their anchors. |
| `settlements` | `{id, name, point, role, population, faction, status}`. Population is null or a nonnegative integer. Faction is null or a valid faction ID. |
| `factions` | `{id, name, kind, reach}`. Kind is `state`, `community` or `network`; reach is descriptive, not an exclusive polygon. |

All IDs are unique across collections. Each river's `downstream` is a receiving river ID, `sea`, or `closed-basin`. A tributary's final point must exactly match a vertex in its receiver. The graph must have no cycle. These rules catch broken references; they do not prove downhill flow or that a mouth visibly enters the sea.

Site status is `planned`, `painted`, `moved`, `deferred` or `unresolved`. Candidate reviews separately account for intersecting sites. The helper does not silently update world anchors from pixels; maintain observed positions and reasons in the society/decision records, then deliberately revise world JSON when appropriate.

Additional fields can carry authoring notes but are not automatically interpreted. The renderer draws polygons, river and road lines and simple settlement symbols. It does not support terrain elevation, climate simulation, true political boundaries, automatic road routing, detailed buildings or automatic population allocation. Extend the format deliberately if adding those features.

`style.json` provides the guide colors in `palette.water`, `land`, `forest`, `upland`, `road` and `ink`, plus instructions for external painting. Use valid Pillow color strings such as `#61715b`.
