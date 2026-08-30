#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Dependency-free repository checks used locally and in CI."""

from __future__ import annotations

import csv
import json
import math
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "ROADMAP.md",
    "SAFETY.md",
    "SECURITY.md",
    "LICENSE.md",
    "LICENSES/GPL-3.0-or-later.txt",
    "LICENSES/CERN-OHL-S-2.0.txt",
    "LICENSES/CC-BY-4.0.txt",
    "docs/architecture/system.md",
    "docs/research/source-register.csv",
    "docs/safety/hazard-analysis.md",
    "protocol/manifests/vehicle-manifest.schema.json",
    "protocol/manifests/2025-model3-highland-candidate.json",
]

RAW_CAPTURE_SUFFIXES = {
    ".asc",
    ".bin",
    ".blf",
    ".dump",
    ".img",
    ".log",
    ".mf4",
    ".pcap",
    ".pcapng",
}

LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
SPDX_RE = re.compile(r"SPDX-License-Identifier:")
PATCH_MARKER_RE = re.compile(r"^\*{3} (?:Add|Update|Delete|End) File", re.MULTILINE)

VEHICLE_PILOT_REQUIRED_TESTS = {
    "CAN-001",
    "CAN-002",
    "CAN-003",
    "DISP-001",
    "DISP-002",
    "DISP-003",
    "INST-001",
    "INST-002",
    "PWR-001",
    "REL-001",
    "REV-001",
    "REV-002",
    "SAFE-001",
    "SAFE-002",
    "SAFE-003",
    "SAFE-004",
    "SAFE-005",
    "SAFE-006",
    "SAFE-007",
    "SAFE-008",
    "TOUCH-001",
    "TOUCH-002",
    "UPD-001",
}

SUPPORTED_REQUIRED_TESTS = VEHICLE_PILOT_REQUIRED_TESTS | {
    "PRIV-001",
    "PRIV-002",
    "PWR-002",
    "PWR-003",
    "REL-002",
    "REV-003",
    "SEC-001",
    "SEC-002",
    "SIG-001",
    "UI-001",
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def reject_json_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant {value}")


def load_json_strict(text: str) -> Any:
    return json.loads(text, parse_constant=reject_json_constant)


def check_required(errors: list[str]) -> None:
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            fail(errors, f"missing required file: {relative}")


JSON_TYPES = {
    "array": list,
    "boolean": bool,
    "integer": int,
    "null": type(None),
    "number": (int, float),
    "object": dict,
    "string": str,
}

SUPPORTED_SCHEMA_KEYS = {
    "$id",
    "$schema",
    "additionalProperties",
    "const",
    "description",
    "enum",
    "format",
    "items",
    "maximum",
    "minimum",
    "minItems",
    "minLength",
    "pattern",
    "properties",
    "required",
    "title",
    "type",
}


def schema_type_matches(value: Any, expected: str) -> bool:
    python_type = JSON_TYPES[expected]
    if expected in {"integer", "number"} and isinstance(value, bool):
        return False
    return isinstance(value, python_type)


def validate_schema_keywords(schema: Any, path: str, errors: list[str]) -> None:
    if not isinstance(schema, dict):
        return
    unknown = sorted(set(schema) - SUPPORTED_SCHEMA_KEYS)
    if unknown:
        fail(errors, f"schema {path}: validator does not implement keywords {unknown}")
    for name, child in schema.get("properties", {}).items():
        validate_schema_keywords(child, f"{path}.properties.{name}", errors)
    if isinstance(schema.get("items"), dict):
        validate_schema_keywords(schema["items"], f"{path}.items", errors)


def validate_instance(value: Any, schema: dict[str, Any], path: str, errors: list[str]) -> None:
    expected = schema.get("type")
    if expected is not None:
        expected_types = [expected] if isinstance(expected, str) else expected
        if not any(schema_type_matches(value, item) for item in expected_types):
            fail(errors, f"{path}: expected type {expected_types}, got {type(value).__name__}")
            return

    if "const" in schema and value != schema["const"]:
        fail(errors, f"{path}: must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        fail(errors, f"{path}: value {value!r} is not in {schema['enum']!r}")

    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            fail(errors, f"{path}: shorter than minLength {schema['minLength']}")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            fail(errors, f"{path}: does not match pattern {schema['pattern']!r}")
        if schema.get("format") == "date":
            try:
                date.fromisoformat(value)
            except ValueError:
                fail(errors, f"{path}: invalid ISO date")
        if schema.get("format") == "uri":
            parsed = urlparse(value)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                fail(errors, f"{path}: invalid HTTP(S) URI")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if not math.isfinite(value):
            fail(errors, f"{path}: numeric value must be finite")
            return
        if "minimum" in schema and value < schema["minimum"]:
            fail(errors, f"{path}: below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            fail(errors, f"{path}: above maximum {schema['maximum']}")

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            fail(errors, f"{path}: fewer than {schema['minItems']} items")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                validate_instance(item, item_schema, f"{path}[{index}]", errors)

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                fail(errors, f"{path}: missing required property {key!r}")
        if schema.get("additionalProperties") is False:
            for key in sorted(set(value) - set(properties)):
                fail(errors, f"{path}: unexpected property {key!r}")
        for key, child in properties.items():
            if key in value:
                validate_instance(value[key], child, f"{path}.{key}", errors)


def check_manifest_invariants(data: dict[str, Any], path: str, errors: list[str]) -> None:
    status = data.get("status")
    gates = data.get("feature_gates", {})
    risky_gates = (
        "external_video",
        "touch_to_local",
        "can_receive",
        "vehicle_installation",
        "moving_mode",
        "can_transmit",
    )

    unique_fields = (
        ("interfaces", "name"),
        ("harnesses", "harness_id"),
        ("capture_artifacts", "artifact_id"),
        ("validation", "test_id"),
        ("evidence", "id"),
    )
    for collection, key in unique_fields:
        values = [item.get(key) for item in data.get(collection, [])]
        duplicates = sorted({value for value in values if value and values.count(value) > 1})
        if duplicates:
            fail(errors, f"{path}: duplicate {collection}.{key} values {duplicates}")

    instance_ids = data.get("validated_vehicle_instance_ids", [])
    if len(instance_ids) != len(set(instance_ids)):
        fail(errors, f"{path}: validated vehicle instance IDs must be unique")
    if data.get("independent_vehicle_instances") != len(instance_ids):
        fail(errors, f"{path}: independent vehicle count must equal instance ID count")

    capture_hashes = [
        item.get("sha256") for item in data.get("capture_artifacts", []) if item.get("sha256")
    ]
    if len(capture_hashes) != len(set(capture_hashes)):
        fail(errors, f"{path}: capture artifact hashes must be unique")

    reviewer_names = [
        item.get("reviewer", "").strip() for item in data.get("reviewers", [])
    ]
    if len(reviewer_names) != len(set(reviewer_names)):
        fail(errors, f"{path}: reviewer identities must be distinct")

    if status in {"candidate", "retired"}:
        enabled = [name for name in risky_gates if gates.get(name)]
        if enabled:
            fail(errors, f"{path}: {status} manifest enables gated features {enabled}")
        return

    if status not in {"bench-verified", "vehicle-pilot", "supported"}:
        return

    vehicle = data.get("vehicle", {})
    build_range = vehicle.get("build_date_range", {})
    if build_range.get("start") and build_range.get("end"):
        try:
            reversed_range = date.fromisoformat(build_range["start"]) > date.fromisoformat(
                build_range["end"]
            )
        except ValueError:
            reversed_range = False
        if reversed_range:
            fail(errors, f"{path}: build-date range starts after it ends")
    required_identity = {
        "market": vehicle.get("market"),
        "plant": vehicle.get("plant"),
        "steering_side": None
        if vehicle.get("steering_side") == "unknown"
        else vehicle.get("steering_side"),
        "build_start": build_range.get("start"),
        "build_end": build_range.get("end"),
        "mcu_family": vehicle.get("mcu_family"),
    }
    unresolved = [name for name, value in required_identity.items() if value is None]
    if unresolved:
        fail(errors, f"{path}: promoted manifest has unresolved identity fields {unresolved}")
    if not any(item.strip() for item in vehicle.get("display_part_numbers", [])):
        fail(errors, f"{path}: promoted manifest needs a verified display part number")
    if data.get("tesla_reference", {}).get("program_id") is None:
        fail(errors, f"{path}: promoted manifest needs an exact Tesla program_id")

    interfaces = data.get("interfaces", [])
    if not interfaces:
        fail(errors, f"{path}: promoted manifest needs interfaces")
    allowed_pinout = {"reviewed", "bench-verified"}
    if any(item.get("pinout_status") not in allowed_pinout for item in interfaces):
        fail(errors, f"{path}: promoted manifest contains unreviewed interface pinouts")
    steering_side = vehicle.get("steering_side")
    mismatched_interfaces = [
        item.get("name")
        for item in interfaces
        if item.get("applies_to_steering_side") not in {steering_side, "both"}
    ]
    if mismatched_interfaces:
        fail(
            errors,
            f"{path}: interfaces do not apply to selected steering side: {mismatched_interfaces}",
        )
    if any(not (item.get("tesla_part_number") or "").strip() for item in interfaces):
        fail(errors, f"{path}: promoted interfaces need nonempty Tesla part numbers")

    harnesses = data.get("harnesses", [])
    if not harnesses:
        fail(errors, f"{path}: promoted manifest needs a reviewed bench harness")
    if any(item.get("status") not in allowed_pinout for item in harnesses):
        fail(errors, f"{path}: promoted manifest contains an unreviewed harness")
    interface_names = {item.get("name") for item in interfaces}
    invalid_endpoints = [
        item.get("harness_id")
        for item in harnesses
        if item.get("from_interface") not in interface_names
        or item.get("to_interface") not in interface_names
    ]
    if invalid_endpoints:
        fail(errors, f"{path}: harnesses reference missing interfaces {invalid_endpoints}")

    if data.get("protocol_profile", {}).get("status") != "bench-verified":
        fail(errors, f"{path}: promoted manifest needs a bench-verified protocol profile")
    if data.get("power_profile", {}).get("status") != "bench-verified":
        fail(errors, f"{path}: promoted manifest needs a bench-verified power profile")

    captures = data.get("capture_artifacts", [])
    validation = data.get("validation", [])
    reviewers = data.get("reviewers", [])
    if not captures:
        fail(errors, f"{path}: promoted manifest needs a hashed capture artifact")
    if not validation or any(item.get("status") != "pass" for item in validation):
        fail(errors, f"{path}: promoted manifest requires nonempty all-pass validation")
    if any(not item.get("evidence_sha256") for item in validation):
        fail(errors, f"{path}: every promoted validation result needs an evidence hash")
    if not reviewers:
        fail(errors, f"{path}: promoted manifest needs a named review record")

    protocol = data.get("protocol_profile", {})
    if gates.get("external_video") and not any(
        protocol.get(name)
        for name in ("edid_sha256", "displayid_sha256", "dpcd_sha256")
    ):
        fail(errors, f"{path}: external video needs a hashed display/link identity")
    if gates.get("touch_to_local") and not protocol.get("touch_profile_sha256"):
        fail(errors, f"{path}: local touch needs a hashed touch profile")
    if gates.get("can_receive"):
        can_profile = data.get("can_profile", {})
        if can_profile.get("status") != "bench-verified" or not can_profile.get(
            "signal_profile_sha256"
        ):
            fail(errors, f"{path}: CAN receive needs a bench-verified hashed signal profile")

    if status == "bench-verified" and gates.get("vehicle_installation"):
        fail(errors, f"{path}: bench-verified status cannot enable vehicle installation")

    if status in {"vehicle-pilot", "supported"}:
        if any(item.get("pinout_status") != "bench-verified" for item in interfaces):
            fail(errors, f"{path}: vehicle use requires bench-verified interfaces")
        if any(item.get("status") != "bench-verified" for item in harnesses):
            fail(errors, f"{path}: vehicle use requires bench-verified harnesses")
        if any(not (item.get("mating_part") or "").strip() for item in interfaces):
            fail(errors, f"{path}: vehicle use requires verified counter-mating parts")
        safe_state = data.get("safe_state", {})
        if safe_state.get("park_state_max_age_ms") is None:
            fail(errors, f"{path}: vehicle use needs a measured Park-state age bound")
        if safe_state.get("native_recovery_timeout_ms") is None:
            fail(errors, f"{path}: vehicle use needs a measured native-recovery bound")
        if not gates.get("vehicle_installation"):
            fail(errors, f"{path}: vehicle-pilot/supported status requires its explicit feature gate")
        if len(reviewers) < 2:
            fail(errors, f"{path}: vehicle use requires two independent review records")
        completed_tests = {item.get("test_id") for item in validation}
        missing_tests = sorted(VEHICLE_PILOT_REQUIRED_TESTS - completed_tests)
        if missing_tests:
            fail(errors, f"{path}: vehicle pilot is missing mandatory tests {missing_tests}")

    if status == "supported":
        if data.get("independent_vehicle_instances", 0) < 2:
            fail(errors, f"{path}: supported requires at least two independent vehicle instances")
        if len(captures) < 2:
            fail(errors, f"{path}: supported requires at least two hashed capture artifacts")
        captured_instances = {
            item.get("vehicle_instance_id")
            for item in captures
            if item.get("vehicle_instance_id")
        }
        if not set(instance_ids).issubset(captured_instances):
            fail(errors, f"{path}: supported captures do not cover every vehicle instance")
        completed_tests = {item.get("test_id") for item in validation}
        missing_tests = sorted(SUPPORTED_REQUIRED_TESTS - completed_tests)
        if missing_tests:
            fail(errors, f"{path}: supported profile is missing mandatory tests {missing_tests}")


def check_json(errors: list[str]) -> None:
    schema_path = ROOT / "protocol/manifests/vehicle-manifest.schema.json"
    try:
        schema = load_json_strict(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        fail(errors, f"invalid manifest schema: {exc}")
        return
    if not schema.get("required"):
        fail(errors, "manifest schema has no required keys")
    validate_schema_keywords(schema, "$schema", errors)

    manifest_dir = schema_path.parent
    for path in sorted(manifest_dir.glob("*.json")):
        if path == schema_path:
            continue
        try:
            data = load_json_strict(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError) as exc:
            fail(errors, f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
            continue
        validate_instance(data, schema, str(path.relative_to(ROOT)), errors)
        check_manifest_invariants(data, str(path.relative_to(ROOT)), errors)
        if data.get("status") == "supported" and len(data.get("evidence", [])) < 2:
            fail(errors, f"{path.relative_to(ROOT)}: supported requires at least two evidence entries")


def check_source_register(errors: list[str]) -> None:
    path = ROOT / "docs/research/source-register.csv"
    if not path.exists():
        return
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        aliases = {
            "id": {"id", "source_id"},
            "url": {"url", "source_url"},
            "accessed": {"accessed", "access_date", "accessed_date"},
        }
        chosen: dict[str, str] = {}
        for logical, names in aliases.items():
            match = next((name for name in names if name in fields), None)
            if not match:
                fail(errors, f"source register missing {logical} column")
            else:
                chosen[logical] = match
        if len(chosen) != len(aliases):
            return
        seen: set[str] = set()
        for line_number, row in enumerate(reader, start=2):
            source_id = (row.get(chosen["id"]) or "").strip()
            url = (row.get(chosen["url"]) or "").strip()
            accessed = (row.get(chosen["accessed"]) or "").strip()
            if not source_id or source_id in seen:
                fail(errors, f"source register line {line_number}: empty or duplicate id")
            seen.add(source_id)
            if not url.startswith(("https://", "http://")):
                fail(errors, f"source register line {line_number}: invalid URL")
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", accessed):
                fail(errors, f"source register line {line_number}: invalid access date")


def check_links(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                fail(errors, f"{path.relative_to(ROOT)}: link escapes repository: {target}")
                continue
            if not resolved.exists():
                fail(errors, f"{path.relative_to(ROOT)}: broken link: {target}")


def check_capture_policy(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if path.is_file() and ".git" not in path.parts and path.suffix.lower() in RAW_CAPTURE_SUFFIXES:
            fail(errors, f"raw capture must not be committed: {path.relative_to(ROOT)}")


def check_spdx(errors: list[str]) -> None:
    for path in sorted((ROOT / "tools").rglob("*.py")):
        head = "\n".join(path.read_text(encoding="utf-8").splitlines()[:8])
        if not SPDX_RE.search(head):
            fail(errors, f"{path.relative_to(ROOT)}: missing SPDX identifier")


def check_patch_artifacts(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if PATCH_MARKER_RE.search(text):
            fail(errors, f"{path.relative_to(ROOT)}: contains an apply-patch control marker")


def main() -> int:
    errors: list[str] = []
    check_required(errors)
    check_json(errors)
    check_source_register(errors)
    check_links(errors)
    check_capture_policy(errors)
    check_spdx(errors)
    check_patch_artifacts(errors)
    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
