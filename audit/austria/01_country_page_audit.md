# Austria country page: research and coverage audit

Date: 19 October 2026. Page: `projectsnow` branch `france-redesign`, `src/austria.njk`, built on the shared country template. Scores: `coverage.csv` (run `score.py`).

## Coverage against the question register

| Score | Austria | Switzerland | France |
|---|---|---|---|
| 3 | 38 | 33 | 40 |
| 2 | 42 | 53 | 51 |
| 1 | 35 | 29 | 28 |
| 0 | 24 | 24 | 20 |

Austria is strongest on snowmaking, glaciers and opening dates, the hut and après culture, hut prices, accommodation mix, tourist tax, night trains, winter driving law and avalanche data. It is weakest on lodging prices, ski school and rental prices, transfers, accessibility and a national family label, which Austria does not have.

## How the data was built

* **Ski areas:** 139 Austrian areas with 10 km of piste or more, from skiresort.com state listings (measured piste lengths, lowest and highest points, main season adult day pass). Stored in `projectsnow/src/data/at_resorts.json`. Closed areas and Hochficht, in the Bohemian Forest, are excluded.
* **Ranges:** grouped by Snow Catchers into seven: Northern Limestone Alps; Silvretta, Rätikon and Samnaun Alps; Ötztal and Stubai Alps; Zillertal and Tux Alps; Kitzbühel Alps (with the Salzburg slate hills); Hohe and Niedere Tauern; Southern and Eastern Alps. Four cross border areas (Silvretta Arena, Steinplatte, Fellhorn and Kanzelwand, Nassfeld) are listed but not added to range totals.
* **Linked areas:** 28, each with its own page.
* **Industry:** WKO cableway association (about 54 million skier days in 2025/26, up about 4%; 75% snowmaking; 1,111 cableways and about 1,415 drag lifts), Statistik Austria via ORF (74.2 million winter overnights), Land Salzburg (overnights by accommodation type).

## Price rules followed

No weekly accommodation price is published, because no source gives one with stated assumptions. Prices shown: day passes (skiresort.com), hut prices (AK Salzburg survey, January 2024), the Holidu index, vignette and tolls (Austria Tourism), tourist tax range (Land Tirol).

## Judgement calls to review

* The range grouping is ours, and the Southern and Eastern Alps group joins the Nock Mountains, the Carnic Alps and the eastern hills near Vienna for practical reasons.
* The quiet windows count Austrian, German, Dutch and English holidays. Baden-Württemberg schools set their own carnival dates.
* skiresort.com's Tyrol listing could only be read in part; a handful of small Tyrolean areas between 10 and 22 km may be missing.

## Gaps still open (priority order)

1. Measured weekly lodging prices, including half board (AC19, AC20, CV05).
2. Ski school and rental prices (CV06, FA12).
3. Transfer options and costs from Innsbruck, Salzburg and Munich (TA10, TA11).
4. Arrival days and Saturday traffic on the Inntal and Tauern motorways (AC22, TA09).
5. Accessibility and adaptive skiing (AC24, TA15).
6. Austrian snow trend research to match the SLF and Météo-France studies (SN10).
