# ADR 0004: License code, hardware, and documentation explicitly

- Status: Accepted
- Date: 2026-08-30

## Context

The project is intended to be public and reusable, and it may integrate or
interoperate with GPL software such as Tesla Android, LIVI, OpenAuto, or related
phone-projection projects. Hardware source needs an open-hardware license, while
research documentation should be easy to share with attribution. Tesla, TI,
Apple, Google, and community materials have their own terms and cannot be
assumed redistributable merely because they are visible online.

Ambiguous or missing license information creates risk for contributors,
builders, and downstream forks.

## Decision

Use these default licenses for original project work:

- software and firmware: `GPL-3.0-or-later`;
- original hardware design source, schematics, PCB layouts, and mechanical
  source: `CERN-OHL-S-2.0`;
- original documentation and diagrams: `CC-BY-4.0`.

Every source file that supports comments receives an SPDX identifier. Repository
license texts, a third-party-notices file, source provenance, and a generated
SBOM accompany releases.

Third-party content retains its original license and is kept separable when
terms differ. DBCs, VSS material, code, schematics, captures, fonts, binary
blobs, and vendor reference designs are reviewed individually before import.
No-license code or CAD is reference-only and is not copied. Linking to a vendor
document does not grant permission to redistribute or modify it.

The repository will not contain leaked or extracted proprietary firmware,
service credentials, decryption keys, MFi credentials, Google service packages,
NDA material, or personal vehicle data. Reverse-engineering notes record lawful
source and capture provenance. Tesla names are used only for nominative
compatibility descriptions with an unaffiliated disclaimer.

Contributions use a Developer Certificate of Origin or equivalent provenance
attestation rather than assuming contributors have the right to submit copied
material.

## Consequences

### Positive

- Copyleft improvements to the main code and hardware remain available to the
  community.
- Contributors and builders can identify obligations by artifact type.
- Explicit provenance and SBOM practices reduce accidental contamination.

### Negative

- GPL and strong reciprocal hardware terms may not fit every commercial use.
- Mixed-license third-party dependencies require careful notices and source
  distribution.
- Some attractive reference implementations cannot be copied.
- App-store, MFi, Google Automotive Services, DRM, trademark, and patent issues
  are not solved by these licenses.

## Rejected alternatives

- **One license for the entire repository:** software, hardware source, docs,
  and imported data have different legal needs.
- **Permissive-only licensing:** permissive original code can be combined into a
  GPL distribution, but this policy intentionally keeps improvements to the
  project's core code and hardware reciprocal.
- **Treat public GitHub code or vendor schematics as automatically reusable:**
  publication without a license does not grant copying rights.

## Implementation notes

This ADR is a project policy, not legal advice. Before a public release, verify
that top-level license files, per-file SPDX tags, dependency manifests, notices,
and downloadable corresponding source agree. Material legal uncertainty blocks
distribution until reviewed.
