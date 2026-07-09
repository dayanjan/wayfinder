# Kernel Reuse Evidence (Part C)

The Python kernel persists state across separate tool calls within a session.

- `persistent_df` was created in an earlier cell with shape **30 rows x 3 original columns** (`group`, `x`, `y`).
- `persistent_marker` was set in that earlier cell to the live value: **`kernel_reuse_marker_db_audit_2026_07_08`**.
- In a **later, separately-executed cell** (this one), both objects were accessed directly from kernel memory — no CSV was re-read — and a new column `z = x + y` was appended, giving final shape **(30, 4)**.

Proof that no reload occurred: the assertion `persistent_df` and `persistent_marker` are present in the namespace (`dir()`) succeeded before `z` was computed, and the marker string retained its exact earlier value.

First 3 rows after adding `z`:

```
group      x      y      z
    C 0.0623 2.2395 2.3018
    A 0.8170 3.2270 4.0440
    B 0.8633 5.1041 5.9674
```
