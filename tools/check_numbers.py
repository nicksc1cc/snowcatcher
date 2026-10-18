"""Checks that every number in a draft exists in verified data. Do not edit.
python3 tools/check_numbers.py <draft.md> <record.json> [more records or research/derived files]
A number passes when the same value appears in a field with status found, or anywhere in a derived file.
Numbers inside HTML comments are ignored, so source notes can be left there."""
import json, re, sys

NUM = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)(?![\w])")

def to_float(s):
    return float(s.replace(",", ""))

def numbers_in(obj, out):
    if isinstance(obj, bool): return
    if isinstance(obj, (int, float)): out.add(round(float(obj), 4)); return
    if isinstance(obj, str):
        for m in NUM.findall(obj): out.add(round(to_float(m), 4))
        return
    if isinstance(obj, dict):
        for v in obj.values(): numbers_in(v, out)
    if isinstance(obj, list):
        for v in obj: numbers_in(v, out)

def verified_numbers(path):
    rec, out = json.load(open(path)), set()
    if "/derived/" in path:
        numbers_in(rec, out); return out
    for sec, fields in rec.items():
        if sec == "meta" or not isinstance(fields, dict): continue
        for f in fields.values():
            if isinstance(f, dict) and f.get("status") == "found":
                numbers_in(f.get("value"), out)
                if f.get("season"): numbers_in(f["season"].split("-"), out)
    return out

def main():
    draft, records = sys.argv[1], sys.argv[2:]
    known = set()
    for r in records: known |= verified_numbers(r)
    text = re.sub(r"(?s)<!--.*?-->", "", open(draft).read())
    bad = []
    for n, line in enumerate(text.splitlines(), 1):
        for m in NUM.findall(line):
            if round(to_float(m), 4) not in known: bad.append(f"line {n}: {m}  |  {line.strip()[:120]}")
    print(f"unmatched numbers: {len(bad)}")
    for b in bad: print("  " + b)
    sys.exit(1 if bad else 0)

if name == "__main__":
    main()