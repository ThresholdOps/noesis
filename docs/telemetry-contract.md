# NOESIS Telemetry Contract v0

## Scope

This document defines the repository-level telemetry contract for NOESIS v0.

It defines intended producer direction, minimum event coverage, and JSONL schema requirements.
It does not claim that all producer paths are implemented today.

## Canonical Producer Direction

The intended authoritative telemetry path is:

MUX-side emitter protocol -> bridge ingest -> append-only JSONL -> optional downstream enrichment/rendering

Repository truth:

- MUX-side emission is the authoritative producer direction
- bridge-side ambient parsing is transitional and non-authoritative
- rendering and AI are downstream consumers only

If bridge-side parsing and MUX-side emitted telemetry disagree, the MUX-side emitter contract wins.

## Telemetry Objectives

Telemetry v0 must capture factual world-side signals needed for later enrichment without making narrative assumptions.

Telemetry exists to preserve:

- causal order
- actor and location anchors
- raw content where applicable
- realm and perception-relevant raw context
- refusal/error visibility as first-class outcomes

## Minimum Event Coverage v0

Telemetry v0 must cover these envelopes:

- `SAY_ATTEMPT`
- `MOVE_ATTEMPT`
- `POSE_ATTEMPT`
- `ROOM_EMIT`
- `REFUSAL`
- `ERROR`

Notes:

- `ROOM_EMIT` is used here instead of plain `EMIT` to keep the scope explicit at v0.
- `REFUSAL` is the telemetry envelope for denied actions; domain-specific refusal names may be carried in subtype fields.
- `ERROR` is for capture or emission-path failures, not world-truth replacement.

## Raw Capture vs Enrichment

### Raw Capture

Raw capture is the required authoritative payload written at ingest time.

It must carry enough information to support later:

- observer-set expansion
- realm-aware filtering
- perception reconstruction or enrichment
- rendering in multiple clients

### Optional Enrichment

Optional enrichment is downstream and non-authoritative.

It may add:

- resolved names
- observer projections
- derived perception sets
- render-friendly phrasing

Optional enrichment must not overwrite or discard raw capture fields.

## JSONL Schema v0

Each line is one JSON object.

### Required Core Fields

Every event record must include:

- `schema_version`: string, fixed to `noesis.telemetry.v0`
- `event_id`: stable event identifier within the capture domain
- `ts_utc`: event timestamp in UTC ISO-8601
- `run_id`: capture-run identifier
- `seq`: monotonic sequence within the run
- `event_type`: canonical event type
- `event_phase`: one of `attempt`, `fact`, `refusal`, `error`, `emit`
- `producer`: object describing producer source
- `actor`: object or `null`
- `location`: object or `null`
- `raw`: object containing uninterpreted payload relevant to the event

### Required Producer Fields

- `producer.kind`: string
- `producer.source`: string
- `producer.authoritative`: boolean

Examples:

- `kind = "mux_emitter"`
- `kind = "bridge_parser"`

### Required Actor / Location Fields

If present, actor and location objects must carry:

- `dbref`
- `name_raw`

`name_raw` is capture-time raw naming, not a canonical identity guarantee.

### Required Realm / Perception-Relevant Raw Fields

`raw` must preserve, when available:

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

Fields may be `null` when unavailable, but the schema reserves them because later enrichment depends on them.

### Optional Enrichment Fields

Optional downstream fields may include:

- `perception`
- `realms`
- `observers`
- `render_hints`
- `resolved`

These are additive only.

## Event-Type Notes

### SAY_ATTEMPT

Minimum expectation:

- actor
- location
- raw spoken content
- raw verb if present

### MOVE_ATTEMPT

Minimum expectation:

- actor
- origin location
- destination location or exit anchor
- raw movement command if present

### POSE_ATTEMPT

Minimum expectation:

- actor
- location
- raw pose content

### ROOM_EMIT

Minimum expectation:

- source object or system source where available
- location
- raw emitted content

### REFUSAL

Minimum expectation:

- originating attempted action type
- actor where available
- refusal reason code or raw refusal payload

### ERROR

Minimum expectation:

- failing producer path
- raw error payload
- relation to attempted event if known

## Example: SAY_ATTEMPT

```json
{
  "schema_version": "noesis.telemetry.v0",
  "event_id": "run-2026-03-24T21:00:00Z-000001",
  "ts_utc": "2026-03-24T21:00:00.123Z",
  "run_id": "2026-03-24T21:00:00Z-ab12cd",
  "seq": 1,
  "event_type": "SAY_ATTEMPT",
  "event_phase": "attempt",
  "producer": {
    "kind": "mux_emitter",
    "source": "tinymux.noesis.telemetry",
    "authoritative": true
  },
  "actor": {
    "dbref": "#123",
    "name_raw": "Entity B"
  },
  "location": {
    "dbref": "#456",
    "name_raw": "Room_1"
  },
  "raw": {
    "command_raw": "say hello",
    "content_raw": "hello",
    "verb_raw": "say",
    "from_dbref": null,
    "to_dbref": null,
    "realm_tx_raw": "WORLD.PRIME",
    "realm_rx_raw": "WORLD.PRIME",
    "realm_context_raw": "WORLD.PRIME",
    "perception_context_raw": null,
    "target_raw": null,
    "error_raw": null
  }
}
```

## Example: MOVE_ATTEMPT

```json
{
  "schema_version": "noesis.telemetry.v0",
  "event_id": "run-2026-03-24T21:00:00Z-000002",
  "ts_utc": "2026-03-24T21:00:02.456Z",
  "run_id": "2026-03-24T21:00:00Z-ab12cd",
  "seq": 2,
  "event_type": "MOVE_ATTEMPT",
  "event_phase": "attempt",
  "producer": {
    "kind": "mux_emitter",
    "source": "tinymux.noesis.telemetry",
    "authoritative": true
  },
  "actor": {
    "dbref": "#123",
    "name_raw": "Entity B"
  },
  "location": {
    "dbref": "#789",
    "name_raw": "Room_2"
  },
  "raw": {
    "command_raw": "north",
    "content_raw": null,
    "verb_raw": "move",
    "from_dbref": "#456",
    "to_dbref": "#789",
    "realm_tx_raw": "WORLD.PRIME",
    "realm_rx_raw": "WORLD.PRIME",
    "realm_context_raw": "GATE.UMBRA",
    "perception_context_raw": null,
    "target_raw": "#900",
    "error_raw": null
  }
}
```

## Relationship to Current Bridge

The current bridge implementation may continue to produce transitional JSONL using bridge-side parsing.

That transitional path:

- is useful for development visibility
- is not the repository-authoritative telemetry source
- should evolve toward this v0 contract instead of redefining it
