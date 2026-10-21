# Les Sybelles — publication QA and remaining work

**Status:** Not publication-ready  
**Last checked:** 21 October 2026

## Blocking issues

- [ ] Confirm the 2026–27 official lift/piste map and the current status of every main inter-sector connection.
- [ ] Confirm whether Saint-Colomban-des-Villards remains disconnected from the main ski network and whether the full Sybelles pass covers its local lifts.
- [ ] Resolve the scope of the operator's 310 km, 136-piste and 68-lift figures for the current season; do not mix the winter 2025–26 press-kit figures with a 2026–27 connected-core model.
- [ ] Verify the adult six-day 2026–27 pass price in the operator's current checkout or official rate sheet. A third-party price tracker reports €307.20; the operator's accessible public page currently exposes a dynamic “from” price.
- [ ] Build a reproducible lift/piste graph from a dated data snapshot, document OSM completeness and licence, then check it against the official piste map.
- [ ] Calculate base-to-sector reach and ability matrices only after the graph is verified.
- [ ] Build snow history by comparable elevation bands; keep snowfall separate from snow depth and compare model values with observations where possible.
- [ ] Confirm current 2026–27 opening dates by sector and avoid treating published plans as guarantees.
- [ ] Verify current transport information by base and season before including journey times.
- [ ] Run the Eleventy build, HTML/data validation, internal-link checks, and rendered desktop/mobile QA.

## Editorial QA

- [x] Level 3 page job is distinct from resort/village pages.
- [x] Meaning map separates physical network from commercial domain identity.
- [x] Known contradiction around Saint-Colomban is visible rather than smoothed over.
- [x] Marketing figure is labelled as operator-published, not independent measurement.
- [x] No unsupported snow-reliability statistics have been added.
- [ ] Every material public claim mapped to an evidence ID in the production JSON.
- [ ] Compare table uses matched sources and definitions.
- [ ] Final repetition and narrative edit.
- [ ] Human approval before publication.

## Next actions in order

1. Obtain the current 2026–27 piste map and confirm the Saint-Colomban link/pass status with the operator.
2. Complete the core network graph and sector metric table.
3. Confirm adult and sector pass prices from the current official rate sheet.
4. Build snow history and source metadata, or omit numeric snow claims until complete.
5. Update production page data and generate a claim-to-copy report.
6. Build, inspect rendered HTML and mobile layout, then request publication approval.
