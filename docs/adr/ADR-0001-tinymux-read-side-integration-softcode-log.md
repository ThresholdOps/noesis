# ADR-0001: TinyMUX Read-Side Integration via Softcode Relay and `@log`

## Status

Accepted

## Date

2026-07-09

## Context

TinyMUX player-visible output is intended for human readers, not as a stable machine-readable integration contract.

It may vary due to client settings, color handling, width, encoding negotiation, Pueblo mode, server configuration, permissions, and release changes.

Maintainer clarification upstreamed in `brazilofmux/tinymux#846` confirms that external tooling should not rely on parsing player-visible output as the primary integration boundary.

This matters for NOESIS because read-side observation must be reliable enough to support perception, memory, validation, replay fixtures, and bounded NPC response routing.

## Decision

NOESIS will adopt the following read-side integration assumption:

TinyMUX owns world execution.

TinyMUX softcode relay classifies observable activity while it is still meaningful as an in-world event.

TinyMUX `@log` emits caller-controlled structured records.

NOESIS ingests those records and owns event normalization, perception, memory, validation, and routing.

PLLuM receives only NOESIS-prepared context and produces bounded NPC phrasing under NOESIS control.

## Preferred Architecture

```text
TinyMUX activity
→ softcode listener / puppet / @listen / @ahear
→ caller-controlled @log payload
→ local structured event record
→ NOESIS ingestion
→ NOESIS perception, memory, validation, routing
→ PLLuM bounded NPC response
→ NOESIS validator
→ gated write-back path
```

## Scope

This ADR defines the preferred read-side observation boundary between TinyMUX and NOESIS.

It does not define the final write-back implementation, the complete event schema, the PLLuM prompt format, or the production deployment topology.

## Consequences

NOESIS must not treat player-visible TinyMUX output as the canonical read-side integration contract.

Client transcript parsing may remain available only as fallback, diagnostics, or manual debugging support.

Replay fixtures should be built from structured `@log` records rather than raw telnet/player-output transcripts.

Muxscript remains useful for deterministic command/replay testing, but it is not the primary observation path.

PLLuM must not read from or write to TinyMUX directly.

NOESIS becomes the control boundary for perception, memory, validation, routing, and gated write-back.

## Non-Goals

This ADR does not forbid telnet, muxscript, or transcript capture for debugging.

This ADR does not require immediate removal of existing transcript-based experiments.

This ADR does not make PLLuM responsible for TinyMUX protocol handling, socket handling, softcode execution, or direct world mutation.

## Next Actions

1. Define a local JSONL event schema for TinyMUX softcode-emitted records.
2. Prototype a TinyMUX `@log` event adapter.
3. Build replay fixtures from `@log` records.
4. Keep muxscript for deterministic command/replay tests.
5. Demote telnet/player-output parsing to fallback/debug status.
6. Document the gated write-back boundary in a later ADR.

## References

- `brazilofmux/tinymux#846`
