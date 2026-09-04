#!/usr/bin/env python3
"""Maintain a content-addressed, date-aware research cache without inventing freshness."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cache", type=Path)
    parser.add_argument("--url", required=True)
    parser.add_argument("--content", type=Path, required=True)
    parser.add_argument("--lane", required=True)
    parser.add_argument("--source-date", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    content = args.content.read_text(encoding="utf-8")
    key = digest(args.url + "\n" + content)
    index = {"schema_version": "2.0", "entries": []}
    if args.cache.is_file():
        index = json.loads(args.cache.read_text(encoding="utf-8"))
    if not isinstance(index, dict) or not isinstance(index.get("entries", []), list):
        parser.error("cache must contain an object with an entries list")
    entry = {"key": key, "url": args.url, "lane": args.lane, "source_date": args.source_date, "cached_at": datetime.now(timezone.utc).isoformat(), "content_sha256": digest(content)}
    index["schema_version"] = "2.0"
    index["entries"] = [item for item in index["entries"] if isinstance(item, dict) and item.get("key") != key]
    index["entries"].append(entry)
    rendered = json.dumps(index, ensure_ascii=False, indent=2) + "\n"
    args.cache.parent.mkdir(parents=True, exist_ok=True)
    args.cache.write_text(rendered, encoding="utf-8", newline="\n")
    if args.output:
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
