#!/usr/bin/env python3
"""Detect converged layout silhouettes before color and surface styling."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

AXES = ("canvas", "navigation", "entry", "information_units", "density_curve", "mobile_transform")


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError("fingerprint record must be an object")
    return value


def audit(record: dict[str, Any]) -> dict[str, Any]:
    candidates = record.get("candidates", [])
    if not isinstance(candidates, list) or not candidates:
        raise ValueError("candidates must be a non-empty list")
    fingerprints: dict[str, list[str]] = {}
    findings: list[dict[str, Any]] = []
    for candidate in candidates:
        if not isinstance(candidate, dict):
            findings.append({"severity": "error", "reason": "candidate_not_object"})
            continue
        name = str(candidate.get("name", "unnamed"))
        missing = [axis for axis in AXES if not str(candidate.get(axis, "")).strip()]
        if missing:
            findings.append({"severity": "error", "candidate": name, "reason": "missing_axes", "items": missing})
        fingerprint = "|".join(str(candidate.get(axis, "")).strip().lower() for axis in AXES)
        fingerprints.setdefault(fingerprint, []).append(name)
    for fingerprint, names in fingerprints.items():
        if len(names) > 1:
            findings.append({"severity": "warning", "reason": "duplicate_fingerprint", "candidates": names, "fingerprint": fingerprint})
    required_distinct = int(record.get("required_distinct", 2))
    distinct_count = len(fingerprints)
    if distinct_count < required_distinct:
        findings.append({"severity": "error", "reason": "insufficient_distinct_silhouettes", "required": required_distinct, "actual": distinct_count})
    errors = sum(1 for item in findings if item["severity"] == "error")
    return {
        "schema_version": "2.0",
        "status": "blocked" if errors else ("needs_review" if findings else "verified"),
        "candidate_count": len(candidates),
        "distinct_fingerprints": distinct_count,
        "fingerprints": fingerprints,
        "findings": findings,
        "rule": "Color, imagery or radius differences do not count as materially different layout silhouettes.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        rendered = json.dumps(audit(load(args.record)), ensure_ascii=False, indent=2) + "\n"
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    if args.output:
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
