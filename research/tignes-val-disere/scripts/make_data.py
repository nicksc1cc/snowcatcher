"""Build facts.csv and model/network.json for the Tignes Val d'Isère package.
Hand facts are listed with their evidence record; model facts come from the network run.
Usage: python3 scripts/make_data.py  (from research/tignes-val-disere)"""
import csv, json

RUN = json.load(open("model/run_2026-10-24.json", encoding="utf-8"))
NET_DS, SNOW_DS, ROAD_DS = "ds:tvi-network-2026-10-24", "ds:tvi-era5-snow-2026-10-24", "ds:tvi-osrm-2026-10-24"
A, TG, VI = "area:tignes-val-disere", "resort:tignes", "resort:val-disere"
CELL = "cell:era5.45.5.7.0"
IDS = ["brevieres", "le-lac", "val-claret", "grande-motte", "la-daille", "val-disere", "solaise", "le-fornet"]
BASES = ["val-claret", "le-lac", "val-disere", "la-daille", "brevieres", "le-fornet"]
COLS = ["le-lac", "val-disere", "le-fornet", "top3000"]
S = lambda s: "sector:tignes-val-disere." + s
L = lambda s: "lift:tignes-val-disere." + s
UNITS = {"piste_km": "km", "run_length_km": "km", "road_km": "km", "area_high_m": "m", "area_low_m": "m", "lift_top_max_m": "m",
         "lift_base_min_m": "m", "run_drop_m": "m", "snowfall_median_cm": "cm", "pass_price_eur": "eur", "family_pack_discount_eur": "eur",
         "grade_share_pct": "pct", "drag_lift_share_pct": "pct", "event_year": "year", "opened_year": "year", "season_opens": "date",
         "season_closes": "date", "reduced_period_starts": "date", "reduced_period_ends": "date", "high_season_starts": "date", "high_season_ends": "date"}
rows = []


def f(name, place, prop, value, method, ref, scope="", q=None, season="", ds="", note=""):
    rows.append(dict(name=name, place_id=place, property=prop, value=str(value), unit=UNITS.get(prop, "count"), method=method, legacy_ref=ref,
                     scope=scope, qualifiers=json.dumps(q, ensure_ascii=False) if q else "", season=season, dataset=ds, note=note, source_id=""))


# operator figures
f("op_km", A, "piste_km", 300, "operator", "T003", scope="total")
f("runs_total", A, "runs_count", 161, "operator", "T003", q={"grade": "total"})
for g, v in (("green", 23), ("blue", 67), ("red", 41), ("black", 30)):
    f("runs_" + g, A, "runs_count", v, "operator", "T003", q={"grade": g})
f("op_lifts74", A, "lifts_count", 74, "operator", "T003", scope="all_lifts", note="Guide Ski, Tignes page")
f("op_lifts71", A, "lifts_count", 71, "operator", "T004", scope="all_lifts", note="Guide Ski, Val d'Isère page")
f("op_high", A, "area_high_m", 3456, "operator", "T003", scope="highest_skiing")
f("op_low", A, "area_low_m", 1550, "operator", "T003", scope="lowest_skiing")
f("open_tignes", TG, "season_opens", "2026-11-21", "operator", "T003")
f("open_linked", A, "season_opens", "2026-11-28", "operator", "T003", scope="linked")
f("close_linked", A, "season_closes", "2027-05-02", "operator", "T003", scope="linked")
# history
f("tg_flooded", TG, "event_year", 1952, "editorial", "T021", q={"event": "old_village_flooded"})
f("tg_olympic", TG, "event_year", 1992, "editorial", "T021", q={"event": "olympic_freestyle"})
f("vi_olympic", VI, "event_year", 1992, "editorial", "T022", q={"event": "olympic_downhill"})
f("vi_worlds", VI, "event_year", 2009, "editorial", "T022", q={"event": "world_championships"})
# lifts, runs, places
f("pn_minutes", L("perce-neige"), "ride_minutes", 7, "editorial", "T003", note="About seven minutes")
f("ok_len", "piste:tignes-val-disere.oreiller-killy", "run_length_km", 3, "operator", "T004", note="Just over 3 km")
f("ok_drop", "piste:tignes-val-disere.oreiller-killy", "run_drop_m", 900, "operator", "T004", note="About 900 m")
f("gm_drop", "piste:tignes-val-disere.grande-motte-glacier", "run_drop_m", 1350, "operator", "T003", note="About 1,350 m from the glacier to Val Claret when fully open")
f("cobra_len", "poi:expedition-cobra", "run_length_km", 3, "operator", "T003", note="About 3 km")
f("folie_opened", "poi:la-folie-douce-val-disere", "opened_year", 1982, "editorial", "T062")
f("dicks_opened", "poi:dicks-tea-bar", "opened_year", 1979, "editorial", "T064")
# passes
PA, PT, PV = "pass:tignes-val-disere", "pass:tignes", "pass:val-disere"
hi = lambda age, d: dict(age=age, days=d, period="high")
f("child_1d", PA, "pass_price_eur", 63, "operator", "T001", q=hi("child", 1), season="2026/27", note="Reduced rate, 8 to 18 and 65 to 74")
f("child_6d", PA, "pass_price_eur", 378, "operator", "T001", q=hi("child", 6), season="2026/27", note="Reduced rate, 8 to 18 and 65 to 74; six days = seven days")
f("early_1d", PA, "pass_price_eur", 67, "operator", "T003", q={"age": "adult", "days": 1, "period": "reduced"}, season="2026/27")
f("tg_1d", PT, "pass_price_eur", 70, "operator", "T001", q=hi("adult", 1), season="2026/27")
f("tg_1d_early", PT, "pass_price_eur", 60, "operator", "T003", q={"age": "adult", "days": 1, "period": "reduced"}, season="2026/27", note="28 Nov to 11 Dec 2026 and 24 Apr to 2 May 2027")
f("vi_1d", PV, "pass_price_eur", 70, "operator", "T004", q=hi("adult", 1), season="2026/27")
f("vi_1d_early", PV, "pass_price_eur", 60, "operator", "T004", q={"age": "adult", "days": 1, "period": "reduced"}, season="2026/27")
f("red1_start", PA, "reduced_period_starts", "2026-11-28", "operator", "T003", q={"part": 1})
f("red1_end", PA, "reduced_period_ends", "2026-12-11", "operator", "T003", q={"part": 1})
f("red2_start", PA, "reduced_period_starts", "2027-04-24", "operator", "T003", q={"part": 2})
f("red2_end", PA, "reduced_period_ends", "2027-05-02", "operator", "T003", q={"part": 2})
f("high_start", PA, "high_season_starts", "2026-12-12", "operator", "T001")
f("high_end", PA, "high_season_ends", "2027-04-23", "operator", "T001")
f("family_pack", PA, "family_pack_discount_eur", 330, "operator", "T003", q={"passes": 4}, season="2026/27",
  note="Off the total, not per pass; four or more passes of 6 to 13 days, with at least two adults of 19 to 64 and two children of 8 to 18")
# network model
t = RUN["totals"]
f("m_lifts", A, "lifts_count", t["lifts"], "modelled", "T020", scope="all_mapped", ds=NET_DS, note="Includes the two funiculars")
f("m_main", A, "lifts_count", t["main"], "modelled", "T020", scope="main_lifts_mapped", ds=NET_DS)
f("m_drags", A, "drag_lifts_count", t["drags"], "modelled", "T020", ds=NET_DS)
f("m_sections", A, "piste_sections_count", t["pisteWays"], "modelled", "T020", ds=NET_DS)
f("m_km", A, "piste_km", t["pisteKm"], "modelled", "T020", scope="mapped_length", ds=NET_DS)
for sid in IDS:
    s = RUN["sectors"][sid]
    f("lo." + sid, S(sid), "lift_base_min_m", s["lo"], "modelled", "T020", ds=NET_DS)
    f("hi." + sid, S(sid), "lift_top_max_m", s["hi"], "modelled", "T020", ds=NET_DS)
    f("easy." + sid, S(sid), "grade_share_pct", round(100 * s["easyKm"] / s["km"]), "modelled", "T020", scope="mapped_length", q={"grade": "easy"}, ds=NET_DS)
    f("drag." + sid, S(sid), "drag_lift_share_pct", round(100 * s["drags"] / s["main"]), "modelled", "T020", ds=NET_DS, note="Share of main lifts")
for sid in BASES:
    for col in COLS:
        f(f"b.{sid}.{col}", S(sid), "lift_rides_from_village", RUN["base"][sid][col], "modelled", "T020",
          q={"to": "lift_top_above_3000" if col == "top3000" else S(col)}, ds=NET_DS)
crit = {c[0]: c for c in RUN["critical"]}
f("leissieres_cut", L("leissieres"), "sector_pairs_cut_count", crit["Leissières"][2], "modelled", "T020", ds=NET_DS)
for key, name, lift in (("olympique_extra", "Olympique", "olympique"), ("solaise_extra", "Solaise", "solaise"),
                        ("tommeuses_extra", "Tommeuses", "tommeuses"), ("funival_extra", "Funival", "funival")):
    f(key, L(lift), "extra_lift_rides_count", crit[name][3], "modelled", "T020", ds=NET_DS)
# snowfall (F000105 already holds 263 cm at 1,600 m for 1991 to 2020 in this cell)
f("s1600_old", CELL, "snowfall_median_cm", 335.5, "reanalysis", "T030", q={"period": "1961-1990", "elevation_m": 1600}, ds=SNOW_DS)
for h, new, old in ((2100, 477.5, 525.5), (2600, 474.5, 523.5)):
    f(f"s{h}", CELL, "snowfall_median_cm", new, "reanalysis", "T030", q={"period": "1991-2020", "elevation_m": h}, ds=SNOW_DS)
    f(f"s{h}_old", CELL, "snowfall_median_cm", old, "reanalysis", "T030", q={"period": "1961-1990", "elevation_m": h}, ds=SNOW_DS)
# roads
f("gva_brev", "village:les-brevieres", "road_km", 175, "modelled", "T040", q={"from": "poi:gva"}, ds=ROAD_DS)
f("gva_fornet", "village:le-fornet", "road_km", 192, "modelled", "T040", q={"from": "poi:gva"}, ds=ROAD_DS)
for src, lo, hi_ in (("lys", 214, 231), ("cmf", 136, 153)):
    f(f"{src}_min", A, "road_km", lo, "modelled", "T040", q={"from": "poi:" + src, "bound": "min"}, ds=ROAD_DS)
    f(f"{src}_max", A, "road_km", hi_, "modelled", "T040", q={"from": "poi:" + src, "bound": "max"}, ds=ROAD_DS)
f("bsm_min", A, "road_km", 23, "modelled", "T040", q={"from": "poi:bourg-saint-maurice-station", "bound": "min"}, ds=ROAD_DS)
f("bsm_max", A, "road_km", 41, "modelled", "T040", q={"from": "poi:bourg-saint-maurice-station", "bound": "max"}, ds=ROAD_DS)

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
net = {"source": "snowcatcher research/tignes-val-disere model/run_2026-10-24.json, OpenStreetMap snapshot " + RUN["snapshot"] + "; from the first lift base in each area",
       "ids": IDS, "all": {a: RUN["all"][a] for a in IDS}, "ability": {"ids": IDS, "easy": easy, "red": red}}
json.dump(net, open("model/network.json", "w", encoding="utf-8"), ensure_ascii=False)
print(len(rows), "facts")
