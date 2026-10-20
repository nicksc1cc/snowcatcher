"""Build the Les 3 Vallées pilot seed for the Snow Catchers database.

Reads the live page data (projectsnow src/data/l3/les-3-vallees*.json/csv) and the evidence
register, and writes seed SQL plus a coverage report. Every figure that becomes a fact is
checked: the formatted fact must equal the text on the live page, or the build stops.

Usage: python3 build_seed.py <projectsnow dir> <out dir>
"""
import csv
import json
import os
import re
import sys
import unicodedata
from urllib.parse import quote, urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from snowdb import q, qarr, fmt_fact, resolve_text, token_refs  # noqa: E402

SITE, OUT = sys.argv[1], sys.argv[2]
L3 = os.path.join(SITE, "src/data/l3")
REGDIR = os.path.join(os.path.dirname(os.path.dirname(HERE)), "research/les-3-vallees/data")
PAGE = json.load(open(os.path.join(L3, "les-3-vallees.json"), encoding="utf-8"))
NET = json.load(open(os.path.join(L3, "les-3-vallees.network.json"), encoding="utf-8"))
SNOW = list(csv.DictReader(open(os.path.join(L3, "les-3-vallees.snow.csv"), encoding="utf-8")))
REG = {r["id"]: r for r in csv.DictReader(open(os.path.join(REGDIR, "evidence_register.csv"), encoding="utf-8"))}
MATRICES = {"all": NET["all"], "easy": NET["ability"]["easy"], "red": NET["ability"]["red"]}

A = "area:les-3-vallees"
DS_NET, DS_SNOW = "ds:l3v-network-2026-10-20", "ds:l3v-era5-snow-2026-10-20"
DS_CMP, DS_OSRM = "ds:savoie-era5-compare-2026-10-20", "ds:l3v-osrm-2026-10-20"
CELL = "cell:era5.45.25.6.5"
RETRIEVED = "2026-10-20"
ACCEPTED_BY = "Nick (page approved for publication 20 Oct 2026; pilot import)"


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


# ---------------------------------------------------------------- places
places, links, aliases = [], [], []


def place(pid, name, **kw):
    places.append(dict(id=pid, type=pid.split(":")[0], name=name, slug=kw.pop("slug", slug(name)), **kw))
    return pid


def link(a, b, rel, primary=False, ord_=None, cond=None):
    links.append((a, b, rel, primary, ord_, cond or {}))


place("country:fr", "France")
place("country:ch", "Switzerland")
place("region:savoie", "Savoie"); link("region:savoie", "country:fr", "in_country", True)
place("range:northern-alps", "Northern Alps"); link("range:northern-alps", "country:fr", "in_country", True)
place(A, "Les 3 Vallées", summary="Three valleys of the Tarentaise on one lift system, from Brides-les-Bains to the summit above Orelle.")
link(A, "range:northern-alps", "in_range", True); link(A, "region:savoie", "in_region"); link(A, "country:fr", "in_country")
for al in ["Les Trois Vallées", "The Three Valleys", "3 Vallées", "les-trois-vallees"]:
    aliases.append((A, al))
for pid, nm in [("area:paradiski", "Paradiski"), ("area:tignes-val-disere", "Tignes Val d'Isère"), ("area:les-sybelles", "Les Sybelles")]:
    place(pid, nm); link(pid, "range:northern-alps", "in_range", True); link(pid, "region:savoie", "in_region"); link(pid, "country:fr", "in_country")
aliases += [("area:tignes-val-disere", "Espace Killy"), ("area:tignes-val-disere", "Tignes-Val d'Isère"), ("area:tignes-val-disere", "espace-killy")]
place("area:portes-du-soleil", "Portes du Soleil"); link("area:portes-du-soleil", "country:fr", "in_country", True); link("area:portes-du-soleil", "country:ch", "in_country")

RESORTS = {"Courchevel": "courchevel", "La Tania": "la-tania", "Méribel": "meribel", "Brides-les-Bains": "brides-les-bains",
           "Saint-Martin-de-Belleville": "saint-martin-de-belleville", "Les Menuires": "les-menuires", "Val Thorens": "val-thorens", "Orelle": "orelle"}
for nm, s in RESORTS.items():
    place("resort:" + s, nm); link("resort:" + s, A, "in_area", True)

VILLAGES = {  # page base label -> (village slug, name, resort slug, sector id)
    "Le Praz": ("le-praz", "Le Praz", "courchevel", "le-praz"),
    "Courchevel 1550": ("courchevel-1550", "Courchevel 1550", "courchevel", "c1550"),
    "Courchevel 1850": ("courchevel-1850", "Courchevel 1850", "courchevel", "c1850"),
    "Moriond": ("courchevel-moriond", "Moriond", "courchevel", "moriond"),
    "La Tania": ("la-tania", "La Tania", "la-tania", "la-tania"),
    "Méribel": ("meribel", "Méribel", "meribel", "meribel"),
    "Méribel-Mottaret": ("meribel-mottaret", "Méribel-Mottaret", "meribel", "mottaret"),
    "Brides-les-Bains": ("brides-les-bains", "Brides-les-Bains", "brides-les-bains", "brides"),
    "Saint-Martin": ("saint-martin-de-belleville", "Saint-Martin-de-Belleville", "saint-martin-de-belleville", "saint-martin"),
    "Les Menuires": ("les-menuires", "Les Menuires", "les-menuires", "menuires"),
    "Val Thorens": ("val-thorens", "Val Thorens", "val-thorens", "val-thorens"),
    "Orelle": ("orelle", "Orelle", "orelle", "orelle"),
}
SEC = lambda sid: "sector:les-3-vallees." + sid  # noqa: E731
for s in PAGE["sectors"]:
    place(SEC(s["id"]), s["name"], slug="les-3-vallees-" + s["id"])
    link(SEC(s["id"]), A, "in_area", True); link(SEC(s["id"]), "resort:" + RESORTS[s["base"]], "in_resort")
for label, (vs, nm, rs, sid) in VILLAGES.items():
    place("village:" + vs, nm); link("village:" + vs, "resort:" + rs, "in_resort", True); link("village:" + vs, SEC(sid), "serves")
aliases += [("village:courchevel-moriond", "Courchevel 1650"), ("village:courchevel-moriond", "Courchevel Moriond"), ("village:meribel-mottaret", "Mottaret")]

PASSES = {"pass:les-3-vallees": "Les 3 Vallées pass", "pass:meribel-valley": "Méribel valley pass",
          "pass:les-menuires-saint-martin": "Les Menuires and Saint-Martin pass", "pass:val-thorens-orelle": "Val Thorens and Orelle pass",
          "pass:paradiski": "Paradiski pass", "pass:tignes-val-disere": "Tignes Val d'Isère pass", "pass:les-sybelles": "Les Sybelles pass"}
for pid, nm in PASSES.items():
    place(pid, nm)
link("pass:les-3-vallees", A, "covers", True)
for s in RESORTS.values():
    link("pass:les-3-vallees", "resort:" + s, "covers")
link("pass:meribel-valley", "resort:meribel", "covers", True)
link("pass:les-menuires-saint-martin", "resort:les-menuires", "covers", True); link("pass:les-menuires-saint-martin", "resort:saint-martin-de-belleville", "covers")
link("pass:val-thorens-orelle", "resort:val-thorens", "covers", True); link("pass:val-thorens-orelle", "resort:orelle", "covers")
for a in ["paradiski", "tignes-val-disere", "les-sybelles"]:
    link("pass:" + a, "area:" + a, "covers", True)

for pid, lat, lon, area in [(CELL, 45.25, 6.5, A), ("cell:era5.45.5.6.75", 45.5, 6.75, "area:paradiski"),
                            ("cell:era5.45.5.7.0", 45.5, 7.0, "area:tignes-val-disere"), ("cell:era5.45.25.6.25", 45.25, 6.25, "area:les-sybelles")]:
    place(pid, f"ERA5 cell {lat} N {lon} E", slug=slug(pid.split(":")[1]), lat=lat, lon=lon); link(pid, area, "serves")

for pid, nm, sub, c in [("poi:gva", "Geneva Airport", "airport", "country:ch"), ("poi:lys", "Lyon Saint-Exupéry Airport", "airport", "country:fr"),
                        ("poi:cmf", "Chambéry Savoie Mont Blanc Airport", "airport", "country:fr"),
                        ("poi:moutiers-station", "Moûtiers-Salins-Brides-les-Bains station", "station", "country:fr")]:
    place(pid, nm, subtype=sub); link(pid, c, "in_country", True)
aliases += [("poi:gva", "GVA"), ("poi:lys", "LYS"), ("poi:cmf", "CMF"), ("poi:moutiers-station", "Moûtiers")]

LIST_KIND = {"snowboard": "snowpark", "families": "family", "food": "eat", "apres": "apres"}
SUB = {"snowboard": "snowpark", "families": "family", "food": "restaurant", "apres": "bar"}
list_items = {}  # list id -> [(place id, attrs, blurb literal)]
for ch in PAGE["chapters"]:
    lid = "list:les-3-vallees." + ch["id"]
    list_items[lid] = []
    for it in ch["items"]:
        if it["name"] == "Ski routes":
            pid, attrs = A, {"name": "Ski routes", "where": it["where"]}
        else:
            pid = "poi:" + slug(it["name"])
            if it["name"] == "La Folie Douce":
                pid += "-" + slug(it["where"].split(", ")[-1])
            if not any(p["id"] == pid for p in places):
                place(pid, it["name"], subtype=SUB[ch["id"]]); link(pid, A, "in_area", True)
            attrs = {"where": it["where"]}
        list_items[lid].append([pid, attrs, it["text"]])

# ---------------------------------------------------------------- sources
STYPE = {"operator": "operator", "independent": "listing", "derived": "open_data", "model": "model",
         "press": "press", "tourism": "tourism", "internal": "internal"}
sources, src_of = {}, {}
for lid, r in REG.items():
    url = r["url"].strip()
    if not url:
        sid = "src:snow-catchers-analysis"
        sources.setdefault(sid, dict(id=sid, title="Snow Catchers analysis", publisher="Snow Catchers", url=None, source_type="internal"))
    else:
        u = urlparse(url)
        host = u.netloc.replace("www.", "")
        host = host.rsplit(".", 1)[0] if host.count(".") >= 1 else host
        sid = ("src:" + slug(host + "-" + u.path + ("-" + u.query if u.query else "")))[:64].rstrip("-")
        if sid not in sources:
            sources[sid] = dict(id=sid, title=r["source"], publisher=r["source"].split(" (")[0], url=url, source_type=STYPE[r["type"]])
    src_of[lid] = sid

# ---------------------------------------------------------------- properties
ALL = ["operator", "measured", "modelled", "reanalysis", "forecast", "estimated", "editorial", "scored"]
props, scopes = [], []


def prop(key, label, vtype, unit, applies, quals=(), scope=None, max_age=None, methods=ALL, definition=None, require=None):
    props.append(dict(key=key, label=label, value_type=vtype, unit=unit, applies_to=list(applies), qualifier_keys=list(quals),
                      max_age_days=max_age, allowed_methods=list(methods), definition=definition,
                      requires_scope=bool(scope) if require is None else require))
    for k, d in (scope or {}).items():
        scopes.append((key, k, d))


prop("piste_km", "Piste", "number", "km", ["area", "resort", "pass"], max_age=365,
     scope={"total": "Marked piste length as published for the whole area"})
prop("ski_routes_km", "Ski routes", "number", "km", ["area"], max_age=365, definition="Marked but ungroomed routes")
prop("lifts_count", "Lifts", "number", "count", ["area", "resort"], max_age=365, scope={
    "all_lifts": "Every lift on the pass as counted by the publisher",
    "all_mapped": "Every lift in the OpenStreetMap model",
    "main_lifts_mapped": "Cable cars, gondolas, chairs and drag lifts in the OpenStreetMap model, without carpets"})
prop("drag_lifts_count", "Drag lifts", "number", "count", ["area", "resort"], methods=["modelled", "operator", "measured"],
     definition="Platters, T bars and other surface lifts among the main mapped lifts")
prop("runs_count", "Runs", "number", "count", ["area", "resort"], quals=["grade"], max_age=365)
prop("grade_share_pct", "Share by difficulty", "number", "pct", ["area", "resort"], quals=["grade"], max_age=365, scope={
    "listing_length": "Share of piste length by difficulty in the skiresort.com listing",
    "mapped_length": "Share of mapped piste length in the OpenStreetMap model, green and blue counted as easy"})
prop("drag_lift_share_pct", "Drag lift share", "number", "pct", ["resort", "area"], methods=["modelled"])
prop("area_low_m", "Lowest point", "number", "m", ["area"], scope={"lowest_skiing": "Lowest point of the ski area as published"})
prop("area_high_m", "Highest point", "number", "m", ["area"], scope={"highest_skiing": "Highest point of the ski area as published"})
prop("lift_base_min_m", "Lowest lift base", "number", "m", ["sector", "resort", "village"], methods=["modelled", "measured", "operator"])
prop("lift_top_max_m", "Highest lift top", "number", "m", ["sector", "resort"], methods=["modelled", "measured", "operator"])
prop("share_above_1800_pct", "Share above 1,800 m", "number", "pct", ["area"])
prop("valleys_count", "Valleys", "number", "count", ["area"])
prop("resorts_count", "Resorts", "number", "count", ["area"], definition="Resorts as counted by the operator")
prop("restaurants_count", "Restaurants", "number", "count", ["area", "resort"], quals=["kind"], max_age=365)
prop("michelin_stars_count", "Michelin stars", "number", "count", ["area", "resort"], max_age=365)
prop("facility_count", "Facilities", "number", "count", ["area", "resort"], quals=["kind"], max_age=365)
prop("event_year", "Year", "number", "year", ["area", "resort", "village"], quals=["event"])
prop("piste_sections_count", "Mapped piste sections", "number", "count", ["area"], methods=["modelled"])
prop("season_opens", "Season opens", "date", "date", ["area", "resort", "pass"], max_age=200, scope={
    "linked": "Opening of the whole linked area", "earliest_sector": "Earliest opening of any part of the area"}, require=False)
prop("season_closes", "Season closes", "date", "date", ["area", "resort", "pass"], max_age=200, scope={
    "linked": "Closing of the whole linked area", "earliest_sector": "Latest closing of any part of the area"}, require=False)
prop("high_season_starts", "High season starts", "date", "date", ["pass"], max_age=200)
prop("high_season_ends", "High season ends", "date", "date", ["pass"], max_age=200)
prop("reduced_period_starts", "Reduced price period starts", "date", "date", ["pass"], quals=["part"], max_age=200)
prop("reduced_period_ends", "Reduced price period ends", "date", "date", ["pass"], quals=["part"], max_age=200)
prop("pass_price_eur", "Lift pass price", "number", "eur", ["pass"], quals=["age", "days", "period", "channel", "product"],
     max_age=200, methods=["operator", "estimated"])
prop("snowfall_median_cm", "Median seasonal snowfall", "number", "cm", ["cell"], quals=["elevation_m", "period"], methods=["reanalysis"],
     definition="Median of November to April snowfall totals over the period")
prop("road_km", "Road distance", "number", "km", ["area", "village", "resort"], quals=["from", "bound"], methods=["modelled"],
     definition="Fastest road route by the OSRM router, without traffic or snow")
prop("bus_fare_eur", "Bus fare", "number", "eur", ["poi"], max_age=365, methods=["operator"])
prop("bus_advance_discount_pct", "Advance booking discount", "number", "pct", ["poi"], max_age=365, methods=["operator"])
prop("run_length_km", "Run length", "number", "km", ["poi", "piste"])
prop("opened_year", "Open since", "number", "year", ["poi"])
prop("lift_rides_from_village", "Lift rides from the village", "number", "count", ["village"], quals=["to"], methods=["modelled"],
     definition="Fewest lift rides from the village lifts before reaching the first lift of the target, allowing a ride down where no piste returns")

# ---------------------------------------------------------------- facts
facts = {}  # name -> row
order = []


def fact(name, place_id, prop_key, value, method, L, scope=None, quals=None, ds=None, season=None, note=None, src=None):
    p = next(x for x in props if x["key"] == prop_key)
    row = dict(id=None, place_id=place_id, property=prop_key, scope=scope, qualifiers=quals or {}, season=season, method=method,
               source_id=src or (src_of[L] if L else None), dataset_id=ds, legacy_ref=L, note=note, unit=p["unit"],
               value_num=None, value_text=None)
    if p["value_type"] == "date":
        row["value_text"] = value
    else:
        row["value_num"] = value
    assert name not in facts, name
    facts[name] = row
    order.append(name)


S = "2026/27"
fact("piste_op", A, "piste_km", 600, "operator", "L001", "total")
fact("piste_sr", A, "piste_km", 600, "measured", "L010", "total")
fact("routes_km", A, "ski_routes_km", 50, "measured", "L010")
fact("lifts_op", A, "lifts_count", 169, "operator", "L001", "all_lifts")
fact("lifts_sr", A, "lifts_count", 159, "measured", "L010", "all_lifts")
fact("lifts_mapped", A, "lifts_count", 167, "modelled", "L020", "all_mapped", ds=DS_NET)
fact("main_lifts", A, "lifts_count", 132, "modelled", "L023", "main_lifts_mapped", ds=DS_NET)
fact("drags", A, "drag_lifts_count", 35, "modelled", "L023", ds=DS_NET)
fact("sections", A, "piste_sections_count", 1126, "modelled", "L020", ds=DS_NET)
for g, v in [("total", 337), ("green", 50), ("blue", 137), ("red", 113), ("black", 37)]:
    fact("runs_" + g, A, "runs_count", v, "operator", "L001", quals={"grade": g})
for g, v in [("easy", 56), ("intermediate", 34), ("difficult", 10)]:
    fact("gs_" + g, A, "grade_share_pct", v, "measured", "L010", "listing_length", {"grade": g})
fact("low_op", A, "area_low_m", 1300, "operator", "L001", "lowest_skiing")
fact("low_sr", A, "area_low_m", 1100, "measured", "L010", "lowest_skiing")
fact("high_op", A, "area_high_m", 3230, "operator", "L001", "highest_skiing")
fact("high_sr", A, "area_high_m", 3230, "measured", "L010", "highest_skiing")
fact("above1800", A, "share_above_1800_pct", 85, "operator", "L001")
fact("valleys", A, "valleys_count", 3, "operator", "L001")
fact("resorts7", A, "resorts_count", 7, "operator", "L001")
fact("rest_all", A, "restaurants_count", 355, "operator", "L001", quals={"kind": "all"})
fact("rest_mtn", A, "restaurants_count", 66, "operator", "L001", quals={"kind": "mountain"})
fact("rest_mich", A, "restaurants_count", 10, "operator", "L001", quals={"kind": "michelin"})
fact("stars", A, "michelin_stars_count", 15, "operator", "L001")
fact("parks", A, "facility_count", 4, "operator", "L080", quals={"kind": "snowpark"})
fact("funzones", A, "facility_count", 35, "operator", "L080", quals={"kind": "fun_zone"})
fact("yr_first", A, "event_year", 1936, "operator", "L002", quals={"event": "first_lift"})
fact("yr_1992", A, "event_year", 1992, "operator", "L002", quals={"event": "la_tania_and_brides_join"})
fact("open_linked", A, "season_opens", "2026-12-05", "operator", "L040", "linked", season=S)
fact("close_linked", A, "season_closes", "2027-04-18", "operator", "L040", "linked", season=S)
fact("open_sr", A, "season_opens", "2026-11-21", "measured", "L010", "earliest_sector", season=S)
fact("close_sr", A, "season_closes", "2027-05-02", "measured", "L010", "earliest_sector", season=S)
fact("open_vt", "resort:val-thorens", "season_opens", "2026-11-21", "operator", "L046", season=S)
fact("close_vt", "resort:val-thorens", "season_closes", "2027-05-02", "operator", "L046", season=S)
fact("open_or", "resort:orelle", "season_opens", "2026-11-21", "operator", "L046", season=S)
fact("close_or", "resort:orelle", "season_closes", "2027-05-02", "operator", "L046", season=S)
fact("brides612", "village:brides-les-bains", "lift_base_min_m", 612, "measured", "L010", note="Olympe gondola bottom station")
P3 = "pass:les-3-vallees"
fact("p6", P3, "pass_price_eur", 421, "operator", "L040", quals={"age": "adult", "days": 6, "period": "high"}, season=S)
fact("p6red", P3, "pass_price_eur", 378.50, "operator", "L042", quals={"age": "adult", "days": 6, "period": "reduced"}, season=S)
fact("p1", P3, "pass_price_eur", 84.20, "operator", "L040", quals={"age": "adult", "days": 1, "period": "high"}, season=S)
fact("p6child", P3, "pass_price_eur", 345, "operator", "L040", quals={"age": "child", "days": 6, "period": "high"}, season=S)
fact("pflex", P3, "pass_price_eur", 345, "operator", "L040", quals={"age": "family_flex", "days": 6, "period": "high"}, season=S)
fact("pvet", P3, "pass_price_eur", 105, "operator", "L040", quals={"age": "veteran", "days": 6, "period": "high", "channel": "ticket_office"}, season=S)
fact("psat", P3, "pass_price_eur", 67.30, "operator", "L041", quals={"age": "adult", "days": 1, "period": "saturday", "channel": "online"}, season=S)
fact("pped", P3, "pass_price_eur", 31.40, "operator", "L045", quals={"product": "pedestrian"}, season=S, note="Lowest pedestrian pass price")
fact("hs_s", P3, "high_season_starts", "2026-12-19", "operator", "L040", season=S)
fact("hs_e", P3, "high_season_ends", "2027-04-09", "operator", "L040", season=S)
fact("red1_s", P3, "reduced_period_starts", "2026-12-05", "operator", "L042", quals={"part": 1}, season=S)
fact("red1_e", P3, "reduced_period_ends", "2026-12-18", "operator", "L042", quals={"part": 1}, season=S)
fact("red2_s", P3, "reduced_period_starts", "2027-04-10", "operator", "L042", quals={"part": 2}, season=S)
fact("red2_e", P3, "reduced_period_ends", "2027-04-18", "operator", "L042", quals={"part": 2}, season=S)
AM = "Alti-Mag compilation, used where the same source is needed across areas"
fact("am_p1", P3, "pass_price_eur", 84.2, "operator", "L044", quals={"age": "adult", "days": 1, "period": "high"}, season=S, note=AM)
fact("am_p6", P3, "pass_price_eur", 421, "operator", "L044", quals={"age": "adult", "days": 6, "period": "high"}, season=S, note=AM)
fact("mv1", "pass:meribel-valley", "pass_price_eur", 69.20, "operator", "L043", quals={"age": "adult", "days": 1, "period": "high"}, season=S)
fact("mv6", "pass:meribel-valley", "pass_price_eur", 356, "operator", "L043", quals={"age": "adult", "days": 6, "period": "high"}, season=S)
fact("lm1", "pass:les-menuires-saint-martin", "pass_price_eur", 70, "operator", "L042", quals={"age": "adult", "days": 1, "period": "high"}, season=S)
fact("lm6", "pass:les-menuires-saint-martin", "pass_price_eur", 350, "operator", "L042", quals={"age": "adult", "days": 6, "period": "high"}, season=S)
fact("lm6red", "pass:les-menuires-saint-martin", "pass_price_eur", 315, "operator", "L042", quals={"age": "adult", "days": 6, "period": "reduced"}, season=S)
fact("vt1", "pass:val-thorens-orelle", "pass_price_eur", 73.5, "operator", "L044", quals={"age": "adult", "days": 1, "period": "high"}, season=S)
fact("vt6", "pass:val-thorens-orelle", "pass_price_eur", 367.50, "operator", "L044", quals={"age": "adult", "days": 6, "period": "high"}, season=S)
for a, d1, d6 in [("paradiski", 78, 412), ("tignes-val-disere", 78, 468), ("les-sybelles", 60.5, 307.2)]:
    k = a.split("-")[0][:3] if a != "tignes-val-disere" else "tvi"
    fact(k + "_p1", "pass:" + a, "pass_price_eur", d1, "operator", "L044", quals={"age": "adult", "days": 1, "period": "high"}, season=S)
    fact(k + "_p6", "pass:" + a, "pass_price_eur", d6, "operator", "L044", quals={"age": "adult", "days": 6, "period": "high"}, season=S)
CMP = {"par": ("area:paradiski", "L070", 425, 126, 1200, 3226, (57, 30, 12), (157, 160)),
       "tvi": ("area:tignes-val-disere", "L071", 300, 80, 1550, 3456, (55, 25, 20), (181, 183)),
       "les": ("area:les-sybelles", "L072", 275, 61, 1100, 2620, (21, 71, 8), (178, 189))}
for k, (pid, L, km, lifts, lo, hi, gs, road) in CMP.items():
    note = "La Plagne and Les Arcs Peisey listings added together" if k == "par" else None
    fact(k + "_piste", pid, "piste_km", km, "measured", L, "total", note=note)
    fact(k + "_lifts", pid, "lifts_count", lifts, "measured", L, "all_lifts", note=note)
    fact(k + "_low", pid, "area_low_m", lo, "measured", L, "lowest_skiing")
    fact(k + "_high", pid, "area_high_m", hi, "measured", L, "highest_skiing")
    for g, v in zip(["easy", "intermediate", "difficult"], gs):
        fact(f"{k}_gs_{g}", pid, "grade_share_pct", v, "measured", L, "listing_length", {"grade": g}, note=note)
    fact(k + "_gva_min", pid, "road_km", road[0], "modelled", "L073", quals={"from": "poi:gva", "bound": "min"}, ds=DS_OSRM)
    fact(k + "_gva_max", pid, "road_km", road[1], "modelled", "L073", quals={"from": "poi:gva", "bound": "max"}, ds=DS_OSRM)
for e, (a, b) in {1600: (279, 325), 2100: (401, 429), 2600: (420, 453.5)}.items():
    fact(f"snow{e}", CELL, "snowfall_median_cm", a, "reanalysis", "L050", quals={"elevation_m": e, "period": "1991-2020"}, ds=DS_SNOW)
    fact(f"snow{e}_old", CELL, "snowfall_median_cm", b, "reanalysis", "L050", quals={"elevation_m": e, "period": "1961-1990"}, ds=DS_SNOW)
for k, cell, v in [("par", "cell:era5.45.5.6.75", 290), ("tvi", "cell:era5.45.5.7.0", 263), ("les", "cell:era5.45.25.6.25", 426)]:
    fact(k + "_snow1600", cell, "snowfall_median_cm", v, "reanalysis", "L052", quals={"elevation_m": 1600, "period": "1991-2020"}, ds=DS_CMP)
for ap, lo, hi in [("gva", 130, 160), ("lys", 163, 199), ("cmf", 85, 121)]:
    fact(ap + "_min", A, "road_km", lo, "modelled", "L060", quals={"from": "poi:" + ap, "bound": "min"}, ds=DS_OSRM)
    fact(ap + "_max", A, "road_km", hi, "modelled", "L060", quals={"from": "poi:" + ap, "bound": "max"}, ds=DS_OSRM)
fact("orelle_gva", "village:orelle", "road_km", 186, "modelled", "L060", quals={"from": "poi:gva"}, ds=DS_OSRM)
fact("bus", "poi:moutiers-station", "bus_fare_eur", 12, "operator", "L062", note="Adult, Moûtiers to the resorts, about")
fact("bus_disc", "poi:moutiers-station", "bus_advance_discount_pct", 10, "operator", "L062", note="Booked more than two days ahead")
fact("cosmojet", "poi:cosmojet", "run_length_km", 6, "operator", "L081")
fact("caphorn", "poi:le-cap-horn", "opened_year", 1954, "operator", "L086")

# sector and resort figures from the network model
for s in PAGE["sectors"]:
    fact(f"sec_lo.{s['id']}", SEC(s["id"]), "lift_base_min_m", s["lo"], "modelled", "L022", ds=DS_NET)
    fact(f"sec_hi.{s['id']}", SEC(s["id"]), "lift_top_max_m", s["hi"], "modelled", "L022", ds=DS_NET)
for r in PAGE["areas"]["rows"]:
    rs = "resort:" + RESORTS[r["name"]]
    fact(f"res_lo.{rs}", rs, "lift_base_min_m", r["lo"], "modelled", "L022", ds=DS_NET)
    fact(f"res_hi.{rs}", rs, "lift_top_max_m", r["hi"], "modelled", "L022", ds=DS_NET)
    if r["easy"] is not None:
        fact(f"res_easy.{rs}", rs, "grade_share_pct", r["easy"], "modelled", "L023", "mapped_length", {"grade": "easy"}, ds=DS_NET)
    fact(f"res_drag.{rs}", rs, "drag_lift_share_pct", r["drag"], "modelled", "L023", ds=DS_NET)
BASE_TO = [SEC("c1850"), SEC("meribel"), SEC("val-thorens"), "lift_top_above_2800"]
for b in PAGE["access"]["bases"]:
    vs = VILLAGES[b["base"]][0]
    for to, v in zip(BASE_TO, b["v"]):
        fact(f"vb.{vs}.{to.split('.')[-1]}", "village:" + vs, "lift_rides_from_village", v, "modelled", "L020", quals={"to": to}, ds=DS_NET)
fact("vb.courchevel-moriond.orelle", "village:courchevel-moriond", "lift_rides_from_village", 8, "modelled", "L020",
     quals={"to": SEC("orelle")}, ds=DS_NET)

for i, n in enumerate(order, 1):
    facts[n]["id"] = f"F{i:06d}"
ID = {n: facts[n]["id"] for n in order}
BYID = {facts[n]["id"]: facts[n] for n in order}

# ---------------------------------------------------------------- figures in the words
# (field regex, text on the live page, template with tokens by fact name)
R = [
    (r"hero\.lead", "3,230 m", "{{f:high_op}}"), (r"hero\.lead", "600 km", "{{f:piste_op}}"), (r"hero\.lead", "1,300 m", "{{f:low_op}}"),
    (r"stats\.0\.v", "600 km", "{{f:piste_op}}"), (r"stats\.1\.v", "3 valleys", "{{f:valleys}} valleys"),
    (r"stats\.2\.v", "1,300 to 3,230 m", "{{f:low_op|n}} to {{f:high_op}}"), (r"stats\.3\.v", "€421", "{{f:p6}}"),
    (r"stats\.3\.t", "€378.50", "{{f:p6red}}"),
    (r"network\.figs\.0\.v", "4 lift rides", "{{f:vb.courchevel-1850.val-thorens}} lift rides"),
    (r"network\.figs\.0\.t", "and four back", "and {{f:vb.val-thorens.c1850|w}} back"),
    (r"network\.figs\.2\.v", "8 lift rides", "{{f:vb.courchevel-moriond.orelle}} lift rides"),
    (r"network\.figs\.4\.v", "1936", "{{f:yr_first}}"), (r"network\.figs\.5\.v", "1992", "{{f:yr_1992}}"),
    (r"network\.paras\.0", "in four lift rides and comes back in four",
     "in {{f:vb.courchevel-1850.val-thorens|w}} lift rides and comes back in {{f:vb.val-thorens.c1850|w}}"),
    (r"routes\.after", "Orelle takes seven lift rides going south and five coming back",
     "Orelle takes {{m:all.moriond.orelle|w}} lift rides going south and {{m:all.orelle.moriond|w}} coming back"),
    (r"terrain\.paras\.0", "337 runs: 50 green, 137 blue, 113 red and 37 black",
     "{{f:runs_total}} runs: {{f:runs_green}} green, {{f:runs_blue}} blue, {{f:runs_red}} red and {{f:runs_black}} black"),
    (r"terrain\.paras\.0", "56% of the piste as easy, 34% as intermediate and 10% as difficult",
     "{{f:gs_easy}} of the piste as easy, {{f:gs_intermediate}} as intermediate and {{f:gs_difficult}} as difficult"),
    (r"terrain\.paras\.0", "50 km", "{{f:routes_km}}"),
    (r"terrain\.paras\.1", "Val Thorens takes five rides on green and blue against three when reds are allowed",
     "Val Thorens takes {{m:easy.c1850.val-thorens|w}} rides on green and blue against {{m:red.c1850.val-thorens|w}} when reds are allowed"),
    (r"terrain\.paras\.1", "Le Praz takes three against two", "Le Praz takes {{m:easy.menuires.le-praz|w}} against {{m:red.menuires.le-praz|w}}"),
    (r"terrain\.paras\.3", "the 37 black runs", "the {{f:runs_black}} black runs"),
    (r"snow\.paras\.0", "85%", "{{f:above1800}}"),
    (r"snow\.paras\.1", "279 cm", "{{f:snow1600}}"), (r"snow\.paras\.1", "401 cm", "{{f:snow2100}}"), (r"snow\.paras\.1", "420 cm", "{{f:snow2600}}"),
    (r"snow\.paras\.2", "from 325 cm", "from {{f:snow1600_old}}"), (r"snow\.paras\.2", "to 279 cm", "to {{f:snow1600}}"),
    (r"snow\.paras\.2", "from 454 cm to 420 cm", "from {{f:snow2600_old}} to {{f:snow2600}}"),
    (r"snow\.paras\.3", "from 21 November to 2 May this season, against 5 December to 18 April",
     "from {{f:open_vt|dm}} to {{f:close_vt|dm}} this season, against {{f:open_linked|dm}} to {{f:close_linked|dm}}"),
    (r"snow\.chartDesc", "279 cm", "{{f:snow1600}}"), (r"snow\.chartDesc", "401 cm", "{{f:snow2100}}"), (r"snow\.chartDesc", "420 cm", "{{f:snow2600}}"),
    (r"snow\.conditions\.status", "21 November 2026", "{{f:open_vt}}"), (r"snow\.conditions\.status", "on 5 December", "on {{f:open_linked|dm}}"),
    (r"pass\.paras\.0", "€421", "{{f:p6}}"), (r"pass\.paras\.0", "between €53.50 and €71", "between {{diff:p6,vt6}} and {{diff:p6,lm6}}"),
    (r"pass\.paras\.0", "€356", "{{f:mv6}}"), (r"pass\.paras\.0", "€350", "{{f:lm6}}"), (r"pass\.paras\.0", "€367.50", "{{f:vt6}}"),
    (r"pass\.paras\.0", "€84.20", "{{f:p1}}"),
    (r"pass\.table\.rows\.0\.1", "€356", "{{f:mv6}}"), (r"pass\.table\.rows\.0\.2", "€421", "{{f:p6}}"), (r"pass\.table\.rows\.0\.3", "€65", "{{diff:p6,mv6}}"),
    (r"pass\.table\.rows\.1\.1", "€350", "{{f:lm6}}"), (r"pass\.table\.rows\.1\.2", "€421", "{{f:p6}}"), (r"pass\.table\.rows\.1\.3", "€71", "{{diff:p6,lm6}}"),
    (r"pass\.table\.rows\.2\.1", "€367.50", "{{f:vt6}}"), (r"pass\.table\.rows\.2\.2", "€421", "{{f:p6}}"), (r"pass\.table\.rows\.2\.3", "€53.50", "{{diff:p6,vt6}}"),
    (r"pass\.table\.rows\.3\.1", "€70", "{{f:lm1}}"), (r"pass\.table\.rows\.3\.2", "€84.20", "{{f:p1}}"), (r"pass\.table\.rows\.3\.3", "€14.20", "{{diff:p1,lm1}}"),
    (r"pass\.scenarios\.0\.what", "€65", "{{diff:p6,mv6}}"), (r"pass\.scenarios\.1\.what", "€71", "{{diff:p6,lm6}}"),
    (r"pass\.scenarios\.2\.what", "€53.50", "{{diff:p6,vt6}}"), (r"pass\.scenarios\.3\.what", "€345", "{{f:pflex}}"),
    (r"pass\.scenarios\.4\.what", "€378.50", "{{f:p6red}}"), (r"pass\.scenarios\.4\.what", "€315", "{{f:lm6red}}"),
    (r"pass\.scenarios\.5\.what", "€67.30", "{{f:psat}}"),
    (r"pass\.after", "€105", "{{f:pvet}}"), (r"pass\.after", "19 December to 9 April", "{{f:hs_s|dm}} to {{f:hs_e|dm}}"),
    (r"access\.paras\.0", "130 to 160 km", "{{f:gva_min|n}} to {{f:gva_max}}"),
    (r"access\.paras\.1", "€12", "{{f:bus}}"), (r"access\.paras\.1", "10% off", "{{f:bus_disc}} off"),
    (r"access\.paras\.2", "186 km", "{{f:orelle_gva}}"),
    (r"access\.basesParas\.0", "four rides from the village lifts", "{{f:vb.les-menuires.c1850|w}} rides from the village lifts"),
    (r"chapters\.0\.paras\.0", "four snowparks and 35 fun zones", "{{f:parks|w}} snowparks and {{f:funzones}} fun zones"),
    (r"chapters\.0\.paras\.1", "35 of the 132 main lifts", "{{f:drags}} of the {{f:main_lifts}} main lifts"),
    (r"chapters\.0\.paras\.2", "50 km", "{{f:routes_km}}"),
    (r"chapters\.1\.paras\.2", "6 km", "{{f:cosmojet}}"),
    (r"chapters\.2\.paras\.0", "15 Michelin stars across 10 restaurants", "{{f:stars}} Michelin stars across {{f:rest_mich}} restaurants"),
    (r"chapters\.2\.paras\.1", "66 mountain restaurants among the 355", "{{f:rest_mtn}} mountain restaurants among the {{f:rest_all}}"),
    (r"chapters\.2\.paras\.1", "since 1954", "since {{f:caphorn}}"),
    (r"fit\.rows\.0\.limit", "eight lift rides", "{{f:vb.courchevel-moriond.orelle|w}} lift rides"),
    (r"fit\.rows\.3\.limit", "€53.50 to €71", "{{diff:p6,vt6}} to {{diff:p6,lm6}}"),
    (r"fit\.rows\.5\.why", "Four snowparks and 35 fun zones", "{{f:parks|W}} snowparks and {{f:funzones}} fun zones"),
    (r"fit\.rows\.6\.why", "37 black runs, 50 km", "{{f:runs_black}} black runs, {{f:routes_km}}"),
    (r"fit\.rows\.7\.why", "85%", "{{f:above1800}}"),
    (r"fit\.rows\.10\.why", "15 Michelin stars across 10 restaurants and 66 mountain restaurants",
     "{{f:stars}} Michelin stars across {{f:rest_mich}} restaurants and {{f:rest_mtn}} mountain restaurants"),
    (r"fit\.rows\.12\.limit", "€31.40", "{{f:pped}}"),
    (r"compare\.paras\.0", "600 km of piste against 425 km", "{{f:piste_sr}} of piste against {{f:par_piste}}"),
    (r"compare\.paras\.1", "3,456 m", "{{f:tvi_high}}"), (r"compare\.paras\.1", "2,620 m", "{{f:les_high}}"),
    (r"compare\.note", "Orelle at 186 km", "Orelle at {{f:orelle_gva}}"),
    (r"method\.conflicts", "169 lifts and skiresort.com 159", "{{f:lifts_op}} lifts and skiresort.com {{f:lifts_sr}}"),
    (r"method\.conflicts", "1,300 m and skiresort.com 1,100 m", "{{f:low_op}} and skiresort.com {{f:low_sr}}"),
    (r"method\.conflicts", "612 m", "{{f:brides612}}"), (r"method\.conflicts", "seven resorts", "{{f:resorts7|w}} resorts"),
    (r"method\.conflicts", "3,211 m against the operator's 3,230 m", "{{f:sec_hi.orelle}} against the operator's {{f:high_op}}"),
    (r"method\.conflicts", "21 November to 2 May", "{{f:open_sr|dm}} to {{f:close_sr|dm}}"),
    (r"method\.conflicts", "5 December to 18 April", "{{f:open_linked|dm}} to {{f:close_linked|dm}}"),
    (r"method\.sources", "167 lifts and 1,126 piste sections", "{{f:lifts_mapped}} lifts and {{f:sections}} piste sections"),
]
# list item blurbs
RL = [("list:les-3-vallees.snowboard", "Ski routes", "50 km", "{{f:routes_km}}"),
      ("list:les-3-vallees.families", "Cosmojet", "6 km", "{{f:cosmojet}}"),
      ("list:les-3-vallees.food", "Le Cap Horn", "1954", "{{f:caphorn}}")]
# comparison table: whole cells from facts
CMPROWS = [
    ["{{f:piste_sr}}", "{{f:par_piste}}", "{{f:tvi_piste}}", "{{f:les_piste}}"],
    ["{{f:lifts_sr}}", "{{f:par_lifts}}", "{{f:tvi_lifts}}", "{{f:les_lifts}}"],
    ["{{f:low_sr|n}} to {{f:high_sr}}", "{{f:par_low|n}} to {{f:par_high}}", "{{f:tvi_low|n}} to {{f:tvi_high}}", "{{f:les_low|n}} to {{f:les_high}}"],
    ["{{f:gs_easy|n}}, {{f:gs_intermediate|n}}, {{f:gs_difficult}}"] + [f"{{{{f:{k}_gs_easy|n}}}}, {{{{f:{k}_gs_intermediate|n}}}}, {{{{f:{k}_gs_difficult}}}}" for k in ["par", "tvi", "les"]],
    ["{{f:am_p1}}", "{{f:par_p1}}", "{{f:tvi_p1}}", "{{f:les_p1}}"],
    ["{{f:am_p6}}", "{{f:par_p6}}", "{{f:tvi_p6}}", "{{f:les_p6}}"],
    ["{{f:snow1600}}", "{{f:par_snow1600}}", "{{f:tvi_snow1600}}", "{{f:les_snow1600}}"],
    ["{{f:gva_min|n}} to {{f:gva_max}}", "{{f:par_gva_min|n}} to {{f:par_gva_max}}", "{{f:tvi_gva_min|n}} to {{f:tvi_gva_max}}", "{{f:les_gva_min|n}} to {{f:les_gva_max}}"],
]

NAMED = re.compile(r"\{\{(f|diff):([^}|]+)")


def to_ids(t):
    def rep(mt):
        kind, ref = mt.group(1), mt.group(2)
        return "{{" + kind + ":" + ",".join(ID[x] for x in ref.split(",")) if kind == "diff" else "{{f:" + ID[ref]
    return NAMED.sub(rep, t)


def check(template, literal, where):
    got = resolve_text(to_ids(template), BYID, MATRICES)
    assert got == literal, f"{where}: database gives {got!r}, page has {literal!r}"


# ---------------------------------------------------------------- layout and blocks
STRUCT = {"_about", "slug", "permalink", "nav", "href", "u", "photo", "id", "cc", "link", "kind", "place", "lat", "lon", "ev"}
SECTION = {"sectors": "network", "links": "network", "mapNotes": "network", "title": "meta", "description": "meta", "crumbs": "meta",
           "routes": "routes", "areas": "areas"}
SLOT = {"h2": "heading", "h3": "heading", "basesH3": "heading", "catchesH3": "heading", "conflictsH3": "heading", "kicker": "kicker",
        "listTitle": "heading", "mapTitle": "heading", "heightsTitle": "heading", "chartTitle": "heading", "matrixTitle": "heading",
        "coverageTitle": "heading", "scenariosTitle": "heading", "paras": "para", "basesParas": "para", "lead": "lead",
        "caption": "caption", "heightsCaption": "caption", "chartCaption": "caption", "basesCaption": "caption", "mapHelp": "caption",
        "note": "note", "accessNote": "note", "basesNote": "note", "matrixNote": "note", "tableNote": "note", "after": "note"}
blocks, used = [], set()
ord_ctr = {}
num_fact = {}  # field -> fact name for numeric leaves
for i, s in enumerate(PAGE["sectors"]):
    num_fact[f"sectors.{i}.lo"] = f"sec_lo.{s['id']}"; num_fact[f"sectors.{i}.hi"] = f"sec_hi.{s['id']}"
for i, r in enumerate(PAGE["areas"]["rows"]):
    rs = "resort:" + RESORTS[r["name"]]
    for k, n in [("lo", "res_lo"), ("hi", "res_hi"), ("easy", "res_easy"), ("drag", "res_drag")]:
        if r[k] is not None:
            num_fact[f"areas.rows.{i}.{k}"] = f"{n}.{rs}"
for i, b in enumerate(PAGE["access"]["bases"]):
    vs = VILLAGES[b["base"]][0]
    for j, to in enumerate(BASE_TO):
        num_fact[f"access.bases.{i}.v.{j}"] = f"vb.{vs}.{to.split('.')[-1]}"
PNAME = {p["name"]: p["id"] for p in places if p["type"] in ("resort",)}
SECT_SLUG = {"chapters": None}


def section_of(path):
    top = path[0]
    if top == "chapters":
        return PAGE["chapters"][path[1]]["id"]
    return SECTION.get(top, top)


def add_block(field, section, slotkey, text):
    template = text
    for rx, lit, tpl in R:
        if re.fullmatch(rx, field) and lit in template:
            check(tpl, lit, field)
            template = template.replace(lit, tpl)
            used.add((rx, lit))
    if field.startswith("compare.rows.") and field.count(".") == 4:
        _, _, ri, _, ci = field.split(".")
        ri, ci = int(ri), int(ci)
        if ri < len(CMPROWS):
            check(CMPROWS[ri][ci], text, field)
            template = CMPROWS[ri][ci]
    slot = SLOT.get(slotkey, "line")
    key = (section, slot)
    ord_ctr[key] = ord_ctr.get(key, -1) + 1
    body = to_ids(template)
    assert resolve_text(body, BYID, MATRICES) == text, field
    blocks.append(dict(field=field, section=section, slot=slot, ord=ord_ctr[key], body=body, fact_refs=sorted(set(token_refs(body)))))
    return {"$b": field}


def build(node, path):
    field = ".".join(str(p) for p in path)
    last = path[-1] if path else None
    lastkey = next((p for p in reversed(path) if isinstance(p, str)), None)
    if path == ["name"]:
        return {"$p": A}
    if path == ["links"]:
        return {"$links": DS_NET}
    if path and path[0] == "photos" and len(path) == 2:
        return {"$media": media_id[last]}
    if len(path) == 3 and path[0] == "chapters" and last == "items":
        return {"$list": "list:les-3-vallees." + PAGE["chapters"][path[1]]["id"]}
    if path[:1] == ["sectors"] and last == "name":
        return {"$p": SEC(PAGE["sectors"][path[1]]["id"])}
    if path[:1] == ["sectors"] and last == "base":
        return {"$p": "resort:" + RESORTS[node]}
    if path[:2] == ["areas", "rows"] and last == "name":
        return {"$p": "resort:" + RESORTS[node]}
    if path[:2] == ["areas", "rows"] and last == "cc":
        return {"$p": "country:fr"}
    if path[:2] == ["compare", "cols"] and last == "name":
        return {"$p": {"Les 3 Vallées": A, "Paradiski": "area:paradiski", "Tignes Val d'Isère": "area:tignes-val-disere",
                       "Les Sybelles": "area:les-sybelles"}[node]}
    if path[:2] == ["routes", "rows"] and last in ("out", "back"):
        r = PAGE["routes"]["rows"][path[2]]
        ids = {v[0]: v[3] for v in VILLAGES.values()}
        by_label = {"Courchevel 1850": "c1850", "Méribel": "meribel", "La Tania": "la-tania", "Saint-Martin": "saint-martin",
                    "Brides-les-Bains": "brides", "Val Thorens": "val-thorens", "Les Menuires": "menuires", "Orelle": "orelle"}
        fr, to = by_label[r["from"]], by_label[r["to"]]
        if last == "back":
            fr, to = to, fr
        assert MATRICES["all"][fr][to] == node, (field, node)
        return {"$m": ["all", fr, to]}
    if path == ["mapBox"] or lastkey in STRUCT or (path and path[0] == "breaks"):
        return node
    if isinstance(node, dict):
        return {k: build(v, path + [k]) for k, v in node.items()}
    if isinstance(node, list):
        return [build(v, path + [i]) for i, v in enumerate(node)]
    if isinstance(node, bool) or node is None:
        return node
    if isinstance(node, (int, float)):
        n = num_fact.get(field)
        assert n, f"untracked number at {field}: {node}"
        assert BYID[ID[n]]["value_num"] == node, field
        return {"$f": ID[n]}
    return add_block(field, section_of(path), lastkey, node)


media, media_links, media_id = [], [], {}
for key, (file, author, lic, alt) in PAGE["photos"].items():
    mid = "m:" + slug(os.path.splitext(file)[0])[:56]
    media_id[key] = mid
    media.append(dict(id=mid, file_name=file, author=author, licence=lic, alt=alt,
                      remote_url="https://commons.wikimedia.org/wiki/Special:FilePath/" + quote(file.replace(" ", "_")),
                      page_url="https://commons.wikimedia.org/wiki/File:" + quote(file.replace(" ", "_"))))
    role = "hero" if key == "hero" else ("break" if any(v.get("photo") == key for v in PAGE["breaks"].values()) else "chapter")
    media_links.append((mid, A, role, key))

layout = build(PAGE, [])

# list blurbs
lists_sql_items = []
for lid, items in list_items.items():
    for o, (pid, attrs, text) in enumerate(items):
        tpl = text
        for l2, nm, lit, t in RL:
            if l2 == lid and (attrs.get("name") or next(p["name"] for p in places if p["id"] == pid)) == nm:
                check(t, lit, lid + " " + nm)
                tpl = tpl.replace(lit, t)
        body = to_ids(tpl)
        assert resolve_text(body, BYID, MATRICES) == text
        lists_sql_items.append((lid, pid, o, body, sorted(set(token_refs(body))), attrs))

unused = [x for x in R if (x[0], x[1]) not in used]
assert not unused, f"replacements that matched nothing: {unused}"

# ---------------------------------------------------------------- SQL
sql = []
add = sql.append
add("-- Snow Catchers pilot seed: Les 3 Vallées. Generated by db/pilot_l3v/build_seed.py; do not edit by hand.")
add("insert into core.place (id,type,subtype,name,slug,status,lat,lon,summary) values\n" + ",\n".join(
    f"({q(p['id'])},{q(p['type'])},{q(p.get('subtype'))},{q(p['name'])},{q(p['slug'])},'live',{q(p.get('lat'))},{q(p.get('lon'))},{q(p.get('summary'))})"
    for p in places) + ";")
add("insert into core.place_alias (place_id,alias) values\n" + ",\n".join(f"({q(a)},{q(b)})" for a, b in aliases) + ";")
add("insert into core.place_link (from_id,to_id,relation,is_primary,ord,conditions) values\n" + ",\n".join(
    f"({q(a)},{q(b)},{q(r)},{q(p)},{q(o)},{q(c)})" for a, b, r, p, o, c in links) + ";")
add("insert into core.source (id,title,publisher,url,source_type) values\n" + ",\n".join(
    f"({q(s['id'])},{q(s['title'])},{q(s['publisher'])},{q(s['url'])},{q(s['source_type'])})" for s in sources.values()) + ";")
add("insert into core.property (key,label,value_type,unit,applies_to,qualifier_keys,max_age_days,allowed_methods,definition,requires_scope) values\n" + ",\n".join(
    f"({q(p['key'])},{q(p['label'])},{q(p['value_type'])},{q(p['unit'])},{qarr(p['applies_to'])},{qarr(p['qualifier_keys'])},"
    f"{q(p['max_age_days'])},{qarr(p['allowed_methods'])},{q(p['definition'])},{q(p['requires_scope'])})" for p in props) + ";")
add("insert into core.metric_scope (property,key,definition) values\n" + ",\n".join(f"({q(a)},{q(b)},{q(c)})" for a, b, c in scopes) + ";")
add("insert into core.season (id,starts,ends) values ('2026/27','2026-11-01','2027-05-31');")
DATASETS = [
    (DS_NET, "network", "Les 3 Vallées lift and piste network", A,
     {"osm_snapshot": "2026-10-20T15:39:51Z", "lifts": 167, "piste_sections": 1126, "elevation": "Copernicus GLO-90 via Open-Meteo",
      "matrix_origin": "first lift base in each sector", "base_table_origin": "village lifts within 200 m of the lowest lift",
      "hand_added": ["walk from the Olympe gondola top to the Chaudanne lifts, Méribel", "Orelle lifts assigned to the Orelle sector"]},
     None, "Built in a browser session; the query and graph code is not yet committed, so raw nodes and edges are not loaded", NET),
    (DS_SNOW, "snow", "ERA5 seasonal snowfall, Les 3 Vallées cell", A,
     {"cell": CELL, "lat": 45.25, "lon": 6.5, "elevations_m": [1600, 2100, 2600], "months": "November to April", "model": "era5",
      "api": "Open-Meteo historical weather", "seasons": "1950/51 to 2025/26"}, None, "Fetched in a browser session", None),
    (DS_CMP, "snow", "ERA5 seasonal snowfall, Savoie comparison cells", None,
     {"cells": ["cell:era5.45.5.6.75", "cell:era5.45.5.7.0", "cell:era5.45.25.6.25"], "elevation_m": 1600, "model": "era5",
      "period": "1991-2020"}, None, "Medians only; season rows not kept", None),
    (DS_OSRM, "routing", "Road distances from airports, OSRM", A, {"router": "OSRM demo server, OpenStreetMap", "profile": "car"},
     None, "Fastest route without traffic or snow", None),
]
add("insert into model.dataset (id,kind,title,place_id,inputs,script_repo,script_path,run_at,status,note,outputs) values\n" + ",\n".join(
    f"({q(i)},{q(k)},{q(t)},{q(p)},{q(inp)},'nicksc1cc/snowcatcher',{q(sp)},'2026-10-20','accepted',{q(n)},{q(o) if o else 'null'})"
    for i, k, t, p, inp, sp, n, o in DATASETS) + ";")
add("insert into core.fact (id,place_id,property,scope,value_num,value_text,unit,qualifiers,season,method,source_id,dataset_id,retrieved_at,status,legacy_ref,note,created_by,accepted_by) values\n" + ",\n".join(
    f"({q(f['id'])},{q(f['place_id'])},{q(f['property'])},{q(f['scope'])},{q(f['value_num'])},{q(f['value_text'])},{q(f['unit'])},{q(f['qualifiers'])},"
    f"{q(f['season'])},{q(f['method'])},{q(f['source_id'])},{q(f['dataset_id'])},{q(RETRIEVED)},'accepted',{q(f['legacy_ref'])},{q(f['note'])},'pilot import',{q(ACCEPTED_BY)})"
    for f in (facts[n] for n in order)) + ";")
add(f"select setval('core.fact_seq', {len(order)});")
rows = []
for r in SNOW:
    y = int(r["season_start"])
    for e in (1600, 2100, 2600):
        rows.append(f"({q(DS_SNOW)},{q(CELL)},{e},'{y}/{str(y + 1)[2:]}',{r[f'snowfall_cm_{e}']})")
add("insert into model.weather_obs (dataset_id,cell_id,elevation_m,season,snowfall_cm) values\n" + ",\n".join(rows) + ";")
GVA = [("village:brides-les-bains", 130), ("village:meribel", 141), ("village:la-tania", 142), ("village:saint-martin-de-belleville", 143),
       ("village:courchevel-1850", 148), ("village:les-menuires", 153), ("village:val-thorens", 160), ("village:orelle", 186), ("poi:moutiers-station", 124)]
add("insert into model.route (dataset_id,from_id,to_id,mode,distance_km) values\n" + ",\n".join(
    f"({q(DS_OSRM)},'poi:gva',{q(t)},'road',{d})" for t, d in GVA) + ";")
add("insert into model.sector_link (dataset_id,from_sector,to_sector,by,one_way,critical_edges,conditions,note) values\n" + ",\n".join(
    f"({q(DS_NET)},{q(SEC(a))},{q(SEC(b))},{q('lift_down' if k == 'ride' else 'ski')},false,{qarr([lab] if crit else [])},"
    f"{q({'ord': i, 'critical': crit})},{q(lab)})" for i, (a, b, k, crit, lab) in enumerate(PAGE["links"])) + ";")
SECTIONS = sorted({b["section"] for b in blocks})
add("insert into content.section (key,label,levels,ord) values\n" + ",\n".join(
    f"({q(s)},{q(s.capitalize())},array['area']::text[],{i})" for i, s in enumerate(SECTIONS)) + ";")
add("insert into content.content_block (place_id,section,slot,ord,body,fact_refs,status,author,field) values\n" + ",\n".join(
    f"({q(A)},{q(b['section'])},{q(b['slot'])},{b['ord']},{q(b['body'])},{qarr(b['fact_refs'])},'live','pilot import',{q(b['field'])})"
    for b in blocks) + ";")
add("insert into content.place_list (id,place_id,title,kind,status) values\n" + ",\n".join(
    f"({q(lid)},{q(A)},{q(ch['listTitle'])},{q(LIST_KIND[ch['id']])},'live')"
    for lid, ch in zip(list_items, PAGE["chapters"])) + ";")
add("insert into content.place_list_item (list_id,item_place_id,ord,blurb,fact_refs,attrs) values\n" + ",\n".join(
    f"({q(l)},{q(p)},{o},{q(b)},{qarr(fr)},{q(at)})" for l, p, o, b, fr, at in lists_sql_items) + ";")
add("insert into content.media (id,kind,remote_url,page_url,file_name,author,licence,alt,status) values\n" + ",\n".join(
    f"({q(m['id'])},'photo',{q(m['remote_url'])},{q(m['page_url'])},{q(m['file_name'])},{q(m['author'])},{q(m['licence'])},{q(m['alt'])},'live')"
    for m in media) + ";")
add("insert into content.media_link (media_id,place_id,role,slot) values\n" + ",\n".join(
    f"({q(a)},{q(b)},{q(c)},{q(d)})" for a, b, c, d in media_links) + ";")
add("insert into content.page (id,place_id,level,template,canonical_path,title,status,approved_by,approved_at,published_commit,published_at,layout) values\n"
    f"('page:area:les-3-vallees',{q(A)},3,'l3-domain','/france/les-3-vallees/',{q(PAGE['title'])},'published','Nick','2026-10-20','9a85cd8','2026-10-20',{q(layout)}),\n"
    "('page:area:portes-du-soleil','area:portes-du-soleil',3,'l3-domain','/france/portes-du-soleil/','Portes du Soleil','published','Nick','2026-10-20','c6642b2','2026-10-20',null),\n"
    "('page:country:fr','country:fr',1,'country-base','/france/','Skiing in France','published','Nick','2026-10-20','e3bfc26','2026-10-20',null);")
add("insert into content.page_place (page_id,place_id,role) values\n" + ",\n".join(
    f"('page:area:les-3-vallees',{q(p)},{q(r)})" for p, r in
    [("area:paradiski", "compares"), ("area:tignes-val-disere", "compares"), ("area:les-sybelles", "compares"), (CELL, "mentions"),
     ("cell:era5.45.5.6.75", "compares"), ("cell:era5.45.5.7.0", "compares"), ("cell:era5.45.25.6.25", "compares"),
     ("pass:les-3-vallees", "subject"), ("pass:meribel-valley", "compares"), ("pass:les-menuires-saint-martin", "compares"),
     ("pass:val-thorens-orelle", "compares"), ("pass:paradiski", "compares"), ("pass:tignes-val-disere", "compares"),
     ("pass:les-sybelles", "compares"), ("poi:moutiers-station", "mentions"), ("poi:cosmojet", "lists"), ("poi:le-cap-horn", "lists")]
    + [("resort:" + s, "lists") for s in RESORTS.values()] + [("village:" + v[0], "lists") for v in VILLAGES.values()]
    + [(SEC(s["id"]), "lists") for s in PAGE["sectors"]]) + ";")
# the import itself should not leave pages flagged
add("update content.page set needs_review = false, review_reasons = '{}';")

os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "seed.sql"), "w", encoding="utf-8") as fh:
    fh.write("\n\n".join(sql) + "\n")

# ---------------------------------------------------------------- coverage report
FIG = re.compile(r"(?<![\w{|:.])(?:€\s?)?\d[\d,.]*(?:\s?(?:km|m|cm|%))?")
typed = []
for b in blocks:
    plain = re.sub(r"\{\{[^}]+\}\}", "", re.sub(r"<[^>]+>", "", b["body"]))
    for mt in FIG.findall(plain):
        typed.append((b["field"], mt.strip()))
words = re.compile(r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b", re.I)
typed_words = [(b["field"], w) for b in blocks for w in words.findall(re.sub(r"\{\{[^}]+\}\}", "", b["body"]))]
tok = sum(len(TOKS) for TOKS in (re.findall(r"\{\{", b["body"]) for b in blocks))
rep = {"places": len(places), "aliases": len(aliases), "links": len(links), "sources": len(sources), "properties": len(props),
       "scopes": len(scopes), "facts": len(order), "blocks": len(blocks), "tokens_in_blocks": tok, "list_items": len(lists_sql_items),
       "media": len(media), "weather_rows": len(rows), "typed_figures_left": len(typed), "typed_number_words_left": len(typed_words)}
with open(os.path.join(OUT, "coverage.json"), "w", encoding="utf-8") as fh:
    json.dump({"summary": rep, "typed_figures": typed, "typed_number_words": typed_words}, fh, ensure_ascii=False, indent=1)
print(json.dumps(rep, indent=1))
print("SQL bytes:", sum(len(s.encode()) for s in sql))

# ---------------------------------------------------------------- self test: the layout alone rebuilds the page
from snowdb import resolve_layout  # noqa: E402
ctx = dict(blocks={b["field"]: b["body"] for b in blocks}, facts=BYID, matrices=MATRICES,
           places={p["id"]: p for p in places}, media={m["id"]: m for m in media},
           lists={lid: [dict(item_place_id=p, attrs=at, blurb=b) for l, p, o, b, fr, at in lists_sql_items if l == lid] for lid in list_items},
           links={DS_NET: PAGE["links"]})
assert resolve_layout(layout, ctx) == PAGE, "layout does not rebuild the page"
print("self test: layout rebuilds the live page exactly")
