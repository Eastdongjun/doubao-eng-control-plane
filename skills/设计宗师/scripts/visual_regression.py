#!/usr/bin/env python3
"""Compare baseline and candidate screenshots without pretending pixel identity is taste."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

try:
    from scripts.dependency_contract import (
        AUTHORIZATION_EXIT_CODE,
        PythonPackageRequest,
        python_package_authorization,
    )
except ModuleNotFoundError:  # Direct execution from the scripts directory.
    from dependency_contract import (
        AUTHORIZATION_EXIT_CODE,
        PythonPackageRequest,
        python_package_authorization,
    )


def pillow_authorization(error: str = "") -> dict[str, Any]:
    return python_package_authorization(
        PythonPackageRequest(
            package="Pillow",
            module="PIL",
            blocked_capability="Pixel-level visual regression comparison",
            purpose="Decode screenshots and calculate a normalized pixel-difference signal.",
        ),
        detected_error=error,
    )


def compare(
    baseline: Path,
    candidate: Path,
    threshold: float,
    *,
    allow_binary_fallback: bool = False,
) -> dict[str, Any]:
    first = baseline.read_bytes()
    second = candidate.read_bytes()
    result: dict[str, Any] = {
        "schema_version": "2.0",
        "baseline": baseline.as_posix(),
        "candidate": candidate.as_posix(),
        "baseline_sha256": hashlib.sha256(first).hexdigest(),
        "candidate_sha256": hashlib.sha256(second).hexdigest(),
        "method": "sha256",
        "difference": 0.0 if first == second else 1.0,
        "threshold": threshold,
        "status": "match" if first == second else "needs_review",
        "limitations": ["Binary comparison is a change signal, not a visual-quality verdict."],
    }
    try:
        from PIL import (  # type: ignore[import-untyped]  # compatibility: optional pixel backend
            Image,
            ImageChops,
            ImageStat,
        )

        left = Image.open(baseline).convert("RGBA")
        right = Image.open(candidate).convert("RGBA")
        if left.size != right.size:
            result.update({"method": "pixel_mean", "status": "blocked", "reason": "viewport_dimensions_differ", "baseline_size": left.size, "candidate_size": right.size})
            return result
        diff = ImageChops.difference(left, right)
        mean = sum(ImageStat.Stat(diff).mean) / (255.0 * 4.0)
        result.update({"method": "pixel_mean", "difference": round(mean, 6), "status": "match" if mean <= threshold else "needs_review"})
    except ImportError as exc:
        if allow_binary_fallback:
            result["fallback_authorized"] = True
            result["limitations"].append(
                "Pillow is unavailable; the caller explicitly accepted binary-only comparison."
            )
            return result
        request = pillow_authorization(str(exc))
        request["partial_evidence"] = result
        return request
    except OSError as exc:
        result.update({
            "status": "blocked",
            "reason": "image_decode_failed",
            "error": str(exc),
        })
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--threshold", type=float, default=0.02)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--allow-binary-fallback",
        action="store_true",
        help="Use SHA-256 only after the user explicitly accepts the reduced proof quality.",
    )
    args = parser.parse_args()
    if not args.baseline.is_file() or not args.candidate.is_file():
        parser.error("baseline and candidate must exist")
    result = compare(
        args.baseline,
        args.candidate,
        args.threshold,
        allow_binary_fallback=args.allow_binary_fallback,
    )
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    if result.get("status") == "authorization_required":
        return AUTHORIZATION_EXIT_CODE
    return 2 if result.get("status") == "blocked" else 0


if __name__ == "__main__":
    raise SystemExit(main())
