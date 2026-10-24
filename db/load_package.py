"""Load a research package into the Snow Catchers database as drafts, and render a local preview.

A package is a folder in research/<area>/ with:
  package.json          page id, place, template, path, datasets and their files
  data/evidence_register.csv   the sources (id, claim, value, source, url, type, retrieved)
  data/places.csv       id,type,name,subtype,lat,lon,parent,links,aliases
  data/facts.csv        name,place_id,property,value,method,legacy_ref,scope,qualifiers,season,dataset,note
  data/properties.csv   optional, new properties (same columns as core.property)
  page/draft.json       the page in its template's shape, see below

In the draft every string is text. Figures inside it are tokens: {{f:name}}, {{f:name|n}}, {{diff:a,b}},
{{m:all.from.to|w}}, where a name is a fact in facts.csv or an existing fact id such as F000071.
A number that is a figure is {"$f": "name"} or {"$m": ["all", from, to]}; a place name is {"$p": id}.
Chapter items are [{"place": id, "name": optional, "where": text, "text": text}].
Photos are [file, author, licence, alt]. Network links are [from, to, kind, critical, label].

Usage:
  python3 load_package.py <package dir> --start <next fact number> --existing <existing facts json>
                         --contract <template contract> --out <sql dir> [--preview <site l3 dir>]
Nothing is written to the database by this script; it writes SQL for review and loading.
"""
import argparse, csv, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from snowdb import q, qarr, resolve_text, resolve_layout, token_refs, fmt_fact  # noqa: E402

ap = argparse.ArgumentParser()
for a in ("package", ):
    ap.add_argument(a)
ap.add_argument("--start", type=int, required=True)
ap.add_argument("--existing", required=True)
ap.add_argument("--contract", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--preview")
args = ap.parse_args()
P = args.package
problems, notes = [], []


def rd(path):
    return list(csv.DictReader(open(os.path.join(P, path), encoding="utf-8")))


def slug(s):
    import unicodedata
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


meta = json.load(open(os.path.join(P, "package.json"), encoding="utf-8"))
draft = json.load(open(os.path.join(P, "page/draft.json"), encoding="utf-8"))
contract = json.load(open(args.contract, encoding="utf-8"))
existing = {f["id"]: f for f in json.load(open(args.existing, encoding="utf-8"))}
A = meta["place_id"]

# ---------------------------------------------------------------- contract
MAPS = {"photos", "breaks"}


def check_shape(v, s, path):
    if s is None:
        problems.append(f"{path}: not in the template contract")
        return
    types = set(s["type"].split("|"))
    t = ("null" if v is None else "boolean" if isinstance(v, bool) else "number" if isinstance(v, (int, float))
         else "string" if isinstance(v, str) else "array" if isinstance(v, list) else "object")
    if isinstance(v, dict) and set(v) & {"$f", "$m"}:
        t = "number"
    if isinstance(v, dict) and "$p" in v:
        t = "string"
    if t not in types:
        problems.append(f"{path}: {t} where the template expects {s['type']}")
        return
    if t == "object" and path.split(".")[-1] not in MAPS:
        for k, sub in s.get("keys", {}).items():
            if k not in v and not sub.get("optional"):
                problems.append(f"{path}.{k}: missing")
        for k, x in v.items():
            check_shape(x, s.get("keys", {}).get(k), f"{path}.{k}")
    if t == "array" and s.get("items"):
        for i, x in enumerate(v):
            check_shape(x, s["items"], f"{path}.{i}")


# the contract is checked on the rendered page, after references are resolved (see below)

# ---------------------------------------------------------------- sources, places, properties
STYPE = {"operator": "operator", "guide": "guide", "independent": "listing", "derived": "open_data", "model": "model",
         "press": "press", "tourism": "tourism", "internal": "internal"}
REG = {r["id"]: r for r in rd("data/evidence_register.csv")}
sources, src_of = {}, {}
for lid, r in REG.items():
    url = r["url"].strip()
    if not url:
        sid = "src:snow-catchers-analysis"
        sources.setdefault(sid, dict(id=sid, title="Snow Catchers analysis", publisher="Snow Catchers", url=None, source_type="internal"))
    else:
        from urllib.parse import urlparse
        u = urlparse(url)
        host = u.netloc.replace("www.", "")
        host = host.rsplit(".", 1)[0] if "." in host else host
        sid = ("src:" + slug(host + "-" + u.path + ("-" + u.query if u.query else "")))[:64].rstrip("-")
        sources.setdefault(sid, dict(id=sid, title=r["source"], publisher=r["source"].split(" (")[0], url=url, source_type=STYPE[r["type"]]))
    src_of[lid] = sid

places = rd("data/places.csv")
place_ids = {p["id"] for p in places}
links, aliases = [], []
for p in places:
    if p.get("parent"):
        rel, to = p["parent"].split(":", 1)
        links.append((p["id"], to, rel, True))
    for l in filter(None, (p.get("links") or "").split(";")):
        rel, to = l.split(":", 1)
        links.append((p["id"], to, rel, False))
    for a in filter(None, (p.get("aliases") or "").split("|")):
        aliases.append((p["id"], a))
props = rd("data/properties.csv") if os.path.exists(os.path.join(P, "data/properties.csv")) else []

# ---------------------------------------------------------------- facts
facts, ID = {}, {}
n = args.start
for r in rd("data/facts.csv"):
    name = r["name"]
    if name in facts:
        problems.append(f"fact {name}: defined twice")
    v = r["value"]
    is_date = bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", v))
    unit = r.get("unit") or ({"km": "km"}.get(None))
    row = dict(id=f"F{n:06d}", place_id=r["place_id"], property=r["property"], scope=r["scope"] or None,
               qualifiers=json.loads(r["qualifiers"]) if r["qualifiers"] else {}, season=r["season"] or None,
               method=r["method"], legacy_ref=r["legacy_ref"] or None, dataset_id=r["dataset"] or None,
               note=r["note"] or None, unit=r["unit"], value_text=v if is_date or not re.fullmatch(r"-?\d+(\.\d+)?", v) else None,
               value_num=None if is_date or not re.fullmatch(r"-?\d+(\.\d+)?", v) else (float(v) if "." in v else int(v)))
    row["source_id"] = r.get("source_id") or (src_of.get(r["legacy_ref"]) if r["legacy_ref"] else None)
    if r["legacy_ref"] and r["legacy_ref"] not in REG:
        problems.append(f"fact {name}: evidence {r['legacy_ref']} is not in the register")
    if not row["source_id"] and not row["dataset_id"]:
        problems.append(f"fact {name}: no source and no dataset")
    facts[name] = row
    ID[name] = row["id"]
    n += 1
BYID = {f["id"]: f for f in facts.values()}
BYID.update(existing)

NAMED = re.compile(r"\{\{(f|diff):([^}|]+)")


def to_ids(t):
    def one(x):
        if re.fullmatch(r"F\d{6}", x):
            if x not in existing:
                problems.append(f"fact {x} is not in the database")
            return x
        if x not in ID:
            problems.append(f"token refers to unknown fact {x}")
            return x
        return ID[x]
    return NAMED.sub(lambda m: "{{" + m.group(1) + ":" + ",".join(one(x) for x in m.group(2).split(",")), t)


# ---------------------------------------------------------------- matrices, datasets
MATRICES = {}
net_meta = meta.get("network")
NET = None
if net_meta:
    NET = json.load(open(os.path.join(P, net_meta["file"]), encoding="utf-8"))
    MATRICES = {"all": NET["all"], "easy": NET["ability"]["easy"], "red": NET["ability"]["red"]}

# ---------------------------------------------------------------- layout, blocks, lists, media
STRUCT = {"_about", "slug", "permalink", "nav", "href", "u", "photo", "id", "cc", "link", "kind", "place", "lat", "lon", "ev"}
SLOT = {"h2": "heading", "h3": "heading", "basesH3": "heading", "catchesH3": "heading", "conflictsH3": "heading", "kicker": "kicker",
        "listTitle": "heading", "mapTitle": "heading", "heightsTitle": "heading", "chartTitle": "heading", "matrixTitle": "heading",
        "coverageTitle": "heading", "scenariosTitle": "heading", "paras": "para", "basesParas": "para", "lead": "lead",
        "caption": "caption", "heightsCaption": "caption", "chartCaption": "caption", "basesCaption": "caption", "mapHelp": "caption",
        "note": "note", "accessNote": "note", "basesNote": "note", "matrixNote": "note", "after": "note"}
SECTION = {"sectors": "network", "links": "network", "mapNotes": "network", "title": "meta", "description": "meta", "crumbs": "meta"}
blocks, ordc, lists, media, media_links, sector_links = [], {}, {}, [], [], []
ref_places = set()
sec_prefix = meta.get("sector_prefix", "")


def section_of(path):
    if path[0] == "chapters":
        return draft["chapters"][path[1]]["id"]
    return SECTION.get(path[0], path[0])


def add_block(field, section, key, text):
    if "—" in text or "–" in text:
        problems.append(f"{field}: contains a dash")
    body = to_ids(text)
    slot = SLOT.get(key, "line")
    ordc[(section, slot)] = ordc.get((section, slot), -1) + 1
    blocks.append(dict(field=field, section=section, slot=slot, ord=ordc[(section, slot)], body=body,
                       fact_refs=sorted(set(token_refs(body)))))
    return {"$b": field}


def build(node, path):
    field = ".".join(str(p) for p in path)
    lastkey = next((p for p in reversed(path) if isinstance(p, str)), None)
    if isinstance(node, dict) and "$p" in node:
        ref_places.add(node["$p"])
        return node
    if isinstance(node, dict) and "$f" in node:
        return {"$f": to_ids("{{f:" + node["$f"] + "}}")[4:-2]}
    if isinstance(node, dict) and "$m" in node:
        return node
    if path == ["links"]:
        for i, (a, b, kind, crit, label) in enumerate(node):
            sector_links.append((sec_prefix + a, sec_prefix + b, "lift_down" if kind == "ride" else "ski", crit, label, i))
        return {"$links": net_meta["dataset"]}
    if path and path[0] == "photos" and len(path) == 2:
        file, author, lic, alt = node
        from urllib.parse import quote
        mid = "m:" + slug(os.path.splitext(file)[0])[:56]
        media.append(dict(id=mid, file_name=file, author=author, licence=lic, alt=alt,
                          remote_url="https://commons.wikimedia.org/wiki/Special:FilePath/" + quote(file.replace(" ", "_")),
                          page_url="https://commons.wikimedia.org/wiki/File:" + quote(file.replace(" ", "_"))))
        role = "hero" if path[1] == "hero" else ("break" if any(v.get("photo") == path[1] for v in draft["breaks"].values()) else "chapter")
        media_links.append((mid, A, role, path[1]))
        return {"$media": mid}
    if len(path) == 3 and path[0] == "chapters" and path[2] == "items":
        lid = f"list:{A.split(':')[1]}.{draft['chapters'][path[1]]['id']}"
        lists[lid] = dict(title=draft["chapters"][path[1]]["listTitle"], chapter=draft["chapters"][path[1]]["id"], items=[])
        for it in node:
            pid = it["place"]
            ref_places.add(pid)
            attrs = {"where": it["where"]}
            if it.get("name"):
                attrs["name"] = it["name"]
            body = to_ids(it["text"])
            lists[lid]["items"].append(dict(place=pid, attrs=attrs, blurb=body, fact_refs=sorted(set(token_refs(body)))))
        return {"$list": lid}
    if path == ["mapBox"] or lastkey in STRUCT or (path and path[0] == "breaks"):
        return node
    if isinstance(node, dict):
        return {k: build(v, path + [k]) for k, v in node.items()}
    if isinstance(node, list):
        return [build(v, path + [i]) for i, v in enumerate(node)]
    if isinstance(node, bool) or node is None:
        return node
    if isinstance(node, (int, float)):
        problems.append(f"{field}: number {node} typed into the page; it must be a fact")
        return node
    return add_block(field, section_of(path), lastkey, node)


layout = build(draft, [])
for pid in ref_places:
    if pid not in place_ids and not any(pid == f.get("place_id") for f in existing.values()) and pid not in meta.get("existing_places", []):
        problems.append(f"place {pid} is neither in places.csv nor listed as existing")

# ---------------------------------------------------------------- local render
ctx = dict(blocks={b["field"]: b["body"] for b in blocks}, facts=BYID, matrices=MATRICES,
           places={**{p["id"]: p for p in places}, **meta.get("existing_place_names", {})},
           media={m["id"]: m for m in media},
           lists={lid: [dict(item_place_id=i["place"], attrs=i["attrs"], blurb=i["blurb"]) for i in L["items"]] for lid, L in lists.items()},
           links={net_meta["dataset"]: [[a[len(sec_prefix):], b[len(sec_prefix):], "ride" if by == "lift_down" else "lift", c, l]
                                        for a, b, by, c, l, o in sector_links]} if net_meta else {})
for k, v in meta.get("existing_place_names", {}).items():
    ctx["places"][k] = {"name": v}
try:
    rendered = resolve_layout(layout, ctx)
except KeyError as e:
    problems.append(f"render failed: missing {e}")
    rendered = None
if rendered is not None:
    check_shape(rendered, contract, "page")

if problems:
    print("PROBLEMS")
    for p in problems:
        print(" -", p)
    sys.exit(1)

# figures still typed in the words
FIG = re.compile(r"(?<![\w{|:.])(?:€\s?)?\d[\d,.]*(?:\s?(?:km|m|cm|%))?")
typed = [(b["field"], m.strip()) for b in blocks for m in FIG.findall(re.sub(r"\{\{[^}]+\}\}", "", re.sub(r"<[^>]+>", "", b["body"])))]

# ---------------------------------------------------------------- SQL
sql = [f"-- Draft load for {meta['page_id']}, generated by db/load_package.py from {os.path.basename(os.path.normpath(P))}. Review before running."]
add = sql.append
add("insert into core.place (id,type,subtype,name,slug,status,lat,lon) values\n" + ",\n".join(
    f"({q(p['id'])},{q(p['type'])},{q(p.get('subtype') or None)},{q(p['name'])},{q(p.get('slug') or slug(p['name']))},'draft',"
    f"{q(float(p['lat'])) if p.get('lat') else 'null'},{q(float(p['lon'])) if p.get('lon') else 'null'})" for p in places)
    + "\non conflict (id) do nothing;")
if aliases:
    add("insert into core.place_alias (place_id,alias) values\n" + ",\n".join(f"({q(a)},{q(b)})" for a, b in aliases) + "\non conflict do nothing;")
if links:
    add("insert into core.place_link (from_id,to_id,relation,is_primary) values\n" + ",\n".join(
        f"({q(a)},{q(b)},{q(r)},{q(p)})" for a, b, r, p in links) + "\non conflict do nothing;")
add("insert into core.source (id,title,publisher,url,source_type) values\n" + ",\n".join(
    f"({q(s['id'])},{q(s['title'])},{q(s['publisher'])},{q(s['url'])},{q(s['source_type'])})" for s in sources.values()) + "\non conflict (id) do nothing;")
if props:
    add("insert into core.property (key,label,value_type,unit,applies_to,qualifier_keys,allowed_methods,definition,requires_scope) values\n" + ",\n".join(
        f"({q(p['key'])},{q(p['label'])},{q(p['value_type'])},{q(p['unit'] or None)},{qarr(p['applies_to'].split('|'))},"
        f"{qarr([x for x in p['qualifier_keys'].split('|') if x])},{qarr(p['allowed_methods'].split('|'))},{q(p['definition'] or None)},{q(p['requires_scope'] == 'true')})"
        for p in props) + "\non conflict (key) do nothing;")
for d in meta.get("datasets", []):
    outputs = json.load(open(os.path.join(P, d["outputs_file"]), encoding="utf-8")) if d.get("outputs_file") else None
    add("insert into model.dataset (id,kind,title,place_id,inputs,script_repo,script_path,run_at,status,note,outputs) values "
        f"({q(d['id'])},{q(d['kind'])},{q(d['title'])},{q(d.get('place_id'))},{q(d.get('inputs', {}))},'nicksc1cc/snowcatcher',"
        f"{q(d.get('script_path'))},{q(d.get('run_at'))},'draft',{q(d.get('note'))},{q(outputs) if outputs else 'null'}) on conflict (id) do nothing;")
add("insert into core.fact (id,place_id,property,scope,value_num,value_text,unit,qualifiers,season,method,source_id,dataset_id,retrieved_at,status,legacy_ref,note,created_by) values\n" + ",\n".join(
    f"({q(f['id'])},{q(f['place_id'])},{q(f['property'])},{q(f['scope'])},{q(f['value_num'])},{q(f['value_text'])},{q(f['unit'] or None)},{q(f['qualifiers'])},"
    f"{q(f['season'])},{q(f['method'])},{q(f['source_id'])},{q(f['dataset_id'])},{q(meta['retrieved'])},'draft',{q(f['legacy_ref'])},{q(f['note'])},'loader')"
    for f in facts.values()) + ";")
add(f"select setval('core.fact_seq', greatest((select last_value from core.fact_seq), {n - 1}));")
snow = meta.get("snow")
if snow:
    rows = list(csv.DictReader(open(os.path.join(P, snow["file"]), encoding="utf-8")))
    heights = [int(k.split("_")[-1]) for k in rows[0] if k.startswith("snowfall_cm_")]
    add("insert into model.weather_obs (dataset_id,cell_id,elevation_m,season,snowfall_cm) values\n" + ",\n".join(
        f"({q(snow['dataset'])},{q(snow['cell'])},{h},'{r['season_start']}/{str(int(r['season_start']) + 1)[2:]}',{r[f'snowfall_cm_{h}']})"
        for r in rows for h in heights) + ";")
if sector_links:
    add("insert into model.sector_link (dataset_id,from_sector,to_sector,by,one_way,critical_edges,conditions,note) values\n" + ",\n".join(
        f"({q(net_meta['dataset'])},{q(a)},{q(b)},{q(by)},false,{qarr([l] if c else [])},{q({'ord': o, 'critical': c})},{q(l)})"
        for a, b, by, c, l, o in sector_links) + ";")
sections = sorted({b["section"] for b in blocks})
add("insert into content.section (key,label,levels,ord) values\n" + ",\n".join(
    f"({q(s)},{q(s.capitalize())},array['area']::text[],100)" for s in sections) + "\non conflict (key) do nothing;")
add("insert into content.content_block (place_id,section,slot,ord,body,fact_refs,status,author,field) values\n" + ",\n".join(
    f"({q(A)},{q(b['section'])},{q(b['slot'])},{b['ord']},{q(b['body'])},{qarr(b['fact_refs'])},'review','loader',{q(b['field'])})" for b in blocks) + ";")
KIND = {"snowboard": "snowpark", "families": "family", "food": "eat", "apres": "apres"}
if lists:
    add("insert into content.place_list (id,place_id,title,kind,status) values\n" + ",\n".join(
        f"({q(lid)},{q(A)},{q(L['title'])},{q(KIND.get(L['chapter'], 'other'))},'review')" for lid, L in lists.items()) + ";")
    add("insert into content.place_list_item (list_id,item_place_id,ord,blurb,fact_refs,attrs) values\n" + ",\n".join(
        f"({q(lid)},{q(i['place'])},{o},{q(i['blurb'])},{qarr(i['fact_refs'])},{q(i['attrs'])})"
        for lid, L in lists.items() for o, i in enumerate(L["items"])) + ";")
if media:
    add("insert into content.media (id,kind,remote_url,page_url,file_name,author,licence,alt,status) values\n" + ",\n".join(
        f"({q(m['id'])},'photo',{q(m['remote_url'])},{q(m['page_url'])},{q(m['file_name'])},{q(m['author'])},{q(m['licence'])},{q(m['alt'])},'draft')"
        for m in media) + "\non conflict (id) do nothing;")
    add("insert into content.media_link (media_id,place_id,role,slot) values\n" + ",\n".join(
        f"({q(a)},{q(b)},{q(c)},{q(d)})" for a, b, c, d in media_links) + "\non conflict do nothing;")
add("insert into content.page (id,place_id,level,template,canonical_path,title,status,layout) values "
    f"({q(meta['page_id'])},{q(A)},{meta['level']},{q(meta['template'])},{q(meta['canonical_path'])},{q(draft['title'])},'review',{q(layout)});")
pp = sorted({f["place_id"] for f in facts.values()} | ref_places | {s[0] for s in sector_links} | {s[1] for s in sector_links})
add("insert into content.page_place (page_id,place_id,role) values\n" + ",\n".join(
    f"({q(meta['page_id'])},{q(p)},{q('subject' if p == A else 'mentions')})" for p in pp) + "\non conflict do nothing;")

os.makedirs(args.out, exist_ok=True)
open(os.path.join(args.out, "load.sql"), "w", encoding="utf-8").write("\n\n".join(sql) + "\n")
json.dump({"facts": len(facts), "next_fact": n, "blocks": len(blocks), "list_items": sum(len(L["items"]) for L in lists.values()),
           "media": len(media), "places": len(places), "typed_figures": typed},
          open(os.path.join(args.out, "report.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"facts {len(facts)} (next {n}), blocks {len(blocks)}, places {len(places)}, media {len(media)}, typed figures left {len(typed)}")

if args.preview and rendered is not None:
    s = draft["slug"]
    open(os.path.join(args.preview, f"{s}.json"), "w", encoding="utf-8").write(json.dumps(rendered, ensure_ascii=False, indent=2) + "\n")
    if NET is not None:
        open(os.path.join(args.preview, f"{s}.network.json"), "w", encoding="utf-8").write(json.dumps(NET, ensure_ascii=False))
    if snow:
        import shutil
        shutil.copy(os.path.join(P, snow["file"]), os.path.join(args.preview, f"{s}.snow.csv"))
    print("preview written for", s)
