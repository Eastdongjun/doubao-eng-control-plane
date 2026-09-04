#!/usr/bin/env python3
"""Run browser geometry auditing and pause for authorization when its runtime is absent."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

try:
    from scripts.dependency_contract import (
        emit_result,
        node_runtime_authorization,
        playwright_browser_authorization,
        playwright_package_authorization,
    )
except ModuleNotFoundError:  # Direct execution from the scripts directory.
    from dependency_contract import (
        emit_result,
        node_runtime_authorization,
        playwright_browser_authorization,
        playwright_package_authorization,
    )

BOUNDARY_CAPABILITY = "Automated responsive boundary geometry audit"


def parse_authorization_result(text: str) -> dict[str, Any] | None:
    """Recognize a dependency contract emitted by the Node audit."""

    try:
        value = json.loads(text.strip())
    except (json.JSONDecodeError, TypeError):
        return None
    return value if isinstance(value, dict) and value.get("status") == "authorization_required" else None


def classify_dependency_failure(message: str, skill_root: Path) -> dict[str, Any] | None:
    """Convert known runtime failures into an actionable authorization request."""

    normalized = message.lower()
    if "playwright" in normalized and (
        "cannot find module" in normalized
        or "is required" in normalized
        or "module_not_found" in normalized
    ):
        return playwright_package_authorization(
            skill_root,
            blocked_capability=BOUNDARY_CAPABILITY,
            detected_error=message,
        )
    browser_markers = (
        "executable doesn't exist",
        "executable does not exist",
        "browser executable",
        "playwright install",
        "failed to launch chromium",
    )
    if any(marker in normalized for marker in browser_markers):
        return playwright_browser_authorization(
            skill_root,
            blocked_capability=BOUNDARY_CAPABILITY,
            detected_error=message,
        )
    return None


def handle_completed_audit(
    completed: subprocess.CompletedProcess[str],
    *,
    output: Path,
    skill_root: Path,
) -> int:
    """Translate dependency failures or forward the completed audit result."""

    node_authorization = parse_authorization_result(completed.stdout)
    if node_authorization is not None:
        return emit_result(node_authorization, output)

    combined_error = "\n".join(
        part for part in (completed.stderr, completed.stdout) if part
    ).strip()
    dependency_request = classify_dependency_failure(combined_error, skill_root)
    if dependency_request is not None:
        return emit_result(dependency_request, output)

    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="")
    if completed.returncode != 0:
        return completed.returncode
    if not output.is_file():
        print(json.dumps({"status": "blocked", "error": "boundary audit produced no report"}))
        return 2
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="Local HTML file or http(s)/file URL")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--viewport", action="append", default=[], help="Viewport such as 1280x800; repeatable")
    parser.add_argument("--browser", type=Path, help="Explicit Chrome, Edge, or Chromium executable")
    args = parser.parse_args()
    is_url = bool(re.match(r"^(?:https?|file)://", args.target, re.IGNORECASE))
    if not is_url and not Path(args.target).is_file():
        parser.error(f"HTML does not exist: {args.target}")

    skill_root = Path(__file__).resolve().parents[1]
    node = shutil.which("node")
    if not node:
        return emit_result(
            node_runtime_authorization(
                blocked_capability=BOUNDARY_CAPABILITY,
                detected_error="The node executable was not found on PATH.",
            ),
            args.output,
        )

    script = Path(__file__).with_name("audit_layout_boundaries.mjs")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    command = [node, str(script), "--target", args.target, "--output", str(args.output)]
    if args.viewport:
        command.extend(["--viewports", ",".join(args.viewport)])
    if args.browser:
        command.extend(["--browser", str(args.browser)])

    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError as exc:
        return emit_result(
            node_runtime_authorization(
                blocked_capability=BOUNDARY_CAPABILITY,
                detected_error=str(exc),
            ),
            args.output,
        )

    return handle_completed_audit(completed, output=args.output, skill_root=skill_root)


if __name__ == "__main__":
    raise SystemExit(main())
