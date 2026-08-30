# Security Policy

## Reporting

Do not open a public issue for a vulnerability that could enable CAN injection,
unsafe display control, update compromise, vehicle-data exposure, or bypass of
a safety interlock. Use GitHub's private vulnerability reporting for this
repository when available, or contact the repository owner privately through
their GitHub profile.

Include affected revision, impact, reproduction conditions, and a safe proof of
concept. Never test against a vehicle you do not own or have explicit permission
to inspect.

## Supported versions

There are no supported releases yet. Research commits and prototype artifacts
are not safe for road use.

## Design baseline

- independent supervisor owns the display selector;
- unpowered/fault state is factory-native;
- CAN is physically listen-only by default;
- updates are intended to be signed, atomic, and rollback-capable;
- external inputs and debug services are untrusted;
- sensitive captures are minimized, scrubbed, and never committed raw.
