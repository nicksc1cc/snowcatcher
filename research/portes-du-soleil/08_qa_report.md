# QA report

Deliverable 14. First research pass, 20 October 2026.

## 1. Checks run

| Check | Result |
|---|---|
| Arithmetic in the pass comparison (EUR 76 and 28%, EUR 61 and 20%, CHF 7 and 10%) | Recomputed: 76 (27.5%), 61 (19.6%), 7 (10.3%) |
| Network figures quoted in 04 and 05 against `network_graph.json` and `base_access.csv` | Match |
| Snow figures quoted in 03 against `snow_era5_seasons.csv` and `snow_era5_summary.json` | Match; one draft sentence on recent low seasons was corrected after recalculation |
| Question bank duplicates | None (the build script refuses duplicates) |
| Question count | 1,325, above the 1,000 minimum |
| Evidence register completeness | All 55 records have source, URL, period, data type, confidence and retrieval date |
| Text rules in the reports | No em dashes; no hyphenated compounds outside the schema value `traveller-specific` |

## 2. Unsupported or weakly supported claims

| Claim | Where | Problem | Action |
|---|---|---|---|
| Two networks joined only through Morzine | 04, 05, evidence E048 | OpenStreetMap model only | Check on the official map (backlog 1) |
| Critical lift list | 04, E049 | Depends on OpenStreetMap completeness and the 19 working sectors | Check each link on the map; repeat after adding ride times |
| No ski home at Super-Châtel, Nyon and the Champéry cable car | 05 | skiresort.com says valley runs reach almost all bases and names only Super-Morzine and Panthiaz as exceptions | Treat as unconfirmed; check the official map |
| Links needing a red run | 05, `network_ability_matrices.txt` | OpenStreetMap difficulty tags are incomplete | Do not publish until checked |
| Piste km by sector | `sector_matrix.csv` | OpenStreetMap totals 428 km against 600 km official | Use only as relative size until official sector figures are found |
| Snowmaking on all main links | E047 | One independent source; not confirmed by the operator | Ask the operators |
| Snowfall by elevation | 03 | Modelled; one grid cell for the whole domain; elevation adjustment method unconfirmed | Station comparison (backlog 6) |

## 3. Missing data

* ERA5-Land snow depth: the Open-Meteo hourly quota was exhausted by the 76 year snowfall requests, so the snow depth pull is not done.
* No measured station data yet.
* No current conditions: the season has not started and the daily pipeline is not yet running.
* Avoriaz and Châtel local pass prices; pages 2 to 4 of the domain price PDF.
* Village crossing times, last lift times for 2026/27, transfers, buses.
* Aspect, tree cover, wind exposure, restaurants, après, reviews.

## 4. Stale or time limited information

| Item | Valid until |
|---|---|
| Forecast snapshot (`forecast_snapshot_2026-10-20.csv`) | Already historical; kept as a sample of the pipeline output |
| 2026/27 prices | End of the 2026/27 season; late season prices change on 20 March 2027 |
| OpenStreetMap snapshot | Lifts change each autumn (the new Pointe du Chéry chair is not yet in the model) |
| Season dates | Subject to snow; partial openings vary by resort |

## 5. Licensing to resolve before any public use

* Open-Meteo free API is non commercial only; historical data on a commercial site needs a paid plan (the provider's pricing page is inconsistent about which plan).
* OpenStreetMap data is ODbL; any published map or derived graphic must credit "© OpenStreetMap contributors", and a derived database shared publicly must stay under ODbL.
* Station and avalanche data: terms for IMIS, MeteoSwiss and Météo-France products to be read.
* Operator snow reports and webcams: display terms to be agreed.
