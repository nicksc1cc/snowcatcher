"""Print JSON the way Postgres jsonb prints it, so a page can be compared with the database by hash."""
import hashlib, json, sys

def canon(o):
    if isinstance(o, dict):
        ks = sorted(o, key=lambda k: (len(k.encode()), k.encode()))
        return "{" + ", ".join(json.dumps(k, ensure_ascii=False) + ": " + canon(o[k]) for k in ks) + "}"
    if isinstance(o, list):
        return "[" + ", ".join(canon(x) for x in o) + "]"
    return json.dumps(o, ensure_ascii=False)

if __name__ == "__main__":
    s = canon(json.load(open(sys.argv[1], encoding="utf-8")))
    print(hashlib.md5(s.encode()).hexdigest(), len(s))
    if len(sys.argv) > 2:
        d = json.load(open(sys.argv[1], encoding="utf-8"))
        for k in d: print(k, hashlib.md5(canon(d[k]).encode()).hexdigest())
