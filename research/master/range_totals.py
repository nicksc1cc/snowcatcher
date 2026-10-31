"""Range totals for the France page ranges table, from fr_resorts.csv.

Ski areas: standalone resorts plus linked areas, each linked area once.
Piste km: each linked area once at the km in projectsnow's linked_domains.json;
an area shared with another country counts its largest French resort figure;
standalone resorts count their own Alti-Mag figure.
Usage: python3 range_totals.py /path/to/projectsnow/src/data/linked_domains.json
"""
import csv, json, sys
from pathlib import Path

HERE = Path(__file__).parent
RANGES = ["northern-alps", "southern-alps", "pyrenees", "jura", "vosges", "massif-central"]


def main(linked_path):
    linked = {d["slug"]: d for d in json.load(open(linked_path))["domains"]}
    rows = [r for r in csv.DictReader(open(HERE / "fr_resorts.csv")) if not r["part_of"]]
    out = []
    for rg in RANGES:
        rs = [r for r in rows if r["range"] == rg]
        areas = {}
        for r in rs:
            for a in filter(None, r["linked_areas"].split(";")):
                areas.setdefault(a, []).append(r)
        km = sum(max(float(m["alpine_km"]) for m in ms) if linked[a].get("shared_with") else float(linked[a]["km"])
                 for a, ms in areas.items())
        standalone = [r for r in rs if not r["linked_areas"]]
        km += sum(float(r["alpine_km"]) for r in standalone)
        top = max(rs, key=lambda r: int(r["top_m"] or 0))
        out.append({"range": rg, "resorts": len(rs), "areas": len(standalone) + len(areas),
                    "km": round(km), "top_m": top["top_m"], "top_resort": top["name"]})
    with open(HERE / "range_totals.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    for o in out:
        print(o)


if __name__ == "__main__":
    main(sys.argv[1])
