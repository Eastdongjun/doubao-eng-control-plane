#!/usr/bin/env python3
"""Build platform packages from the canonical Agent Skill."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "platforms" / "manifest.json"
LOCAL_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def skill_name(text: str) -> str:
    if not text.startswith("---"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    match = re.search(r"(?m)^name:\s*[\"']?([^\"'\r\n]+)[\"']?\s*$", text)
    if not match:
        raise ValueError("SKILL.md frontmatter is missing name")
    return match.group(1).strip()


def canonical_files(include_agents: bool) -> list[tuple[Path, Path]]:
    files = [(ROOT / "SKILL.md", Path("SKILL.md"))]
    for folder in ("references", "assets"):
        base = ROOT / folder
        if base.is_dir():
            files.extend(
                (path, path.relative_to(ROOT))
                for path in sorted(base.rglob("*"))
                if path.is_file()
            )
    if include_agents:
        base = ROOT / "agents"
        if base.is_dir():
            files.extend(
                (path, path.relative_to(ROOT))
                for path in sorted(base.rglob("*"))
                if path.is_file()
            )
    return files


def validate_source(manifest: dict) -> None:
    core = ROOT / "SKILL.md"
    text = core.read_text(encoding="utf-8")
    expected = manifest["skill"]["name"]
    actual = skill_name(text)
    if actual != expected:
        raise ValueError(f"manifest name {expected!r} != SKILL.md name {actual!r}")

    missing: list[str] = []
    for source, _ in canonical_files(include_agents=False):
        if source.suffix.lower() != ".md":
            continue
        for raw in LOCAL_LINK.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().split("#", 1)[0]
            if not target or "://" in target or target.startswith(("#", "mailto:")):
                continue
            resolved = (source.parent / target).resolve()
            if not resolved.is_file():
                missing.append(f"{source.relative_to(ROOT)} -> {target}")
    if missing:
        raise FileNotFoundError("Missing local references: " + ", ".join(sorted(set(missing))))


def safe_reset(path: Path, output_root: Path) -> None:
    resolved = path.resolve()
    output = output_root.resolve()
    if resolved == output or output not in resolved.parents:
        raise ValueError(f"Refusing to reset unsafe path: {resolved}")
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_files(destination: Path, include_agents: bool) -> None:
    for source, relative in canonical_files(include_agents):
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def zip_files(archive_path: Path, wrapper: str, files: list[tuple[Path, Path]]) -> Path:
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for source, relative in files:
            archive.write(source, (Path(wrapper) / relative).as_posix())
    return archive_path


def zip_directory(archive_path: Path, directory: Path) -> Path:
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for source in sorted(directory.rglob("*")):
            if source.is_file():
                archive.write(source, source.relative_to(directory.parent).as_posix())
    return archive_path


def build_trae(output: Path, manifest: dict) -> list[Path]:
    name = manifest["skill"]["name"]
    return [
        zip_files(
            output / "trae" / f"{name}.zip",
            name,
            canonical_files(include_agents=False),
        )
    ]


def build_portable(output: Path, manifest: dict) -> list[Path]:
    name = manifest["skill"]["name"]
    return [
        zip_files(
            output / "portable" / f"{name}.zip",
            name,
            canonical_files(include_agents=True),
        )
    ]


def build_openai(output: Path, manifest: dict) -> list[Path]:
    skill = manifest["skill"]
    name = skill["name"]
    marketplace = output / "openai-marketplace"
    plugin = marketplace / "plugins" / name
    safe_reset(plugin, output)
    copy_files(plugin / "skills" / name, include_agents=True)

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
            "developerName": skill["publisher"]["name"],
            "category": skill["category"],
            "capabilities": skill["capabilities"],
            "defaultPrompt": skill["default_prompts"],
        },
    }
    plugin_file = plugin / ".codex-plugin" / "plugin.json"
    plugin_file.parent.mkdir(parents=True, exist_ok=True)
    plugin_file.write_text(
        json.dumps(plugin_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    marketplace_manifest = {
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
    marketplace_file = marketplace / ".agents" / "plugins" / "marketplace.json"
    marketplace_file.parent.mkdir(parents=True, exist_ok=True)
    marketplace_file.write_text(
        json.dumps(marketplace_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    plugin_zip = zip_directory(output / "openai" / f"{name}-plugin.zip", plugin)
    return [marketplace_file, plugin_file, plugin_zip]


def build_coze(output: Path, manifest: dict) -> list[Path]:
    skill = manifest["skill"]
    name = skill["name"]
    package = output / "coze" / name
    safe_reset(package, output)
    shutil.copy2(ROOT / "platforms" / "coze" / "agent-prompt.md", package / "agent-prompt.md")

    knowledge = package / "knowledge"
    knowledge.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "SKILL.md", knowledge / "00-skill-core.md")
    for source in sorted((ROOT / "references").rglob("*")):
        if source.is_file():
            target = knowledge / source.relative_to(ROOT / "references")
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

    templates = package / "templates"
    if (ROOT / "assets").is_dir():
        shutil.copytree(ROOT / "assets", templates, dirs_exist_ok=True)

    guide = (
        "# 扣子导入说明\n\n"
        "1. 将 `agent-prompt.md` 正文粘贴到智能体系统提示词。\n"
        "2. 新建知识库并上传 `knowledge/` 中全部 Markdown。\n"
        "3. 将知识库绑定到智能体并启用检索。\n"
        "4. `templates/` 是可复制交付模板，不是知识规则。\n"
        "5. 仅在需要外部动作时配置联网、文件、设计、视频或代码工具。\n\n"
        f"生成来源：{skill['repository']}\n"
    )
    (package / "IMPORT.md").write_text(guide, encoding="utf-8")

    package_manifest = {
        "adapter": "coze-prompt-knowledge",
        "skill": name,
        "source": skill["repository"],
        "generated_from": [
            "SKILL.md",
            "references/",
            "assets/",
            "platforms/coze/agent-prompt.md",
        ],
        "knowledge_files": sorted(
            path.relative_to(package).as_posix()
            for path in knowledge.rglob("*")
            if path.is_file()
        ),
    }
    (package / "manifest.json").write_text(
        json.dumps(package_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    package_zip = zip_directory(output / "coze" / f"{name}-coze.zip", package)
    return [package / "agent-prompt.md", package / "manifest.json", package_zip]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--platform",
        choices=("all", "trae", "openai", "coze", "portable"),
        default="all",
    )
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()

    manifest = load_manifest()
    validate_source(manifest)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    builders = {
        "trae": build_trae,
        "openai": build_openai,
        "coze": build_coze,
        "portable": build_portable,
    }
    selected = tuple(builders) if args.platform == "all" else (args.platform,)
    artifacts: list[Path] = []
    for platform in selected:
        artifacts.extend(builders[platform](output, manifest))
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
