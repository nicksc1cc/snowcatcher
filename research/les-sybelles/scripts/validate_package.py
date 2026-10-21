#!/usr/bin/env python3
"""Validate the Les Sybelles Level 3 research package using only Python stdlib."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ALLOWED_STATUS = {
    "unresearched", "researching", "evidenced",
    "conflicting/incomplete", "unavailable", "rejected",
}
ALLOWED_TYPES = {
    "factual", "comparative", "analytical", "temporal",
    "operational", "traveller-specific",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    questions_csv = read_csv(DATA / "question_bank.csv")
    questions_json = json.loads((DATA / "question_bank.json").read_text(encoding="utf-8"))
    evidence = read_csv(DATA / "evidence_register.csv")
    coverage = read_csv(DATA / "coverage_matrix.csv")

    errors: list[str] = []
    if len(questions_csv) != len(questions_json):
        errors.append("Question CSV/JSON row counts differ.")

    evidence_ids = {r["evidence_id"] for r in evidence}
    question_ids = [r["question_id"] for r in questions_csv]
    question_texts = [r["question"] for r in questions_csv]
    if len(question_ids) != len(set(question_ids)):
        errors.append("Duplicate question_id values.")
    if len(question_texts) != len(set(question_texts)):
        errors.append("Duplicate atomic question text.")

    json_by_id = {r["question_id"]: r for r in questions_json}
    for row in questions_csv:
        qid = row["question_id"]
        other = json_by_id.get(qid)
        if other is None:
            errors.append(f"{qid}: missing from JSON.")
            continue
        for key, value in row.items():
            if str(other.get(key, "")) != value:
                errors.append(f"{qid}: CSV/JSON mismatch in {key}.")
                break
        if row["status"] not in ALLOWED_STATUS:
            errors.append(f"{qid}: invalid status {row['status']!r}.")
        if row["question_type"] not in ALLOWED_TYPES:
            errors.append(f"{qid}: invalid question_type {row['question_type']!r}.")
        try:
            int(row["priority"])
        except ValueError:
            errors.append(f"{qid}: priority must be an integer.")
        for evidence_id in filter(None, row["evidence_ids"].split(";")):
            if evidence_id not in evidence_ids:
                errors.append(f"{qid}: unknown evidence ID {evidence_id}.")

    if not coverage:
        errors.append("Coverage matrix is empty.")

    print(f"Questions: {len(questions_csv)}")
    print(f"Evidence records: {len(evidence)}")
    print(f"Coverage rows: {len(coverage)}")
    if errors:
        print(f"FAIL: {len(errors)} issue(s)")
        for error in errors[:100]:
            print(f"- {error}")
        raise SystemExit(1)
    print("PASS: question IDs, question text, statuses, priorities, evidence references and CSV/JSON parity.")
    

if __name__ == "__main__":
    main()
