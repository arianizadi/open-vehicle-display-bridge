# Roadmap

Every phase is bench-first and gated. Dates are deliberately omitted until the
unknown display interface and vehicle revision are verified.

## Phase 0 — evidence and zero-intercept prototype

- Freeze the first target to the owner's exact 2025 Model 3 Highland revision.
- Record build plant/date, MCU family, public schematic program, connector
  markings, and display part number without publishing VIN or location data.
- Create a signed vehicle manifest and evidence pack.
- Prototype the UI on commodity compute with simulated or recorded,
  privacy-scrubbed telemetry.

Exit gate: the connector/pinout review has two independent approvals, all
unknowns are explicit, and no hardware has touched the vehicle.

## Phase 1 — salvaged-display bench

- Obtain a legally sourced, matching factory display and mating harness.
- Build current-limited protected power and an emergency disconnect.
- Characterize power-up, EDID/timing, link lock, touch, and sideband behavior.
- Drive a static test pattern at the timing discovered from the matching
  display's EDID/DisplayID and verified link measurements, using an evaluation
  module or original serializer design selected from that evidence.

Exit gate: repeatable cold/warm startup, no damaged hardware, full provenance,
and oscilloscope/current logs attached to the test report.

## Phase 2 — fail-native two-source bridge

- Create a passive/de-energized native path and external-source selector.
- Put selector ownership in an independent supervisor.
- Add a physical bypass control and a removable direct-coupler harness.
- Run at least 1,000 switch cycles plus power loss, computer crash, cable fault,
  undervoltage, overtemperature, and watchdog fault injection.

Exit gate: every injected fault returns to or preserves the native source;
no frozen external frame is treated as safe.

## Phase 3 — touch and read-only vehicle context

- Translate the verified touch/backchannel into USB HID for external compute.
- Add a physically transmit-disabled CAN listener.
- Normalize supported signals through a versioned vehicle adapter.
- Treat stale, invalid, or ambiguous state as unknown and therefore native.

Exit gate: touch cannot reach the wrong source; no transmitted CAN frame is
possible on production listener hardware; replay tests cover every signal.

## Phase 4 — controlled vehicle pilot

- Use a reversible, keyed harness for one exact manifest revision.
- Allow external content only while parked during the initial pilot.
- Force native display for reverse, motion, stale state, boot, shutdown, update,
  brownout, thermal fault, watchdog reset, or physical bypass.
- Keep a second person present and a documented rollback path.

Exit gate: all validation evidence is reviewed before each vehicle session.
Passing a prototype test does not imply regulatory or automotive qualification.

## Phase 5 — appliance quality

- Signed reproducible builds and signed A/B updates with rollback.
- Sleep-current, thermal chamber, EMI/pre-compliance, and long-duration tests.
- Hardware-in-the-loop fixtures generated from vehicle manifests.
- SBOM, release provenance, security response process, and documented support
  matrix.

## Phase 6 — additional vehicle revisions

Each revision starts as unsupported. The onboarding pipeline is:

1. create a candidate manifest from official documentation;
2. mechanically verify connector keying and pinout;
3. capture only lawfully observed signals on owned/salvaged equipment;
4. generate continuity, replay, and HIL fixtures;
5. validate a matching salvaged display;
6. review safety behavior; and
7. publish support only for the exact evidence-backed range.

Advanced compositing, dual-view capture, and any active vehicle command remain
separate research tracks. They are not prerequisites for the display bridge.
