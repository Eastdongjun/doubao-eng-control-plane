#!/usr/bin/env python3
"""Validate progressive-loading decisions for meaning, geometry and recovery."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ALLOWED = {"eager", "priority", "deferred-visible", "on-intent", "optional", "forbidden-delay"}
CRITICAL = {"critical-meaning", "primary-action", "consent", "error"}


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError("loading manifest must be an object")
    return value


def audit(manifest: dict[str, Any]) -> dict[str, Any]:
    resources = manifest.get("resources", [])
    if not isinstance(resources, list) or not resources:
        raise ValueError("resources must be a non-empty list")
    findings: list[dict[str, Any]] = []
    for index, resource in enumerate(resources):
        if not isinstance(resource, dict):
            findings.append({"severity": "error", "resource": index, "reason": "resource_not_object"})
            continue
        kind = str(resource.get("kind", ""))
        priority = str(resource.get("priority", ""))
        if priority not in ALLOWED:
            findings.append({"severity": "error", "resource": resource.get("id", index), "reason": "invalid_priority"})
        if kind in CRITICAL and priority in {"deferred-visible", "on-intent", "optional"}:
            findings.append({"severity": "error", "resource": resource.get("id", index), "reason": "critical_meaning_deferred"})
        if priority in {"deferred-visible", "on-intent"}:
            for field in ("reserved_geometry", "failure", "reduced_mode"):
                if not str(resource.get(field, "")).strip():
                    findings.append({"severity": "error", "resource": resource.get("id", index), "reason": "missing_loading_contract", "field": field})
        if priority == "on-intent" and not str(resource.get("cancel", "")).strip():
            findings.append({"severity": "warning", "resource": resource.get("id", index), "reason": "cancel_not_defined"})
    errors = sum(1 for item in findings if item["severity"] == "error")
    return {
        "schema_version": "2.0",
        "status": "blocked" if errors else ("needs_review" if findings else "verified"),
        "resource_count": len(resources),
        "finding_count": len(findings),
        "findings": findings,
        "rule": "Never defer critical meaning, primary actions, consent or errors; delayed resources need stable geometry, truthful status and recovery.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        rendered = json.dumps(audit(load(args.manifest)), ensure_ascii=False, indent=2) + "\n"
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    if args.output:
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
