# From the example to your first painting

## 1. Prepare the plan

Run the README quickstart. Inspect `previews/guide.jpg`, then replace the example assumptions in `planning/brief.md` and `planning/societies.md`. Select or trial an art style, save its reference in `assets/masters/`, and update `style.json`.

Preparing a candidate freezes inputs. If you have already run the quickstart and then changed the world/style, use `pilot-v2` in the following commands instead of `pilot-v1`.

## 2. Paint the prepared crop

The quickstart rectangle `[300, 220, 768, 512]` includes forest, a tributary/main river relationship and settlement approaches. Inspect `iterations/pilot-v1/guide.png`, `prior.png` and `context.jpg`.

Use prompt.md as a starting point. Add the selected style reference, the wood-road crossing and explicit expectations for the river and site entrances. Submit the exact brief and references to your configured image tool or paint the crop manually. Ask for a 768 × 512 lossless PNG. Verify the returned dimensions; some tools cannot produce that size. If unsupported, prepare a new native rectangle at a supported size within the canvas, rather than upscaling returned pixels.

Save the returned painting to `work/my-world/assets/masters/pilot-returned-v1.png`. Copy [provenance.json](../templates/provenance.json) into that same folder as `pilot-provenance-v1.json`, and replace its placeholders with the exact tool, prompt, call count, references and actual dimensions.

```sh
python scripts/mapkit.py ingest work/my-world pilot-v1   --image work/my-world/assets/masters/pilot-returned-v1.png   --provenance work/my-world/assets/masters/pilot-provenance-v1.json
python scripts/mapkit.py inspect work/my-world pilot-v1
```

## 3. Review and select

Open the candidate's evidence/overview.jpg and native PNG crops. Follow [review.md](review.md), including the complete affected river and road connections beyond the crop. Add evidence as needed. Fill review.json honestly with actual observations, project-relative evidence paths and the reviewer name. Do not mark a guide-only test as a successful painted pilot.

```sh
python scripts/mapkit.py accept work/my-world pilot-v1
```

Unclear checks or stale inputs will block acceptance with an error. Repair defects with a new candidate and then review again. User approval is separate; follow the user's requested checkpoints rather than interpreting this command as consent.

## 4. Expand or repair

Prepare neighbouring rectangles only after selecting the pilot. Include overlapping context and review all joins against the current assembled pixels. The simple helper pastes the new rectangle in full; it does not automatically solve seams. Choose boundaries carefully or use a refinement mask to preserve accepted pixels.

For a local repair, create an L-mode grayscale mask in an image editor, with the same size as a new repair rectangle. Then:

```sh
python scripts/mapkit.py prepare work/my-world ford-repair-v1   --rect 620 430 256 256 --mask work/my-world/assets/masters/ford-mask-v1.png
```

Use the prior.png as the edit target and repeat ingestion, inspection and acceptance. Keep black-mask areas untouched and inspect the entire blend boundary.

## 5. Deliver

After the full canvas has accepted coverage:

```sh
python scripts/mapkit.py export work/my-world release-v1
```

For an intentionally partial pilot, use `--allow-partial` and label the result as a work in progress. Unpainted areas will still contain the schematic guide. The helper refuses to call an untouched guide a release.

Inspect and adjust labels.svg against the actual painted sites, complete the release notes, and choose public files explicitly. This workflow does not claim a fully painted atlas from the offline commands alone.
