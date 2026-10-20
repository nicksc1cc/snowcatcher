# Sectors, bases, pass value and ability

Deliverable 8 (sector matrix) and the Priority 1 questions on bases, pass value and ability. Full data in `data/sector_matrix.csv`, `data/base_access.csv` and `data/network_ability_matrices.txt`. Lift and piste figures come from OpenStreetMap and a 90 m elevation model and must be checked against the official 2026/27 map before publication.

## 1. Sector matrix (summary)

Piste km are from OpenStreetMap geometry, which totals 428 km against the official 600 km, so treat them as relative sizes. Colours follow OpenStreetMap tags (novice green, easy blue, intermediate red, advanced black).

| Sector | Linked | Lifts | Drag lift share | Lowest lift base | Highest lift top | Piste km (OSM) | Green and blue share |
|---|---|---|---|---|---|---|---|
| Les Gets: Mont Chéry | via village | 4 | 0% | 1,170 m | 1,809 m | 16 | 14% |
| Les Gets: Chavannes and Ranfoilly | yes | 19 | 37% | 1,111 m | 1,782 m | 41 | 68% |
| Morzine: Nyon and Pointe de Nyon | yes | 10 | 20% | 1,029 m | 1,947 m | 21 | 50% |
| Morzine: Pléney | yes | 12 | 17% | 980 m | 1,545 m | 24 | 66% |
| Morzine: Super-Morzine and Zore | yes | 4 | 25% | 957 m | 1,758 m | 8 | 100% |
| Avoriaz | yes | 26 | 62% | 1,171 m | 2,192 m | 48 | 73% |
| Montriond: Les Lindarets and Ardent | yes | 9 | 11% | 1,205 m | 2,243 m | 30 | 64% |
| Châtel: Linga and Pré la Joux | yes | 10 | 30% | 1,124 m | 2,078 m | 34 | 49% |
| Châtel: Super-Châtel and Barbossine | yes | 23 | 65% | 1,102 m | 1,955 m | 21 | 55% |
| Torgon | yes | 8 | 62% | 1,337 m | 1,985 m | 21 | 49% |
| La Chapelle: Panthiaz and Braitaz | one way | 3 | 33% | 1,009 m | 1,817 m | 8 | 73% |
| La Chapelle: Crêt Béni | pass only | 7 | 71% | 993 m | 1,565 m | 15 | 77% |
| Abondance | pass only | 10 | 80% | 918 m | 1,674 m | 10 | 63% |
| Saint-Jean-d'Aulps: Roc d'Enfer | pass only | 16 | 69% | 943 m | 1,792 m | 30 | 37% |
| Morgins: Foilleuse | yes | 6 | 50% | 1,312 m | 1,829 m | 12 | 78% |
| Morgins: Corbeau | yes | 3 | 67% | 1,349 m | 1,834 m | 7 | 100% |
| Champoussin | yes | 7 | 57% | 1,454 m | 2,143 m | 25 | 75% |
| Les Crosets | yes | 14 | 36% | 1,652 m | 2,216 m | 46 | 48% |
| Champéry: Planachaux and Grand Paradis | yes | 5 | 20% | 1,034 m | 1,935 m | 12 | 19% |

Drag lift shares include short beginner platters, which inflate Avoriaz and Super-Châtel.

Patterns worth checking against the official map:
* **The high ground is in the middle.** Only Avoriaz, Les Lindarets, Châtel's Linga side, Champoussin and Les Crosets have lifts topping out above 2,000 m. Les Gets and Pléney stay below 1,810 m.
* **Les Crosets has the highest bases** (about 1,650 m), so its runs are the least exposed to low level rain in the modelled snow history.
* **Mont Chéry and Champéry are red territory** in the OpenStreetMap tags, with green and blue below 20% of their piste length.

## 2. Bases: how far the domain is from each village

Minimum lift rides to reach the first lift of each area (`data/base_access.csv`):

| Base | Avoriaz | Les Crosets | Super-Châtel | Torgon | First lift above 2,000 m | Ski back to start |
|---|---|---|---|---|---|---|
| Les Gets | 4 | 6 | 8 | 9 | 6 | yes |
| Morzine | 2 | 4 | 6 | 7 | 4 | Pléney yes, Super-Morzine and Nyon no |
| Avoriaz | 0 | 2 | 4 | 5 | 1 | yes |
| Les Lindarets | 1 | 2 | 4 | 5 | 2 | yes |
| Châtel | 4 | 5 | 0 | 2 | 2 | Linga yes, Super-Châtel to check |
| Morgins | 5 | 4 | 2 | 3 | 3 | yes |
| Champoussin | 3 | 2 | 3 | 4 | 1 | yes |
| Les Crosets | 1 | 0 | 3 | 4 | 1 | yes |
| Champéry | 2 | 1 | 4 | 5 | 2 | no (cable car) |
| La Chapelle (Panthiaz) | 11 | 10 | 4 | 2 | 9 | no |

* **Avoriaz, Les Lindarets and Les Crosets are the hubs.** From them, the high ground and both countries are one or two lifts away.
* **Les Gets and the pass only villages are far from the centre.** A skier based in Les Gets needs about four lifts and a crossing of Morzine town to reach Avoriaz, and eight to reach Super-Châtel, before turning round.
* **Some bases have no ski home.** The model finds no piste back to the Super-Morzine gondola, the Nyon cable car, Panthiaz or the Champéry cable car; skiers ride down or take a bus. skiresort.com confirms Super-Morzine and Panthiaz.

## 3. Is the full domain pass worth it?

| Comparison, adult, 2026/27 | Local pass | Full domain pass | Difference |
|---|---|---|---|
| Six days, Les Gets-Morzine, online | EUR 276 | EUR 352 | EUR 76 (28%) |
| Six days, Les Gets-Morzine, ticket office | EUR 312 | EUR 373 | EUR 61 (20%) |
| One day, Swiss 3CM area, online (adult 26 to 64) | CHF 68 | CHF 75 | CHF 7 (10%) |

* **For a week in Les Gets or Morzine**, the full pass costs about the same as one extra full domain day ticket (EUR 69 online). One trip to Avoriaz or Switzerland covers it, but the network section shows that trip costs four or more lifts each way and depends on the Super-Morzine gondola and the Morzine crossing.
* **On the Swiss side**, the full pass costs only CHF 7 a day more than the local 3CM pass, so a local pass rarely makes sense for anyone planning to reach Avoriaz.
* **For the pass only resorts** (Abondance, Crêt Béni, Roc d'Enfer), the full pass buys access mainly by bus or car; their own prices still need sourcing.
* Still missing: Avoriaz and Châtel local pass prices, any day extension product, and the cost of buses between pass only resorts and the network.

## 4. Ability: where the links need a red run

Using only runs tagged green or blue (`data/network_ability_matrices.txt`):

* Les Gets, Morzine, Avoriaz, Les Lindarets, Châtel's Linga side and Les Crosets connect on green and blue runs.
* **Super-Châtel, Torgon, Morgins and Champoussin do not connect to the Avoriaz side on green and blue** in the model, and Champéry's Planachaux is not reachable from Les Crosets without a red.
* With reds allowed, every linked sector is reachable, and the lift counts barely change from the all runs case.

These results depend on OpenStreetMap difficulty tags, which are incomplete. They identify the links to check first on the official map, not facts to publish.

## 5. Traveller fit (first evidence, not yet assessments)

| Traveller | What the evidence points to so far |
|---|---|
| Beginners | Every resort has beginner lifts; local beginner passes exist (P'tite Glisse in Les Gets-Morzine, Crosets, Champoussin and Morgins beginner passes). Base choice matters more than the domain pass. |
| Intermediates | The Les Gets to Les Crosets corridor connects on blue in the model; the Swiss north (Champoussin, Morgins) and Châtel to Torgon need reds. |
| Experts | The Chavanette (Swiss Wall), 1 km and 330 m drop with gradients up to 100%, and the high sectors around Les Crosets and Avoriaz. Freeride terrain is unsourced so far. |
| Snowboarders | Drag lifts make up a large share of lifts in Avoriaz, Super-Châtel, Torgon and the pass only resorts. Flat traverses are not yet identified. |
| Families | Châtel, Les Gets and Morzine hold the Famille Plus label. |
| Non skiers | Pedestrian lift tickets exist on both sides (Champéry cable car return CHF 24, Les Gets gondola return EUR 11). |
