"""Write out/facts_compact.sql, a shorter form of the facts insert in out/load.sql. Usage: python3 scripts/compact_facts.py (from research/grand-massif)"""
import re
s = open("out/load.sql").read()
start = s.index("insert into core.fact ")
end = s.index(");\n", start) + 2
rows = re.findall(r"^\((.*)\),?$", s[start:end].split(" values\n", 1)[1].rstrip(";"), re.M)
srcs, dss, out = {}, {}, []
for r in rows:
    f, cur, q, i = [], "", False, 0
    while i < len(r):
        c = r[i]
        if c == "'":
            if q and i + 1 < len(r) and r[i + 1] == "'":
                cur += "''"; i += 2; continue
            q = not q; cur += c
        elif c == "," and not q:
            f.append(cur); cur = ""
        else:
            cur += c
        i += 1
    f.append(cur)
    id_, pl, pr, sc, vn, vt, un, qu, se, me, so, ds, ret, st, lr, no, cb = f
    qu = qu.replace("::jsonb", "")
    qu = "''" if qu == "'{}'" else qu
    if so != "null": so = "'s%d'" % srcs.setdefault(so, len(srcs))
    if ds != "null": ds = "'d%d'" % dss.setdefault(ds, len(dss))
    out.append("(%s)" % ",".join([id_, pl, pr, sc, vn, vt, un, qu, se, me, so, ds, lr, no]))
smap = ",".join("('s%d',%s)" % (i, k) for k, i in srcs.items())
dmap = ",".join("('d%d',%s)" % (i, k) for k, i in dss.items())
sql = ("with s(k,id) as (values %s), d(k,id) as (values %s), v(id,place_id,property,scope,value_num,value_text,unit,q,season,method,sk,dk,legacy_ref,note) as (values\n%s)\n"
       "insert into core.fact (id,place_id,property,scope,value_num,value_text,unit,qualifiers,season,method,source_id,dataset_id,retrieved_at,status,legacy_ref,note,created_by)\n"
       "select v.id,v.place_id,v.property,v.scope,v.value_num::numeric,v.value_text,v.unit,coalesce(nullif(v.q,''),'{}')::jsonb,v.season,v.method,s.id,d.id,'2026-10-26','draft',v.legacy_ref,v.note,'loader' from v left join s on s.k=v.sk left join d on d.k=v.dk;\n"
       ) % (smap, dmap, ",\n".join(out))
sql += s[end:s.index("\n", s.index("select setval", end)) + 1]
open("out/facts_compact.sql", "w").write(sql)
print(len(rows), len(sql))
