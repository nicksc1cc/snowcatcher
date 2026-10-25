"""Score the Northern Alps resorts on the automatic measures of method v1.

Inputs (written from the browser run, see README):
  resorts.csv           Alti-Mag station list with the base point used for each resort
  data/snow.json        ERA5 seasonal snowfall at base, middle and top height for each resort
  data/measures_raw.csv SCBulk.measure output (OpenStreetMap network, venues, accommodation)
  data/access.csv       OSRM road time and distance from Geneva, Lyon, Chambéry and Grenoble airports
Output:
  out/measures.csv      raw value of every measure for every resort
  out/scores.csv        score 0 to 100 for every measure and theme, with confidence
"""
import csv, json, math, os, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(HERE, *a)

# Anchors: (floor, ceiling, shape). Linear unless shape is "sqrt". A floor above the ceiling means lower is better.
ANCHORS = {
    "snow_median_cm": (150, 800, "lin"),
    "snow_cv_pct": (60, 20, "lin"),
    "km_beginner": (0, 150, "sqrt"),
    "km_intermediate": (0, 300, "sqrt"),
    "km_advanced": (0, 300, "sqrt"),
    "drag_pct": (70, 0, "lin"),
    "enclosed_pct": (0, 40, "lin"),
    "vertical_m": (300, 2000, "lin"),
    "resilience_lost_pct": (60, 0, "lin"),
    "bed_to_lift_m": (1500, 100, "lin"),
    "ski_in_out_pct": (0, 60, "lin"),
    "access_min": (240, 60, "lin"),
    "bars": (0, 40, "sqrt"),
    "late_bars": (0, 10, "sqrt"),
    "restaurants": (0, 80, "sqrt"),
}
LEVELS = ["beginner", "intermediate", "advanced"]
THEMES = {
    "snow": ["snow_reliability", "bad_weather"],
    "skiing": ["reachable_km", "ski_in_out", "vertical_long_runs", "network_resilience", "lift_quality"],
    "getting-there": ["access"],
    "apres-food": ["bars", "late_bars", "restaurants"],
}


def scale(key, v):
    if v is None:
        return None
    lo, hi, shape = ANCHORS[key]
    t = (v - lo) / (hi - lo)
    t = min(1.0, max(0.0, t))
    if shape == "sqrt":
        t = math.sqrt(t)
    return round(100 * t, 1)


def mean(xs, w=None):
    pairs = [(x, (w or [1] * len(xs))[i]) for i, x in enumerate(xs) if x is not None]
    if not pairs:
        return None
    return round(sum(x * k for x, k in pairs) / sum(k for _, k in pairs), 1)


def at_height(bands, h):
    """Seasonal snowfall at height h, interpolated between the two nearest bands (clamped at the ends)."""
    hs = sorted(int(k) for k in bands)
    h = min(max(h, hs[0]), hs[-1])
    lo = max(x for x in hs if x <= h)
    hi = min(x for x in hs if x >= h)
    w = 0 if hi == lo else (h - lo) / (hi - lo)
    A, B = bands[str(lo)], bands[str(hi)]
    return {y: A[y] * (1 - w) + B[y] * w for y in A if y in B}


def main():
    resorts = list(csv.DictReader(open(P("resorts.csv"))))
    snow = json.load(open(P("data", "snow_cells.json"))) if os.path.exists(P("data", "snow_cells.json")) else {}
    cells = {row["slug"]: row["cell"] for row in csv.DictReader(open(P("data", "snow_cell_of_resort.csv")))}
    meas = {}
    for row in csv.DictReader(open(P("data", "measures_raw.csv"))):
        meas[row["slug"]] = {k: (None if v == "" else (v if k in ("slug", "critical_lift", "note") else float(v))) for k, v in row.items()}
    acc = {}
    for row in csv.DictReader(open(P("data", "access.csv"))):
        acc[row["slug"]] = {k: {"min": int(row[k + "_min"]), "km": int(row[k + "_km"])} for k in ["gva", "lys", "cmf", "gnb"] if row[k + "_min"]}
    raw_rows, score_rows = [], []
    for r in resorts:
        s, m, a = r["slug"], meas.get(r["slug"], {}), acc.get(r["slug"], {})
        raw = {"slug": s, "name": r["name"]}
        sc = {"slug": s, "name": r["name"]}
        conf = {}
        # snow reliability by level: Alti-Mag base height for beginners, the middle for intermediates, the top
        # for advanced. Seasons are interpolated by height between the ERA5 bands fetched for the resort's cell.
        cell = cells.get(s)
        sn = snow.get(cell) if cell else None
        b, t = int(r["base_m"]), int(r["top_m"])
        raw["era5_cell"] = cell
        for lv, h in zip(LEVELS, [b, round((b + t) / 2), t]):
            if not sn:
                continue
            seasons = at_height(sn["bands"], h)
            ref = [v for y, v in seasons.items() if 1991 <= int(y) <= 2020]
            recent = [v for y, v in seasons.items() if 2021 <= int(y) <= 2025]
            med = statistics.median(ref)
            cv = 100 * statistics.pstdev(ref) / statistics.mean(ref)
            raw[f"snow_height_{lv}_m"] = h
            raw[f"snow_median_{lv}_cm"] = round(med)
            raw[f"snow_cv_{lv}_pct"] = round(cv)
            raw[f"snow_recent_below_median_{lv}"] = sum(1 for v in recent if v < med)
            sc[f"snow_reliability.{lv}"] = mean([scale("snow_median_cm", med), scale("snow_cv_pct", cv)], [0.7, 0.3])
            conf[f"snow_reliability.{lv}"] = "medium"  # reanalysis cell of about 25 km
        if sn:
            new = statistics.median([v for y, v in sn["bands"]["1500"].items() if 1991 <= int(y) <= 2020])
            old = statistics.median(list(sn["old1500"].values()))
            raw["snow_median_1500_1961_1990_cm"] = round(old)
            raw["snow_median_1500_1991_2020_cm"] = round(new)
        for k in ["km_beginner", "km_intermediate", "km_advanced", "km_all", "lifts", "drag_pct", "enclosed_pct", "top_m", "bottom_m",
                  "vertical_m", "resilience_lost_pct", "critical_lift", "bar_village", "bar_mountain", "late", "restaurant_village",
                  "restaurant_mountain", "beds_mapped", "bed_to_lift_m", "ski_in_out_pct", "startLifts", "note"]:
            raw[k] = m.get(k)
        mapped = bool(m) and m.get("lifts")
        for lv in LEVELS:
            sc[f"reachable_km.{lv}"] = scale(f"km_{lv}", m.get(f"km_{lv}")) if mapped else None
            conf[f"reachable_km.{lv}"] = "medium" if mapped else "low"
        sc["lift_quality"] = scale("drag_pct", m.get("drag_pct")) if mapped else None
        sc["bad_weather"] = scale("enclosed_pct", m.get("enclosed_pct")) if mapped else None
        conf["bad_weather"] = "low"  # treeline share not yet measured
        sc["vertical_long_runs"] = scale("vertical_m", m.get("vertical_m")) if mapped else None
        sc["network_resilience"] = scale("resilience_lost_pct", m.get("resilience_lost_pct")) if mapped else None
        beds_ok = (m.get("beds_mapped") or 0) >= 10
        sc["ski_in_out"] = mean([scale("bed_to_lift_m", m.get("bed_to_lift_m")), scale("ski_in_out_pct", m.get("ski_in_out_pct"))], [0.6, 0.4]) if mapped and m.get("beds_mapped") else None
        conf["ski_in_out"] = "medium" if beds_ok else "low"
        times = [v["min"] for v in a.values() if v]
        raw["access_min"] = min(times) if times else None
        raw["access_from"] = min(a, key=lambda k: a[k]["min"] if a[k] else 1e9) if times else None
        sc["access"] = scale("access_min", raw["access_min"])
        bars = (m.get("bar_village") or 0) + (m.get("bar_mountain") or 0)
        rest = (m.get("restaurant_village") or 0) + (m.get("restaurant_mountain") or 0)
        sc["bars"] = scale("bars", bars) if m else None
        sc["late_bars"] = scale("late_bars", m.get("late")) if m else None
        sc["restaurants"] = scale("restaurants", rest) if m else None
        for k in ["bars", "late_bars", "restaurants"]:
            conf[k] = "medium"  # OpenStreetMap, not yet checked against tourist offices
        # theme scores, by level where a measure has levels
        for th, ms in THEMES.items():
            for lv in LEVELS:
                vals = [sc.get(f"{x}.{lv}", sc.get(x)) for x in ms]
                sc[f"theme.{th}.{lv}"] = mean(vals)
            sc[f"theme.{th}.measures_scored"] = sum(1 for x in ms if sc.get(f"{x}.intermediate", sc.get(x)) is not None)
        raw_rows.append(raw)
        sc["confidence"] = json.dumps(conf, separators=(",", ":"))
        score_rows.append(sc)
    os.makedirs(P("out"), exist_ok=True)
    for name, rows in [("measures.csv", raw_rows), ("scores.csv", score_rows)]:
        keys = []
        for row in rows:
            for k in row:
                if k not in keys:
                    keys.append(k)
        with open(P("out", name), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)
    print(len(score_rows), "resorts scored")


if __name__ == "__main__":
    main()
