#!/usr/bin/env python3
"""Route a design task to the smallest evidence-backed capability set."""

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

MODES = {
    "conformance": {"system", "boundaries", "proof"},
    "product": {"experience", "interaction", "responsive", "proof"},
    "visual": {"research", "aesthetic", "layout", "assets", "proof"},
    "redesign": {"inheritance", "research", "aesthetic", "layout", "responsive", "proof"},
    "production": {"system", "typography", "assets", "responsive", "boundaries", "proof"},
    "critique": {"critique", "system", "responsive"},
}

CAPABILITIES = {
    "system": "design-system-conformance.md",
    "inheritance": "visual-inheritance-typography-and-layout.md",
    "research": "aesthetic-discovery-research.md",
    "aesthetic": "aesthetic-governor.md",
    "layout": "layout-intelligence-and-freshness.md",
    "typography": "mixed-script-typography-and-creative-composition.md",
    "experience": "experience-strategy.md",
    "interaction": "interaction-cognition-emotion.md",
    "responsive": "responsive-motion-data.md",
    "boundaries": "layout-boundary-safety.md",
    "assets": "artifact-production-validation.md",
    "proof": "artifact-production-validation.md",
    "critique": "critique-prototype-handoff.md",
}


def load_data(path: Path) -> dict[str, Any]:
    value = load_json_or_yaml(path, document_label="task manifest")
    if not isinstance(value, dict):
        raise TypeError("task manifest must be an object")
    return value


def as_bool(value: Any) -> bool:
    return value is True or (isinstance(value, str) and value.lower() in {"true", "yes", "1"})


def route(task: dict[str, Any]) -> dict[str, Any]:
    mode = str(task.get("mode", "")).strip().lower()
    if mode not in MODES:
        raise ValueError("mode must be one of: " + ", ".join(sorted(MODES)))
    authority = str(task.get("authority", "unresolved")).strip().lower()
    allowed_authority = {"binding-system", "user-directed", "research-derived", "unresolved"}
    if authority not in allowed_authority:
        raise ValueError("authority is invalid")
    risk = max(0, min(5, int(task.get("business_risk", 0))))
    visual_stakes = max(0, min(5, int(task.get("visual_stakes", 0))))
    needs_research = as_bool(task.get("needs_research")) or authority in {"unresolved", "research-derived"}
    capabilities = set(MODES[mode])
    if needs_research:
        capabilities.update({"research", "aesthetic"})
    if visual_stakes >= 3:
        capabilities.update({"layout", "typography", "assets"})
    if as_bool(task.get("mixed_script")):
        capabilities.add("typography")
    if as_bool(task.get("uses_svg")):
        capabilities.add("assets")
    if as_bool(task.get("needs_loading_decision")):
        capabilities.update({"responsive", "interaction"})

    required = sorted(capabilities)
    conditional = []
    if authority == "binding-system":
        conditional.append("research: only for unresolved local expression")
    if mode in {"product", "conformance"} and visual_stakes < 3:
        conditional.append("aesthetic: keep structural decisions in grayscale")
    if not as_bool(task.get("runnable_artifact")):
        conditional.append("proof: provide a truthful non-rendered limitation record")

    minimum_artifacts = {
        "conformance": ["DESIGN_AUTHORITY.yaml", "DESIGN_VALUE_AUDIT.md"],
        "product": ["EXPERIENCE_MATRIX.md", "STATE_MATRIX.md", "BOUNDARY_REPORT.md"],
        "visual": ["RESEARCH_BRIEF.md", "AESTHETIC_DECISION_RECORD.md", "SILHOUETTE_PROOF.md"],
        "redesign": ["DESIGN_AUTHORITY.yaml", "INHERITANCE_CONTRACT.md", "AESTHETIC_DECISION_RECORD.md"],
        "production": ["DESIGN_VALUE_AUDIT.md", "ASSET_MANIFEST.yaml", "BOUNDARY_REPORT.md", "PROOF_LOG.md"],
        "critique": ["CRITIQUE.md"],
    }[mode]
    return {
        "schema_version": "2.0",
        "mode": mode,
        "authority": authority,
        "risk": {"business": risk, "visual_stakes": visual_stakes},
        "required_capabilities": [
            {"id": item, "reference": CAPABILITIES[item]} for item in required
        ],
        "conditional_capabilities": conditional,
        "minimum_artifacts": minimum_artifacts,
        "blocking_gates": ["authority", "token", "symbol", "boundary", "evidence", "proof"],
        "evidence_status": "unproven",
        "routing_note": "Load only required references; never treat an unproven direction as approved.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", type=Path, help="JSON or YAML task manifest")
    parser.add_argument("--output", type=Path, help="Write route JSON to this path")
    args = parser.parse_args()
    try:
        result = route(load_data(args.task))
    except DependencyAuthorizationRequired as exc:
        return emit_result(exc.payload, args.output)
    except (OSError, TypeError, ValueError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
