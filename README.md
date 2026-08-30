# Open Vehicle Display Bridge

An open, bench-first reference architecture for adding a secondary computer and
video source to an existing vehicle display without making that computer part
of the vehicle's safety path.

The first concrete target is a **2025 Tesla Model 3 (Highland)**. The project is
not affiliated with, endorsed by, or sponsored by Tesla or any vehicle
manufacturer.

> [!WARNING]
> This repository is research and architecture, not a released in-vehicle
> product. Do not install prototype hardware in a road vehicle. A display fault
> can hide warnings, controls, or the reversing camera. Work on a powered EV can
> cause injury, vehicle damage, fire, or loss of warranty coverage.

## Engineering premise

Adding an independent computer and external video source to the factory display
is not an Android application alone. The difficult parts are the automotive
interfaces and safe-state behavior:

- an Android/mobile compute module;
- vehicle-specific high-speed display harnesses;
- a high-speed video/touch bridge;
- an external-input switch or compositor;
- automotive power, sleep, wake, and fault handling;
- CAN/data interfaces and vehicle-specific firmware; and
- a physical/native bypass path.

The open design does not assume or require installing software on the Tesla
computer. It targets a reversible inline hardware bridge. For the 2025 Model 3,
Tesla's public electrical reference shows a separate sideband display connector
carrying DisplayPort AUX, I2C, hot-plug detection, and touch interrupt signals.
That makes this a hardware, signal-integrity, and safety project—not an Android
app alone.

We do **not** need to reverse engineer every Tesla CAN message to prove the
core idea. The first useful milestone is external video on a salvaged display,
then a two-source bench bridge that always falls back to the native source.
CAN begins physically listen-only and is optional.

## Architecture

    Factory MCU video ─────┐
                           ▼
                    fail-native selector ───► factory display
                           ▲                         ▲
    external HDMI/DP ─► video transmitter           │
                                                     │
    display sideband ◄──────── touch bridge ─────────┘

    vehicle power ─► protected power stage ─► compute
                         │
                         └─► independent safety supervisor
                                  │
                                  └─ owns selector; default = native

    vehicle CAN ─► physically listen-only interface ─► signal gateway
                                                        │
                                                        └─► versioned adapter

Linux or Android never owns the safety selector. Loss of power, a crashed
computer, stale state, reverse selection, undervoltage, overtemperature, or an
unknown fault must select the factory display path.

See [system architecture](docs/architecture/system.md), [interfaces](docs/architecture/interfaces.md),
and [hazard analysis](docs/safety/hazard-analysis.md).

## Initial build path

1. Identify the exact 2025 Model 3 electrical-reference revision and connector
   family from build plant/date and non-sensitive vehicle metadata.
2. Bench a salvaged matching display with a known-good source. Do not connect
   to the car.
3. Prove a de-energized native path and two-source switching on the bench.
4. Add touch/backchannel translation and read-only telemetry.
5. Run brownout, crash, thermal, stale-data, and repeated-switching tests.
6. Consider a reversible, park-only vehicle pilot only after every safety gate
   passes.

The details are in [ROADMAP.md](ROADMAP.md), [the bench guide](docs/build-guides/bench-rig.md),
and [the prototype BOM](bom/prototype.csv).

## Supporting past and future Teslas

Vehicle differences live in versioned manifests rather than application code.
A manifest records:

- model, market, plant, build-date range, MCU generation, and Tesla schematic
  program;
- connector part numbers, pinouts, mating parts, lane/link characteristics,
  timing, EDID, and sideband behavior;
- evidence provenance and confidence for each field;
- safe-state rules and supported features; and
- hashes for captured test vectors and automated hardware-in-the-loop results.

The schema and first draft target are in [protocol/manifests](protocol/manifests/).
Adding a vehicle revision requires an evidence pack, two-person pinout review,
generated continuity fixtures, bench validation, and regression tests. A nearby
model year is never assumed compatible.

The full automation boundary and promotion pipeline are in
[vehicle revision onboarding](docs/architecture/vehicle-onboarding.md).

## Repository map

| Path | Purpose |
| --- | --- |
| [docs/research](docs/research/) | Tesla interface, prior-art, and evidence research |
| [docs/architecture](docs/architecture/) | System boundaries, interfaces, and threat model |
| [docs/safety](docs/safety/) | Hazards, gates, fault injection, and validation |
| [hardware](hardware/) | Original schematics, PCB, harness, and enclosure work |
| [firmware](firmware/) | Safety supervisor, touch bridge, and listen-only CAN |
| [software](software/) | Display manager, UI, gateway, adapters, and updater |
| [protocol](protocol/) | Revision manifests, legal captures, test vectors, and signal models |
| [bom](bom/) | Evidence-rated cost models; not purchasing advice |
| [tools](tools/) | Bench automation and repository validation |

## Current status

**Research/architecture only.** There are no released schematics, firmware
binaries, harnesses, or road-ready builds yet. Unknowns are intentionally
visible in the [confidence ledger](docs/research/confidence-ledger.md).

## Contributing and licensing

Start with [CONTRIBUTING.md](CONTRIBUTING.md), [SAFETY.md](SAFETY.md), and the
[clean-room policy](docs/legal/clean-room-policy.md). Original software and
firmware are GPL-3.0-or-later; original hardware is CERN-OHL-S-2.0; original
documentation is CC-BY-4.0. See [LICENSE.md](LICENSE.md).

Tesla is a trademark of its owner and is used only to identify compatibility
and research scope. See [TRADEMARKS.md](TRADEMARKS.md).
