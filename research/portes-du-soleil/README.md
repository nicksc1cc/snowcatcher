# Portes du Soleil: linked domain research, first pass

Started 20 October 2026. Research framework, question bank, evidence base and content plan for the Snow Catchers linked domain page. No public copy yet.

## Contents

| File | Deliverable |
|---|---|
| `01_methodology_and_schema.md` | Methodology, question bank structure, data schema (1, 2) |
| `02_snow_weather_sources.md` | Snow and weather source comparison, recommended stack, pipeline, historical and current condition plans (3, 4, 5, 6) |
| `03_snow_history_first_analysis.md` | First modelled snow history by elevation |
| `04_network_graph.md` | Network graph specification and first results (7) |
| `05_sectors_bases_passes.md` | Sector matrix, base access, pass value, ability links (8 and Priority 1 findings) |
| `06_evidence_coverage_backlog.md` | Evidence register summary and conflicts, coverage matrix, backlog (9, 10, 11) |
| `07_page_architecture_and_visuals.md` | Page architecture, internal links, visualisation plan (12, 13) |
| `08_qa_report.md` | QA report (14) |
| `data/question_bank.csv` and `.json` | 1,325 atomic questions |
| `data/evidence_register.csv` | 55 evidence records |
| `data/coverage_matrix.csv` | Question status by page section |
| `data/network_graph.json` | Sector connectivity matrix and critical lift test |
| `data/network_ability_matrices.txt` | Connectivity on green and blue, up to red, all runs |
| `data/sector_matrix.csv` | Sector comparison |
| `data/base_access.csv` | Lift rides from each base |
| `data/snow_era5_*` | Seasonal snowfall, weekly medians, summary statistics |
| `data/forecast_snapshot_2026-10-20.csv` | Sample forecast pull |
| `raw/official_notes.md` | Notes from official and independent sources, with URLs |
| `scripts/` | Question bank and evidence register builders |

## Headline findings (to verify against the official map)

1. The domain behaves as two networks joined through Morzine town: Les Gets and Morzine's Pléney side on one, Avoriaz and Switzerland on the other. Coming back from Avoriaz means riding a gondola down to Morzine.
2. Abondance, Saint-Jean-d'Aulps and La Chapelle's Crêt Béni side are pass only; La Chapelle's Panthiaz gondola links one way to Torgon.
3. A handful of lifts carry most cross domain routes: the Super-Morzine gondola, the Zore, Proclou and Séraussaix chairs, and the Champoussin chairs (Pointe de l'Au, Bochasses, Aiguille des Champeys).
4. Avoriaz, Les Lindarets and Les Crosets are the hubs; from Les Gets it takes about four lifts to reach Avoriaz and eight to reach Super-Châtel.
5. A six day full domain pass costs EUR 76 more online than the Les Gets-Morzine pass, roughly one extra day ticket. On the Swiss side the gap is CHF 7 a day.
6. On the ERA5 model, median seasonal snowfall at 1,100 m fell from 173 cm (1961 to 1990) to 116 cm (1991 to 2020), and all of the last five seasons were in the lowest third of the record; at 2,100 m the fall is smaller.
