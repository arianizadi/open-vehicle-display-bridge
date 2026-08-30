# Phase 1: External Video on a Salvaged Display

Phase 1 proves only the display-side link. It does not intercept the vehicle.

## Work packages

### WP1 — target acquisition

- Obtain a display assembly matching the reviewed target manifest.
- Obtain a cut donor pigtail or new mating connector without damaging the car.
- Record source, part revision, condition, and return policy.

### WP2 — protected power

- Design a fused, current-limited bench harness with keyed connectors.
- Add reverse-polarity protection, transient suppression appropriate to the
  bench setup, current measurement, and a latching emergency disconnect.
- Review creepage, conductor gauge, connector rating, and thermal behavior.

### WP3 — link characterization

- Identify the display-side deserializer and sideband devices from public
  documentation or non-destructive inspection.
- Confirm native resolution, refresh/timing, link mode, channel count, and
  required initialization.
- Keep register observations separate from original firmware design.

### WP4 — image proof

- Use an evaluation module or minimal original transmitter board.
- Render deterministic test patterns with frame number, grid, RGB ramps, and
  touch-coordinate targets.
- Automate cold/warm starts and record lock time, errors, current, and thermal
  results.

## Deliverables

- reviewed vehicle manifest;
- source/provenance register entries;
- protected-power schematic;
- connector continuity worksheet;
- privacy-scrubbed test report and hashes;
- reproducible source/timing configuration; and
- go/no-go review for Phase 2.

The project must be able to abandon an incompatible donor screen without
changing the target manifest to fit the desired result.
