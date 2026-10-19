# France page: prioritised gap report

Baseline: `projectsnow` branch `france-redesign`, commit `7641bd4`. Full scores are in `coverage.csv` (199 questions, one row each).

## Where the page stands

Of the 199 traveller questions, 110 belong on the France page (country or range level). The other 89 belong on domain, resort or village pages and are recorded as dependencies.

| Score | France page questions |
|---|---|
| 4, strong comparative answer | 0 |
| 3, useful and evidenced | 1 (where the linked areas are) |
| 2, partial | 8 |
| 1, passing mention | 34 |
| 0, not answered | 67 |

The page describes France well in places and explains one idea, altitude, with some care. It does not yet help anyone decide whether France suits them, which range to pick, or what the trip will cost. Every comparison it makes is internal to France, and most of its figures rest on files that predate the verification rules.

## The gaps, grouped into page additions

Ranked by decision impact, then by how many travellers each helps, how distinctive the answer would be, and whether the evidence exists. Each one is a section or a component, not a heading per question.

### 1. The ranges, side by side
**Questions:** RG01 to RG17, TR02 to TR05, SN01, SN07, SN08, SN11, NS01, NS03, TA01 to TA04 (31 questions; 27 score 0 or 1).
**Why it matters:** choosing a range is the decision the France page is uniquely placed to help with, and it changes everything downstream: snow, cost, journey, atmosphere.
**What to build:** a map of France's ski ranges and a comparison across the same dimensions for each: Northern Alps (with the Tarentaise, Maurienne, Haute-Savoie and Isère as sub areas), Southern Alps, Pyrenees, Jura, Vosges and Massif Central. Dimensions: scale of skiing, altitude spread, typical season, resort character, journey from the UK, relative cost, and who each range suits. The 19 linked areas stay, regrouped under their ranges. The Vosges and Massif Central are added.
**Evidence:** good. France Montagnes and Domaines Skiables de France publish range level figures; resort counts and altitudes can be compiled from operators.
**Uncertain:** range level averages hide large differences within a range. The text must say so.

### 2. Why France, and when not
**Questions:** CC01 to CC09, CV02, CV03 (11 questions; 9 score 0, none above 1).
**Why it matters:** the first decision a traveller makes. A page that never says what France does differently, or when Austria, Italy or Switzerland would suit better, cannot be trusted on anything else.
**What to build:** a short comparative section with a table on consistent measures: size of the largest linked areas, share of skiing above 1,800 m, typical six day pass price, resort type mix, and journey from the UK. Then a plain account of where another country is the better choice.
**Evidence:** mixed. Area sizes and pass prices are checkable; claims about atmosphere or apres across countries are easy to make and hard to support, so they stay out unless sourced.
**Uncertain:** cross country price comparisons need the same season and the same pass type.

### 3. What a week costs
**Questions:** CV01 to CV09, CC05, CC06, FA12, TA11 (13 questions; all score 0).
**Why it matters:** cost is the second filter after snow for most travellers, and the page says nothing about it.
**What to build:** a worked cost model with stated assumptions for a week: lift pass by area size, rental, lessons, food, getting there, accommodation type. Show it for a small area, a mid size resort and a large linked area, so the trade off in question CV08 becomes visible.
**Evidence:** 2026/27 pass prices are being published now; rental and lesson prices can be sampled from operators. UK cost surveys are useful only where their method is stated.
**Uncertain:** accommodation varies too much to give one figure; use ranges and say what drives them.

### 4. Who France suits, and where to look
**Questions:** CC03, CC04, CC08, AB09, AB10, FA01, FA02, FA05, FA14, FA15, SB01, SB05 to SB08, SO01, GF07, OP01 to OP04, OP07, OP14, AP01, AP03, AP05, AP06, AP12, NS07, PR10 (30 questions; 29 score 0).
**Why it matters:** the same area can be ideal for one group and wrong for another. This is where the page explains trade offs rather than ranking places.
**What to build:** a guide by traveller: first timers, improving intermediates, experts and freeriders, snowboarders, families with young children, families with teenagers, mixed ability groups, solo travellers, couples, friends, and groups with non skiers. Each says what matters for them, how France performs, which ranges or resort types to look at, and what to watch for. Snowboarders get their own treatment: drag lifts, flat links, parks, trees.
**Evidence:** variable. Famille Plus criteria and member resorts, French piste grading rules, park listings and drag lift shares are checkable. Lived experience from reviews needs dates, sample sizes and limits.
**Uncertain:** much of the real answer is resort level; this section gives the rule of thumb and points to the next page.

### 5. When to go, properly
**Questions:** TR01, TR06 to TR09 (5 questions; scores 0 to 2).
**What to build:** the 2026/27 French school holiday zones against UK half term and Easter, what each period does to prices and crowds, and early and late season by range.
**Evidence:** good. Zone dates are published by the French government.

### 6. Getting there, by range
**Questions:** TA05 to TA10, TA12 to TA15 plus the range rows above (10 more; scores 0 to 2).
**What to build:** for each range, the nearest airports with typical transfer times, rail options including any direct winter services from the UK, the drive with tolls and Saturday traffic, and which resorts work without a car.
**Evidence:** good from operators and timetables.

### 7. Snow and climate, beyond altitude
**Questions:** SN02 to SN06, SN09, SN10 (7 questions; mostly 0).
**What to build:** extend the altitude section with aspect, the difference between a high resort and a high ski area, snowmaking, how seasons have changed and what the evidence says about the future. Every figure dated and sourced.
**Evidence:** good for history (Meteo France and peer reviewed studies), weaker for projections, which must be presented as projections.

### 8. Off piste and safety
**Questions:** OP07, OP10 to OP12, PR05 to PR07 (7 questions; scores 0 to 2).
**What to build:** what off piste means in France (unpatrolled, at the skier's own risk), how altitude and aspect shape conditions, what to do on poor visibility days, the avalanche bulletin, guides, insurance and rescue costs. Stable information only; nothing implying conditions are safe.

### 9. Beyond skiing
**Questions:** NS02 to NS04, NS09, RG15, AP08, AP09 (7 questions; scores 0 or 1).
**What to build:** Nordic skiing, snowshoeing, thermal spa towns in the mountains, villages, food, and how purpose built stations and old villages feel different in the evening, by range.

### 10. First time in France
**Questions:** PR08, AC01, AC03, AC12, PR03, PR09 and the access items PR01, PR02 at pointer level.
**What to build:** the words and systems that confuse first timers (ESF, forfait, domaine, liaison), how passes and lessons are bought, accessibility labels, and the practical facts already on the page.

## Figures to verify before any of this is built on

| Figure | Problem |
|---|---|
| Resort base altitudes (all 67) | Legacy files, base altitude defined inconsistently |
| Season windows | Legacy country file |
| Airport list | Summary of legacy resort files |
| TGV journey times | Unsourced |
| Calais driving times and tolls | Legacy country file |
| Carré Neige price | 2025/26 price; needs 2026/27 |
| Linked area piste km | Secondary sources; confirm with operators |

## Dependencies for lower level pages

89 questions belong on domain, resort or village pages, for example flat sections for snowboarders (SB02, SB03), nursery slope layout (FA03), late bars (AP02) and lockers (AC10). They are recorded in `coverage.csv` with action type `later` and will seed the domain and resort audits.

## Proposed order for checkpoint 2

1. Verify the legacy figures above.
2. Build item 1 (ranges) and item 2 (why France), since every other section refers back to them.
3. Items 3 and 4 (cost and travellers).
4. Items 5 to 10, which mostly extend sections that already exist.
5. Rescore every question, check the rendered page on desktop and mobile, and write the QA report.
