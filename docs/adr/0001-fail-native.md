# ADR 0001: Fail native under loss of power or control

- Status: Accepted
- Date: 2026-08-30

## Context

The center display presents native vehicle state, warnings, controls, and the
reversing view. An add-on application computer has a large failure and attack
surface. A software-only fallback, a mux-select pull resistor, or a watchdog
running on that same computer cannot establish that the native path survives a
power loss, crash, broken wire, corrupt update, or hostile process.

## Decision

The video and touch bridge will be fail-native by physical design:

- The complete unpowered add-on assembly connects native video and native touch
  between the Tesla infotainment source and display.
- An independent supervisor MCU is the sole owner of route controls.
- Reset, bootloader, high-impedance pins, open control wiring, invalid profile,
  watchdog timeout, power/thermal fault, update, and loss of health all request
  native.
- A hardwired user bypass has priority over firmware.
- Local video is permissive only while the exact target profile is validated,
  the vehicle is positively and freshly known to be in Park, and local link and
  compute health are valid.
- Touch is routed exclusively and break-before-make with the selected video.
- No vehicle installation occurs until the unpowered path and injected-fault
  behavior pass on a representative bench rig.

The final switch technology is deliberately undecided. It must prove native
continuity and signal integrity in the full unpowered circuit; component data
sheet truth tables alone are insufficient.

## Consequences

### Positive

- Most compute, OS, application, and update failures collapse to the original
  Tesla interface.
- The safety claim is narrow, testable, and independent of UI complexity.
- Bench acceptance tests can verify electrical behavior before vehicle use.

### Negative

- The hardware is more complex and may need a normally closed high-speed path,
  route feedback, a supervisor, and a physical bypass.
- Switching and link reacquisition must be characterized for every display
  revision.
- Split-screen compositing cannot be the initial architecture because it would
  put an active processing chain in the native path.

## Rejected alternatives

- **Application-controlled mux:** a compromised or crashed OS could obscure the
  native interface.
- **Software heartbeat on the application computer only:** the same fault could
  break both detection and recovery.
- **Always-on compositor:** loss of the compositor would remove the native
  image; a separate hard bypass would still be required.
- **Default-local with a software escape gesture:** touch or UI failure could
  remove the escape path.

## Verification

Evidence must cover powered and unpowered continuity, supervisor reset, open and
shorted control lines, compute crash, heartbeat loss, local-link loss, touch
faults, brownout, thermal fault, interrupted update, and repeated switching.
Passing one board or vehicle profile does not qualify another.
