# Les Sybelles — Level 3 linked-domain research

**Status:** Research and editorial build in progress  
**Started:** 21 October 2026  
**Target:** Snow Catchers Level 3 linked ski-area page  
**Website data:** `nicksc1cc/projectsnow/src/data/l3/les-sybelles.json`  
**Research standard:** Use the Portes du Soleil research package as the methodological benchmark, not as a copy template.

## Working proposition

Les Sybelles is marketed as a 310 km, six-resort ski domain in the Maurienne. Its useful story is the five-resort linked ski network around the Ouillon and Saint-Colomban-des-Villards, whose connection stopped operating in winter 2025–26 and is now being prepared for a planned 2026–27 restart. The restart is not yet confirmed operational. The page must not present six resort names as proof of one continuously skiable network.

## Current evidence position

- The operator's public pages advertise 310 km and describe six resorts, while some resort pages describe the core ski area as five resorts.
- Saint-Colomban-des-Villards' link was not maintained in 2025–26. A newer local-authority update says inspections and maintenance are underway for a planned 2026–27 restart; a municipal council record still describes the ski domain as five areas after the closure. Treat the reconnection as planned but not operationally verified, and keep full-pass validity unresolved until the operator confirms both.
- The operator's ski map and live status page are the primary sources for operational topology. A static map and a live status page answer different questions; neither should be treated as a guarantee that every connection is open on a particular day.
- A current search-indexed result for the Saint-Jean-d'Arves tourist-office brochure page identifies a 2026–27 Les Sybelles piste map (6.98 MB). However, the page content available to this research session still renders the 2025–26 map. The current PDF's direct asset URL therefore needs to be recovered and checked before we treat it as inspected evidence.
- A public integration identifies a Lumiplan data-service map ID and static/dynamic POI endpoints. The capture workflow is in `scripts/fetch_official_map.py`; it has been committed but not run in this session. Attempts to open those endpoints through the available browser reader were blocked, so no current API snapshot has yet been verified or added to the evidence register.
- A current 2026–27 rate table lists €307.20 for an adult six-day pass and says rates were verified against official sources. The official checkout remains the final check for age band, dates, product and purchase channel.
- The 2026–27 map is listed by the tourist office, but its actual PDF geometry has not yet been inspected in this session and the public Lumiplan API could not be captured. The sector-level boundary is checked; the pairwise lift/piste graph remains unverified. Do not publish route counts or label 310 km as independently measured.
- Snowfall history by elevation is not yet modelled or checked against station observations. Do not add a numerical snow-reliability claim until that work is complete.

## Production page

A Level 3 page data file now exists at `nicksc1cc/projectsnow/src/data/l3/les-sybelles.json`. It distinguishes the verified five-sector core from the planned but unverified Saint-Colomban reconnection, withholds route and snow metrics that lack a reproducible model, and uses the shared Level 3 template. The page is structurally produced; network-route QA remains open.

See `05_network-check-2026-10-21.md` for the dated decision record.

## Atomic question coverage

The current bank contains 250 destination-specific atomic questions across domain identity, network connections, sector profiles, base access, snow, passes and traveller fit. Question statuses are recorded per item; the bank is not a claim that every question has been researched. Run `python3 research/les-sybelles/scripts/validate_package.py` from the repository root to check CSV/JSON parity, duplicate questions, statuses, priorities and evidence references.

## Files

- `01_question-triage.md` — Level 3 atomic-question selection and rationale.
- `02_network-and-sector-analysis.md` — known topology, sector model, map-data capture and unresolved network claims.
- `03_meaning-map.md` — central proposition and narrative progression.
- `04_publication-qa.md` — current publication gate and next verification actions.
- `data/question_bank.csv` — destination-specific atomic questions.
- `data/evidence_register.csv` — claim-level evidence with scope and caveats.
- `data/coverage_matrix.csv` — section coverage and gaps.
- `scripts/fetch_official_map.py` — timestamped capture of the public Lumiplan static inventory and live status response.

## Publication rule

This is not approved for publication until the current official map has been checked against every claimed link, Saint-Colomban pass/link status is resolved, the full-pass price is confirmed, and production JSON, graphics and prose pass claim-to-copy and build QA.
