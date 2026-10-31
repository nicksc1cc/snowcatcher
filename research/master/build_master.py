"""Build the master list of French alpine resorts: each resort once, with its
range, department and any linked areas (slugs from projectsnow's
src/data/linked_domains.json). A single resort with several villages is a
resort, not a linked area.

Inputs: ../scoring/northern-alps/resorts.csv (Alti-Mag, Northern Alps) and
altimag_south_pyr_jura_vosges_mc.csv (Alti-Mag range pages, 2026-10-31).
Output: fr_resorts.csv
"""
import csv, re, unicodedata
from pathlib import Path

HERE = Path(__file__).parent


def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


# Northern Alps departments: nearest GeoNames place to the resort point,
# with these corrections where the nearest place lies over a border.
NA_DEPT = {}
CORRECT = {
    "bessans": "Savoie", "val-cenis": "Savoie", "vallorcine": "Haute-Savoie",
    "crest-voland": "Savoie", "flumet": "Savoie", "notre-dame-de-bellecombe": "Savoie",
    "la-giettaz": "Savoie",
}

LINKED = {
    "les-3-vallees": ["courchevel", "meribel", "les-menuires", "saint-martin-de-belleville", "val-thorens", "orelle"],
    "paradiski": ["la-plagne", "champagny-en-vanoise", "montchavin-les-coches", "les-arcs", "peisey-vallandry"],
    "les-sybelles": ["le-corbier", "la-toussuire", "saint-sorlin-d-arves", "saint-jean-d-arves", "les-bottieres", "saint-colomban-des-villards"],
    "tignes-val-disere": ["tignes", "val-d-isere"],
    "espace-diamant": ["les-saisies", "hauteluce", "notre-dame-de-bellecombe", "flumet", "crest-voland", "praz-sur-arly"],
    "le-grand-domaine": ["valmorel", "saint-francois-longchamp"],
    "galibier-thabor": ["valloire", "valmeinier"],
    "espace-san-bernardo": ["la-rosiere"],
    "portes-du-soleil": ["avoriaz-1800", "morzine", "les-gets", "chatel", "montriond", "abondance", "la-chapelle-d-abondance", "saint-jean-d-aulps"],
    "evasion-mont-blanc": ["megeve", "saint-gervais", "combloux", "la-giettaz"],
    "grand-massif": ["flaine", "samoens", "les-carroz-d-araches", "morillon"],
    "la-clusaz-manigod": ["la-clusaz", "manigod"],
    "les-contamines-hauteluce": ["les-contamines-montjoie", "hauteluce"],
    "les-houches-saint-gervais": ["les-houches", "saint-gervais"],
    "hirmentaz-les-haberes": ["bellevaux-hirmentaz", "habere-poche"],
    "vallorcine-le-tour": ["vallorcine", "chamonix-mont-blanc"],
    "alpe-dhuez-grand-domaine": ["l-alpe-d-huez", "auris-en-oisans", "oz-en-oisans", "vaujany", "villard-reculas"],
    "villard-correncon": ["villard-de-lans"],
    "via-lattea": ["montgenevre"],
    "foret-blanche": ["vars", "risoul"],
    "espace-lumiere": ["pra-loup", "val-d-allos-la-foux"],
    "devoluy": ["superdevoluy", "la-joue-du-loup"],
    "valberg-beuil": ["valberg", "beuil-les-launes"],
    "molines-saint-veran": ["molines-en-queyras", "saint-veran"],
    "grand-tourmalet": ["bareges", "la-mongie-grand-tourmalet"],
    "font-romeu-pyrenees-2000": ["font-romeu", "pyrenees-2000"],
    "les-rousses": ["les-rousses"],
}

# Stations Alti-Mag lists separately that belong to another resort.
PART_OF = {"briancon": "serre-chevalier", "termignon": "val-cenis"}

SHARED = {"le-somport-candanchu": "Spain"}


def main():
    import reverse_geocoder as rg

    out = []
    na = list(csv.DictReader(open(HERE.parent / "scoring/northern-alps/resorts.csv")))
    geo = rg.search([(float(r["lat"]), float(r["lon"])) for r in na], verbose=False)
    for r, g in zip(na, geo):
        dept = CORRECT.get(r["slug"]) or re.sub(r"^Departement (de la |de l'|du |de |d')", "", g["admin2"])
        dept = {"Isere": "Isère", "Drome": "Drôme"}.get(dept, dept)
        out.append({"slug": r["slug"], "name": r["name"], "range": "northern-alps", "department": dept,
                    "base_m": r["base_m"], "top_m": r["top_m"], "alpine_km": r["alpine_km"]})
    for r in csv.DictReader(open(HERE / "altimag_south_pyr_jura_vosges_mc.csv")):
        if not r["alpine_km"]:
            continue
        out.append({"slug": slugify(r["name"].split(" / ")[0]), "name": r["name"], "range": r["range"],
                    "department": r["department"], "base_m": r["base_m"], "top_m": r["top_m"],
                    "alpine_km": r["alpine_km"]})

    member = {}
    for area, slugs in LINKED.items():
        for s in slugs:
            member.setdefault(s, []).append(area)
    known = {r["slug"] for r in out}
    missing = [s for s in member if s not in known]
    assert not missing, f"linked slugs not in list: {missing}"

    rows = []
    for r in out:
        r["linked_areas"] = ";".join(member.get(r["slug"], []))
        r["part_of"] = PART_OF.get(r["slug"], "")
        r["shared_with"] = SHARED.get(r["slug"], "")
        r["source"] = "Alti-Mag range page"
        rows.append(r)
    rows.sort(key=lambda r: (r["range"], r["slug"]))
    dupes = {s for s in (r["slug"] for r in rows) if [x["slug"] for x in rows].count(s) > 1}
    assert not dupes, dupes
    cols = ["slug", "name", "range", "department", "base_m", "top_m", "alpine_km",
            "linked_areas", "part_of", "shared_with", "source"]
    with open(HERE / "fr_resorts.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    from collections import Counter
    resorts = [r for r in rows if not r["part_of"]]
    print(len(rows), "rows,", len(resorts), "resorts")
    print(Counter(r["range"] for r in resorts))
    print("standalone:", sum(1 for r in resorts if not r["linked_areas"]))


if __name__ == "__main__":
    main()
