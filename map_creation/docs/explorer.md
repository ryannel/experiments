# The tiled atlas explorer

The public delivery lives in `showcase/explorer/`. It adapts the same small-tile canvas approach as the scent wheel, with a rectangular camera, two map modes, bounded decoded-image caching and no dependency on another experiment. The maintained HTML, CSS and JavaScript are the delivered files; there is no bundler or generated runtime to edit elsewhere.

## View after cloning

From `map_creation`, serve the folder with Python’s standard HTTP server and open `/showcase/explorer/`. Alternatively serve the explorer folder itself. No Pillow, Node, fonts, CDNs or API keys are needed for visitors. A `file://` URL cannot fetch the map configuration and tiles; the page explains this instead of silently failing.

The initial camera fits the whole map. The article embed always starts fitted, including reloads and back-navigation, rather than restoring the iframe’s last zoom. Standalone links still restore explicit view hashes. Zooming out stops at Fit map. Drag, scroll, pinch and double-click move through it. The embedded canvas and surrounding surface are transparent; site colours and pill controls follow a same-origin `lantern-sea:theme` message from the parent, including explicit theme changes. The standalone viewer follows the operating-system theme. The compact header links and camera controls align to the right, matching the companion scent explorer. Fit map, Actual detail, Place names and Expand map are available on small screens too. The 100% view means one source pixel per CSS pixel; device-pixel-ratio rendering is capped at 2 and magnification at 200%. Enlarging past native size adds no detail. The browser stores x/y, scale and name visibility in the standalone URL hash. Shared standalone links and reloads restore that view, constrained to the viewport; the article embed intentionally starts fitted.

The viewer fetches a tiny fallback overview and only visible tiles at a level appropriate to the camera. Six concurrent requests and a 96-tile decoded cache limit resource use; obsolete requests are cancelled. The native PNG is never requested. This is a browser delivery mechanism, not a claim about bounded-memory painting or assembly.

## Rebuild tiles from explicitly selected paintings

Install the pinned Pillow dependency in a project-local environment, as described in [setup](setup.md). The offline encoder decodes one full source at a time and can use several hundred megabytes of memory. It has a 200-megapixel ceiling; it does not remove the small-map helper’s production limit.

Supply the clean native PNG and its matching labelled export explicitly:

```sh
python3 scripts/build_explorer.py \
  --artwork /path/to/world-artwork-unlabelled-v1.png \
  --labelled /path/to/world-labelled-v1.png \
  --output tmp/new-explorer
```

The output must be fresh; existing tiles are never overwritten. The encoder verifies equal dimensions, keeps source files unchanged, strips delivery metadata and records source hashes without private absolute paths. Review the new tiles before replacing `showcase/explorer/tiles/` and `map.json`. Keep the viewer files and safe overview beside them. Quality defaults to WebP 90; a different painting or quality needs a new visual comparison. Never check full PNG masters into the web folder or copy an entire private source repository.

The current delivery selects only the two paintings from world-atlas-complete-v1; its provenance is in [the explorer README](../showcase/explorer/README.md) and `map.json`. The original release’s review limitations remain in force.

## Check an update

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_explorer.py
python3 scripts/check_package.py
```

The checker verifies exact pyramid coverage and edge/overlap dimensions for both modes, WebP headers, counts and local links. Tests exercise odd dimensions, native tile reconstruction, source preservation and refusal to install mismatched modes. Inspect the actual browser at overview and native detail, near tile joins, with/without names, on narrow portrait and landscape screens. Test drag, pointer-centred zoom, Fit map, expanded mode, reload and a failed tile. Structural checks do not establish artistic quality.

## Reuse on the article site

Copy the **whole explorer folder** into a static public path. It is intentionally portable and requires no private project checkout. Embed that same index rather than implement a second viewer:

```html
<iframe src="/map-explorer/index.html?embed=1"
  title="Explore the Lantern Sea map"
  loading="lazy" allow="fullscreen"
  style="width:100%;height:75svh;min-height:420px;border:0"></iframe>
```

The viewer posts a same-origin `lantern-sea:layout` message with its preferred pixel `height`, calculated from the painting’s 3:2 aspect ratio and measured toolbar/caption heights. The article sizes the iframe to that value, keeping controls close to the image rather than centering it inside an oversized viewport. Expanded mode overrides this preferred height and fills the window.

For same-origin article embeds, expansion also posts a `lantern-sea:expanded` message with a boolean `expanded` value to the parent. The article can use this to fill the viewport when native fullscreen is unavailable; validate both the origin and the iframe source. Sending `lantern-sea:collapse` back closes it.

In embedded mode, wheel zoom requires Ctrl or ⌘ so ordinary scrolling continues through the article; pinch, drag, buttons and keyboard controls remain available. Link to the non-embedded index for a full-window alternative. Lazy loading avoids downloading tiles until the explorer is near the reader. Keep the existing article figures for its narrative; the explorer lets readers inspect the actual map. Update the static assets as one versioned delivery, and preserve the source hash/provenance. The viewer revision can be cache-busted in the iframe path when deploying a replacement. Preparing the repo does not publish the article or deploy a site.
