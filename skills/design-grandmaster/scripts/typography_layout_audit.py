#!/usr/bin/env python3
"""Validate mixed-script fixtures, rhythm tokens and optical correction ownership."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REQUIRED_SAMPLE_FIELDS = {"text", "script_roles", "font_family", "line_height", "baseline_status"}


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError("fixture must be an object")
    return value


def audit(fixture: dict[str, Any]) -> dict[str, Any]:
    samples = fixture.get("samples", [])
    if not isinstance(samples, list) or not samples:
        raise ValueError("samples must be a non-empty list")
    spacing = {str(value) for value in fixture.get("spacing_tokens", [])}
    findings: list[dict[str, Any]] = []
    for index, sample in enumerate(samples):
        if not isinstance(sample, dict):
            findings.append({"severity": "error", "sample": index, "reason": "sample_not_object"})
            continue
        missing = sorted(REQUIRED_SAMPLE_FIELDS - set(sample))
        if missing:
            findings.append({"severity": "error", "sample": index, "reason": "missing_fields", "items": missing})
        if str(sample.get("baseline_status", "")) not in {"verified", "needs_review"}:
            findings.append({"severity": "error", "sample": index, "reason": "baseline_unverified"})
        for field in ("block_gap", "line_gap", "letter_spacing"):
            value = sample.get(field)
            if value is not None and spacing and str(value) not in spacing:
                findings.append({"severity": "warning", "sample": index, "reason": "unmapped_spacing", "field": field, "value": value})
        if sample.get("optical_correction") and not sample.get("correction_owner"):
            findings.append({"severity": "error", "sample": index, "reason": "unowned_optical_correction"})
    errors = sum(1 for item in findings if item["severity"] == "error")
    return {
        "schema_version": "2.0",
        "status": "blocked" if errors else ("needs_review" if findings else "verified"),
        "sample_count": len(samples),
        "finding_count": len(findings),
        "findings": findings,
        "rule": "Mixed scripts require actual font and metric evidence; optical corrections need a bounded semantic owner.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        rendered = json.dumps(audit(load(args.fixture)), ensure_ascii=False, indent=2) + "\n"
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    if args.output:
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
