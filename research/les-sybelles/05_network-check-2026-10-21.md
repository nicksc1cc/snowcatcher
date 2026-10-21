# Les Sybelles — network check, 21 October 2026

**Decision:** publish the five-sector core and show Saint-Colomban-des-Villards as a planned but unverified reconnection. Do not treat the sixth sector as currently ski-linked, and do not publish route metrics yet.

## What the sources establish

1. **Five-sector connected core.** The official Saint-Sorlin-d’Arves ski-area page explicitly defines the Sybelles linked area as Saint-Sorlin-d’Arves, Saint-Jean-d’Arves, Le Corbier, La Toussuire and Les Bottières. It reports the local Saint-Sorlin sector as 1,500–2,620 m, 41 marked pistes and 18 lifts. Those counts are local-sector figures, not domain totals.
   - https://www.saintsorlindarves.com/en/skiing-sliding/ski-area

2. **The Saint-Colomban link was not operating in 2025–26.** The local tourism-office page for the previous winter said the ski link with Les Sybelles would no longer be maintained from winter 2025–26, and described a reduced local beginner offer.
   - https://www.tourisme-la-chambre.com/en/tourisme/activities/saint-colomban-des-villards-79704

3. **A restart is being prepared for 2026–27.** Newer local-authority pages say the commune is preparing the return of the link, with major inspections of the Ormet and Charmette chairlifts and maintenance work underway. Published dates list a planned opening from 19 December 2026 to 27 March 2027. This is evidence of intent and preparation, not confirmation that the link is operational or that the full Sybelles pass covers it.
   - https://www.tourisme-la-chambre.com/fr/tourisme/activites/domaine-skiable-saint-colomban-des-villards-79704
   - https://www.maurienne-tourisme.com/domaine_skiable/domaine-skiable-saint-colomban-des-villards-79704/

4. **There is a material counter-signal.** Saint-Sorlin-d’Arves municipal council minutes from 26 February 2026 record the proposed 2026–27 Sybelles price increase being refused partly because the domain had only five ski areas after Saint-Colomban’s closure in December 2025. This does not disprove the later restart effort; it means the planned reopening must not be described as complete without current operational confirmation.
   - https://mairie-saintsorlindarves.fr/wp-content/uploads/2026/03/LISTE-DES-DELIBERATIONS-CM-DU-26-02-2026.pdf

5. **A current-season map is listed, but not yet inspected.** The Saint-Jean-d’Arves tourist-office brochure page search result lists a 6.98 MB 2026–27 Les Sybelles piste map. The page body available to this research session still rendered the 2025–26 document, so the current PDF asset URL and map geometry have not been verified.
   - https://www.sja73.com/brochures.html

6. **The operator’s interactive map is the live operational reference.** It reports current lift and piste status. At the 21 October 2026 snapshot, the domain was out of season. The live map does not settle future operating status in advance.
   - https://www.sybelles.ski/en/skiing-in-les-sybelles/ski-map/
   - https://www.sybelles.ski/en/skiing-in-les-sybelles/slopes-and-lifts-open/

## Network model decision

| Item | Decision |
|---|---|
| Le Corbier, La Toussuire, Saint-Jean-d’Arves, Saint-Sorlin-d’Arves, Les Bottières | Treat as the named connected core, following the official Saint-Sorlin page |
| Saint-Colomban-des-Villards | Show separately as **connection unverified; reconnection planned for 2026–27** |
| Exact direct sector-to-sector edges | Not published until the current map is inspected and graph edges are checked |
| Lift-ride counts and route times | Withheld |
| Easiest route grade / green-blue reachability | Withheld |
| Critical lift and closure alternatives | Withheld |
| Full-domain pass validity for Saint-Colomban | Confirm directly with the operator before stating |

## Page implementation

The production Level 3 data file is src/data/l3/les-sybelles.json in nicksc1cc/projectsnow. It presents the verified five-sector core, keeps Saint-Colomban visually distinct, uses current 2026–27 pass-rate evidence with a checkout caveat, and omits unsupported route and snow-history metrics.

The page is structurally produced, but the exact network graph remains an explicit QA item. This is preferable to inventing a route matrix from sector names or an uninspected PDF.

## Next network verification step

Recover the actual 2026–27 PDF from the tourist-office document service or obtain the official map-data snapshot. Then:

1. Record all lift and piste IDs, names, grades, directions, lengths and endpoint coordinates/elevations.
2. Validate the snapshot date, map ID and sector coverage.
3. Build a graph with lift nodes and piste edges; keep pedestrian transfers and road transfers as distinct edge types.
4. Compare every cross-sector connection against the official map.
5. Calculate routes in both directions and test ability constraints and critical-lift closures.
6. Ask the lift operator to confirm whether Saint-Colomban's reopening and full-pass coverage are in force before the season opens.
