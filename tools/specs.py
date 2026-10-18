"""Field specifications for every record type. Do not edit.
Each field: (expects, question IDs, seasonal, guidance)."""

T, N, I, L, TB, B, D = "text", "number", "integer", "list", "table", "boolean", "date"

# One file: research/countries/france.json
COUNTRY = {
 "01_industry": {
  "skier_days_latest": (N, "C002 C085", True, "Millions of skier days for the latest completed season"),
  "skier_days_history": (TB, "C085", False, "Rows: season, skier_days_millions. Back to 2008/09"),
  "world_rank": (I, "C002", True, "Rank by skier days"),
  "peer_comparison": (TB, "C002", True, "Rows: country, skier_days_millions, season"),
  "ski_area_count": (I, "C003", True, "scope_note MUST state the definition used"),
  "lift_count": (I, "C086", True, ""),
  "lift_count_history": (TB, "C086", False, "Rows: year, lifts"),
  "drag_lift_count": (I, "C086", True, ""),
  "average_lift_age_years": (N, "C086", True, ""),
  "snowmaking_coverage_pct": (N, "C087", True, "Share of pistes covered"),
  "foreign_visitor_share_pct": (N, "C088", True, ""),
  "visitor_origin": (TB, "C089", True, "Rows: nationality, share_pct"),
  "top_resorts_by_attendance": (L, "C090", True, "In rank order"),
  "attendance_share_by_range": (TB, "C085", True, "Rows: range, share_pct"),
  "attendance_concentration": (T, "C085", True, "e.g. share of attendance in the 15 largest resorts"),
  "lift_revenue_eur": (N, "C085", True, ""),
  "employment_direct": (I, "C091", True, ""),
  "employment_total": (I, "C091", True, ""),
  "tourist_beds_total": (I, "C085", True, ""),
 },
 "02_geography": {
  "ranges": (TB, "C007 C008", False, "Rows: name, departments, highest_point_m, character, ski_area_count"),
  "northern_vs_southern_alps": (T, "C008", False, ""),
  "cross_border_domains": (TB, "C026", False, "Rows: domain, linked_country, link_type"),
 },
 "03_history_culture": {
  "plan_neige": (T, "C009", False, "What it was, dates, resorts it created"),
  "timeline": (TB, "C009", False, "Rows: year, event"),
  "savoyard_culture": (T, "C079", False, ""),
  "dishes": (TB, "C072", False, "Rows: name, region, description"),
  "cheeses": (TB, "C073", False, "Rows: name, aop_status, region"),
  "drinks": (TB, "C074", False, "Rows: name, region, description"),
  "meal_times": (T, "C075", False, ""),
  "tipping_norms": (T, "C076", False, ""),
  "shop_hours": (T, "C077", False, "Including Sundays in resorts"),
  "english_spoken": (T, "C078", False, ""),
 },
 "04_calendar": {
  "season_general": (T, "C028", True, "Typical opening and closing by altitude"),
  "school_holiday_zones": (TB, "C029", True, "Rows: zone, academies, winter_start, winter_end"),
  "uk_half_term_dates": (TB, "C030", True, "Rows: nation, start, end"),
  "peak_weeks": (T, "C031", True, ""),
  "summer_glacier_skiing": (TB, "C033", True, "Rows: resort, glacier, months"),
  "snow_trends": (T, "C034", False, "Name the study and period"),
 },
 "05_access": {
  "airports": (TB, "C036", True, "Rows: code, name, ranges_served, uk_routes"),
  "rail_routes": (TB, "C037", True, "Rows: route, changes, duration, seasonal"),
  "coach_services": (TB, "C043", True, "Rows: operator, from, to"),
  "skis_on_planes": (T, "C044", False, ""),
 },
 "06_driving": {
  "calais_to_alps_hours": (N, "C038", False, "scope_note states the destination used"),
  "routes": (TB, "C038", False, "Rows: route, via, distance_km"),
  "tolls": (TB, "C039", True, "Rows: route, cost_eur"),
  "winter_equipment_law": (T, "C040", True, "Dates, number of departments, penalty"),
  "low_emission_zones": (TB, "C041", True, "Rows: city, rules"),
  "required_kit": (L, "C042", False, ""),
  "speed_limits": (TB, "C042", False, "Rows: road, dry_kmh, wet_kmh"),
  "blood_alcohol_limit": (T, "C042", False, ""),
 },
 "07_entry_practical": {
  "uk_passport_rules": (T, "C045", False, ""),
  "uk_days_rule": (T, "C045", False, ""),
  "ees_status": (T, "C045", True, "Entry/Exit System"),
  "etias_status": (T, "C045", True, ""),
  "ghic_coverage": (T, "C046", False, ""),
  "currency_and_cards": (T, "C047", False, ""),
  "mobile_roaming": (T, "C048", False, ""),
  "plugs_and_time_zone": (T, "C049", False, ""),
  "emergency_numbers": (TB, "C066", False, "Rows: number, service"),
 },
 "08_costs": {
  "average_day_pass_eur": (N, "C051", True, "scope_note states how the average was calculated"),
  "pricing_patterns": (T, "C053", True, "Online discounts, dynamic pricing, family offers"),
  "ancv_acceptance": (T, "C056", False, ""),
  "multi_resort_passes": (TB, "C055", True, "Rows: pass, french_resorts"),
  "week_cost_estimates": (TB, "C054", True, "Rows: resort_type, item, cost_eur"),
 },
 "09_ski_schools": {
  "esf": (T, "C057", True, "Founding, number of schools, number of instructors"),
  "esf_levels": (TB, "C058", False, "Rows: level, audience, what_it_means"),
  "independent_schools": (T, "C059", False, ""),
  "minimum_ages": (TB, "C060", False, "Rows: school_type, min_age"),
  "uk_instructor_rules": (T, "C061", True, ""),
 },
 "10_safety": {
  "helmet_rules": (T, "C062", False, ""),
  "carre_neige": (T, "C063", True, "Cover and daily price"),
  "rescue_costs": (T, "C064", False, ""),
  "insurance_guidance": (T, "C065", False, ""),
  "piste_grading": (TB, "C067", False, "Rows: colour, meaning"),
  "off_piste_law": (T, "C068", False, ""),
  "avalanche_bulletin": (T, "C069", False, "Name, scale, where published"),
  "alcohol_rules": (T, "C070", False, ""),
  "drone_rules": (T, "C071", False, ""),
 },
 "11_accommodation": {
  "accommodation_types": (TB, "C080", False, "Rows: type, description, typical_inclusions"),
  "apartment_norms": (T, "C081", False, ""),
  "self_catering_inclusions": (T, "C082", False, ""),
  "tourist_tax": (T, "C083", True, ""),
  "changeover_norms": (T, "C084", False, ""),
 },
 "12_climate_sustainability": {
  "closed_resorts": (TB, "C092", False, "Rows: resort, closed_year, reason"),
  "climate_projections": (T, "C034 C092", False, "Name the study"),
  "national_commitments": (T, "C093", False, ""),
  "labels": (TB, "C094", True, "Rows: label, criteria, number_of_resorts"),
 },
 "13_beyond_living": {
  "cross_country_overview": (T, "C095", False, ""),
  "thermal_spas": (TB, "C096", False, "Rows: town, nearest_resort"),
  "summer_offer": (T, "C097", False, ""),
  "season_work_rules": (T, "C098", True, "Including rules for UK nationals"),
  "property_buying": (T, "C099", False, ""),
 },
}


# One file per region: research/structure/<region-slug>.json
STRUCTURE = {
 "01_region": {
  "name": (T, "", False, "Official or most widely used name of the region"),
  "departments": (L, "", False, "French departments the region covers"),
  "description": (T, "", False, "Two or three sentences on where it is and what defines it"),
 },
 "02_resorts": {
  "resorts": (TB, "", False, "Rows: name, slug, villages (list of village names), commune. A resort is the place people book. One row per resort"),
 },
 "03_linked_domains": {
  "linked_domains": (TB, "", False, "Rows: name, slug, member_resorts (list of resort slugs, at least 2), link_evidence (what joins them: named lifts or pistes). Only areas where two or more resorts are joined by lifts or pistes on one pass"),
 },
 "04_pass_networks": {
  "pass_networks": (TB, "", False, "Rows: name, slug, member_resorts (list of resort slugs), link_type (bus, separate areas, partial lift link). Areas sold on one pass but not fully joined by lifts"),
 },
}

# One file per linked domain: research/domains/<slug>.json
DOMAIN = {
 "01_identity": {
  "name": (T, "", False, ""),
  "operator": (T, "", False, "Company or companies operating the lifts"),
  "website": (T, "", False, "Official URL"),
  "member_resorts": (L, "", False, "Resort slugs, matching the structure file"),
  "link_description": (T, "", False, "How the resorts are joined, naming the key lifts"),
  "cross_border": (T, "C026", False, "Country and resorts on the other side, if any"),
  "linked_since_year": (I, "", False, ""),
 },
 "02_statistics": {
  "pistes_km_claimed": (N, "C004", True, "The operator's own figure"),
  "pistes_km_measured": (N, "C004", False, "An independent measurement, if one exists. scope_note names the method"),
  "runs_total": (I, "", True, ""),
  "runs_by_colour": (TB, "", True, "Rows: colour, count. Counts, not percentages"),
  "lifts_total": (I, "", True, ""),
  "lifts_by_type": (TB, "", True, "Rows: type, count"),
  "highest_lift_served_m": (N, "C005", False, "Highest point reached by a lift that skiers use"),
  "lowest_skiable_m": (N, "", False, ""),
  "snowmaking_coverage_pct": (N, "", True, ""),
  "glaciers": (L, "", False, ""),
 },
 "03_season": {
  "opening_date": (D, "", True, ""),
  "closing_date": (D, "", True, ""),
 },
 "04_passes": {
  "adult_1day_eur": (N, "", True, "Ticket office price. scope_note says if online prices differ"),
  "adult_6day_eur": (N, "", True, ""),
  "child_6day_eur": (N, "", True, "scope_note states the age band"),
  "senior_6day_eur": (N, "", True, "scope_note states the age band"),
  "season_pass_eur": (N, "", True, ""),
  "free_under_age": (I, "", True, ""),
  "family_offer": (T, "", True, ""),
  "pricing_notes": (T, "", True, "Dynamic pricing, online discounts, extensions"),
 },
 "05_terrain": {
  "signature_runs": (TB, "", False, "Rows: name, colour, length_m, vertical_m, description"),
  "off_piste_zones": (TB, "", False, "Rows: name, location, guide_recommended, description"),
  "terrain_parks": (TB, "", True, "Rows: name, location, features"),
  "ski_touring": (T, "", False, ""),
  "night_skiing": (T, "", True, ""),
  "connections": (TB, "", True, "Rows: from_resort, to_resort, via_lifts, level_needed, last_lift_time"),
 },
}

# One file per resort: research/resorts/<slug>.json
RESORT = {
 "01_identity": {
  "name": (T, "", False, ""), "known_for": (T, "", False, ""),
  "founded_year": (I, "", False, ""), "history": (T, "", False, ""),
  "website": (T, "", False, ""), "tourist_office_url": (T, "", False, ""),
  "awards": (TB, "", False, "Rows: award, year, awarding_body"),
 },
 "02_ski_area": {
  "base_altitude_m": (N, "", False, "Altitude of the main village. scope_note names it"),
  "top_altitude_m": (N, "", False, "Highest lift served point in the resort's own area"),
  "pistes_km": (N, "", True, "The resort's own area, not the linked domain. scope_note required"),
  "runs_by_colour": (TB, "", True, "Rows: colour, count"),
  "lifts_total": (I, "", True, ""), "lifts_by_type": (TB, "", True, "Rows: type, count"),
  "snow_cannons": (I, "", True, ""), "snowmaking_coverage_pct": (N, "", True, ""),
  "main_aspect": (T, "", False, ""), "glacier": (T, "", False, ""),
  "longest_run": (T, "", False, "Name and length"), "steepest_run": (T, "", False, ""),
  "beginner_areas": (T, "", False, ""), "free_beginner_lifts": (T, "", True, ""),
  "easiest_way_home": (T, "", False, ""), "progression_notes": (T, "", False, ""),
  "bad_weather_skiing": (T, "", False, ""), "nordic_km": (N, "", True, ""),
  "snowboard_notes": (T, "", False, "Flat sections, drag lifts"),
 },
 "03_season_weather": {
  "opening_date": (D, "", True, ""), "closing_date": (D, "", True, ""),
  "monthly_snow_depth": (TB, "", False, "Rows: month, upper_cm, lower_cm. scope_note names years averaged"),
  "monthly_temperature": (TB, "", False, "Rows: month, avg_high_c, avg_low_c"),
  "wind_closures": (T, "", False, ""), "busiest_periods": (T, "", True, ""),
  "quietest_periods": (T, "", True, ""),
 },
 "04_access": {
  "airports": (TB, "", False, "Rows: code, name, distance_km, transfer_minutes"),
  "transfer_options": (TB, "", True, "Rows: mode, operator, duration_min, price_eur"),
  "nearest_station": (T, "", False, ""), "station_transfer": (T, "", True, ""),
  "rail_from_london": (T, "", True, ""), "drive_from_calais_hours": (N, "", False, ""),
  "road_notes": (T, "", False, ""), "parking": (T, "", True, "Locations and prices"),
  "ev_charging": (T, "", True, ""), "car_free": (T, "", False, ""),
  "shuttle_bus": (T, "", True, "Free or paid, hours, routes"), "luggage_storage": (T, "", False, ""),
 },
 "05_passes_lessons": {
  "local_pass_1day_eur": (N, "", True, ""), "local_pass_6day_eur": (N, "", True, ""),
  "domain_pass_6day_eur": (N, "", True, ""), "beginner_pass": (T, "", True, ""),
  "discounts": (T, "", True, ""), "free_ages": (T, "", True, ""),
  "refund_policy": (T, "", True, ""), "pedestrian_passes": (T, "", True, ""),
  "ski_schools": (TB, "", True, "Rows: name, english_spoken, min_age, website"),
  "group_lessons_6day_eur": (N, "", True, ""), "private_lesson_2h_eur": (N, "", True, ""),
  "booking_lead_time": (T, "", True, ""),
 },
 "06_off_piste_parks": {
  "off_piste": (T, "", False, ""), "guide_companies": (TB, "", True, "Rows: name, website"),
  "touring": (T, "", False, ""), "parks": (TB, "", True, "Rows: name, features"),
  "heliskiing": (T, "", False, "Heliskiing is banned in France. Record nearby options abroad if any"),
 },
 "07_families": {
  "childcare": (TB, "", True, "Rows: name, min_age, max_age, hours"),
  "evening_kids_club": (T, "", True, ""), "babysitting": (T, "", True, ""),
  "toddler_activities": (T, "", False, ""), "teen_activities": (T, "", False, ""),
  "family_hotels": (TB, "", True, "Rows: name, kids_club"), "toboggan_runs": (T, "", True, ""),
  "labels": (L, "", True, "Famille Plus and other labels held"),
 },
 "08_stay": {
  "accommodation_mix": (T, "", False, ""), "ski_in_ski_out": (T, "", False, ""),
  "notable_hotels": (TB, "", True, "Rows: name, stars, village, notes"),
  "large_groups": (T, "", False, ""), "pool_spa_hotels": (L, "", True, ""),
  "central_booking": (T, "", False, ""), "bed_capacity": (I, "", False, ""),
 },
 "09_food_apres": {
  "restaurants": (L, "", False, "Restaurant slugs, each with its own file"),
  "local_dishes": (L, "", False, ""), "picnic_rooms": (T, "", True, ""),
  "supermarkets_bakeries": (T, "", True, ""), "meal_prices": (TB, "", True, "Rows: item, price_eur, where"),
  "apres_venues": (TB, "", True, "Rows: name, type, location, access_on_foot"),
  "nightlife": (T, "", True, ""), "closing_times": (T, "", True, ""),
 },
 "10_beyond_skiing": {
  "activities": (TB, "", True, "Rows: activity, where, price_eur"),
  "events": (TB, "", True, "Rows: name, dates"), "walks_snowshoe": (T, "", False, ""),
  "pool_spa": (T, "", True, ""), "indoor_options": (T, "", False, ""),
  "shopping": (T, "", False, ""), "summer": (T, "", False, ""),
 },
 "11_services_safety": {
  "hire_shops": (T, "", True, ""), "hire_6day_eur": (N, "", True, ""),
  "medical_centre": (T, "", False, ""), "pharmacy": (T, "", False, ""),
  "nearest_hospital": (T, "", False, ""), "wifi_coworking": (T, "", True, ""),
  "lost_property": (T, "", False, ""), "atm": (T, "", False, ""),
  "accessibility": (T, "", False, ""), "adaptive_skiing": (T, "", True, ""),
  "dogs": (T, "", False, ""),
 },
 "12_character": {
  "atmosphere": (T, "", False, ""), "architecture": (T, "", False, ""),
  "visitor_mix": (T, "", False, ""), "year_round_life": (T, "", False, ""),
  "sustainability": (T, "", True, "Certifications and named initiatives"),
 },
}

# One file per village: research/villages/<slug>.json
VILLAGE = {
 "01_identity": {
  "name": (T, "", False, ""), "resort": (T, "", False, "Resort slug"),
  "altitude_m": (N, "", False, ""), "commune": (T, "", False, ""),
  "description": (T, "", False, ""), "permanent_population": (I, "", True, ""),
 },
 "02_character": {
  "atmosphere": (T, "", False, ""), "architecture": (T, "", False, ""),
  "ski_access": (T, "", False, "How skiers reach the slopes and get home"),
  "walkability": (T, "", False, ""), "sun": (T, "", False, ""),
  "car_free": (T, "", False, ""), "open_year_round": (T, "", False, ""),
 },
 "03_practical": {
  "lifts_from_village": (L, "", True, ""), "shops_and_services": (T, "", True, "Supermarket, bakery, butcher, pharmacy"),
  "ski_schools": (L, "", True, ""), "hire_shops": (I, "", True, ""),
  "parking": (T, "", True, ""), "shuttle": (T, "", True, ""),
 },
 "04_food_nightlife": {
  "restaurants": (L, "", False, "Restaurant slugs"), "bars": (L, "", True, ""),
 },
}

# One file per restaurant: research/restaurants/<slug>.json
RESTAURANT = {
 "01_identity": {
  "name": (T, "", False, ""), "resort": (T, "", False, "Resort slug"),
  "village": (T, "", False, "Village slug, or not_applicable on the mountain"),
  "location_type": (T, "", False, "village, mountain or altitude"),
  "altitude_m": (N, "", False, ""), "website": (T, "", False, ""),
 },
 "02_offer": {
  "cuisine": (T, "", False, ""), "signature_dishes": (L, "", True, ""),
  "price_range": (T, "", True, "Typical main course price range in euros"),
  "dietary_options": (T, "", True, ""), "guide_recognition": (TB, "", True, "Rows: guide, award, year"),
 },
 "03_visit": {
  "opening_hours": (T, "", True, ""), "booking": (T, "", True, ""),
  "access_on_skis": (T, "", False, "Nearest lifts and pistes"), "access_on_foot": (T, "", False, ""),
  "terrace_and_views": (T, "", False, ""),
 },
}

SPECS = {"country": COUNTRY, "structure": STRUCTURE, "domain": DOMAIN, "resort": RESORT,
         "village": VILLAGE, "restaurant": RESTAURANT}