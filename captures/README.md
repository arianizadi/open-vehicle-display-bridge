# Capture Policy

Do not commit raw vehicle captures. They can contain VINs, location, phone,
account, driving, and diagnostic data.

Store acquisition notes, a SHA-256 hash, equipment/configuration, target
manifest, timestamps rounded as needed, redaction method, and the smallest
synthetic or scrubbed test vector that reproduces the relevant behavior.
