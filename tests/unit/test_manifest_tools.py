#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "tools/compare_vehicle_manifests.py"
SPEC = importlib.util.spec_from_file_location("manifest_diff", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ManifestDiffTests(unittest.TestCase):
    def test_connector_change_is_blocking(self) -> None:
        before = {"interfaces": [{"connector_ref": "X861"}]}
        after = {"interfaces": [{"connector_ref": "X999"}]}
        rows = MODULE.changes(before, after)
        self.assertEqual(rows[0][3], "BLOCKING")

    def test_evidence_change_requires_review(self) -> None:
        before = {"evidence": [{"id": "A"}]}
        after = {"evidence": [{"id": "B"}]}
        rows = MODULE.changes(before, after)
        self.assertEqual(rows[0][3], "REVIEW")

    def test_equal_documents_have_no_changes(self) -> None:
        value = {"vehicle": {"model": "Model 3"}, "interfaces": []}
        self.assertEqual(MODULE.changes(value, value), [])

    def test_status_promotion_is_blocking(self) -> None:
        rows = MODULE.changes(
            {"status": "candidate"},
            {"status": "supported"},
        )
        self.assertEqual(rows[0][3], "BLOCKING")

    def test_feature_enablement_is_blocking(self) -> None:
        rows = MODULE.changes(
            {"feature_gates": {"external_video": False}},
            {"feature_gates": {"external_video": True}},
        )
        self.assertEqual(rows[0][3], "BLOCKING")


if __name__ == "__main__":
    unittest.main()
