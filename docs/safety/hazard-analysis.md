# Hazard analysis

## Important limitation

This is a project engineering analysis for an experimental, user-built device.
It is not an ISO 26262 HARA, safety case, certification, or statement of road
fitness. Initial residual risks are `UNKNOWN` until a physical 2025 Model 3
Highland bench configuration completes the validation matrix.

## Scope

The analysis covers hazards introduced or worsened by inserting an add-on video,
touch, power, and read-only telemetry bridge between the native infotainment
source and center display. It considers bench work, installation, Park-only use,
sleep/wake, updates, and foreseeable faults. It does not analyze unrelated Tesla
vehicle functions.

On Highland, the center display also carries the primary on-screen gear selector
and reversing image. Loss, freeze, or misrouting is therefore treated as a
highest-severity display hazard even in a project whose intended local mode is
Park-only.

## Method

Hazards are identified from component failures, interface failures, misuse,
security abuse, revision mismatch, and maintenance/update errors. The risk
register tracks each hazard through controls and evidence.

Qualitative severity:

| Level | Meaning |
| --- | --- |
| S1 | Inconvenience with no expected injury or material damage |
| S2 | Possible minor injury, privacy harm, or limited equipment damage |
| S3 | Possible serious distraction, loss of an important function, battery damage, or significant equipment damage |
| S4 | Potential loss of safety-relevant display/control information, unintended vehicle interaction, fire, or serious injury |

Qualitative likelihood describes the project team's current evidence, not fleet
statistics:

| Level | Meaning |
| --- | --- |
| L1 | Requires multiple unusual independent conditions |
| L2 | Unlikely in intended use but credible |
| L3 | Plausible over prototype life |
| L4 | Expected without a specific control |
| L5 | Observed or inherent in normal operation |

Detectability is ranked D1 (obvious before consequence) through D5 (unlikely to
be noticed before consequence). Initial risk is conservative. Residual risk is
not assigned until named verification evidence exists.

## Safety principles

- Native display and touch are the safe fallback state.
- Loss of add-on power or control selects native by hardware.
- The application OS is not trusted with routing authority.
- Local display is allowed only with positive, fresh Park state; uncertainty is
  not permission.
- CAN is physically receive-only on normal hardware.
- Every vehicle revision is unsupported until separately identified and tested.
- Bench and HIL evidence precedes any stationary vehicle pilot.
- A physical bypass and reversible harness remain available to the user.

## Hazard inventory

### H-001: Native display unavailable or black

An unpowered component, mux fault, connector fault, link mismatch, supervisor
failure, or damaged harness could prevent the center display from presenting
native information. Primary controls are de-energized native continuity, an
independent supervisor, physical bypass, signal-integrity qualification, and
bench fault injection.

### H-002: Local content remains visible when it must not

Stale Park state, decoder error, compute spoofing, route-control fault, or state
transition race could obscure native warnings or the reversing view. Local mode
requires independently observed fresh Park, continuous health, and immediate
native request on any failed gate. Vehicle motion is not an initial use case.

### H-003: Frozen or misleading image appears current

A GPU, decoder, link, or application can freeze while heartbeat logic remains
alive. Route/link monitoring, bounded end-to-end freshness where available,
native timeout behavior, and a narrow local UI reduce this risk. The local UI
must not imitate safety-critical native indicators.

### H-004: Touch is delivered to the wrong source

A switch race, stuck contact, malformed report, or routing fault could operate a
hidden native control or local app. Video and touch change as one supervised
transaction, break-before-make, with all contacts released and route feedback.

### H-005: Add-on transmits onto vehicle CAN

Firmware error, compromise, debug configuration, or wrong transceiver wiring
could inject traffic. Normal hardware has no routed TX path and no software
method to enable one. Any transmit research uses physically distinct lab-only
equipment.

### H-006: Passive CAN tap disrupts the bus

Excess termination, long stub, capacitance, short, ESD failure, or unpowered
loading could affect vehicle communication even without transmission. Harness
and receiver loading require measurement, protection, and fault-containment
testing on representative hardware.

### H-007: Battery drain or improper sleep/wake

The compute module, radios, or power converter could remain awake, repeatedly
reboot, or backfeed a vehicle circuit. Controls include a measured quiescent
budget, bounded shutdown, wake-source logging, undervoltage cutoff, no backfeed,
and multi-day sleep tests.

### H-008: Electrical, thermal, or fire hazard

Load transients, reverse polarity, short circuits, inadequate wiring/fusing,
converter failure, or a hot enclosure can damage the vehicle or cause injury.
Use a fused protected input, appropriate transient/reverse/overcurrent design,
temperature monitoring, derating, flame-conscious enclosure/material choices,
and lab-only transient testing.

### H-009: Intermittent video or touch from signal integrity

HSD cable length, impedance discontinuity, mux loss, crosstalk, connectors, EMI,
or component variation can cause intermittent blackouts or input errors. The
exact Highland transport must be measured; layout simulation/measurement,
margin tests, soak, vibration-aware connection design, and native fallback are
required.

### H-010: Wrong vehicle-revision profile

A visually matching connector or model name can hide a different link, display,
or CAN layout. Authenticated profile identity, hardware/build checks, explicit
exclusions, and deny-by-default behavior prevent best-effort operation.

### H-011: Tesla OTA invalidates decoded signals or timing

An OTA can change frame semantics, counters, startup timing, or display behavior.
Signal freshness and conflicts fail closed, versions are recorded, and OTA
changes trigger static/bench revalidation before local mode is restored.

### H-012: Update or storage failure prevents recovery

Power loss, corrupt media, incompatible component versions, or a bad release can
brick the application or supervisor. Native remains locked during update;
signed compatible bundles, application A/B recovery, and independent supervisor
recovery are tested with interrupted writes.

### H-013: Unauthorized access changes display behavior

Wi-Fi, Bluetooth, USB, phone projection, web content, or supply-chain compromise
can give an attacker application control. Network isolation, least privilege,
minimal services, signed updates, SBOM review, and the hardware safety boundary
limit the consequence.

### H-014: Driver distraction

Interactive apps, video, animation, notifications, or complex gestures can
distract even if the bridge is technically working. The prototype is Park-only,
has no moving-mode exception, and returns native when Park cannot be positively
verified. Local law and insurer requirements remain the builder's responsibility.

### H-015: Sensitive vehicle or personal data disclosure

Raw traces and logs can reveal VIN, location, routines, accounts, contacts, or
device identifiers. Default-local processing, collection minimization,
redaction, short retention, synthetic public vectors, and explicit consent are
required.

### H-016: Installation or removal damage

Incorrect depowering, pinout, connector handling, cable routing, or trim work
can damage the vehicle or injure the installer. Use exact-revision instructions,
reversible keyed harnesses, fuse protection, inspection, stop criteria, and no
work on unknown high-voltage or restraint circuits.

### H-017: A new native warning is hidden during valid Park-only local mode

The vehicle can raise a charging, thermal, security, electrical, or other
important warning while it remains in Park and all previously decoded state is
fresh. A Park gate alone therefore cannot prove that hiding the native UI is
safe. The user must always have an immediate hardwired return-native control.
Bounded local sessions and periodic native checks may reduce exposure, and
audible/phone alerts must be measured rather than assumed, but they are not a
substitute for critical-warning coverage. A vehicle pilot is blocked unless the
project can justify and validate a prompt native-warning path for the exact
profile.

## Safety lifecycle and review

Every risk has an owner and evidence field in `risk-register.csv`. A control is
not credited merely because it appears in a design document. Review is required
after any display/touch/power schematic change, supervisor change, vehicle
profile change, CAN definition update, Tesla OTA, new radio/cloud feature, or
failed validation test.

Before a Park-only vehicle pilot:

1. all mandatory validation rows have objective evidence;
2. open S4 risks have an explicitly reviewed disposition;
3. physical bypass and unpowered native continuity are demonstrated on the
   installed harness configuration;
4. CAN receive-only construction is inspected and measured;
5. sleep current, thermal behavior, and update recovery pass;
6. compatibility is limited to the exact documented Highland profile.
