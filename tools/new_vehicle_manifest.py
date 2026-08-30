#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Scaffold an intentionally unsupported vehicle-revision manifest."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "protocol/manifests"


def slug(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if len(normalized) < 3:
        raise argparse.ArgumentTypeError("identifier must contain at least three characters")
    return normalized


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a candidate manifest containing explicit unknowns."
    )
    parser.add_argument("manifest_id", type=slug)
    parser.add_argument("--make", default="Tesla")
    parser.add_argument("--model", required=True)
    parser.add_argument("--model-year", type=int, required=True)
    parser.add_argument("--generation", required=True)
    parser.add_argument("--market")
    parser.add_argument("--plant")
    parser.add_argument(
        "--steering-side",
        choices=("unknown", "LHD", "RHD"),
        default="unknown",
    )
    parser.add_argument("--reference-index-url", required=True)
    args = parser.parse_args()

    output = OUTPUT_DIR / f"{args.manifest_id}.json"
    if output.exists():
        parser.error(f"refusing to overwrite {output.relative_to(ROOT)}")

    data = {
        "schema_version": "0.2.0",
        "manifest_revision": 1,
        "manifest_id": args.manifest_id,
        "status": "candidate",
        "exact_match_required": True,
        "independent_vehicle_instances": 0,
        "validated_vehicle_instance_ids": [],
        "vehicle": {
            "make": args.make,
            "model": args.model,
            "generation": args.generation,
            "model_year": args.model_year,
            "market": args.market,
            "plant": args.plant,
            "steering_side": args.steering_side,
            "build_date_range": {"start": None, "end": None},
            "mcu_family": None,
            "autopilot_hardware": None,
            "display_part_numbers": [],
            "tesla_software_versions": [],
        },
        "tesla_reference": {
            "program_id": None,
            "candidate_program_ids": [],
            "index_url": args.reference_index_url,
            "connector_reference_url": None,
        },
        "interfaces": [],
        "harnesses": [],
        "protocol_profile": {
            "status": "unknown",
            "main_transport": None,
            "transport_confidence": "unknown",
            "native_width_px": None,
            "native_height_px": None,
            "refresh_hz": None,
            "lane_count": None,
            "link_rate": None,
            "edid_sha256": None,
            "displayid_sha256": None,
            "dpcd_sha256": None,
            "aux_hpd_profile_sha256": None,
            "touch_transport": None,
            "touch_profile_sha256": None,
        },
        "power_profile": {
            "status": "unknown",
            "platform_class": None,
            "display_rail_net_name": None,
            "accessory_nominal_max_v": None,
            "measured_awake_min_v": None,
            "measured_awake_max_v": None,
            "startup_peak_a": None,
            "sleep_current_ma": None,
            "transient_profile_sha256": None,
        },
        "can_profile": {
            "status": "unknown",
            "access_connector": None,
            "bitrate_bps": None,
            "physical_mode": "receive-only",
            "termination_ohms_added": 0,
            "signal_profile_sha256": None,
            "source_software_version": None,
            "notes": "No access point or signal is supported until exact-revision validation.",
        },
        "safe_state": {
            "deenergized_source": "factory-native",
            "fault_source": "factory-native",
            "required_native_conditions": [
                "boot",
                "shutdown",
                "reverse",
                "stale-or-unknown-state",
                "watchdog-fault",
                "physical-bypass",
            ],
            "park_state_max_age_ms": None,
            "native_recovery_timeout_ms": None,
        },
        "feature_gates": {
            "bench_identification": True,
            "external_video": False,
            "touch_to_local": False,
            "can_receive": False,
            "vehicle_installation": False,
            "moving_mode": False,
            "can_transmit": False,
        },
        "capture_artifacts": [],
        "validation": [],
        "evidence": [],
        "reviewers": [],
    }
    output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    try:
        display_path = output.relative_to(ROOT)
    except ValueError:
        display_path = output
    print(display_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
