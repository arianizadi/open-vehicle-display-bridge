# Contributing

Thanks for helping build a safer, reproducible open vehicle interface.

## Before opening a change

1. Read [SAFETY.md](SAFETY.md), [SECURITY.md](SECURITY.md), and the
   [clean-room policy](docs/legal/clean-room-policy.md).
2. Search existing issues and declare the exact vehicle revision or state that
   the work is vehicle-independent.
3. Do not upload proprietary firmware, leaked service material, secrets,
   authentication chips/keys, personal vehicle data, VINs, precise GPS traces,
   or unexplained binary captures.
4. Include provenance, measurement setup, uncertainty, and a reproducible test.

## Evidence labels

Use one of these labels for technical claims:

- **confirmed-official** — directly supported by public manufacturer material;
- **confirmed-measured** — reproducible measurement with setup and raw-data hash;
- **independent-report** — credible third-party observation, not yet reproduced;
- **inferred** — reasoned from known behavior but not directly observed;
- **unknown** — intentionally unresolved.

Do not silently promote an inference into a pinout, compatibility claim, or
safety requirement.

## Change requirements

- Keep vehicle-specific behavior inside manifests and adapters.
- Add tests with behavior changes.
- Update hazards when changing video, touch, power, CAN, update, or selector
  behavior.
- Original code must carry an SPDX license identifier.
- Third-party material must retain its license and be listed in
  [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
- Run: python3 tools/validate_repo.py

Hardware changes need source schematics, design rules, manufacturing outputs,
and a reviewed fail-native analysis. Road tests are not accepted as a substitute
for bench evidence.

## Pull requests

Explain the problem, target manifest, evidence, risks, validation, and rollback.
Safety-affecting changes require two reviewers and must not be merged by their
author alone.

## Developer Certificate of Origin

By contributing, you certify the
[Developer Certificate of Origin 1.1](https://developercertificate.org/).
Sign every commit with:

    git commit -s

The Signed-off-by line attests that you have the right to submit the work under
the project's licenses. Maintainers verify signoffs during review; unsigned
external contributions are not merged.
