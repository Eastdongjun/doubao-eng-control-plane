#!/usr/bin/env python3
"""Enforce mode-specific minimum deliverables and evidence states."""

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

REQUIRED = {
    "conformance": ["DESIGN_AUTHORITY.yaml", "DESIGN_VALUE_AUDIT.md"],
    "product": ["EXPERIENCE_MATRIX.md", "STATE_MATRIX.md", "BOUNDARY_REPORT.md"],
    "visual": ["RESEARCH_BRIEF.md", "AESTHETIC_DECISION_RECORD.md", "SILHOUETTE_PROOF.md"],
    "redesign": ["DESIGN_AUTHORITY.yaml", "INHERITANCE_CONTRACT.md", "AESTHETIC_DECISION_RECORD.md"],
    "production": ["DESIGN_VALUE_AUDIT.md", "ASSET_MANIFEST.yaml", "BOUNDARY_REPORT.md", "PROOF_LOG.md"],
    "critique": ["CRITIQUE.md"],
}
VALID_STATES = {"not_started", "in_progress", "unproven", "evidenced", "approved", "shipped", "blocked"}


def load_data(path: Path) -> dict[str, Any]:
    value = load_json_or_yaml(path, document_label="design gate task")
    if not isinstance(value, dict):
        raise TypeError("task must be an object")
    return value


def check(task: dict[str, Any], artifact_root: Path) -> dict[str, Any]:
    mode = str(task.get("mode", "")).strip().lower()
    if mode not in REQUIRED:
        raise ValueError("invalid mode")
    state = str(task.get("evidence_status", "not_started")).strip().lower()
    findings: list[dict[str, str]] = []
    if state not in VALID_STATES:
        findings.append({"severity": "error", "reason": "invalid_evidence_status"})
    missing = [name for name in REQUIRED[mode] if not (artifact_root / name).is_file()]
    if missing:
        findings.append({"severity": "error", "reason": "missing_artifacts", "items": ", ".join(missing)})
    if state in {"approved", "shipped"} and missing:
        findings.append({"severity": "error", "reason": "cannot_approve_with_missing_artifacts"})
    if state in {"approved", "shipped"} and not task.get("decision_owner"):
        findings.append({"severity": "error", "reason": "decision_owner_required"})
    if state == "unproven":
        findings.append({"severity": "warning", "reason": "visual_or_runtime_proof_is_unproven"})
    status = "blocked" if any(item["severity"] == "error" for item in findings) else state
    return {
        "schema_version": "2.0",
        "status": status,
        "mode": mode,
        "evidence_status": state,
        "required_artifacts": REQUIRED[mode],
        "missing_artifacts": missing,
        "findings": findings,
        "rule": "Written intent is not evidence; approved/shipped requires the mode's minimum artifacts and an accountable decision owner.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", type=Path)
    parser.add_argument("--artifacts", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        rendered = json.dumps(check(load_data(args.task), args.artifacts), ensure_ascii=False, indent=2) + "\n"
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
