"""Accommodation, food and daily living audit for the France page (2026-10-19).

Scores the 37 new questions (AC13 to AC26, FD, DL, RT, TI) and rescores related
existing questions, before and after the 'Where to stay, and how to eat' section.
Before = live page at f3075b6. After = projectsnow branch france-redesign.
Writes coverage_accommodation.csv and merges the new rows into coverage_after.csv.
Run: python3 audit/france/score_accommodation.py
"""
import csv, json, os, sys
from collections import Counter

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, ".."))
from question_bank import build

# id: (before, after, confidence, where, priority, research still needed)
S = {
 "AC13": (2, 3, "medium", "Stay section: apartments dominate; MKG 2015, Cour des comptes 2024", 1, "Current bed mix by type from Atout France or regional observatories"),
 "AC14": (0, 3, "medium", "Stay section: catered chalets after Brexit", 2, "UK operator chalet counts by season"),
 "AC15": (0, 2, "low", "Stay section: types described, comfort only via building age", 2, "Comparable comfort and service evidence by type"),
 "AC16": (0, 3, "medium", "Stay section: five palaces, all in Courchevel", 3, ""),
 "AC18": (1, 3, "medium", "Stay section and resort type table", 1, ""),
 "AC19": (0, 2, "low", "Stay section: January or spring against February, illustrative only", 1, "Measured weekly prices by period and range with stated property size"),
 "AC20": (0, 2, "low", "Stay section: Alti-Mag illustrative family estimates with assumptions", 1, "Measured realistic totals; couple and group scenarios"),
 "AC21": (0, 3, "medium", "Stay section: tourist tax range, extras to check", 1, "Typical cleaning and linen charges by operator"),
 "AC22": (0, 1, "low", "Stay section: many rentals change over on Saturday", 2, "Operator terms on arrival days and minimum stays"),
 "AC23": (0, 2, "low", "Stay section: compact apartments, studio with bunk alcove", 2, "Average floor area by advertised capacity"),
 "AC24": (0, 2, "medium", "Stay section: Tourisme & Handicap, Serre Chevalier lifts", 2, "Labelled lodgings by range"),
 "AC25": (0, 3, "medium", "Stay section: energy ratings from 2022 study", 3, ""),
 "AC26": (0, 1, "low", "Who: some residences add pools and children's clubs", 3, "Resort level"),
 "FD01": (0, 1, "low", "Resort type table, village shops", 2, "Restaurant counts by resort type"),
 "FD02": (0, 3, "medium", "Stay section: €29 average bill, by department", 1, "Mountain restaurant prices against village"),
 "FD03": (1, 3, "high", "Stay section: dishes and cheeses by range", 2, ""),
 "FD04": (0, 1, "medium", "Stay section: palaces in Courchevel", 3, "Michelin guide by resort"),
 "DL01": (1, 2, "medium", "Stay section: Sherpa network", 1, "Resort against valley grocery prices"),
 "DL02": (0, 2, "low", "Stay section: Sherpa pre-ordering, 2014 source flagged", 2, "Current delivery services by resort"),
 "DL04": (0, 1, "low", "Getting there: Saturday traffic; Stay: Saturday changeover", 2, "Check in times and luggage services"),
 "RT01": (2, 3, "high", "Stay section: Courchevel 1948, Plan Neige 1964 to 1977, villages", 1, ""),
 "RT02": (1, 3, "medium", "Resort type table", 1, ""),
 "RT03": (0, 3, "medium", "Stay section: La Plagne seven high sites and three villages", 2, "More hybrid examples by range"),
 "RT05": (0, 2, "low", "Resort type table; evenings paragraph", 2, "Shuttle hours by resort"),
 "TI01": (1, 2, "low", "Who: families with young children", 1, ""),
 "TI02": (0, 2, "low", "Who: couples and friends", 2, ""),
 "TI03": (0, 2, "low", "Who: solo travellers", 2, ""),
 "TI04": (1, 2, "low", "Who: couples and friends", 2, ""),
 "TI05": (1, 1, "low", "Beyond downhill; villages in stay section", 2, "Non skier activity by resort type"),
 "TI06": (0, 1, "low", "Stay: snow close to the door", 3, ""),
 # existing questions now better answered
 "AC01": (1, 3, "medium", "Resort type table", 1, ""),
 "AC03": (2, 3, "medium", "Stay section", 1, ""),
 "AC12": (1, 2, "low", "Stay section: fees, photos and floor area", 2, ""),
 "CC06": (0, 2, "medium", "Stay section: apartments dominate, chalets rarer", 1, ""),
 "CV05": (0, 1, "low", "Stay section: illustrative only, no like for like comparison", 1, "Like for like cost by type"),
 "AP08": (2, 3, "medium", "Stay section: evenings by resort type", 2, ""),
 "AP09": (1, 3, "high", "Stay section: food by range", 2, ""),
 "GF07": (1, 2, "low", "Who: couples and friends", 2, ""),
}

bank = build()
qs = {q["id"]: q for q in bank["questions"]}
rows = []
for qid, (b, a, conf, where, pri, need) in S.items():
    q = qs[qid]
    rows.append({"id": qid, "category": q["category"], "question": q["template"].format(country="France"),
                 "audience": q["audience"], "level": q["level"], "score_before": b, "score": a,
                 "confidence": conf, "evidence": where, "priority": pri, "research_still_needed": need})
with open(os.path.join(HERE, "coverage_accommodation.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

# merge into coverage_after.csv
path = os.path.join(HERE, "coverage_after.csv")
existing = list(csv.DictReader(open(path, encoding="utf-8")))
by = {r["id"]: r for r in existing}
for qid, (b, a, conf, where, pri, need) in S.items():
    q = qs[qid]
    base = by.get(qid, {"id": qid, "category": q["category"], "question": q["template"].format(country="France"),
                        "audience": q["audience"], "dimension": q["dimension"], "level": q["level"],
                        "research": need, "priority": pri, "action": "", "action_type": "", "score_before": b})
    base.update({"score": a, "confidence": conf, "evidence": where})
    by[qid] = base
# questions in the bank not yet scored anywhere (resort level new ones) get a dependency row
for qid, q in qs.items():
    if qid not in by:
        by[qid] = {"id": qid, "category": q["category"], "question": q["template"].format(country="France"),
                   "audience": q["audience"], "dimension": q["dimension"], "level": q["level"], "score": 0,
                   "confidence": "none", "evidence": "", "research": "Resort level research", "priority": 9,
                   "action": "Dependency for resort pages", "action_type": "later", "score_before": 0}
fields = list(existing[0].keys())
with open(path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore"); w.writeheader()
    for qid in [q["id"] for q in bank["questions"]]: w.writerow(by[qid])

new_ids = [k for k in S if k[:2] in ("AC", "FD", "DL", "RT", "TI") and (k[:2] != "AC" or int(k[2:]) >= 13)]
print("new questions scored on page:", len(new_ids), "of 37")
print("before", sorted(Counter(S[k][0] for k in new_ids).items()))
print("after ", sorted(Counter(S[k][1] for k in new_ids).items()))
page = [by[q["id"]] for q in bank["questions"] if q["level"] in ("country", "range")]
print("France page questions:", len(page), sorted(Counter(int(r["score"]) for r in page).items()))
