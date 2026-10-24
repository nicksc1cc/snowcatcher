"""Build facts.csv, properties.csv and model/network.json for the Paradiski package.
Hand facts are listed below with their evidence record; model facts are read from the network run.
Usage: python3 scripts/make_data.py  (from research/paradiski)"""
import csv, json

RUN = json.load(open("model/run_2026-10-24.json", encoding="utf-8"))
NET_DS, SNOW_DS, ROAD_DS = "ds:paradiski-network-2026-10-24", "ds:paradiski-era5-snow-2026-10-24", "ds:paradiski-osrm-2026-10-24"
A, LP, LA, PV = "area:paradiski", "resort:la-plagne", "resort:les-arcs", "resort:peisey-vallandry"
CELL = "cell:era5.45.5.6.75"
IDS = ["montalbert", "plagne-centre", "bellecote", "champagny", "montchavin-les-coches",
       "peisey-vallandry", "arc-1600", "arc-1800", "arc-2000", "villaroger"]
S = lambda s: "sector:paradiski." + s
rows = []


UNITS = {"piste_km": "km", "run_length_km": "km", "road_km": "km", "area_high_m": "m", "lift_top_max_m": "m", "lift_base_min_m": "m",
         "lift_length_m": "m", "span_height_m": "m", "run_drop_m": "m", "snowfall_median_cm": "cm", "pass_price_eur": "eur",
         "family_pack_discount_eur": "eur", "grade_share_pct": "pct", "drag_lift_share_pct": "pct", "event_year": "year",
         "opened_year": "year", "season_opens": "date", "season_closes": "date", "reduced_period_starts": "date", "reduced_period_ends": "date"}


def f(name, place, prop, value, method, ref, scope="", q=None, season="", ds="", note=""):
    rows.append(dict(name=name, place_id=place, property=prop, value=str(value), unit=UNITS.get(prop, "count"), method=method, legacy_ref=ref,
                     scope=scope, qualifiers=json.dumps(q, ensure_ascii=False) if q else "", season=season, dataset=ds,
                     note=note, source_id=""))


# operator figures for the whole area
f("op_km", A, "piste_km", 425, "operator", "P001", scope="total")
f("op_runs", A, "runs_count", 260, "operator", "P001", q={"grade": "total"})
f("op_top", A, "area_high_m", 3226, "operator", "P001", scope="highest_skiing")
f("op_resorts", A, "resorts_count", 3, "operator", "P001")
f("par_opens", A, "season_opens", "2026-12-12", "operator", "P003", scope="linked")
f("ve_closes", A, "season_closes", "2027-04-17", "operator", "P003", scope="linked",
  note="Last day of the Vanoise Express; Montalbert, Champagny and Montchavin-Les Coches close the same day (P004)")
# resorts
f("lp_opens", LP, "season_opens", "2026-12-12", "operator", "P005")
f("lp_closes", LP, "season_closes", "2027-04-24", "operator", "P005", note="High altitude area of La Plagne")
f("la_closes", LA, "season_closes", "2027-04-24", "operator", "P003")
f("lp_km", LP, "piste_km", 225, "operator", "P004", scope="total")
f("lp_runs", LP, "runs_count", 139, "operator", "P004", q={"grade": "total"})
f("lp_blue", LP, "runs_count", 78, "operator", "P004", q={"grade": "blue"})
f("lp_lifts", LP, "lifts_count", 77, "operator", "P004", scope="all_lifts")
f("lp_top", LP, "lift_top_max_m", 3080, "operator", "P004", note="Live 3000, top of the Glaciers gondola")
f("la_km", LA, "piste_km", 200, "operator", "P003", scope="total", note="Les Arcs with Peisey-Vallandry")
f("la_lifts", LA, "lifts_count", 52, "operator", "P003", scope="all_lifts", note="Les Arcs with Peisey-Vallandry")
for g, v in (("green", 14), ("blue", 51), ("red", 35), ("black", 17)):
    f("la_" + g, LA, "runs_count", v, "operator", "P003", q={"grade": g}, note="Les Arcs with Peisey-Vallandry")
# history
f("lp_opened", LP, "event_year", 1961, "editorial", "P022", q={"event": "opened"})
f("lp_olympic", LP, "event_year", 1992, "editorial", "P022", q={"event": "olympic_bobsleigh"})
f("la_1600", LA, "event_year", 1968, "editorial", "P023", q={"event": "arc_1600_opens"})
f("la_1800", LA, "event_year", 1974, "editorial", "P023", q={"event": "arc_1800_opens"})
f("la_2000", LA, "event_year", 1979, "editorial", "P023", q={"event": "arc_2000_opens"})
f("la_1950", LA, "event_year", 2003, "editorial", "P023", q={"event": "arc_1950_first_residences"})
f("la_olympic", LA, "event_year", 1992, "editorial", "P023", q={"event": "olympic_speed_skiing"})
# lifts and runs
VE = "lift:paradiski.vanoise-express"
f("ve_opened", VE, "opened_year", 2003, "editorial", "P021")
f("ve_len", VE, "lift_length_m", 1800, "editorial", "P021")
f("ve_height", VE, "span_height_m", 380, "editorial", "P021")
f("ve_cap", VE, "cabin_capacity", 200, "editorial", "P021", note="More than 200 per cabin")
f("ve_min", VE, "ride_minutes", 4, "editorial", "P021")
f("fun_opened", "lift:paradiski.arc-en-ciel", "opened_year", 1986, "editorial", "P023")
f("fun_min", "lift:paradiski.arc-en-ciel", "ride_minutes", 7, "editorial", "P003")
f("lonzagne_cap", "lift:paradiski.lonzagne", "cabin_capacity", 10, "editorial", "P003", note="Seated places; from Christmas 2026")
f("av_len", "piste:paradiski.aiguille-rouge-villaroger", "run_length_km", 7, "operator", "P024")
f("av_drop", "piste:paradiski.aiguille-rouge-villaroger", "run_drop_m", 2000, "operator", "P024", note="More than 2,000 m")
f("folie_opened", "poi:la-folie-douce-les-arcs", "opened_year", 2019, "editorial", "P062")
# passes
PLP, PLA, PP = "pass:la-plagne", "pass:les-arcs-peisey-vallandry", "pass:paradiski"
hi = lambda age, d, **k: dict(age=age, days=d, period="high", **k)
f("lp_1d", PLP, "pass_price_eur", 72, "operator", "P004", q=hi("adult", 1), season="2026/27")
f("lp_6d", PLP, "pass_price_eur", 370, "operator", "P004", q=hi("adult", 6), season="2026/27")
f("lp_c1d", PLP, "pass_price_eur", 58, "operator", "P004", q=hi("child", 1), season="2026/27")
f("lp_c6d", PLP, "pass_price_eur", 296, "operator", "P004", q=hi("child", 6), season="2026/27")
f("lp_red6", PLP, "pass_price_eur", 314.5, "operator", "P004", q={"age": "adult", "days": 6, "period": "reduced"}, season="2026/27")
f("lp_red_start", PLP, "reduced_period_starts", "2026-12-12", "operator", "P004", q={"part": 1})
f("lp_red_end", PLP, "reduced_period_ends", "2026-12-18", "operator", "P004", q={"part": 1})
f("la_1d", PLA, "pass_price_eur", 71, "operator", "P002", q=hi("adult", 1), season="2026/27", note="Classic pass")
f("la_6d", PLA, "pass_price_eur", 368, "operator", "P002", q=hi("adult", 6), season="2026/27", note="Classic pass")
f("par_c1d", PP, "pass_price_eur", 63, "operator", "P004", q=hi("child", 1), season="2026/27")
f("par_c6d", PP, "pass_price_eur", 330, "operator", "P004", q=hi("child", 6), season="2026/27")
f("prem_1d", PP, "pass_price_eur", 91, "operator", "P002", q=hi("adult", 1, product="premium"), season="2026/27")
f("prem_6d", PP, "pass_price_eur", 491, "operator", "P002", q=hi("adult", 6, product="premium"), season="2026/27")
f("family_pack", PP, "family_pack_discount_eur", 25, "operator", "P004", q={"passes": 4}, season="2026/27",
  note="Per person; four simultaneous Paradiski passes of six to eight days, two people of 13 to 74 and at least two of 5 to 17")
# network model
t = RUN["totals"]
f("m_lifts", A, "lifts_count", t["lifts"], "modelled", "P020", scope="all_mapped", ds=NET_DS)
f("m_main", A, "lifts_count", t["main"], "modelled", "P020", scope="main_lifts_mapped", ds=NET_DS)
f("m_drags", A, "drag_lifts_count", t["drags"], "modelled", "P020", ds=NET_DS)
f("m_sections", A, "piste_sections_count", t["pisteWays"], "modelled", "P020", ds=NET_DS)
f("m_km", A, "piste_km", t["pisteKm"], "modelled", "P020", scope="mapped_length", ds=NET_DS)
for sid in IDS:
    s = RUN["sectors"][sid]
    f("lo." + sid, S(sid), "lift_base_min_m", s["lo"], "modelled", "P020", ds=NET_DS)
    f("hi." + sid, S(sid), "lift_top_max_m", s["hi"], "modelled", "P020", ds=NET_DS)
    f("easy." + sid, S(sid), "grade_share_pct", round(100 * s["easyKm"] / s["km"]), "modelled", "P020", scope="mapped_length", q={"grade": "easy"}, ds=NET_DS)
    f("drag." + sid, S(sid), "drag_lift_share_pct", round(100 * s["drags"] / s["main"]), "modelled", "P020", ds=NET_DS, note="Share of main lifts")
    for col in ("plagne-centre", "arc-1800", "arc-2000", "top3000"):
        f(f"b.{sid}.{col}", S(sid), "lift_rides_from_village", RUN["base"][sid][col], "modelled", "P020",
          q={"to": "lift_top_above_3000" if col == "top3000" else S(col)}, ds=NET_DS)
crit = {c[0]: c for c in RUN["critical"]}
f("ve_cut", VE, "sector_pairs_cut_count", crit["Vanoise Express 1"][2], "modelled", "P020", ds=NET_DS)
f("peisey_cut", "lift:paradiski.peisey", "sector_pairs_cut_count", crit["Peisey"][2], "modelled", "P020", ds=NET_DS)
f("montalbert_cut", "lift:paradiski.montalbert", "sector_pairs_cut_count", crit["Montalbert"][2], "modelled", "P020", ds=NET_DS)
f("bijolin_extra", "lift:paradiski.bijolin", "extra_lift_rides_count", crit["Bijolin"][3], "modelled", "P020", ds=NET_DS)
f("colosses_extra", "lift:paradiski.colosses", "extra_lift_rides_count", crit["Colosses"][3], "modelled", "P020", ds=NET_DS)
# snowfall
for h, new, old in ((1600, 288, 348), (2100, 478.5, 534.5), (2600, 478, 532)):
    f(f"s{h}", CELL, "snowfall_median_cm", new, "reanalysis", "P030", q={"period": "1991-2020", "elevation_m": h}, ds=SNOW_DS)
    f(f"s{h}_old", CELL, "snowfall_median_cm", old, "reanalysis", "P030", q={"period": "1961-1990", "elevation_m": h}, ds=SNOW_DS)
# roads
f("gva_champagny", "village:champagny-en-vanoise", "road_km", 142, "modelled", "P040", q={"from": "poi:gva"}, ds=ROAD_DS)
f("gva_arc2000", "village:arc-2000", "road_km", 175, "modelled", "P040", q={"from": "poi:gva"}, ds=ROAD_DS)
f("lys_min", A, "road_km", 181, "modelled", "P040", q={"from": "poi:lys", "bound": "min"}, ds=ROAD_DS)
f("lys_max", A, "road_km", 215, "modelled", "P040", q={"from": "poi:lys", "bound": "max"}, ds=ROAD_DS)
f("cmf_min", A, "road_km", 103, "modelled", "P040", q={"from": "poi:cmf", "bound": "min"}, ds=ROAD_DS)
f("cmf_max", A, "road_km", 136, "modelled", "P040", q={"from": "poi:cmf", "bound": "max"}, ds=ROAD_DS)

cols = ["name", "place_id", "property", "value", "unit", "method", "legacy_ref", "scope", "qualifiers", "season", "dataset", "note", "source_id"]
with open("data/facts.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, cols)
    w.writeheader()
    w.writerows(rows)

with open("data/properties.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["key", "label", "value_type", "unit", "applies_to", "qualifier_keys", "allowed_methods", "definition", "requires_scope"])
    w.writerow(["sector_pairs_cut_count", "Sector pairs cut", "number", "count", "lift", "", "modelled",
                "Ordered pairs of sectors that can no longer reach each other when this lift closes", "false"])
    w.writerow(["extra_lift_rides_count", "Extra lift rides", "number", "count", "lift", "", "modelled",
                "Lift rides added across all sector pairs when this lift closes", "false"])

# network file in the site format
easy = {a: dict(RUN["all"][a]) for a in IDS}
for a, row in RUN["easy_differs_from_all"].items():
    easy[a].update(row)
assert RUN["red_equals_easy"]
net = {"source": "snowcatcher research/paradiski model/run_2026-10-24.json, OpenStreetMap snapshot " + RUN["snapshot"] + "; from the first lift base in each area",
       "ids": IDS, "all": {a: RUN["all"][a] for a in IDS}, "ability": {"ids": IDS, "easy": easy, "red": easy}}
json.dump(net, open("model/network.json", "w", encoding="utf-8"), ensure_ascii=False)
print(len(rows), "facts")
