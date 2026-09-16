# Set up the agent

## Required: GPT-6 Astra with High reasoning

Open `map_creation` as your Codex project, start a task, and select **GPT-6 Astra** with reasoning effort **High**. This is the required agent setup for this experiment, chosen by its author. It is not a comparative claim that other models cannot make maps.

The model identifier is `gpt-6-astra`; High corresponds to `high`. OpenAI documents that reasoning level for [GPT-6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra).

The included [.codex/config.toml](../.codex/config.toml) sets both project defaults. Codex loads project configuration only for trusted projects, and explicit overrides can take precedence. Check the actual task settings in your client; a prompt or skill cannot switch the running model or prove which model is active. These settings are local to this experiment and do not edit your personal defaults. See [official configuration guidance](https://learn.chatgpt.com/docs/config-file/config-basic).

If GPT-6 Astra or High is unavailable in your account/client, resolve that setup before following the map-production workflow. The agent should report a known mismatch and help you select the required settings, rather than silently choosing another model. If it cannot inspect session settings, it should say so and ask you to check the displayed selection once.

## Give the agent the project and tools

Keep the entire folder, including `.agents/skills/`, `.codex/`, docs and templates. The agent needs project file access, a way to run local helpers, image inspection, and image generation/editing. GPT-6 Astra is the directing agent; the image tool creates or edits the artwork. Model selection alone does not establish that those tools are connected.

Ask the agent to check its available tools at the start. It can prepare the brief and world plan while resolving a missing image tool, but must explain what is needed before painting. It should not switch to a paid API or make you perform a manual image handoff without discussing that change. Agree a generation/time budget before a batch.

Codex discovers project skills in `.agents/skills`. If the director does not appear, ask the agent to read `.agents/skills/map-director/SKILL.md` directly, or restart the task in this folder. Specify the project-local skill if you also have older Lantern skills installed. See the [official skills documentation](https://learn.chatgpt.com/docs/build-skills). These setup references were checked on 16 September 2026.

## Let the agent handle technical setup

You can begin with the starting prompt in the README. When local helper work is needed, the agent checks for Python 3.10+, creates a project-local virtual environment if appropriate, and installs the pinned Pillow dependency. It should diagnose missing dependencies and perform available setup within its permissions; involve you only for an unavailable capability, account access or a required permission.

The [helper reference](tools.md) and [offline demo](offline-demo.md) provide the technical commands. They are reference material for the agent, not prerequisites for your first conversation. Node, Blender and the original private asset library are not required by the bundled helper.

## First response to expect

The agent should acknowledge your premise, check the required settings as far as its tools allow, ask a few useful creative/budget questions, and suggest the first concrete step. It should create and maintain the records itself. You should not receive a list of JSON files to populate or shell commands to execute as the normal onboarding flow.
