# Italy country page: research and coverage audit

Date: 19 October 2026. Page: `projectsnow` branch `france-redesign`, `src/italy.njk`, built on the shared country template. Scores: `coverage.csv` (run `score.py`).

## Coverage against the question register

| Score | Italy | Austria | Switzerland | France |
|---|---|---|---|---|
| 3 | 23 | 38 | 33 | 40 |
| 2 | 43 | 42 | 53 | 51 |
| 1 | 36 | 35 | 29 | 28 |
| 0 | 37 | 24 | 24 | 20 |

Italy is strongest on ranges and linked areas, snowmaking, Dolomiti Superski prices, school holidays by region, piste law (helmets, insurance, alcohol), rescue charges, avalanche data and winter driving. It is the weakest of the four pages so far, mainly on accommodation mix, closing dates, trains, après, food prices and photography.

## How the data was built

* **Ski areas:** 108 Italian areas with 10 km of piste or more, from skiresort.com regional listings (measured piste lengths, lowest and highest points, main season adult day pass). Stored in `projectsnow/src/data/it_resorts.json`. Closed areas excluded (Chiomonte, Argentera, Bagolino, San Simone, Prato Selva, Pratospilla, Valbella, Selvarotonda).
* **Ranges:** grouped by Snow Catchers into seven: Maritime and Cottian Alps; Graian and Pennine Alps; Rhaetian, Ortler and Adamello Alps; South Tyrol's Central Alps; Dolomites; Carnic and Julian Alps; Apennines and Etna. Four cross border areas (Via Lattea, Cervinia with Zermatt, Espace San Bernardo, Sella Nevea with Kanin) are listed but not added to range totals.
* **Linked areas:** 17, each with its own page. The Sella Ronda figure is the sum of its four areas as measured separately.
* **Industry:** Vanat via SnowBrains (34.1 million skier visits in 2024/25, up 6.6%), Legambiente Nevediversa 2023 via QuiFinanza (90% snowmaking, 249 abandoned installations), JFC via Il Nordest (2025/26 forecast).

## Price rules followed

The JFC week prices (€700 to €1,200 a person in a three star hotel with pass) are shown with the caveat that the study states no assumptions. Day passes come from skiresort.com, BusinessOnline (2026/27), Il Dolomiti (Dolomiti Superski) and Altroconsumo via SiViaggia.

## Judgement calls to review

* The range grouping is ours. Lombardy's Prealps sit with the Rhaetian, Ortler and Adamello Alps, and Etna sits with the Apennines.
* Val Gardena and the Alpe di Siusi have no listed single area price, so they are left out of the range average.
* Closing dates for 2026/27 are not yet published, so the calendar shows opening dates with fading bars rather than invented end dates.
* Photographs are not yet sourced. Wikimedia Commons could not be reached in this session, so drawn mountains stand in, apart from three photos reused from the France and Switzerland pages for the shared areas.

## Gaps still open (priority order)

1. Licensed photographs for the hero, the seven range banners, the section breaks and the linked area cards.
2. Closing dates for 2026/27 (TR01, TR03).
3. Accommodation mix and measured lodging prices (AC13, AC19, AC20, CV05).
4. Trains and onward travel (RG13, TA04, TA05).
5. Après, food and hut prices (AP01, AP05, FD02).
6. Piste grading, family schemes and lessons in English (AB09, FA05, FA15).
