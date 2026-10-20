# Page architecture, internal links and visualisation plan

Deliverables 12 and 13. This is a plan for the eventual linked domain page; no public copy is written yet.

## 1. Proposed page order

| # | Section | Visitor question | Main evidence | Status of evidence |
|---|---|---|---|---|
| 1 | Overview | What is the Portes du Soleil and how big is it really? | Official and measured size side by side; 12 resorts; two countries | Ready, conflicts noted |
| 2 | Network map | How does it fit together? | Graph with sectors, lifts, link runs, village crossings and pass only resorts | Model built; needs map check |
| 3 | How the network works | Can I get from here to there, and what can stop me? | Two network split at Morzine; critical lifts; one way and no ski home bases; minimum lift counts | Model built; needs map check |
| 4 | Sector comparison | Which part suits me? | Sector matrix: heights, piste mix, drag lift share, links | Model built; needs official piste km by sector |
| 5 | Snow and weather | How reliable is the snow, and what is it like this week? | ERA5 history by height (labelled modelled); later ERA5-Land and stations; forecast panel; avalanche bulletins | History started; current pipeline designed |
| 6 | Terrain and character | Where are the long cruises, steeps, parks and trees? | Longest and steepest runs; parks; tree line | Partial |
| 7 | Pass value | Do I need the full pass? | Local versus full pass prices; lifts needed to reach the other side from each base | Partial (Avoriaz and Châtel local prices missing) |
| 8 | Where to stay | Which base gives the domain I want? | Base access table; ski home; hubs versus edges | Model built |
| 9 | Who it suits | Is it right for my group? | Traveller evidence table; links needing red runs; drag lifts | Early |
| 10 | Food, après, non skiing | What else is there? | Domain patterns; pedestrian passes; indoor options | Early |
| 11 | Getting around | How do I get there and between bases? | Geneva transfers, rail, ski buses, village crossings | Not started |
| 12 | Trade offs | What are the catches? | Morzine crossing, Super-Morzine dependency, low village returns, drag lifts, distance from Les Gets to the north | Evidence building |
| 13 | Research notes | How was this checked, and when? | Sources, dates, data types, conflicts | Ready |

Sections 2, 3 and 8 may combine into one interactive map with a base selector if that reads better on mobile.

## 2. Internal links

* **Up:** to the France and Switzerland country pages at the "Northern Alps" and "Chablais" range sections.
* **Across:** to other linked domains that share pass partner days (4 Vallées, Espace San Bernardo, Via Lattea) only where the partner days are mentioned.
* **Down:** to future resort pages for Avoriaz, Morzine, Les Gets, Châtel, Champéry, Morgins, Champoussin, Les Crosets, Torgon, La Chapelle d'Abondance, Abondance and Saint-Jean-d'Aulps; and to village pages (Les Lindarets, Ardent, Pré la Joux, Plaine Dranse) when they exist. Hotel, restaurant and ski school detail stays on those pages.
* **No repetition:** the domain page links to resort pages for anything about staying in one place; resort pages link back to the domain page for anything about crossing the network.

## 3. Visualisation plan

| Visual | Shows | Data | Mobile treatment |
|---|---|---|---|
| Network map | Sectors as areas, lifts as lines, link runs coloured by easiest colour, village crossings dashed, pass only resorts greyed with bus links | `network_graph.json`, OpenStreetMap geometry (with attribution) | Pan and zoom map with a list view fallback; tap a sector for its card |
| Base selector | Lift rides from a chosen base to each area, as a ring or bar chart | `base_access.csv` | Simple ranked list |
| Critical lift chart | Lifts ranked by routes lost if closed | `network_graph.json` | Top five as a list |
| Sector comparison | Small multiples: lift base and top height, piste colour split, drag lift share | `sector_matrix.csv` | Swipeable cards, one sector each |
| Snow by height | Seasonal snowfall at 1,100, 1,600 and 2,100 m, 1950 to 2026, with the 1991 to 2020 band shaded | `snow_era5_seasons.csv` | One height at a time with a toggle |
| Snow through the season | Median weekly snowfall by height | `snow_era5_weekly_median_1991_2020.csv` | Single line chart |
| Rain at low level | December to March rain at 1,100 m against 1,600 m | `snow_era5_seasons.csv` | Single chart |
| Current conditions | Depth at base, mid and top per resort as reported, with time stamps and "not available" gaps; forecast strip by height | Daily pipeline | Stacked cards by resort |
| Pass value | Local versus full pass price, and lifts to the far side | Evidence register, `base_access.csv` | Two line table |

Every chart carries its source, period, data type (measured, modelled, forecast) and retrieval date.
