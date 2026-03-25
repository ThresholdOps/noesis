# Project Decisions

- NOESIS operating bootstrap is local to this repository and must use NOESIS paths only.
- Repository docs are mandatory startup context before bounded implementation work.
- `project_memory/` is the continuity source for session-to-session handoff.
- `os_sandbox/` is the source for project operating state and night-run flow.
- `PROJECT.md` defines NOESIS system boundary and source-of-truth hierarchy.
- NOESIS project truth is organized around three foundational primitives: Relations, Information, and Structures.
- `LAYERS.md` defines the intended NOESIS 32 REALMS governance contract on top of TinyMUX Reality Levels.
- `docs/telemetry-contract.md` defines telemetry v0 and the intended authoritative producer direction.
- This bootstrap does not redesign NOESIS, TinyMUX gameplay logic, bridge behavior, or production orchestration.
