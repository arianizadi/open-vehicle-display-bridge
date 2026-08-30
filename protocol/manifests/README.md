# Vehicle Manifests

Manifests are the compatibility boundary between generic bridge components and
a particular vehicle wiring/display revision.

- vehicle-manifest.schema.json defines the contract.
- 2025-model3-highland-candidate.json is deliberately incomplete until the
  owner's plant/build and physical part revision are resolved.
- An unsupported or candidate manifest must never enable a vehicle installation.

Use tools/new_vehicle_manifest.py to scaffold future or past Tesla revisions,
then tools/compare_vehicle_manifests.py to review differences. The generator
does not infer compatibility; it creates explicit unknowns that must be closed
with evidence and tests. See the
[onboarding workflow](../../docs/architecture/vehicle-onboarding.md).
