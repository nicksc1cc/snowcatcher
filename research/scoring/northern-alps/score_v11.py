"""Method v1.1: scores that fit the trip rather than reward size, plus list recipes.

Changes from v1:
  - kilometres count only up to what a week at that level needs (25, 100 and 120 km); total size is its own theme
  - level specific skiing measures: drags, run length per lift, vertical, flat sections, steep terrain
  - value from Alti-Mag pass prices; ease from road time and bed to lift distance
  - families, non skiers and village life from OpenStreetMap features (data/measures2.json)
  - lists are recipes (lists.json): weights, filters, minimums and required measures
Inputs: resorts.csv, data/measures_raw.csv, data/measures2.json (optional), data/access.csv, data/altimag_prices.csv
Outputs: out/scores_v11.csv, out/lists_v11.md
"""
import csv, json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(HERE, *a)
LEVELS = ["beginner", "intermediate", "advanced"]
PARKS = json.load(open(P("data", "parks.json"))) if os.path.exists(P("data", "parks.json")) else {}
NOT_AT_BASE = {("megeve", "Les Portes du Mont-Blanc"), ("saint-gervais", "Les Houches – Saint-Gervais")}
NEED_KM = {"beginner": 25, "intermediate": 100, "advanced": 120}


def num(x):
    try:
        return None if x in ("", None) else float(x)
    except ValueError:
        return None


def lin(v, lo, hi):
    """0 to 100 between floor lo and ceiling hi (lo above hi means lower is better)."""
    if v is None:
        return None
    t = (v - lo) / (hi - lo)
    return round(100 * min(1, max(0, t)), 1)


def sq(v, lo, hi):
    s = lin(v, lo, hi)
    return None if s is None else round(100 * math.sqrt(s / 100), 1)


def mean(parts):
    """parts: list of (score, weight); None scores are skipped."""
    p = [(s, w) for s, w in parts if s is not None]
    if not p:
        return None
    return round(sum(s * w for s, w in p) / sum(w for _, w in p), 1)


def load():
    resorts = list(csv.DictReader(open(P("resorts.csv"))))
    m = {r["slug"]: r for r in csv.DictReader(open(P("data", "measures_raw.csv")))}
    m2 = {}
    if os.path.exists(P("data", "measures2.json")):
        m2 = {r["slug"]: r for r in json.load(open(P("data", "measures2.json")))}
    acc = {r["slug"]: r for r in csv.DictReader(open(P("data", "access.csv")))}
    prices = {}
    for r in csv.DictReader(open(P("data", "altimag_prices.csv"))):
        prices.setdefault(r["slug"], []).append(r)
    # local passes for resorts whose only listed pass covers a larger linked domain (data/local_passes.csv)
    if os.path.exists(P("data", "local_passes.csv")):
        for r in csv.DictReader(open(P("data", "local_passes.csv"))):
            prices.setdefault(r["slug"], []).append(r)
    return resorts, m, m2, acc, prices


def load_apres():
    """Reputation, named venues, clubs, slope venues and events from the guides in data/apres_sources.csv."""
    import re, unicodedata
    def key(v):
        v = unicodedata.normalize("NFD", v).encode("ascii", "ignore").decode().lower()
        v = re.sub(r"\b(la|le|les|l|the|bar|club|nightclub)\b", " ", v.replace("'", " "))
        return re.sub(r"[^a-z0-9]+", "", v)
    out = {}
    if not os.path.exists(P("data", "apres_mentions.csv")):
        return out
    for r in csv.DictReader(open(P("data", "apres_mentions.csv"))):
        o = out.setdefault(r["slug"], {"rep": 0.0, "sources": set(), "venues": {}, "clubs": {}, "slope": {}, "events": 0})
        if r["source"] not in ("J", "K"):
            o["sources"].add(r["source"])
            o["rep"] += (11 - int(r["rank"])) / 10 if r["rank"] else 0.5
        for col, dest in (("venues", "venues"), ("clubs", "clubs"), ("slope_venues", "slope")):
            for v in filter(None, (x.strip() for x in r[col].split(";"))):
                o[dest].setdefault(key(v), v)
        for v in filter(None, (x.strip() for x in r["slope_venues"].split(";"))):
            o["venues"].setdefault(key(v), v)
    if os.path.exists(P("data", "apres_verdicts.csv")):
        for r in csv.DictReader(open(P("data", "apres_verdicts.csv"))):
            o = out.setdefault(r["slug"], {"rep": 0.0, "sources": set(), "venues": {}, "clubs": {}, "slope": {}, "events": 0})
            o["rep"] += {"lively": 1.0, "moderate": 0.5, "quiet": 0.0}[r["verdict"]]
            o["verdict"] = r["verdict"]
    for r in csv.DictReader(open(P("data", "apres_events.csv"))):
        out.setdefault(r["slug"], {"rep": 0.0, "sources": set(), "venues": {}, "clubs": {}, "slope": {}, "events": 0})["events"] += 1
    return out


APRES = load_apres()

def load_food():
    """Michelin 2026 points (3 stars 10, 2 stars 6, 1 star 3, Bib Gourmand 1) and Gault&Millau toques by resort."""
    out = {}
    pts = {"3": 10, "2": 6, "1": 3, "bib": 1}
    if os.path.exists(P("data", "michelin_2026.csv")):
        for r in csv.DictReader(open(P("data", "michelin_2026.csv"))):
            o = out.setdefault(r["slug"], {"michelin": 0, "stars": 0, "bib": 0, "gm": 0.0, "toqued": 0})
            o["michelin"] += pts[r["distinction"]]
            if r["distinction"] == "bib":
                o["bib"] += 1
            else:
                o["stars"] += int(r["distinction"])
    if os.path.exists(P("data", "gaultmillau.csv")):
        for r in csv.DictReader(open(P("data", "gaultmillau.csv"))):
            o = out.setdefault(r["slug"], {"michelin": 0, "stars": 0, "bib": 0, "gm": 0.0, "toqued": 0})
            o["gm"] += float(r["toques"]) if r["guide_year"] == "2026" else 0.5
            o["toqued"] += 1
    return out


FOOD = load_food()


def load_offpiste():
    """Off piste reputation from the guides in data/offpiste_sources.csv, plus map checks from SCBulk.offpiste.

    guides: each source naming the resort counts 1; a domain named without a village counts 0.5 for each
    member (data/offpiste_domains.csv). routes: distinct named routes across all guides."""
    import re, unicodedata
    key = lambda v: re.sub(r"[^a-z0-9]+", "", unicodedata.normalize("NFD", v).encode("ascii", "ignore").decode().lower())
    out = {}
    blank = lambda: {"guides": {}, "routes": {}}
    if os.path.exists(P("data", "offpiste_mentions.csv")):
        for r in csv.DictReader(open(P("data", "offpiste_mentions.csv"))):
            o = out.setdefault(r["slug"], blank())
            o["guides"][r["source"]] = 1.0
            for v in filter(None, (x.strip() for x in r["routes"].split(";"))):
                o["routes"].setdefault(key(v), v)
    if os.path.exists(P("data", "offpiste_domains.csv")):
        for r in csv.DictReader(open(P("data", "offpiste_domains.csv"))):
            for slug in r["members"].split(";"):
                o = out.setdefault(slug, blank())
                o["guides"].setdefault(r["source"], 0.5)
    mp = {}
    if os.path.exists(P("data", "offpiste_map.json")):
        mp = {r["slug"]: r for r in json.load(open(P("data", "offpiste_map.json")))}
    return out, mp


OFFPISTE, OFFMAP = load_offpiste()


# value anchors by size band (mapped piste km): (day pass worst, best), (six day pass worst, best) in euros
VALUE_BANDS = {
    "large": ((85, 55), (470, 280)),    # 200 km or more
    "medium": ((75, 45), (400, 220)),   # 60 to 200 km
    "small": ((55, 20), (280, 120)),    # under 60 km
}


def score_resort(r, m, x, a, pr):
    raw, sc = {}, {}
    km = {lv: num(m.get("km_" + lv)) for lv in LEVELS}
    kmall, lifts = num(m.get("km_all")) or 0, num(m.get("lifts")) or 0
    raw.update({"km_" + lv: km[lv] for lv in LEVELS})
    raw["km_all"] = kmall
    raw["km_per_lift"] = round(kmall / lifts, 2) if lifts else None
    # skiing by level
    for lv in LEVELS:
        drag = lin(num(m.get("drag_pct")), 70, 0) if lv != "advanced" else lin(num(m.get("drag_pct")), 90, 20)
        flat = lin(num(x.get("flat_pct_" + lv)), 30, 5) if x else None
        parts = [(lin(km[lv], 0, NEED_KM[lv]), 3), (drag, 2 if lv == "beginner" else 1), (lin(raw["km_per_lift"], 0.5, 3), 1), (flat, 1)]
        if lv != "beginner":
            parts.append((lin(num(m.get("vertical_m")), 300, 1500), 1))
        if lv == "advanced" and x:
            parts.append((lin(num(x.get("steep_km")), 0, 25), 1))
        sc["skiing." + lv] = mean(parts)
        if x:
            raw["flat_pct_" + lv] = x.get("flat_pct_" + lv)
    sc["size"] = mean([(sq(kmall, 0, 400), 2), (sq(lifts, 0, 120), 1)])
    # ease
    gva, lys = num(a.get("gva_min")), num(a.get("lys_min"))
    near = min([t for t in (gva, lys) if t is not None], default=None)
    raw["airport_min"] = near
    raw["gva_min"] = gva
    sc["ease"] = mean([(lin(near, 240, 60), 2), (lin(num(m.get("bed_to_lift_m")), 1500, 100), 1), (lin(num(m.get("ski_in_out_pct")), 0, 60), 1)])
    # value: the cheapest alpine pass listed for the resort
    # passes that do not cover the lifts at the scored base are left out (checked by hand)
    pr = [p for p in pr if (r["slug"], p["domain"]) not in NOT_AT_BASE]
    days = [num(p["day_eur"]) for p in pr if num(p["day_eur"])]
    sixes = [num(p["six_day_eur"]) for p in pr if num(p["six_day_eur"])]
    raw["day_pass_eur"] = min(days) if days else None
    raw["six_day_pass_eur"] = min(sixes) if sixes else None
    # value is scored against resorts of a similar size, so a big domain is compared with big domains
    band = "large" if kmall >= 200 else "medium" if kmall >= 60 else "small"
    (d_hi, d_lo), (s_hi, s_lo) = VALUE_BANDS[band]
    raw["size_band"] = band
    sc["value"] = mean([(lin(raw["day_pass_eur"], d_hi, d_lo), 1), (lin(raw["six_day_pass_eur"], s_hi, s_lo), 1)])
    # après and food
    bars = (num(m.get("bar_village")) or 0) + (num(m.get("bar_mountain")) or 0)
    rest = (num(m.get("restaurant_village")) or 0) + (num(m.get("restaurant_mountain")) or 0)
    raw.update({"bars": bars, "restaurants": rest, "late_bars": num(m.get("late"))})
    ap = APRES.get(r["slug"])
    raw["apres_sources"] = len(ap["sources"]) if ap else 0
    raw["apres_reputation"] = round(ap["rep"], 1) if ap else 0
    raw["named_venues"] = len(ap["venues"]) if ap else 0
    raw["clubs"] = len(ap["clubs"]) if ap else 0
    raw["slope_apres"] = len(ap["slope"]) if ap else 0
    raw["apres_events"] = ap["events"] if ap else 0
    sc["apres"] = mean([(sq(raw["apres_reputation"], 0, 5), 4), (sq(raw["named_venues"], 0, 20), 2), (lin(raw["clubs"], 0, 4), 2),
                        (lin(raw["slope_apres"], 0, 4), 1), (lin(raw["apres_events"], 0, 1), 1), (sq(bars, 0, 30), 1)])
    # audience measures built from the parts above
    raw["drag_pct"] = num(m.get("drag_pct"))
    raw["vertical_m"], raw["top_m"] = num(m.get("vertical_m")), num(m.get("top_m"))
    raw["beds_mapped"] = num(m.get("beds_mapped"))
    raw["restaurants_mountain"] = num(m.get("restaurant_mountain"))
    flat_i = num(x.get("flat_pct_intermediate")) if x else None
    sc["board"] = mean([(lin(raw["drag_pct"], 70, 0), 2), (lin(flat_i, 25, 3), 2), (lin(km["intermediate"], 0, 80), 1)]) if flat_i is not None else None
    fd = FOOD.get(r["slug"], {"michelin": 0, "stars": 0, "bib": 0, "gm": 0, "toqued": 0})
    raw.update({"michelin_stars": fd["stars"], "bib_gourmand": fd["bib"], "gm_toqued": fd["toqued"], "gm_toques": fd["gm"]})
    food_shops = None
    if x:
        poi = x.get("poi", {})
        food_shops = sum(poi.get(k, 0) for k in ("shop_bakery", "shop_butcher", "shop_cheese", "shop_deli", "shop_chocolate", "shop_greengrocer"))
    sc["food"] = mean([(sq(fd["michelin"], 0, 30), 3), (sq(fd["gm"], 0, 40), 3), (sq(num(m.get("restaurant_village")), 0, 40), 1),
                       (sq(raw["restaurants_mountain"], 0, 40), 1), (sq(food_shops, 0, 8), 1)])
    sc["mixed_ability"] = mean([(lin(km["beginner"], 0, 30), 1), (lin(km["intermediate"], 0, 80), 1), (lin(km["advanced"], 0, 60), 1)])
    sc["beds"] = sq(raw["beds_mapped"], 0, 60)
    raw["steep_km"] = num(x.get("steep_km")) if x else None
    sc["adventure"] = mean([(lin(km["advanced"], 0, 150), 2), (lin(raw["vertical_m"], 500, 2200), 2), (lin(raw["top_m"], 1800, 3400), 1),
                            (lin(raw["steep_km"], 0, 30), 2), (lin(num(m.get("resilience_lost_pct")), 80, 0), 1)])
    # off piste: guide reputation and named routes, glaciers and mapped freeride routes reachable by lift
    op, om = OFFPISTE.get(r["slug"], {"guides": {}, "routes": {}}), OFFMAP.get(r["slug"])
    raw["offpiste_guides"] = round(sum(op["guides"].values()), 1)
    raw["offpiste_routes"] = len(op["routes"])
    parts = [(sq(raw["offpiste_guides"], 0, 8), 3), (sq(raw["offpiste_routes"], 0, 15), 2)]
    if om:
        raw["glacier_ha"], raw["glacier_tops"], raw["freeride_km"] = om["glacier_ha"], om["glacier_tops"], om["freeride_km"]
        parts += [(sq(om["glacier_ha"], 0, 2000), 1), (sq(om["freeride_km"], 0, 30), 1)]
    sc["offpiste"] = mean(parts)
    pk = PARKS.get(r["slug"])
    if pk:
        raw["parks"], raw["park_area_ha"] = pk["parks"], pk["area_ha"]
        sc["parks"] = mean([(lin(pk["parks"], 0, 8), 1), (sq(pk["area_ha"], 0, 50), 2)])
    # families, non skiers and village life from OpenStreetMap features
    if x:
        poi = x.get("poi", {})
        g = lambda *k: sum(poi.get(i, 0) for i in k)
        raw.update({
            "ski_schools": g("ski_school"), "childcare": g("kindergarten", "childcare"), "playgrounds": g("playground"),
            "ice_rinks": g("ice_rink"), "pools": g("swimming_pool", "water_park"), "spas": g("spa", "sauna"),
            "culture": g("cinema", "theatre", "museum", "gallery", "library"), "attractions": g("attraction", "zoo"),
            "food_shops": g("shop_bakery", "shop_butcher", "shop_cheese", "shop_deli", "shop_chocolate", "shop_greengrocer"),
            "groceries": g("shop_supermarket", "shop_convenience"), "hire_shops": g("shop_ski", "ski_rental", "shop_sports"),
            "sled_km": x.get("trail_km_sled"), "nordic_km": x.get("trail_km_nordic"),
            "walk_km": round((x.get("trail_km_hike") or 0) + (x.get("trail_km_snowshoe") or 0), 1),
        })
        sc["families"] = mean([(lin(km["beginner"], 0, 25), 2), (lin(raw["ski_schools"], 0, 2), 2), (lin(raw["childcare"], 0, 2), 1),
                               (lin(raw["playgrounds"], 0, 3), 1), (lin(raw["sled_km"], 0, 3), 1), (lin(raw["ice_rinks"], 0, 1), 1)])
        sc["non_skiers"] = mean([(lin(raw["spas"] + raw["pools"], 0, 3), 2), (lin(raw["culture"] + raw["attractions"], 0, 4), 1),
                                 (sq(raw["walk_km"], 0, 30), 2), (sq(raw["nordic_km"], 0, 50), 1), (lin(raw["ice_rinks"], 0, 1), 1),
                                 (sq(num(m.get("restaurant_village")), 0, 30), 1), (lin(num(m.get("enclosed_pct")), 0, 30), 1)])
        sc["village"] = mean([(sq(raw["food_shops"], 0, 8), 2), (lin(raw["groceries"], 0, 3), 1), (sq(num(m.get("restaurant_village")), 0, 30), 1)])
    return raw, sc


LABEL = {"km_beginner": "Beginner km", "km_intermediate": "Intermediate km", "km_advanced": "Advanced km", "km_all": "Mapped km",
         "day_pass_eur": "Day pass €", "six_day_pass_eur": "6 day pass €", "airport_min": "Minutes from Geneva or Lyon",
         "gva_min": "Minutes from Geneva", "ski_schools": "Ski schools", "spas": "Spas", "pools": "Pools", "walk_km": "Winter walks km",
         "food_shops": "Food shops", "childcare": "Childcare", "sled_km": "Sledge km", "drag_pct": "Drag %", "parks": "Parks", "park_area_ha": "Park area ha", "restaurants_mountain": "Mountain restaurants", "nordic_km": "Cross country km", "culture": "Culture", "late_bars": "Late bars", "apres_sources": "Guides naming it", "apres_reputation": "Reputation points", "named_venues": "Named venues", "clubs": "Nightclubs", "slope_apres": "Slope après", "michelin_stars": "Michelin stars", "bib_gourmand": "Bib Gourmand", "gm_toqued": "Gault&Millau listed", "gm_toques": "Toques", "beds_mapped": "Places to stay mapped", "vertical_m": "Vertical m", "steep_km": "Steep km", "top_m": "Top m", "bars": "Bars", "restaurants": "Restaurants", "flat_pct_intermediate": "Flat %", "offpiste_guides": "Off piste guides", "offpiste_routes": "Named routes", "glacier_ha": "Glacier ha", "freeride_km": "Freeride km"}


def fmt(v):
    if v is None:
        return "n/a"
    return f"{v:g}" if isinstance(v, (int, float)) else str(v)


def run_lists(rows, recipes):
    out = []
    for L in recipes:
        cand = []
        for row in rows:
            v = {**row["raw"], **row["sc"]}
            if any(v.get(k) is None for k in L.get("require", [])):
                continue
            ok = True
            for k, (op, lim) in L.get("filters", {}).items():
                val = v.get(k)
                if val is None or (op == "<=" and val > lim) or (op == ">=" and val < lim):
                    ok = False
            if not ok:
                continue
            s = mean([(row["sc"].get(k), w) for k, w in L["weights"].items()])
            if s is None:
                continue
            contrib = sorted(((row["sc"].get(k) or 0) * w, k) for k, w in L["weights"].items())[::-1][:3]
            cand.append((s, row["name"], [k for _, k in contrib], row["raw"]))
        cand.sort(key=lambda c: -c[0])
        out.append((L, cand[: L.get("top", 10)], len(cand)))
    return out


def main():
    resorts, M, M2, A, PR = load()
    rows = []
    for r in resorts:
        raw, sc = score_resort(r, M.get(r["slug"], {}), M2.get(r["slug"]), A.get(r["slug"], {}), PR.get(r["slug"], []))
        rows.append({"slug": r["slug"], "name": r["name"], "raw": raw, "sc": sc})
    keys = sorted({k for x in rows for k in x["sc"]})
    rkeys = sorted({k for x in rows for k in x["raw"]})
    os.makedirs(P("out"), exist_ok=True)
    with open(P("out", "scores_v11.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["slug", "name"] + ["score." + k for k in keys] + rkeys)
        for x in rows:
            w.writerow([x["slug"], x["name"]] + [x["sc"].get(k) for k in keys] + [x["raw"].get(k) for k in rkeys])
    recipes = json.load(open(P("audiences.json"))) + json.load(open(P("lists.json")))
    md = ["# Lists, method v1.1 (pilot, snow not yet scored)", ""]
    for L, top, n in run_lists(rows, recipes):
        show = L.get("show", ["km_intermediate", "day_pass_eur", "airport_min"])
        md += [f"## {L['title']}", "", f"{L['note']} {n} resorts qualified.", "",
               "| Rank | Resort | Score | " + " | ".join(LABEL.get(k, k) for k in show) + " |", "|---" * (3 + len(show)) + "|"]
        for i, (s, name, lead, raw) in enumerate(top, 1):
            md.append(f"| {i} | {name} | {s / 10:.1f} | " + " | ".join(fmt(raw.get(k)) for k in show) + " |")
        md.append("")
    open(P("out", "lists_v11.md"), "w").write("\n".join(md))
    # every resort's score and rank for each audience, for the resort page hero
    allr = run_lists(rows, [{**L, "top": 10 ** 6} for L in json.load(open(P("audiences.json")))])
    aud = {x["slug"]: {} for x in rows}
    name2slug = {x["name"]: x["slug"] for x in rows}
    for L, cand, n in allr:
        for i, (sv, name, lead, raw) in enumerate(cand, 1):
            aud[name2slug[name]][L["id"]] = {"score": round(sv / 10, 1), "rank": i, "of": n}
    json.dump(aud, open(P("out", "audience_scores_v11.json"), "w"), ensure_ascii=False, indent=1)
    # the eight scores shown in a resort page hero, in a fixed order; the three highest are marked top
    HERO = [("beginners", "Beginners"), ("families", "Families"), ("adventurers", "Experts & Off Piste"), ("snowboarders", "Snowboarders"),
            ("park-rats", "Park rats"), ("non-skiers", "Non skiers"), ("party", "Après"), ("foodies", "Foodies")]
    hero = {}
    for slug, v in aud.items():
        items = [{"id": k, "label": lab, "score": v[k]["score"]} for k, lab in HERO if k in v]
        if len(items) < len(HERO):
            continue
        for i in sorted(range(len(items)), key=lambda i: -items[i]["score"])[:3]:
            items[i]["top"] = True
        for it in items:
            it["score"] = f'{it["score"]:.1f}'
        hero[slug] = {"method": "v1.1", "range": "northern-alps", "items": items}
    json.dump(hero, open(P("out", "hero_scores_v11.json"), "w"), ensure_ascii=False, indent=1)
    print(len(rows), "resorts;", len(recipes), "lists")


if __name__ == "__main__":
    main()
