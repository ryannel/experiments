# Optional offline helper demo

This page is for inspecting the implementation or for an agent checking its local tools. To make a map through conversation, use the [agent-led starting prompt](../README.md). The demo produces a schematic planning guide; it does not require a model or generate painted art.

Requires Python 3.10+ and Pillow. Run inside `map_creation`:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/mapkit.py new --output work/my-world
python scripts/mapkit.py validate work/my-world/world.json
python scripts/mapkit.py guide work/my-world
python scripts/mapkit.py prepare work/my-world pilot-v1 --rect 300 220 768 512
```

On Windows use `py -m venv .venv`, then `.venv\Scripts\Activate.ps1` in PowerShell; use `python` for the remaining commands. Choose a fresh output directory if `work/my-world` already exists.

Inspect `work/my-world/previews/guide.jpg`. Bracken Reach contains three territorial communities, an overlapping trade faction, connected rivers, roads and settlement markers. The prepared candidate contains a native guide crop, context and a starting brief. This geometry remains a proposal for review.

The agent can then follow the [technical walkthrough](technical-walkthrough.md) to import paintings, inspect candidates, apply bounded repairs and export a release. People following the normal workflow steer these stages in conversation while the agent operates the tools.

The helper uses no image API. A fresh dependency installation needs package-index access; guide rendering is offline once dependencies are installed.
