# Phase 0: Identify the Exact 2025 Model 3 Target

No trim removal or vehicle probing is required for the initial inventory.

## Owner-supplied metadata

Keep the full VIN private. Record only what is needed to resolve the public
Tesla electrical-reference revision:

- market/country;
- manufacturing plant, if known;
- month and year of manufacture;
- left- or right-hand drive;
- displayed MCU/infotainment processor generation, if Tesla exposes it;
- display and MCU part/revision numbers only when safely observable under the
  official service procedure; and
- clear connector/label photos with barcodes, serials, VIN fragments, faces,
  reflections, and GPS metadata removed.

The project can derive a non-identifying target identifier such as:

    model3-highland-fremont-2025q1-candidate

Do not commit a VIN, license plate, account screenshot, precise location,
Bluetooth identifier, Wi-Fi credential, or service-mode log containing personal
data.

## Resolution workflow

1. Match plant/date against Tesla's current Model 3 Electrical Reference index.
   Current candidate ranges are SOP8/program 233 (Fremont through 2025-10-03;
   Shanghai through 2025-09-12) and SOP9/program 333 after those plant-specific
   cutovers.
2. Download the matching connector reference and schematic pages from Tesla's
   public service site.
3. Record the program/revision and source URL in the vehicle manifest.
4. Compare connector face, keying, assembly part, cavity names, and wire colors
   with the target—without back-probing a powered connector.
5. Mark each field confirmed-official, confirmed-measured, inferred, or unknown.
6. Have a second reviewer approve power, ground, and every sideband assignment.
7. Generate a continuity worksheet and harness labels from the manifest.

If plant/date spans two Tesla programs, both remain candidates until a physical
part or connector reference distinguishes them.
