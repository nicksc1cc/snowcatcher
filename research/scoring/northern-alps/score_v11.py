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
    return resorts, m, m2, acc, prices


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
    sc["value"] = mean([(lin(raw["day_pass_eur"], 85, 20), 1), (lin(raw["six_day_pass_eur"], 470, 120), 1)])
    # après and food
    bars = (num(m.get("bar_village")) or 0) + (num(m.get("bar_mountain")) or 0)
    rest = (num(m.get("restaurant_village")) or 0) + (num(m.get("restaurant_mountain")) or 0)
    raw.update({"bars": bars, "restaurants": rest, "late_bars": num(m.get("late"))})
    sc["apres"] = mean([(sq(bars, 0, 30), 2), (sq(num(m.get("late")), 0, 6), 1), (sq(rest, 0, 80), 2)])
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
         "food_shops": "Food shops", "bars": "Bars", "restaurants": "Restaurants", "flat_pct_intermediate": "Flat %"}


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
    recipes = json.load(open(P("lists.json")))
    md = ["# Lists, method v1.1 (pilot, snow not yet scored)", ""]
    for L, top, n in run_lists(rows, recipes):
        show = L.get("show", ["km_intermediate", "day_pass_eur", "airport_min"])
        md += [f"## {L['title']}", "", f"{L['note']} {n} resorts qualified.", "",
               "| Rank | Resort | Score | " + " | ".join(LABEL.get(k, k) for k in show) + " |", "|---" * (3 + len(show)) + "|"]
        for i, (s, name, lead, raw) in enumerate(top, 1):
            md.append(f"| {i} | {name} | {s / 10:.1f} | " + " | ".join(fmt(raw.get(k)) for k in show) + " |")
        md.append("")
    open(P("out", "lists_v11.md"), "w").write("\n".join(md))
    print(len(rows), "resorts;", len(recipes), "lists")


if __name__ == "__main__":
    main()
