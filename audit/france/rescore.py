"""Rescore the France page after checkpoint 2.

Baseline: projectsnow branch france-redesign after the checkpoint 2 commit (2026-10-19).
Reads coverage.json (checkpoint 1 scores), applies the new scores below, writes
coverage_after.csv with before and after side by side.
Run: python3 audit/france/rescore.py
"""
import csv, json, os
from collections import Counter

HERE = os.path.dirname(__file__)
rows = json.load(open(os.path.join(HERE, "coverage.json")))["rows"]

# id: (score, confidence, where on the page)
AFTER = {
 "CC01": (3,"medium","What sets French skiing apart"), "CC02": (3,"medium","What sets French skiing apart; ranges table"),
 "CC03": (2,"medium","Who France suits"), "CC04": (1,"low","Who France suits: snowboarders deferred to area pages"),
 "CC05": (2,"medium","What a week costs: passes, lessons, spending shares; no accommodation prices"),
 "CC07": (3,"medium","What sets French skiing apart: trade off paragraph"), "CC08": (2,"medium","Who France suits: first timers"),
 "TR01": (2,"low","When to go: season windows still legacy"), "TR02": (2,"low","Season windows; range panels"),
 "TR03": (2,"low","Season windows"), "TR04": (2,"medium","Range panels, Watch for"), "TR05": (2,"medium","Range panels; altitude section"),
 "TR06": (3,"high","School holidays table and pinch point"), "TR07": (3,"high","Quiet windows from the dates"),
 "TR08": (2,"medium","Quiet windows; no price data"), "TR09": (2,"low","Altitude section"),
 "CV01": (2,"medium","Range table pass averages"), "CV02": (3,"medium","Pass table with per km"), "CV03": (3,"medium","Pass table"),
 "CV04": (1,"medium","Sector passes mentioned"), "CV06": (2,"medium","ESF prices, spending shares"), "CV08": (3,"medium","Per km and beginner paragraph"),
 "CV09": (1,"medium","Range averages only"),
 "RG01": (3,"medium","Map, table, six range panels"), "RG02": (3,"medium","Range panels"), "RG03": (3,"medium","Range panels"),
 "RG04": (3,"medium","Range panels; Beyond downhill"), "RG05": (3,"medium","Range table, highest lifts"), "RG06": (3,"low","Linked areas by range; km unconfirmed"),
 "RG07": (2,"medium","Range panels"), "RG08": (2,"medium","Apart section; range panels"), "RG09": (1,"low","Couples and friends"),
 "RG10": (2,"medium","Range Suits lines; families"), "RG11": (2,"medium","Experts; range panels"), "RG12": (2,"medium","Range Getting there"),
 "RG13": (2,"high","Eurostar, OUIGO, night train"), "RG14": (2,"medium","Jura, Vosges panels"), "RG15": (2,"medium","Range panels; Beyond downhill"),
 "RG16": (3,"medium","Range panels"), "RG17": (3,"medium","Range Watch for lines; cost section"),
 "SK01": (1,"medium","Sarenne"), "SK03": (1,"low","Linked area sizes"),
 "AB09": (3,"medium","First timers: colour grading and its limits"), "AB10": (1,"medium","First timers"),
 "FA01": (2,"medium","Families with young children"), "FA02": (2,"low","Families with teenagers"), "FA12": (1,"medium","Child lesson prices only"),
 "FA14": (1,"low","Mixed ability"), "FA15": (3,"medium","Famille Plus criteria"),
 "SB01": (1,"low","Snowboarders deferred"), "SO01": (2,"medium","Solo travellers"), "GF07": (1,"low","Couples and friends"),
 "OP01": (2,"medium","Experts; Pyrenees"), "OP04": (1,"low","Experts"), "OP07": (1,"medium","Off piste section"), "OP10": (1,"low","Altitude section"),
 "OP12": (3,"medium","Off piste section"), "AP01": (1,"low","Couples and friends"), "AP03": (1,"low","Couples and friends"),
 "AP05": (1,"low","Couples and friends"), "AP06": (1,"low","Couples and friends"), "AP08": (2,"medium","Apart section"), "AP09": (1,"medium","Jura"),
 "AP12": (1,"low","Couples and friends"), "NS07": (1,"medium","Beyond downhill"), "PR10": (1,"medium","Apart section trade off"),
 "SN01": (3,"low","Altitude section; bands still legacy data"), "SN04": (2,"medium","Snowmaking share"), "SN06": (2,"low","Altitude section"),
 "SN08": (2,"low","Glaciers"), "SN09": (3,"high","Météo-France 1971 to 2019 finding"), "SN11": (2,"medium","Southern Alps panel"),
 "TA01": (2,"medium","Range Getting there"), "TA02": (3,"medium","Range Getting there"), "TA04": (3,"high","Train paragraph; range panels"),
 "TA05": (2,"high","Eurostar ski train; Briançon night train"), "TA08": (2,"low","Winter driving"), "TA14": (1,"low","Flying with skis"),
 "NS01": (3,"medium","Beyond downhill; Jura panel"), "NS02": (1,"low","Vosges panel"), "NS04": (2,"medium","Range panels"),
 "NS06": (2,"medium","Pic du Midi, Les Rousses"), "NS09": (1,"low","Range panels"),
 "PR03": (2,"medium","Emergencies"), "PR05": (2,"medium","Insurance at the lift"), "PR06": (3,"medium","Rescue; off piste"),
 "PR07": (2,"medium","Off piste section"), "PR08": (2,"medium","Words to know"), "AC03": (2,"medium","Apart section"),
 "AC12": (1,"low","First time in France"), "AC01": (1,"low","Apart section"),
}

out = []
for r in rows:
    s, c, ev = AFTER.get(r["id"], (r["score"], r["confidence"], r["evidence"]))
    out.append({**r, "score_before": r["score"], "score": s, "confidence": c, "evidence": ev})

with open(os.path.join(HERE, "coverage_after.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
    w.writeheader(); w.writerows(out)

page = [r for r in out if r["level"] in ("country", "range")]
print("France page before", sorted(Counter(r["score_before"] for r in page).items()))
print("France page after ", sorted(Counter(r["score"] for r in page).items()))
print("still 0 or 1:", [r["id"] for r in page if r["score"] <= 1])
