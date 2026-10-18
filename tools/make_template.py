"""Creates a blank record. Do not edit.
python3 tools/make_template.py <record_type> <slug>
Writes research/<folder>/<slug>.json and refuses to overwrite an existing file."""
import json, os, sys
from specs import SPECS

FOLDERS = {"country": "countries", "structure": "structure", "domain": "domains", "resort": "resorts",
           "village": "villages", "restaurant": "restaurants"}

def blank(record_type, slug):
    rec = {"meta": {"record_type": record_type, "slug": slug, "spec_version": 1,
                    "verification": {"status": "unverified"}}}
    for sec, fields in SPECS[record_type].items():
        rec[sec] = {name: {"expects": e, "questions": q.split(), "seasonal": s, "guidance": g,
                           "value": None, "status": "not_researched", "sources": []}
                    for name, (e, q, s, g) in fields.items()}
    return rec

if __name__ == "__main__":
    rtype, slug = sys.argv[1], sys.argv[2]
    path = f"research/{FOLDERS[rtype]}/{slug}.json"
    if os.path.exists(path):
        sys.exit(f"{path} already exists")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(blank(rtype, slug), open(path, "w"), indent=2, ensure_ascii=False)
    print(path)