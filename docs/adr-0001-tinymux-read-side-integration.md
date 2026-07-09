# Deprecated: TinyMUX Read-Side Integration ADR

This document has been superseded by the canonical ADR:

`docs/adr/ADR-0001-tinymux-read-side-integration-softcode-log.md`

The canonical decision is that TinyMUX read-side integration should use:

```text
TinyMUX softcode relay
→ caller-controlled @log
→ structured records
→ NOESIS ingestion
```

Player-visible transcript parsing is fallback/debug only and is not the canonical read-side integration contract.

See also:

`docs/tinymux/event-schema-v0.md`
