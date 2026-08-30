# Threat model

## Scope and safety relationship

This model covers the add-on display bridge, its update/build pipeline, its
local radios and services, the read-only vehicle tap, and the connection to the
2025 Model 3 Highland display system. It does not claim to model Tesla's own
systems.

Security controls support, but do not replace, the fail-native hardware design.
The primary security safety objective is that compromise of the application
computer cannot block access to the native display, misroute native touch, or
transmit onto the vehicle bus.

## Assets

1. Availability and authenticity of the native display, warnings, gear state,
   controls, and reversing view.
2. Exclusive, correct routing of touch events.
3. Integrity and availability of the vehicle communication buses.
4. Safety-supervisor firmware, configuration, update keys, and route controls.
5. Vehicle-revision manifests and decoded signal provenance.
6. User privacy: vehicle identifiers, location, routes, device identifiers,
   media, contacts, and diagnostic captures.
7. Build provenance, release artifacts, dependency integrity, and signing keys.

## Security objectives

- The hardware defaults to native even when application software is hostile.
- Normal assemblies cannot transmit on vehicle CAN.
- Only authenticated, compatible firmware and profile data can be activated.
- Remote services cannot directly control the supervisor or vehicle interface.
- Sensitive captures are opt-in, minimized, redacted, and locally controlled.
- Debug paths are absent or locked in release hardware.
- Recovery does not require a network service or a functioning application OS.

## Actors and assumptions

| Actor | Capability considered |
| --- | --- |
| Accidental fault | Corrupt storage, malformed frames, bad configuration, user error, incompatible profile |
| Malicious application | Code execution as an app or normal OS user on the application computer |
| Remote network attacker | Reachable through Wi-Fi, Bluetooth, projection, browser, or an exposed local service |
| Malicious peripheral | Crafted USB, Bluetooth, HDMI/video, or phone-projection traffic |
| Supply-chain attacker | Tampered dependency, build action, binary, board, or update artifact |
| Local opportunistic attacker | Short physical access to USB/debug ports or removable storage |
| Skilled physical attacker | Extended access, probing and board modification |

The prototype does not promise resistance to a skilled attacker with indefinite
physical possession. It still removes production debug access, protects signing
keys, and detects obvious tampering where practical.

## Trust boundaries

### TB-1: vehicle to add-on

Native video, touch, power, and CAN cross this boundary. Anything decoded from
the vehicle is untrusted until it passes the exact revision adapter, freshness,
counter, plausibility, and conflict checks. The add-on must not drive CAN or an
endpoint outside the validated electrical contract.

### TB-2: supervisor safety island

The supervisor, route control, hardware bypass input, route feedback, and
minimal Park-state feed form the safety island. Application-computer input is
untrusted. The supervisor exposes no general shell, package manager, scripting
engine, network stack, or arbitrary mux-control API.

### TB-3: application computer

The UI OS processes untrusted apps, media, phone projection, USB, Wi-Fi, and
Bluetooth. It may fail completely without preventing a native route. The
vehicle gateway uses least privilege and has no vehicle transmit capability.

### TB-4: update and build pipeline

Source control, CI runners, dependencies, release signing, artifact hosting,
and field updates cross this boundary. A successful CI job is not by itself a
trusted release. Reproducible metadata, review, signatures, SBOMs, and protected
release keys are required.

### TB-5: developer and diagnostic access

Bench-only headers, logging ports, laboratory CAN transmitters, and profile
capture tools must be physically and procedurally separated from release
hardware. A production assembly must not silently gain transmit ability when a
debug flag changes.

## Threats and mitigations

| ID | Threat | Main mitigations | Verification |
| --- | --- | --- | --- |
| T-01 | Compromised app requests local video while moving | Supervisor independently requires fresh, valid Park; application request is non-authoritative; fail-native route | Replay, stale-state, contradictory-state, and moving-state HIL tests |
| T-02 | Compute crash or resource exhaustion freezes a native-looking local image | Heartbeat timeout, local link monitoring, forced native, visible source indication where appropriate | Kill/pause/kernel-panic and GPU-hang fault injection |
| T-03 | Malicious software manipulates mux GPIO | Mux control is not routed to compute; supervisor is sole owner | Schematic/netlist review and penetration test |
| T-04 | Crafted CAN frames falsely indicate Park | Exact profile, counters/freshness/conflict checks, deny on uncertainty, bench and static validation; no sole reliance on UI broker | Recorded/adversarial trace replay and bus-disconnect tests |
| T-05 | Add-on transmits or disturbs vehicle CAN | No TX route, permanent receive-only topology, no termination, bounded stub/loading, separate lab adapter | Schematic inspection, continuity test, bus loading measurement |
| T-06 | Touch event reaches hidden native UI or both sources | Break-before-make, all-contacts-up, exclusive route, route feedback, native on malformed/stuck input | Touch flood, stuck-contact, switching-race tests |
| T-07 | Remote service reaches vehicle/supervisor | Network segmentation, default-deny firewall, no supervisor network route, least privilege, minimal services | Port inventory, route tests, application compromise exercise |
| T-08 | Malicious USB/phone projection exploits media stack | Sandboxing, read-only filesystems where practical, prompt/allowlist peripherals, rapid security updates | Fuzzing, malformed-media tests, dependency scanning |
| T-09 | Forged or incompatible update changes safety behavior | Signed manifests/images, compatibility matrix, protected trust root, A/B recovery, native lock during update | Signature rejection, downgrade, mismatch, interrupted-update tests |
| T-10 | Stolen signing key enables malicious release | Offline or hardware-backed key, limited signers, rotation/revocation plan, transparent release provenance | Release ceremony review and revocation drill |
| T-11 | Wrong vehicle profile is selected | Hardware/build identity checks, authenticated profile, deny-by-default, no selection by editable label alone | Wrong-profile and partial-profile tests |
| T-12 | Diagnostic capture exposes VIN/location/accounts | Data minimization, local storage, explicit collection, automated redaction, short retention, pre-publication scan | Privacy test corpus and release scanning |
| T-13 | Supply-chain dependency executes in privileged context | Pin versions and hashes, SBOM, review updates, isolate build jobs, prefer source builds | Dependency diff and provenance checks |
| T-14 | Physical bypass is disabled by software | Hardwired priority path independent of firmware | Powered/unpowered continuity and forced-input tests |
| T-15 | Debug interface modifies supervisor or profile | Disable/lock debug in release, authenticated recovery, physical presence for service | Production-board debug-access test |
| T-16 | Denial of service through video/touch/backchannel | Input bounds, rate limits, watchdogs, link timeout, native fallback | Protocol fuzzing and sustained flood tests |

## Abuse cases

### Hostile application computer

Assume root compromise of Linux or Android. The attacker can render arbitrary
content, forge normal application heartbeats, and request local mode. It still
must not be able to select local outside independently confirmed Park, change
the touch route directly, disable the physical bypass, update the supervisor,
or transmit on vehicle CAN.

### Malformed or changed vehicle signals

Assume a Tesla software update changes an arbitration ID, bit meaning, counter,
or timing. The adapter should produce `UNKNOWN`, `STALE`, or `CONFLICT`, never a
best guess. That denies local mode and marks the profile unsupported pending a
new bench validation.

### Interrupted update

Assume power is removed during every write and reboot boundary. Native bypass
must remain available. Application images use a recoverable A/B or equivalent
scheme. Supervisor recovery is small, independently authenticated, and does not
depend on the application partition.

### Malicious contributor or copied proprietary material

Review provenance, require declarations for captures and protocol facts, scan
for secrets/binaries, and reject leaked firmware, keys, NDA material, or code
without a redistributable license. Open source does not make improperly
obtained material safe to publish.

## Privacy model

- Operate locally by default; cloud telemetry is off unless separately designed
  and explicitly enabled.
- Do not store raw VIN, precise location, contacts, media metadata, or complete
  vehicle traces unless required for a named diagnostic session.
- Use short retention and per-capture purpose metadata.
- Provide a redaction tool and a human review step before issue attachments.
- Test vectors should be synthetic or minimized. Public captures include
  provenance and a statement that personal identifiers were removed.

## Residual risk and review triggers

The project cannot eliminate all risks of modifying an in-vehicle display
path. Residual risk remains unknown until physical hardware and the exact
Highland revision complete the validation matrix. Threat-model review is
mandatory when adding a radio, cloud service, privileged application, update
mechanism, CAN definition, display/touch component, vehicle profile, or active
vehicle interface.
