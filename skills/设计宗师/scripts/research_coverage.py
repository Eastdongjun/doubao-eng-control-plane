#!/usr/bin/env python3
"""Validate that a visual research ledger has enough diverse, dated evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from scripts.dependency_contract import (
        DependencyAuthorizationRequired,
        emit_result,
        load_json_or_yaml,
    )
except ModuleNotFoundError:  # Direct execution from the scripts directory.
    from dependency_contract import (
        DependencyAuthorizationRequired,
        emit_result,
        load_json_or_yaml,
    )

LANES = {"lineage", "category", "adjacency", "counter-reference", "material-interaction"}


def load_data(path: Path) -> dict[str, Any]:
    value = load_json_or_yaml(path, document_label="research source ledger")
    if not isinstance(value, dict):
        raise TypeError("research ledger must be an object")
    return value


def validate(ledger: dict[str, Any]) -> dict[str, Any]:
    entries = ledger.get("sources", [])
    if not isinstance(entries, list):
        raise TypeError("sources must be a list")
    findings: list[dict[str, str]] = []
    covered = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            findings.append({"severity": "error", "item": str(index), "reason": "source must be an object"})
            continue
        lane = str(entry.get("lane", "")).strip()
        covered.add(lane)
        required = ("url", "date", "observation", "transferable_mechanism", "do_not_copy")
        missing = [key for key in required if not str(entry.get(key, "")).strip()]
        if lane not in LANES:
            missing.append("valid_lane")
        if missing:
            findings.append({"severity": "error", "item": str(index), "reason": "missing: " + ", ".join(missing)})
    required_lanes = set(ledger.get("required_lanes", ["lineage", "category", "counter-reference"]))
    missing_lanes = sorted(required_lanes - covered)
    for lane in missing_lanes:
        findings.append({"severity": "error", "item": lane, "reason": "required research lane has no source"})
    saturation = bool(ledger.get("saturation_test_passed", False))
    if not saturation:
        findings.append({"severity": "warning", "item": "saturation_test", "reason": "new sources may still change the visual grammar"})
    status = "verified" if not any(item["severity"] == "error" for item in findings) and saturation else "unproven"
    return {
        "schema_version": "2.0",
        "status": status,
        "source_count": len(entries),
        "covered_lanes": sorted(covered),
        "required_lanes": sorted(required_lanes),
        "missing_lanes": missing_lanes,
        "findings": findings,
        "rule": "A moodboard without dated, diverse, mechanism-level evidence is not a verified direction.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        rendered = json.dumps(validate(load_data(args.ledger)), ensure_ascii=False, indent=2) + "\n"
    except DependencyAuthorizationRequired as exc:
        return emit_result(exc.payload, args.output)
    except (OSError, TypeError, ValueError) as exc:
        parser.error(str(exc))
    if args.output:
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
