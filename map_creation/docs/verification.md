# Packaging verification

Checked 16 September 2026 during preparation of this public kit.

- All seven skills passed the skill-creator frontmatter/name validator.
- Twelve automated behavior tests passed, including image dimension rejection, stale input rejection, style reference retention, review requirements, source mutation detection, path constraints, full/partial coverage handling and exact preservation outside black repair-mask pixels.
- The standalone ZIP was extracted to a temporary location; its own helper created a fresh project and rendered the example without access to the source world-building repository.
- The quickstart ran in a separate virtual environment using the already installed Pillow package. A clean network download of dependencies was not tested. Runtime was Python 3.14.5 / Pillow 12.2.0; Python 3.10 is the declared minimum, not a separately tested interpreter here.
- Maintained Markdown links, JSON, skill metadata, supplied images, showcase hash/dimensions and basic machine-path/credential patterns passed the package audit.
- Both supplied JPEGs were visually inspected. The atlas preview is 1600 × 1067; the schematic example is 1536 × 1024. Neither contains EXIF entries.

The automated workflow tests use synthetic solid-color paintings to test bookkeeping and masks. Their artificial pass records do not count as visual acceptance of a map. No new generative painting, provider integration, full atlas reproduction, hydrological simulation or population validation was performed for this package.

The skill instructions were reviewed against the retained source lessons, but have not yet been independently forward-tested on a new painted world. The showcase's original review limits remain documented separately. Reuse-license selection is still an owner decision; no license grant is inferred from these checks.
