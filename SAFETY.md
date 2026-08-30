# Safety

This repository does not contain an automotive-qualified product. No design,
test, or disclaimer here guarantees road safety, legal compliance, warranty
coverage, electromagnetic compatibility, or fitness for a particular vehicle.

## Non-negotiable rules

- Prototype first on salvaged bench hardware.
- Never work around high voltage or airbags without the applicable service
  procedure, training, and equipment.
- Never probe an unidentified connector in a powered vehicle.
- Current-limit new power assemblies and use a fused emergency disconnect.
- The factory/native image is the de-energized and fault state.
- A physical direct-coupler rollback must be available.
- Initial vehicle experiments are stationary and controlled.
- The CAN listener cannot transmit by component population and PCB routing, not
  only by software configuration.
- Unknown, stale, corrupt, or conflicting state selects native.
- Do not obscure warnings, speed, gear state, controls, or the reversing camera.

Stop immediately for unexpected heat, odor, smoke, current draw, link loss,
vehicle alert, boot loop, touch mismatch, or a failure to return native.

Read the [hazard analysis](docs/safety/hazard-analysis.md) and
[fault-injection plan](docs/safety/fault-injection-plan.md) before hardware work.
