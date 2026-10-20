# Methodology and data schema

Deliverables 1 (question bank) and 2 (schema and methodology). The question bank is `data/question_bank.csv` (1,325 questions), built by `scripts/build_question_bank.py`.

## 1. Research method

1. **Question first.** Every piece of research answers a question in the bank. Each question names its sources, method, output, freshness and the page section it feeds.
2. **Source order.** Official domain and lift operators for boundaries, passes and status; documented weather APIs and national services for weather; measuring stations and resort reports for local snow; open map data and elevation models for terrain and the network; tourism sources for facilities; independent research for trends; reviews last, labelled as opinion.
3. **Evidence records.** Every claim used goes into `data/evidence_register.csv` with value, unit, scope, period, source, retrieval date, data type and confidence. Conflicting figures share a `conflict_group` and are all kept.
4. **Model, then check.** Network and terrain results come from OpenStreetMap and a 90 m elevation model and are marked first pass until checked against the official map and on site.
5. **Separation.** Facts, calculations, estimates, forecasts and opinions are stored and shown separately. Long term snow history and current conditions are never merged.

## 2. Question bank

| Source of questions | How built | Count |
|---|---|---|
| Domain level | Written one by one across identity, network, geography, snow data, snow history, current conditions, passes, suitability, food, transport and reviews | 121 |
| Sector profiles | 32 questions applied to 19 working sectors | 608 |
| Connections | 12 questions applied to 22 modelled links and routes | 264 |
| Bases | 14 questions applied to 16 base villages | 224 |
| Traveller segments | 6 questions applied to 18 traveller types | 108 |
| **Total** | | **1,325** |

The template questions are distinct research needs because each applies to a different place, link or traveller, and each answer is different. No question is repeated (the build script refuses duplicates).

Status after this pass: 134 evidenced, 5 disputed, 447 researching, 739 unresearched. Priority: 713 at level 1 (core decision), 477 at level 2 (trip planning), 135 at level 3 (deeper).

### Question record fields

`question_id`, `domain_id`, `category`, `subcategory`, `question`, `question_type` (factual, comparative, analytical, temporal, operational, traveller-specific), `geographic_scope` (domain, sector, route, village, point, elevation band), `traveller_segments`, `variables_required`, `definitions_and_units`, `data_source_candidates`, `research_method`, `expected_output_type`, `time_period_or_freshness_requirement`, `dependencies`, `evidence_required`, `confidence_method`, `limitations`, `content_use`, `public_page_destination`, `refresh_frequency`, `status` (unresearched, researching, evidenced, disputed, unavailable, rejected), `evidence_ids`, `priority`, `last_verified_at`.

## 3. Domain data model

Designed so a second domain can be added without changing the structure.

| Table | Key fields |
|---|---|
| `domain` | domain_id, name, countries, official_km, measured_km, pass_name, season_start, season_end |
| `sector` | sector_id, domain_id, name, country, linked (yes, one way, pass only), base_m, top_m, centre_lat, centre_lon |
| `village` | village_id, sector_ids, name, elevation_m, rail_station, bus_lines |
| `node` | node_id, domain_id, type (lift base, lift top, junction, village), lat, lon, elevation_m, source |
| `edge` | edge_id, from_node, to_node, type (lift, piste, walk, bus, ride down), name, difficulty, length_m, duration_s, lift_type, capacity_pph, direction, depends_on, exposure_flags, source, osm_id |
| `pass_product` | product_id, domain_id, name, coverage (sector_ids), duration_days, age_band, channel, period_from, period_to, price, currency, source, retrieved |
| `evidence` | evidence_id, claim, value, unit, applies_to, period, source, url, source_type, data_type, confidence, conflict_group, retrieved |
| `question` | as above |

## 4. Weather and snow record

One long table for all observations, reports, model values and forecasts.

| Field | Notes |
|---|---|
| domain_id, sector_id, location_id | location is a named point with fixed coordinates and elevation |
| lat, lon, elevation_m | of the point the value applies to |
| model_grid_lat, model_grid_lon, grid_elevation_m | for model values; station id and distance for stations |
| aspect | only when derived from the elevation model |
| valid_time | the date or hour the value describes |
| issue_time | forecast run time, report time or observation time |
| retrieved_at | when Snow Catchers fetched it (UTC) |
| variable | snowfall, snow_depth, new_snow_24h, rain, temperature_mean, wind_gust, freezing_level, lifts_open, km_open |
| value, unit | displayed units: cm, mm, C, km/h, m |
| original_value, original_unit | as supplied |
| source, source_ref | provider and endpoint, model or station id |
| data_type | measured, reported, modelled, reanalysis, forecast |
| spatial_resolution | grid size or station distance |
| quality_flag, confidence | from the source and from checks |
| missing | true when the source had no value |
| licence, attribution | per source |

Raw responses are stored unchanged; normalised rows and derived statistics sit in separate tables tagged with the script version.

## 5. Definitions

* **Season:** 1 November to 30 April, labelled by start year.
* **Snowfall:** new snow over a period, in cm. **Snow depth:** snow on the ground at a time, in cm. Never interchanged.
* **Linked:** reachable from the main network by lift and piste, allowing the three village transfers; **pass only:** covered by the pass with no such link.
* **Minimum lift rides:** fewest lifts on any route in the modelled graph, ignoring time and opening hours.
