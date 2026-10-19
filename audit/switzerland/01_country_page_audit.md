# Switzerland country page: research and coverage audit

Date: 19 October 2026. Page: `projectsnow` branch `france-redesign`, `src/switzerland.njk`, built on the France template. Scores: `coverage.csv` (run `score.py`).

## Coverage against the question register

The 139 country and range questions were scored on the France scale (0 not answered, 1 passing mention, 2 partial, 3 useful and evidenced).

| Score | Switzerland | France |
|---|---|---|
| 3 | 33 | 40 |
| 2 | 53 | 51 |
| 1 | 29 | 28 |
| 0 | 24 | 20 |

Switzerland is stronger than France on rail access, luggage, glacier seasons, top against base altitude, measured piste lengths and tourist tax. It is weaker on accommodation prices and building stock, catered chalets, luxury, arrival days and changeover logistics.

## How the data was built

* **Ski areas:** 115 Swiss areas with 10 km of piste or more, from skiresort.com (measured piste lengths, lowest and highest points, main season adult day pass). Stored in `projectsnow/src/data/ch_resorts.json`. Closed areas excluded.
* **Ranges:** grouped by Snow Catchers into Pennine, Bernese, Uri Glarus and Lepontine (central), Rhaetian, Prealps and Jura. Cross border areas (Zermatt with Cervinia, Silvretta Arena, Portes du Soleil, La Dôle) are listed but not added to range totals.
* **Linked areas:** 15, each with its own page. Piste lengths are measured figures; operator claims are given where sourced.
* **Industry:** Seilbahnen Schweiz final report 2025/26 (25.7 million skier days, 38.5% foreign) and Fakten & Zahlen 2025 (54% snowmaking, 717 drag lifts, CHF 37.04 per skier day, CHF 77.50 average day pass).

## Price rules followed

No weekly accommodation price is published, because no source gives one with stated assumptions; the page says so. Prices shown are day passes (skiresort.com), summit restaurant prices (HolidayCheck, June 2025), one ski school price (Zermatters), tourist tax examples (Comparis 2024) and the Holidu index, each labelled with its source and date.

## Judgement calls to review

* The range grouping is ours. skiresort.com puts Leysin and Les Mosses in the Bernese Alps; we place them in the Prealps.
* Day pass averages per range use main season list prices; several large areas use dynamic pricing and show no price (Laax, St. Moritz, Adelboden-Lenk), so they are not in the averages.
* Zürich, Aargau and St. Gallen set sports holidays by municipality; the quiet windows assume they fall in February, as is usual.

## Gaps still open (priority order)

1. Measured weekly lodging prices by period, region and property size (AC19, AC20, CV05).
2. Catered chalets and UK operators in Switzerland (AC14).
3. Arrival days, minimum stays and changeover traffic, including the Saturday queues at the Gotthard and Lötschberg (AC22, DL04, TA09).
4. Transfer options and costs from Zürich and Geneva (TA10, TA11).
5. Snowpark list beyond Laax, tree skiing and bad weather options (SB05 to SB08, OP03, OP11).
6. English language ski school availability (FA05).
7. Accessible lodging and lifts (AC24, TA15).
