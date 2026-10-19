"""Coverage scores for the France page against the traveller question bank.

Baseline: projectsnow branch france-redesign, commit 7641bd4 (2026-10-19).
Score: 0 none, 1 passing or unsupported, 2 partial, 3 useful with evidence and implication,
4 strong comparative answer with trade offs and links.
Confidence is about the evidence behind whatever the page says, kept separate from score.

Run: python3 audit/france/score.py -> writes coverage.json and coverage.csv beside this file.
"""
import csv, json, os, sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, ".."))
from question_bank import build

PRIORITY = {  # brief's order: comparison, economics, suitability, snow and terrain, atmosphere, practical
    "Country choice": 1, "Ranges": 1,
    "Cost": 2, "Timing": 2, "Transport": 2,
    "Ability": 3, "Families": 3, "Snowboarders": 3, "Mixed groups": 3, "Piste skiers": 3,
    "Solo travellers": 3, "Couples": 3, "Friends": 3,
    "Snow": 4, "Off piste": 4, "Beyond downhill": 4,
    "Atmosphere": 5,
    "Accommodation": 6, "Practical": 6,
}

RESEARCH = {
    "Country choice": "Cross country comparison: domain sizes, altitude profiles, pass and holiday costs for France, Austria, Italy, Switzerland from consistent sources (DSF, national bodies, operator price lists, UK operator cost surveys).",
    "Ranges": "France Montagnes and DSF range level data; resort and domain counts, altitude spread, piste km by range; access times; Nordic networks.",
    "Cost": "2026/27 published adult six day pass prices for a sample across ranges and sizes; rental, lesson and meal price samples; UK cost of skiing surveys with stated method.",
    "Timing": "French school holiday zones for 2026/27; published opening and closing dates by resort; historical opening data where it exists.",
    "Transport": "Airport and rail operator timetables; transfer times from operators; SNCF and Eurostar winter services; toll and fuel costs.",
    "Ability": "Piste grading rules in France (green to black, Norme NF S52-100 if applicable); operator piste maps for terrain share by level.",
    "Families": "Famille Plus label criteria and member resorts; ESF and ESI English lesson provision; childcare age limits.",
    "Snowboarders": "Operator lift lists (drag lift share), park listings; snowboard press and forum themes with dates and sample sizes.",
    "Mixed groups": "Domain level research; at country level only a generalisation if evidence supports it.",
    "Piste skiers": "Operator piste maps and run lengths; at country level only the defining examples.",
    "Solo travellers": "Operator social and group lesson offers; car free resort list; review themes.",
    "Couples": "Resort level research.",
    "Friends": "Apres and nightlife evidence by resort; group accommodation supply.",
    "Snow": "Meteo France or academic snow cover studies by range and altitude; snowmaking coverage (DSF); dated and time bounded.",
    "Off piste": "Guide bureaus (Compagnie des Guides), Meteo France avalanche bulletin, ANENA; freeride terrain by range.",
    "Beyond downhill": "Nordic France network data; thermal spa towns in mountain ranges; non ski activity listings.",
    "Atmosphere": "Review and press themes with dates; resort level evidence.",
    "Accommodation": "Range level patterns from tourism bodies; resort level for specifics.",
    "Practical": "Official safety, medical and accessibility sources (Handiski, Tourisme et Handicap label); insurance terms.",
}

# id: (score, confidence, evidence on page)
SCORED = {
    "CC02": (1, "low", "'Where the resorts join up' calls the linked area a French speciality, citing France.fr. No comparison with other countries."),
    "CC07": (1, "medium", "Hero and Savoie intro mention farming villages and 1960s resorts; no explanation of what the difference means for a trip."),
    "TR01": (2, "low", "'When to go' season windows. Legacy unverified data; no dates by range."),
    "TR02": (1, "low", "Season card names high resorts and glaciers for late November opening."),
    "TR03": (1, "low", "Glacier card mentions May; no guidance on where to look."),
    "TR04": (1, "low", "Altitude section explains altitude; Southern Alps intro mentions sun. Nothing compares ranges."),
    "TR05": (1, "low", "Altitude section: below 1,300 m a mild spell softens runs. Not by range."),
    "TR06": (1, "medium", "February busiest, French zones overlap UK half term. No price effect, no Christmas or Easter detail."),
    "TR07": (1, "low", "January after New Year described as usually quiet. Unsourced; no price claim."),
    "TR09": (2, "low", "Altitude section argues base altitude is the best single guide, with band chart. No snowfall or depth data."),
    "RG01": (1, "medium", "Areas grouped under Savoie, Haute-Savoie, Isère, Southern Alps, Pyrenees, Jura. Mixes departments with ranges; Vosges and Massif Central missing; no map."),
    "RG02": (1, "medium", "Southern Alps intro: light changes, Risoul sunshine claim. One sided."),
    "RG03": (1, "medium", "Pyrenees intro: smaller in scale, wilder. No practical comparison."),
    "RG04": (1, "medium", "Jura intro: more cross country than downhill. Other ranges not characterised this way."),
    "RG05": (1, "low", "Savoie intro and altitude section name high resorts. Not compared by range."),
    "RG06": (3, "low", "19 linked areas with size bars, grouped by area, with what links them. Figures unconfirmed with operators."),
    "RG08": (1, "medium", "Savoie and Haute-Savoie intros contrast purpose built and village. Not mapped across ranges."),
    "RG12": (1, "low", "'Getting there': Geneva for most of the northern Alps."),
    "RG13": (1, "low", "'Getting there': TGV to the Tarentaise. Unsourced."),
    "RG15": (1, "medium", "Comté cellars, Pic du Midi, Flaine art, Samoëns heritage mentioned in passing."),
    "RG16": (1, "medium", "Jura described as quiet; Pyrenees as wilder. No guidance."),
    "RG17": (1, "low", "Altitude section implies the snow trade off. No mention of scale, cost or crowd trade offs."),
    "SK01": (1, "medium", "Sarenne 16 km and 2,000 m named. One example only."),
    "SK03": (1, "low", "Linked area sizes imply variety. No guidance on how much a week needs."),
    "OP01": (1, "medium", "Pic du Midi freeride descent mentioned. Nothing else."),
    "OP12": (1, "medium", "'Before you travel': PGHM and CRS rescue, rescue charged. No avalanche bulletin or guiding."),
    "AP08": (1, "medium", "Implied through Méribel, Avoriaz, Flaine stories. Not stated."),
    "AP09": (1, "medium", "Comté in the Jura only."),
    "TA02": (2, "low", "'Getting there': Geneva, Lyon, Chambéry, Grenoble, Turin, by area. Unverified, no transfer times."),
    "TA04": (2, "low", "'Getting there': TGV to Moûtiers, Aime, Bourg-Saint-Maurice, onward by bus or taxi. Unsourced times."),
    "TA08": (2, "low", "'Before you travel': winter tyres or chains, 1 November to 31 March, signed zones, hire car note."),
    "TA14": (1, "low", "'Flying with skis': book skis with the flight. Nothing on trains or buses."),
    "TA01": (1, "low", "Driving times from Calais and Geneva gateway. No comparison by range."),
    "AC03": (1, "medium", "Implied by village stories. Not addressed for accommodation."),
    "SN01": (2, "low", "Altitude section with band chart. Bands drawn from legacy resort altitudes; not split by range."),
    "SN04": (1, "low", "Below 1,300 m the season leans on snowmaking. No coverage data."),
    "SN06": (1, "low", "Altitude section: lower runs soften in a mild spell."),
    "SN08": (1, "low", "Glaciers keep skiing going after lower slopes close."),
    "SN11": (1, "low", "Southern Alps sunshine versus altitude, implied only."),
    "NS01": (1, "medium", "Jura and Vercors cross country mentioned."),
    "NS04": (1, "medium", "Samoëns, Megève, Flaine art mentioned."),
    "NS06": (1, "medium", "Pic du Midi cable car from La Mongie."),
    "NS09": (1, "low", "Nothing beyond the Jura fort."),
    "PR03": (1, "medium", "Emergency numbers listed."),
    "PR05": (2, "low", "Carré Neige at about €3.50 a day; rescue is charged. Price is 2025/26 legacy data."),
    "PR06": (2, "medium", "Patrollers on piste, PGHM and CRS off piste, rescue charged."),
    "AB08": (1, "low", "Helmets note mentions ski schools only in passing."),
    "FA05": (0, "none", ""),
}

def action(q, score):
    lvl = q["level"]
    if lvl in ("domain", "resort", "village"):
        return ("Dependency for %s pages. France gives a range level pointer only if evidence supports one." % lvl, "later")
    if score >= 3:
        return ("Keep; confirm figures with operators.", "verify")
    if score == 2:
        return ("Strengthen with sourced, comparative detail.", "improve")
    return ("Research and answer on the France page.", "add")

def main():
    bank = build()
    rows = []
    for q in bank["questions"]:
        s, conf, ev = SCORED.get(q["id"], (0, "none", ""))
        act, kind = action(q, s)
        on_page = q["level"] in ("country", "range")
        rows.append({
            "id": q["id"], "category": q["category"], "question": q["template"].format(country="France"),
            "audience": q["audience"], "dimension": q["dimension"], "level": q["level"],
            "score": s, "confidence": conf, "evidence": ev,
            "research": RESEARCH[q["category"]] if kind != "verify" else "Operator confirmation of each area's piste km.",
            "priority": PRIORITY[q["category"]] if on_page else 9,
            "action": act, "action_type": kind,
        })
    json.dump({"baseline": "projectsnow france-redesign 7641bd4, 2026-10-19", "rows": rows},
              open(os.path.join(HERE, "coverage.json"), "w"), indent=1, ensure_ascii=False)
    with open(os.path.join(HERE, "coverage.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    from collections import Counter
    print("rows", len(rows))
    print("scores", sorted(Counter(r["score"] for r in rows).items()))
    print("france page rows", sum(r["level"] in ("country", "range") for r in rows))
    print("france page scores", sorted(Counter(r["score"] for r in rows if r["level"] in ("country","range")).items()))
    print("actions", Counter(r["action_type"] for r in rows))

if __name__ == "__main__":
    main()
