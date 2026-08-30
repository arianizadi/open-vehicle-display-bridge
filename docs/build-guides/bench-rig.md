# Bench Rig Guide

This is the first hardware milestone. It uses a lawfully sourced, matching
salvaged display and never connects experimental electronics to the vehicle.

## Outcome

Display a static test pattern from an external HDMI/DisplayPort source on the
factory screen, record link and power behavior, and remove power without damage.
Touch, CAN, vehicle installation, and video switching are later phases.

## Required evidence before ordering

- exact display assembly part number and clear connector photos;
- Tesla public electrical-reference program for the target build;
- build plant and approximate production date stored privately;
- connector reference, cavity map, mating part, keying, and wire gauge;
- documented voltage, polarity, ground, and current-limit rationale;
- verified video serializer/deserializer family and required configuration;
- two-person review of every powered pin.

For a 2025 Model 3 Highland, both the main high-speed display connector and the
separate sideband connector may matter. Do not transplant a pre-Highland
six-pin harness or assume another 2025 plant/date is identical.

## Bench blocks

    protected bench supply
        │
        ├── fuse + emergency disconnect + current measurement
        │
        └── verified display power/ground

    HDMI test-pattern source
        │
        └── serializer/evaluation module
                │
                └── keyed mating harness ─── factory display

    isolated laptop ─── configuration/debug only

Use commercial evaluation modules for the earliest signal proof when possible,
but select one only after identifying the Highland transport. The TI
DS90UB949-Q1/A-Q1 is useful prior art for verified 2017–2019 FPD-Link III donor
displays; it is **not a Highland BOM choice**. The 2025 main-link electrical
standard remains unknown until measured.

## Procedure

1. Photograph and inventory every part. Record seller, donor model, part
   revision, connector markings, and chain of custody.
2. Perform unpowered continuity and short checks. Compare every result with the
   reviewed manifest.
3. Set the bench supply to the verified voltage with a conservative current
   limit. Keep the output off and the emergency disconnect open.
4. Attach only display power and ground. Do not attach CAN or vehicle harnesses.
5. Power through a fuse while observing current and temperature. Stop on any
   unexpected draw, heat, odor, noise, or voltage collapse.
6. Configure the source for the measured/native timing. Start with a static
   color-bars image containing an obvious frame counter.
7. Attach the video link with power removed. Reapply power and record link-lock,
   first-image time, resolution, color, flicker, and current.
8. Cycle cold power, warm power, source loss, cable removal, and malformed
   timing under controlled conditions.
9. Save minimal logs, photos, register dumps, and scope captures outside Git.
   Commit only scrubbed derivatives plus hashes and acquisition notes.
10. Disconnect, inspect connectors, and repeat continuity/short checks.

## Pass criteria

- no component damage or unexpected heating;
- repeatable image at the verified native timing;
- documented maximum steady and startup current;
- at least 25 cold and 25 warm starts with recorded outcomes;
- no private donor/vehicle data in the evidence pack; and
- another contributor can reproduce the result from the manifest and notes.

Do not proceed to a two-source bridge until this report is reviewed.
