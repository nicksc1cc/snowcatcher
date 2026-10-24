"""Build facts.csv and model/network.json for the Évasion Mont Blanc package.
Hand facts are listed with their evidence record; model facts come from the network run.
Usage: python3 scripts/make_data.py  (from research/evasion-mont-blanc)"""
import csv, json

RUN = json.load(open("model/run_2026-10-24.json", encoding="utf-8"))
NET_DS, SNOW_DS, ROAD_DS = "ds:emb-network-2026-10-24", "ds:emb-era5-snow-2026-10-24", "ds:emb-osrm-2026-10-24"
A = "area:evasion-mont-blanc"
CELL = "cell:era5.45.75.6.75"
IDS = ["rochebrune", "mont-d-arbois", "princesse", "saint-gervais", "saint-nicolas", "jaillet", "combloux", "la-giettaz"]
BASES = ["rochebrune", "mont-d-arbois", "princesse", "saint-gervais", "saint-nicolas"]
COLS = ["rochebrune", "saint-gervais", "saint-nicolas", "top2000"]
S = lambda s: "sector:evasion-mont-blanc." + s
L = lambda s: "lift:evasion-mont-blanc." + s
UNITS = {"piste_km": "km", "road_km": "km", "area_high_m": "m", "area_low_m": "m", "lift_top_max_m": "m", "lift_base_min_m": "m",
         "snowfall_median_cm": "cm", "pass_price_eur": "eur", "grade_share_pct": "pct", "drag_lift_share_pct": "pct",
         "event_year": "year", "opened_year": "year", "season_opens": "date", "season_closes": "date"}
rows = []


def f(name, place, prop, value, method, ref, scope="", q=None, season="", ds="", note=""):
    rows.append(dict(name=name, place_id=place, property=prop, value=str(value), unit=UNITS.get(prop, "count"), method=method, legacy_ref=ref,
                     scope=scope, qualifiers=json.dumps(q, ensure_ascii=False) if q else "", season=season, dataset=ds, note=note, source_id=""))


# operator figures, as published by Alti-Mag and the Saint-Gervais tourist office
f("op_km", A, "piste_km", 445, "operator", "M001", scope="total", note="Includes Les Contamines-Hauteluce, on the pass but not linked on skis")
f("runs_total", A, "runs_count", 133, "operator", "M001", q={"grade": "total"})
for g, v in (("green", 28), ("blue", 35), ("red", 52), ("black", 18)):
    f("runs_" + g, A, "runs_count", v, "operator", "M001", q={"grade": g})
f("op_lifts114", A, "lifts_count", 114, "operator", "M001", scope="all_lifts", note="Alti-Mag")
f("op_lifts110", A, "lifts_count", 110, "operator", "M003", scope="all_lifts", note="Saint-Gervais tourist office")
f("op_low", A, "area_low_m", 800, "operator", "M001", scope="lowest_skiing", note="Alti-Mag")
f("op_high", A, "area_high_m", 2370, "operator", "M001", scope="highest_skiing", note="Alti-Mag")
f("ot_high", A, "area_high_m", 2353, "operator", "M003", scope="highest_skiing", note="Saint-Gervais tourist office")
f("open_first", A, "season_opens", "2026-12-12", "operator", "M002", scope="earliest_sector", note="Progressive opening; a partial pre-opening on 5 and 6 December")
f("open_all", A, "season_opens", "2026-12-19", "operator", "M002", scope="linked")
f("close_all", A, "season_closes", "2027-04-04", "operator", "M002", scope="linked")
f("pdmb_close", "pass:les-portes-du-mont-blanc", "season_closes", "2027-03-21", "operator", "M004", note="Alti-Mag domain page")
f("giettaz_close", "resort:la-giettaz", "season_closes", "2027-04-04", "operator", "M006", note="Alti-Mag La Giettaz page")
# history
f("rothschild", "resort:megeve", "event_year", 1921, "editorial", "M018", q={"event": "domaine_du_mont_d_arbois_opened"})
f("folie_opened", "poi:la-folie-douce-saint-gervais", "opened_year", 2014, "editorial", "M018", note="Opened for the 2014/15 season")
# measured listings: skiresort.com Megève/Saint-Gervais (185 km) and Les Portes du Mont-Blanc (89 km), added together
f("sr_km", A, "piste_km", 274, "measured", "M008", scope="total", note="skiresort.com Megève/Saint-Gervais 185 km plus Les Portes du Mont-Blanc 89 km (M009); without Les Contamines")
f("sr_lifts", A, "lifts_count", 80, "measured", "M008", scope="all_lifts", note="60 plus 20 (M009)")
f("sr_low", A, "area_low_m", 850, "measured", "M008", scope="lowest_skiing")
f("sr_high", A, "area_high_m", 2353, "measured", "M008", scope="highest_skiing")
for g, v in (("easy", 41), ("intermediate", 46), ("difficult", 13)):
    f("sr_" + g, A, "grade_share_pct", v, "measured", "M008", scope="listing_length", q={"grade": g},
      note="From the two listings added together: easy 112, intermediate 126, difficult 36 of 274 km")
f("ct_km", "resort:les-contamines", "piste_km", 120, "measured", "M010", scope="total")
# comparison areas
for key, place, km, lifts, lo, hi, e, i, d, ref in (("pds", "area:portes-du-soleil", 580, 163, 985, 2254, 54, 36, 10, "M011"),
                                                    ("gm", "area:grand-massif", 265, 63, 697, 2480, 51, 36, 13, "M012")):
    f(key + "_km", place, "piste_km", km, "measured", ref, scope="total")
    f(key + "_lifts", place, "lifts_count", lifts, "measured", ref, scope="all_lifts")
    f(key + "_low", place, "area_low_m", lo, "measured", ref, scope="lowest_skiing")
    f(key + "_high", place, "area_high_m", hi, "measured", ref, scope="highest_skiing")
    for g, v in (("easy", e), ("intermediate", i), ("difficult", d)):
        f(f"{key}_{g}", place, "grade_share_pct", v, "measured", ref, scope="listing_length", q={"grade": g})
hi = lambda age, d: dict(age=age, days=d, period="high")
P, PM, MBU = "pass:evasion-mont-blanc", "pass:les-portes-du-mont-blanc", "pass:mont-blanc-unlimited"
f("pds_1d", "pass:portes-du-soleil", "pass_price_eur", 73, "operator", "M013", q=hi("adult", 1), season="2026/27")
f("pds_6d", "pass:portes-du-soleil", "pass_price_eur", 373, "operator", "M013", q=hi("adult", 6), season="2026/27")
f("gm_1d", "pass:grand-massif", "pass_price_eur", 63, "operator", "M013", q=hi("adult", 1), season="2026/27")
f("gm_6d", "pass:grand-massif", "pass_price_eur", 378, "operator", "M013", q=hi("adult", 6), season="2026/27")
# passes
f("em_1d", P, "pass_price_eur", 65, "operator", "M002", q=hi("adult", 1), season="2026/27")
f("em_6d", P, "pass_price_eur", 324.5, "operator", "M002", q=hi("adult", 6), season="2026/27")
f("em_6d_online", P, "pass_price_eur", 289.5, "operator", "M002", q={"age": "adult", "days": 6, "period": "high", "channel": "online"}, season="2026/27",
  note="Bought online at least ten days ahead")
f("em_child_1d", P, "pass_price_eur", 55.5, "operator", "M002", q=hi("child", 1), season="2026/27", note="Child 5 to 14")
f("em_child_6d", P, "pass_price_eur", 276, "operator", "M002", q=hi("child", 6), season="2026/27", note="Child 5 to 14")
f("em_4h", P, "pass_price_eur", 58.5, "operator", "M002", q={"age": "adult", "product": "four_hours"}, season="2026/27")
f("em_week", P, "pass_price_eur", 369, "operator", "M003", q={"age": "adult", "product": "week"}, season="2026/27", note="Listed as a week pass by the Saint-Gervais tourist office")
f("em_season", P, "pass_price_eur", 1189, "operator", "M014", q={"age": "adult", "product": "season"}, season="2026/27")
f("em_season_pre", P, "pass_price_eur", 890, "operator", "M014", q={"age": "adult", "product": "season", "channel": "presale"}, season="2026/27",
  note="Until 30 November 2026")
f("beginner_1d", P, "pass_price_eur", 29, "operator", "M002", q={"age": "adult", "days": 1, "product": "rochebrune_mont_d_arbois_beginner"}, season="2026/27")
f("pdmb_1d", PM, "pass_price_eur", 52.5, "operator", "M004", q=hi("adult", 1), season="2026/27")
f("pdmb_6d", PM, "pass_price_eur", 262.5, "operator", "M004", q=hi("adult", 6), season="2026/27")
f("mbu_1d", MBU, "pass_price_eur", 104, "operator", "M015", q=hi("adult", 1), season="2026/27")
f("mbu_6d", MBU, "pass_price_eur", 499, "operator", "M015", q=hi("adult", 6), season="2026/27")
# Michelin 2026
f("stars_megeve", "resort:megeve", "michelin_stars_count", 5, "editorial", "M019",
  note="Michelin 2026: Flocons de Sel three, La Table de l'Alpaga one, Vous one")
f("stars_saint_gervais", "resort:saint-gervais", "michelin_stars_count", 1, "editorial", "M019",
  note="Michelin 2026: La Table d'Armante at Saint-Nicolas-de-Véroce, new in 2026")
# network model
t = RUN["totals"]
f("m_lifts", A, "lifts_count", t["lifts"], "modelled", "M030", scope="all_mapped", ds=NET_DS)
f("m_main", A, "lifts_count", t["main"], "modelled", "M030", scope="main_lifts_mapped", ds=NET_DS)
f("m_drags", A, "drag_lifts_count", t["drags"], "modelled", "M030", ds=NET_DS)
f("m_sections", A, "piste_sections_count", t["pisteWays"], "modelled", "M030", ds=NET_DS)
f("m_km", A, "piste_km", t["pisteKm"], "modelled", "M030", scope="mapped_length", ds=NET_DS)
for sid in IDS:
    s = RUN["sectors"][sid]
    f("lo." + sid, S(sid), "lift_base_min_m", s["lo"], "modelled", "M030", ds=NET_DS)
    f("hi." + sid, S(sid), "lift_top_max_m", s["hi"], "modelled", "M030", ds=NET_DS)
    f("easy." + sid, S(sid), "grade_share_pct", round(100 * s["easyKm"] / s["km"]), "modelled", "M030", scope="mapped_length", q={"grade": "easy"}, ds=NET_DS)
    f("black." + sid, S(sid), "grade_share_pct", round(100 * s["blackKm"] / s["km"]), "modelled", "M030", scope="mapped_length", q={"grade": "difficult"}, ds=NET_DS)
    f("drag." + sid, S(sid), "drag_lift_share_pct", round(100 * s["drags"] / s["main"]), "modelled", "M030", ds=NET_DS, note="Share of main lifts")
for sid in BASES:
    for col in COLS:
        f(f"b.{sid}.{col}", S(sid), "lift_rides_from_village", RUN["base"][sid][col], "modelled", "M030",
          q={"to": "lift_top_above_2000" if col == "top2000" else S(col)}, ds=NET_DS)
crit = {}
for c in RUN["critical"]:
    crit.setdefault(c[0], c)
for key, name in (("rocharbois", "Rocharbois"), ("princesse", "Princesse"), ("mont-d-arbois", "Mont d'Arbois"), ("mont-joux", "Mont Joux"),
                  ("christomet", "TSD6 du Christomet"), ("bonjournal", "TKE1 du Bonjournal"), ("pres", "TSF4 des Prés")):
    f("cut." + key, L(key), "sector_pairs_cut_count", crit[name][2], "modelled", "M030", ds=NET_DS)
# snowfall
for h, new, old in ((1600, 362, 426), (2100, 470, 581), (2600, 488, 600.5)):
    f(f"s{h}", CELL, "snowfall_median_cm", new, "reanalysis", "M031", q={"period": "1991-2020", "elevation_m": h}, ds=SNOW_DS)
    f(f"s{h}_old", CELL, "snowfall_median_cm", old, "reanalysis", "M031", q={"period": "1961-1990", "elevation_m": h}, ds=SNOW_DS)
f("pds_snow", "cell:era5.46.25.6.75", "snowfall_median_cm", 285, "reanalysis", "M032", q={"period": "1991-2020", "elevation_m": 1600}, ds="ds:geneva-era5-compare-2026-10-20")
f("gm_snow", "cell:era5.46.0.6.75", "snowfall_median_cm", 391, "reanalysis", "M032", q={"period": "1991-2020", "elevation_m": 1600}, ds="ds:geneva-era5-compare-2026-10-20")
# roads
for src, lo, hi_ in (("gva", 71, 85), ("lys", 169, 187), ("cmf", 91, 109)):
    f(f"{src}_min", A, "road_km", lo, "modelled", "M040", q={"from": "poi:" + src, "bound": "min"}, ds=ROAD_DS)
    f(f"{src}_max", A, "road_km", hi_, "modelled", "M040", q={"from": "poi:" + src, "bound": "max"}, ds=ROAD_DS)
for key, poi, lo, hi_ in (("sal", "poi:sallanches-station", 8, 31), ("fay", "poi:le-fayet-station", 5, 32)):
    f(f"{key}_min", A, "road_km", lo, "modelled", "M040", q={"from": poi, "bound": "min"}, ds=ROAD_DS)
    f(f"{key}_max", A, "road_km", hi_, "modelled", "M040", q={"from": poi, "bound": "max"}, ds=ROAD_DS)
for key, place, lo, hi_ in (("pds", "area:portes-du-soleil", 69, 129), ("gm", "area:grand-massif", 65, 80)):
    f(f"{key}_gva_min", place, "road_km", lo, "modelled", "M041", q={"from": "poi:gva", "bound": "min"}, ds="ds:geneva-osrm-compare-2026-10-20")
    f(f"{key}_gva_max", place, "road_km", hi_, "modelled", "M041", q={"from": "poi:gva", "bound": "max"}, ds="ds:geneva-osrm-compare-2026-10-20")

cols = ["name", "place_id", "property", "value", "unit", "method", "legacy_ref", "scope", "qualifiers", "season", "dataset", "note", "source_id"]
with open("data/facts.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, cols)
    w.writeheader()
    w.writerows(rows)

# network file in the site format
easy = {a: dict(RUN["all"][a]) for a in IDS}
for a, row in RUN["easy_differs_from_all"].items():
    easy[a].update(row)
red = {a: dict(RUN["all"][a]) for a in IDS}
for a, row in RUN["red_differs_from_all"].items():
    red[a].update(row)
allm = {a: RUN["all"][a] for a in IDS}
net = {"source": "snowcatcher research/evasion-mont-blanc model/run_2026-10-24.json, OpenStreetMap snapshot " + RUN["snapshot"] + "; from the first lift base in each area",
       "ids": IDS, "all": allm, "ability": {"ids": IDS, "easy": easy, "red": red}}
json.dump(net, open("model/network.json", "w", encoding="utf-8"), ensure_ascii=False)
print(len(rows), "facts")
