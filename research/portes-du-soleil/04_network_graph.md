# Network graph: specification and first results

Status: first pass, 20 October 2026. Every result below comes from OpenStreetMap and must be checked against the official 2026/27 piste map and lift opening data before it is used on a public page.

## 1. Data

| Item | Source | Notes |
|---|---|---|
| Lifts and pistes | OpenStreetMap via Overpass API, snapshot 2026-10-20T07:23:10Z | Ways tagged `aerialway=*` and `piste:type=downhill`, plus `landuse=winter_sports` areas. Licence ODbL; attribution "© OpenStreetMap contributors" required on any public map or derived graphic. |
| Bounding box | 46.10 to 46.36 N, 6.55 to 6.95 E | Praz de Lys Sommand, Bernex and Les Giettes fall inside the box and are excluded. |
| Elevation | Open-Meteo elevation API (Copernicus DEM GLO-90, 90 m) | Sampled at both ends of every lift and every open piste way: 1,451 points. |

Extracted after exclusions: 196 lifts (including magic carpets and rope tows) and 1,133 piste ways, 427.6 km of open piste geometry. The official figure is 600 km and skiresort.com's measured figure 580 km, so the OpenStreetMap piste layer is incomplete or measured differently. Lift positions are more complete than piste geometry.

## 2. Graph model

* **Nodes:** every vertex of every piste way and both ends of every lift, snapped together within 20 m (40 m for lift ends). 8,252 nodes.
* **Piste edges:** directed from first to last vertex of each way, which in OpenStreetMap convention runs downhill. Checked against the DEM: 955 ways run downhill end to end, 66 appear to rise (mostly short connectors and traverses), 151 could not be checked.
* **Lift edges:** directed bottom to top, oriented by DEM elevation. Gondolas and cable cars also carry a "ride down" edge, used only in the scenario that allows it. Chairlifts with less than 30 m of height gain (Gabelou in Châtel) are treated as two way.
* **Walk edges:** both ways between a lift end and any node within 80 m.
* **Village transfers:** three walks or bus rides added by hand, each about 400 to 600 m between lift bases: Morzine (Pléney to Super-Morzine), Les Gets (Mont Chéry to Chavannes), Morgins (Foilleuse to Corbeau). Their real form (walk, bus, road train, ski path) still needs checking.
* **Sectors:** 19 working sectors, each lift assigned to the nearest sector centre. These are analysis units, not the domain's official sector names.

Cost of a route = number of lift rides. Routes are found with a 0/1 breadth first search (pistes and walks cost 0, lifts cost 1).

## 3. Findings to verify

1. **Three resorts are pass only.** Abondance, the Crêt Béni side of La Chapelle d'Abondance and Saint-Jean-d'Aulps (Roc d'Enfer) have no lift or piste connection to the rest of the network. This agrees with skiresort.com ("can only be reached by ski bus").
2. **La Chapelle's Panthiaz gondola is the exception.** It reaches Torgon by the Braitaz chairlift, so La Chapelle has one lift link into the network. No piste returns to Panthiaz, which agrees with skiresort.com's note that Panthiaz has no valley run. Skiers based there must ride back down or take a bus.
3. **The domain is two networks joined through Morzine.** The Les Gets and Morzine side (Mont Chéry, Chavannes, Nyon, Pléney) and the Avoriaz and Swiss side have no lift or piste link. They meet only at Morzine, where a walk or bus joins the Pléney and Super-Morzine bases. Coming back from Avoriaz needs a ride down the Super-Morzine or Prodains gondola, because no piste reaches the Super-Morzine base (again matching skiresort.com).
4. **Critical lifts.** Removing one lift at a time, the lifts whose closure disconnects the most sector pairs are:

| Lift | Type | Connection it carries | Ordered sector pairs lost |
|---|---|---|---|
| Super-Morzine | gondola | Morzine to Avoriaz side | 92 |
| Séraussaix | chairlift | Avoriaz back towards Super-Morzine | 55 |
| Proclou | chairlift | Super-Morzine side up to Avoriaz | 55 |
| Pointe de l'Au | chairlift | Champoussin to Les Crosets | 50 |
| Bochasses | chairlift | Champoussin, on the Morgins to Les Crosets route | 44 |
| Zore | chairlift | Super-Morzine plateau towards Avoriaz | 44 |
| Aiguille des Champeys | chairlift | Champoussin towards Les Crosets | 40 |
| Morgins-Foilleuse | gondola | Morgins to Champoussin | 36 |
| Morclan | chairlift | Super-Châtel towards Torgon | 26 |
| Chaux Fleurie | chairlift | Les Lindarets towards Châtel | 13 |

Lifts whose closure leaves everything reachable but adds many lift rides include Corbeau (Morgins to Châtel), Mossettes and Rochassons (Les Lindarets to Switzerland and Châtel), Barbossine and Pléney.

5. **Crossing the domain.** From Mont Chéry in Les Gets, reaching Super-Châtel takes at least 8 lift rides and Torgon 9; from Les Gets to Champéry 5. skiresort.com counts 15 lifts one way and 14 the other to cross the whole area, which uses a different end to end route.

These numbers are minimum lift counts on the modelled network, not times. They ignore opening hours, last lift times and closures.

## 4. Next steps

* Check every finding against the official piste map, the domain's lift status page and each resort's map.
* Add ride times (OpenStreetMap `aerialway:duration` exists for about half the lifts) and piste lengths to turn lift counts into journey times.
* Record which link pistes are red or black, so routes can be filtered by ability; OpenStreetMap difficulty tags exist for most ways.
* Model weather closures: exposed lifts above 2,000 m (Mossettes, Chavanette, Cuboré, Pointe de l'Au, Fornet) are candidates.
* Replace the 19 working sectors with official sector names.
