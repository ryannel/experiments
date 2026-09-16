# Map creation project instructions

This experiment requires GPT-6 Astra (`gpt-6-astra`) with High reasoning (`high`). Check available session metadata when starting a map-production task. If the settings are unknown, ask the user to verify the displayed selection once; never claim the model was verified from a prompt alone. Report a known mismatch and ask for the required selection rather than silently substituting. Project defaults live in `.codex/config.toml`; do not change global settings.

Drive the workflow through conversation. The user supplies creative direction and meaningful choices; you manage setup, project files, templates, image-tool calls, render helpers, review records and exports. Run supporting commands yourself when available and authorized. Do not send the user a script tutorial or blank JSON forms as the default onboarding experience.

Read README.md, then use `.agents/skills/map-director/SKILL.md` for a full map task. Use the narrower skills for focused requests. Run commands from this experiment's root. Keep all project-local skills and their linked docs together; do not assume an installed private art library.

Create user projects in `work/<slug>/`. It is ignored and never packaged. Record agreed canon, proposals, observed painting geometry and visual review separately. Do not invent user approval. Ask only for decisions that materially change the work; continue independently within established scope and generation budget.

Use a configured image tool for authored painting. Inspect the actual supplied images before edits; retain original returned pixels and provenance. The Python guide is schematic, not a substitute for requested painted artwork. Do not silently switch tools or incur API costs when a requested provider is unavailable.

Keep masters, masks and editable dependencies. Never overwrite source art through a symlink. Use versioned candidate IDs. Show whole-map previews no wider than 1600 pixels and native local crops; never automatically open a full atlas master or full-canvas SVG. Technical checks do not establish visual quality or user acceptance.

The bundled scripts handle small maps only. Read docs/scaling.md before larger production. Keep hidden GM writing outside public metadata and exports. Public packages must use explicit selected files, not a recursive copy of a working world. Do not publish or upload as a side effect of local preparation.
