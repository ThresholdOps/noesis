# TinyMUX `@log` to NOESIS Telemetry Mapping v0

## Status

Draft

## Purpose

This document defines the planned mapping from canonical TinyMUX softcode-emitted `@log` JSONL records to NOESIS telemetry v0 records.

## Inputs

References:

- `docs/tinymux/event-schema-v0.md`
- `fixtures/tinymux/log_events/v0/`

Input fields:

- `schema_version`
- `event_id`
- `timestamp`
- `source`
- `world`
- `room`
- `actor`
- `event_type`
- `text`
- `visibility`
- `raw`

## Outputs

References:

- `docs/telemetry-contract.md`
- `fixtures/telemetry/v0/`

Output fields:

- `schema_version`
- `ts_utc`
- `run_id`
- `seq`
- `event_id`
- `event_type`
- `event_phase`
- `producer`
- `actor`
- `location`
- `raw`

## Mapping Principles

- TinyMUX `@log` records are canonical read-side observations.
- Player-visible transcript parsing is not canonical input.
- Mapping must preserve source event identity.
- Mapping must not pretend perception was computed if it was not.
- Visibility from TinyMUX is input evidence, not full NOESIS perception resolution.
- NOESIS owns normalization and later perception processing.
- PLLuM must not consume TinyMUX records directly.

## Field Mapping

| TinyMUX log field | NOESIS telemetry field | Rule |
|---|---|---|
| `schema_version` | `raw.realm_tx_raw` source metadata | Preserve input schema version diagnostically under raw source metadata. |
| `event_id` | `raw.realm_tx_raw` source metadata | Preserve source event id; telemetry `event_id` may be newly generated unless the contract is later clarified to require reuse. |
| `timestamp` | `ts_utc` | Convert or validate as UTC ISO timestamp. |
| `source` | `producer.source` | Use `tinymux` for direct emitter source or `noesis.tinymux.adapter` if an adapter is the telemetry producer. |
| `world` | `raw.realm_context_raw` or `raw.realm_tx_raw` source metadata | Preserve source world diagnostically; do not promote it to authoritative world state without normalization. |
| `room.dbref` / `room.name` | `location.dbref` / `location.name_raw` | Map directly where available. |
| `actor.dbref` / `actor.name` | `actor.dbref` / `actor.name_raw` | Map directly where available. |
| `actor.type` | `raw.realm_tx_raw` source metadata | Preserve actor type diagnostically if present. |
| `event_type` | `event_type` | Map through the event type mapping table below. |
| `text` | `raw.content_raw` plus raw source metadata | Preserve original text without transcript scraping. |
| `visibility` | `raw.perception_context_raw` | Preserve as input evidence, not final perception. |
| `raw` | `raw.realm_tx_raw` source metadata | Preserve diagnostic metadata without treating it as the primary contract. |

The current `docs/telemetry-contract.md` reserves scalar/string raw fields such as `realm_tx_raw`, `realm_context_raw`, and `perception_context_raw` but does not define a structured `source_event` object. Until that is clarified, source metadata should be preserved in the smallest compatible representation available to the adapter and documented in fixtures/tests before implementation.

## Event Type Mapping

| TinyMUX event_type | NOESIS telemetry event_type | event_phase | Notes |
|---|---|---|---|
| `say` | `SAY_ATTEMPT` | `attempt` | Room speech observation. |
| `pose` | `POSE_ATTEMPT` | `attempt` | Character pose/action observation. |
| `emit` | `ROOM_EMIT` | `emit` | Room/system-visible emit. |
| `page` | `SAY_ATTEMPT` or future private communication type | `attempt` | Open question: telemetry v0 does not define `PAGE_ATTEMPT`. |
| `enter` | `MOVE_ATTEMPT` | `attempt` | Arrival/movement observation. |
| `leave` | `MOVE_ATTEMPT` | `attempt` | Departure/movement observation. |
| `ooc` | `ROOM_EMIT` or custom mapping | `attempt` | Open question: telemetry v0 does not define `OOC_ATTEMPT`. |
| `system` | `ROOM_EMIT`, `ERROR`, or `REFUSAL` depending on explicit classification | `emit` / `error` / `refusal` | Depends on payload and softcode/adapter classification. |
| `custom` | custom mapping required | `attempt` | Requires explicit subtype convention before implementation. |

If the telemetry contract does not support `page`, `ooc`, or `custom` cleanly, the adapter must mark the case unresolved or route through an explicitly documented compatibility mapping. It must not invent final event families without updating the contract.

## Perception Handling

- Do not emit `perceived_by: [actor]` as if visibility was computed.
- If visibility is unresolved, represent it as unresolved or preserve it under `raw.perception_context_raw`.
- Real Rx/Tx resolution belongs to NOESIS perception processing, not the raw TinyMUX adapter.

## Error and Refusal Handling

- `REFUSAL` and `ERROR` are telemetry events produced by NOESIS/adapter logic, not necessarily direct TinyMUX world events.
- TinyMUX `system` and `custom` records may contribute evidence for `ERROR` or `REFUSAL`, but mapping must be explicit.
- Do not infer refusal/error from arbitrary text without explicit softcode/adapter classification.

## Non-Goals

This document does not:

- implement adapter code
- modify `bridge.py`
- modify telemetry fixtures
- modify TinyMUX fixtures
- modify CI
- implement ingestion
- implement perception
- modify PLLuM prompts
- connect to TinyMUX

## Open Questions

- Should telemetry `event_id` reuse TinyMUX `event_id` or generate a new telemetry id with source event id preserved under `raw`?
- Does telemetry v0 need `PAGE_ATTEMPT`?
- Does telemetry v0 need `OOC_ATTEMPT`?
- How should custom softcode events declare subtypes?
- Where should original TinyMUX text live if telemetry contract keeps no canonical top-level content field?
- Should `visibility.scope` map to `perception_context_raw` only, or also to a normalized visibility hint?
- Should `raw.realm_tx_raw` and related fields remain scalar strings, or allow structured source metadata for mappings like this?

## References

- `docs/adr/ADR-0001-tinymux-read-side-integration-softcode-log.md`
- `docs/tinymux/event-schema-v0.md`
- `fixtures/tinymux/log_events/v0/`
- `docs/telemetry-contract.md`
- `docs/telemetry-migration-plan.md`
- `fixtures/telemetry/v0/`
- `docs/runtime/prototype-status.md`
- `docs/audits/2026-07-09-contract-implementation-gap.md`
