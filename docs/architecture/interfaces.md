# Interface contracts

## Purpose

These contracts prevent application code, Tesla-specific decoding, and future
vehicle revisions from bypassing the fail-native safety boundary. Values marked
`profile-defined` must be measured for the exact 2025 Model 3 Highland target
and committed to its revision manifest before vehicle use.

## Interface summary

| ID | Producer | Consumer | Direction | Safety posture |
| --- | --- | --- | --- | --- |
| IF-V1 | Tesla infotainment source | video bridge | Vehicle to bridge | Native source is preserved; transport is profile-defined |
| IF-V2 | Local compute/video adapter | video bridge | Add-on internal | Never has routing authority |
| IF-D1 | Video bridge | Tesla display | Bridge to vehicle display | De-energized route is native |
| IF-T1 | Tesla display touch | native source or local touch bridge | Mutually exclusive | Touch follows verified video route |
| IF-S1 | Application computer | safety supervisor | Request/heartbeat only | Untrusted and fail-deny |
| IF-S2 | CAN listener | safety supervisor | One-way state | Cannot alone force local mode |
| IF-S3 | Safety supervisor | video/touch bridge | Selection control | Sole route authority; native-biased |
| IF-C1 | Vehicle CAN | receive-only listener | Vehicle to bridge | No physical transmit path |
| IF-G1 | Vehicle gateway | UI clients | Local IPC | Normalized, timestamped, quality-tagged |
| IF-P1 | Power manager | supervisor/compute | Status and control | Faults request native first |
| IF-U1 | Update bundle | updater | Signed local/update channel | Update occurs with native locked |

## IF-V1, IF-V2, and IF-D1: video transport

The bridge must not assume that legacy Model 3 display link details apply to a
2025 Highland. The target profile defines connector, lane count, signaling,
pixel clock, resolution, color format, scrambling, equalization, sideband
channels, and power sequencing based on lawful documentation and bench
measurement.

Required invariants:

- Native video passes through when the bridge is unpowered.
- No local source can electrically drive the native source pins.
- Route controls are inaccessible to the application computer.
- A local link is never selected until its timing and health are valid.
- Loss of local link, clock, compute heartbeat, supervisor health, or route
  feedback requests native.
- Unsupported or unidentified video-link hardware locks the system native.
- Source switching does not inject an invalid voltage into either endpoint.

The target manifest supplies `T_LOCAL_LOCK`, `T_NATIVE_RECOVER`, and allowed
transient behavior. These values are derived from a native baseline and bench
fault tests; `unknown` is not an acceptable value for a vehicle pilot.

## IF-T1: touch routing

Touch routing is break-before-make and must follow the displayed source. The
bridge never broadcasts a touch report to both sources.

Switch-to-local sequence:

1. Disable local and native touch forwarding.
2. Select and verify local video.
3. Reset or drain the local HID report state.
4. Select the local touch route.
5. Enable local touch only after the route is stable.

Return-to-native sequence:

1. Emit an all-contacts-up report locally and disable local touch.
2. Select the native touch path and native video path.
3. Verify route feedback and the native link.
4. Re-enable native touch only after the profile-defined settle interval.

Any stuck contact, malformed report, impossible coordinate, report flood,
backchannel failure, or discrepancy between video and touch route causes native
selection and a latched diagnostic. Coordinate transforms and multitouch limits
belong to the vehicle profile.

## IF-S1: compute request and heartbeat

This is a small framed protocol over a dedicated internal link. It has no mux
control command. At minimum, a frame contains:

```text
protocol_version
message_type
monotonic_sequence
sender_uptime_ms
requested_mode      # NATIVE or LOCAL
ui_health            # STARTING, READY, DEGRADED, FAILED
profile_id
payload_length
integrity_check
```

Properties:

- `NATIVE` is always accepted; `LOCAL` is only a request.
- Sequence, length, version, and integrity failures invalidate the frame.
- Heartbeat timeout is profile/supervisor configuration and fails to native.
- Replaying an old `READY` frame cannot maintain local mode.
- A profile ID mismatch prevents local mode.
- The supervisor protocol has no command for disabling watchdogs or safety
  gates.

## IF-S2: one-way safety-state feed

The receive-only listener supplies a deliberately small state set to the
supervisor. Initial fields are expected to include gear/park state, data age,
adapter revision, source-frame health, and decoder self-test status. Exact CAN
IDs and bit definitions are not part of this interface and remain in the Tesla
adapter.

```text
state_version
profile_id
monotonic_sequence
vehicle_mode         # PARK, NOT_PARK, UNKNOWN
source_age_ms
source_health        # VALID, STALE, COUNTER_ERROR, CONFLICT, UNSUPPORTED
decoder_health
integrity_check
```

Only `PARK` plus `VALID`, within the configured maximum age, is permissive.
Every other combination denies local mode. The feed is one-way at the
electrical or hardware boundary; the supervisor cannot transmit onto vehicle
CAN through it.

## IF-S3: supervisor route controls

Only the supervisor connects to mux enable/select and touch-route controls.
Control truth tables are designed so all of the following select native:

- supervisor reset or bootloader;
- high-impedance output;
- open circuit;
- loss of supervisor or add-on power;
- failed or absent physical-enable input;
- watchdog timeout;
- invalid configuration.

`LOCAL_SELECT` must require an actively driven, continuously healthy condition.
Independent route feedback is sampled where practical. A disagreement between
commanded and observed route is a latched fault.

The user-accessible bypass is a hardware input with priority over firmware. Its
native position cannot be overridden by a software command.

## IF-C1: vehicle CAN receive-only tap

Normal hardware requirements:

- use a receive-only or permanently silent/listen-only transceiver topology;
- do not route MCU TX to the transceiver or vehicle connector;
- do not add 120-ohm termination;
- bound input capacitance and stub length in the revision/harness design;
- isolate or otherwise contain faults so loss of add-on power cannot load the
  vehicle bus outside validated limits;
- expose receive traffic to the application and minimal decoder only;
- make debug/test transmission require physically different laboratory
  hardware that cannot be mistaken for a release assembly.

Software flags, socket permissions, and an empty transmit queue are defense in
depth, not proof of read-only behavior.

## IF-G1: normalized vehicle signals

UI clients consume normalized signals over a local, versioned IPC API. A signal
contains:

```json
{
  "path": "Vehicle.Powertrain.Transmission.SelectedGear",
  "value": "PARK",
  "unit": null,
  "monotonicTimestampMs": 123456,
  "ageMs": 8,
  "quality": "VALID",
  "vehicleProfile": "profile-id",
  "adapterRevision": "git-or-data-revision",
  "source": "vehicle-can"
}
```

Allowed quality values are `VALID`, `STALE`, `UNAVAILABLE`, `CONFLICT`, and
`UNVERIFIED`. Clients must display or handle quality explicitly. The broker does
not fabricate values, infer safety state from UI state, or persist a stale value
as current. Safety-supervisor decisions do not depend on this general-purpose
IPC path.

Signal names should follow COVESA VSS where a suitable concept exists. A
project-specific extension namespace is used otherwise. Tesla arbitration IDs
and DBC field names do not leak into UI APIs.

## IF-P1: power and thermal status

The power manager exposes these logical conditions to the supervisor:

- input supply valid/invalid;
- brownout warning;
- overvoltage or load-protection event;
- overcurrent;
- board and compute temperature state;
- ignition/wake/sleep intent when lawfully and reliably available;
- shutdown deadline.

Every fault first requests native and disables local touch. Compute shutdown is
secondary. The native bypass cannot depend on a clean application shutdown.
Power thresholds and quiescent-current budgets are profile/hardware-revision
parameters proven on the bench.

## IF-U1: update bundles

- Updates are signed and versioned; hashes alone are not authentication.
- The update trust root is not writable by the normal application account.
- Supervisor, adapter, and application compatibility constraints are declared
  in the bundle.
- Rollback protection prevents known-vulnerable images, while a tested A/B or
  recovery mechanism handles interruption.
- The bridge is locked native throughout download activation, reboot, rollback,
  and supervisor update.
- Supervisor recovery must work without the application computer.
- Target-profile data is signed or built into an authenticated image. A profile
  cannot be selected solely by a user-editable string.

## Profile-onboarding interface

Each new Tesla revision implements the same logical interfaces but supplies its
own hardware adapter, manifest, test vectors, and evidence. Reviewers must be
able to answer:

1. How was this exact revision identified without publishing personal vehicle
   identifiers?
2. Which electrical facts are measured, which are from public documentation,
   and which remain hypotheses?
3. What makes the link, touch, power, and CAN definitions different from or
   equivalent to an existing profile?
4. Which HIL and fault tests were rerun on the new physical combination?
5. What explicit exclusions remain?

No profile may inherit `validated` status solely because marketing model names
match.
