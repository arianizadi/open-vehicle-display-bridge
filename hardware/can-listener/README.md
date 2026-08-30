# CAN Listener Hardware

The normal assembly is physically receive-only: MCU TX is not routed, no bus
termination is added, and no firmware option can enable transmission. Loading,
stub length, ESD behavior, unpowered behavior, and fault containment require
bench validation.

Any active-CAN research uses visibly different lab-only hardware and is outside
the initial product.
