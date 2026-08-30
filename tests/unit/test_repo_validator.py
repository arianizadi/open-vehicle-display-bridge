#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "tools/validate_repo.py"
SPEC = importlib.util.spec_from_file_location("repo_validator", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

GENERATOR_PATH = ROOT / "tools/new_vehicle_manifest.py"
GENERATOR_SPEC = importlib.util.spec_from_file_location("manifest_generator", GENERATOR_PATH)
assert GENERATOR_SPEC and GENERATOR_SPEC.loader
GENERATOR = importlib.util.module_from_spec(GENERATOR_SPEC)
GENERATOR_SPEC.loader.exec_module(GENERATOR)


class SchemaValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(
            (ROOT / "protocol/manifests/vehicle-manifest.schema.json").read_text()
        )
        cls.candidate = json.loads(
            (ROOT / "protocol/manifests/2025-model3-highland-candidate.json").read_text()
        )

    def test_candidate_satisfies_full_schema(self) -> None:
        errors: list[str] = []
        MODULE.validate_instance(self.candidate, self.schema, "candidate", errors)
        self.assertEqual(errors, [])

    def test_nested_extra_property_is_rejected(self) -> None:
        value = json.loads(json.dumps(self.candidate))
        value["vehicle"]["guess_from_year"] = True
        errors: list[str] = []
        MODULE.validate_instance(value, self.schema, "candidate", errors)
        self.assertTrue(any("unexpected property" in error for error in errors))

    def test_status_flip_cannot_promote_candidate(self) -> None:
        value = json.loads(json.dumps(self.candidate))
        value["status"] = "supported"
        errors: list[str] = []
        MODULE.check_manifest_invariants(value, "candidate", errors)
        self.assertGreater(len(errors), 5)

    def test_candidate_cannot_enable_vehicle_installation(self) -> None:
        value = json.loads(json.dumps(self.candidate))
        value["feature_gates"]["vehicle_installation"] = True
        errors: list[str] = []
        MODULE.check_manifest_invariants(value, "candidate", errors)
        self.assertTrue(any("gated features" in error for error in errors))

    def test_generator_output_satisfies_current_schema(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            arguments = [
                "new_vehicle_manifest.py",
                "generated-contract-test",
                "--model",
                "Model 3",
                "--model-year",
                "2025",
                "--generation",
                "Highland",
                "--reference-index-url",
                "https://service.tesla.com/docs/Model3/ElectricalReference/",
            ]
            with patch.object(GENERATOR, "OUTPUT_DIR", Path(temp_dir)), patch.object(
                sys, "argv", arguments
            ):
                self.assertEqual(GENERATOR.main(), 0)
            generated = json.loads(
                (Path(temp_dir) / "generated-contract-test.json").read_text()
            )
            errors: list[str] = []
            MODULE.validate_instance(generated, self.schema, "generated", errors)
            self.assertEqual(errors, [])

    def test_non_finite_json_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            MODULE.load_json_strict('{"value": NaN}')

    def test_reversed_build_range_is_rejected_on_promotion(self) -> None:
        value = json.loads(json.dumps(self.candidate))
        value["status"] = "supported"
        value["vehicle"]["build_date_range"] = {
            "start": "2025-12-01",
            "end": "2025-01-01",
        }
        errors: list[str] = []
        MODULE.check_manifest_invariants(value, "candidate", errors)
        self.assertTrue(any("starts after it ends" in error for error in errors))

    def test_steering_side_mismatch_is_rejected_on_promotion(self) -> None:
        value = json.loads(json.dumps(self.candidate))
        value["status"] = "supported"
        value["vehicle"]["steering_side"] = "RHD"
        errors: list[str] = []
        MODULE.check_manifest_invariants(value, "candidate", errors)
        self.assertTrue(any("selected steering side" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
