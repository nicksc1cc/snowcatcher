"""Builds src/data/l3/les-3-vallees.json for the Snow Catchers site from the research of 20 October 2026.
Every figure is traced in data/evidence_register.csv. Run: python3 build_page_json.py <path to projectsnow>"""
import json, sys

OUT = (sys.argv[1] if len(sys.argv) > 1 else "/home/claude/projectsnow") + "/src/data/l3/les-3-vallees.json"
A = lambda u, t: f'<a href="{u}">{t}</a>'
U = dict(
    l3v="https://press.les3vallees.com/en/guide/in-figures",
    story="https://press.les3vallees.com/en/guide/our-story",
    sr="https://www.skiresort.com/en/ski-resort/les-3-vallees-val-thorens-les-menuires-meribel-courchevel/",
    srtest="https://www.skiresort.com/en/ski-resort/les-3-vallees-val-thorens-les-menuires-meribel-courchevel/test-report/",
    cour="https://www.skipasscourchevel.com/en/skipass-prices-3-vallees",
    skipass="https://www.les3vallees.com/en/skipass",
    menu="https://lesmenuires.com/en/ski-passes",
    meri="https://guide-ski.fr/?p=1221",
    alti="https://www.alti-mag.com/tarifs-forfaits-de-ski/tarifs-forfaits-ski-alpes/tarifs-forfaits-ski-alpes-du-nord",
    parks="https://www.les3vallees.com/en/activities/snowparks-and-fun-zones",
    new="https://www.skiworld.co.uk/blog/?p=15672",
    fam="https://www.les3vallees.com/en/experiences/best-family-activities",
    kids="https://www.les3vallees.com/en/new/kids-co",
    fplus="https://www.france.fr/fr/article/label-ski-famille-plus/",
    stars="https://presse.explore-savoie.com/les-tables-distinguees-2026/",
    terr="https://www.les3vallees.com/en/experiences/restaurant-terraces-3-vallees",
    fest="https://www.les3vallees.com/en/experiences/restaurants-with-festive-atmosphere",
    sng="https://www.skinewgen.com/ski-blog/ski-resorts/best-three-valleys-restaurants/",
    seem="https://www.seemeribel.com/nightlife/apres/apres-ski-in-meribel",
    iglu="https://www.igluski.com/blog/post/best-apres-nightlife-val-thorens",
    scott="https://scottdunn.com/france/guides/courchevel-insiders-guide/bars-and-nightclubs",
    access="https://press.les3vallees.com/en/guide/getting-to-les-3-vallees",
    bus="https://www.les3vallees.com/en/access-map/by-bus/from-moutiers/",
    seat61="https://www.seat61.com/trains-and-routes/eurostar-ski-train.htm",
    live="https://www.les3vallees.com/en/live",
    map="https://www.les3vallees.com/en/fatmap/3vallees.html",
    osm="https://www.openstreetmap.org/copyright",
    elev="https://open-meteo.com/en/docs/elevation-api",
    hist="https://open-meteo.com/en/docs/historical-weather-api",
    osrm="https://project-osrm.org/",
    mf="https://meteofrance.com/meteo-montagne",
)

d = {}
d["_about"] = "Level 3 linked domain page content. Every figure traces to the evidence register in snowcatcher research/les-3-vallees (data/evidence_register.csv); ev lists the record IDs behind each block. Network figures come from an OpenStreetMap model and must be checked against the official 2026/27 piste map."
d["slug"] = "les-3-vallees"; d["permalink"] = "france/les-3-vallees/"; d["nav"] = "france"; d["name"] = "Les 3 Vallées"
d["title"] = "Les 3 Vallées | Linked ski areas | Snow Catchers"
d["description"] = "How Les 3 Vallées fits together, which base reaches which valley, how its snow changes with height, when the full pass pays, and what the area is like for boarders, families, food and evenings."
d["crumbs"] = [{"label": "France", "href": "/projectsnow/france/"}, {"label": "Linked ski areas", "href": "/projectsnow/france/#areas"}, {"label": "Northern Alps", "href": "/projectsnow/france/#range-northern-alps"}]
d["hero"] = {"photo": "hero", "lead": "Three valleys of the Tarentaise share one lift system, from the spa town of Brides-les-Bains at the bottom to the summit above Orelle at 3,230 m. In a single day a skier can start in Courchevel, stop for lunch above Méribel and finish the afternoon in Val Thorens, the highest village in the area. The operator counts 600 km of piste and puts its lowest runs at 1,300 m."}
d["stats"] = [
    {"v": "600 km", "t": "of linked piste on the operator's count, the same figure skiresort.com gives", "ev": ["L001", "L010"]},
    {"v": "3 valleys", "t": "Saint-Bon, Les Allues and Les Belleville, with Orelle reached from the Maurienne", "ev": ["L001", "L020"]},
    {"v": "1,300 to 3,230 m", "t": "from the operator's base height to the top of the area; the Olympe gondola starts lower, at Brides-les-Bains", "ev": ["L001", "L010"]},
    {"v": "€421", "t": "for six days, adult, high season 2026/27; €378.50 in the first and last weeks", "ev": ["L040", "L042"]},
]
d["network"] = {
    "h2": "Three valleys on one ridge line",
    "paras": [
        "The lifts of the three valleys meet along the high ground between them. Courchevel and Méribel share the Saulire and the Col de la Loze; Méribel and the Belleville valley share the ridge from the Tougnète to Mont de la Chambre. Most of the area works as one network, and in the map data a skier starting from the village lifts of Courchevel 1850 reaches Val Thorens in four lift rides and comes back in four.",
        "The middle valley is the one that holds it together. From the lift bases of Méribel every sector except Orelle lies within three lift rides, and from Mottaret within two. A few lifts carry much of that traffic. Closing the Plattières gondola above Mottaret adds more lift rides across the area than closing any other single lift, followed by the Dou des Lanches chair above La Tania, the Côte Brune gondola from Les Menuires and the two Saulire lifts.",
        "Three places hang on a single line of lifts. Brides-les-Bains reaches Méribel only by the Olympe gondola, in three sections, and no piste comes back down to it. Orelle village sits on the far side of the ridge in the Maurienne, linked by a gondola that climbs from about 900 m; skiers come down the same way. Saint-Martin-de-Belleville depends on its gondola and the Saint Martin Express chair above it.",
    ],
    "figs": [
        {"v": "4 lift rides", "t": "from the village lifts of Courchevel 1850 to Val Thorens, and four back"},
        {"v": "No black run", "t": "is needed between any two sectors in the map data"},
        {"v": "8 lift rides", "t": "from the village of Moriond to Orelle, the longest crossing of the area"},
        {"v": "3 places", "t": "hang on one line of lifts: Brides-les-Bains, Saint-Martin and Orelle village"},
        {"v": "1936", "t": "the first sledge lift runs at Les Allues, below Méribel"},
        {"v": "1992", "t": "La Tania is born and Brides-les-Bains joins the area"},
    ],
    "mapTitle": "Explore the network",
    "mapHelp": "Choose a starting point to see how many lift rides it takes to reach each other area, then limit the runs to see what stays within reach.",
    "caption": "Schematic, not to scale, with sectors moved apart for legibility. Built from OpenStreetMap lift and piste data (© OpenStreetMap contributors, snapshot 20 October 2026) with heights from the Copernicus 90 m elevation model. An orange link carries routes that no other link replaces when a single lift on it closes. Lift rides are the fewest needed between the lift bases of two areas. The model is being checked against the official 2026/27 piste map.",
    "ev": ["L020", "L021", "L022", "L023", "L030"],
}


def S(i, n, b, lat, lon, lo, hi, place, short=None):
    x = {"id": i, "name": n, "base": b, "cc": "FR", "lat": lat, "lon": lon, "lo": lo, "hi": hi, "link": "yes", "place": place}
    if short:
        x["short"] = short
    return x


d["sectors"] = [
    S("brides", "Brides-les-Bains", "Brides-les-Bains", 45.462, 6.470, 628, 1317, [0, -20, "middle"], "Brides"),
    S("le-praz", "Le Praz", "Courchevel", 45.465, 6.640, 1262, 1884, [0, -20, "middle"]),
    S("la-tania", "La Tania", "La Tania", 45.445, 6.560, 1347, 2300, [-16, 5, "end"]),
    S("c1550", "Courchevel 1550", "Courchevel", 45.445, 6.730, 1469, 2171, [16, 5, "start"], "Courchevel 1550"),
    S("c1850", "Courchevel 1850", "Courchevel", 45.415, 6.660, 1741, 2666, [0, 32, "middle"], "Courchevel 1850"),
    S("moriond", "Moriond (1650)", "Courchevel", 45.400, 6.760, 1522, 2540, [16, 5, "start"], "Moriond"),
    S("meribel", "Méribel", "Méribel", 45.398, 6.540, 1317, 2666, [-16, 5, "end"]),
    S("saint-martin", "Saint-Martin-de-Belleville", "Saint-Martin-de-Belleville", 45.360, 6.440, 1379, 2380, [-16, 5, "end"], "Saint-Martin"),
    S("mottaret", "Méribel-Mottaret", "Méribel", 45.355, 6.600, 1674, 2888, [16, 5, "start"], "Mottaret"),
    S("menuires", "Les Menuires", "Les Menuires", 45.315, 6.500, 1564, 2831, [-16, 5, "end"]),
    S("val-thorens", "Val Thorens", "Val Thorens", 45.285, 6.620, 2048, 2985, [16, 5, "start"]),
    S("orelle", "Orelle", "Orelle", 45.225, 6.560, 897, 3211, [16, 5, "start"]),
]
d["links"] = [
    ["brides", "meribel", "ride", True, "Olympe gondola, ridden both ways"],
    ["le-praz", "c1850", "lift", False, "Praz gondola"],
    ["le-praz", "la-tania", "lift", False, "Forêt chair"],
    ["c1550", "c1850", "lift", False, "Grangettes gondola"],
    ["c1850", "moriond", "lift", False, ""],
    ["la-tania", "meribel", "lift", False, "Dou des Lanches chair"],
    ["c1850", "meribel", "lift", False, "Saulire and the Saulire Express"],
    ["c1850", "mottaret", "lift", False, "Saulire and Pas du Lac"],
    ["meribel", "mottaret", "lift", False, ""],
    ["meribel", "saint-martin", "lift", True, "Saint Martin 1 and the Saint Martin Express"],
    ["mottaret", "menuires", "lift", False, "Plattières and Côte Brune"],
    ["mottaret", "val-thorens", "lift", False, "Funitel 3 Vallées"],
    ["menuires", "val-thorens", "lift", False, ""],
    ["val-thorens", "orelle", "ride", True, "Orelle gondola, ridden both ways to the village"],
]
d["mapNotes"] = [{"lat": 45.392, "lon": 6.605, "text": "Saulire"}, {"lat": 45.338, "lon": 6.535, "text": "Belleville ridge"}]
d["mapBox"] = {"lon0": 6.40, "lon1": 6.80, "lat0": 45.215, "lat1": 45.475}
d["routes"] = {
    "h3": "Five sample days",
    "intro": "Each trip is counted in lift rides out and back, from the first lift base in each area, with the easiest grade of run that makes it in the map data. The counts start lower than the base table further down, which starts in the village. Time on the pistes, in queues and on foot is not included.",
    "rows": [
        {"from": "Courchevel 1850", "to": "Val Thorens", "out": 3, "back": 3, "grade": "Red", "note": "On green and blue alone the way out takes five lift rides instead of three."},
        {"from": "Méribel", "to": "Val Thorens", "out": 3, "back": 1, "grade": "Green and blue", "note": "The return is a single ride on the Funitel 3 Vallées and a long run down the Méribel side."},
        {"from": "La Tania", "to": "Les Menuires", "out": 3, "back": 2, "grade": "Green and blue", "note": "The route crosses the Méribel valley in both directions."},
        {"from": "Saint-Martin", "to": "Courchevel 1850", "out": 3, "back": 3, "grade": "Red", "note": "Out by the Saint Martin Express and both Saulire Express gondolas; the way back needs a red unless a fourth lift is added."},
        {"from": "Brides-les-Bains", "to": "Orelle", "out": 7, "back": 5, "grade": "Red", "note": "The two ends of the area, each reached by gondola with no piste home."},
    ],
    "after": "Even by this measure the corners of the area are a long way apart: from Moriond, Orelle takes seven lift rides going south and five coming back.",
    "ev": ["L020"],
}


def R(n, net, lo, hi, e, dr, note):
    return {"name": n, "cc": "France", "net": net, "lo": lo, "hi": hi, "easy": e, "drag": dr, "note": note}


d["areas"] = {
    "h2": "The eight resorts compared",
    "intro": "The pass covers places as different as Brides-les-Bains, a spa town with no pistes of its own, and Val Thorens, where every lift starts above 2,000 m. Their place on the ridge decides how quickly the rest of the area can be reached.",
    "caption": "Resorts on the Les 3 Vallées pass",
    "rows": [
        R("Courchevel", "Linked; four villages from Le Praz to 1850", 1262, 2666, 57, 41, "Holds the most drag lifts in the area; the Saulire cable car leaves from 1850."),
        R("La Tania", "Linked, between Courchevel and Méribel", 1347, 2300, None, 40, "Too little mapped piste to compare grades."),
        R("Méribel", "Linked, centre of the area", 1317, 2888, 55, 25, "The Mont Vallon gondola above Mottaret has the highest lift top in the valley."),
        R("Brides-les-Bains", "Linked by the Olympe gondola only", 628, 1317, None, 0, "No pistes; the gondola is ridden both ways."),
        R("Saint-Martin-de-Belleville", "Linked by one gondola and one chair", 1379, 2380, None, 33, "Too little mapped piste to compare grades."),
        R("Les Menuires", "Linked, Belleville valley", 1564, 2831, 68, 15, "The highest share of green and blue among the big resorts."),
        R("Val Thorens", "Linked, head of the Belleville valley", 2048, 2985, 55, 15, "Every lift starts above 2,000 m."),
        R("Orelle", "Linked by gondola from the Maurienne", 897, 3211, None, 0, "The Bouchet chair reaches the highest lift top in the area."),
    ],
    "note": "From the OpenStreetMap lift and piste data (snapshot 20 October 2026) with heights from the Copernicus 90 m elevation model. Green and blue is the share of mapped piste length; drag lifts include platters and T bars as a share of all lifts. Mapped piste is incomplete, so the shares are useful for comparing resorts but not as totals, and they are being checked against the official 2026/27 piste map.",
}
d["terrain"] = {
    "h2": "Blues reach every valley",
    "paras": [
        "The operator counts 337 runs: 50 green, 137 blue, 113 red and 37 black. skiresort.com measures 56% of the piste as easy, 34% as intermediate and 10% as difficult, and lists another 50 km of ski routes.",
        "In the map data, no pair of sectors needs a black run, and every sector can be reached on green and blue alone. The easy way round usually costs one to three extra lift rides: from the lift bases of Courchevel 1850, Val Thorens takes five rides on green and blue against three when reds are allowed, and from Les Menuires, Le Praz takes three against two.",
        "That makes the area unusually forgiving for a group of mixed ability, as long as the group meets in the middle. From Mottaret every sector except Orelle is within two lift rides, so the gentler skiers can stay on the blues of the Méribel valley while the others range out to Courchevel or Val Thorens and come back for lunch.",
        "Stronger skiers have more to find at the top of the lifts than in the run counts. skiresort.com rates the area among its best for experts and freeriders, and the 37 black runs are spread across all three valleys rather than gathered in one corner.",
    ],
    "matrixTitle": "Lift rides between the areas, and the grade they need",
    "matrixNote": "Rows are where the day starts, columns where it goes. Shaded cells can be reached on green and blue runs, and show the fewest lift rides on those runs. Unshaded cells need at least one red, and show the fewest lift rides with reds allowed. From the OpenStreetMap piste grades, snapshot 20 October 2026; untagged or wrongly tagged runs can distort the result, and each one is being checked against the official map.",
    "ev": ["L001", "L010", "L011", "L021"],
}
d["snow"] = {
    "h2": "Height keeps the snow",
    "paras": [
        "Most of the skiing here is high. The operator puts 85% of the area above 1,800 m. In Val Thorens every lift starts above 2,000 m, and above Orelle the Bouchet chair climbs past 3,200 m. The low ground is short: the lowest lift bases of Le Praz, La Tania and Saint-Martin sit between about 1,250 and 1,400 m.",
        "The weather model behind the snowfall figures covers the centre of the area with one grid cell, so it cannot tell Courchevel from Les Menuires, but it shows plainly what height does. In a typical season between 1991 and 2020, about 279 cm of snow fell at 1,600 m, 401 cm at 2,100 m and 420 cm at 2,600 m.",
        "The lower slopes have lost the most. At 1,600 m the typical season fell from 325 cm in 1961 to 1990 to 279 cm in 1991 to 2020, and four of the last five seasons sat in the lowest third of the 76 year record. At 2,600 m the fall was smaller, from 454 cm to 420 cm, and only two of the last five seasons were that poor.",
        "On this evidence the top half of the area is the safest bet in a thin winter, and Val Thorens and Orelle open first and close last: from 21 November to 2 May this season, against 5 December to 18 April for the linked area. The model gives snowfall rather than depth on the ground, and measured depths from weather stations are still being collected.",
    ],
    "heightsTitle": "Lift heights by sector",
    "heightsCaption": "Lowest lift base to highest lift top in each sector. From OpenStreetMap lift positions and the Copernicus 90 m elevation model, which reads a little low on the highest summits.",
    "chartTitle": "Seasonal snowfall at three heights, 1950 to 2026",
    "chartCaption": "Modelled snowfall from November to April, from the ERA5 reanalysis via the Open-Meteo historical weather API, for the grid cell at 45.25 N, 6.5 E adjusted to each height. Dots are single seasons; lines are 11 season running means. These are model values, not measurements on a piste.",
    "chartDesc": "Modelled snowfall from November to April. Dots are single seasons; lines are 11 season running means. Median 1991 to 2020: 279 cm at 1,600 m, 401 cm at 2,100 m, 420 cm at 2,600 m.",
    "conditions": {
        "status": "<b>No conditions are reported here yet.</b> Val Thorens and Orelle are due to open on 21 November 2026 and the linked area on 5 December. Until live data arrives, the official sources below give open lifts, pistes and forecasts.",
        "items": [
            {"dt": "Lifts and pistes open", "dd": A(U["live"], "Les 3 Vallées live status")},
            {"dt": "Mountain forecast", "dd": A(U["mf"], "Météo-France mountain weather")},
            {"dt": "Avalanche danger", "dd": A(U["mf"], "Météo-France bulletins") + " for the Vanoise massif, published daily in winter"},
        ],
        "safety": "Terrain beyond the marked pistes is not controlled. The avalanche bulletin and local advice take precedence over anything on this page.",
    },
    "ev": ["L001", "L050", "L051", "L052", "L043"],
}
d["pass"] = {
    "h2": "Does the full pass pay?",
    "paras": [
        "A six day adult pass for the whole area costs €421 in high season. The valley passes undercut it by between €53.50 and €71: €356 for the Méribel valley, €350 for Les Menuires and Saint-Martin, and €367.50 for Val Thorens and Orelle. The gap is less than a single day on the full pass at €84.20.",
        "That arithmetic favours the full pass for almost any week with a day's travel in it. The case for the valley pass is strongest in Val Thorens, where every lift starts above 2,000 m and the local season runs a fortnight longer at each end.",
    ],
    "table": {
        "caption": "Valley pass against full pass, adult, 2026/27",
        "rows": [
            ["Méribel valley, six days", "€356", "€421", "€65"],
            ["Les Menuires and Saint-Martin, six days", "€350", "€421", "€71"],
            ["Val Thorens and Orelle, six days", "€367.50", "€421", "€53.50"],
            ["Les Menuires and Saint-Martin, one day", "€70", "€84.20", "€14.20"],
        ],
        "note": "Sources: " + A(U["skipass"], "Les 3 Vallées") + ", " + A(U["menu"], "Les Menuires") + ", " + A(U["meri"], "Guide Ski") + " for Méribel and " + A(U["alti"], "Alti-Mag") + " for Val Thorens and Orelle. Courchevel's own valley price is still being checked.",
    },
    "coverageTitle": "What the pass covers",
    "coverage": [
        {"label": "Linked both ways by lift and piste", "kind": "yes", "items": ["Courchevel", "La Tania", "Méribel", "Saint-Martin-de-Belleville", "Les Menuires", "Val Thorens"]},
        {"label": "Linked by gondola, no piste home", "kind": "oneway", "items": ["Brides-les-Bains, by the Olympe gondola", "Orelle village, by the Orelle gondola"]},
    ],
    "scenariosTitle": "Which pass for which trip",
    "scenarios": [
        {"who": "A week in Méribel", "what": "The full pass costs €65 more, and from Méribel every other valley is one to three lift rides away."},
        {"who": "A week in Les Menuires or Saint-Martin", "what": "The full pass costs €71 more; Val Thorens is on both passes, Méribel and Courchevel only on the full one."},
        {"who": "A week in Val Thorens", "what": "The local pass covers Orelle and the highest lifts in the area for €53.50 less."},
        {"who": "Families", "what": "The Family Flex pass charges every member the child price, €345 each for six days, for one or two adults with one to six children. Children under five ski free."},
        {"who": "Early and late season", "what": "From 5 to 18 December 2026 and 10 to 18 April 2027 the six day full pass falls to €378.50, and the Les Menuires and Saint-Martin pass to €315."},
        {"who": "Saturdays", "what": "A full pass day costs €67.30 when bought online by midnight on the Friday."},
    ],
    "after": "Adults are 18 to 74, children 5 to 17 and veterans 75 and over, who pay €105 for six days at the ticket office only. High season runs from 19 December to 9 April.",
    "ev": ["L040", "L041", "L042", "L043", "L044", "L045"],
}
d["access"] = {
    "h2": "Getting there and choosing a base",
    "paras": [
        "Geneva airport is about 130 to 160 km from the main resorts by road, Lyon 170 to 200 km and Chambéry 90 to 120 km. The roads converge at the end, on the A43 to Albertville and the RN90 dual carriageway to Moûtiers, where the three valleys fork. The operator reckons on about two hours from Geneva or Lyon.",
        "Moûtiers is also the railway station, around four and a half hours from Paris by TGV, and the Eurostar ski train from London stops there on winter Saturdays. From the bus station, coaches run up to Courchevel, Méribel, Brides-les-Bains, Les Menuires, Saint-Martin and Val Thorens for about €12 an adult, with 10% off when booked more than two days ahead, and the operator puts every resort within an hour.",
        "Orelle is the exception. It lies on the far side of the ridge in the Maurienne valley, 186 km from Geneva by the fastest road, and its gondola climbs straight into the Val Thorens ski area, a back door for anyone driving in from that side.",
    ],
    "accessNote": "Road distances are the fastest route by the OSRM router on OpenStreetMap data, without traffic or snow. Train and bus details as published by " + A(U["access"], "Les 3 Vallées") + " and its " + A(U["bus"], "Moûtiers bus page") + "; the Eurostar ski train as reported by " + A(U["seat61"], "Seat 61") + ". 2026/27 timetables have not yet been checked.",
    "basesH3": "How far each base reaches",
    "basesParas": [
        "Where a skier sleeps changes the holiday more than which pass they buy. Méribel and Mottaret sit in the middle, with Courchevel and Val Thorens two or three lift rides away. Les Menuires and Val Thorens are close to each other but far from Courchevel, four rides from the village lifts.",
        "The corners pay for their charm or their price in lifts. Moriond, Brides-les-Bains and Orelle are each six lift rides from one end of the area, and a lunch on the far side can mean a long afternoon getting home.",
    ],
    "basesCaption": "Lift rides from each base",
    "baseCols": ["To Courchevel 1850", "To Méribel", "To Val Thorens", "To a lift top above 2,800 m"],
    "bases": [
        {"base": "Méribel-Mottaret", "v": [2, 0, 2, 2]}, {"base": "Méribel", "v": [2, 0, 3, 3]}, {"base": "Courchevel 1850", "v": [0, 2, 4, 4]},
        {"base": "Les Menuires", "v": [4, 2, 2, 2]}, {"base": "Val Thorens", "v": [4, 2, 0, 1]}, {"base": "Courchevel 1550", "v": [1, 3, 5, 5]},
        {"base": "La Tania", "v": [2, 2, 5, 5]}, {"base": "Le Praz", "v": [2, 2, 5, 5]}, {"base": "Saint-Martin", "v": [4, 2, 4, 4]},
        {"base": "Moriond", "v": [2, 4, 6, 6]}, {"base": "Brides-les-Bains", "v": [5, 2, 6, 6]}, {"base": "Orelle", "v": [6, 4, 2, 2]},
    ],
    "basesNote": "Fewest lift rides from the village lifts before reaching the first lift of each area, on the OpenStreetMap model, allowing a gondola ride down where no piste returns and the walk from the Olympe gondola to the Chaudanne lifts in Méribel. Times are not included.",
    "ev": ["L060", "L061", "L062", "L063", "L022"],
}
d["chapters"] = [
    {"id": "snowboard", "kicker": "Snowboarders", "h2": "Riding the three valleys on a board", "photo": "powder",
     "paras": [
         "The operator counts four snowparks and 35 fun zones across the area. Méribel-Mottaret's Open Park is the one for intermediate and expert riders, and this winter the Châtelet chair returns to join the lower and upper parts of the park. Courchevel's Family Park starts beginners on small features, Méribel's Bump'N'Jump runs from beginner to expert, Les Menuires has the Pixel Area for intermediates, and Val Thorens has the JF Chapuis skicross course.",
         "Drag lifts are the nuisance they always are, and they are not spread evenly. In the map data 35 of the 132 main lifts are drags, and they are thickest in Courchevel, where they make up about two in five of the lifts. In Les Menuires and Val Thorens fewer than one lift in six is a drag, which makes the Belleville valley the easier base on a board.",
         "Away from the parks, skiresort.com lists 50 km of ski routes, marked but not groomed, and ranks the area among its best for freeriders and snowparks. Terrain beyond the markers is not controlled, so the avalanche bulletin and a local guide come first.",
     ],
     "listTitle": "Parks and places to ride",
     "items": [
         {"name": "Open Park", "where": "Méribel-Mottaret", "text": "Intermediate to expert; the Châtelet chair links its two parts from this winter."},
         {"name": "Family Park", "where": "Courchevel", "text": "Beginners to intermediates."},
         {"name": "Bump'N'Jump", "where": "Méribel", "text": "Beginners to experts."},
         {"name": "Pixel Area", "where": "Les Menuires", "text": "A fun zone for intermediates."},
         {"name": "JF Chapuis SkiCross", "where": "Val Thorens", "text": "A skicross course for intermediates and experts."},
         {"name": "Ski routes", "where": "Across the area", "text": "50 km marked but not groomed."},
     ],
     "note": "Parks: " + A(U["parks"], "Les 3 Vallées") + "; Châtelet chair: " + A(U["new"], "Skiworld") + " and " + A(U["meri"], "Guide Ski") + ". Ski routes and ratings: " + A(U["sr"], "skiresort.com") + " and its " + A(U["srtest"], "test report") + " (January 2025). Drag lift shares from OpenStreetMap. Park layouts change every season."},
    {"id": "families", "kicker": "Families", "h2": "Holidays with children", "photo": "family",
     "paras": [
         "Four of the resorts, Courchevel, Méribel, Les Menuires and Val Thorens, carry the Famille Plus label for family resorts, and skiresort.com counts families and beginners among the area's strengths. The pass helps too: the Family Flex rate charges everyone the child price, and children under five ski free.",
         "Courchevel does most for the very young. Its Village des Enfants at 1850 has its own lifts and conveyor belts, under threes can join BB Ski sessions, and the Aquamotion pool takes babies from six months and runs the Ludiboo Club for children of three to six.",
         "Méribel has the Piste des Inuits, a run of games and slides for learners, the Yeti Park for younger children and a reindeer farm, the Ranch Nordique. Les Menuires adds an indoor Fun Park with zones for under threes, three to sixes and six to twelves, and the Boukty Snow Camp for igloos and snowball fights. Val Thorens has the Cosmojet, a sledging run of 6 km.",
         "For a base, Les Menuires has the highest share of green and blue runs of the big resorts in the map data and sits two lift rides from Val Thorens; Méribel and Mottaret put the most of the area within easy reach for parents who want a day further afield.",
     ],
     "listTitle": "Where children are looked after",
     "items": [
         {"name": "Village des Enfants", "where": "Courchevel 1850", "text": "Ski school area with its own lifts and conveyor belts."},
         {"name": "Aquamotion", "where": "Courchevel", "text": "Pools, slides and the Ludiboo Club for ages 3 to 6."},
         {"name": "Piste des Inuits", "where": "Méribel", "text": "A fun zone of games and slides for learners."},
         {"name": "Yeti Park", "where": "Méribel", "text": "Play areas and snow tunnels for younger children."},
         {"name": "Fun Park", "where": "Les Menuires", "text": "Indoor trampolines and rope bridges, zoned by age."},
         {"name": "Cosmojet", "where": "Val Thorens", "text": "A 6 km sledging run open to all."},
     ],
     "note": "Sources: " + A(U["fam"], "Les 3 Vallées family activities") + ", " + A(U["kids"], "Les 3 Vallées children's activities") + ", " + A(U["fplus"], "France.fr on Famille Plus") + " (updated October 2023), " + A(U["cour"], "Courchevel lift passes") + " for the Family Flex rate. Ages and opening times are best checked when booking."},
    {"id": "food", "kicker": "Food", "h2": "Eating on the mountain", "photo": "village",
     "paras": [
         "On the operator's count the area holds 15 Michelin stars across 10 restaurants. Courchevel has most of them, led by Le 1947 at the Cheval Blanc, where Yannick Alléno holds three stars, with two each at Beaumanière 1850 and Les Grandes Alpes. In Saint-Martin-de-Belleville, René and Maxime Meilleur keep two stars at La Bouitte, and the village also has the Bib Gourmand Simple et Meilleur.",
         "Lunch on the slopes is easier to find than to choose, with 66 mountain restaurants among the 355 in the area. Le Cap Horn beside the Courchevel altiport has been open since 1954. La 1928 sits on the Col de la Loze with a heated terrace and a view all round, and Le Bel Air at the top of the Ariondaz gondola has a south facing terrace above Moriond.",
         "The Belleville valley keeps more of the old farm food. Le Corbeleys at the top of the Saint-Martin gondola has been run by one family for over a century; Chez Pépé Nicolas, on the Chasse blue between Les Menuires and Val Thorens, makes its own cheese in summer; and Le Chalet de la Marine, off the Dalles blue above Val Thorens, is a fixture of the resort.",
     ],
     "listTitle": "Tables worth the detour",
     "items": [
         {"name": "Le 1947", "where": "Courchevel 1850", "text": "Yannick Alléno's three star table at the Cheval Blanc."},
         {"name": "La Bouitte", "where": "Saint-Martin-de-Belleville", "text": "Two stars, René and Maxime Meilleur."},
         {"name": "Le Cap Horn", "where": "Courchevel altiport", "text": "Open since 1954, with a south facing terrace."},
         {"name": "La 1928", "where": "Col de la Loze", "text": "Simple local cooking and a heated terrace."},
         {"name": "Le Corbeleys", "where": "Above Saint-Martin", "text": "A family chalet at the top of the gondola."},
         {"name": "Chez Pépé Nicolas", "where": "Between Les Menuires and Val Thorens", "text": "Savoie produce, cheese made on site in summer."},
         {"name": "Le Chalet de la Marine", "where": "Val Thorens", "text": "Off the Dalles blue, a resort institution."},
     ],
     "note": "Stars and Bib Gourmand: " + A(U["stars"], "Savoie tourism, Michelin 2026") + ". Restaurant counts: " + A(U["l3v"], "Les 3 Vallées") + ". Mountain restaurants: " + A(U["terr"], "Les 3 Vallées terraces") + ", " + A(U["fest"], "Les 3 Vallées festive restaurants") + " and " + A(U["sng"], "Ski New Gen") + ". Restaurants change hands and menus each season."},
    {"id": "apres", "kicker": "Après", "h2": "Après and evenings", "photo": "night",
     "paras": [
         "The loudest afternoons happen on the mountain. La Folie Douce has two branches here: one at the middle station of the Saulire Express above Méribel, with cabaret during lunch and electro after it, and one at the top of the Plein Sud chair in Val Thorens. Méribel also has Le Rond Point, known as the Ronnie, a ski in terrace known for its après and live music.",
         "Val Thorens keeps the party going longest. Le 360 Bar on the Combe de Thorens green brings in well known artists and hosts Festival'Tho, and in the village The Frog is described as the highest pub in Europe, while the Malaysia club stays open until four or five in the morning. In Les Menuires, Roc Seven, reached by the Roc 1 gondola, has DJs every afternoon, and the Chalet du Sunny has live music from two until half past four and snowcat rides up for Sunny Nights.",
         "Courchevel's evenings move indoors. At 1850 Les Caves de Courchevel is the nightclub and La Mangeoire turns into a piano bar at night, and Moriond has the Fire & Ice bar at the Portetta, with fire pits and an ice bar.",
     ],
     "listTitle": "Where the evenings start",
     "items": [
         {"name": "La Folie Douce", "where": "Saulire Express, Méribel", "text": "Cabaret at lunch, electro after."},
         {"name": "Le Rond Point", "where": "Méribel", "text": "The Ronnie: a ski in terrace with live music."},
         {"name": "La Folie Douce", "where": "Plein Sud chair, Val Thorens", "text": "Afternoon dancing on a south facing terrace."},
         {"name": "Le 360 Bar", "where": "Val Thorens", "text": "Open air, on the Combe de Thorens green."},
         {"name": "Roc Seven", "where": "Les Menuires", "text": "DJ sets every afternoon, by the Roc 1 gondola."},
         {"name": "Chalet du Sunny", "where": "Les Menuires", "text": "Live music from 2 pm to 4.30 pm."},
         {"name": "Les Caves de Courchevel", "where": "Courchevel 1850", "text": "The resort's nightclub."},
     ],
     "note": "Sources: " + A(U["fest"], "Les 3 Vallées festive restaurants") + ", " + A(U["seem"], "See Méribel") + " (October 2026), " + A(U["iglu"], "Iglu Ski") + " (2023) and " + A(U["scott"], "Scott Dunn") + ". Bars open and close from season to season."},
]


def F(w, f, why, lim):
    return {"who": w, "fit": f, "why": why, "limit": lim}


d["fit"] = {
    "h2": "Who it suits",
    "intro": "How the area suits different kinds of trip, on the evidence gathered so far.",
    "rows": [
        F("Exploring a large network", "Good fit", "Six resorts share one network linked both ways by lift and piste, and from Méribel every valley is one to three lift rides away.", "From the village of Moriond, Orelle takes eight lift rides."),
        F("Intermediates who want variety", "Good fit", "No black run is needed between any two sectors, and green and blue reach them all in the map data.", "The easy way round often costs one to three extra lift rides."),
        F("Groups of mixed ability", "Good fit", "From Mottaret every sector except Orelle is within two lift rides, so a group can split and meet again for lunch.", "From Courchevel or Val Thorens the other end is a long day."),
        F("First timers", "Good fit", "Courchevel, Méribel, Les Menuires and Val Thorens hold the Famille Plus label, and skiresort.com rates the area highly for beginners.", "The full pass is wasted on a first week; the valley passes cost €53.50 to €71 less."),
        F("Families", "Good fit", "Children's villages, pools and fun zones in every big resort, Family Flex pricing and free skiing for under fives.", "Prices for lessons and childcare vary by resort and are best checked when booking."),
        F("Snowboarders", "Mixed", "Four snowparks and 35 fun zones, and few drag lifts in Les Menuires and Val Thorens.", "About two in five of Courchevel's lifts are drags."),
        F("Experts", "Good fit", "37 black runs, 50 km of ski routes and a top rating for experts and freeriders on skiresort.com.", "Off piste terrain is not controlled; the avalanche bulletin and a guide come first."),
        F("Putting snow first", "Good fit", "85% of the area is above 1,800 m, and Val Thorens and Orelle open first and close last.", "At 1,600 m modelled snowfall has fallen, and four of the last five seasons were poor there."),
        F("Travelling without a car", "Good fit", "The Eurostar ski train and the TGV reach Moûtiers, and buses run from there to the main resorts within about an hour.", "2026/27 timetables have not yet been checked."),
        F("Preferring a smaller area", "Mixed", "The valley passes cover Méribel, the Belleville valley or Val Thorens and Orelle on their own.", "Even the valley areas are large; a small area elsewhere may suit better."),
        F("Food lovers", "Good fit", "15 Michelin stars across 10 restaurants and 66 mountain restaurants.", "The best known tables are expensive and book up."),
        F("Looking for après", "Good fit", "Two Folie Douce branches, Le Rond Point, Le 360 Bar and late clubs in Val Thorens.", "Courchevel's evenings lean to hotel bars and nightclubs rather than parties on the slopes."),
        F("Non skiers", "Mixed", "Aquamotion, the thermal spa at Brides-les-Bains, sledging runs and a pedestrian pass.", "The pedestrian pass starts at €31.40, and each activity is paid for separately."),
    ],
    "catchesH3": "The catches",
    "catches": "The catches are about price and distance more than snow. The day ticket is the dearest of the four areas compared below, and the gap to the valley passes is small enough that most weeks end up on the full pass. The corners are a long way from each other: Moriond, Brides-les-Bains and Orelle are six lift rides from one end of the area, and Brides and Orelle depend on a single gondola each way. Lower down, the snow is thinner than it was, and four of the last five modelled seasons at 1,600 m were poor.",
}
d["compare"] = {
    "h2": "The other large areas of Savoie",
    "paras": [
        "Set against its neighbours, Les 3 Vallées is the biggest by a distance, with 600 km of piste against 425 km for Paradiski, the next largest, and about a quarter more lifts. It also has the dearest day ticket of the four, though its six day pass costs less than Tignes Val d'Isère's.",
        "Tignes Val d'Isère climbs highest, to 3,456 m, and has the most difficult skiing, a fifth of its piste. Paradiski is two big areas joined by the Vanoise Express cable car. Les Sybelles, in the Maurienne, is the cheapest by a wide margin, mostly red, and has the most modelled snowfall at 1,600 m, though it tops out at 2,620 m.",
    ],
    "caption": "Four linked areas of Savoie",
    "cols": [{"name": "Les 3 Vallées", "href": ""}, {"name": "Paradiski", "href": "/projectsnow/france/paradiski/"}, {"name": "Tignes Val d'Isère", "href": "/projectsnow/france/tignes-val-disere/"}, {"name": "Les Sybelles", "href": "/projectsnow/france/les-sybelles/"}],
    "rows": [
        {"label": "Piste", "v": ["600 km", "425 km", "300 km", "275 km"]},
        {"label": "Lifts", "v": ["159", "126", "80", "61"]},
        {"label": "Lift heights", "v": ["1,100 to 3,230 m", "1,200 to 3,226 m", "1,550 to 3,456 m", "1,100 to 2,620 m"]},
        {"label": "Easy, intermediate, difficult", "v": ["56, 34, 10%", "57, 30, 12%", "55, 25, 20%", "21, 71, 8%"]},
        {"label": "Day ticket, adult, high season", "v": ["€84.20", "€78", "€78", "€60.50"]},
        {"label": "Six days, adult, high season", "v": ["€421", "€412", "€468", "€307.20"]},
        {"label": "Snowfall at 1,600 m, typical season 1991 to 2020", "v": ["279 cm", "290 cm", "263 cm", "426 cm"]},
        {"label": "Road from Geneva airport", "v": ["130 to 160 km", "157 to 160 km", "181 to 183 km", "178 to 189 km"]},
        {"label": "How it links", "v": ["Three valleys joined by lift; Orelle and Brides by gondola", "Two areas joined by the Vanoise Express", "Two resorts sharing one area", "Six villages meeting at the Ouillon summit"]},
    ],
    "note": "Size, lifts, heights and grade split: skiresort.com listings for " + A(U["sr"], "Les 3 Vallées") + ", " + A("https://www.skiresort.com/en/ski-resort/la-plagne-paradiski/", "La Plagne") + " and " + A("https://www.skiresort.com/en/ski-resort/les-arcs-peisey-vallandry-paradiski/", "Les Arcs and Peisey-Vallandry") + " (added together for Paradiski), " + A("https://www.skiresort.com/en/ski-resort/tignes-val-disere/", "Tignes Val d'Isère") + " and " + A("https://www.skiresort.com/en/ski-resort/les-sybelles-le-corbier-la-toussuire-les-bottieres-st-sorlin-st-jean-darves/", "Les Sybelles") + ", retrieved 20 October 2026; Les Sybelles' operator counts 310 km. Prices: " + A(U["alti"], "Alti-Mag") + ", 2026/27 high season, indicative. Snowfall: ERA5 via the Open-Meteo historical weather API, one grid cell per area adjusted to 1,600 m; the cells are about 20 to 30 km across, so the figures describe regions, not single resorts. Road: fastest route from Geneva airport to the main villages by the OSRM router, leaving out Orelle at 186 km.",
    "ev": ["L010", "L070", "L071", "L072", "L044", "L073", "L074"],
}
d["explore"] = [
    {"h3": "Official information", "links": [{"t": "Interactive piste map", "u": U["map"]}, {"t": "Lift and piste status", "u": U["live"]}, {"t": "2026/27 lift passes", "u": U["skipass"]}, {"t": "The area in figures", "u": U["l3v"]}, {"t": "Getting there", "u": U["access"]}]},
    {"h3": "On Snow Catchers", "links": [{"t": "Skiing in France", "u": "/projectsnow/france/"}, {"t": "Paradiski", "u": "/projectsnow/france/paradiski/"}, {"t": "Tignes Val d'Isère", "u": "/projectsnow/france/tignes-val-disere/"}, {"t": "Les Sybelles", "u": "/projectsnow/france/les-sybelles/"}, {"t": "Portes du Soleil", "u": "/projectsnow/france/portes-du-soleil/"}]},
    {"h3": "Resorts and villages", "text": "Pages for each of the eight resorts and their villages come next, with the runs, ski schools, restaurants and places to stay that this page leaves out."},
]
d["method"] = {
    "items": [
        {"dt": "Which resorts count", "dd": "The eight places reached on the 2026/27 Les 3 Vallées pass, counting Orelle and Brides-les-Bains; the operator counts seven resorts. Sharing the pass is recorded separately from being linked by lift and piste."},
        {"dt": "How links were checked", "dd": "A sector counts as linked only when a route of lifts and pistes reaches it in the OpenStreetMap data. Drag lifts run one way, gondolas may be ridden down, and the walk from the Olympe gondola to the Chaudanne lifts in Méribel is added by hand. A link is critical when closing one lift on it cuts routes that no other lift replaces. The model has not yet been checked against the official 2026/27 piste map."},
        {"dt": "Piste totals", "dd": "Operator and measured figures are both shown and never averaged. Mapped piste from OpenStreetMap is used only to compare resorts and grades."},
        {"dt": "Comparisons", "dd": "The four areas compared use the same source for each row, so a figure can be set against its neighbour."},
    ],
    "fresh": [
        ["Lift pass prices", "2026/27 season", "Operator, Guide Ski, Alti-Mag", "20 Oct 2026"],
        ["Season dates", "2026/27 season", "Operator", "20 Oct 2026"],
        ["Run and lift counts, size, altitude", "Current listings", "Operator and skiresort.com", "20 Oct 2026"],
        ["Network, bases, routes, resort comparison", "Map snapshot", "Derived from OpenStreetMap", "20 Oct 2026"],
        ["Snowfall", "1950/51 to 2025/26", "Reanalysis model", "20 Oct 2026"],
        ["Bus and train services", "Undated pages; 2026/27 timetables not checked", "Operator and Seat 61", "20 Oct 2026"],
        ["Comparison with other areas", "Current listings", "skiresort.com, Alti-Mag, model, router", "20 Oct 2026"],
        ["Restaurants, bars, parks and family facilities", "Current guides; some from 2018 to 2023", "Operator, tourist offices, guides and press", "20 Oct 2026"],
        ["Michelin stars", "2026 guide", "Savoie tourism", "20 Oct 2026"],
        ["Visitor reviews", "Not yet analysed", "None", "Not started"],
        ["Current conditions", "Not shown on this page", "Linked to operator and forecasters", "Links checked 20 Oct 2026"],
    ],
    "conflictsH3": "Figures that do not agree",
    "conflicts": "The operator counts 169 lifts and skiresort.com 159. The operator gives a base height of 1,300 m and skiresort.com 1,100 m, with the Olympe gondola starting at 612 m in Brides-les-Bains. The operator counts seven resorts, while the pass reaches eight places including Orelle. The elevation model puts the highest lift top at 3,211 m against the operator's 3,230 m. skiresort.com gives the season as 21 November to 2 May, the dates for Val Thorens and Orelle; the linked area runs from 5 December to 18 April. This page names each source alongside its figure.",
    "sources": "Research of 20 October 2026. Size, runs, lifts, heights, restaurants and history: " + A(U["l3v"], "Les 3 Vallées in figures") + " and " + A(U["story"], "the area's history") + ". Measured size, grades, lifts and ratings: " + A(U["sr"], "skiresort.com") + ". Prices: " + A(U["skipass"], "Les 3 Vallées") + ", " + A(U["cour"], "Courchevel lift passes") + ", " + A(U["menu"], "Les Menuires") + ", " + A(U["meri"], "Guide Ski") + " and " + A(U["alti"], "Alti-Mag") + ". Season and new lifts: " + A(U["new"], "Skiworld") + ". Network, bases, routes and lift heights: a graph of 167 lifts and 1,126 piste sections from " + A(U["osm"], "OpenStreetMap") + " (© OpenStreetMap contributors, ODbL), with heights from the Copernicus 90 m elevation model via " + A(U["elev"], "Open-Meteo") + ". Snowfall: ERA5 reanalysis via the " + A(U["hist"], "Open-Meteo historical weather API") + " (CC BY 4.0). Road distances: " + A(U["osrm"], "OSRM") + ". Facts from operators, measurements, model results and estimates are kept apart in the research files, and conflicting figures are listed above rather than averaged.",
}
d["breaks"] = {"network": {"photo": "caron"}, "terrain": {"photo": "mottaret"}, "access": {"photo": "belleville"}}
d["photos"] = {
    "hero": ["View northeast from Mont Vallon, Méribel, 2022.jpg", "DimiTalen", "CC0", "Looking north east from Mont Vallon above Méribel"],
    "caron": ["Cime de Caron enneigée depuis Pointe de la Masse (janvier 2024).JPG", "Florian Pépellin", "CC BY-SA 4.0", "The Cime de Caron above Val Thorens, seen from the Pointe de la Masse"],
    "mottaret": ["Méribel-Mottaret seen from below Mont Vallon.jpg", "DimiTalen", "CC0", "Méribel-Mottaret seen from below Mont Vallon"],
    "belleville": ["Vallée des Belleville entre St-Martin et Menuires en hiver (décembre 2024).JPG", "Florian Pépellin", "CC BY-SA 4.0", "The Belleville valley between Saint-Martin and Les Menuires in winter"],
    "powder": ["Pistes de ski Versant nord de Mottaret (février 2023).JPG", "Florian Pépellin", "CC BY-SA 4.0", "Pistes on the north side of Mottaret"],
    "family": ["Terrasses au Front de neige des Menuires (janvier 2024).JPG", "Florian Pépellin", "CC BY-SA 4.0", "Terraces at the foot of the slopes in Les Menuires"],
    "village": ["Centre Village de Saint-Martin-de-Belleville en hiver (décembre 2024).JPG", "Florian Pépellin", "CC BY-SA 4.0", "The centre of Saint-Martin-de-Belleville in winter"],
    "night": ["Nuit à Méribel-Mottaret en hiver (décembre 2019).JPG", "Florian Pépellin", "CC BY-SA 4.0", "Méribel-Mottaret at night"],
}
json.dump(d, open(OUT, "w"), ensure_ascii=False, indent=2)
open(OUT, "a").write("\n")
print("written", OUT)
