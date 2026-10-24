# Tignes Val d'Isère: linked domain research

Started 24 October 2026 for the Snow Catchers Level 3 page (france/tignes-val-disere/), built with db/load_package.py.

| File | Contents |
|---|---|
| package.json | Page, place, datasets and the files the loader reads |
| data/evidence_register.csv | Sources T001 to T064 |
| data/places.csv | Resorts, the eight sectors, lifts, passes and the places named on the page |
| data/facts.csv | Facts written by scripts/make_data.py; model facts come from the network run |
| data/snow_era5_seasons.csv | ERA5 seasonal snowfall, cell 45.5 N 7.0 E, 1950/51 to 2025/26 |
| data/existing_facts.json | Facts already in the database that the page uses (comparison table) |
| model/network_config.json, run_2026-10-24.json | Network model input and output (db/model/network.js, OSM snapshot 2026-10-24T11:32:51Z) |
| model/network.json | Lift ride matrices in the site format; the network dataset's outputs |
| page/draft.json | The page in the l3-domain shape, with figures as fact tokens |
| out/load.sql, out/report.json, out/blocks*.json | Loader output |

## Status

Loaded into the database on 24 October 2026 as drafts: 117 facts (F000373 to F000489, all draft), 370 blocks and 25 list items (review), 8 photos and 48 places (draft), three datasets (draft) and page:area:tignes-val-disere (review). A dry run of approve_page inside a rolled back transaction rendered the page with the same hash as the local preview (97f4e048f06650104bc65fa72a984642).

## Model notes

- The two funiculars (Perce-Neige and Funival) are modelled as lifts; network.js now reads railway=funicular. Three OSM ways are dropped (dropWays in the config).
- The Perce-Neige stations sit underground, more than 80 m from the pistes, so walking transfers were added by hand at both ends and along the Val Claret snow front.
- No single lift closure separates Tignes from Val d'Isère. The Leissières chair is Le Fornet's only lift out (7 sector pairs cut). Olympique and Solaise add 10 lift rides each when closed, Tommeuses 8, Funival 6.
- The fewest lift rides back into Tignes Le Lac and Les Brévières from Val d'Isère use a black run.

## Open points

- Lift count: 74 (Guide Ski, Tignes page) against 71 (Guide Ski, Val d'Isère page), both quoting the operator, against 80 on skiresort.com. The page shows all three.
- Neither resort sells a local six day pass; the page says so rather than showing a local week price.
- Network checks still to do against the 2026/27 piste maps: Leissières as Le Fornet's only exit, the black runs on the way back into Le Lac and Les Brévières, the Perce-Neige transfers.
- Bus timetables from Bourg-Saint-Maurice for 2026/27 not checked.
