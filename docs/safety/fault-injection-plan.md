# Fault-injection plan

## Purpose and limits

This plan tests whether credible faults return the add-on bridge to the native
Tesla display and avoid disturbance of the vehicle network. It is written for a
representative 2025 Model 3 Highland bench/HIL fixture. It does not authorize
fault injection on a public road or into a connected vehicle bus.

High-energy transient, short-circuit, thermal-limit, and signal-integrity tests
must use suitable laboratory equipment, current limiting, shielding, fire
precautions, and personnel competent for the equipment. Never apply a load-dump
or destructive transient to the vehicle.

## Preconditions

- Exact device, board, harness, display/source fixture, profile, firmware, and
  software revisions are recorded.
- The native source and display work without the bridge and establish a baseline.
- A hardware emergency power disconnect and physical native bypass are within
  reach.
- CAN tests use an isolated simulator or representative bench network unless a
  test explicitly says static vehicle; the normal device remains receive-only.
- Capture equipment timestamps native/local video, route feedback, touch,
  supervisor state, power rails, current, temperature, and relevant bus input.
- `T_NATIVE_RECOVER`, freshness limits, electrical limits, and stop criteria are
  declared in the target manifest before pass/fail testing.
- Test data contains no public VIN, precise location, account, or personal data.

## Evidence record

Each run records:

```text
test ID and procedure revision
date and operator
vehicle-profile ID and maturity
board, harness, fixture, display, and native-source revisions
firmware/software commits and build hashes
instruments and calibration status
initial mode and environmental conditions
injected fault and exact timing
measured route/recovery timing and observed touch behavior
logs, traces, video, photos, and artifact hashes
result: PASS, FAIL, BLOCKED, or INVALID
anomalies, linked issue, and reviewer
```

A rerun after a fix receives a new record; failed evidence is retained.

## General pass criteria

- Native is selected without application or user intervention after a
  safety-relevant fault.
- Recovery is within the profile's validated `T_NATIVE_RECOVER` bound and is no
  worse than the approved native-link baseline allowance.
- No touch reaches the wrong source and all local contacts are released.
- No vehicle CAN dominant bit or transmitted frame can be caused by the normal
  bridge hardware.
- No unsafe temperature, backfeed, sustained overcurrent, connector damage, or
  uncontrolled reboot loop occurs.
- A diagnostic reason is retained when retaining it does not compromise native
  recovery.
- A test that depends on an unknown limit is `BLOCKED`, not `PASS`.

## Test catalogue

| ID | Phase | Injection | Starting state | Expected result |
| --- | --- | --- | --- | --- |
| FI-001 | Bench | Remove all add-on power | Native and local, separate runs | Unpowered path is native; local run automatically returns native |
| FI-002 | Bench | Remove supervisor power only | Local | Route is driven/biased native without compute cooperation |
| FI-003 | Bench | Hold supervisor in reset/bootloader | Power-up and local | Native remains selected; local cannot be requested |
| FI-004 | Bench | Stop compute heartbeat | Local | Native within declared timeout; local touch released |
| FI-005 | Bench | Kill UI, display process, and OS separately | Local | Each loss is detected or bounded; native recovery meets manifest |
| FI-006 | Bench | Freeze GPU/video frame while process heartbeat continues | Local | Independent link/freshness strategy detects the covered fault or limitation is explicitly documented and pilot blocked |
| FI-007 | Bench | Disconnect or corrupt local video clock/data | Local | Touch disables and native returns |
| FI-008 | Bench | Disconnect native source while local, then request native | Local | Fault is latched; no oscillation or hidden touch; behavior is documented |
| FI-009 | Bench | Open, ground, and supply-short route-control lines through current-limited fixtures | Native/local | Defined faults prefer native or are detected; no component damage outside declared fault containment |
| FI-010 | Bench | Open or short route-feedback input | Local | Disagreement latches fault and requests native |
| FI-011 | Bench | Toggle physical bypass during boot, local, update, and fault | All | Hardware bypass always wins and cannot be overridden |
| FI-012 | Bench | Stop touch reports mid-contact | Local | All-contacts-up is generated locally; native receives no ghost touch |
| FI-013 | Bench | Flood, truncate, reorder, and corrupt touch reports | Local/transition | Bounds hold; malformed input cannot cross routes; native fallback on threshold |
| FI-014 | Bench | Request source changes during active multitouch | Local/native | Break-before-make and release sequence prevent hidden-source input |
| FI-015 | HIL | Remove CAN input | Local | Safety state becomes unknown/stale and native returns |
| FI-016 | HIL | Replay old valid Park frames | Local request | Replay/age cannot grant or retain local mode |
| FI-017 | HIL | Inject malformed counters, timing, unknown IDs, and contradictory gear states in simulator | Local request/local | Decoder reports invalid/conflict; local is denied or exited |
| FI-018 | HIL | Simulate non-Park and Park-to-non-Park transition | Local request/local | Non-Park never grants local; transition requests native immediately according to bound |
| FI-019 | Bench | Attempt CAN transmit through every normal MCU pin/software API | Any | No electrical transmit path; no dominant bit or frame observed |
| FI-020 | Bench | Power bridge off/on while measuring CAN loading | Any | Bus remains within profile loading and waveform limits |
| FI-021 | Bench | Brownout ramp, fast dip, surge within nondestructive design range, and repeated power cycling | All | Native path survives; no latch-up/backfeed; deterministic restart native |
| FI-022 | Bench | Reverse input polarity/current-limited miswire as supported by test fixture | Unpowered | Protection operates without hazardous heating or vehicle-side energy |
| FI-023 | Bench | Controlled overcurrent/short at protected outputs | Powered | Protection isolates fault; native bypass remains available |
| FI-024 | Bench | Heat/cool within declared prototype test envelope and force sensor overtemperature | Native/local | Local exits before component limits; no thermal runaway; native path remains |
| FI-025 | Bench | Fill/corrupt application storage and root filesystem | Boot/local | Native remains; application uses recovery or stays unavailable safely |
| FI-026 | Bench | Interrupt update at each erase/write/activate/reboot boundary | Update | Native is locked; previous or recovery image boots; incompatible mix rejected |
| FI-027 | Bench | Present unsigned, altered, downgraded, and wrong-profile bundles | Update | Every unauthorized or incompatible bundle is rejected |
| FI-028 | HIL | Select wrong/partial/unknown vehicle manifest | Boot | System remains native and reports unsupported profile |
| FI-029 | HIL | Apply recorded pre/post-OTA signal and startup timing variations | Boot/local request | Changed semantics fail closed until the profile is revalidated |
| FI-030 | Bench | Rapidly request native/local for at least the lifecycle target and a 1,000-cycle early gate | Native/local | No route mismatch, accumulating touch state, link degradation, or crash |
| FI-031 | Bench | 24–72 hour mixed-mode soak with scheduled faults | Mixed | No unrecovered native outage, resource leak, thermal drift, or unexpected touch |
| FI-032 | Static vehicle only after bench gates | Repeated lock/sleep/wake over multi-day observation | Native | Sleep-current budget, wake behavior, and native operation remain within approved limits |
| FI-033 | Static vehicle only after bench gates | Vehicle software reboot/update observation without altering update process | Native | Add-on remains or returns native; profile is suspended pending regression evidence if behavior changes |
| FI-034 | Bench | Compromise simulation: root on application computer sends arbitrary supervisor and gateway traffic | Local request | Cannot directly control mux, disable bypass, transmit CAN, or bypass independent Park gate |
| FI-035 | HIL/static only after safe procedure review | Cause or replay an approved non-destructive representative native warning while Park remains valid and local is selected; separately remove assumed audible/phone alert paths | Local | Native warning becomes promptly visible through the justified design path; hardwired return works immediately; otherwise the vehicle pilot remains blocked |

## Sequencing

1. Run FI-001 through FI-014 with generated sources before a salvaged Tesla
   display is used.
2. Repeat applicable tests with the representative Highland display/source and
   final harness topology.
3. Run CAN tests on a simulator/HIL bus and inspect the release PCB physically.
4. Run power and thermal tests in a protected lab fixture.
5. Complete update/security cases and the soak/cycle gates.
6. Only then run the two static-vehicle observations. Keep the physical bypass
   selected native whenever the test does not require the add-on path.

## Stop conditions

Stop immediately on smoke, odor, unexpected heating, connector damage, bus
errors beyond the approved fixture limit, loss of physical bypass, unexplained
touch into the native source, inability to recover native, or measurement-tool
saturation. Quarantine the assembly and open a risk issue before resuming.
