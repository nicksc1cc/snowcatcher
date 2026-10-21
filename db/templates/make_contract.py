"""Derive the data contract of a page template from pages already live on it.
A path present in every page is required; one present in some is optional. Arrays are described
by the union of their elements. Usage: python3 make_contract.py <out.json> <page.json> [<page.json> ...]"""
import json, sys

def shape(v):
    if isinstance(v, dict): return {"type": "object", "keys": {k: shape(x) for k, x in v.items()}}
    if isinstance(v, list):
        el = None
        for x in v: el = merge(el, shape(x), union=True)
        return {"type": "array", "items": el}
    if isinstance(v, bool): return {"type": "boolean"}
    if isinstance(v, (int, float)): return {"type": "number"}
    if v is None: return {"type": "null"}
    return {"type": "string"}

def merge(a, b, union=False):
    """Combine two shapes. In union mode (array elements) keys missing on either side become optional."""
    if a is None: return b
    if b is None: return a
    ta, tb = set(a["type"].split("|")), set(b["type"].split("|"))
    out = {"type": "|".join(sorted(ta | tb))}
    if "object" in ta | tb:
        ka, kb = a.get("keys", {}), b.get("keys", {})
        keys = {}
        for k in list(ka) + [k for k in kb if k not in ka]:
            s = merge(ka.get(k), kb.get(k), union=True)
            if k not in ka or k not in kb or ka[k].get("optional") or kb[k].get("optional"):
                s = dict(s, optional=True)
            keys[k] = s
        out["keys"] = keys
    if "array" in ta | tb:
        out["items"] = merge(a.get("items"), b.get("items"), union=True)
    return out

pages = [shape(json.load(open(p, encoding="utf-8"))) for p in sys.argv[2:]]
c = None
for p in pages: c = merge(c, p)
json.dump(c, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
req = [k for k, s in c["keys"].items() if not s.get("optional")]
print(len(c["keys"]), "top level keys,", len(req), "required:", ", ".join(req))
print("optional:", ", ".join(k for k, s in c["keys"].items() if s.get("optional")))
