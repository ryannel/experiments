# Map creation

**A practical kit for turning an imagined world into a map worth exploring.**

Start with the places and journeys that matter. Find an art style on a small test scene. Give rivers, settlements and factions enough room. Then paint, inspect and refine the world a region at a time.

![A painted fantasy atlas from the original experiment](showcase/atlas-preview.jpg)

*An example from the original Lantern Sea experiment, shown at 1600 pixels wide. It was built through guided painting and revision. The offline demo below produces a schematic guide, not this painting. [Provenance and review limits](showcase/README.md).*

This package brings together the woodland and settlement skills developed during that experiment, with new guidance for art direction, world planning, render production and delivery. It includes a small fictional world so you can try the mechanics without an account or an art library.

## Choose your starting point

| I want to… | Start with… |
| --- | --- |
| See something run locally | The offline quickstart below |
| Make my own world with an AI assistant | [Start a map](docs/start-here.md) and `$map-director` |
| Understand the full process | [The production arc](docs/workflow.md) |
| Use my existing map or setting | [Bring your own material](docs/start-here.md#bring-your-own-material) |
| Inspect the code and data format | [Tool reference](docs/tools.md) and [world format](docs/world-format.md) |
| Write about the experiment | [Case study](docs/case-study.md) and [website copy](showcase/website-copy.md) |

## Offline quickstart

Requires **Python 3.10+** and Pillow. No API key, Node, Blender or paid service is needed for this demo. Run inside this folder:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/mapkit.py new --output work/my-world
python scripts/mapkit.py validate work/my-world/world.json
python scripts/mapkit.py guide work/my-world
python scripts/mapkit.py prepare work/my-world pilot-v1 --rect 300 220 768 512
```

On Windows use `py -m venv .venv`, then `.venv\Scripts\Activate.ps1` in PowerShell; use `python` for the remaining commands.

Open `work/my-world/previews/guide.jpg`. You'll see **Bracken Reach**, a deliberately small example with three territorial communities, an overlapping trade faction, a main river, tributary, roads and settlement markers. The first painting brief and native guide crop are in `work/my-world/iterations/pilot-v1/`.

Read `work/my-world/planning/brief.md`, edit the world and style, and prepare a new candidate ID after changes. The commands prepare references and retain results; painting happens in your chosen image tool. See the [worked walkthrough](docs/walkthrough.md).

## Make a painted map with an assistant

Open **this `map_creation` folder** as your workspace. The project includes seven local skills in `.agents/skills/`; they do not need a global installation. See [setup and tool capabilities](docs/setup.md).

Start with this prompt:

> Use $map-director to help me make a new fantasy map with this kit. Read AGENTS.md and docs/start-here.md. Help me choose the scope, explore a visual style, and build the geography, population and factions before painting. Save decisions and assumptions. Start with one representative region and review it at native size before expanding. My starting idea is: [describe your world].

| Skill | Job |
| --- | --- |
| `map-director` | Coordinate the whole process and resume from saved decisions. |
| `map-art-direction` | Compare style trials and establish a visual reference. |
| `map-world-planning` | Connect geography, travel, population and political space. |
| `lantern-forest` | Compose coherent habitats, canopy and woodland edges. |
| `lantern-village` | Design settlements with usable approaches and signs of life. |
| `map-render` | Prepare, paint, inspect, repair and accept bounded candidates. |
| `map-release` | Prepare clean artwork, labels, safe previews and a shareable release. |

The Lantern skills are portable adaptations. They retain the practical lessons without requiring the original setting or its asset library. Keep this folder together: skills reference the included docs and templates.

## What is included

- Seven editable skills, with linked guidance and project instructions.
- Brief, style, society, region, review, provenance and asset templates.
- An original public fictional example and an offline guide renderer.
- Tools for local painting briefs, immutable candidate inputs, image ingestion, review crops, bounded repairs, acceptance and export.
- A small atlas showcase and a plain-language account of what worked and what failed.

The original private world files, full atlas masters, asset packs and project-specific Blender/render scripts are not dependencies and are not included. The supplied showcase is a visual reference; it cannot reconstruct the original atlas. To make new artwork, use your own compatible assets or follow the included style and asset-generation workflow.

## What this experiment does—and does not establish

The source experiment demonstrates iterative guided painting and local repairs. Generative images can shift rivers, invent buildings and redraw neighbours even when told to preserve them. The kit therefore makes review an explicit part of production.

The helper is intentionally small: schematic geometry, a single local project, and a canvas capped at 16 million pixels. It does not simulate drainage, estimate agricultural capacity, guarantee model fidelity or implement a streaming continent renderer. Large-map methods and their limits are described in [scaling](docs/scaling.md). The preview is not a benchmark or a promise of one-click results.

## Check and share

```sh
python -m unittest discover -s tests -v
python scripts/check_package.py
python scripts/package_experiment.py --output dist/map_creation.zip
```

The archive uses an explicit source allowlist and excludes `work/`, private writing, caches and credentials. The entire experiment is independent of the repository root. [Verification record](docs/verification.md) · [Release guidance](docs/releasing.md) · [Reuse terms](LICENSE.md) · [Credits](CREDITS.md).
