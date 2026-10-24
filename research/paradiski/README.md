# Paradiski: linked domain research

Started 24 October 2026 for the Snow Catchers Level 3 page (france/paradiski/), the first page built with db/load_package.py.

| File | Contents |
|---|---|
| package.json | Page, place, datasets and the files the loader reads |
| data/evidence_register.csv | Sources P001 to P063 |
| data/places.csv | Resorts, sectors, lifts, passes and the places named on the page |
| data/facts.csv | Facts written by scripts/make_data.py; model facts come from the network run |
| data/properties.csv | Two new properties: sector_pairs_cut_count, extra_lift_rides_count |
| data/snow_era5_seasons.csv | ERA5 seasonal snowfall, cell 45.5 N 6.75 E, 1950/51 to 2025/26 |
| data/existing_facts.json | Facts already in the database that the page uses (comparison table) |
| model/network_config.json, run_2026-10-24.json | Network model input and output (db/model/network.js) |
| model/network.json | Lift ride matrices in the site format; the network dataset's outputs |
| page/draft.json | The page in the l3-domain shape, with figures as fact tokens |
| out/load.sql, out/report.json | Loader output |

## Status

Loaded into the database on 24 October 2026 as drafts: 154 facts (F000219 to F000372, all draft), 380 blocks and 31 list items (review), 8 photos and 58 places (draft), three datasets (draft) and page:area:paradiski (review). A dry run of approve_page inside a rolled back transaction rendered the page with the same hash as the local preview (696903141bdcc2efce045e2d213cc1fe).

## Open points

- Snowfall at 1,600 m for this cell is 288 cm in this run and 290 cm in F000104 (comparison run of 20 October). Approving this page puts two accepted values in one fact group. Proposal: supersede F000104 with F000361.
- piste_km needed a new scope, mapped_length, added to core.metric_scope by hand. The loader does not yet write new scopes.
- 16 facts are researched but not shown on the page (for example operator totals per resort and child day prices); they stay draft when the page is approved.
- Network checks still to do against the 2026/27 piste maps: the Peisey chair and Montalbert gondola as critical links, the Champagny black shortcut, Millerette left out of the base table.
- Bus timetables from Aime and Bourg-Saint-Maurice not checked.
