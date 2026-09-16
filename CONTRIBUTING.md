# Adding an experiment

Give each experiment a descriptive `snake_case` folder. Include:

- A README explaining the question, a visual or example, prerequisites, a short runnable path, expected results, limitations and reuse terms.
- All code, agent instructions, templates, references and small samples required to run it independently. Use relative paths.
- Its own dependency file, ignore rules and meaningful verification command.
- Honest provenance for any supplied art or datasets; include only material intended for public distribution.

Keep experiments independent. If two projects need the same small resource, package a maintained copy in each or declare a separately installable dependency; do not reach into a sibling folder. No shared secrets, hidden global configuration or untracked local assets.

Before sharing, copy the folder to a fresh directory and follow its quickstart. Check links, generated output, package contents and image dimensions. Record what was actually tested. Generated demonstrations should be clearly distinguished from real production examples. Add the experiment to the root README table. Do not initialize nested Git repositories inside experiment folders.

Choose and include reuse terms for each experiment. Root documentation does not silently license third-party assets or future experiments.
