#!/usr/bin/env python3
"""Build platform adapters from the canonical Agent Skill without duplicating sources."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "platforms" / "manifest.json"
LOCAL_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def frontmatter_name(skill_text: str) -> str:
    if not skill_text.startswith("---"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    match = re.search(r"(?m)^name:\s*[\"']?([^\"'\r\n]+)[\"']?\s*$", skill_text)
    if not match:
        raise ValueError("SKILL.md frontmatter is missing name")
    return match.group(1).strip()


def validate_source(manifest: dict) -> None:
    skill_file = ROOT / "SKILL.md"
    if not skill_file.is_file():
        raise FileNotFoundError(skill_file)
    skill_text = skill_file.read_text(encoding="utf-8")
    expected_name = manifest["skill"]["name"]
    actual_name = frontmatter_name(skill_text)
    if actual_name != expected_name:
        raise ValueError(f"manifest name {expected_name!r} != SKILL.md name {actual_name!r}")

    missing: list[str] = []
    for raw_target in LOCAL_LINK.findall(skill_text):
        target = raw_target.strip().split("#", 1)[0]
        if not target or "://" in target or target.startswith(("#", "mailto:")):
            continue
        if not (ROOT / target).resolve().is_file():
            missing.append(target)
    if missing:
        raise FileNotFoundError("Missing local references: " + ", ".join(sorted(set(missing))))


def canonical_files(include_openai_metadata: bool) -> list[tuple[Path, Path]]:
    files: list[tuple[Path, Path]] = [(ROOT / "SKILL.md", Path("SKILL.md"))]
    for folder in ("references", "assets", "templates", "examples"):
        base = ROOT / folder
        if base.is_dir():
            files.extend((path, path.relative_to(ROOT)) for path in sorted(base.rglob("*")) if path.is_file())
    if include_openai_metadata:
        base = ROOT / "agents"
        if base.is_dir():
            files.extend((path, path.relative_to(ROOT)) for path in sorted(base.rglob("*")) if path.is_file())
    return files


def copy_canonical(destination: Path, include_openai_metadata: bool) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for source, relative in canonical_files(include_openai_metadata):
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def reset_directory(path: Path, output_root: Path) -> None:
    resolved_path = path.resolve()
    resolved_output = output_root.resolve()
    if resolved_path == resolved_output or resolved_output not in resolved_path.parents:
        raise ValueError(f"Refusing to reset unsafe path: {resolved_path}")
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def zip_files(zip_path: Path, wrapper: str, files: list[tuple[Path, Path]]) -> Path:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source, relative in files:
            archive.write(source, (Path(wrapper) / relative).as_posix())
    return zip_path


def zip_directory(zip_path: Path, directory: Path) -> Path:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source in sorted(directory.rglob("*")):
            if source.is_file():
                archive.write(source, source.relative_to(directory.parent).as_posix())
    return zip_path


def build_trae(output_root: Path, manifest: dict) -> list[Path]:
    name = manifest["skill"]["name"]
    artifact = output_root / "trae" / f"{name}.zip"
    zip_files(artifact, name, canonical_files(include_openai_metadata=False))
    return [artifact]


def build_portable(output_root: Path, manifest: dict) -> list[Path]:
    name = manifest["skill"]["name"]
    artifact = output_root / "portable" / f"{name}.zip"
    zip_files(artifact, name, canonical_files(include_openai_metadata=True))
    return [artifact]


def build_openai(output_root: Path, manifest: dict) -> list[Path]:
    skill = manifest["skill"]
    name = skill["name"]
    marketplace_root = output_root / "openai-marketplace"
    plugin_root = marketplace_root / "plugins" / name
    reset_directory(plugin_root, output_root)
    copy_canonical(plugin_root / "skills" / name, include_openai_metadata=True)

    plugin_manifest = {
        "name": name,
        "version": skill["version"],
        "description": skill["long_description"],
        "author": skill["publisher"],
        "repository": skill["repository"],
        "keywords": skill["keywords"],
        "skills": "./skills/",
        "interface": {
            "displayName": skill["display_name"],
            "shortDescription": skill["short_description"],
            "longDescription": skill["long_description"],
            "developerName": "qlhouseClub",
            "category": skill["category"],
            "capabilities": skill["capabilities"],
            "defaultPrompt": skill["default_prompts"],
        },
    }
    plugin_manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    plugin_manifest_path.parent.mkdir(parents=True, exist_ok=True)
    plugin_manifest_path.write_text(json.dumps(plugin_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    marketplace = {
        "name": f"{name}-local",
        "interface": {"displayName": f"{skill['display_name']} Local"},
        "plugins": [
            {
                "name": name,
                "source": {"source": "local", "path": f"./plugins/{name}"},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": skill["category"],
            }
        ],
    }
    marketplace_path = marketplace_root / ".agents" / "plugins" / "marketplace.json"
    marketplace_path.parent.mkdir(parents=True, exist_ok=True)
    marketplace_path.write_text(json.dumps(marketplace, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    plugin_zip = output_root / "openai" / f"{name}-plugin.zip"
    zip_directory(plugin_zip, plugin_root)
    return [marketplace_path, plugin_manifest_path, plugin_zip]


def build_coze(output_root: Path, manifest: dict) -> list[Path]:
    skill = manifest["skill"]
    name = skill["name"]
    package_root = output_root / "coze" / name
    reset_directory(package_root, output_root)
    prompt_source = ROOT / "platforms" / "coze" / "agent-prompt.md"
    shutil.copy2(prompt_source, package_root / "agent-prompt.md")

    knowledge_root = package_root / "knowledge"
    knowledge_root.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "SKILL.md", knowledge_root / "00-skill-core.md")
    references = ROOT / "references"
    if references.is_dir():
        for source in sorted(references.rglob("*")):
            if source.is_file():
                target = knowledge_root / source.relative_to(references)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)

    import_guide = f"""# 扣子导入说明\n\n1. 新建智能体，将 `agent-prompt.md` 的正文粘贴到系统提示词。\n2. 新建知识库，上传 `knowledge/` 中的全部 Markdown 文件。\n3. 将知识库绑定到智能体，并开启知识检索。\n4. 仅在需要外部动作时再配置插件、工作流、数据库或 API。\n5. 用真实任务测试检索命中、规则遵循、事实标注和输出深度。\n\n生成来源：{skill['repository']}\n"""
    (package_root / "IMPORT.md").write_text(import_guide, encoding="utf-8")
    package_manifest = {
        "adapter": "coze-prompt-knowledge",
        "skill": name,
        "source": skill["repository"],
        "generated_from": ["SKILL.md", "references/", "platforms/coze/agent-prompt.md"],
        "knowledge_files": sorted(path.relative_to(package_root).as_posix() for path in knowledge_root.rglob("*") if path.is_file()),
    }
    (package_root / "manifest.json").write_text(
        json.dumps(package_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    package_zip = output_root / "coze" / f"{name}-coze.zip"
    zip_directory(package_zip, package_root)
    return [package_root / "agent-prompt.md", package_root / "manifest.json", package_zip]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--platform",
        choices=("all", "trae", "openai", "coze", "portable"),
        default="all",
        help="Adapter to build. 'portable' is suitable for manual Hermes/OpenClaw installation.",
    )
    parser.add_argument("--output", type=Path, default=ROOT / "dist", help="Output directory")
    args = parser.parse_args()

    manifest = load_manifest()
    validate_source(manifest)
    output_root = args.output.resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    builders = {
        "trae": build_trae,
        "openai": build_openai,
        "coze": build_coze,
        "portable": build_portable,
    }
    selected = tuple(builders) if args.platform == "all" else (args.platform,)
    artifacts: list[Path] = []
    for platform in selected:
        artifacts.extend(builders[platform](output_root, manifest))

    print(
        json.dumps(
            {
                "skill": manifest["skill"]["name"],
                "platform": args.platform,
                "artifacts": [str(path.resolve()) for path in artifacts],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
