# Make a map through conversation

Use **GPT-6 Astra with High reasoning** in the `map_creation` project. Start with the README prompt; the agent uses `map-director` to coordinate the other skills. You can phrase requests naturally and give feedback while work progresses.

## 1. Find the world

> I want a cold coastal region with three competing port cities, fishing villages and a large wild interior. Help me turn that into a workable map.

The agent asks about the map's purpose, tone and useful scale, proposes a manageable first region, and saves the brief. It also checks its tools and agrees a generation budget. You make the meaningful creative choices; it keeps the records.

## 2. Find the style

> Show me a few art directions for the same small coastal scene. I want detailed terrain but readable towns, and room for labels.

The agent uses `map-art-direction` to prepare comparable trials and generate them within the agreed budget. It explains differences in camera, light, palette and readability. You choose a direction or describe what to combine. The agent retains the chosen reference and writes the style contract.

## 3. Give people and factions room

> Plan where the ports, villages and powers belong. Include how they trade and what supports their populations, and leave genuine wilderness between the settled areas.

The agent uses `map-world-planning` to propose landforms, catchments, journeys and territories. It distinguishes countries from overlapping factions and marks uncertain population/resource assumptions. It shows a layout you can discuss, then updates the world model and society ledger itself.

## 4. Paint a representative region

> Paint the first region around a port, river crossing and woodland edge. Use the chosen style and check that the routes and water still connect.

The agent prepares the structural references, uses its image tool, retains the returned master and reviews native crops. It brings in the woodland and village skills where needed, fixes concrete defects, and shows you a preview with its findings. The pilot proves how the components work together before a larger batch.

## 5. Steer the refinement

> The port feels too monumental. Keep the river and coastline, make the homes more ordinary, and give the working waterfront more life.

The agent proposes or makes a bounded refinement within the established scope. It protects good surrounding artwork, checks the mask perimeter, rechecks journeys through the changed area and saves the new version. Your feedback becomes a recorded decision rather than a reason to restart the world.

## 6. Continue the render arc

> Continue into the neighbouring region using this style. Keep the accepted port intact and show me the next regional checkpoint within our remaining budget.

The agent works from the current accepted pixels, includes every affected neighbour, and reconciles required sites and faction space. It inspects rivers and roads across joins, not just individual attractive crops. It reports unresolved issues and reaches the next agreed checkpoint without handing you routine bookkeeping.

## 7. Return another day

> Resume this world from the last accepted version. Read our decisions and open issues, tell me the next useful step, and continue within the saved scope and budget.

The agent reads the saved brief, decisions, world/style records and accepted state. Recheck GPT-6 Astra / High when starting a new task. The project files preserve continuity across sessions.

## 8. Prepare delivery

> Prepare the map for sharing: a clean artwork master, editable labels, a safe overview, a few detail crops and notes on anything unresolved. Keep private setting material out.

The agent uses `map-release` to review the agreed scope, position labels against the painting, and prepare the files. It distinguishes its visual review from your approval and does not upload merely because a local release was prepared.

The [production arc](workflow.md) explains the records and review gates behind this conversation. The [technical walkthrough](technical-walkthrough.md) is available when the agent or a maintainer needs exact helper commands.
