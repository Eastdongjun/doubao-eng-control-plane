#!/usr/bin/env python3
"""Find consequential visual literals that are not mapped to approved tokens."""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Iterable
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

HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")
PX = re.compile(r"(?<![\w.-])(-?\d+(?:\.\d+)?)px\b")
CSS_FILES = {".css", ".scss", ".sass", ".less", ".html", ".htm", ".svg", ".vue", ".jsx", ".tsx"}


def load_data(path: Path) -> dict[str, Any]:
    value = load_json_or_yaml(path, document_label="design authority file")
    if not isinstance(value, dict):
        raise TypeError("authority file must be an object")
    return value


def tokens(authority: dict[str, Any]) -> dict[str, set[str]]:
    registry = authority.get("tokens", {})
    if not isinstance(registry, dict):
        raise TypeError("authority.tokens must be an object")
    result: dict[str, set[str]] = {"color": set(), "spacing": set(), "size": set(), "radius": set()}
    for category, approved_values in result.items():
        values = registry.get(category, [])
        if isinstance(values, dict):
            values = values.values()
        for value in values if isinstance(values, Iterable) and not isinstance(values, (str, bytes)) else []:
            approved_values.add(str(value).lower())
    return result


def audit(root: Path, authority: dict[str, Any]) -> dict[str, Any]:
    approved = tokens(authority)
    findings: list[dict[str, Any]] = []
    files_scanned = 0
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in CSS_FILES:
            continue
        if any(part in {"node_modules", "dist", "build", ".git"} for part in path.parts):
            continue
        files_scanned += 1
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append({"severity": "error", "path": path.as_posix(), "reason": "unreadable_utf8"})
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            for value in HEX.findall(line):
                if value.lower() not in approved["color"]:
                    findings.append({"severity": "warning", "path": path.as_posix(), "line": line_number, "category": "color", "value": value, "reason": "unmapped_color"})
            for value in PX.findall(line):
                normalized = value.rstrip("0").rstrip(".") if "." in value else value
                if normalized not in approved["spacing"] and normalized not in approved["size"] and normalized not in approved["radius"]:
                    findings.append({"severity": "warning", "path": path.as_posix(), "line": line_number, "category": "dimension", "value": normalized + "px", "reason": "unmapped_dimension"})
    status = "blocked" if any(item["severity"] == "error" for item in findings) else ("needs_review" if findings else "clean")
    return {
        "schema_version": "2.0",
        "status": status,
        "files_scanned": files_scanned,
        "finding_count": len(findings),
        "findings": findings,
        "rule": "A literal is evidence to investigate, not permission to create a new shared token. Record intrinsic or authorized exceptions separately.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--authority", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        rendered = json.dumps(audit(args.root, load_data(args.authority)), ensure_ascii=False, indent=2) + "\n"
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
