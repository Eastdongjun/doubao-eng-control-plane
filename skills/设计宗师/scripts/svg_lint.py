#!/usr/bin/env python3
"""Check SVG assets for one accessible, project-consistent icon grammar."""

from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

EMOJI = re.compile("[\\U0001F300-\\U0001FAFF]")


def lint_file(path: Path, require_current_color: bool) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    try:
        text = path.read_text(encoding="utf-8")
        root = ET.fromstring(text)
    except (OSError, UnicodeDecodeError, ET.ParseError) as exc:
        return [{"severity": "error", "path": path.as_posix(), "reason": "invalid_svg", "detail": str(exc)}]
    view_box = root.attrib.get("viewBox", "").split()
    if len(view_box) != 4:
        findings.append({"severity": "error", "path": path.as_posix(), "reason": "missing_viewBox"})
    if "width" not in root.attrib or "height" not in root.attrib:
        findings.append({"severity": "warning", "path": path.as_posix(), "reason": "explicit_width_height_missing"})
    if EMOJI.search(text):
        findings.append({"severity": "error", "path": path.as_posix(), "reason": "emoji_not_allowed"})
    decorative = root.attrib.get("aria-hidden") == "true"
    has_title = any(element.tag.rsplit("}", 1)[-1] == "title" for element in root.iter())
    if not decorative and not has_title and not root.attrib.get("aria-label"):
        findings.append({"severity": "error", "path": path.as_posix(), "reason": "accessible_name_missing"})
    if require_current_color and "currentColor" not in text and not decorative:
        findings.append({"severity": "warning", "path": path.as_posix(), "reason": "currentColor_not_used"})
    for attribute in root.iter():
        if "style" in attribute.attrib and "!important" in attribute.attrib["style"]:
            findings.append({"severity": "warning", "path": path.as_posix(), "reason": "important_inline_style"})
    return findings


def audit(root: Path, require_current_color: bool) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    files = sorted(root.rglob("*.svg"))
    for path in files:
        findings.extend(lint_file(path, require_current_color))
    errors = sum(1 for item in findings if item["severity"] == "error")
    status = "blocked" if errors else ("needs_review" if findings else "clean")
    return {
        "schema_version": "2.0",
        "status": status,
        "files_scanned": len(files),
        "finding_count": len(findings),
        "findings": findings,
        "rule": "Use one project icon grammar; SVG is the default functional icon format and emoji is never a substitute.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--allow-fixed-color", action="store_true", help="Do not warn when decorative/brand SVGs omit currentColor")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(audit(args.root, not args.allow_fixed_color), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
