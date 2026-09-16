# Prepare a public release

## A finished map

Keep clean lossless artwork, editable labels and reconstruction inputs locally. Present safe overviews and native detail crops. Use a release manifest with exact source versions, hashes, dimensions and review status. Carry unresolved demographic/geographic assumptions forward. The kit's helper export is a local handoff, not a publishing service.

Review label hierarchy at actual overview size and local names at intended zoom. Move labels against observed painted anchors; do not repaint terrain to change text. Keep a clean text-free master even when delivering a flattened labelled copy.

Select public artwork and metadata deliberately. Hidden GM material can leak through filenames, SVG text, alt text, JSON, prompts and layer names. A sanitized release summary can accompany private exact production records. Include only references and source art you have permission to distribute, with their actual terms.

## This experiment kit

Run:

```sh
python -m unittest discover -s tests -v
python scripts/check_package.py
python scripts/package_experiment.py --output dist/map_creation.zip
```

The packager includes only maintained docs, skills, scripts, templates, examples, tests, showcase and named root files. It refuses symlinks and does not include working projects, credentials, generated release archives or caches. It writes a SHA-256 sidecar beside the ZIP. Extract the archive into a new location and run its quickstart there before publishing.

The ZIP contains `map_creation/`, including `.agents/`. It has no dependency on the experiments root. Root sparse-checkout instructions work once the owner publishes the repository and the reader supplies its clone URL. A future experiment must supply its own quickstart and reuse terms.

## Publication copy

[showcase/website-copy.md](../showcase/website-copy.md) provides a short summary, accessible image description and a suggested page structure. The preview is already small enough for a README; host larger files separately only when deliberately needed. Do not publish the original source repository, its private setting, or its full asset library as part of this kit.
