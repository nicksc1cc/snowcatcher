# Grand Massif: linked domain research

Started 26 October 2026 for the Snow Catchers Level 3 page (france/grand-massif/), built with db/load_package.py. Replaces the hand edited JSON on the projectsnow `grand-massif` branch, which was used only for leads. Not published; the page waits for Nick's review.

| File | Contents |
|---|---|
| package.json | Page, place, four datasets and the files the loader reads |
| data/evidence_register.csv | Sources G001 to G042 |
| data/places.csv | Resorts, the five village sectors, upper stations, lifts, passes and the places named on the page |
| data/facts.csv | Facts written by scripts/make_data.py (F000644 to F000817), with a check against the database property rules |
| data/snow_era5_seasons.csv | ERA5 seasonal snowfall, cell 46.0 N 6.75 E, 1100, 1600 and 2100 m, 1950/51 to 2025/26 |
| data/snow_era5_clusaz_1600.json | ERA5 seasonal snowfall at 1600 m for the La Clusaz cell (46.0 N 6.5 E), for the comparison |
| data/existing_facts.json | Facts already in the database that the page uses (Grand Massif listing, Portes du Soleil and Évasion Mont Blanc comparisons) |
| model/network_config.json, run_2026-10-26.json | Network model input and output (db/model/network.js, OSM snapshot 2026-10-26T21:08:20Z) |
| model/network.json | Lift ride matrices in the site format |
| page/draft.json | The page in the l3-domain shape, written by scripts/make_draft.py |
| scripts/compact_facts.py, compact_blocks.py | Shorter forms of the facts and block inserts for loading through the SQL tool |
| out/load.sql, out/report.json | Loader output |

## Scope

Five village sectors, agreed with Nick: Flaine, Les Carroz, Morillon, Samoëns and Sixt. Comparison areas, agreed with Nick: Portes du Soleil, Évasion Mont Blanc and La Clusaz Manigod (the nearest linked areas).

## Status

Loaded into the database on 26 October 2026 as drafts: 174 facts (F000644 to F000817), 379 blocks and 34 list items (review), 8 photos, 66 places, four datasets, 228 weather rows, 7 sector links and page:area:grand-massif (review). The layout hashes to d18bc4796c57d17efc7879a2d62ec8fa. The local preview hashes to 920fc60d4875229e846c2b1073f78c49 (49,494 characters).

A dry run of approve_page inside a rolled back transaction rendered 49,491 characters: the database draws the Sixt skibus link as a lift. With db/migrations/2026-10-26_links_bus_walk.sql applied inside the same rolled back transaction the render matched the preview hash exactly. That migration must be run before the page is approved and published; no other dataset has a bus or walk link.

## Model notes

- With five large sectors, starting each matrix row at every main lift base made most cells zero, so network.js gained `cfg.matrixFrom = "village"`: matrices, critical lifts and routes start from the village lifts (lowest main lift and any within 200 m).
- Sixt has no lift link. The free skibus from the Sixt drags to the Grand Massif Express, and from Vercland to the Grand Massif Express, are hand transfers that cost no lift ride.
- The Vagnys and Pralet chairs at Sixt are still in OpenStreetMap but closed (Guide Ski, Wikipedia) and are dropped. The Chavannes drag west of Les Carroz is outside the area.
- A second run gave Vercland, Morillon 1100, Samoëns 1600 and Flaine Forêt their own base rows (basesExtra in the run file).
- Critical lifts: Kédeuze, the Morillon gondola and the Sairon chair are each the only lift route out of their village (4 resorts cut). Coulouvrier adds 6 lift rides when closed, Tête des Saix 3. The Sixt Cascades drag shows as critical only because the skibus is anchored at its foot; it is not used.
- The Cascades is tagged intermediate in OpenStreetMap, which matches Mon séjour en montagne (regraded red for its length).

## QA, 26 October 2026

- Every figure on the page is a fact token; the loader reported no problems and the style check reports nothing for grand-massif.
- Recomputed from the data: snow medians (391 cm at 1600 m reproduces F000629 from the Évasion comparison run), the three lowest of five seasons at 1100 m (2023/24 second, 2022/23 fourth, 2024/25 fifth of 76), price differences in the pass table, compare row differences, base table against the run file.
- Each route note was checked against SCNet.route from the village lifts.
- Network findings against sources: Sixt has no lift link and the Cascades is one way with a shuttle back (Guide Ski, Wikipedia, skiresort.com, Mon séjour en montagne); Les Carroz joins the area by the Kédeuze gondola (Les Carroz tourist office); no run returns to the Grand Massif Express (Alpine Answers). The official piste map page did not load in the browser.
- Claims removed or reworded in QA: the Loi Montagne sentence now refers to the listed communes; skibus coverage limited to what Guide Ski and the Samoëns tourist office state; La Pointe Noire, Le Potet 2.0, the Gîte du Lac de Gers and the Salvagny snowmaking reworded to their sources; Cluses distances credited to Skiinfo and Guide Ski.
- Facts the database rules reject were dropped and the figures put into words: the Cascades drop and open days, the Combe de Gers drop, Cluses and Sixt distances, the Jaÿsinia flower count.

## Open points

- Run db/migrations/2026-10-26_links_bus_walk.sql before approve_page.
- Évasion Mont Blanc and La Clusaz Manigod have only basic pages, so their comparison links lead there.
- About 45 unique source links on the page against about 60 on the Portes du Soleil page.
