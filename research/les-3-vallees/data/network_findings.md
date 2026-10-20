# Les 3 Vallées network: first pass, 20 October 2026

Data: OpenStreetMap via Overpass, snapshot 2026-10-20T15:39:51Z, bbox 45.20 to 45.47 N, 6.45 to 6.70 E, excluding lon >= 6.69 (Champagny, Valfréjus), lat < 45.205 (Bissorte) and lon < 6.47 (Valmorel, Télégraphe). 167 lifts kept, 132 main lifts (no carpets or rope tows), 1,649 piste ways of which 523 are areas (not used in the graph); 547 km of open piste ways in the graph. Lift end heights from the Open-Meteo elevation API (Copernicus GLO-90).

Model as in research/portes-du-soleil/04_network_graph.md (20 m piste snap, 40 m lift snap, 80 m walk edges, gondolas and cable cars ride down at cost 1). One transfer added by hand: the Olympe 3 top station to the Chaudanne lift bases in Méribel (Rhodos 1, Saulire Express 1, Tougnète 1, Legends), 340 to 440 m. Starts are village lift bases: lifts whose bottom is within 200 m of the lowest main lift in the sector. Targets are any main lift base in the sector.

Sectors (working, by nearest centre to the lift bottom): Le Praz, La Tania, Courchevel 1550, Courchevel 1850, Courchevel Moriond (1650), Brides-les-Bains, Méribel, Méribel-Mottaret, Saint-Martin-de-Belleville, Les Menuires, Val Thorens, Orelle (Peyron, Bouchet, Marmottons and Orelle-Caron assigned to Orelle by hand).

Findings to check against the official piste map:
1. Up to red equals all runs: no pair of sectors needs a black run.
2. Green and blue alone reach every sector; it usually costs one to three extra lift rides.
3. Longest crossings: Moriond to Orelle 8 lift rides (10 on green and blue); Courchevel 1850 to Val Thorens 4, and 4 back.
4. Single lift links: Brides-les-Bains depends on the Olympe gondola (three sections); Saint-Martin on Saint Martin 1 and the Saint Martin Express; Orelle village on the Orelle gondola. No piste returns to Brides or to Orelle village.
5. Lifts that add most rides when closed (sum over ordered pairs): Plattières +28, Dou des Lanches +20, Côte Brune +16, Saulire Express 1 +15, Saulire +12, Grand Fond +11, Mont de la Chambre +8, Doron +8, Forêt +8.
6. Base table (to Courchevel 1850, Méribel, Val Thorens, top of a lift reaching 2,800 m): Le Praz 2,2,5,5; La Tania 2,2,5,5; Courchevel 1550 1,3,5,5; Courchevel 1850 0,2,4,4; Moriond 2,4,6,6; Brides 5,2,6,6; Méribel 2,0,3,3; Mottaret 2,0,2,2; Saint-Martin 4,2,4,4; Les Menuires 4,2,2,2; Val Thorens 4,2,0,1; Orelle 6,4,2,2.
7. Mapped piste by resort (open ways only, sector by nearest centre, so rough): Courchevel 135 km, 57% green and blue, 41% of 41 main lifts are drags; Méribel 142 km, 55%, 25% drags; Les Menuires 94 km, 68%, 15%; Val Thorens 147 km, 55%, 15%; La Tania 13 km; Saint-Martin 11 km; Orelle 5 km; Brides none. Whole area: 35 of 132 main lifts are drags.
8. DEM heights by sector (lowest main lift base to highest top): Le Praz 1,262 to 1,884; La Tania 1,347 to 2,300; 1550 1,469 to 2,171; 1850 1,741 to 2,666; Moriond 1,522 to 2,540; Brides 628 to 1,317; Méribel 1,317 to 2,666; Mottaret 1,674 to 2,888; Saint-Martin 1,379 to 2,380; Les Menuires 1,564 to 2,831; Val Thorens 2,048 to 2,985; Orelle 897 to 3,211.

Route checks: Courchevel 1850 to Val Thorens: Saulire, Plattières, Côte Brune. Val Thorens to Courchevel 1850: Funitel 3 Vallées, Pas du Lac 1, Pas du Lac 2. Le Praz to Orelle: Forêt, Dou des Lanches, Legends, Plattières, Côte Brune, Deux Lacs, Grand Fond.
