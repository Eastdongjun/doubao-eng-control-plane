#!/usr/bin/env python3
"""Validate dated trend evidence and its project-specific adaptation boundary."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def audit(record: dict[str, Any]) -> dict[str, Any]:
    trends = record.get("trends", [])
    if not isinstance(trends, list) or not trends:
        raise ValueError("trends must be a non-empty list")
    required = ("name", "source", "date", "mechanism", "project_fit", "expiry_risk", "rejected_surface")
    findings: list[dict[str, Any]] = []
    for index, trend in enumerate(trends):
        if not isinstance(trend, dict):
            findings.append({"severity": "error", "item": index, "reason": "trend_not_object"})
            continue
        missing = [field for field in required if not str(trend.get(field, "")).strip()]
        if missing:
            findings.append({"severity": "error", "item": trend.get("name", index), "reason": "missing_fields", "fields": missing})
    errors = sum(1 for item in findings if item["severity"] == "error")
    return {
        "schema_version": "2.0",
        "status": "blocked" if errors else ("needs_review" if findings else "verified"),
        "trend_count": len(trends),
        "finding_count": len(findings),
        "findings": findings,
        "rule": "A trend is an input with lineage, current evidence, a functional role and an expiry boundary, never a complete art direction.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        value = json.loads(args.record.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise TypeError("trend record must be an object")
        rendered = json.dumps(audit(value), ensure_ascii=False, indent=2) + "\n"
    except (OSError, UnicodeDecodeError, TypeError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    if args.output:
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
