#!/usr/bin/env python3
"""Capture Les Sybelles' public Lumiplan map metadata for research.

This script captures official-map static POI metadata and a separate dynamic
status snapshot. It deliberately does not infer physical links or route counts:
the Lumiplan POI response is a source inventory, not a validated piste graph.

Run from the snowcatcher repository root:
    python3 research/les-sybelles/scripts/fetch_official_map.py

Outputs are written to research/les-sybelles/raw/lumiplan/.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "raw" / "lumiplan"
# Map identifier used by the public interactive-map integration. Verify it still
# matches the current official iframe before treating a capture as current.
MAP_ID = "ec83ba74-a7db-4fb1-9b5e-8c16b7c90a7f"
API = "https://lumiplay.link/interactive-map-services/public/map"


def get_json(url: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "SnowCatchersResearch/1.0 (public ski-map research)",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError(f"HTTP {response.status} for {url}")
        return json.loads(response.read().decode("utf-8"))


def items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows = payload.get("items", [])
    return [x for x in rows if isinstance(x, dict)] if isinstance(rows, list) else []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--lang", default="en", choices=("en", "fr"))
    parser.add_argument("--map-id", default=MAP_ID)
    args = parser.parse_args()

    captured = datetime.now(timezone.utc)
    stamp = captured.strftime("%Y-%m-%dT%H%M%SZ")
    base = f"{API}/{args.map_id}"
    try:
        static = get_json(f"{base}/staticPoiData?lang={args.lang}")
        dynamic = get_json(f"{base}/dynamicPoiData?lang={args.lang}")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, RuntimeError) as exc:
        print(f"Could not capture map data: {exc}", file=sys.stderr)
        return 2

    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    static_path = out / f"static-{stamp}.json"
    dynamic_path = out / f"dynamic-{stamp}.json"
    static_path.write_text(json.dumps(static, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    dynamic_path.write_text(json.dumps(dynamic, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    dynamic_by_id = {
        str(row.get("id")): row for row in items(dynamic) if row.get("id") is not None
    }
    fields = (
        "id", "name", "type", "liftType", "trailType", "trailLevel", "length",
        "duration", "capacity", "uphillCapacity", "speed", "departureAltitude",
        "arrivalAltitude", "averageSlope", "exposure", "guaranteedSnow",
        "openingTimesTheoretic", "openingStatus", "operating", "openingTimesReal",
        "groomingStatus", "snowQuality", "message",
    )
    csv_path = out / f"poi-inventory-{stamp}.csv"
    static_items = items(static)
    counts: Counter[str] = Counter()
    grades: Counter[str] = Counter()
    with csv_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in static_items:
            data = row.get("data") if isinstance(row.get("data"), dict) else {}
            item_id = data.get("id")
            live = dynamic_by_id.get(str(item_id), {})
            merged = {**data}
            merged.update({k: live[k] for k in (
                "openingStatus", "operating", "openingTimesReal", "groomingStatus",
                "snowQuality",
            ) if k in live})
            if isinstance(live.get("message"), dict):
                merged["message"] = live["message"].get("content", "")
            writer.writerow({k: merged.get(k, "") for k in fields})
            counts[str(data.get("type", "unknown"))] += 1
            if data.get("trailLevel"):
                grades[str(data["trailLevel"])] += 1

    summary = {
        "captured_at_utc": captured.isoformat(),
        "source": "Public Lumiplan interactive-map services",
        "map_id": args.map_id,
        "language": args.lang,
        "endpoints": {
            "static": f"{base}/staticPoiData?lang={args.lang}",
            "dynamic": f"{base}/dynamicPoiData?lang={args.lang}",
        },
        "static_item_count": len(static_items),
        "dynamic_item_count": len(items(dynamic)),
        "static_type_counts": dict(counts),
        "trail_level_counts": dict(grades),
        "files": {
            "static": static_path.name,
            "dynamic": dynamic_path.name,
            "inventory_csv": csv_path.name,
        },
        "limitations": [
            "A live status snapshot is not a season-wide availability guarantee.",
            "This inventory does not establish spatial topology or continuous ski connections.",
            "Do not calculate lift rides, fastest routes, or ability reachability from this inventory alone.",
            "Cross-check the map ID and every claimed inter-sector link against the current official map.",
        ],
    }
    summary_path = out / f"summary-{stamp}.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
