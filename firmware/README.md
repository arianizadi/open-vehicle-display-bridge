# Firmware

Planned firmware components are the independent safety supervisor, touch/HID
bridge, and physically listen-only CAN listener. Application compute cannot
command around supervisor safety policy.

No firmware release exists yet. Future releases require reproducible builds,
signed artifacts, pinned manifest hashes, watchdog/fault tests, and rollback.
