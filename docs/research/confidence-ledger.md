# Research confidence ledger

Accessed: 2026-08-30
Initial target: user-owned 2025 Tesla Model 3 Highland

## Rating method

| Rating | Meaning |
| --- | --- |
| **High** | Direct, specific evidence from the responsible primary source, or an original target observation. Still subject to revision and reproduction. |
| **Medium** | Multiple consistent sources, a qualified independent observation, or a strong inference from confirmed interfaces. |
| **Low** | Single anecdote, indirect evidence, model-year mismatch, or an inference with important alternatives. |
| **Unknown** | The reviewed evidence does not establish the claim. Unknown is not false. |

Evidence classes are `official`, `independent`, `open-source primary`,
`inferred`, `user scope`, and `absence finding`. Source IDs resolve through
`source-register.csv`.

## Claims

| ID | Claim | Class | Confidence | Target relevance | Evidence / reasoning | Required validation or action |
| --- | --- | --- | --- | --- | --- | --- |
| CL-001 | The initial target is a user-owned 2025 Model 3 Highland. | User scope | **High** | Direct | Explicit project scope supplied by the owner. | Record exact build date, region, steering side, MCU/AP generation, and Tesla firmware before hardware work. |
| CL-002 | A 2025 Model 3 resolves to SOP8 or SOP9 solely from model year. | Official | **High that model year alone is insufficient** | Direct | Tesla bounds SOP8/SOP9 by factory and manufacture date; the cutover occurs during calendar 2025. [TES-001] | Resolve plant and manufacture date privately before donor or harness selection. |
| CL-003 | LHD Highland has separate X860-X861 main display/power and X176-X189 control/touch/AUX paths; RHD uses X860A/X176A at the MCU side. | Official | **High** | Direct | Tesla SOP8/SOP9 LHD and RHD schematics publish both paths and steering-side designators. [TES-002], [TES-003], [TES-016], [TES-017] | Resolve steering side and verify physical connector labels, keying, orientation, and part revisions on matching donor hardware. |
| CL-004 | X861 and X189 are two mating halves of one connector. | Official | **High that this is false** | Direct | Tesla identifies them as separate harness connector endpoints for the main and sideband paths. [TES-002], [TES-003], [TES-005], [TES-007] | Preserve both paths in the bench breakout and verify the device-side counter-mating parts physically. |
| CL-005 | The Highland X860-X861 main transport is conclusively FPD-Link III, GMSL, or conventional DisplayPort. | Unsupported protocol claim | **Unknown** | Direct | Tesla calls the aggregate contacts `Display Data`; separate DP AUX and HPD nets support a DisplayPort-family inference but do not disclose the main-lane electrical standard. [TES-002], [TES-003] | Capture EDID/DisplayID, DPCD, AUX/HPD, lane count/rate, and link training on a matching bench display. |
| CL-006 | Tesla-native touch transaction framing and arbitration are fully documented by the public schematics. | Absence finding | **Unknown** | Direct | The drawings identify differential I2C SDA/SCL and touch-interrupt nets, but do not publish transaction semantics, addresses, timing, or arbitration behavior. [TES-002], [TES-003] | Characterize native touch on a current-limited donor bench without copying proprietary firmware. |
| CL-007 | A 12 V-only SBC supply can be connected directly to Highland's accessory feed. | Official safety correction | **High that this is unsafe** | Power | Tesla documents a 16 V-class LV platform and accessory voltage up to 16 V. [TES-010], [TES-011] | Design and validate the complete accessory voltage, transient, thermal, and brownout envelope. |
| CL-008 | The separately named X860-X861 display supply is proven to share the full accessory-feed envelope. | Absence finding | **Unknown** | Power | The display schematic names a `12V` rail while the accessory bulletin covers a separate 16 V-class source. Public documents do not establish equivalence. [TES-002], [TES-003], [TES-011] | Measure the donor display rail and startup current before selecting a power design. |
| CL-009 | Highland electrical references include an X181 connector whose Tesla part changes between SOP8 and SOP9. | Official | **High for the published connector records** | CAN/profile identity | Tesla publishes X181 under both programs with different Tesla part numbers. [TES-012], [TES-015] | Verify market/build presence, role, bitrate, and safe signals; initial hardware remains physically receive-only. |
| CL-010 | A minimum external-video/pass-through MVP requires complete Tesla CAN reverse engineering. | Architecture inference | **Medium that this is unnecessary** | Scope | Tesla publishes the display paths separately from the candidate vehicle-data connector, so video characterization can begin on an isolated donor display. [TES-002], [TES-003], [TES-012] | Prove the bench path with CAN disconnected; separately observe whether wake or configuration eventually requires authenticated state. |
| CL-011 | The exact Highland data-connector buses, bit rates, and accessible signals are established in this repository. | Absence finding | **Unknown** | Direct | Connector records alone do not establish the chosen vehicle's bus topology or signal applicability. [TES-012], [TES-015] | Obtain authorized information and use a protected, hardware-silent capture interface. |
| CL-012 | opendbc contains relevant Tesla HW4 2024-25 support and a Model 3 vehicle DBC. | Open-source primary | **High** | Candidate input | Its supported-car table and repository DBC are public. [OSS-001], [OSS-002], [OSS-003] | Pin an immutable commit and preserve license and provenance. |
| CL-013 | Every opendbc Tesla signal applies unchanged to the selected 2025 Highland connector and firmware. | Open-source applicability | **Low** | Direct | Repository support is not a guarantee about every bus, tap point, vehicle revision, or firmware version. | Validate message by message against controlled target observations and publish per-signal confidence. |
| CL-014 | joshwardell/model3dbc guarantees 2025 Highland coverage. | Open-source applicability | **Low** | Direct | The repository describes Model 3/Y generally but makes no target-year guarantee. [OSS-004] | Use only as an attributed comparison set. |
| CL-015 | AOSP includes Google Play or Google Mobile Services for unrestricted use. | Official | **High that this is false** | Software choice | Google states that Play access is separate and not automatic for AOSP-derived devices. [OSS-014], [OSS-017] | Plan an open distribution path or undertake formal Android compatibility and licensing work separately. |
| CL-016 | Linux MGB4 support proves the Highland link is FPD-Link III. | Inference control | **High that it does not** | Lab planning | MGB4 supports named lab modules, but no primary source ties those protocols to the target car. [OSS-013] | Select protocol-specific equipment only after target-link identification. |
| CL-017 | The open project should begin with CAN transmit enabled. | Safety decision | **High that it should not** | Safety-critical | MVP goals are achievable with passive video characterization and listen-only telemetry; community tools include dangerous send/replay paths. | Enforce silent mode in hardware, remove transmit code from discovery builds, and add a physical transmit inhibit. |
| CL-018 | The older DS90UB948-Q1 display teardown proves the Highland serializer choice. | Independent applicability | **High that it does not** | Video | The teardown is for 2017-2019 hardware; Highland publishes a different two-path topology. [TES-013], [TES-014], [TES-002] | Use the older TI pair only on a verified matching older donor; characterize Highland independently. |

## Promotion rule

A vehicle-specific claim may move to **High** only when it has:

1. a named source or original capture with immutable hash;
2. exact target metadata (vehicle family, build region/date, steering side, and
   relevant Tesla firmware);
3. a reproducible procedure and expected result;
4. at least one negative or control test;
5. no unresolved contradiction in the source register; and
6. a review that separates observation from inference.

Safety-critical claims additionally require failure-injection evidence. A
successful happy-path drive or a single owner's report is never enough to
promote bypass, wake/power, touch arbitration, or active-CAN behavior.
