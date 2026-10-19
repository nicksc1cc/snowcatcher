"""Coverage of the Italy country page against the question register (2026-10-19).

Scores 0 to 3 for the 139 country and range level questions, using the same scale
as the France audit: 0 not answered, 1 passing mention, 2 partial, 3 useful and evidenced.
Page: projectsnow src/italy.njk. Run: python3 audit/italy/score.py
"""
import csv, os, sys
from collections import Counter
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, ".."))
from question_bank import build

S = """CC01 3 What sets Italian skiing apart: languages, Dolomiti Superski, snowmaking
CC02 3 Ranges table, linked areas, altitude bands
CC03 2 Who: first timers to experts
CC04 2 Who: snowboarders; skiresort.com park ranking
CC05 2 JFC week costs with caveat, pass prices; no rental or food totals
CC06 1 Resort types table only
CC07 2 Three kinds of resort table and text
CC08 1 Who: first timers
CC09 0 Not covered
TR01 1 Opening dates only; closing dates not yet announced
TR02 3 Cervinia and Val Senales from 24 October
TR03 0 Not covered: closing dates not published
TR04 2 Peaks chart and range tops
TR05 2 Altitude section, range watch for lines
TR06 3 Holiday dates by region, Dolomiti Superski peak periods, busiest week
TR07 3 Quiet windows 2027
TR08 2 When to go
TR09 2 Altitude: top lift against base
CV01 3 Range day pass averages
CV02 3 Per km chart
CV03 2 Cortina and Dolomiti Superski against Champorcher
CV04 2 Cheaper ranges and Via Lattea per km
CV05 0 No like for like lodging comparison
CV06 2 Lessons from €150 a week; no rental or hut prices
CV07 2 Mont Blanc tunnel tolls, tourist tax; no transfer prices
CV08 3 Per km argument
CV09 1 Who section patterns
RG01 3 Map, table, range articles
RG02 3 Range articles compare west, central and Dolomites
RG03 2 Alps against the Apennines and Etna
RG04 3 Table and range leads
RG05 3 Peaks chart and altitude bands
RG06 3 Linked areas by range, Sella Ronda
RG07 2 Carnic and Julian Alps, South Tyrol size
RG08 2 Purpose built Sestriere against valley villages
RG09 1 Towns named for evenings only
RG10 2 Range suits lines
RG11 2 Monterosa, Courmayeur, Cervinia
RG12 2 Getting there per range
RG13 0 Not covered
RG14 2 Turin and Apennine weekends
RG15 2 Spas, Olympic venues, Etna
RG16 2 Carnic and Julian Alps, South Tyrol
RG17 2 Watch for lines
SB01 2 Park ranking
SB05 3 Parks named from skiresort.com ranking
SB06 1 Freeride areas named
SB07 0 Not covered
SB08 1 Parks and freeride areas
AB09 0 Not covered
AB10 2 Measured against advertised km
FA01 1 Helmet and tourist tax rules only
FA02 2 Teenagers
FA05 0 Not covered
FA12 1 Altroconsumo group day cost only
FA14 1 Mixed ability groups
FA15 0 Not covered
SO01 1 Solo travellers
GF07 1 Couples and friends
OP01 2 Experts and freeriders
OP03 0 Not covered
OP04 1 Monterosa, Courmayeur
OP07 0 Not covered
OP10 2 Altitude section; no aspect
OP11 1 Spas and Olympic venues
OP12 3 Avalanche deaths 2025/26, rescue charges, equipment
OP14 1 Experts paragraph
AP01 0 Not covered
AP03 1 Towns named
AP05 0 Not covered
AP06 1 Couples line
AP08 2 Resort types table
AP09 2 Rifugio dishes; no regional cheese detail
AP12 1 Couples and friends
TA01 2 Airport transfer times
TA02 3 Turin, Geneva, Innsbruck, Verona, Venice with times
TA04 0 Not covered
TA05 0 Not covered
TA08 3 Winter tyre dates and fines
TA09 0 Not covered
TA10 0 Not covered
TA11 0 Not covered
TA14 0 Not covered
TA15 0 Not covered
AC01 1 Resort types table
AC03 2 Valley village against purpose built resort
AC12 2 Village choice and bus in the Dolomites
SN01 3 Altitude section and bands
SN02 0 Not covered
SN04 3 90% snowmaking against neighbours, abandoned lifts
SN05 3 Top lift against village height
SN06 2 Low runs home in March
SN07 0 Not covered
SN08 1 Altitude bands
SN09 1 Opening dates only
SN10 0 Not covered
SN11 1 Altitude section
NS01 1 Olympic Nordic venues named
NS02 0 Not covered
NS03 2 QC Terme Bormio
NS04 1 Historic towns named
NS07 1 Spas and towns
NS09 1 Towns and Etna
PR03 1 Emergency number
PR05 3 Compulsory third party insurance, rescue charges
PR06 3 Rescue charges, avalanche data
PR07 2 Helmet, insurance and alcohol rules
PR08 2 Words to know
PR09 0 Not covered
PR10 1 Village choice
AC13 0 Not covered: no accommodation mix data
AC14 0 Not covered
AC15 1 Hotel types named
AC16 0 Not covered
AC18 2 Resort types table
AC19 1 JFC range by resort only
AC20 1 JFC week per person, assumptions not stated
AC21 3 South Tyrol tourist tax range and child exemption
AC22 0 Not covered
AC23 0 Not covered
AC24 0 Not covered
AC25 0 Not covered
FD01 1 Resort types table
FD02 0 Not covered
FD03 2 Rifugio dishes
FD04 0 Not covered
DL01 0 Not covered
DL02 0 Not covered
DL04 0 Not covered
RT01 2 Resort types table
RT02 2 Resort types table
RT03 0 Not covered
RT05 1 Cheaper village down the valley
TI01 2 Families
TI02 2 Couples
TI03 1 Solo travellers
TI04 1 Friends
TI05 1 Spas
TI06 2 Village choice in the Dolomites"""

bank = {q["id"]: q for q in build()["questions"]}
fr = {r["id"]: r for r in csv.DictReader(open(os.path.join(HERE, "..", "france", "coverage_after.csv"), encoding="utf-8"))}
rows = []
for line in S.splitlines():
    qid, sc, ev = line.split(" ", 2)
    q = bank[qid]
    rows.append({"id": qid, "category": q["category"], "question": q["template"].format(country="Italy"),
                 "level": q["level"], "score": int(sc), "evidence": ev, "france_score": fr[qid]["score"]})
with open(os.path.join(HERE, "coverage.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(len(rows), "questions")
print("Italy      ", sorted(Counter(r["score"] for r in rows).items()))
print("France     ", sorted(Counter(int(r["france_score"]) for r in rows).items()))
