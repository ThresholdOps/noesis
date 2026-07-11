# NOESIS Telemetry v0 Fixture Examples

These are sample telemetry fixtures for `noesis.telemetry.v0`.

References:

- `docs/telemetry-contract.md`
- `docs/telemetry-migration-plan.md`
- `docs/audits/2026-07-09-contract-implementation-gap.md`

These fixtures are not emitted by current `bridge.py` yet.

Current `bridge.py` is prototype/fallback and is not canonical telemetry.

Future tests and emitters should align to these examples and `docs/telemetry-contract.md`.

Fixture files:

- `say_attempt.jsonl`
- `move_attempt.jsonl`
- `pose_attempt.jsonl`
- `room_emit.jsonl`
- `refusal_and_error.jsonl`

Assumptions made from `docs/telemetry-contract.md`:

- `ts_utc` is the canonical telemetry timestamp field.
- `actor` and `location` objects use `dbref` and `name_raw` when present.
- Reserved `raw` fields are included with `null` when they are unavailable or not applicable.
- `POSE_ATTEMPT` uses `event_phase: "attempt"`.
- `ROOM_EMIT` uses `event_phase: "emit"` and may have `actor: null`.
- `REFUSAL` uses `event_phase: "refusal"`.
- `ERROR` uses `event_phase: "error"`.
- Refusal/error details are carried in `raw.error_raw` until a narrower subtype convention is defined.
