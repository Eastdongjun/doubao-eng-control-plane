import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.capability_router import route
from scripts.dependency_contract import (
    DependencyAuthorizationRequired,
    load_json_or_yaml,
    playwright_package_authorization,
)
from scripts.design_gate import check
from scripts.evaluate_aesthetic import evaluate
from scripts.layout_fingerprint import audit as audit_layout
from scripts.loading_manifest import audit as audit_loading
from scripts.regression_catalog import audit as audit_catalog
from scripts.research_cache import digest
from scripts.research_coverage import validate
from scripts.run_boundary_audit import (
    classify_dependency_failure,
    parse_authorization_result,
)
from scripts.svg_lint import audit as audit_svg
from scripts.trend_evidence import audit as audit_trends
from scripts.typography_layout_audit import audit as audit_typography
from scripts.visual_regression import compare as compare_visual


class ExecutionContractTests(unittest.TestCase):
    def test_visual_unresolved_routes_research_and_typography(self):
        result = route({"mode": "visual", "authority": "unresolved", "visual_stakes": 4, "mixed_script": True})
        ids = {item["id"] for item in result["required_capabilities"]}
        self.assertTrue({"research", "aesthetic", "typography", "layout"}.issubset(ids))
        self.assertEqual(result["evidence_status"], "unproven")

    def test_unverified_research_cannot_approve_aesthetic_direction(self):
        result = evaluate({
            "authority": "research-derived",
            "research_status": "unproven",
            "candidates": [{
                "name": "candidate",
                "scores": {key: 4 for key in (
                    "business_fit", "audience_fit", "hierarchy", "brand_specificity",
                    "accessibility", "feasibility", "distinctiveness", "trend_half_life",
                )},
                "gates": {"business_fit": True, "hierarchy": True, "accessibility": True},
            }],
        })
        self.assertEqual(result["status"], "unproven")
        self.assertIsNone(result["winner"])

    def test_research_requires_lanes_and_saturation(self):
        result = validate({"sources": [], "required_lanes": ["lineage", "category"], "saturation_test_passed": False})
        self.assertEqual(result["status"], "unproven")
        self.assertEqual(set(result["missing_lanes"]), {"lineage", "category"})

    def test_gate_blocks_missing_proof(self):
        with tempfile.TemporaryDirectory() as directory:
            result = check({"mode": "visual", "evidence_status": "approved", "decision_owner": "owner"}, Path(directory))
        self.assertEqual(result["status"], "blocked")

    def test_svg_audit_rejects_missing_viewbox_and_name(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "icon.svg"
            path.write_text('<svg><path d="M0 0"/></svg>', encoding="utf-8")
            result = audit_svg(Path(directory), True)
        reasons = {item["reason"] for item in result["findings"]}
        self.assertIn("missing_viewBox", reasons)
        self.assertIn("accessible_name_missing", reasons)

    def test_layout_fingerprint_requires_material_difference(self):
        result = audit_layout({"required_distinct": 2, "candidates": [{"name": "a", "canvas": "single", "navigation": "top", "entry": "task", "information_units": "list", "density_curve": "constant", "mobile_transform": "stack"}]})
        self.assertEqual(result["status"], "blocked")

    def test_loading_manifest_blocks_deferred_critical_meaning(self):
        result = audit_loading({"resources": [{"id": "heading", "kind": "critical-meaning", "priority": "deferred-visible"}]})
        self.assertEqual(result["status"], "blocked")

    def test_typography_fixture_reports_unowned_correction(self):
        result = audit_typography({"spacing_tokens": ["8"], "samples": [{"text": "中 A 1", "script_roles": ["CJK", "Latin", "numeral"], "font_family": "sans", "line_height": "24px", "baseline_status": "verified", "optical_correction": True}]})
        self.assertEqual(result["status"], "blocked")

    def test_catalog_requires_cross_industry_states(self):
        result = audit_catalog({"minimum_industries": 3, "cases": [{"industry": "finance", "viewports": ["desktop"], "states": ["default"], "baseline": "x"}]})
        self.assertEqual(result["status"], "blocked")

    def test_trend_evidence_and_cache_are_deterministic(self):
        trend = {"trends": [{"name": "x", "source": "https://example.com", "date": "2026-08-28", "mechanism": "layering", "project_fit": "secondary", "expiry_risk": "high", "rejected_surface": "primary action"}]}
        self.assertEqual(audit_trends(trend)["status"], "verified")
        self.assertEqual(digest("same"), digest("same"))

    def test_dependency_contract_requires_explicit_user_choice(self):
        payload = playwright_package_authorization(
            Path("."),
            blocked_capability="Boundary audit",
            detected_error="Cannot find module 'playwright'",
        )
        self.assertEqual(payload["status"], "authorization_required")
        self.assertEqual(payload["schema_version"], "2.0")
        self.assertEqual(payload["next_action"], "ask_user_before_install")
        self.assertTrue(payload["fallback"]["requires_user_choice"])
        self.assertIn("npm install --prefix", payload["installation_options"][0]["command"])

    def test_boundary_dependency_failure_becomes_authorization_request(self):
        payload = classify_dependency_failure(
            "Error: Playwright is required; Cannot find module 'playwright'",
            Path("."),
        )
        self.assertIsNotNone(payload)
        assert payload is not None
        self.assertEqual(payload["dependency"]["id"], "playwright")
        self.assertEqual(payload["status"], "authorization_required")
        self.assertEqual(parse_authorization_result(__import__("json").dumps(payload)), payload)

    def test_yaml_dependency_raises_authorization_instead_of_plain_error(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "task.yaml"
            manifest.write_text("mode: visual\n", encoding="utf-8")
            real_import = __import__

            def without_yaml(name, *args, **kwargs):
                if name == "yaml":
                    raise ImportError("simulated missing PyYAML")
                return real_import(name, *args, **kwargs)

            with (
                patch("builtins.__import__", side_effect=without_yaml),
                self.assertRaises(DependencyAuthorizationRequired) as raised,
            ):
                load_json_or_yaml(manifest, document_label="task manifest")
        self.assertEqual(raised.exception.payload["dependency"]["id"], "yaml")

    def test_visual_regression_does_not_silently_fallback_without_pillow(self):
        with tempfile.TemporaryDirectory() as directory:
            baseline = Path(directory) / "baseline.png"
            candidate = Path(directory) / "candidate.png"
            baseline.write_bytes(b"baseline")
            candidate.write_bytes(b"candidate")
            real_import = __import__

            def without_pillow(name, *args, **kwargs):
                if name == "PIL":
                    raise ImportError("simulated missing Pillow")
                return real_import(name, *args, **kwargs)

            with patch("builtins.__import__", side_effect=without_pillow):
                result = compare_visual(baseline, candidate, 0.02)
                fallback = compare_visual(baseline, candidate, 0.02, allow_binary_fallback=True)
        self.assertEqual(result["status"], "authorization_required")
        self.assertTrue(fallback["fallback_authorized"])


if __name__ == "__main__":
    unittest.main()
