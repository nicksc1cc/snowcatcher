# Scoring pipeline runbook

How to score a range of resorts with the Snow Catchers method (v1.1). The Northern Alps run in `northern-alps/` is the worked example; a new range is a new folder with its own `config.json`.

## 1. Resort list and base points

1. Save the station list for the range (France: the Alti-Mag range page) as `altimag_stations.csv`, then keep stations with alpine km in `resorts.csv`.
2. Match each station to an OpenStreetMap place (village, hamlet or locality) by name, preferring the candidate nearest an aerial lift station.
3. Check by hand any match more than 1 km from a lift, or a name that repeats. Record the reason in `osm_ref`.
4. After the network download (step 2), move any base point with no main lift within 800 m to the main lift bottom within 5 km closest to the station's published base height. `resorts.csv` keeps the original reference.

## 2. Map measures (browser)

The research workspace cannot reach Overpass, Open-Meteo, OSRM or the elevation tiles, so these steps run in the built-in browser on a page such as https://example.com. Load `db/model/bulk.js` from GitHub by commit, then:

```js
await SCBulk.fetch(bbox, 6)             // lifts, pistes, venues, places to stay; lift heights
const m1 = SCBulk.measure(resorts)      // km by level, lifts, drags, vertical, resilience, venues, ski in and out
await SCBulk.extra(bbox, 6)             // trails, piste outlines, leisure, culture, shops, schools, hire
await SCBulk.demTiles(50, 13)           // piste gradient from AWS terrarium tiles: flat and steep km
const m2 = SCBulk.measure2(resorts)     // capacity, flat and steep km by level, trails and facilities
const op = await SCBulk.offpiste(bbox, 1, resorts)   // glaciers and mapped freeride routes near reachable lift tops
const acc = await SCBulk.access(resorts, airports)   // OSRM road time
```

Copy the results into `data/measures_raw.csv`, `data/measures2.json`, `data/offpiste_map.json` and `data/access.csv`.

Known limits: Overpass is often busy (502, 504, 429) and the browser slows hidden pages, so keep the browser pane visible. The Open-Meteo elevation API allows about 5,000 points an hour, so gradients use the terrarium tiles instead (DEMTiles in bulk.js).

## 3. Researched inputs

| File | What | Source (France) |
|---|---|---|
| data/altimag_prices.csv | Day, six day and season pass for every pass listed at the station | Alti-Mag station pages |
| data/parks.json | Snow park count and area within 6 km | OpenStreetMap, to be checked against resort park pages |
| data/apres_sources.csv, apres_mentions.csv, apres_verdicts.csv, apres_events.csv | Après reputation, named venues, clubs, slope après, guide verdicts, festivals | Nine guides, Snowcarbon resort pages, La Folie Douce |
| data/offpiste_sources.csv, offpiste_mentions.csv, offpiste_domains.csv | Guides naming each resort for off piste and the routes they name. Credit a route to the village whose lifts reach it, not the heading it sits under, and note the move. A domain named without a village gives each member half a mention | Thirteen guides in English and French, Powderhounds Best for Powder and Secret Stashes lists |
| data/michelin_2026.csv | Stars and Bib Gourmand | Michelin area pages |
| data/gaultmillau.csv | Toques and scores | Gault&Millau via Alti-Mag, Gault&Millau Savoie |

Every row carries its source. Passes that do not cover the lifts at the scored base go in `NOT_AT_BASE` in `score_v11.py`.

## 4. Score

```
python3 score_v11.py
```

writes `out/scores_v11.csv` (every measure score and raw value) and `out/lists_v11.md` (the nine audiences and the extra lists in `audiences.json` and `lists.json`).

## 5. Checks before anything is published

- Base points moved or overridden (listed in `resorts.csv`).
- Resorts with under 3 km of mapped piste.
- Passes that cover a different network from the base.
- Neighbouring villages within 1.5 km of each other, which share bars and restaurants.
- Michelin or Gault&Millau pages that failed to load, and conflicts with published pages (`data/michelin_conflicts.csv`).
- Snow: not yet scored. ERA5 through Open-Meteo flattens above about 2,000 m; the plan is Météo-France S2M for France or Copernicus CERRA for every country.

## A new range or country

Copy `northern-alps/config.json` and change the station list source, bbox, airports, currency and school holidays. Country specific sources to find: a station list with prices (Austria and Switzerland: Bergfex or skiresort.info), après guides, food guides (Gault&Millau publishes in Austria and Switzerland too) and tourist bed counts.
