// Network graph for the Portes du Soleil, as run in a browser console on 20 October 2026.
// Steps: 1. Overpass query; 2. elevations from the Open-Meteo elevation API; 3. graph build; 4. 0/1 BFS on lift rides.
// The exact code run is condensed here; constants match 04_network_graph.md.

const QUERY = `[out:json][timeout:180];(
  way["aerialway"](46.10,6.55,46.36,6.95);
  way["piste:type"="downhill"](46.10,6.55,46.36,6.95);
  relation["piste:type"="downhill"](46.10,6.55,46.36,6.95);
  way["landuse"="winter_sports"](46.10,6.55,46.36,6.95);
  relation["landuse"="winter_sports"](46.10,6.55,46.36,6.95););out tags geom;`;

// Exclude Praz de Lys Sommand, Bernex and Les Giettes (inside the box, not in the domain)
const excluded = (lat, lon) => (lat < 46.176 && lon < 6.600) || (lat > 46.334 && lon < 6.72) || lon > 6.94;

// Working sector centres; each lift and piste is assigned to the nearest centre
const SECTORS = {
  "mont-chery": [46.165, 6.652], "les-gets": [46.148, 6.684], "nyon-pointe": [46.152, 6.716], "pleney": [46.170, 6.697],
  "super-morzine": [46.192, 6.725], "avoriaz": [46.188, 6.775], "lindarets-brochaux": [46.205, 6.783],
  "linga-pre-la-joux": [46.232, 6.805], "super-chatel": [46.268, 6.857], "champoussin": [46.212, 6.860],
  "les-crosets": [46.180, 6.828], "champery-planachaux": [46.170, 6.846], "torgon": [46.300, 6.848],
  "la-chapelle": [46.282, 6.773], "abondance": [46.265, 6.708], "roc-d-enfer": [46.208, 6.605],
  "morgins-foilleuse": [46.228, 6.864], "morgins-corbeau": [46.246, 6.866], "panthiaz-braitaz": [46.300, 6.812],
};

// Village transfers added by hand (walk, bus or road train), both directions
const TRANSFERS = [
  ["Morzine: Pléney to Super-Morzine", [46.1799, 6.70194], [46.18355, 6.70354]],
  ["Les Gets: Mont Chéry to Chavannes", [46.16077, 6.66976], [46.15696, 6.66873]],
  ["Morgins: Foilleuse to Corbeau", [46.23669, 6.85812], [46.24114, 6.85424]],
];

// Graph rules
//  - piste vertices snapped within 20 m, lift ends within 40 m
//  - piste edges follow way order (downhill by OSM convention); oneway=no adds the reverse
//  - lift edges bottom to top, oriented by DEM elevation; gondolas and cable cars also get a "ride down" edge
//  - chairlifts with < 30 m height gain are two way (Gabelou)
//  - walk edges both ways between a lift end and any node within 80 m
// Cost: lift and ride down edges 1, everything else 0. Minimum lift rides by 0/1 breadth first search.
// Critical lift test: remove one lift (> 300 m, not a carpet or rope tow) at a time and count ordered
// sector pairs that become unreachable and the extra lift rides for pairs that stay reachable.
// Ability test: piste edges limited to OSM piste:difficulty in {novice, easy} (green and blue),
// then {novice, easy, intermediate} (up to red), then all.
