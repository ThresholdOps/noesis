# TinyMUX `@log` JSONL Event Schema v0

## Status

Draft

## Purpose

This document defines the initial JSONL record shape for TinyMUX softcode-emitted `@log` events.

The schema is intended for replay fixtures and future NOESIS ingestion work. It gives TinyMUX softcode a stable caller-controlled read-side payload without treating player-visible transcript text as canonical machine input.

## Boundary

One JSON object per line represents one TinyMUX-observed event emitted through caller-controlled softcode and `@log`.

The intended boundary is:

```text
TinyMUX softcode relay
→ caller-controlled @log
→ structured JSONL record
→ NOESIS ingestion
```

NOESIS owns normalization after ingestion.

PLLuM must not consume these records directly from TinyMUX.

This schema does not define write-back.

## Record Format

Each line must be a complete JSON object.

Each record represents one observed TinyMUX event as classified by softcode while the activity is still meaningful as an in-world event.

Records should be stable enough for replay fixtures.

Player-visible transcript text is not canonical input.

## Required Fields

- `schema_version`
  - string
  - recommended value: `tinymux.log_event.v0`
- `event_id`
  - string
  - unique within the producing log stream or replay fixture
- `timestamp`
  - string
  - UTC timestamp in ISO-8601 format
- `source`
  - string
  - producer identifier, for example `tinymux`
- `world`
  - string
  - world or runtime identifier
- `room`
  - object
  - observed room identity
- `actor`
  - object or `null`
  - actor identity when available
- `event_type`
  - string
  - one of the v0 event type values
- `text`
  - string
  - event text as emitted by the softcode boundary
- `visibility`
  - object
  - initial visibility context emitted by TinyMUX softcode

## Optional Fields

- `target`
  - object or `null`
  - direct target when the event has one
- `channel`
  - string
  - local channel or routing hint, for example `room`, `page`, or `ooc`
- `softcode`
  - object
  - relay/listener metadata
- `raw`
  - object
  - source-specific metadata preserved for diagnostics

`raw` may preserve source-specific metadata but must not become the primary contract.

## Event Types

Required `event_type` values for v0:

- `say`
- `pose`
- `emit`
- `enter`
- `leave`
- `page`
- `ooc`
- `system`
- `custom`

## Visibility Model

`visibility` records the initial visibility context known at the TinyMUX softcode boundary.

Suggested fields:

- `scope`
  - string
  - examples: `room`, `private`, `global`, `system`
- `audience`
  - array of strings
  - optional explicit audience dbrefs or logical groups
- `realm`
  - string or `null`
  - optional realm/perception label if softcode can provide it

NOESIS may enrich, normalize, or reinterpret visibility later. The softcode record is only the source observation.

## Example Records

Room `say` event:

```json
{"schema_version":"tinymux.log_event.v0","event_id":"tmux-20260709-000001","timestamp":"2026-07-09T12:00:00Z","source":"tinymux","world":"noesis-v0","room":{"dbref":"#3","name":"Room_1"},"actor":{"dbref":"#1","name":"Wizard"},"event_type":"say","text":"Przyjdźcie natychmiast.","visibility":{"scope":"room","audience":["#3"],"realm":null},"raw":{"verb":"+nsay"}}
```

`pose` event:

```json
{"schema_version":"tinymux.log_event.v0","event_id":"tmux-20260709-000002","timestamp":"2026-07-09T12:00:05Z","source":"tinymux","world":"noesis-v0","room":{"dbref":"#3","name":"Room_1"},"actor":{"dbref":"#1","name":"Wizard"},"event_type":"pose","text":"Wizard unosi dłoń w ostrzegawczym geście.","visibility":{"scope":"room","audience":["#3"],"realm":null},"raw":{"verb":"+pose"}}
```

Softcode-emitted `system` event:

```json
{"schema_version":"tinymux.log_event.v0","event_id":"tmux-20260709-000003","timestamp":"2026-07-09T12:00:10Z","source":"tinymux","world":"noesis-v0","room":{"dbref":"#3","name":"Room_1"},"actor":null,"event_type":"system","text":"softcode relay heartbeat","visibility":{"scope":"system","audience":["staff"],"realm":null},"raw":{"relay":"NoesisTelemetry","kind":"heartbeat"}}
```

## Replay Fixture Guidance

Replay fixtures should be built from structured `@log` records rather than raw telnet or player-output transcripts.

Fixtures should preserve:

- original record order
- original `event_id`
- original `timestamp`
- exact `text`
- enough `room`, `actor`, and `visibility` context to reproduce NOESIS ingestion behavior

Fixtures should not require a live TinyMUX connection.

## Validation Rules

- Each line must parse as one JSON object.
- `schema_version` must equal `tinymux.log_event.v0` for this draft schema.
- Required fields must be present.
- `event_type` must be one of the v0 values.
- `timestamp` must be UTC ISO-8601 text.
- `room` must include at least a stable identifier such as `dbref`.
- `actor` may be `null` only when the event has no meaningful actor.
- `visibility` must be an object.
- `raw` must be optional and non-authoritative.

## Non-Goals

This spec does not implement ingestion.

This spec does not implement parsing.

This spec does not define socket handling.

This spec does not define live TinyMUX integration.

This spec does not define PLLuM prompts.

This spec does not define write-back.

This spec does not require removing transcript capture used for fallback, diagnostics, or manual debugging.

## Open Questions

- Should `room` and `actor` require both `dbref` and `name`, or only `dbref` for v0?
- Should `visibility.audience` use room dbrefs, actor dbrefs, logical groups, or a constrained union?
- Should `event_id` be generated by TinyMUX softcode, NOESIS ingestion, or both with separate IDs?
- Should `world` be configured by softcode, runtime environment, or NOESIS ingestion?
- Which softcode relay metadata belongs in `softcode` versus `raw`?
