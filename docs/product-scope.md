# Product Scope

## Goal

Create an open, reproducible display bridge that can present an external
computer on the factory screen while preserving a hardware-controlled path to
the native vehicle image.

The first evidence-backed target is one exact revision of the owner's 2025
Tesla Model 3 Highland. "2025 Model 3" alone is not a harness specification:
plant, build date, electrical-reference program, MCU/display part, connector
keying, and regional configuration must be verified.

## In scope

- salvaged-display bench characterization;
- external DisplayPort or HDMI input through a verified link adapter;
- independent fail-native video and touch switching;
- touch translation after the sideband is understood;
- read-only vehicle context for safe source selection and optional UI;
- protected 16 V-class low-voltage power and sleep/wake behavior;
- versioned vehicle manifests, adapters, fixtures, and validation automation;
- reversible installation research; and
- open hardware, firmware, software, and reproducible documentation.

## Explicitly out of scope for initial releases

- active CAN commands or vehicle control;
- defeating OEM safety, security, DRM, subscriptions, or access controls;
- video entertainment while driving;
- replacing mandatory warnings, controls, gear selection, speed, or reversing
  camera;
- high-voltage vehicle work;
- Google certification, Widevine L1, certified CarPlay, or MFi credentials;
- claims of ISO 26262, automotive qualification, regulatory approval, or OEM
  endorsement; and
- support for a model year without a reviewed exact-revision manifest.

## Success criteria

The first milestone is not "boots Android." It is a repeatable bench system
that displays an external test image on a matching salvaged screen and cannot
prevent the original source from being restored. Each later milestone adds one
capability without weakening that invariant.
