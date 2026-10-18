# Packaging verification

Checked 16 September 2026 during preparation of this public kit.

- All seven skills passed the skill-creator frontmatter/name validator.
- Twelve automated behavior tests passed, including image dimension rejection, stale input rejection, style reference retention, review requirements, source mutation detection, path constraints, full/partial coverage handling and exact preservation outside black repair-mask pixels.
- The standalone ZIP was extracted to a temporary location; its own helper created a fresh project and rendered the example without access to the source world-building repository.
- The offline helper demo ran in a separate virtual environment using the already installed Pillow package. A clean network download of dependencies was not tested. Runtime was Python 3.14.5 / Pillow 12.2.0; Python 3.10 is the declared minimum, not a separately tested interpreter here.
- Maintained Markdown links, JSON, skill metadata, supplied images, showcase hash/dimensions and basic machine-path/credential patterns passed the package audit.
- Both supplied JPEGs were visually inspected. The atlas preview is 1600 × 1067; the schematic example is 1536 × 1024. Neither contains EXIF entries.

The automated workflow tests use synthetic solid-color paintings to test bookkeeping and masks. Their artificial pass records do not count as visual acceptance of a map. No new generative painting, provider integration, full atlas reproduction, hydrological simulation or population validation was performed for this package.

The skill instructions were reviewed against the retained source lessons, but have not yet been independently forward-tested on a new painted world. The showcase's original review limits remain documented separately. Reuse-license selection is still an owner decision; no license grant is inferred from these checks.

## Agent-led guide revision

The README and walkthrough now lead with a creative conversation using GPT-6 Astra on High. Project defaults specify `gpt-6-astra` and `high`; model and configuration references were checked against official documentation. The configuration was parsed locally, all seven skills revalidated, and all twelve helper tests rerun successfully. The package includes only the specific `.codex/config.toml` file, not other local Codex state. Model configuration expresses the required setup; it does not prove a reader's active session or establish a newly completed painted-map trial.

## Tiled explorer — 18 October 2026

The selected clean and labelled world-atlas-complete-v1 paintings were encoded into 1,044 WebP tiles (522 per mode) at their native 12,276 × 8,184 dimensions. Both source hashes are retained in the delivery configuration. Original PNGs and editable layers remain in the original project; only the viewing derivatives were selected for this repo.

- Fourteen behavior tests pass, including two new tests for odd-size tile reconstruction, source preservation, overwrite refusal and rejection of mismatched map modes.
- The package audit and explorer checker pass: both pyramids have complete coverage, correct overlapping edge dimensions and valid local links. The standalone ZIP was extracted; all 1,050 explorer files match the maintained delivery, and the extracted copy loaded and zoomed without the source repository.
- Actual browser checks covered whole-map fit, native detail, mouse dragging, name visibility, URL/reload restoration, expanded-view fallback, 320 × 568 and 390 × 844 portrait layouts, 844 × 390 landscape, and operation inside an iframe. Phone layouts showed no horizontal overflow. Pinch handling is implemented; a physical multi-touch device was not tested in this pass.
- Removing one overview tile temporarily produced an unavailable-detail message and Retry control; restoring it and clicking Retry recovered the map. The final tile set and delivery configuration were restored and rechecked.
- At a 1280 × 720 browser viewport, the initial overview resolved seven tiles totalling approximately 0.85 MB; zooming to native detail brought the cumulative resolved tile payload to approximately 1.50 MB. These are observed tile payloads for that route, not a guarantee for every viewport, cache state or exploration path. The complete two-mode delivery is approximately 113 MB on disk; visitors do not load all of it at once.

These are delivery and interaction checks. They do not constitute new approval of the painting, independent geographic validation or a bounded-memory production-render benchmark. The article site has not been modified by this work.
