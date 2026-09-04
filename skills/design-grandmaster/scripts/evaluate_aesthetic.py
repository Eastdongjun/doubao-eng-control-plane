#!/usr/bin/env python3
"""Evaluate aesthetic directions with business-weighted, non-compensatory gates."""

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

DEFAULT_WEIGHTS = {
    "business_fit": 0.22,
    "audience_fit": 0.14,
    "hierarchy": 0.16,
    "brand_specificity": 0.12,
    "accessibility": 0.12,
    "feasibility": 0.10,
    "distinctiveness": 0.08,
    "trend_half_life": 0.06,
}


def load_data(path: Path) -> dict[str, Any]:
    value = load_json_or_yaml(path, document_label="aesthetic decision record")
    if not isinstance(value, dict):
        raise TypeError("decision record must be an object")
    return value


def evaluate(record: dict[str, Any]) -> dict[str, Any]:
    candidates = record.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        raise ValueError("candidates must be a non-empty list")
    weights = dict(DEFAULT_WEIGHTS)
    supplied = record.get("weights", {})
    if supplied:
        if not isinstance(supplied, dict):
            raise ValueError("weights must be an object")
        weights.update({str(k): float(v) for k, v in supplied.items()})
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("weights must have a positive total")
    weights = {key: value / total for key, value in weights.items()}
    evaluated = []
    for candidate in candidates:
        if not isinstance(candidate, dict):
            raise TypeError("each candidate must be an object")
        name = str(candidate.get("name", "unnamed"))
        scores = candidate.get("scores", {})
        if not isinstance(scores, dict):
            raise TypeError(f"{name}: scores must be an object")
        missing = [key for key in weights if key not in scores]
        if missing:
            raise ValueError(f"{name}: missing scores: {', '.join(missing)}")
        normalized = {key: max(0.0, min(5.0, float(scores[key]))) for key in weights}
        gates = candidate.get("gates", {})
        if not isinstance(gates, dict):
            raise TypeError(f"{name}: gates must be an object")
        failed_gates = sorted(str(key) for key, value in gates.items() if value is False)
        score = sum(normalized[key] * weights[key] for key in weights)
        minimum = float(candidate.get("minimum_gate", 3.0))
        rejected = bool(failed_gates) or any(normalized[key] < minimum for key in ("business_fit", "hierarchy", "accessibility"))
        if rejected and not str(candidate.get("rejection_reason", "")).strip():
            raise ValueError(f"{name}: rejected candidates require rejection_reason")
        evaluated.append({
            "name": name,
            "weighted_score": round(score, 3),
            "scores": normalized,
            "failed_gates": failed_gates,
            "decision": "rejected" if rejected else "survives",
            "confidence": str(candidate.get("confidence", "unknown")),
            "rejection_reason": str(candidate.get("rejection_reason", "")),
        })
    survivors = [item for item in evaluated if item["decision"] == "survives"]
    winner = max(survivors, key=lambda item: item["weighted_score"]) if survivors else None
    research_status = str(record.get("research_status", "unproven")).strip().lower()
    research_required = str(record.get("authority", "unresolved")).strip().lower() in {"unresolved", "research-derived"}
    research_blocked = research_required and research_status != "verified"
    return {
        "schema_version": "2.0",
        "weights": weights,
        "candidates": evaluated,
        "winner": winner["name"] if winner and not research_blocked else None,
        "status": "approved" if winner and not research_blocked else ("unproven" if winner and research_blocked else "blocked"),
        "research_status": research_status,
        "rule": "A direction failing business fit, hierarchy, accessibility, or an explicit gate cannot be rescued by spectacle elsewhere.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        rendered = json.dumps(evaluate(load_data(args.record)), ensure_ascii=False, indent=2) + "\n"
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
