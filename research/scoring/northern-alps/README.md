# Northern Alps scoring, method v1

Pilot of the Snow Catchers scoring method (Claude Docs: Snow Catchers resort scoring method) on every Northern Alps resort with downhill skiing.

| File | Contents |
|---|---|
| altimag_stations.csv | The 124 stations Alti-Mag lists for the Northern Alps (retrieved 25 October 2026), with base and top heights and alpine and nordic km |
| resorts.csv | The 113 with alpine skiing, each with the base point used for scoring (OpenStreetMap place, or the ski area outline where no village fits) |
| data/access.csv | OSRM road time and distance from Geneva, Lyon, Chambéry and Grenoble airports, run 25 October 2026 |
| score_v1.py | Turns the raw measures into scores against the v1 anchors |
| ../../../db/model/bulk.js | Browser script for the OpenStreetMap measures: reachable km by level, lifts, vertical, resilience, venues, ski in and ski out |

## Status, 25 October 2026

- Resort list and base points: done. Points checked by hand where the name match was doubtful (17 overrides).
- Road access: done for all 113.
- Snow: 16 resorts fetched, then Open-Meteo's hourly limit stopped the run. The default model mixes sources, so older seasons came back the same at every height; the rerun should use models=era5, as the domain pages did, and fetch per height band rather than per resort to stay inside the limit.
- OpenStreetMap download: 20 of 36 tiles fetched when the computer running the browser went offline. The tiles were held in the browser, so the run starts again from the first tile.

## Known issues

- Valmorel's point is the ski area centre on the mountain, which gives an odd road route (186 minutes from Geneva for 136 km). Move it to the village before the final run.
- Linked resorts take Alti-Mag's domain figures for top height and km; scoring uses the mapped network instead.
