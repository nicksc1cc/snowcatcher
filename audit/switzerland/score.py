"""Coverage of the Switzerland country page against the question register (2026-10-19).

Scores 0 to 3 for the 139 country and range level questions, using the same scale
as the France audit: 0 not answered, 1 passing mention, 2 partial, 3 useful and evidenced.
Page: projectsnow src/switzerland.njk. Run: python3 audit/switzerland/score.py
"""
import csv, os, sys
from collections import Counter
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, ".."))
from question_bank import build

S = """CC01 3 What sets Swiss skiing apart
CC02 3 Ranges table, linked areas, altitude bands
CC03 2 Who: first timers to experts
CC04 2 Who: snowboarders; Laax Superpipe, drag lift counts
CC05 2 Cost section; no lodging totals
CC06 2 Stay: hotel and apartment overnights, second homes
CC07 2 Three kinds of resort table
CC08 1 Who: first timers
CC09 0 Not covered
TR01 3 When to go; seasons list
TR02 3 Glaciers row and opening dates
TR03 2 Glaciers into May, high resorts to late April
TR04 2 Peaks chart and range tops
TR05 2 Altitude section, Prealps and Jura watch for
TR06 3 Holiday waves and pinch week
TR07 3 Quiet windows 2027
TR08 2 When to go
TR09 2 Altitude: top lift against base
CV01 3 Range day pass averages
CV02 3 Per km chart
CV03 3 Holidu index, Zermatt price
CV04 2 Magic Pass, Prealps prices
CV05 0 No like for like lodging comparison
CV06 2 Restaurants, ski school; no rental prices
CV07 2 Vignette, tourist tax, luggage forwarding
CV08 3 Per km argument
CV09 1 Who section patterns
RG01 3 Map, table, range articles
RG02 3 Range articles compare the four high ranges
RG03 2 High Alps against Prealps and Jura
RG04 3 Table and range leads
RG05 3 Peaks chart and altitude bands
RG06 3 Linked areas by range
RG07 2 Prealps, Jura, small valley resorts
RG08 1 Car free villages; no purpose built stations named
RG09 2 Apres resorts named
RG10 2 Range suits lines
RG11 2 Pennine and central suits; experts
RG12 2 Getting there per range
RG13 3 Train times per range
RG14 1 Prealps for day trips
RG15 2 Spas and food
RG16 2 Prealps, Jura, small valleys
RG17 2 Watch for lines
SB01 2 Laax
SB05 2 Superpipe
SB06 1 Freeride resorts named
SB07 0 Not covered
SB08 1 Laax parks and terrain
AB09 3 Grading and ski routes
AB10 2 Measured against advertised km
FA01 2 Family Destination list
FA02 2 Teenagers
FA05 0 Not covered
FA12 1 Ski school price only
FA14 1 Mixed ability groups
FA15 3 Family Destination label and criteria
SO01 1 Solo travellers
GF07 2 Couples and friends
OP01 2 Experts and freeriders
OP03 0 Not covered
OP04 2 Verbier, Bec des Rosses, Engelberg, Gemsstock
OP07 1 Ski routes against off piste
OP10 2 Altitude section; no aspect
OP11 1 Rail viewpoints, spas
OP12 3 SLF bulletin, deaths, Rega
OP14 1 Experts paragraph
AP01 2 Apres resorts
AP03 1 Village evenings
AP05 2 Liveliest resorts
AP06 1 Couples line
AP08 2 Resort types table
AP09 3 Food by language region
AP12 1 Couples and friends
TA01 2 Train and road times
TA02 3 Airports and train times
TA04 3 Train times, car free arrivals
TA05 2 London by rail via Paris
TA08 2 Winter driving
TA09 0 Not covered
TA10 0 Not covered
TA11 0 Not covered
TA14 3 SBB luggage and skis
TA15 0 Not covered
AC01 1 Resort types table
AC03 2 Car free village against resort town
AC12 2 Car free logistics
SN01 3 Altitude section and bands
SN02 0 Not covered
SN04 3 Snowmaking 54%, comparison
SN05 3 Top lift against village height
SN06 3 Grindelwald, Flumserberg low runs
SN07 0 Not covered
SN08 2 Altitude results 2025/26
SN09 3 SLF season study, Zermatt summer 2026
SN10 1 Snow study only
SN11 1 Altitude section
NS01 2 Engadin, Jura
NS02 1 Sledging
NS03 3 Leukerbad, Vals, Scuol, Bad Ragaz
NS04 1 Rail viewpoints
NS07 2 Wengernalpbahn, viewpoints, spas
NS09 1 Spas and trains
PR03 1 Emergency numbers
PR05 2 Rega and travel insurance
PR06 3 Rescue and Rega
PR07 2 Ski routes and off piste
PR08 2 Words to know
PR09 0 Not covered
PR10 1 Car free villages, trains
AC13 2 Hotel and apartment overnights, second homes
AC14 0 Not covered
AC15 1 Hotel types named
AC16 0 Not covered
AC18 1 Resort types table
AC19 0 Not covered: no reliable price data
AC20 0 Not covered: no reliable price data
AC21 3 Tourist tax and guest cards
AC22 0 Not covered
AC23 0 Not covered
AC24 0 Not covered
AC25 0 Not covered
FD01 1 Village evenings
FD02 3 HolidayCheck summit restaurant prices
FD03 3 Food by region
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
TI05 1 Non skiers via trains and spas
TI06 2 Car free distance to lifts"""

bank = {q["id"]: q for q in build()["questions"]}
fr = {r["id"]: r for r in csv.DictReader(open(os.path.join(HERE, "..", "france", "coverage_after.csv"), encoding="utf-8"))}
rows = []
for line in S.splitlines():
    qid, sc, ev = line.split(" ", 2)
    q = bank[qid]
    rows.append({"id": qid, "category": q["category"], "question": q["template"].format(country="Switzerland"),
                 "level": q["level"], "score": int(sc), "evidence": ev, "france_score": fr[qid]["score"]})
with open(os.path.join(HERE, "coverage.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(len(rows), "questions")
print("Switzerland", sorted(Counter(r["score"] for r in rows).items()))
print("France     ", sorted(Counter(int(r["france_score"]) for r in rows).items()))
