# Open-source landscape

Accessed: 2026-08-30
Initial target: 2025 Tesla Model 3 Highland
Policy: reuse only material with clear provenance and a compatible license; do not use extracted competitor firmware

## Summary

There is a strong open-source foundation for CAN capture, DBC decoding, signal normalization, USB touch, MCU firmware, Android/Linux UI, and testing. There is **not** a verified open-source drop-in bridge for the 2025 Highland center-display link in the evidence reviewed.

The practical strategy is therefore:

1. reuse mature open tooling around the unknown vehicle-specific edge;
2. isolate Tesla-specific knowledge in manifests, DBC/VSS overlays, harness definitions, and test vectors;
3. derive the Highland display bridge from original measurements;
4. keep vehicle transmit physically disabled during the discovery and MVP phases.

An entry in this landscape is not blanket approval to vendor its code. Pin a commit, review the exact files and transitive licenses, retain notices, and record the decision before importing anything.

## Candidate projects

| Project | Area and license | Useful contribution | 2025 Highland relevance and limit | Disposition |
| --- | --- | --- | --- | --- |
| [Android Open Source Project](https://source.android.com/) and [AAOS VHAL](https://source.android.com/docs/automotive/vhal) | Android platform; mostly Apache-2.0, with separately licensed components | Optional Android UI/app platform; VHAL provides a clean property boundary between vehicle gateway and apps. AAOS power documentation is a useful architecture reference. | Does not solve Tesla video or CAN. Google Mobile Services and Google Play are not part of AOSP and require separate compatibility/licensing work. | **Evaluate later**. A Linux MVP reduces bring-up scope; keep the gateway API compatible with a future AAOS adapter. |
| [COVESA Vehicle Signal Specification](https://github.com/COVESA/vehicle_signal_specification) | Protocol-independent vehicle signal model; MPL-2.0 | Stable names and metadata for normalized, read-only vehicle signals. Fits `protocol/vss-overlays/`. | Generic taxonomy, not a Tesla decoder. Tesla-specific mappings must be independently validated. | **Adopt as semantic model**, with license notice and local overlays. |
| [comma.ai opendbc](https://github.com/commaai/opendbc) | DBCs, CAN parsing, vehicle interfaces, and safety models; MIT | Tesla DBC material, parser patterns, checks/counters, and a tested safety architecture. Its supported-car table lists Tesla Model 3 HW4 2024-25. | Openpilot support does not prove that every signal exists on the Highland connector used by this project, nor that every model-year definition is stable. Some code is aimed at control, which is outside MVP. | **Reference and selectively reuse**. Pin a commit and validate each read-only signal on the target vehicle. Do not enable control paths. |
| [opendbc Tesla Model 3 vehicle DBC](https://github.com/commaai/opendbc/blob/master/opendbc/dbc/tesla_model3_vehicle.dbc) | Tesla-specific DBC within opendbc; MIT repository | Candidate identifiers, layouts, counters, and checksums for controlled validation. | Public DBC content is reverse-engineered and may combine generations. File presence is not proof that it matches the particular target tap point. | **Seed hypotheses only** until confirmed by target captures. |
| [joshwardell/model3dbc](https://github.com/joshwardell/model3dbc) | Model 3/Y DBC; MIT | Independent comparison set for message/signal hypotheses and provenance cross-checks. | README does not make a 2025 Highland coverage guarantee. Never resolve conflicts by majority vote; resolve with controlled target observations. | **Reference only** initially. |
| [Linux can-utils](https://github.com/linux-can/can-utils) | SocketCAN capture, filter, generation, and replay tools; per-file GPL-2.0-only/BSD-3-Clause/Linux-syscall-note licensing | `candump`, `canplayer`, filters, bus statistics, and reproducible capture/replay formats. | Tooling is vehicle-neutral. Replay and generation can transmit; those commands must be blocked from in-vehicle discovery workflows. | **Adopt for bench and listen-only capture**; review per-file SPDX terms. |
| [cantools](https://github.com/cantools/cantools) | DBC/ARXML/etc. parsing, decoding, plotting, and C generation; MIT | Reproducible DBC validation, log decoding, and generated read-only parsers. | Correct decoding depends on correct DBC data. The tool cannot establish that a community signal definition is true. | **Adopt** for tooling/tests. |
| [SavvyCAN](https://github.com/collin80/SavvyCAN) | Cross-platform CAN capture, visualization, and reverse-engineering UI; MIT | Visual comparison, frame filtering, signal graphing, and offline log exploration. | It includes sending/replay capabilities. Use offline or behind a hardware-enforced transmit inhibit during discovery. | **Developer tool**, not a runtime dependency. |
| [comma.ai panda](https://github.com/commaai/panda) | CAN/CAN-FD interface firmware and safety model; MIT unless otherwise specified | Strong example of vehicle-specific safety rules, unit/mutation tests, relay-malfunction checks, and HIL discipline. | Not a display bridge and not automatically the correct Highland harness/interface. `allOutput` examples are expressly inappropriate for this project's discovery phase. | **Architecture/test reference**; consider supported hardware only for a separately reviewed lab interface. |
| [candleLight firmware](https://github.com/candle-usb/candleLight_fw) | `gs_usb` USB-CAN firmware; MIT core, with separately licensed STM32 components | Low-cost SocketCAN-compatible listen-only lab adapter patterns. | Supported MCU set and CAN-FD capability vary by board/branch. Verify galvanic isolation, transceiver, termination, voltage, and true silent mode before vehicle use. | **Bench candidate**, not an assumed production solution. |
| [TinyUSB](https://github.com/hathach/tinyusb) | Embedded USB host/device stack; MIT | USB HID touch-device emulation, CDC diagnostics, DFU/update transport, and portable MCU support. | Does not implement the Tesla-native touch side. A production USB VID/PID must be legitimate; examples' identifiers cannot be copied into a product. | **Strong candidate** for `firmware/touch-bridge/`. |
| [Zephyr RTOS](https://github.com/zephyrproject-rtos/zephyr) | Embedded RTOS; Apache-2.0, with component-level exceptions | CAN, USB HID, watchdog, settings, logging, signed-update, and test frameworks for bridge/supervisor MCUs. | Board support and worst-case timing must be verified. Using an RTOS does not itself create a safety case. | **Evaluate** against a smaller bare-metal design; favor it if drivers and update infrastructure reduce custom code. |
| [Linux MGB4 driver](https://cdn.kernel.org/doc/html/latest/admin-guide/media/mgb4.html) | Mainline V4L2 driver for a specialized automotive frame grabber; kernel licensing applies | Demonstrates a supported Linux capture/generation workflow for certain FPD-Link III and GMSL2/3 lab modules. Could inform a professional bench setup. | Its supported protocols do **not** identify the Tesla Highland link or any target component. Associated lab hardware is specialized and must be sourced separately. | **Lab reference only** pending target-link identification. |

## Recommended reuse boundary

```text
apps / UI shell
      |
      v
vehicle-neutral signal API  <---- COVESA VSS naming
      |
      v
Tesla adapter               <---- validated DBC/VSS overlay + test vectors
      |
      v
read-only SocketCAN         <---- can-utils / cantools / vetted interface firmware

video manager               <---- Linux/AOSP APIs
      |
      v
original Highland bridge    <---- clean-room hardware + firmware + measurements

touch manager               <---- TinyUSB/Zephyr candidate on external USB side
      |
      v
original native-touch bridge<---- clean-room target-specific implementation
```

The Tesla adapter must not leak model-specific frame IDs or link details into UI code. A target manifest should select the exact harness, capture provenance, DBC overlay, expected firmware ranges, and safety policy.

## License and provenance rules

- Record source URL, immutable commit, license file, imported paths, and modifications in a dependency manifest before merging third-party material.
- Do not copy snippets from forums, manuals, screenshots, binaries, or vendor firmware merely because they are publicly reachable.
- Keep factual observations separate from copyrightable expression: record connector measurements, timings, state transitions, and independently written register sequences with lab provenance.
- Community Tesla DBC files may be used only under their declared license and still require target validation. Preserve attribution and original license notices.
- Do not combine MPL/GPL-covered files into permissively licensed deliverables without a file-level compliance review. Tool use is different from source incorporation.
- Do not represent AOSP as including Google Play. Google states that Google Mobile Services are outside AOSP and Google Play access is not automatic. See https://source.android.com/docs/compatibility/compatibility-faq.
- Keep captures sanitized: remove VIN, precise location, phone identifiers, account data, Bluetooth identifiers, and unrelated traffic before publication.

## Gaps no listed project closes

The following remain original-research tasks for the 2025 Highland:

- center-display connector and safe breakout;
- exact display-link electrical/protocol characteristics;
- native touch transport and arbitration;
- native-first hardware bypass and failure detection;
- target power/wake/transient envelope;
- proof that an external source can meet the display's timing without disrupting the Tesla UI;
- exact CAN buses/signals available at the chosen Highland data connector;
- regression testing across Tesla firmware updates.

No project above should be cited as proof of an exact serializer/deserializer, scaler, FPGA, cable pinout, or Tesla protocol version.

## Shortlist for the first prototype

1. **Linux + SocketCAN + can-utils + cantools** for capture and test automation.
2. **COVESA VSS overlays** for the application-facing signal schema.
3. **TinyUSB** on a dedicated touch-bridge MCU if USB HID emulation is needed.
4. **Zephyr or a minimal audited firmware stack** for the power/safety supervisor after timing and board requirements are known.
5. **opendbc and model3dbc only as attributed hypotheses**, never as unverified target truth.
6. **Original video-bridge hardware and firmware**, developed from target measurements with a hard native bypass.
