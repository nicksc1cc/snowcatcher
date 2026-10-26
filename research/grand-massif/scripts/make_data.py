"""Build facts.csv and model/network.json for the Grand Massif package.
Hand facts are listed with their evidence record; model facts come from the network run and the snow series.
Usage: python3 scripts/make_data.py  (from research/grand-massif)"""
import csv, json, statistics

RUN = json.load(open("model/run_2026-10-26.json", encoding="utf-8"))
NET_DS, SNOW_DS, CL_DS = "ds:gm-network-2026-10-26", "ds:gm-era5-snow-2026-10-26", "ds:clusaz-era5-snow-2026-10-26"
A = "area:grand-massif"
CELL, CL_CELL = "cell:era5.46.0.6.75", "cell:era5.46.0.6.5"
IDS = ["flaine", "carroz", "morillon", "samoens", "sixt"]
S = lambda s: "sector:grand-massif." + s
L = lambda s: "lift:grand-massif." + s
UNITS = {"piste_km": "km", "road_km": "km", "area_high_m": "m", "area_low_m": "m", "lift_top_max_m": "m", "lift_base_min_m": "m",
         "snowfall_median_cm": "cm", "pass_price_eur": "eur", "grade_share_pct": "pct", "drag_lift_share_pct": "pct",
         "event_year": "year", "opened_year": "year", "season_opens": "date", "season_closes": "date", "run_length_km": "km",
         "run_drop_m": "m", "vertical_drop_m": "m", "free_pass_under_age_years": "year", "kids_club_min_age_years": "year",
         "trail_km": "km", "ride_minutes": "count"}
rows = []


def f(name, place, prop, value, method, ref, scope="", q=None, season="", ds="", note=""):
    rows.append(dict(name=name, place_id=place, property=prop, value=str(value), unit=UNITS.get(prop, "count"), method=method, legacy_ref=ref,
                     scope=scope, qualifiers=json.dumps(q, ensure_ascii=False) if q else "", season=season, dataset=ds, note=note, source_id=""))


# size, runs and lifts as published (Alti-Mag reproduces the operator's figures)
f("op_km", A, "piste_km", 265, "operator", "G002", scope="total")
f("runs_total", A, "runs_count", 152, "operator", "G002", q={"grade": "total"}, note="Alti-Mag")
for g, v in (("green", 25), ("blue", 67), ("red", 48), ("black", 12)):
    f("runs_" + g, A, "runs_count", v, "operator", "G002", q={"grade": g}, note="Alti-Mag")
f("ot_runs", A, "runs_count", 139, "operator", "G012", q={"grade": "total"}, note="Samoëns tourist office; Guide Ski gives the same")
f("op_lifts74", A, "lifts_count", 74, "operator", "G002", scope="all_lifts", note="Alti-Mag")
f("ot_lifts62", A, "lifts_count", 62, "operator", "G012", scope="all_lifts", note="Samoëns tourist office; Guide Ski gives the same")
f("wiki_lifts71", A, "lifts_count", 71, "editorial", "G015", scope="all_lifts", note="Wikipedia")
f("op_low", A, "area_low_m", 680, "operator", "G002", scope="lowest_skiing", note="Alti-Mag")
f("op_high", A, "area_high_m", 2480, "operator", "G002", scope="highest_skiing", note="Alti-Mag")
f("vil_km", "pass:villages-grand-massif", "piste_km", 145, "operator", "G003", scope="total", note="Alti-Mag, the four villages without Flaine")
# season
f("open_flaine", "resort:flaine", "season_opens", "2026-12-05", "operator", "G001", note="Subject to snow until 18 December")
f("close_flaine", "resort:flaine", "season_closes", "2027-04-18", "operator", "G001")
f("open_all", A, "season_opens", "2026-12-19", "operator", "G001", scope="")
f("close_all", A, "season_closes", "2027-04-11", "operator", "G001")
f("gs_open", A, "season_opens", "2026-12-12", "editorial", "G010", note="Guide Ski, subject to snow until 19 December")
f("close_villages", "pass:villages-grand-massif", "season_closes", "2027-04-04", "operator", "G003", note="Alti-Mag")
f("close_sixt", "resort:sixt", "season_closes", "2027-03-07", "operator", "G011", note="Guide Ski; Skiinfo gives the same")
f("open_sixt", "resort:sixt", "season_opens", "2026-12-19", "operator", "G011")
# history
f("y_carroz_lift", "resort:les-carroz", "event_year", 1939, "editorial", "G015", q={"event": "first_lift"})
f("y_samoens_lift", "resort:samoens", "event_year", 1945, "editorial", "G015", q={"event": "first_lift"})
f("y_site", "resort:flaine", "event_year", 1959, "editorial", "G014", q={"event": "site_found"})
f("y_flaine", "resort:flaine", "event_year", 1969, "editorial", "G014", q={"event": "resort_opened"}, note="Opened 17 January 1969")
f("y_link", A, "event_year", 1975, "editorial", "G015", q={"event": "flaine_samoens_link"})
f("y_formed", A, "event_year", 1980, "editorial", "G015", q={"event": "grand_massif_formed"})
f("y_gme", L("grand-massif-express"), "opened_year", 2003, "editorial", "G017")
f("y_coulouvrier", L("coulouvrier"), "opened_year", 2018, "editorial", "G015", note="Ready for the 2018/19 season")
f("y_vercland", L("vercland"), "opened_year", 2021, "editorial", "G015", note="Ready for the 2021/22 season")
f("y_masons", "resort:samoens", "event_year", 1659, "editorial", "G026", q={"event": "masons_recorded"})
f("y_jaysinia", "poi:jaysinia", "opened_year", 1906, "editorial", "G027")
f("y_jeff", "poi:chez-jeff", "opened_year", 2001, "editorial", "G025")
f("y_fplus_carroz", "resort:les-carroz", "event_year", 2006, "editorial", "G020", q={"event": "famille_plus_label"})
# runs and lifts
f("casc_km", "poi:piste-des-cascades", "run_length_km", 14, "operator", "G012")
f("dmc_min", L("grandes-platieres"), "ride_minutes", 12, "editorial", "G010", note="Guide Ski, about")
f("gme_park", "resort:samoens", "facility_count", 800, "operator", "G012", q={"kind": "parking_spaces_grand_massif_express"}, note="Paid in winter")
f("ver_park", "resort:samoens", "facility_count", 520, "operator", "G012", q={"kind": "parking_spaces_vercland"}, note="Free")
f("carroz_park", "resort:les-carroz", "facility_count", 1250, "editorial", "G020", q={"kind": "parking_spaces"}, note="Free, at the foot of the slopes, about")
f("s1600_lifts", "resort:samoens", "facility_count", 7, "operator", "G012", q={"kind": "beginner_lifts_samoens_1600"})
f("salv_runs", "resort:sixt", "runs_count", 6, "operator", "G011", q={"grade": "total"}, note="Salvagny local area")
f("salv_lifts", "resort:sixt", "lifts_count", 4, "operator", "G011", scope="all_lifts", note="Salvagny local area")
f("nordic_sixt", "resort:sixt", "trail_km", 16, "operator", "G011", q={"kind": "nordic"}, note="Fer-à-Cheval, about")
f("nordic_giffre", A, "trail_km", 26, "operator", "G011", q={"kind": "nordic"}, note="Along the Giffre between Morillon, Samoëns and Sixt, about")
f("free_under", "pass:grand-massif", "free_pass_under_age_years", 8, "operator", "G001", note="Day passes at the cash desk with proof of age; 75 and over also free")
f("club_age", "resort:morillon", "kids_club_min_age_years", 3, "operator", "G019")
# passes 2026/27, adult high season unless stated
hi = lambda age, d: dict(age=age, days=d, period="high")
P, V, FL = "pass:grand-massif", "pass:villages-grand-massif", "pass:flaine"
f("gm_1d", P, "pass_price_eur", 63, "operator", "G001", q=hi("adult", 1), season="2026/27")
f("gm_child_1d", P, "pass_price_eur", 50.4, "operator", "G001", q=hi("child", 1), season="2026/27", note="Reduced 8 to 14")
f("gm_4h", P, "pass_price_eur", 56.7, "operator", "G001", q={"age": "adult", "product": "four_hours"}, season="2026/27")
f("gm_mini", P, "pass_price_eur", 29, "operator", "G001", q={"age": "under_8_or_75_plus", "product": "two_to_seven_days"}, season="2026/27")
f("gm_season", P, "pass_price_eur", 1316, "operator", "G001", q={"age": "adult", "product": "season"}, season="2026/27")
f("gm_season_prems", P, "pass_price_eur", 658, "operator", "G001", q={"age": "adult", "product": "season", "channel": "presale"}, season="2026/27", note="Until 30 September 2026")
f("gm_season_promo", P, "pass_price_eur", 732, "operator", "G001", q={"age": "adult", "product": "season", "channel": "promo"}, season="2026/27", note="Until 15 November 2026")
f("gm_week_si", P, "pass_price_eur", 366, "operator", "G006", q={"age": "adult", "product": "week"}, season="2026/27", note="Skiinfo, weekday rate")
f("gm_1d_si", P, "pass_price_eur", 61, "operator", "G006", q={"age": "adult", "days": 1, "period": "weekday"}, season="2026/27", note="Skiinfo; skiresort.com also gives 61")
f("fl_1d", FL, "pass_price_eur", 60.7, "operator", "G001", q=hi("adult", 1), season="2026/27")
f("fl_4h", FL, "pass_price_eur", 54.6, "operator", "G001", q={"age": "adult", "product": "four_hours"}, season="2026/27")
f("beg_1d", FL, "pass_price_eur", 30.5, "operator", "G001", q={"age": "adult", "days": 1, "product": "flaine_beginner"}, season="2026/27")
f("ped", FL, "pass_price_eur", 23, "operator", "G001", q={"age": "adult", "product": "grandes_platieres_pedestrian_return"}, season="2026/27")
f("vil_1d", V, "pass_price_eur", 58.5, "operator", "G003", q=hi("adult", 1), season="2026/27", note="Alti-Mag; Guide Ski gives the same")
f("vil_6d", V, "pass_price_eur", 351, "operator", "G003", q=hi("adult", 6), season="2026/27", note="Alti-Mag")
f("vil_1d_si", V, "pass_price_eur", 57, "operator", "G007", q={"age": "adult", "days": 1, "period": "weekday"}, season="2026/27", note="Skiinfo")
f("vil_week_si", V, "pass_price_eur", 342, "operator", "G007", q={"age": "adult", "product": "week"}, season="2026/27", note="Skiinfo")
f("sixt_1d", "pass:sixt-beginner", "pass_price_eur", 16.1, "operator", "G011", q=hi("adult", 1), season="2026/27")
f("giffre_ped", V, "pass_price_eur", 11, "operator", "G011", q={"age": "adult", "product": "giffre_pedestrian_return"}, season="2026/27")
# La Clusaz Manigod for the comparison
C = "area:la-clusaz-manigod"
ROAD_DS = "ds:na-osrm-access-2026-10"
f("cl_km", C, "piste_km", 125, "measured", "G037", scope="total")
f("cl_lifts", C, "lifts_count", 50, "measured", "G037", scope="all_lifts")
f("cl_low", C, "area_low_m", 1050, "measured", "G037", scope="lowest_skiing")
f("cl_high", C, "area_high_m", 2485, "measured", "G037", scope="highest_skiing")
for g, v in (("easy", 53), ("intermediate", 33), ("difficult", 14)):
    f("cl_" + g, C, "grade_share_pct", v, "measured", "G037", scope="listing_length", q={"grade": g})
f("cl_1d", "pass:la-clusaz-manigod", "pass_price_eur", 56.5, "operator", "G036", q=hi("adult", 1), season="2026/27")
f("cl_6d", "pass:la-clusaz-manigod", "pass_price_eur", 285, "operator", "G036", q=hi("adult", 6), season="2026/27")
f("cl_gva", C, "road_km", 58, "modelled", "G039", q={"from": "poi:gva", "bound": "min"}, ds=ROAD_DS)
# roads (scoring run)
for key, src, lo, hi_ in (("lys", "poi:lys", 188, 205), ("cmf", "poi:cmf", 111, 128)):
    f(f"{key}_min", A, "road_km", lo, "modelled", "G032", q={"from": src, "bound": "min"}, ds=ROAD_DS)
    f(f"{key}_max", A, "road_km", hi_, "modelled", "G032", q={"from": src, "bound": "max"}, ds=ROAD_DS)

# network model
t = RUN["totals"]
f("m_lifts", A, "lifts_count", t["lifts"], "modelled", "G034", scope="all_mapped", ds=NET_DS)
f("m_main", A, "lifts_count", t["main"], "modelled", "G034", scope="main_lifts_mapped", ds=NET_DS)
f("m_drags", A, "drag_lifts_count", t["drags"], "modelled", "G034", ds=NET_DS)
f("m_km", A, "piste_km", t["pisteKm"], "modelled", "G034", scope="mapped_length", ds=NET_DS)
for sid in IDS:
    s = RUN["sectors"][sid]
    f("lo." + sid, S(sid), "lift_base_min_m", s["lo"], "modelled", "G034", ds=NET_DS)
    f("hi." + sid, S(sid), "lift_top_max_m", s["hi"], "modelled", "G034", ds=NET_DS)
    f("easy." + sid, S(sid), "grade_share_pct", round(100 * s["easyKm"] / s["km"]), "modelled", "G034", scope="mapped_length", q={"grade": "easy"}, ds=NET_DS)
    f("black." + sid, S(sid), "grade_share_pct", round(100 * s["blackKm"] / s["km"]), "modelled", "G034", scope="mapped_length", q={"grade": "difficult"}, ds=NET_DS)
    f("drag." + sid, S(sid), "drag_lift_share_pct", round(100 * s["drags"] / s["main"]), "modelled", "G034", ds=NET_DS, note="Share of main lifts")
# base table: five villages plus four upper bases, to five targets and a lift top above 2,400 m
BX = RUN["basesExtra"]
BASE_PLACE = {"flaine": S("flaine"), "carroz": S("carroz"), "morillon": S("morillon"), "samoens": S("samoens"), "sixt": S("sixt"),
              "vercland": "village:vercland", "morillon-1100": "village:morillon-1100", "samoens-1600": "village:samoens-1600", "flaine-foret": "village:flaine-foret"}
TARGET = {"flaine": S("flaine"), "carroz": S("carroz"), "samoens-1600": "village:samoens-1600", "morillon-1100": "village:morillon-1100",
          "sixt": S("sixt"), "top2400": "lift_top_above_2400"}
for b, row in BX.items():
    for col, v in row.items():
        f(f"b.{b}.{col}", BASE_PLACE[b], "lift_rides_from_village", v, "modelled", "G034", q={"to": TARGET[col]}, ds=NET_DS)
crit = {}
for c in RUN["critical"]:
    crit.setdefault(c[0], c)
for key, name in (("kedeuze", "Kédeuze"), ("morillon", "Morillon"), ("sairon", "Sairon")):
    f("cut." + key, L(key), "sector_pairs_cut_count", crit[name][2], "modelled", "G034", ds=NET_DS)
for key, name in (("coulouvrier", "Coulouvrier"), ("tete-des-saix", "Tête des Saix")):
    f("extra." + key, L(key), "extra_lift_rides_count", crit[name][3], "modelled", "G034", ds=NET_DS, note="Added lift rides summed over sector pairs when closed")

# snowfall from the series
snow = list(csv.DictReader(open("data/snow_era5_seasons.csv")))
num = lambda x: int(x) if float(x).is_integer() else x
med = lambda h, a, b: num(statistics.median(int(r[f"snowfall_cm_{h}"]) for r in snow if a <= int(r["season_start"]) <= b))
for h in (1100, 1600, 2100):
    f(f"s{h}", CELL, "snowfall_median_cm", med(h, 1991, 2020), "reanalysis", "G033", q={"period": "1991-2020", "elevation_m": h}, ds=SNOW_DS)
    f(f"s{h}_old", CELL, "snowfall_median_cm", med(h, 1961, 1990), "reanalysis", "G033", q={"period": "1961-1990", "elevation_m": h}, ds=SNOW_DS)
cl = json.load(open("data/snow_era5_clusaz_1600.json"))["seasons"]
f("cl_snow", CL_CELL, "snowfall_median_cm", num(statistics.median(cl[str(y)] for y in range(1991, 2021))), "reanalysis", "G038",
  q={"period": "1991-2020", "elevation_m": 1600}, ds=CL_DS)

RULES = {"piste_km": ("area resort pass", "operator measured modelled editorial"), "lifts_count": ("area resort", "operator measured modelled editorial"),
         "runs_count": ("area resort", "operator measured modelled editorial"), "area_low_m": ("area", "operator measured modelled"), "area_high_m": ("area", "operator measured modelled"),
         "lift_base_min_m": ("sector resort village", "modelled measured operator"), "lift_top_max_m": ("sector resort", "modelled measured operator"),
         "facility_count": ("area resort", "operator measured modelled editorial"), "event_year": ("area resort village", "operator measured modelled editorial"),
         "season_opens": ("area resort pass", "operator measured editorial"), "season_closes": ("area resort pass village", "operator measured editorial"),
         "pass_price_eur": ("pass", "operator estimated"), "snowfall_median_cm": ("cell", "reanalysis"), "road_km": ("area village resort", "modelled"),
         "run_length_km": ("poi piste", "operator measured editorial"), "grade_share_pct": ("area resort sector", "operator measured modelled"),
         "drag_lift_share_pct": ("resort area sector", "modelled"), "lift_rides_from_village": ("village sector", "modelled"), "opened_year": ("poi lift", "operator editorial"),
         "ride_minutes": ("lift", "operator editorial"), "sector_pairs_cut_count": ("lift", "modelled"), "extra_lift_rides_count": ("lift", "modelled"),
         "trail_km": ("area resort village", "operator measured"), "kids_club_min_age_years": ("poi resort village", "operator"), "free_pass_under_age_years": ("pass", "operator"),
         "drag_lifts_count": ("area resort", "modelled operator measured")}
for r in rows:
    assert r["method"] not in ("modelled", "reanalysis") or r["dataset"], (r["name"], "dataset")
    types, methods = RULES[r["property"]]
    assert r["place_id"].split(":")[0] in types.split(), (r["name"], "place type")
    assert r["method"] in methods.split(), (r["name"], "method")

cols = ["name", "place_id", "property", "value", "unit", "method", "legacy_ref", "scope", "qualifiers", "season", "dataset", "note", "source_id"]
with open("data/facts.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, cols)
    w.writeheader()
    w.writerows(rows)

# network file in the site format, every row from the village lifts
easy = {a: dict(RUN["all"][a]) for a in IDS}
for a, row in RUN["easy_differs_from_all"].items():
    easy[a].update(row)
red = {a: dict(RUN["all"][a]) for a in IDS}
for a, row in RUN["red_differs_from_all"].items():
    red[a].update(row)
net = {"source": "snowcatcher research/grand-massif model/run_2026-10-26.json, OpenStreetMap snapshot " + RUN["snapshot"] + "; from the village lifts in each area",
       "ids": IDS, "all": {a: RUN["all"][a] for a in IDS}, "ability": {"ids": IDS, "easy": easy, "red": red}}
json.dump(net, open("model/network.json", "w", encoding="utf-8"), ensure_ascii=False)
print(len(rows), "facts")
