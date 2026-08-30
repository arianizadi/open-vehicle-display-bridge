# ADR 0002: Qualify one 2025 Model 3 Highland revision first

- Status: Accepted
- Date: 2026-08-30

## Context

Tesla display computers, panels, connectors, signaling, harnesses, touch paths,
and CAN definitions vary by build date and hardware generation. Marketing names
such as “Model 3” or “Highland” are not sufficiently precise compatibility
boundaries. Assuming that legacy Model 3 FPD-Link or CAN details apply to a 2025
Highland could damage hardware or create unsafe behavior.

The project owner has a 2025 Tesla Model 3 Highland, which provides a concrete
first target for lawful observation and reversible static testing after bench
qualification.

## Decision

The first target is the owner's exact 2025 Model 3 Highland hardware
configuration. The public profile will identify it with non-personal build and
hardware metadata, not a VIN.

Support is expressed through versioned vehicle-revision manifests and adapters.
Each profile includes connector and pin data, measured video/touch transport,
power behavior, pinned CAN definitions, maximum signal ages, hardware and
firmware compatibility, evidence, maturity, and explicit exclusions.

Profiles are deny-by-default:

- `candidate` profiles are documentation/identification only;
- `bench-verified` profiles may run only on isolated fixtures;
- `vehicle-pilot` profiles may be used only in the documented stationary/Park-only
  conditions;
- `supported` requires the stated matrix and independent-instance evidence for
  the enumerated profile, not automotive certification or universal compatibility;
- `retired` profiles keep history but enable no gated feature.

Past and future Tesla revisions are onboarded by creating a new profile,
adapter, fixture configuration, hazard delta, and evidence set. A matching model
name or connector does not allow inheritance of validation status.

## Consequences

### Positive

- Research is grounded in equipment the project can actually inspect.
- Claims remain auditable and do not overgeneralize legacy findings.
- Compatibility growth follows a repeatable boundary rather than conditional
  code scattered across the UI.
- A Tesla software update can invalidate one adapter without corrupting all
  profiles.

### Negative

- Initial compatibility is intentionally narrow.
- A representative salvaged display/source/harness may be difficult or costly
  to obtain.
- Every added vehicle revision requires repeated hardware-in-the-loop and fault
  testing.

## Rejected alternatives

- **Start with pre-Highland because public teardowns exist:** this would not
  address the owner's vehicle and could embed obsolete link assumptions.
- **Claim all Model 3/Model Y compatibility:** there is no evidence for a single
  electrical or protocol configuration across those vehicles.
- **Runtime auto-detection with best-effort defaults:** misidentification could
  select an unsafe link or decode Park incorrectly. Unknown always locks native.

## Review trigger

Review this ADR when the exact first-target hardware identifiers are known, or
when proposing a second vehicle revision. Refinement of the profile is expected;
weakening deny-by-default behavior requires a new ADR.
