#!/usr/bin/env python3
"""Validate a cross-industry visual regression catalog."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REQUIRED_VIEWPORTS = {"desktop", "mobile"}
REQUIRED_STATES = {"default", "loading", "error"}


def audit(catalog: dict[str, Any]) -> dict[str, Any]:
    cases = catalog.get("cases", [])
    if not isinstance(cases, list) or not cases:
        raise ValueError("cases must be a non-empty list")
    findings: list[dict[str, Any]] = []
    industries = set()
    for case in cases:
        if not isinstance(case, dict):
            findings.append({"severity": "error", "reason": "case_not_object"})
            continue
        industry = str(case.get("industry", ""))
        industries.add(industry)
        viewports = set(case.get("viewports", [])) if isinstance(case.get("viewports", []), list) else set()
        states = set(case.get("states", [])) if isinstance(case.get("states", []), list) else set()
        for item in sorted(REQUIRED_VIEWPORTS - viewports):
            findings.append({"severity": "error", "industry": industry, "reason": "missing_viewport", "item": item})
        for item in sorted(REQUIRED_STATES - states):
            findings.append({"severity": "error", "industry": industry, "reason": "missing_state", "item": item})
        if not str(case.get("baseline", "")).strip():
            findings.append({"severity": "error", "industry": industry, "reason": "missing_baseline"})
    if len(industries) < int(catalog.get("minimum_industries", 3)):
        findings.append({"severity": "error", "reason": "insufficient_industry_diversity", "actual": len(industries)})
    errors = sum(1 for item in findings if item["severity"] == "error")
    return {"schema_version": "2.0", "status": "blocked" if errors else "verified", "case_count": len(cases), "industries": sorted(industries), "finding_count": len(findings), "findings": findings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        value = json.loads(args.catalog.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise TypeError("catalog must be an object")
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
