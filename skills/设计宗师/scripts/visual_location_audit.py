#!/usr/bin/env python3
"""Check a visual-location map for unique, addressable and evidenced markers."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

MARKER = re.compile(r"`(VLM-[A-Z0-9-]+-\d{2})`")


def audit(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    rows = [line for line in text.splitlines() if line.startswith("| `VLM-")]
    markers = [match.group(1) for line in rows for match in MARKER.finditer(line)]
    findings: list[dict[str, Any]] = []
    duplicates = sorted({marker for marker in markers if markers.count(marker) > 1})
    for marker in duplicates:
        findings.append({"severity": "error", "marker": marker, "reason": "duplicate_marker"})
    for line in rows:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 7 or cells[3] in {"—", "-", ""} or cells[6].lower() in {"needs review", "not ready"}:
            findings.append({"severity": "warning", "marker": MARKER.search(line).group(1) if MARKER.search(line) else "unknown", "reason": "missing_owner_or_evidence"})
    errors = sum(1 for item in findings if item["severity"] == "error")
    return {
        "schema_version": "2.0",
        "status": "blocked" if errors else ("needs_review" if findings else "verified"),
        "marker_count": len(set(markers)),
        "finding_count": len(findings),
        "findings": findings,
        "rule": "Every delivered meaningful region needs one stable semantic marker, an implementation owner and viewport evidence.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("map", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        rendered = json.dumps(audit(args.map), ensure_ascii=False, indent=2) + "\n"
    except (OSError, UnicodeDecodeError) as exc:
        parser.error(str(exc))
    if args.output:
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
