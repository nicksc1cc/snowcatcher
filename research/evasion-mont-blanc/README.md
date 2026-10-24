# Évasion Mont Blanc: linked domain research

Started 24 October 2026 for the Snow Catchers Level 3 page (france/evasion-mont-blanc/), built with db/load_package.py. Not published; the draft is waiting for Nick's review.

| File | Contents |
|---|---|
| package.json | Page, place, five datasets and the files the loader reads |
| data/evidence_register.csv | Sources M001 to M045 |
| data/places.csv | Region, resorts, the eight sectors, lifts, passes and the places named on the page |
| data/facts.csv | Facts written by scripts/make_data.py (F000490 to F000643) |
| data/snow_era5_seasons.csv | ERA5 seasonal snowfall, cell 45.75 N 6.75 E |
| data/existing_facts.json | Facts already in the database that the page uses (Les 3 Vallées comparison) |
| model/network_config.json, run_2026-10-24.json | Network model input and output (db/model/network.js, OSM snapshot 2026-10-24T22:31:35Z) |
| model/network.json | Lift ride matrices in the site format |
| page/draft.json | The page in the l3-domain shape, written by scripts/make_draft.py |
| out/load.sql, out/report.json | Loader output |

## Status

Loaded into the database as drafts: 154 facts, 372 blocks and 35 list items (review), 8 photos, 75 places, five datasets, 228 weather rows, 7 sector links and page:area:evasion-mont-blanc (review). The blocks hash to d18d4b28a7f4badc2b2b75a39a610d7f. A dry run of approve_page inside a rolled back transaction rendered the page with the same hash as the local preview (19b8d8364a010a9a5f2bbb990c644354).

On 25 October 2026 the four chapters were deepened toward the Portes du Soleil page (M042 to M045: Leo Trippi, Snowcarbon for Saint-Gervais, skiresort.com families, the Pioupiou club). Six places and six list items were added. The block and layout updates went through this time, so there is no SQL for Nick.

## Findings

- Two networks share the pass: Megève with Saint-Gervais, and Les Portes du Mont-Blanc (Le Jaillet, Combloux, La Giettaz). They do not link on skis.
- Critical lifts by sector pairs cut: Rocharbois 6, Princesse 4, Mont d'Arbois 3, Mont Joux 3, Christomet 2, Bonjournal 2, Prés 1.
- Leaving Saint-Nicolas needs a red run.
- Low altitude for its size. ERA5 median snowfall at 1,600 m was 362 cm for 1991 to 2020 against 426 cm for 1961 to 1990, and all five seasons from 2021/22 to 2025/26 came in below 362 cm.
- The cheapest six day pass of the four areas compared (€324.50).

## Model notes

- The TKE1 des Charmots drag keeps its OSM direction (wayOrder in the config); the DEM put it the wrong way round.
- Village beginner lifts (Pattes, Le Valléen, Ascenseur des Thermes, Bouchet, Mowgli) are outlying, so they do not become base starts. Princesse is its own sector.
- Five boxes exclude Espace Diamant and Les Saisies, Les Contamines, Prarion, Cordon and the Balme sector of La Clusaz.

## Open points

- Lift count: 114 (M001) against 110 (Saint-Gervais tourist office) against 80 (skiresort.com, two listings added together) and 75 main lifts in the map data. The page shows the sources rather than one figure.
- Portes du Mont-Blanc closing date: 21 March (Alti-Mag domain page) against 4 April 2027 (Alti-Mag La Giettaz page).
- Adult week pass €369 (Saint-Gervais tourist office) against six days at €324.50 (M013). Not reconciled.
- Network checks against the 2026/27 piste map: Rocharbois as the critical link, the red out of Saint-Nicolas, the base tables.
