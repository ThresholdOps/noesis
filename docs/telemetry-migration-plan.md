# Telemetry Migration Plan

## Status

Draft

## Purpose

This document defines the planned migration from current prototype bridge telemetry toward the canonical `noesis.telemetry.v0` contract.

## Current State

- `docs/telemetry-contract.md` defines `noesis.telemetry.v0`.
- Current bridge output is prototype/ad hoc.
- Current bridge behavior is documented as prototype/fallback in `docs/runtime/prototype-status.md`.
- Current bridge read-side behavior is not canonical ADR-0001 read-side integration.
- Current fixture validation covers TinyMUX `@log` JSONL fixtures, not bridge telemetry.

## Target Contract

The target contract is defined by `docs/telemetry-contract.md`.

Minimum required core fields include:

- `schema_version`
- `event_id`
- `ts_utc`
- `run_id`
- `seq`
- `event_type`
- `event_phase`
- `producer`
- `actor`
- `location`
- `raw`

Required producer fields include:

- `producer.kind`
- `producer.source`
- `producer.authoritative`

Required raw capture reserves fields such as:

- `command_raw`
- `content_raw`
- `verb_raw`
- `from_dbref`
- `to_dbref`
- `realm_tx_raw`
- `realm_rx_raw`
- `realm_context_raw`
- `perception_context_raw`
- `target_raw`
- `error_raw`

Required coverage includes:

- `SAY_ATTEMPT`
- `MOVE_ATTEMPT`
- `POSE_ATTEMPT`
- `ROOM_EMIT`
- `REFUSAL`
- `ERROR`

Open questions:

- Whether current bounded SAY/MOVE compatibility fields should be preserved only under `raw` or under a separate diagnostic compatibility object.
- Whether unresolved perception should use a fixed sentinel value, explicit `null` fields, or a structured unresolved object.
- Whether the canonical bridge-facing emitter grammar should be versioned separately from landed `noesis.telemetry.v0` records.

## Migration Principles

- Do not treat player-visible telnet transcript parsing as canonical input.
- Keep transcript scraping as fallback/debug until replaced.
- Prefer TinyMUX softcode `@log` records as canonical read-side source.
- NOESIS owns normalization after ingestion.
- Perception must not be faked as `perceived_by: [actor]`.
- If perception is unresolved, mark it explicitly as unresolved rather than pretending it was computed.
- PLLuM must receive only NOESIS-prepared bounded context.

## Proposed Migration Steps

1. Add bridge telemetry fixture examples matching `noesis.telemetry.v0`.
2. Add local tests for telemetry fixture shape.
3. Add CI validation for telemetry fixtures.
4. Add an adapter/mapping spec from TinyMUX `@log` JSONL events to NOESIS telemetry events.
5. Refactor bridge/prototype output behind a clearly named fallback/debug path.
6. Implement canonical `noesis.telemetry.v0` emitter.
7. Add tests for `SAY_ATTEMPT`, `MOVE_ATTEMPT`, `POSE_ATTEMPT`, `ROOM_EMIT`, `REFUSAL`, and `ERROR`.
8. Only then consider live/runtime integration changes.

## Compatibility Notes

- Existing ad hoc fields such as `type`, `content`, and `perception.perceived_by` are not canonical.
- If preserved temporarily, they should live under diagnostic/raw compatibility fields or be mapped explicitly.
- Existing consumers should not assume the prototype shape is stable.

## Non-Goals

This document does not:

- modify `bridge.py`
- implement telemetry emission
- implement ingestion
- implement perception
- modify PLLuM prompts
- connect to TinyMUX
- modify CI
- modify deploy workflow

## References

- `docs/telemetry-contract.md`
- `docs/audits/2026-07-09-contract-implementation-gap.md`
- `docs/runtime/prototype-status.md`
- `docs/adr/ADR-0001-tinymux-read-side-integration-softcode-log.md`
- `docs/tinymux/event-schema-v0.md`
- `fixtures/tinymux/log_events/v0/`
- `services/noesis-bridge/src/bridge.py`
