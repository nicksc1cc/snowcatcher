#!/usr/bin/env python3
"""
Snowcatcher / Project Snow — Resort migration v2 → v3.1
Maps existing v2 fields into the v3.1 schema structure without losing data.
Reports what's genuinely missing per resort (overview, families, safety, sustainability...).

Usage: python3 tools/migrate_resorts.py [--dry-run]
"""
import json
import sys
import shutil
from pathlib import Path

RESORT_DIR = Path("/Users/nicholaschristensen/Projects/snowcatcher/data/resorts")

# ---------------------------------------------------------------------------
# Field mapping rules: (v2_path, v3_path, transform)
# ---------------------------------------------------------------------------
MAPS = [
    # Identity
    ("resort",            "name",                 None),
    ("slug",              "slug",                 None),
    ("domain",            "domain",               None),
    ("region",            "region",               None),
    ("altitude",          "statistics.base_altitude", None),
    ("description",       "description",          None),
    ("character",         "overview.atmosphere",  None),
    ("research_sources",  "research_sources",     None),
    ("research_status",   "research_status",      None),

    # stats -> statistics
    ("stats.altitude_resort", "statistics.base_altitude", None),
    ("stats.altitude_top",    "statistics.top_altitude",   None),
    ("stats.vertical_drop",   "statistics.vertical_drop",  None),
    ("stats.own_pistes_km",   "statistics.own_pistes_km",  None),
    ("stats.domain_pistes_km","statistics.domain_pistes_km", None),
    ("stats.own_pistes_count","statistics.own_pistes",     None),
    ("stats.domain_pistes_count","statistics.domain_pistes", None),
    ("stats.own_lifts",       "statistics.own_lifts",      None),
    ("stats.domain_lifts",    "statistics.domain_lifts",   None),
    ("stats.lift_capacity_per_hour", "statistics.lift_capacity_per_hour", None),
    ("stats.snow_cannons",    "statistics.snow_cannons",   None),
    ("stats.snowmaking_km",   "statistics.snowmaking_km",  None),
    ("stats.beginner_pct",    "statistics.beginner_pct",   None),
    ("stats.intermediate_pct","statistics.intermediate_pct", None),
    ("stats.advanced_pct",    "statistics.advanced_pct",   None),
    ("stats.pct_above_2000m", "statistics.pct_above_2000m", None),
    ("stats.glaciers",        "statistics.glacier_count",  None),
    ("stats.longest_run_km",  "statistics.longest_run_km", None),
    ("stats.most_difficult_run", "statistics.most_difficult_run", None),

    # weather_snow -> when_to_go
    ("weather_snow.season_typical",   "when_to_go.season_open", None),
    ("weather_snow.season_latest",    "when_to_go.season_close", None),
    ("weather_snow.snow_reliability_rating", "when_to_go.snow_reliability_detail", None),
    ("weather_snow.snow_reliability_note",   "when_to_go.snow_reliability_note", None),
    ("weather_snow.typical_snowfall_note",   "when_to_go.snow_reliability_notes", None),
    ("weather_snow.best_time_for_snow", "when_to_go.best_time_to_ski", None),
    ("weather_snow.weather_pattern",  "when_to_go.weather_pattern", None),
    ("weather_snow.typical_temperature_range", "when_to_go.how_cold_gets", None),
    ("weather_snow.sun_exposure",     "when_to_go.north_facing_slopes", None),
    ("weather_snow.weakness",         "when_to_go.high_wind_lift_closures", None),
    ("weather_snow.average_snow_depth_mid_season", "when_to_go.average_snow_depth_mid_season", None),
    ("weather_snow.average_annual_snowfall_cm", "when_to_go.average_annual_snowfall_cm", None),
    ("weather_snow.best_time_for_sun", "when_to_go.best_time_for_sun", None),
    ("weather_snow.season_earliest",  "when_to_go.season_earliest", None),

    # non_ski_activities -> beyond_skiing
    ("non_ski_activities.spas_and_wellness", "beyond_skiing.swimming_pool_or_spa", None),
    ("non_ski_activities.swimming",   "beyond_skiing.swimming_pool_or_spa", None),
    ("non_ski_activities.ice_skating", "beyond_skiing.ice_skating", None),
    ("non_ski_activities.zip_line",   "beyond_skiing.non_ski_activities", None),
    ("non_ski_activities.toboggan",   "beyond_skiing.non_ski_activities", None),
    ("non_ski_activities.paragliding","beyond_skiing.paragliding", None),
    ("non_ski_activities.dog_sledding","beyond_skiing.dog_sledding", None),
    ("non_ski_activities.snowshoeing","beyond_skiing.snowshoeing", None),
    ("non_ski_activities.snowmobiling","beyond_skiing.snowmobiling", None),
    ("non_ski_activities.ice_climbing","beyond_skiing.non_ski_activities", None),
    ("non_ski_activities.bowling",    "beyond_skiing.non_ski_activities", None),
    ("non_ski_activities.cinema",     "beyond_skiing.non_ski_activities", None),
    ("non_ski_activities.fitness",    "beyond_skiing.non_ski_activities", None),
    ("non_ski_activities.paintball",  "beyond_skiing.non_ski_activities", None),
    ("non_ski_activities.events",     "beyond_skiing.events_during_stay", None),
    ("non_ski_activities.other",      "beyond_skiing.non_ski_activities", None),

    # dining_guide -> food_and_drink
    ("dining_guide.signature",   "food_and_drink.best_restaurants", None),
    ("dining_guide.stars_1",     "food_and_drink.michelin_starred", None),
    ("dining_guide.mountain",    "food_and_drink.mountain_restaurants", None),
    ("dining_guide.bakery",      "food_and_drink.bakeries", None),
    ("dining_guide.budget",      "food_and_drink.cheap_mountain_lunch", None),
    ("dining_guide.vegetarian",  "food_and_drink.dietary_options", None),
    ("dining_guide.local_dishes","food_and_drink.local_dishes", None),
    ("dining_guide.booking",     "food_and_drink.booking_advice", None),
    ("dining_guide.cost",        "food_and_drink.meal_cost", None),

    # piste_guide -> ski_area
    ("piste_guide.beginners",    "ski_area.beginners_note", None),
    ("piste_guide.intermediates","ski_area.intermediates_note", None),
    ("piste_guide.advanced",     "ski_area.advanced_note", None),
    ("piste_guide.off_piste",    "off_piste.off_piste_detail", None),
    ("piste_guide.snowpark",     "ski_area.snowpark_note", None),
    ("piste_guide.crowding",     "ski_area.lift_queues", None),
    ("piste_guide.longest_run",  "ski_area.longest_run", None),
    ("piste_guide.key_run",      "ski_area.best_runs", None),

    # apres_guide -> apres_and_nightlife
    ("apres_guide.iconic", "apres_and_nightlife.apres_ski_description", None),
    ("apres_guide.bars",   "apres_and_nightlife.nightlife_clubbing", None),
    ("apres_guide.clubs",  "apres_and_nightlife.nightlife_clubbing", None),
    ("apres_guide.vibe",   "apres_and_nightlife.quiet_evenings", None),

    # comparison -> comparisons
    ("comparison.vs_courchevel", "comparisons.comparison_within_domain", None),
    ("comparison.vs_meribel",    "comparisons.comparison_within_domain", None),
    ("comparison.vs_tignes",     "comparisons.rival_comparison", None),

    # practical_info -> services
    ("practical_info.tourist_office",    "services.tourist_office_url", None),
    ("practical_info.lift_pass_6day_2025_26", "pricing.lift_pass_6day_euro", None),
    ("practical_info.lift_pass_vt_only_6day",  "pricing.local_pass_6day_euro", None),
    ("practical_info.ski_school",   "services.ski_school", None),
    ("practical_info.ski_rental",   "services.ski_hire_info", None),
    ("practical_info.supermarket",  "services.supermarket_notes", None),
    ("practical_info.medical",      "services.medical_centre_notes", None),
    ("practical_info.parking",      "getting_around.parking_cost", None),
    ("practical_info.wifi",         "services.free_wifi", None),
    ("practical_info.ski_patrol",   "services.ski_patrol_collection", None),
    ("practical_info.tourist_office_url", "services.tourist_office_url", None),

    # access
    ("access.nearest_airports", "access.nearest_airports", None),
    ("access.by_train",         "access.by_train", None),
    ("access.by_car",           "access.by_car", None),
]


def deep_get(obj, dotted):
    for part in dotted.split("."):
        if not isinstance(obj, dict) or part not in obj:
            return None
        obj = obj[part]
    return obj


def deep_set(obj, dotted, value):
    parts = dotted.split(".")
    cur = obj
    for part in parts[:-1]:
        cur = cur.setdefault(part, {})
    cur[parts[-1]] = value


def migrate(src: dict) -> dict:
    out = {}
    unmapped = {}

    for key, val in src.items():
        if key not in [m[0].split(".")[0] for m in MAPS]:
            unmapped[key] = val

    # Apply mapping rules
    for v2_path, v3_path, _ in MAPS:
        val = deep_get(src, v2_path)
        if val is not None and val != "" and val != [] and val != {}:
            # Merge lists/strings where target exists
            existing = deep_get(out, v3_path)
            if isinstance(existing, list) and isinstance(val, list):
                val = existing + [v for v in val if v not in existing]
            elif isinstance(existing, str) and isinstance(val, str):
                val = f"{existing}. {val}" if existing else val
            deep_set(out, v3_path, val)

    # Keep villages array
    if "villages" in src:
        out["villages"] = src["villages"]

    # Keep honest_drawbacks
    if "honest_drawbacks" in src:
        out["honest_drawbacks"] = src["honest_drawbacks"]

    # Preserve any unmapped fields verbatim (data safety)
    if unmapped:
        out["_preserved_unmapped"] = unmapped

    return out


MISSING_SECTIONS = [
    "overview", "families", "where_to_stay", "safety_and_access",
    "sustainability", "beginners", "off_piste", "comparisons", "pricing",
]


def report_gaps(new: dict, slug: str) -> dict:
    gaps = []
    for sec in MISSING_SECTIONS:
        if sec not in new or not new.get(sec):
            gaps.append(sec)
    # count fields mapped
    field_count = sum(len(v) if isinstance(v, dict) else 1 for v in new.values())
    return {"fields": field_count, "gaps": gaps}


def main():
    dry = "--dry-run" in sys.argv
    files = sorted(RESORT_DIR.glob("*.json"))
    report = {}

    for f in files:
        src = json.loads(f.read_text())

        # Skip files already migrated to v3.1 (have statistics + overview or were written post-migration)
        if "statistics" in src or "overview" in src or "families" in src:
            if not dry:
                print(f"SKIP      {f.stem:30s} already v3.1")
            else:
                print(f"skip      {f.stem:30s} already v3.1")
            continue

        new = migrate(src)
        if not dry:
            # backup original
            bak = f.with_suffix(".json.bak")
            if not bak.exists():
                f.rename(bak)
            f.write_text(json.dumps(new, indent=2, ensure_ascii=False))

        r = report_gaps(new, f.stem)
        report[f.stem] = r
        status = "dry-run" if dry else "migrated"
        print(f"{status:9s} {f.stem:30s} fields={r['fields']:3d} gaps={r['gaps']}")

    # summary
    if not dry:
        print("\n=== SUMMARY ===")
        all_gaps = {}
        for slug, r in report.items():
            for g in r["gaps"]:
                all_gaps.setdefault(g, []).append(slug)
        for g, slugs in sorted(all_gaps.items()):
            print(f"\n  Missing '{g}': {len(slugs)}/{len(files)} resorts  e.g. {', '.join(slugs[:5])}")


if __name__ == "__main__":
    main()