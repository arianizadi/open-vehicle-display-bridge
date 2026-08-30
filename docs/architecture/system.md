# System architecture

## Status and scope

This document describes a research prototype, not an automotive-qualified or
safety-certified product. The first supported target is one specifically
identified 2025 Tesla Model 3 Highland configuration. Compatibility with any
other vehicle, build date, display, infotainment computer, or harness must be
earned through a separate vehicle-revision profile and the validation process
described below.

The architecture has four non-negotiable properties:

1. Removing power from the add-on hardware leaves the original Tesla display
   path selected.
2. An independent safety supervisor, not Linux or Android, owns video and touch
   source selection.
3. Vehicle-bus access is physically receive-only in normal hardware.
4. All display interception is proven on a bench rig before installation in a
   vehicle.

The project initially supports local content only while the vehicle is
positively known to be in Park. Unknown, stale, contradictory, or invalid state
is treated as not parked.

## Goals

- Preserve the unmodified native display and touch behavior whenever the bridge
  is off, booting, updating, unhealthy, or unsupported.
- Show a local Linux or Android source on the factory display when the safety
  supervisor permits it.
- Route touch exclusively to the source currently shown.
- Read vehicle telemetry without creating a transmission path to the vehicle
  network.
- Isolate Tesla-specific electrical and signal details behind a versioned
  vehicle-revision adapter and manifest.
- Produce reproducible bench evidence for every supported revision.

## Explicit non-goals for the first release

- Split-screen or compositing with the native Tesla image.
- CAN transmission or vehicle-control commands.
- Video or interactive third-party applications while driving.
- Compatibility claims for all Model 3, Model Y, or Tesla vehicles.
- Google Automotive Services, DRM guarantees, certified CarPlay, or an app
  store distribution promise.
- Claims of Tesla approval, ISO 26262 compliance, road legality, or automotive
  qualification.

## System context

```text
                       Original vehicle boundary
        +------------------------------------------------------+
        |                                                      |
        |  Tesla infotainment ---- native video/touch ----+    |
        |                                                  |    |
        |  Vehicle network ---- receive-only tap ----+     |    |
        +---------------------------------------------|-----|----+
                                                      |     |
                       Add-on boundary                 |     |
        +---------------------------------------------|-----|----+
        |                                             v     v    |
        |  +----------------+     one-way state   +--------------+|
        |  | CAN listener   | ------------------> | safety       ||
        |  | (no TX path)   |                     | supervisor   ||
        |  +-------+--------+                     +------+-------+|
        |          | normalized telemetry                | owns   |
        |          v                                     | route  |
        |  +----------------+   local request/health      v       |
        |  | application    | --------------------> +----------+  |
        |  | computer       | -- local video/touch --| video & |  |
        |  +----------------+                        | touch    |  |
        |                                            | bridge   |  |
        |  +----------------+ power/thermal status ->|          |  |
        |  | power manager  |                        +----+-----+  |
        |  +----------------+                             |        |
        +-------------------------------------------------|--------+
                                                          v
                                                    Tesla display
```

The diagram is logical. The Highland transport, connector, link topology, and
touch backchannel are intentionally not asserted here; they must be measured
and recorded in the initial revision manifest before a schematic is finalized.

## Components and trust

### Native bypass path

The bypass is the highest-integrity path. Its de-energized state connects the
Tesla infotainment source to the Tesla display and preserves the native touch
return path. A selected mux IC is not considered fail-native merely because its
select pin has a pull resistor. The complete unpowered circuit, including power
rails, ESD parts, connectors, and common-mode behavior, must demonstrate native
continuity and acceptable signal integrity.

A normally closed electromechanical path, passive bypass network, or another
topology may satisfy this requirement. The implementation decision belongs to
the video-bridge hardware design and must be supported by measurements.

### Safety supervisor

The supervisor is a small, independent MCU with a narrow responsibility:

- keep native selected during reset and boot;
- validate target-profile identity and required health inputs;
- accept or reject an untrusted request for local display;
- enforce Park-only and freshness gates;
- route video and touch as one transaction;
- force native on timeout, brownout, overtemperature, link fault, update, or
  contradictory state;
- expose a latched fault reason for diagnosis.

The supervisor has its own watchdog and does not run third-party applications.
Its selection output is biased so that reset, tri-state, broken wiring, or loss
of supervisor power requests native. Application-computer heartbeats are only
one condition for local mode; a heartbeat can never force local mode.

### Application computer

The application computer runs the UI, optional phone projection, display
manager, vehicle gateway, logging, and updater. It is treated as untrusted by
the supervisor because it has a large attack surface and can hang, reboot, or
be compromised. It can request local mode and report health, but cannot drive
the mux or touch switches directly.

### Read-only CAN listener

The listener is a separate electrical boundary. The normal PCB uses a
receive-only transceiver arrangement: no routed transmit signal, no software
switch that can enable transmission, and no added bus termination. A separate
laboratory adapter is required for any transmit research and is outside the
normal device and release images.

The listener feeds raw frames to the gateway and a minimal, one-way safety-state
message to the supervisor. The initial decoder is specific to the validated
2025 Highland profile. Signal absence, disagreement, counter failure, or age
beyond the profile limit results in `UNKNOWN`, which cannot grant local mode.

### Vehicle gateway and normalized signal broker

The gateway decodes a pinned, provenance-tracked Tesla adapter into stable,
vehicle-independent names. The UI consumes only normalized signals. Each value
contains quality, source revision, and age; consumers must not silently reuse a
last-known value after it becomes stale.

### Power manager

The power subsystem protects the vehicle supply and controls orderly compute
startup and shutdown. It reports undervoltage, overvoltage, overcurrent,
overtemperature, and sleep intent to the supervisor. Removal or failure of this
subsystem must not break the native bypass path.

## Operating states

| State | Video/touch route | Entry conditions | Exit behavior |
| --- | --- | --- | --- |
| `UNPOWERED` | Native by hardware | Add-on power absent | Power-up begins in `NATIVE_LOCKED` |
| `NATIVE_LOCKED` | Native | Reset, boot, update, physical bypass, unsupported profile, or latched fault | Remains native until all local-mode gates pass |
| `NATIVE_READY` | Native | Supervisor healthy and supported profile verified | May accept a local request while positively in Park |
| `LOCAL_PARKED` | Local | Physical enable present, fresh Park state, healthy local link, heartbeat valid, no fault | Any failed gate immediately requests native |
| `RETURNING_NATIVE` | Touch inhibited, native route being restored | Local request removed or fault detected | Enter `NATIVE_READY` only after native link/touch settle criteria pass |
| `FAULT_LATCHED` | Native | Safety-relevant diagnostic or failed route verification | Requires documented safe reset; no automatic return to local |

The hardware route always has priority over the software state label. If the
supervisor and telemetry disagree about the actual route, the supervisor treats
that as a fault and requests native.

## Boot, switching, and shutdown

1. The physical route starts native before any MCU or application code runs.
2. The supervisor validates its firmware, watchdog, configuration, target
   profile, route feedback, power, thermal state, and physical bypass input.
3. The application computer may boot and render off-screen. It periodically
   sends a health heartbeat and a local-mode request.
4. A request is permitted only in confirmed Park with all required signals
   fresh and consistent. Touch is inhibited during route changes.
5. Local video is selected, link-lock/display evidence is checked, and only
   then is local touch enabled.
6. On exit, local touch is disabled first, native touch and video are restored,
   and the supervisor verifies the native route before clearing the transition.
7. Shutdown and all update modes remain native.

Exact debounce, freshness, switch, and link-lock timing is profile data. No
vehicle pilot may start while those fields are unknown.

## Vehicle-revision profiles

The initial profile is for the project owner's exact 2025 Model 3 Highland. It
must use non-identifying hardware/build metadata rather than a public VIN. A
profile records at least:

- profile ID and maturity (`candidate`, `bench-verified`, `vehicle-pilot`,
  `supported`, or `retired`);
- vehicle model year, factory/build range, market, and relevant infotainment and
  display hardware identifiers;
- connector part numbers and pin map derived from lawful sources or measurement;
- measured native video transport, lane topology, pixel timing, link settings,
  and link-lock expectations;
- touch transport, coordinate system, report semantics, and route behavior;
- power, wake, sleep, and current limits;
- pinned signal-definition revision, frame provenance, counters, units, and
  maximum signal ages;
- hardware, supervisor, adapter, and application versions used for validation;
- test evidence and known exclusions.

Profiles are deny-by-default. An unknown or partial profile cannot enable local
mode. Adding a past or future Tesla revision requires a new adapter/profile,
bench fixture, risk review, and validation evidence; it is not a metadata-only
change.

## Bench-first development gates

1. **Synthetic bench:** use generated video, virtual CAN, and touch test vectors.
2. **Salvaged-display bench:** characterize the exact Highland display and link
   without connecting the bridge to a vehicle.
3. **Hardware-in-the-loop bench:** exercise a representative native source,
   display, harness, power conditions, and faults. Prove de-energized native
   bypass and repeated switching.
4. **Static vehicle test:** install a reversible harness, keep the vehicle
   stationary, and confirm sleep-current and native recovery behavior.
5. **Park-only pilot:** allowed only after the validation matrix is reviewed and
   every mandatory gate has recorded evidence.

Public-road testing is not a substitute for a bench test and is not part of the
initial validation plan.

## Evidence and configuration control

Test reports must identify the vehicle profile, board revisions, firmware and
software commits, harness, measurement tools, environmental conditions, and
raw artifact hashes. A pass on one combination does not transfer to another.
Unverified claims are labeled as hypotheses in research notes, never as profile
facts.
