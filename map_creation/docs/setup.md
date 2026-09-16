# Setup

## Local helper

Use the README's virtual environment commands. The helpers need Python 3.10+ and Pillow; Python 3.14.5 with Pillow 12.2.0 is the packaging test environment. A fresh dependency installation needs package-index access. Runtime guide generation is offline. A current Git client is useful for versioning; the helper does not create commits or remotes.

## Agent skills

Keep `.agents/skills/` inside this experiment and launch your agent with `map_creation` as the working directory. Codex discovers repository skills in `.agents/skills`; skill mentions can explicitly select them. See the [official skills documentation](https://learn.chatgpt.com/docs/build-skills), checked 16 September 2026. Host interfaces and tool availability can differ.

If a skill is not listed, restart the session in this folder or ask the agent to read `.agents/skills/map-director/SKILL.md` directly. If you have older Lantern skills installed, specify the file in this workspace to avoid ambiguity. With another assistant, supply AGENTS.md and the relevant SKILL.md as instructions. No particular agent product is required to read the workflow.

The skills deliberately rely on the rest of this standalone experiment. Copy the entire folder when moving it; installing only a skill directory globally loses its docs, templates and tools.

## Painting capability

Use an image tool that can create images and accept image references for edits. Native dimensions and reference fidelity vary by provider: verify returned files rather than assuming a requested size was honored. A chat interface without file output or image editing can still help with planning and briefs; use an external image editor for painting and import its lossless output.

These scripts do not call an image API. If your agent has a built-in image tool, use it through that tool's own instructions. If it does not, the same briefs work as a manual handoff. Configure accounts with the provider directly; do not put credentials in prompts or this repository. Paid generation limits and pricing depend on your account; agree a batch budget before starting. Blender and custom asset libraries are optional extensions, not setup requirements.

## Capability check before a full run

Confirm that you can read/write project files, inspect a small image, generate or import one lossless image, and report its actual dimensions. Establish whether edits can use references; the local mask compositor supplies exact outside-mask preservation independently of a model's promises. Stop expansion if the pilot cannot preserve required geography.
