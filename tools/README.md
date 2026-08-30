# Tools

Repository and bench automation lives here. Tools must be deterministic,
dependency-light where practical, and safe by default. A command that can
energize hardware must require an explicit target manifest and print its hash.

- validate_repo.py checks repository invariants.
- new_vehicle_manifest.py scaffolds an unsupported revision with explicit
  unknowns.
- compare_vehicle_manifests.py marks safety-relevant differences as blocking
  review items.
- Future tools will generate continuity sheets, harness labels, cross-revision
  diffs, EDID/DPCD reports, and privacy-scrubbed replay fixtures.
