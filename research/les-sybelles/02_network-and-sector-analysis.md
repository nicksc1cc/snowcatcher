# Les Sybelles — network and sector analysis

**Research date:** 21 October 2026  
**Status:** First-pass synthesis; topology requires map verification.

## Current network interpretation

The domain's main connected skiing is organised around the high ground of the Ouillon and the ridges between the Arvan valley resorts. The core sectors to model are:

- Le Corbier
- La Toussuire
- Saint-Jean-d'Arves
- Saint-Sorlin-d'Arves
- Les Bottières

The operator's site also lists Saint-Colomban-des-Villards among six resorts. However, an independent resort guide states that its ski link with Les Sybelles was no longer maintained from winter 2025–26. This makes Saint-Colomban a high-priority exception: it must not be drawn as a continuous ski link in the network diagram unless the 2026–27 official map and operator confirm a reinstated link.

## What is known

- The operator markets 310 km of piste and lists six resort names on its general site.
- The official ski-map page says the interactive map shows six resorts and current lift/piste status.
- Saint-Sorlin-d'Arves' official resort page describes the linked ski area as Saint-Sorlin, Saint-Jean-d'Arves, Le Corbier, La Toussuire and Les Bottières; it gives Saint-Sorlin's sector as 1,500–2,620 m with 41 marked pistes and 18 lifts.
- La Toussuire's official page describes the main five-resort network and gives the wider area as 1,300–2,620 m.
- The winter 2025–26 press-kit map labels 136 pistes, 68 lifts and an altitude range of 1,100–2,620 m, but that document predates the 2026–27 season and includes Saint-Colomban. Do not mix those totals with the current connected-core count without scope notes.
- Official 2026–27 season messaging advertises opening from 12 December 2026 to 9 April 2027. These are planned dates, not a guarantee that every sector or connection opens on those dates.

## Network questions still open

1. Does the 2026–27 official map show any maintained ski link from Saint-Colomban to the main network?
2. Is Saint-Colomban covered by the current Sybelles full-domain pass despite the discontinued link?
3. What is the current linked-core piste total, lift count and run count excluding Saint-Colomban?
4. Which named lifts make the links between the five core sectors, and which are single points of failure?
5. What are the shortest routes and minimum lift rides between each base and the other sectors?
6. Which links can be skied on green/blue runs, and which require a red?
7. Are the routes symmetric? Check for one-way links, lifts that can be ridden down, and no-piste-return bases.
8. Does the map data cover all pistes and lifts, and what is its licence and snapshot date?
9. Can the route model be checked against the current official piste map rather than only against OSM topology?

## Model rules

- Use a graph whose nodes are lift bases, lift tops, piste junctions and base villages; edges distinguish lift, piste, walk, bus and gondola ride-down.
- Record edge direction, difficulty, lift type, operating dependency and source.
- Calculate shortest lift rides separately from elapsed time. Ride count is not journey time.
- Mark route and grade results as provisional until checked against the official map.
- Treat a disconnected sector as disconnected; do not fill missing matrix cells with invented route counts.
- Do not include a network-ability matrix on the public page until the model can be reproduced and validated.
