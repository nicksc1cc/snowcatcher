# Evidence register, coverage and research backlog

Deliverables 9 (evidence register), 10 (coverage matrix) and 11 (backlog). Files: `data/evidence_register.csv` (55 records), `data/coverage_matrix.csv`, `data/question_bank.csv`.

## 1. Evidence register

55 records from 20 October 2026: 32 from official operator sources, 13 from skiresort.com, 7 from open data and modelled weather (OpenStreetMap, the elevation model, ERA5) and 3 from provider terms and documentation. Each carries value, unit, scope, period, source, URL, data type, confidence and retrieval date.

### Unresolved conflicts

| Conflict | Values found | Sources | Working position |
|---|---|---|---|
| Piste length | 600 km; 580 km measured; 650 km; 428 km in OpenStreetMap | Official site; skiresort.com; Les Gets lift company and skiresort.com body text; OpenStreetMap | Quote 600 km as the operator's figure and 580 km as measured, always together. Ask the operator for its method. |
| Number of runs | 307; 308; 296 | Three pages of the official site | 307 with the colour split (39, 130, 105, 33) is the only figure with a breakdown. |
| Number of lifts | 208; 209; 202; 163 | Official pages; skiresort.com (linked area only) | Operator counts include the pass only resorts; skiresort.com counts the linked area. Publish both with their scope. |
| Snowparks | 30 "snowparks, boarder cross and ski cross"; 10 snowparks | Two official pages | Different definitions; list parks by name instead. |
| Altitude range | 900 to 2,460 m; 985 to 2,254 m; lift tops to 2,243 m in the elevation model | Official; skiresort.com; DEM | 2,460 m is not reached by any lift in OpenStreetMap; check whether it is a summit rather than a lift top. |
| Season dates | 11 Dec; 19 Dec; 28 Nov 2026 to 18 Apr 2027; Les Gets-Morzine closes 11 Apr | Pass page; openings page; skiresort.com; Les Gets | Domain pass valid 11 Dec (price period); main opening 19 Dec; resorts differ. Show dates by resort. |
| Day pass, adult | EUR 73 office, 69 online; EUR 72 | Official PDF; skiresort.com | Use the official PDF. |
| Pass only resorts | Abondance, La Chapelle, Saint-Jean-d'Aulps (skiresort.com); model shows La Chapelle's Panthiaz gondola links to Torgon | skiresort.com; OpenStreetMap graph | La Chapelle is split: Crêt Béni pass only, Panthiaz linked one way. Verify on the map. |

## 2. Coverage by page section

| Page section | Questions | Evidenced | Disputed | Researching | Unresearched | Priority 1 still unresearched |
|---|---|---|---|---|---|---|
| How the network works | 337 | 47 | 0 | 152 | 138 | 26 |
| Sector comparison | 323 | 57 | 0 | 95 | 171 | 38 |
| Who the domain suits | 176 | 1 | 0 | 37 | 138 | 74 |
| Where to stay | 128 | 0 | 0 | 64 | 64 | 64 |
| Terrain and mountain character | 102 | 3 | 1 | 38 | 60 | 0 |
| Snow and weather intelligence | 96 | 9 | 0 | 27 | 60 | 38 |
| Food, après and non skiing | 58 | 0 | 0 | 3 | 55 | 0 |
| Getting around | 39 | 0 | 0 | 0 | 39 | 4 |
| Pass value and usable terrain | 39 | 9 | 0 | 25 | 5 | 2 |
| Research notes and data freshness | 13 | 3 | 2 | 4 | 4 | 1 |
| Domain overview | 10 | 5 | 2 | 2 | 1 | 0 |
| Trade offs and limitations | 4 | 0 | 0 | 0 | 4 | 3 |

"Evidenced" in this pass often means "answered by the OpenStreetMap model" and still needs checking against the official map before it can support public copy.

## 3. Backlog (ordered by traveller value, then uncertainty, then data availability)

| # | Task | Why it matters | Data | Effort |
|---|---|---|---|---|
| 1 | Check the network model against the official 2026/27 piste map: the two network split at Morzine, pass only status, the one way Panthiaz link, every "no ski home" base, the critical lifts | Underpins every network, base and pass claim | Official map (PDF) | Medium |
| 2 | Confirm the Morzine, Les Gets and Morgins village crossings: walk, bus or road train, distance and time | Decides whether Les Gets and Morzine are good bases for the whole domain | Tourist offices, bus timetables | Low |
| 3 | Last lift times for the return to each base, 2026/27 | Stranding risk across the domain | Lift companies | Low |
| 4 | Local pass prices for Avoriaz and Châtel, any day extension, and pass only resort prices | Completes the pass value test | Lift companies | Low |
| 5 | ERA5-Land snow depth for the three or four cells over the domain; days above 30, 50 and 100 cm | First snow depth evidence | Open-Meteo or Copernicus CDS | Low (blocked by API quota this pass) |
| 6 | Nearby measuring stations (IMIS, MeteoSwiss, Météo-France) and a bias check of ERA5-Land | Turns modelled snow into checked snow | Station portals | Medium |
| 7 | Snowmaking coverage by sector and on the link runs | Low sector reliability | Operators, Domaines Skiables de France | Medium |
| 8 | Wind exposure and historical closure frequency of the critical lifts | Practical size of the network on bad days | Operator status archive (start collecting now), reviews | High, slow |
| 9 | Ride times and piste lengths on the graph, so routes become journey times | End to end feasibility | OpenStreetMap durations, lift company data | Medium |
| 10 | Difficulty of every link run, with OpenStreetMap tags checked against the map | Ability routing | Official map | Medium |
| 11 | Flat traverses and drag lift dependencies for snowboarders | Snowboarder suitability | Map, reviews, site visit | Medium |
| 12 | Transfers from Geneva and rail access by base | Getting there | Transport operators | Low |
| 13 | Beginner zones, ski schools and childcare by base | Family and beginner advice | Resorts | Medium |
| 14 | Licensing decision for weather data (Open-Meteo paid plan or Copernicus) | Required before public snow charts | Provider terms | Low |
| 15 | Daily collection of snow reports, lift status and forecasts from December | Current conditions panel and closure history | Pipeline in 02 | Medium |
| 16 | Aspect and tree cover by sector from the elevation model and land cover | Sector snow and visibility character | DEM, land cover | Medium |
| 17 | Mountain restaurants, après and non ski activities by sector | Trip planning | Tourist offices | Medium |
| 18 | Dated review sample by theme and sector | Visitor experience | Review sites | High |
| 19 | Forecast validation using archived forecasts | Confidence labels | Open-Meteo historical forecast API | Medium |
