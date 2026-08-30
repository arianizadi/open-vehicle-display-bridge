#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Render a deterministic, safety-aware diff of two vehicle manifests."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


BLOCKING_PREFIXES = (
    "can_profile",
    "exact_match_required",
    "feature_gates",
    "harnesses",
    "independent_vehicle_instances",
    "interfaces",
    "manifest_id",
    "manifest_revision",
    "power_profile",
    "protocol_profile",
    "safe_state",
    "schema_version",
    "status",
    "tesla_reference",
    "vehicle",
)


def flatten(value: Any, prefix: str = "") -> dict[str, Any]:
    if isinstance(value, dict):
        output: dict[str, Any] = {}
        for key in sorted(value):
            child = f"{prefix}.{key}" if prefix else key
            output.update(flatten(value[key], child))
        return output
    if isinstance(value, list):
        return {prefix: json.dumps(value, sort_keys=True, separators=(",", ":"))}
    return {prefix: value}


def changes(left: dict[str, Any], right: dict[str, Any]) -> list[tuple[str, Any, Any, str]]:
    before = flatten(left)
    after = flatten(right)
    rows = []
    for path in sorted(before.keys() | after.keys()):
        old = before.get(path, "<missing>")
        new = after.get(path, "<missing>")
        if old == new:
            continue
        severity = "BLOCKING" if path.startswith(BLOCKING_PREFIXES) else "REVIEW"
        rows.append((path, old, new, severity))
    return rows


def display(value: Any) -> str:
    rendered = json.dumps(value, sort_keys=True) if not isinstance(value, str) else value
    return rendered.replace("|", "\\|").replace("\n", " ")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("--fail-on-blocking", action="store_true")
    args = parser.parse_args()

    before = json.loads(args.before.read_text(encoding="utf-8"))
    after = json.loads(args.after.read_text(encoding="utf-8"))
    rows = changes(before, after)

    print("| Classification | Field | Before | After |")
    print("| --- | --- | --- | --- |")
    for path, old, new, severity in rows:
        print(f"| {severity} | {path} | {display(old)} | {display(new)} |")
    if not rows:
        print("| NONE | - | - | - |")

    blocking = sum(row[3] == "BLOCKING" for row in rows)
    print(f"\nBlocking changes: {blocking}; review changes: {len(rows) - blocking}")
    return 2 if args.fail_on_blocking and blocking else 0


if __name__ == "__main__":
    raise SystemExit(main())
