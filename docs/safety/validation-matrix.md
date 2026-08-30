# Validation matrix

## Use

This matrix is the minimum evidence map for the initial 2025 Model 3 Highland
profile. `NOT RUN` is the initial state. A requirement is not satisfied by a
design review alone when a physical or fault test is named. `BLOCKED` is the
correct result when the exact transport, limit, fixture, or pass criterion is
unknown.

This is project validation, not automotive certification. A `PASS` applies only
to the recorded hardware, harness, firmware, software, fixture, and vehicle
profile combination.

| Requirement | Requirement statement | Stage | Method / linked tests | Required evidence | Initial status |
| --- | --- | --- | --- | --- | --- |
| SAFE-001 | Complete loss of add-on power leaves or restores native video and native touch without compute action | Bench/HIL | FI-001; continuity, eye/link, and recovery measurement | Unpowered schematic/netlist review, waveforms, video, timing, artifact hashes | NOT RUN |
| SAFE-002 | Independent supervisor alone owns video/touch selection and defaults native on reset, open control, and watchdog fault | Bench | FI-002, FI-003, FI-004, FI-009, FI-010 | Netlist, firmware traceability, scope captures, fault logs | NOT RUN |
| SAFE-003 | Physical bypass overrides every software, boot, update, and fault state | Bench/HIL | FI-011 | Truth-table review, continuity measurements, repeated-use video | NOT RUN |
| SAFE-004 | Local mode is permitted only with positively confirmed, fresh Park state | HIL | FI-015 through FI-018 | Decoder tests, state transition traces, supervisor logs | NOT RUN |
| SAFE-005 | Unknown, stale, conflicting, unsupported, or malformed safety state selects native | HIL | FI-015, FI-016, FI-017, FI-028, FI-029 | Adversarial replay corpus and route traces | NOT RUN |
| SAFE-006 | Linux/Android root compromise cannot directly select the mux, disable bypass, or weaken supervisor gates | Bench/security | FI-034; schematic/netlist and privilege review | Attack transcript, netlist evidence, supervisor logs | NOT RUN |
| SAFE-007 | Native recovery timing and allowed transients are measured and bounded per profile | Salvaged-display bench/HIL | FI-001 through FI-010 | Native baseline, declared `T_NATIVE_RECOVER`, repeated timing distribution | NOT RUN |
| SAFE-008 | A new important native warning raised during otherwise valid Park-only local mode becomes promptly visible; audible/phone behavior is measured, not assumed | HIL/static vehicle after procedure review | FI-035; warning-coverage analysis; hardwired return test | Approved warning scenario, synchronized route/video/audio evidence, exposure bound, reviewer decision | NOT RUN |
| DISP-001 | Exact Highland connector, signaling, lane topology, timing, sideband, and power sequence are measured before custom PCB freeze | Salvaged-display bench | Characterization procedure; independent review | Profile manifest, instrument captures, provenance, reviewer sign-off | NOT RUN |
| DISP-002 | Final bridge and harness meet video-link margin across voltage, temperature, cable, and component tolerances in the declared prototype envelope | Bench | FI-007, FI-021, FI-024, FI-030, FI-031 | SI analysis, eye/link error data, environmental and soak logs | NOT RUN |
| DISP-003 | Loss/corruption of local video disables local touch and requests native | Bench | FI-006, FI-007 | Synchronized video/touch/route trace | NOT RUN |
| TOUCH-001 | Touch is exclusive and break-before-make; source changes release all active contacts | Bench/HIL | FI-012, FI-013, FI-014 | HID/backchannel traces and synchronized route video | NOT RUN |
| TOUCH-002 | Native touch behavior with bridge unpowered is equivalent to the approved native baseline | Salvaged-display bench/HIL | FI-001; native gesture regression | Raw reports, latency/error comparison, test video | NOT RUN |
| CAN-001 | Release hardware has no electrical vehicle-CAN transmit path under any MCU state | Bench/review | FI-019; schematic, layout, continuity, and dominant-bit observation | Signed hardware review and analyzer capture | NOT RUN |
| CAN-002 | Receive-only tap adds no termination and stays within profile-defined loading/stub/waveform limits powered and unpowered | Bench/HIL | FI-020 | Resistance, capacitance/stub design, waveform/error measurements | NOT RUN |
| CAN-003 | Tesla adapter detects stale, counter-error, malformed, conflicting, and changed signal inputs | Unit/HIL | FI-015 through FI-018, FI-029 | Versioned synthetic/recorded corpus and automated results | NOT RUN |
| SIG-001 | Normalized signals expose timestamp, age, quality, unit, source, profile, and adapter revision; clients do not silently use stale values | Unit/integration | Broker conformance and UI degraded-state tests | API fixtures, automated test report, screenshots | NOT RUN |
| PWR-001 | Protected input handles declared brownout, nondestructive transient, reverse, short, and restart cases without defeating native bypass | Bench | FI-021, FI-022, FI-023 | Schematics, component limits, voltage/current/thermal traces | NOT RUN |
| PWR-002 | Thermal limits force native before declared component limits and no uncontrolled thermal condition occurs | Bench | FI-024 | Sensor calibration, chamber/fixture trace, route logs | NOT RUN |
| PWR-003 | Static-vehicle sleep/wake current and backfeed stay within the approved budget over a multi-day run | Static vehicle after gates | FI-032 | Calibrated current log, wake-cause log, native behavior record | NOT RUN |
| REV-001 | First profile identifies the owner's exact 2025 Model 3 Highland configuration without publishing a VIN | Documentation/bench | Profile review | Manifest, redacted hardware/build evidence, provenance | NOT RUN |
| REV-002 | Unknown, partial, or wrong profiles cannot enable local mode | HIL | FI-028 | Negative profile corpus and supervisor trace | NOT RUN |
| REV-003 | Tesla OTA or relevant hardware/software change suspends support until regression evidence is recorded | Process/HIL | FI-029, FI-033 | Change-detection checklist, before/after traces, release decision | NOT RUN |
| UPD-001 | Unsigned, altered, downgraded, wrong-profile, incompatible, or interrupted updates leave the bridge native and recoverable | Bench/security | FI-025, FI-026, FI-027 | Signature/compatibility logs, interruption matrix, recovery video | NOT RUN |
| SEC-001 | Release image exposes only documented services and application compromise cannot reach the supervisor control plane | Integration/security | Service inventory, firewall/route tests, FI-034 | Port/route inventory and penetration-test notes | NOT RUN |
| SEC-002 | Releases include reviewed provenance, dependency pins, SBOM, signatures, and no secrets/proprietary blobs | CI/process | Reproducibility and secret/license scans | Release attestation, SBOM, scan report, reviewer | NOT RUN |
| PRIV-001 | Diagnostic collection is opt-in, minimized, locally controlled, and has a documented retention/deletion path | Integration/process | Privacy-flow review | Configuration tests, retention/deletion evidence | NOT RUN |
| PRIV-002 | Public captures/test vectors contain no VIN, precise location, accounts, contacts, or device secrets | CI/manual review | Redaction corpus and release scan | Automated scan plus human checklist | NOT RUN |
| UI-001 | Local UI is visually distinct from native Tesla safety indicators and makes stale/unverified data explicit | UX/HIL | Scenario review with valid/stale/unavailable signals | Screenshots/video and reviewed checklist | NOT RUN |
| INST-001 | Harness is keyed, reversible, fused as designed, strain-relieved, and does not require cutting factory wiring | Bench/static vehicle | Physical inspection and continuity test | BOM/drawings, installation photos, inspection record | NOT RUN |
| INST-002 | Installation/removal procedure identifies exact profile, depowering, prohibited circuits, inspection, bypass, and stop conditions | Documentation/static vehicle | Independent dry run | Reviewed guide and dry-run record | NOT RUN |
| REL-001 | At least 1,000 early-gate source cycles complete without mismatch, ghost touch, link degradation, or unrecovered fault | Bench/HIL | FI-030 | Automated cycle log, sampled traces, failure summary | NOT RUN |
| REL-002 | A 24–72 hour mixed-mode soak completes without unrecovered native outage, thermal drift, or resource leak | Bench/HIL | FI-031 | Continuous monitoring logs and final review | NOT RUN |

## Gate decisions

### Gate A: custom video-bridge schematic

Requires `DISP-001` and a reviewed initial vehicle profile. Legacy Model 3 link
assumptions are not sufficient.

### Gate B: representative HIL fixture

Requires `SAFE-001`, `SAFE-002`, `SAFE-003`, `TOUCH-002`, `CAN-001`, and
`PWR-001` on the current board/harness topology.

### Gate C: static vehicle installation

Requires all Gate B items plus `SAFE-004` through `SAFE-008`, `DISP-002`,
`DISP-003`, `TOUCH-001`, `CAN-002`, `CAN-003`, `REV-001`, `REV-002`, `UPD-001`,
`INST-001`, `INST-002`, `REL-001`, and an open-risk review. The physical bypass
remains native except during the named stationary test.

### Gate D: Park-only pilot

Requires every mandatory row above, including sleep, soak, security, privacy,
and UI evidence, plus explicit review of all remaining S4 risks. Passing Gate D
does not authorize use while moving or constitute certification.

## Status changes

Status values are `NOT RUN`, `BLOCKED`, `PASS`, or `FAIL`. Every change links to
immutable or content-addressed evidence. A hardware, harness, firmware,
supervisor, vehicle-profile, CAN-definition, or relevant Tesla OTA change marks
affected rows `NOT RUN` until the impact analysis identifies and completes the
required regressions.
