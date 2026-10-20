# Portes du Soleil: full landing page and comparison research (20 October 2026)

The page now follows all 13 sections of the Level 3 framework and is built from a shared template in nicksc1cc/projectsnow:
content in `src/data/l3/portes-du-soleil.json` (each block lists its evidence ids), graphics in `src/_data/l3.js`,
layout in `src/l3-domain.njk`, network explorer in `src/assets/l3-network.js`.

## New evidence (E056 to E069 in data/evidence_register.csv)
- Comparison areas chosen by Nick: the large linked areas nearest Geneva (Grand Massif, Évasion Mont Blanc, 4 Vallées).
- Every comparison row uses one source for all four areas: skiresort.com listings (size, lifts, heights, grade split, day ticket),
  ERA5 via Open-Meteo with models=era5 (one cell per area, 1,600 m, Nov to Apr, median 1991/92 to 2020/21; Portes du Soleil reproduces 285 cm),
  OSRM router on OpenStreetMap for road distance from Geneva airport.
- Note: the default Open-Meteo model (best_match) gives 329 cm for the Portes du Soleil cell; always pass models=era5.
- Access: Portes du Soleil access page, Altibus (Y91, Y92), Châtel tourist office (line 12, VEX), Morzine shuttles (2022 timetables, low confidence),
  Région Dents du Midi (AOMC train at the cable car), Avoriaz (car free, Prodains Express).

## Sample routes and ability
- Taken directly from the min lift ride and ability matrices; matrix values cannot be chained, because each counts from the best lift base in a sector.
- Finding: in the map data every one of the 11 main sectors reaches every other without a black run.

## Still open
- Ski bus to the pass only areas: free with the pass or not.
- 2026/27 timetables; flat sections for snowboarders; reviews; crowds; snow depth; network check against the official map.
