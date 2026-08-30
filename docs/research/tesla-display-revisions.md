# Tesla Display Interface Research

Accessed 2026-08-30. This file distinguishes Tesla-published facts from
independent measurements and engineering inference.

## Initial target: 2025 Model 3 Highland

"2025 Model 3" does not select one electrical revision. Tesla's
[Model 3 Electrical Reference index](https://service.tesla.com/docs/Model3/ElectricalReference/)
currently maps production plant/date ranges as follows:

| Tesla program | Fremont production | Shanghai production | Project status |
| --- | --- | --- | --- |
| SOP8 / program 233 | 2024-01-01 through 2025-10-03 | 2023-09-01 through 2025-09-12 | candidate |
| SOP9 / program 333 | 2025-10-04 onward | 2025-09-13 onward | candidate |

Most 2025-model-year cars will resolve to SOP8, but model year is not production
date. A late calendar-2025 build can be SOP9. The owner should use the full VIN
privately and publish only non-identifying fields. Tesla's
[official VIN guide](https://service.tesla.com/docs/Model3/ServiceManual/2024/en-us/GUID-B7B9507C-C984-41F2-89EE-D23CA4E682ED.html)
identifies 5YJ as Fremont and LRW as Shanghai; position 10 S is model year 2025,
while position 11 identifies plant. The door-jamb manufacture date is still
required near an SOP boundary.

## Confirmed Highland topology and steering-side split

Tesla's public [SOP8 special-cables schematic](https://service.tesla.com/docs/Model3/ElectricalReference/prog-233/interactive/pdf/rf_special_cables_lhd_print.pdf)
and [SOP9 schematic](https://service.tesla.com/docs/Model3/ElectricalReference/prog-333/interactive/pdf/rf_special_cables_lhd_print.pdf)
show two separate MCU-to-center-display paths for **LHD** cars. The corresponding
[SOP8 RHD](https://service.tesla.com/docs/Model3/ElectricalReference/prog-233/interactive/pdf/rf_special_cables_rhd_print.pdf)
and [SOP9 RHD](https://service.tesla.com/docs/Model3/ElectricalReference/prog-333/interactive/pdf/rf_special_cables_rhd_print.pdf)
drawings use MCU-side designators X860A and X176A while retaining display-side
X861 and X189. An LHD interface profile must never resolve for an RHD car.

### Main display and power path

- MCU X860 to display X861;
- cavity 1 carries a 12 V named rail and cavity 2 ground;
- aggregate cavity H is labeled only "Display Data"; individual contacts/lane
  mapping are not published;
- X860: Tesla 1101044-01-B, Rosenberger 99K20K-1D5A5-B;
- X861: Tesla 1086455-03-B, Rosenberger 99K11D-1D5A5-D.

See Tesla's SOP8 connector references for
[X860](https://service.tesla.com/docs/Model3/ElectricalReference/prog-233/connector/x860/)
and [X861](https://service.tesla.com/docs/Model3/ElectricalReference/prog-233/connector/x861/).
The net name "12V" is not a complete power specification; awake/sleep voltage,
startup current, transients, and protection remain bench measurements. Highland
uses a 16 V-class low-voltage system, and Tesla's
[third-party accessory bulletin](https://service.tesla.com/docs/ServiceBulletins/External/CD/CD-23-17-001_LV_Power_Circuit_for_Third-Party_Accessories_2024_M3_2025_MY_R2.pdf)
warns that the nominal accessory voltage can reach 16 V. The project must not
feed a 12 V-only front end from that 16 V accessory circuit. The separately
named X860/X861 display rail remains unmeasured and must not be inferred from
the platform or accessory specification.

### Control, touch, and AUX path

- MCU X176 to display X189;
- X176 cavities 1/2 map to X189 4/3: CENTER-I2C-SDA P/N;
- X176 cavities 5/6 map to X189 8/7: CENTER-I2C-SCL P/N;
- X176 cavities 3/4 map to X189 2/1: MUX-DP2-AUX P/N;
- X176 cavity 8 maps to X189 5: CENTER-TOUCH-INTb;
- X176 cavity 7 maps to X189 6: MUX-DP2-HPD;
- X176: Tesla 1660464-00-A, Hirose GT25-8DS-HU;
- X189: Tesla 1660464-01-A, Hirose GT25-8DS-HU(21).

See Tesla's connector references for
[X176](https://service.tesla.com/docs/Model3/ElectricalReference/prog-233/connector/x176/)
and [X189](https://service.tesla.com/docs/Model3/ElectricalReference/prog-233/connector/x189/).
Tesla's [center-display service procedure](https://service.tesla.com/docs/Model3/ServiceManual/2024/en-us/GUID-429DDA16-EED3-44D0-8E30-2314DE5A9817.html)
also shows two harness connections.

X861 and X189 are distinct harness-connector designators at the display
endpoint; they are not mating halves. A Highland interposer must preserve and,
if needed, switch both independent paths.

## What remains unknown

Tesla calls the X860–X861 high-speed contacts "Display Data." The separate AUX
and HPD nets strongly indicate a DisplayPort-family transport, but the public
schematic does not state the main-lane electrical standard, lane count/rate,
DPCD behavior, EDID/DisplayID, link training, or signal conditioning. Those
items remain **inferred or unknown** until captured on a matching bench display.
There is no credible basis to assume GMSL.

SOP8 and SOP9 publish the same LHD signal names and endpoint connector part
numbers, while the cited LHD cable lengths differ. The published RHD lengths do
not show that same change, but RHD uses different MCU-side designators. Keep
plant, SOP, and steering-side profiles separate until physical and bench
validation proves that sharing is safe.

## Older Model 3/Y is a separate protocol profile

The 2017–2019 display teardown identifies an LG 1920x1200 panel with a TI
DS90UB948-Q1 FPD-Link III deserializer and a Cypress/Infineon touch controller:
[Electronics360 teardown](https://electronics360.globalspec.com/article/14039/teardown-tesla-model-3-center-touchscreen-display-2017-19-model) and
[TI DS90UB948-Q1 datasheet](https://www.ti.com/lit/ds/symlink/ds90ub948-q1.pdf).
This makes a DS90UB949-Q1/A-Q1 evaluation board a credible older-display bench
candidate. It does **not** establish the Highland main transport. Never reuse
the old six-pin/FPD-Link design for Highland without measurement.

## Data needed before a harness or donor purchase

Keep sensitive originals private and publish only scrubbed facts:

1. factory and exact manufacture month/year;
2. left/right-hand drive, market, trim, drivetrain, and rear-display options;
3. infotainment processor and Autopilot hardware as separate fields;
4. current Tesla software version for every capture;
5. center display and car-computer part/revision label photos;
6. existing display-harness assembly labels;
7. the applicable LHD/RHD display-path housings, keys, latches, orientations,
   and markings;
8. actual diagnostic connector for the specific market/build;
9. awake/sleep power envelope; and
10. bench EDID/DisplayID, DPCD, link timing/rate, AUX/HPD, differential-I2C,
    touch interrupt, wake, sleep, and reverse behavior.

Tesla publishes X181 connector records in both
[SOP8](https://service.tesla.com/docs/Model3/ElectricalReference/prog-233/connector/x181/)
and [SOP9](https://service.tesla.com/docs/Model3/ElectricalReference/prog-333/connector/x181/),
with a changed Tesla part number. This is evidence that CAN/data connector
identity belongs in the exact revision profile. It does not establish that the
owner's market exposes the connector, its bitrate, or a safe signal set.

Harness CAD must not freeze a plausible connector mate until mechanical
fit/keying is verified against owned donor hardware.

## Automated revision onboarding

Each manifest pins a vehicle profile, connector records, harness pin map,
protocol observations, read-only CAN profile, evidence, capture hashes, and
safe-state policy. CI validates the schema and produces cross-revision diffs.
Fixtures should be generated from the same manifest used by firmware.

The resolver performs exact matching only. An unknown physical harness identity,
profile mismatch, or unverified field can enable bench identification but must
leave external video disabled and the native path selected. A harness should
eventually carry a read-only EEPROM/QR identity checked against the signed
manifest hash.
