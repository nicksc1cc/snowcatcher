"""Checks any record. Only this script may set meta.verification. Do not edit.

python3 tools/check_record.py <file>                         structure check, all sections
python3 tools/check_record.py <file> --section 02_statistics  one section
python3 tools/check_record.py <file> --fetch                 also confirm each excerpt appears on its page
python3 tools/check_record.py <file> --fetch --write-status  full check that writes meta.verification
"""
import json, re, sys, html, unicodedata, argparse, urllib.request, datetime
from specs import SPECS

STATUSES = {"not_researched", "found", "conflicting", "not_found", "not_applicable"}
SOURCE_TYPES = {"official_resort", "official_lift_operator", "official_tourism", "industry_body",
                "government", "encyclopedia", "news", "secondary_guide", "tour_operator", "other"}
SCOPE_REQUIRED = {"ski_area_count", "average_day_pass_eur", "calais_to_alps_hours", "pistes_km_measured",
                  "child_6day_eur", "senior_6day_eur", "base_altitude_m", "pistes_km", "monthly_snow_depth"}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SEASON = re.compile(r"^\d{4}-\d{4}$")

def type_ok(exp, v):
    if exp == "text": return isinstance(v, str) and len(v.strip()) > 0
    if exp == "number": return isinstance(v, (int, float)) and not isinstance(v, bool)
    if exp == "integer": return isinstance(v, int) and not isinstance(v, bool)
    if exp == "boolean": return isinstance(v, bool)
    if exp == "date": return isinstance(v, str) and bool(DATE.match(v))
    if exp == "list": return isinstance(v, list) and len(v) > 0 and all(isinstance(x, str) and x for x in v)
    if exp == "table": return isinstance(v, list) and len(v) > 0 and all(isinstance(x, dict) and x for x in v)
    return False

def check_source(s, where, errs):
    if not isinstance(s, dict): errs.append(f"{where}: source is not an object"); return
    if not str(s.get("url", "")).startswith("http"): errs.append(f"{where}: source url missing")
    if s.get("source_type") not in SOURCE_TYPES: errs.append(f"{where}: source_type must be one of {sorted(SOURCE_TYPES)}")
    ex = s.get("excerpt", "")
    if not isinstance(ex, str) or not 3 <= len(ex) <= 300: errs.append(f"{where}: excerpt must be 3 to 300 characters")
    if not DATE.match(str(s.get("retrieved", ""))): errs.append(f"{where}: retrieved must be YYYY-MM-DD")

def check_field(path, f, spec, errs):
    exp, qs, seasonal, guide = spec
    if not isinstance(f, dict): errs.append(f"{path}: not an object"); return
    if f.get("expects") != exp or f.get("questions") != qs.split() or f.get("seasonal") != seasonal or f.get("guidance") != guide:
        errs.append(f"{path}: expects, questions, seasonal or guidance was changed from the template")
    st = f.get("status")
    if st not in STATUSES: errs.append(f"{path}: invalid status {st!r}"); return
    v, srcs = f.get("value"), f.get("sources", [])
    if not isinstance(srcs, list): errs.append(f"{path}: sources must be a list"); srcs = []
    for i, s in enumerate(srcs): check_source(s, f"{path}.sources[{i}]", errs)
    if st == "found":
        if not type_ok(exp, v): errs.append(f"{path}: value does not match expected type {exp}")
        if not srcs: errs.append(f"{path}: found but has no sources")
        if path.split(".")[-1] in SCOPE_REQUIRED and not f.get("scope_note"): errs.append(f"{path}: scope_note required")
    elif v is not None:
        errs.append(f"{path}: value must be null when status is {st}")
    if st == "conflicting":
        c = f.get("candidates", [])
        if not isinstance(c, list) or len(c) < 2: errs.append(f"{path}: conflicting needs at least 2 candidates")
        else:
            for i, cand in enumerate(c):
                if not isinstance(cand, dict) or cand.get("value") is None or not cand.get("sources"):
                    errs.append(f"{path}.candidates[{i}]: needs a value and sources")
                else:
                    for j, s in enumerate(cand["sources"]): check_source(s, f"{path}.candidates[{i}].sources[{j}]", errs)
    if st == "not_found" and len(f.get("searched", [])) < 2: errs.append(f"{path}: not_found needs at least 2 entries in searched")
    if st == "not_applicable" and not f.get("notes"): errs.append(f"{path}: not_applicable needs notes explaining why")
    if seasonal and st in ("found", "conflicting") and not SEASON.match(str(f.get("season", ""))):
        errs.append(f"{path}: seasonal field needs season like 2025-2026")

def norm(t):
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    t = re.sub(r"[‘’'`\"]", "", t)
    return re.sub(r"\s+", " ", t).strip()

_cache = {}
def page_text(url):
    if url not in _cache:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 snowcatcher-checker"})
            raw = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "ignore")
            raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
            _cache[url] = norm(raw)
        except Exception as e:
            _cache[url] = e
    return _cache[url]

def fetch_check(path, f, errs, unreachable):
    groups = [f.get("sources", [])] + [c.get("sources", []) for c in f.get("candidates", []) if isinstance(c, dict)]
    for srcs in groups:
        for s in srcs:
            if not isinstance(s, dict) or not s.get("url"): continue
            txt = page_text(s["url"])
            if isinstance(txt, Exception): unreachable.append(f"{path}: {s['url']} ({type(txt).__name__})"); continue
            if norm(s.get("excerpt", "")) not in txt: errs.append(f"{path}: excerpt not found on {s['url']}")

SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

def structure_rules(rec, errs):
    resorts = rec.get("02_resorts", {}).get("resorts", {})
    slugs = set()
    if resorts.get("status") == "found":
        for i, r in enumerate(resorts["value"]):
            if not SLUG.match(str(r.get("slug", ""))): errs.append(f"02_resorts.resorts[{i}]: bad slug")
            slugs.add(r.get("slug"))
    for sec, field, minimum in (("03_linked_domains", "linked_domains", 2), ("04_pass_networks", "pass_networks", 2)):
        f = rec.get(sec, {}).get(field, {})
        if f.get("status") != "found": continue
        for i, d in enumerate(f["value"]):
            members = d.get("member_resorts")
            if not isinstance(members, list) or len(members) < minimum:
                errs.append(f"{sec}.{field}[{i}]: needs at least {minimum} member_resorts")
                continue
            for m in members:
                if "/" in str(m): continue
                if m not in slugs: errs.append(f"{sec}.{field}[{i}]: member {m!r} is not in 02_resorts; use <region-slug>/<slug> or abroad/<slug> for resorts outside this region")
            if field == "linked_domains" and not d.get("link_evidence"):
                errs.append(f"{sec}.{field}[{i}]: link_evidence required")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file"); ap.add_argument("--section"); ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--write-status", action="store_true")
    a = ap.parse_args()
    rec = json.load(open(a.file))
    errs, unreachable, counts = [], [], {}
    rtype = rec.get("meta", {}).get("record_type")
    if rtype not in SPECS: sys.exit(f"unknown meta.record_type {rtype!r}")
    SPEC = SPECS[rtype]
    extra = set(rec) - set(SPEC) - {"meta"}
    if extra: errs.append(f"unknown top level keys: {sorted(extra)}")
    for sec, fields in SPEC.items():
        if a.section and sec != a.section: continue
        got = rec.get(sec, {})
        missing, added = set(fields) - set(got), set(got) - set(fields)
        if missing: errs.append(f"{sec}: missing fields {sorted(missing)}")
        if added: errs.append(f"{sec}: unknown fields {sorted(added)}")
        c = dict.fromkeys(sorted(STATUSES), 0)
        for name, spec in fields.items():
            if name not in got: continue
            path = f"{sec}.{name}"
            check_field(path, got[name], spec, errs)
            c[got[name].get("status")] = c.get(got[name].get("status"), 0) + 1
            if a.fetch and got[name].get("status") in ("found", "conflicting"): fetch_check(path, got[name], errs, unreachable)
        counts[sec] = c
    if rtype == "structure" and not a.section: structure_rules(rec, errs)
    for sec, c in counts.items():
        print(f"{sec:28} " + "  ".join(f"{k}:{v}" for k, v in c.items() if v))
    print(f"\nerrors: {len(errs)}")
    for e in errs: print("  " + e)
    if a.fetch:
        print(f"\nunreachable sources (not counted as passed): {len(unreachable)}")
        for u in unreachable: print("  " + u)
    if a.write_status:
        if not a.fetch or a.section: sys.exit("--write-status needs --fetch and a full run with no --section")
        total = {k: sum(c.get(k, 0) for c in counts.values()) for k in STATUSES}
        ok = not errs and not unreachable
        rec["meta"]["verification"] = {"status": "verified" if ok else "failed",
            "checked_at": datetime.datetime.now().isoformat(timespec="seconds"),
            "coverage": total, "errors": errs[:200], "unreachable": unreachable[:200]}
        json.dump(rec, open(a.file, "w"), indent=2, ensure_ascii=False)
        print(f"\nmeta.verification.status = {rec['meta']['verification']['status']}")
    sys.exit(1 if errs else 0)

if __name__ == "__main__":
    main()