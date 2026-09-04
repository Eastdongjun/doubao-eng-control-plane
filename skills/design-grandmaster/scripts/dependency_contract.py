#!/usr/bin/env python3
"""Create machine-readable authorization requests for missing runtime dependencies."""

from __future__ import annotations

import json
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import Any

AUTHORIZATION_EXIT_CODE = 3


class DependencyAuthorizationRequired(RuntimeError):
    """Signal that execution must pause until the user chooses an install or fallback."""

    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload
        super().__init__(str(payload["user_prompt"]))


@dataclass(frozen=True)
class DependencyRequest:
    dependency_id: str
    dependency_name: str
    dependency_kind: str
    blocked_capability: str
    purpose: str
    installation_options: list[dict[str, Any]]
    impact: list[str]
    fallback: dict[str, Any]


@dataclass(frozen=True)
class PythonPackageRequest:
    package: str
    module: str
    blocked_capability: str
    purpose: str


def authorization_required(
    request: DependencyRequest,
    *,
    detected_error: str = "",
) -> dict[str, Any]:
    """Return the shared dependency-authorization contract used by all skill tools."""

    payload: dict[str, Any] = {
        "schema_version": "2.0",
        "status": "authorization_required",
        "authorization_required": True,
        "authorization_id": f"install:{request.dependency_kind}:{request.dependency_id}",
        "dependency": {
            "id": request.dependency_id,
            "name": request.dependency_name,
            "kind": request.dependency_kind,
        },
        "blocked_capability": request.blocked_capability,
        "purpose": request.purpose,
        "environment": {
            "os": platform.system() or "unknown",
            "architecture": platform.machine() or "unknown",
        },
        "installation_options": request.installation_options,
        "impact": request.impact,
        "fallback": request.fallback,
        "next_action": "ask_user_before_install",
        "user_prompt": (
            f"缺少 {request.dependency_name}，因此无法完成“{request.blocked_capability}”。"
            "是否授权我按上述范围安装依赖并在安装后重新执行验证？"
        ),
        "rules": [
            "Do not install before explicit user authorization.",
            "Do not report the blocked capability as passed.",
            "Use the fallback only after the user declines or defers installation.",
        ],
    }
    if detected_error:
        payload["detected_error"] = detected_error.strip()[:2000]
    return payload


def python_package_authorization(
    request_details: PythonPackageRequest,
    *,
    detected_error: str = "",
) -> dict[str, Any]:
    request = DependencyRequest(
        dependency_id=request_details.module,
        dependency_name=request_details.package,
        dependency_kind="python-package",
        blocked_capability=request_details.blocked_capability,
        purpose=request_details.purpose,
        installation_options=[
            {
                "scope": "active-python-environment",
                "command": f"python -m pip install {request_details.package}",
                "changes": "Installs the package into the active Python environment.",
                "recommended_when": "The project uses a virtual environment or isolated runtime.",
            },
            {
                "scope": "current-user",
                "command": f"python -m pip install --user {request_details.package}",
                "changes": "Installs the package for the current operating-system user.",
                "recommended_when": "No project virtual environment is available.",
            },
        ],
        impact=[
            "Requires network access to the configured Python package index.",
            "Changes the selected Python environment and consumes local disk space.",
        ],
        fallback={
            "available": True,
            "quality_loss": "The requested structured or pixel-level verification remains unproven.",
            "requires_user_choice": True,
        },
    )
    return authorization_required(request, detected_error=detected_error)


def node_runtime_authorization(*, blocked_capability: str, detected_error: str = "") -> dict[str, Any]:
    request = DependencyRequest(
        dependency_id="node",
        dependency_name="Node.js LTS",
        dependency_kind="runtime",
        blocked_capability=blocked_capability,
        purpose="Run the browser automation entry point used by the geometry audit.",
        installation_options=[
            {
                "platform": "Windows",
                "scope": "system",
                "command": "winget install --id OpenJS.NodeJS.LTS -e",
                "changes": "Installs Node.js LTS and npm for the operating system.",
            },
            {
                "platform": "macOS",
                "scope": "system",
                "command": "brew install node",
                "changes": "Installs Node.js and npm through Homebrew.",
            },
            {
                "platform": "Debian or Ubuntu",
                "scope": "system",
                "command": "sudo apt-get install nodejs npm",
                "changes": "Installs Node.js and npm through the system package manager.",
            },
        ],
        impact=[
            "Requires a network download and changes the system runtime inventory.",
            "System installation may require administrator approval.",
        ],
        fallback={
            "available": True,
            "quality_loss": "Only a manual boundary review can be produced; browser geometry remains unproven.",
            "requires_user_choice": True,
        },
    )
    return authorization_required(request, detected_error=detected_error)


def playwright_package_authorization(
    skill_root: Path,
    *,
    blocked_capability: str,
    detected_error: str = "",
) -> dict[str, Any]:
    root = str(skill_root.resolve())
    request = DependencyRequest(
        dependency_id="playwright",
        dependency_name="Playwright for Node.js",
        dependency_kind="node-package",
        blocked_capability=blocked_capability,
        purpose="Open the artifact in a real browser and measure responsive safe areas, clipping, overflow, and scroll endpoints.",
        installation_options=[
            {
                "scope": "skill-local",
                "target": root,
                "command": f'npm install --prefix "{root}" --no-save --no-package-lock playwright',
                "changes": "Creates a skill-local node_modules directory without changing package manifests.",
                "recommended": True,
            }
        ],
        impact=[
            "Requires a network download from the configured npm registry.",
            "Creates a local node_modules directory and consumes disk space.",
            "The package may execute npm lifecycle scripts during installation.",
        ],
        fallback={
            "available": True,
            "quality_loss": "Manual screenshots and inspection cannot prove computed geometry with the same repeatability.",
            "requires_user_choice": True,
        },
    )
    return authorization_required(request, detected_error=detected_error)


def playwright_browser_authorization(
    skill_root: Path,
    *,
    blocked_capability: str,
    detected_error: str = "",
) -> dict[str, Any]:
    root = str(skill_root.resolve())
    request = DependencyRequest(
        dependency_id="playwright-chromium",
        dependency_name="Playwright Chromium browser",
        dependency_kind="browser-runtime",
        blocked_capability=blocked_capability,
        purpose="Provide a compatible headless browser when no usable installed Chrome, Edge, or Chromium executable is available.",
        installation_options=[
            {
                "scope": "current-user-cache",
                "target": root,
                "command": f'npx --prefix "{root}" playwright install chromium',
                "changes": "Downloads the Playwright-managed Chromium build into the user browser cache.",
                "recommended": True,
            }
        ],
        impact=[
            "Requires a substantial network download and additional disk space.",
            "Linux hosts may require separately authorized system libraries.",
        ],
        fallback={
            "available": True,
            "quality_loss": "Automated geometry remains unproven; only an explicitly accepted manual review is possible.",
            "requires_user_choice": True,
        },
    )
    return authorization_required(request, detected_error=detected_error)


def load_json_or_yaml(path: Path, *, document_label: str) -> Any:
    """Load JSON first and request authorization if YAML support is required but absent."""

    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            import yaml  # type: ignore[import-untyped]  # compatibility: optional YAML runtime
        except ImportError as exc:
            raise DependencyAuthorizationRequired(
                python_package_authorization(
                    PythonPackageRequest(
                        package="PyYAML",
                        module="yaml",
                        blocked_capability=f"Parse {document_label}",
                        purpose="Read the YAML input required by this design-governance command.",
                    ),
                    detected_error=str(exc),
                )
            ) from exc
        return yaml.safe_load(text)


def emit_result(payload: dict[str, Any], output: Path | None = None) -> int:
    """Write a result to the evidence path and stdout, then return its protocol exit code."""

    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    return AUTHORIZATION_EXIT_CODE if payload.get("status") == "authorization_required" else 0
