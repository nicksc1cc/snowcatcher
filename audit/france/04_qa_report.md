# France page: checkpoint 2 QA report

Page: `projectsnow` branch `france-redesign`. Scores before and after are in `coverage_after.csv`.

## Coverage

| Score | Before | After |
|---|---|---|
| 3, useful and evidenced | 1 | 25 |
| 2, partial | 8 | 38 |
| 1, passing mention | 34 | 25 |
| 0, not answered | 67 | 22 |

110 questions belong on the France page. No question scores 4 yet: the range comparison is sourced to one database, and several answers still lean on legacy figures.

## What changed

- **What sets French skiing apart:** scale, altitude and the spread from giants to small areas, with the trade off between purpose built resorts and villages. No country comparison, by decision.
- **Altitude section:** now includes the Météo-France finding on lost snow cover (1971 to 2019) and the share of pistes with snowmaking.
- **Six ranges:** map, comparison table (ski areas, piste km, highest lifts, average six day pass) and a panel for each range saying what it is like, who it suits, what to watch for and how to get there. The Vosges and Massif Central are new. The 19 linked areas now sit under their ranges.
- **What a week costs:** pass prices for nine areas with cost per km, why that matters for beginners, ESF lesson prices, and where visitor spending goes.
- **Who France suits:** nine traveller types with what to look for and what catches them out.
- **When to go:** 2026/27 French zones against UK half term and Easter, the 15 February pinch point and the quiet windows.
- **Off piste and avalanche safety**, and **Beyond downhill** (cross country networks, lifts for non skiers).
- **First time in France:** adds the words a first timer meets.

## Corrections made against sources

| Was | Now | Source |
|---|---|---|
| TGV Paris to Bourg-Saint-Maurice in about 4 to 4.5 hours | About 5 hours 40 minutes, plus the Saturday Eurostar ski train | OUIGO; Seat61 |
| Carré Neige about €3.50 a day (2025/26 legacy) | A few euros a day, sold at lift offices; no current published rate found | Carré Neige; a 2022/23 resort tariff showed €3.10 |
| Unsupported claim that the Jura and Vosges have some of Europe's best cross country | France's three largest networks are in the Jura | Alti-Mag |
| Several superlatives in drafts (Pyrenees strongest growth, celebrated terrain) | Removed or reworded to what the source says | La Vie Economique; INC |

## Verified in this pass

Every new figure was checked against the page it came from: range counts, piste km and pass averages (Alti-Mag, with sample sizes shown), top lift heights, the nine pass prices, ESF prices, spending shares, the snowmaking share, the Météo-France snow finding, school holiday dates, the Eurostar and OUIGO timetables, Famille Plus criteria, piste colour gradients and the avalanche guidance.

Text checks on the built page: no em dashes; no hyphenated compounds outside place names; 4,500 words. All internal links and anchors resolve. External links come from sources fetched during research; they were not re-requested from the build environment, which cannot reach outside sites.

Rendered checks: desktop at 1300 px and mobile at 390 px were inspected as screenshots. The comparison table scrolls sideways on narrow phones. Fonts render as fallbacks in the test environment; the live site loads Barlow Condensed and Source Serif.

## Still unverified on the page

- Resort base altitudes behind the altitude bands (legacy files, inconsistent definitions)
- Season windows by altitude type (legacy country file)
- Calais driving times (legacy country file)
- Linked area piste km (secondary sources)
- Range level counts come from one database built from a guide; they may undercount small areas

## Remaining gaps on the France page (score 0 or 1)

- **Snowboarders:** drag lift share, flat links, parks and tree riding need resort level evidence before any range level statement (CC04, SB01, SB05 to SB08).
- **Accommodation:** types and costs, self catering against chalets and hotels, group properties (CC06, CV05, AC01).
- **Journey costs and logistics:** transfers, tolls, Saturday traffic, small group transfers, skis on trains, limited mobility (CV07, TA09 to TA11, TA14, TA15).
- **Atmosphere:** après, nightlife and food by range (RG09, AP01 to AP12). The evidence is mostly reviews and needs dated, sized samples.
- **Snow detail:** aspect, high resort against high ski area, wind and storms by range, future projections (SN02, SN05, SN07, SN10).
- **Off piste detail:** tree skiing, steep terrain, what makes an expert resort (OP03, OP04, OP11, OP14).
- **Other:** English lessons (FA05), family total costs (FA12), spas (NS03), pets (PR09).

## Dependencies for lower level pages

89 questions belong on domain, resort or village pages and are unchanged; see `coverage.csv`, action type `later`.
