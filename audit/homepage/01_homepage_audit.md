# Homepage audit

Date: 19 October 2026. Page: nicksc1cc.github.io/projectsnow, source `projectsnow/src/index.njk` with `src/_data/home.js`, `graphics.js`, `ranges.js`, `linked.js`, `photos.js` and the four country loaders. Rendered at 1300 px and 390 px and inspected.

## 1. Inventory

| # | Section | What it holds | Purpose | Helps the visitor progress? |
|---|---|---|---|---|
| 1 | Hero | "Know the mountain before you go", proposition paragraph, buttons "Explore France" and "How the guide works", Tignes photo | Explain the product | Partly. The proposition is clear, but the only primary action leads to France |
| 2 | Stats strip | 56.1m French skier days, 12,262 km French piste, 71% in the Northern Alps, 19 French linked areas | Credibility | Weakly. All four figures are French and none helps a choice |
| 3 | "One mountain, several holidays" | Two paragraphs on resort character, pull quote "Nobody is promised something for everyone" | Explain why the guide exists | Yes for the first paragraph. The pull quote repeats the hero |
| 4 | Layer strip | 1 Country, 6 ranges, 19 linked areas, 67 resorts, 246 villages | Explain the structure | Confusing. "1 Country" sits above "Four countries live", and every number is French |
| 5 | Photo break | Base altitude quote | Pacing | Repeats the France page |
| 6 | "What the data already shows" | French peaks chart, French base altitude bands | Show the data | No. France only, and the peaks chart links to `#range-…` anchors that do not exist on the homepage (six dead links) |
| 7 | "The lists we are scoring" | Six "Scoring in progress" cards: snowboarders, families, snow, value, mixed groups, après | Trip preference entry | Partly. It is the only place visitors can start from the trip they want, but every card links into France only, and the label promises rankings that do not exist |
| 8 | "The biggest linked areas in France" | Six French area cards | Show scale | Weakly. France only, and it duplicates the France page |
| 9 | Countries | Four cards: ranges, linked areas, areas in the data | Route to country guides | Yes, but they sit seventh of nine sections and say nothing about how the countries differ |
| 10 | "Skiing alone, travelling together" | Coming next: matching solo travellers into groups; "Start with France" button | Future product | Describes functionality that does not exist yet; repeats the France call to action |
| 11 | Footer | "Every figure links to the source it came from"; credits link | Trust | The homepage figures do not link to sources |

Rendered height: about 7,200 px on desktop and 13,200 px on mobile. No horizontal overflow at 390 px. The mobile nav wraps onto two lines.

## 2. Question coverage

Scores: 3 answered well, 2 partly, 1 touched, 0 not answered.

| Question | Score | Note |
|---|---|---|
| Can a visitor understand Snow Catchers in a few seconds? | 2 | Hero is clear; then repeated twice more |
| Is the value clear? | 2 | Checked figures and sources, but shown through France only |
| Meaningful discovery and comparison? | 0 | No comparison between countries anywhere |
| Differentiation credible and supported? | 2 | The sourcing is real; "scoring" and "matching" are not built |
| Claims trustworthy? | 2 | Figures are sourced on the country pages; footer claim of linked sources is not true on this page |
| Start with the holiday rather than the destination? | 1 | The six list cards, France only |
| Traveller types represented? | 2 | Snowboarders, families, mixed groups; couples, friends and solo only in the teaser |
| Priorities (budget, terrain, off piste, après, character, non skiing)? | 1 | Value, snow and après cards only |
| Simple entry without specialist knowledge? | 1 | Altitude charts assume interest in ranges |
| Four country guides presented clearly? | 1 | Present, but low on the page and in the nav only |
| Each country differentiated? | 0 | Cards show counts only |
| Trade offs between countries? | 0 | Not covered |
| Quick route into a known country? | 2 | Nav links work; no country links above the fold except France |
| Avoids repeating country content? | 0 | Sections 2, 5, 6 and 8 repeat the France page |
| What matters when choosing? | 2 | Section 3 and the list cards |
| Terrain, altitude, snow, cost, access, character? | 1 | Altitude and cost for France; access absent |
| Snowboard considerations? | 2 | One card |
| Big domains against small areas, stations against villages? | 2 | Section 3 explains it well |
| Comparisons evidenced? | 1 | Evidence exists in the country data but is not used here |
| Accommodation, food, après, non skiing? | 1 | One card and the teaser |
| Experience beyond the skiing? | 1 | Section 3 only |
| Non skiers and mixed groups? | 1 | Mixed groups card |
| Primary action clear? | 1 | Points to France only |
| Country pages easy to reach? | 2 | Nav and bottom cards |
| Mobile hierarchy? | 1 | Countries appear after about 11,000 px of scrolling |
| Repeated calls to action or dead ends? | 0 | "Explore France" and "Start with France" twice; six dead chart links |
| Prominent links lead to relevant content? | 2 | Apart from the chart anchors |

## 3. Prioritised gaps

1. **The homepage is a France page.** The hero action, statistics, charts, list links and featured areas all point to France, and the closing action repeats it. Three of the four guides are reachable only from the nav and the bottom cards. (Understanding, discovery, progression.)
2. **No comparison between countries.** Nothing tells a visitor what separates France, Switzerland, Austria and Italy, though the country research already holds the evidence: Vanat skier visits for all four from one source, Legambiente snowmaking shares for all four from one source, highest lifts, linked area counts, and the character of each country's resorts.
3. **The trip entry is France only and promises scores that do not exist.** The six list cards are the right idea but should route to all four guides and drop "Scoring in progress".
4. **Implied functionality.** "The lists we are scoring" and the solo matching teaser describe products that are not built.
5. **Six dead links** from the homepage peaks chart, and a footer claim that does not hold on this page.
6. **Repetition.** The proposition is stated three times, and sections 2, 5, 6 and 8 duplicate the France page.
7. **Countries come too late,** especially on mobile.
8. **Cosmetic:** "1 Country" in the layer strip, the meta description still says "starting with France".

## 4. Content jobs

| Job | Visitor question | On the page now? | Change |
|---|---|---|---|
| Proposition and primary action | What is this and where do I start? | Yes, France only | Keep the headline; the action leads to the country comparison |
| Entry by trip | I know the holiday, not the place | Partly (list cards) | Six priorities, each with where to look in all four guides |
| Four country overview | How do these countries differ? | No | One comparison, evidenced, with a line of character per country and a link into each guide |
| What distinguishes destinations | What should I weigh up? | Yes (section 3) | Keep, trim the repeated proposition |
| Resort character and wider experience | Village or station, huts or bars? | Partly | Fold into section 3 and the trip entry |
| Route into the guides | Take me to the detail | Late on the page | Covered by the comparison and the nav |

## 5. Measurement note

Piste totals are not comparable across countries yet: the France figure uses each area's declared kilometres, while Switzerland, Austria and Italy use skiresort.com's measured kilometres. A homepage comparison should not set them side by side without saying so.
