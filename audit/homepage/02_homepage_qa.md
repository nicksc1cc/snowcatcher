# Homepage changes and QA

Date: 19 October 2026. Branch `france-redesign`. Only `src/index.njk`, the homepage styles in `src/assets/france.css` and two homepage only conditions in the shared layout footer changed. The four country pages build byte identical.

## Changes

| Gap (from 01) | Change |
|---|---|
| 1. Homepage is a France page | Hero action now "Compare the four countries"; second link "Start from the trip". French statistics strip, French charts, base altitude break and "Start with France" removed |
| 2. No country comparison | "Where the four countries differ" moved to second place: one line of character per country and four figures on the same basis (Vanat skier visits 2024/25, Legambiente snowmaking 2023, highest lifts, linked areas in the guide), with sources and caveats |
| 3. Trip entry France only | "Start from the trip": six priorities (snowboarding, families, snow, value, steep and off piste, evenings and non skiers), each linking to the matching section of all four guides |
| 4. Implied functionality | "Scoring in progress" labels and the solo matching teaser removed |
| 5. Dead links, footer claim | Six dead chart links gone with the chart; footer on the homepage now says figures are sourced in the country guides; credits link points to a homepage credit line |
| 6. Repetition | Pull quote and repeated proposition removed |
| 7. Countries too late | Comparison starts at about 900 px on desktop and mobile (was about 6,000 px and 11,000 px) |
| 8. Cosmetic | Layer strip shows 4 countries, 26 ranges, 79 linked areas; resort and village counts labelled "France first"; meta description names all four countries |

Linked areas section now shows the largest area wholly inside each country (Les 3 Vallées, 4 Vallées, Ski Arlberg, Sella Ronda), with a note that France's figure is declared and the others measured.

## Verification

* All 34 links on the rendered page return 200, and every anchor exists on its target page.
* Main action scrolls to the comparison; secondary action to the trip section.
* Text check: no em dashes, no lowercase hyphenated compounds, no "undefined" or "NaN", no scoring or matching claims.
* Desktop 1300 px: page height down from about 7,200 px to 4,800 px. Mobile 390 px: no horizontal overflow, height down from about 13,200 px to 10,400 px.
* Every claim on the page traces to a country guide or to the two linked sources.

## Outstanding

* Italy has no photographs yet, so its country card and the Sella Ronda card use drawn mountains.
* The Les 3 Vallées photo credit on the France page names no author ("Wikimedia Commons, CC BY-SA"); the homepage repeats it.
* Piste totals are not comparable across countries (declared for France, measured elsewhere), so the comparison leaves them out.
* Resort and village layers exist for France only.
