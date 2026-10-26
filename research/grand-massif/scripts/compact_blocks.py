"""Write out/blocks_compact_<n>.sql from the content block insert in out/load.sql, in chunks. Usage: python3 scripts/compact_blocks.py"""
import re
s = open("out/load.sql").read()
start = s.index("insert into content.content_block ")
end = s.index(");\n", start) + 2
body = s[start:end].split(" values\n", 1)[1].rstrip(";")
rows = re.findall(r"^\('area:grand-massif',(.*),'review','loader',('[^']*')\),?$", body, re.M)
out = []
for mid, field in rows:
    mid = mid.replace("::text[]", "")
    out.append(f"({mid},{field})")
chunks, cur, size = [], [], 0
for r in out:
    if size + len(r) > 26000 and cur:
        chunks.append(cur); cur, size = [], 0
    cur.append(r); size += len(r)
chunks.append(cur)
for i, c in enumerate(chunks):
    sql = ("insert into content.content_block (place_id,section,slot,ord,body,fact_refs,status,author,field)\n"
           "select 'area:grand-massif',v.section,v.slot,v.ord,v.body,v.refs::text[],'review','loader',v.field from (values\n"
           + ",\n".join(c) + ") as v(section,slot,ord,body,refs,field);\n")
    open(f"out/blocks_compact_{i}.sql", "w").write(sql)
print(len(rows), [len(c) for c in chunks])
