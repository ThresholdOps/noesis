# ADR: TinyMUX Read-Side Integration via Softcode Relay and `@log`

## Status

Proposed / Accepted for NOESIS integration planning.

## Context

Recent upstream TinyMUX discussion and documentation work clarified that ordinary client output is supported for human observation, but should not be treated as a stable machine-readable integration contract.

Player-visible output may vary due to color settings, client width, encoding negotiation, Pueblo mode, server configuration, permissions, and release-to-release formatting changes.

TinyMUX maintainers identified the safer MUSH-family pattern for unambiguous observation:

```text
softcode listener / puppet / @listen / @ahear
→ caller-controlled @log payload
→ external consumer
```

## Decision

NOESIS should prefer server-side softcode classification plus `@log` delivery for read-side TinyMUX observation.

The primary ingestion path should be:

```text
TinyMUX in-world activity
→ softcode relay classifies activity
→ @log writes caller-controlled structured line
→ NOESIS tails/reads log
→ NOESIS normalizes event
→ NOESIS applies perception, memory, validation, and downstream routing
```

Human-readable client output parsing should remain fallback/debug tooling only, not the main integration contract.

## Consequences

NOESIS should implement a TinyMUX `@log` event adapter.

NOESIS should define a local event schema for records emitted by TinyMUX softcode. This schema is ours, not a TinyMUX built-in API.

NOESIS should keep telnet/session transcript capture only for debugging, comparison, and operator review.

NOESIS should use `muxscript` for deterministic tests and replay where the network/client layer is irrelevant.

## Non-goals

This does not require TinyMUX core changes.

This does not require a new TinyMUX API.

This does not give external tooling omniscient world-state access.

This does not authorize PLLUM or any local model to write directly to TinyMUX.
