# Experiments

Small, self-contained experiments in making things with AI. Each directory contains its own instructions, dependencies, examples and agent skills, so you can take the part you want and leave the rest.

| Experiment | What you can try | Start here |
| --- | --- | --- |
| **Map creation** | Work with GPT-6 Astra on High to develop a world and guide it from art direction to a reviewed painted map. | [Open the map-making kit](map_creation/README.md) |

## Get just one experiment

Git clones repositories, not individual directories. A **partial clone with sparse checkout** keeps your working copy focused on the experiment and avoids fetching unrelated file contents when the Git server supports partial clone.

Run these commands in a terminal (Git required) to get the map-creation experiment from [ryannel/experiments](https://github.com/ryannel/experiments):

```sh
git clone --filter=blob:none --sparse https://github.com/ryannel/experiments.git experiments
cd experiments
git sparse-checkout set map_creation
cd map_creation
```

Root files such as this README also remain visible. Repository metadata is still cloned; this is not a zero-metadata folder download. To add another experiment later, run `git sparse-checkout add OTHER_FOLDER` from the repository root. To update, use `git pull` after committing or setting aside your local changes.

Prefer a normal download? Use your Git host's **Download ZIP**, extract it, then keep the experiment's whole directory, including hidden files such as `.agents/` and `.codex/`. A repository ZIP contains all experiments; a separately published experiment ZIP can contain just one. Never copy only a skill's `SKILL.md`: its references and supporting tools matter.

## Run an experiment

Open that experiment's directory as your workspace and follow its README. For map creation, select GPT-6 Astra with High reasoning and paste its starting prompt; the agent handles the technical workflow. There is no root-level installation, shared environment or dependency on a sibling project. Check the experiment's reuse terms before redistributing it.

## Add an experiment

Follow [CONTRIBUTING.md](CONTRIBUTING.md). Each folder must work when copied out of this repository. Keep large outputs, account credentials and private source material out of the shared repository.
