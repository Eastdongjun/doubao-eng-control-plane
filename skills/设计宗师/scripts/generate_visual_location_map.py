#!/usr/bin/env python3
"""Generate a batch-scoped visual location map from semantic HTML anchors."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from html import escape
from html.parser import HTMLParser
from pathlib import Path

SAFE_KEY = re.compile(r"[^a-zA-Z0-9]+")


def key(value: str, fallback: str) -> str:
    normalized = SAFE_KEY.sub("-", value).strip("-").upper()
    return normalized or fallback


def markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


@dataclass(frozen=True)
class Location:
    semantic: str
    name: str
    anchor: str
    tag: str
    line: int


class LocationParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.locations: list[Location] = []
        self._seen: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name: value or "" for name, value in attrs}
        semantic = values.get("data-vloc", "").strip()
        element_id = values.get("id", "").strip()
        if not semantic and tag in {"header", "nav", "main", "section", "article", "aside", "footer"}:
            semantic = element_id
        if not semantic:
            return

        anchor = f'[data-vloc="{escape(semantic, quote=True)}"]' if values.get("data-vloc") else f"#{element_id}"
        uniqueness = f"{semantic}\0{anchor}"
        if uniqueness in self._seen:
            return
        self._seen.add(uniqueness)
        name = (
            values.get("data-vloc-name", "").strip()
            or values.get("aria-label", "").strip()
            or semantic
        )
        self.locations.append(Location(semantic, name, anchor, tag, self.getpos()[0]))


def build_document(
    source_label: str,
    locations: list[Location],
    batch: str,
    page: str,
    project: str,
) -> str:
    batch_key = key(batch, "BATCH")
    page_key = key(page, "PAGE")
    region_counts: dict[str, int] = {}
    rows: list[str] = []
    for location in locations:
        region_source = location.semantic.split(".")[-1]
        region_key = key(region_source, key(location.tag, "REGION"))
        region_counts[region_key] = region_counts.get(region_key, 0) + 1
        marker = f"VLM-{batch_key}-{page_key}-{region_key}-{region_counts[region_key]:02d}"
        source_anchor = f"`{markdown_cell(location.anchor)}` · line {location.line}"
        rows.append(
            "| "
            + " | ".join(
                (
                    f"`{marker}`",
                    markdown_cell(location.name),
                    markdown_cell(location.semantic),
                    source_anchor,
                    "—",
                    "—",
                    "Needs review",
                )
            )
            + " |"
        )

    if not rows:
        rows.append("| — | No semantic regions found | — | — | — | — | Not ready |")

    return f"""# Visual Location Map — {project} / {batch}

Batch: `{batch}`

Generated: `{datetime.now(timezone.utc).date().isoformat()}`

Source: `{source_label}`

Page: `{page}`

## How to reference

Use the complete marker in a revision request, for example: `VLM-{batch_key}-{page_key}-HERO-01`.

## Locations

| Marker | Semantic name | Semantic path | Source anchor | Implementation owner | Viewport evidence | Status |
|---|---|---|---|---|---|---|
{chr(10).join(rows)}

## Revision log

| Marker | Request | Scope | System impact | Result | Evidence |
|---|---|---|---|---|---|
| — | — | — | None / component / token proposal | — | — |

## Unmapped or unstable regions

Record any meaningful visual region that lacks a stable semantic source anchor, plus its owner and correction.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="HTML entry point")
    parser.add_argument("--batch", required=True, help="Task batch key, for example 260813A")
    parser.add_argument("--page", help="Stable page key; defaults to the source filename")
    parser.add_argument("--project", help="Project name; defaults to the source parent folder")
    parser.add_argument("--output", type=Path, help="Markdown output path; defaults beside the source")
    args = parser.parse_args()

    source_label = args.source.as_posix()
    source = args.source.resolve()
    if not source.is_file():
        parser.error(f"source does not exist: {source}")
    if source.suffix.lower() not in {".html", ".htm"}:
        parser.error("source must be an HTML file")

    html = source.read_text(encoding="utf-8")
    if "\ufffd" in html:
        parser.error("source contains replacement characters; check its encoding")
    location_parser = LocationParser()
    location_parser.feed(html)

    page = args.page or source.stem
    project = args.project or source.parent.name
    output = args.output.resolve() if args.output else source.with_name(f"VISUAL-LOCATION-MAP-{key(args.batch, 'BATCH')}.md")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        build_document(source_label, location_parser.locations, args.batch, page, project),
        encoding="utf-8",
        newline="\n",
    )
    print(f"Generated {output} with {len(location_parser.locations)} visual locations")
    return 0 if location_parser.locations else 2


if __name__ == "__main__":
    raise SystemExit(main())
