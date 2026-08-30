# ADR 0003: Normalize vehicle signals behind revision adapters

- Status: Accepted
- Date: 2026-08-30

## Context

Tesla CAN signal definitions are community-derived, can vary by hardware and
software revision, and can change after an OTA update. If UI and safety code
consume arbitration IDs and DBC field names directly, vehicle-specific
assumptions spread throughout the codebase and stale values are easy to mistake
for current facts.

The project also needs a systematic way to onboard future and past Tesla
revisions without rewriting applications.

## Decision

Each vehicle revision has a pinned Tesla adapter that converts observed frames
into a versioned normalized signal model. COVESA Vehicle Signal Specification
names are used where semantics match; project extensions are explicit where
they do not.

Every normalized value carries:

- monotonic timestamp and calculated age;
- quality (`VALID`, `STALE`, `UNAVAILABLE`, `CONFLICT`, or `UNVERIFIED`);
- source and vehicle-profile identifier;
- adapter/data revision;
- unit and documented conversion;
- provenance for the underlying definition and test vectors.

UI code consumes only the normalized broker API. It must display or handle
quality and must not silently retain a stale last-known value.

The supervisor's Park gate uses a smaller one-way safety-state feed from the
receive-only listener, not the general UI broker. The same adapter facts may be
generated from a common reviewed definition, but the safety feed has independent
bounds, freshness checks, and tests. Unknown or contradictory state denies local
mode.

## Consequences

### Positive

- UI and services remain independent of Tesla frame layout.
- Signal freshness and provenance become first-class rather than conventions.
- A changed OTA definition fails closed and can be isolated to one profile.
- Future vehicle adapters can be tested against a common conformance suite.

### Negative

- The adapter and normalized schema add code and versioning work.
- Not every Tesla concept has an exact VSS equivalent.
- Normalization can hide useful raw detail, so diagnostic tools still need a
  controlled raw-frame view.
- A shared erroneous definition could affect both UI and minimal safety decode;
  independent test vectors and review remain necessary.

## Rejected alternatives

- **Expose DBC names directly to the UI:** tightly couples every consumer to one
  unofficial revision.
- **Use only last-known values:** hides loss of freshness and can falsely grant
  a safe state.
- **Let the application broker tell the supervisor the gear state:** compromise
  or failure of the large OS would cross the safety boundary.
- **Infer Park from UI behavior or speed alone:** indirect inference is not a
  positive, validated Park indication.

## Verification

Adapters require synthetic, recorded, stale, missing, malformed, counter-error,
and contradictory test vectors. Conformance tests ensure units, quality,
freshness, and source metadata survive the broker boundary. A Tesla OTA or
hardware revision change reopens adapter validation.
