# Clean-Room and Research Policy

This project supports lawful interoperability research. It does not authorize
access to hardware, networks, software, or data without permission. Laws vary;
contributors are responsible for obtaining legal advice where appropriate.

## Allowed sources

- public manufacturer service information, connector references, and datasheets;
- lawfully purchased or salvaged hardware;
- measurements made on equipment the researcher owns or is authorized to use;
- independently written tests, code, schematics, and documentation; and
- compatibly licensed open-source projects with preserved notices.

## Prohibited inputs

- leaked or access-controlled source code, service files, signing material, or
  credentials;
- competitor firmware, filesystem images, proprietary binaries, or decompiled
  code unless separately reviewed and clearly lawful for the exact use;
- NDA material;
- MFi authentication keys/chips or Google/DRM secrets;
- VINs, precise location histories, phone data, account tokens, or other
  personal information; and
- copied PCB layouts, artwork, trademarks, or trade dress.

## Evidence process

Every compatibility fact must identify its source, access date, revision,
confidence, and whether it was observed or inferred. Raw captures stay outside
Git; commit only minimal, privacy-scrubbed fixtures plus a cryptographic hash
and acquisition notes. At least two people review connector pinouts before
power is applied.

Keep observation and implementation separable: the evidence pack says what was
observed; original design documents explain the independently chosen solution.
Do not copy expressive implementation details merely because behavior must be
compatible.

## US interoperability context

US copyright rules include limited exemptions for diagnosis, repair, lawful
modification, and access to vehicle operational data, and 17 U.S.C. § 1201(f)
addresses interoperability. Those provisions have conditions and do not create
immunity from safety, contract, privacy, anti-tampering, patent, or other law.
See the linked primary sources in the source register. This document is not
legal advice.
