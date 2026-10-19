# France page inventory

Baseline: `projectsnow` branch `france-redesign`, commit `7641bd4`, as built to `docs/france/index.html` on 2026-10-19. The live page on `main` was not used as the baseline, by decision.

## Sections and their job

| Section | What it does now | Words (approx.) |
|---|---|---|
| Hero | Title, 56.1 million skier days, one paragraph of scene setting | 70 |
| Altitude decides the season | Explains base altitude as the main guide to snow; bar chart of 67 resorts in three altitude bands | 280 |
| Where the resorts join up | Defines a linked area; 19 linked areas grouped under six headings, each group with a short introduction | 1,050 |
| When to go | Two paragraphs plus four season windows (glaciers, high resorts, most of the Alps, low ranges) | 190 |
| Getting there | Airports, TGV, driving from Calais | 170 |
| Before you travel | Eight short facts: emergencies, rescue, insurance, winter driving, flying with skis, helmets, money, power | 220 |
| Sources and credits | Source links for place details, photo credits | n/a |

Also built: 19 stub domain pages at `/france/<slug>/` with resorts, piste length, sources. Total page text about 1,980 words; 37 links, 18 external.

## Material statistics and their sources

| Claim | Source | Status |
|---|---|---|
| 56.1 million skier days, 2025/26, more than any other country | Connexion, reporting Domaines Skiables de France | Found in `snowcatcher/research/countries/france.json`; news report of an industry body |
| Val Thorens at 2,300 m, highest resort in Europe | Val Thorens official site | Operator claim, stated as such |
| 31, 21 and 15 of 67 resorts in three altitude bands | `projectsnow/src/research/resorts/*.json` | Legacy unverified. Base altitude is defined inconsistently across files |
| 19 linked areas and their piste km | Alti Mag, France.fr, Skiresort, operators | Secondary sources, unconfirmed with operators. Portes du Soleil 650 km claimed against about 426 km measured |
| Vanoise Express 380 m above the ground, four minutes, 200 per cabin | Savoie Mont Blanc tourism | Sourced |
| Tignes dam 1952; Méribel from 1938 and its building rule; Avoriaz horses; Flaine 1969; Samoëns masons; Megève 1921; Sarenne 16 km and 2,000 m from 3,330 m; Risoul 300 days of sun; Pic du Midi 2,877 m, 15 minutes, 1,700 m descent; Comté cellars at 8°C | Linked on the page | Sourced. Risoul sunshine is a tourism claim |
| Season windows (glaciers November to May, and so on) | `projectsnow/src/research/country.json` | Legacy unverified |
| Airports serving each area | Editorial summary of legacy resort files | Unverified |
| TGV Paris to Moûtiers, Aime, Bourg-Saint-Maurice in about 4 to 4.5 hours | Old page copy | Unsourced |
| Calais to northern Alps 8 to 10 hours, Tarentaise 9 to 11, Pyrenees 10 to 12 | `country.json` | Legacy unverified |
| Carré Neige about €3.50 a day | `country.json`, 2025/26 pricing | Legacy unverified and possibly out of date for 2026/27 |
| Winter tyre or chains rule, 1 November to 31 March | `country.json` | Legacy unverified. Penalty status disputed in earlier research, so the fine was left out |
| Emergency numbers 112, 15, 17, 18, 114 | None on page | Unsourced but stable |

## Mountain ranges covered

The page groups areas under Savoie, Haute-Savoie, Isère, Southern Alps, Pyrenees and Jura. That mixes administrative departments with ranges, and the Northern Alps never appear as a range. The Vosges and the Massif Central are missing from the page entirely; the Grand Sancy was left out pending a decision on its conditional link. Corsica is not mentioned.

## Comparisons on the page

- Altitude bands: the only quantitative comparison, built on unverified data.
- Linked area size bars: compares piste km across 19 areas against the largest claimed figure.
- Season windows by altitude type.
- No comparison with Austria, Italy or Switzerland. No cost comparison. No comparison by traveller type.

## Visuals

Hero photograph (La Plagne); altitude band chart; 19 cards with 4 photographs and 15 drawn illustrations; no map.

## Problems found

1. The page tells rather than helps decide. It never answers why France, which range, or for whom.
2. Ranges are not the organising idea, and two ranges are missing.
3. Several figures come from legacy files that predate the verification rules.
4. Nothing on cost, which is one of the first things a traveller compares.
5. Nothing on snowboarders, families, mixed ability groups, solo travellers, couples or friends.
6. No map, so a reader cannot see where any of this is.
7. Domain stub pages are thin; by decision they stay as they are until the France page is finished.
8. Publishing gap: the site build does not commit its output, so CMS edits do not reach the live site.
