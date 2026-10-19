# Accommodation, restaurants and daily living: France page audit

Date: 19 October 2026. Baseline: live page at `projectsnow` commit `f3075b6`. Changes: branch `france-redesign`, section "Where to stay, and how to eat". Scores: `coverage_accommodation.csv`; all rows merged into `coverage_after.csv`.

## Register changes

37 questions added to `question_bank.py` (now 236), in five groups: accommodation AC13 to AC26, food and dining FD01 to FD07, daily living DL01 to DL05, resort type RT01 to RT05, traveller fit TI01 to TI06. Thirty belong on the France page; seven (AC17, AC26, FD05 to FD07, DL03, DL05, RT04) are resort or domain level and logged as dependencies. Related existing questions were rescored (AC01, AC03, AC12, CC06, CV05, AP08, AP09, GF07).

| Score, 30 new France page questions | Before | After |
|---|---|---|
| 3, useful and evidenced | 0 | 11 |
| 2, partial | 2 | 12 |
| 1, passing mention | 7 | 7 |
| 0, not answered | 21 | 0 |

Whole France page (139 questions): 40 score 3, 51 score 2, 28 score 1, 20 score 0. None scores 4.

## What the page now says, and the evidence

| Dimension | Country level finding | Source | Confidence |
|---|---|---|---|
| Resort types | Purpose built stations began with Courchevel (1948), which invented the front de neige; the Plan Neige created more than 20 resorts in 1964 to 1977. Village resorts grew around Chamonix and Megève. Hybrids such as La Plagne combine seven high sites (1,800 to 2,100 m, free shuttles) with three lower villages (1,250 to 1,350 m). | Alti-Mag; Skiinfo | Medium |
| Accommodation mix | Hotels, holiday villages and campsites under 4% of resort beds (MKG Hospitality, 2015). More than 80% of resort accommodation is second homes or holiday residences built over 30 years ago (Cour des comptes, 2024). Mountain holiday residences grew from 184 (1995) to 676 (2015), 264,190 beds. | Hospitality On; Cour des comptes | Medium; data is dated |
| Building stock | About half of homes in 70 resorts rated F or G for energy, against 16.9% nationally (Heero, 2022, cited by the Cour des comptes). | Cour des comptes | Medium |
| Catered chalets | Since Brexit, British seasonal staff are hard to employ; operators have shifted to hotels and self catering; fewer catered chalets, often dearer. | Iglu Ski | Medium; no counts |
| Luxury | All five palace distinction hotels in ski resorts are in Courchevel. | Alti-Mag | Medium |
| Prices | Illustrative only: Alti-Mag's 2025/26 estimates for a family of four (two adults, two children), one week: residence about €1,000 January or spring; about €1,500 mid size resort, February; about €2,500 well placed, large Alpine resort, February. Property size not stated. These are the author's estimates, not measured averages, and are labelled as such. | Alti-Mag, 13 October 2025 | Low |
| Extra charges | Tourist tax per adult per night, set by the commune: commune share €0.20 to €4.90 by category, or 1% to 5% of the nightly price for unclassified rentals; minors exempt. Cleaning, linen and towels not always included. | Legifiscal | High for the tax; medium for extras |
| Accessibility | Tourisme & Handicap label; more than 500 labelled sites in Auvergne-Rhône-Alpes; Serre Chevalier lists 39 lifts accessible to adapted skiers. | France Montagnes | Medium |
| Groceries | Sherpa: cooperative founded 1988, 119 shops in 97 resorts (Jura, Alps, Pyrenees). Pre-order and delivery to accommodation reported in 2014; flagged on the page as needing a current check. | Franchise Magazine 2024; AC Franchise 2014 | Medium; delivery low |
| Restaurant spend | Average bill per person per meal €29 in winter 2024/25 (from €27), 300,000 bills, Savoie €34, Haute-Savoie €31, Isère €28, Hautes-Alpes €23. | Sunday study via Tendance Hôtellerie | Medium; one payment app's partner restaurants |
| Food budget | Alti-Mag estimates for a family of four, one week: about €250 self catering with one simple meal out, to about €750 with several restaurant evenings. | Alti-Mag | Low; illustrative |
| Regional food | Savoie: fondue and raclette from Switzerland, tartiflette as a modern pela; Reblochon, Beaufort, diots, crozets, génépi. Jura: Comté, Morbier, Mont d'Or. Vosges: Munster. Massif Central: Saint-Nectaire, Cantal, Salers, Bleu d'Auvergne. Western Pyrenees: Ossau-Iraty. | Routard; AOP listings | High |
| Evenings and location | Bars concentrate at the front de neige in purpose built stations; satellite villages depend on the last shuttle or a taxi. | Alti-Mag (front de neige); pattern | Medium as a pattern |

## Price rules followed

No representative prices were invented. The only weekly accommodation figures on the page are Alti-Mag's estimates, shown with family size, period and resort type, and described as illustrations. Two other sources were rejected: SeLoger's February chalet prices (2020, no capacity, internal conflicts) and Skimetrics' averages (no method, undefined property types).

## Not assumed, needs local verification

Restaurant choice in any given resort; whether a resort has a supermarket, bakery or butcher open all season; shuttle routes and last departure times; Sherpa's current delivery service; the distance from any lodging to the lifts behind a "ski in ski out" claim; cleaning and linen charges; arrival days and minimum stays; accessible lodgings and lifts.

## Gaps still open (priority order)

1. Measured weekly prices by period, range and property size, for couples and groups as well as families (AC19, AC20, CV05).
2. Resort against valley grocery prices (DL01).
3. Restaurant counts and opening by resort type; mountain restaurant against village prices (FD01, FD02).
4. Arrival days, minimum stays and changeover logistics from operator terms (AC22, DL04).
5. Average floor area by advertised capacity (AC23).
6. Non skier suitability by resort type (TI05).

## Dependencies for resort and domain pages

AC17 (real distance to lifts), AC26 (pools and clubs), FD05 to FD07 (how mountain restaurants work, eating out nightly, special diets), DL03 (getting around), DL05 (pharmacies and doctors), RT04 (where the evening happens), plus the local checks above.
