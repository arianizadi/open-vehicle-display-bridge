# Tests

Testing will cover unit, replay, integration, hardware-in-the-loop, and fault
injection. A new vehicle manifest generates fixtures; it does not inherit a
"nearest" model-year result.

The key invariant is that every unknown, mismatch, stale input, software crash,
power fault, and supervisor fault preserves or returns the factory-native path.
