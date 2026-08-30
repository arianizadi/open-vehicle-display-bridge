# Vehicle Revision Onboarding

This workflow turns a past or future Tesla revision into a testable adapter
without turning model-year guesses into hardware behavior. It automates
bookkeeping, fixture generation, comparison, replay, and regression—not the
human work of validating a connector or interpreting a newly observed signal.

## Compatibility key

A vehicle profile is resolved from the smallest non-identifying exact key that
separates known electrical variants:

- model and generation;
- Tesla electrical-reference program/SOP;
- plant and build-date range;
- left/right-hand drive and market;
- infotainment computer family and part revision;
- display assembly part revision;
- harness assembly and connector identity;
- relevant options; and
- Tesla software version for capture/test evidence.

Autopilot hardware and infotainment hardware remain separate axes. A display
profile never uses the full VIN as a public key.

## Data model

The current single JSON manifest is the portable release unit. As evidence
grows, generated views may split it into:

- vehicle profile — identity and valid build range;
- connector records — manufacturer/Tesla parts, keying, orientation, terminals,
  CAD provenance, and lifecycle;
- harness netlist — endpoints, pin map, impedance, shielding, length, conductor,
  revision, and physical identifier;
- protocol profile — measured transport, EDID/DisplayID, DPCD, AUX/HPD,
  touch/backchannel, timing, bridge configuration, and confidence;
- CAN profile — connector/bus, bitrate, RX allowlist, signal provenance,
  checksum/counter behavior, units, freshness, and OTA version;
- safety policy — native conditions, thresholds, fault actions, and maturity;
- evidence map — claim, URL or measurement, access date, setup, reviewer, and
  artifact hash; and
- validation record — exact hardware/software versions and test outcomes.

The release artifact pins the canonical manifest SHA-256. Hardware should
eventually expose a read-only harness ID using a small EEPROM or QR label. The
supervisor compares physical identity with the authenticated manifest and locks
native on mismatch.

## Pipeline

### 1. Scaffold

Run:

    python3 tools/new_vehicle_manifest.py \
      m3-highland-sop8-fremont-lhd-candidate \
      --model "Model 3" \
      --model-year 2025 \
      --generation Highland \
      --plant Fremont \
      --market US \
      --steering-side LHD \
      --reference-index-url \
        https://service.tesla.com/docs/Model3/ElectricalReference/

The generated profile is candidate/unsupported and contains explicit unknowns.
Generation never enables a feature.

### 2. Bind official documentation

Resolve the Tesla program using plant/date, add immutable source URLs or saved
hashes, and record connector references. A second reviewer checks power, ground,
every signal cavity, housing key, and orientation.

### 3. Generate mechanical/electrical fixtures

Future generators consume the reviewed harness netlist to produce:

- continuity worksheets and two-ended cable labels;
- a fixture pin map and expected-open/short table;
- BOM manufacturer-part lifecycle warnings;
- schematic net labels and connector symbols;
- harness QR/EEPROM payload; and
- a cross-revision pinout diff.

Generated output never substitutes for a physical mate/keying inspection.

### 4. Characterize on a matching donor bench

Capture power behavior, EDID/DisplayID, DPCD, AUX/HPD, main link, touch, wake,
sleep, and fault behavior. Raw data remains private; publish a scrubbed fixture,
SHA-256, setup, and negative/control test. Every observation includes the
vehicle profile and Tesla software version.

### 5. Implement adapters

The video/touch adapter supplies only measured configuration. The CAN adapter
accepts only a curated receive allowlist and emits normalized, timestamped,
quality-tagged signals. Application code never sees raw routing controls or
CAN transmit handles.

### 6. Diff and review

Run:

    python3 tools/compare_vehicle_manifests.py \
      --fail-on-blocking old.json new.json

Changes to connector, harness, interface, Tesla program, or safe-state fields
are marked BLOCKING. CI validates required fields and produces a human-readable
diff; the flag exits nonzero for a blocking change. CI reporting does not
approve such a change: a reviewer must explain and explicitly accept every
blocking difference.

### 7. Replay and HIL

Generate replay cases from scrubbed vectors and hardware-in-the-loop cases from
the manifest. Re-run native continuity, link margin, touch arbitration, CAN
loading, power, thermal, sleep, update, and fault injection on the exact
combination.

### 8. Promote deliberately

Maturity is monotonic through candidate, bench-verified, vehicle-pilot, and
supported. Supported requires evidence from at least two independently
identified cars/part revisions plus full mandatory validation. A Tesla OTA,
part substitution, unresolved contradiction, or safety regression can suspend
or retire the profile.

## Resolver behavior

There is no nearest-year or fallback-to-similar algorithm:

    exact physical/profile match + authenticated data + passed gates
        -> eligible for the profile's explicitly enabled features

    missing field, ambiguous SOP, unknown harness, version mismatch, or fault
        -> native path only

This is how the project can scale across Tesla revisions without pretending the
protocol is universal.
