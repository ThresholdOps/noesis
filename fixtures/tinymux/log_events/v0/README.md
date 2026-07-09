# TinyMUX `@log` JSONL Replay Fixtures v0

These are sample replay fixtures for the TinyMUX `@log` JSONL event schema v0.

References:

- `docs/adr/ADR-0001-tinymux-read-side-integration-softcode-log.md`
- `docs/tinymux/event-schema-v0.md`

These fixtures are canonical structured examples, not player-visible transcript captures.

They are intended for future validator, ingestion, and replay tests.

They do not imply live TinyMUX connectivity.

Each `.jsonl` file contains one JSON object per line using `schema_version` value `tinymux.log_event.v0`.
