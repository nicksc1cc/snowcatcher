"""Coverage of the Austria country page against the question register (2026-10-19).

Scores 0 to 3 for the 139 country and range level questions, using the same scale
as the France audit: 0 not answered, 1 passing mention, 2 partial, 3 useful and evidenced.
Page: projectsnow src/austria.njk. Run: python3 audit/austria/score.py
"""
import csv, os, sys
from collections import Counter
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, ".."))
from question_bank import build

S = """CC01 3 What sets Austrian skiing apart
CC02 3 Ranges table, linked areas, altitude bands
CC03 2 Who: first timers to experts
CC04 2 Who: snowboarders; park ratings, drag lift counts
CC05 2 Cost section; no lodging totals
CC06 2 Stay: Salzburg overnights by type
CC07 2 Three kinds of resort table
CC08 1 Who: first timers
CC09 0 Not covered
TR01 3 When to go; seasons list
TR02 3 Glaciers row and opening dates
TR03 2 Glaciers into May, high resorts to late April
TR04 2 Peaks chart and range tops
TR05 2 Altitude section, Kitzbühel Alps watch for
TR06 3 Holiday waves and pinch week
TR07 3 Quiet windows 2027
TR08 2 When to go
TR09 2 Altitude: top lift against base
CV01 3 Range day pass averages
CV02 3 Per km chart
CV03 3 Holidu index, Obergurgl-Hochgurgl
CV04 1 Cheaper ranges averages only
CV05 0 No like for like lodging comparison
CV06 2 Hut prices; no lesson or rental prices
CV07 3 Vignette, special tolls, tourist tax
CV08 3 Per km argument
CV09 1 Who section patterns
RG01 3 Map, table, range articles
RG02 3 Range articles compare the four high ranges
RG03 2 Glacier ranges against Kitzbühel Alps and the south
RG04 3 Table and range leads
RG05 3 Peaks chart and altitude bands
RG06 3 Linked areas by range
RG07 2 Northern Limestone Alps east, the south
RG08 2 Villages rather than stations
RG09 2 Apres resorts named
RG10 2 Range suits lines
RG11 2 Arlberg, glaciers; experts
RG12 2 Getting there per range
RG13 3 Train times per range
RG14 1 Not specific
RG15 2 Spas and food
RG16 2 Bregenzerwald, Lungau, south
RG17 2 Watch for lines
SB01 2 Park ratings
SB05 3 Parks named from skiresort.com ratings
SB06 1 Freeride resorts named
SB07 0 Not covered
SB08 1 Parks and Arlberg terrain
AB09 3 Tyrol gradient limits
AB10 2 Measured against advertised km
FA01 3 Serfaus, SkiWelt, Ski Juwel family details
FA02 2 Teenagers
FA05 0 Not covered
FA12 1 Child free passes only
FA14 1 Mixed ability groups
FA15 1 No national family label
SO01 1 Solo travellers
GF07 2 Couples and friends
OP01 2 Experts and freeriders
OP03 0 Not covered
OP04 1 Arlberg, Valluga
OP07 1 Ski routes against off piste
OP10 2 Altitude section; no aspect
OP11 1 Rail viewpoints, spas
OP12 3 Avalanche deaths 2025/26, bulletins, rescue cost
OP14 1 Experts paragraph
AP01 3 Apres ranking, top bars named
AP03 1 Village evenings
AP05 3 Apres resorts and bars
AP06 1 Couples line
AP08 2 Resort types table
AP09 2 Hut dishes; no regional cheese detail
AP12 1 Couples and friends
TA01 2 Train and road times
TA02 3 Airports and train times
TA04 3 Stations in resorts, Nightjet, onward times
TA05 3 Nightjet routes and times
TA08 3 Winter tyre law, fines
TA09 0 Not covered
TA10 0 Not covered
TA11 0 Not covered
TA14 1 Not covered beyond trains
TA15 0 Not covered
AC01 1 Resort types table
AC03 2 Village on a circuit against resort town
AC12 1 Choosing the village on a circuit
SN01 3 Altitude section and bands
SN02 0 Not covered
SN04 3 75% snowmaking, 10.4 million skier days estimate
SN05 3 Top lift against village height
SN06 3 Kitzbühel Alps low runs, Zillertal valley floor
SN07 0 Not covered
SN08 2 Altitude results 2025/26
SN09 2 Season results 2025/26; no Austrian snow trend study
SN10 1 Snow study only
SN11 1 Altitude section
NS01 3 Seefeld 245 km
NS02 1 Sledging
NS03 3 Gastein, Aqua Dome, Römerbad, Tauern Spa
NS04 1 Rail viewpoints
NS07 1 Spas and Kitzbühel
NS09 1 Spas and trains
PR03 1 Emergency numbers
PR05 2 Rescue costs, insurance
PR06 3 Rescue and emergency numbers
PR07 2 Ski routes and off piste
PR08 2 Words to know
PR09 0 Not covered
PR10 1 Trains
AC13 3 Stay: Salzburg hotels 54.8%, apartments 33.3%, private rooms 2.6%
AC14 0 Not covered
AC15 1 Guesthouse and hotel types named
AC16 0 Not covered
AC18 1 Resort types table
AC19 0 Not covered: no reliable price data
AC20 0 Not covered: no reliable price data
AC21 3 Tyrol tourist tax range and child exemption
AC22 0 Not covered
AC23 0 Not covered
AC24 0 Not covered
AC25 0 Not covered
FD01 1 Village evenings
FD02 3 AK Salzburg hut price survey 2024
FD03 3 Hut dishes
FD04 0 Not covered
DL01 1 Self catering line
DL02 0 Not covered
DL04 0 Not covered
RT01 2 Resort types table
RT02 2 Resort types table
RT03 0 Not covered
RT05 1 Small valley resort column
TI01 2 Families
TI02 2 Couples
TI03 2 Solo travellers
TI04 2 Friends
TI05 1 Spas
TI06 1 Village choice on a circuit"""

bank = {q["id"]: q for q in build()["questions"]}
fr = {r["id"]: r for r in csv.DictReader(open(os.path.join(HERE, "..", "france", "coverage_after.csv"), encoding="utf-8"))}
rows = []
for line in S.splitlines():
    qid, sc, ev = line.split(" ", 2)
    q = bank[qid]
    rows.append({"id": qid, "category": q["category"], "question": q["template"].format(country="Austria"),
                 "level": q["level"], "score": int(sc), "evidence": ev, "france_score": fr[qid]["score"]})
with open(os.path.join(HERE, "coverage.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(len(rows), "questions")
print("Austria    ", sorted(Counter(r["score"] for r in rows).items()))
print("France     ", sorted(Counter(int(r["france_score"]) for r in rows).items()))
