# Contract vs Implementation Gap Audit — 2026-07-09

## Status

Draft / Review

## Summary

The conceptual layer is coherent and should govern implementation:

- `README.md`
- `PROJECT.md`
- `LAYERS.md`
- `ARCHITECTURE.md`
- `design-constraints.md`
- `event-model.md`
- `event-types.md`
- `perception-model.md`
- `poc.md`

The services layer is still an early prototype and currently diverges from the documented contracts.

## Confirmed Alignment

The current conceptual layer consistently supports these ideas:

- Event and Information are separate concerns.
- The Rx/Tx model separates transmission from reception.
- The 32 REALMS model defines layered visibility and meaning.
- There is no omniscient observer.
- NOESIS is the perception, memory, validation, and routing boundary.
- PLLuM is bounded by NOESIS-prepared context.

## Contract vs Implementation Gaps

### 1. Telemetry contract mismatch

- `docs/telemetry-contract.md` requires schema `noesis.telemetry.v0`.
- Required concepts include `schema_version`, `event_id`, `event_phase`, `producer.authoritative`, and `raw.*` fields such as `realm_tx_raw` and `perception_context_raw`.
- Required coverage includes `SAY_ATTEMPT`, `MOVE_ATTEMPT`, `POSE_ATTEMPT`, `ROOM_EMIT`, `REFUSAL`, and `ERROR`.
- `bridge.py` currently writes an ad hoc schema with fields such as `type`, `content`, and `perception.perceived_by`.
- `bridge.py` currently covers only SAY/MOVE and does not emit fields required by the telemetry contract.

### 2. ADR-0001 vs bridge.py read-side behavior

- ADR-0001 establishes softcode relay plus caller-controlled `@log` as the canonical read-side path.
- Player-visible/telnet transcript parsing is fallback/debug only.
- `bridge.py` currently logs in as a player and extracts `NOESIS:...` lines from a raw stream.
- Therefore `bridge.py` should be classified as fallback/prototype, not canonical integration.

### 3. Perception model stub

- `perception-model.md` makes perception central.
- Current bridge behavior uses `perceived_by: [actor]`.
- This does not implement real Rx/Tx visibility or observer resolution.
- Treat this as a stub, not as the perception model.

### 4. Documentation inconsistency: docs/LAYERS-ATTRS.md

- `docs/LAYERS-ATTRS.md` says semantics live in `LAYERS.md`.
- It uses different nomenclature such as `MATERIAL`, `UMBRA`, `SHADOWLANDS`, and `DREAMING`.
- Canonical `LAYERS.md` uses terms like `WORLD.SHADOW`, `WORLD.UMBRAL`, and `SENSE.SIGHT`.
- `docs/LAYERS-ATTRS.md` references `BITMASKS.md`, which is absent.
- Mark this as needing reconciliation with canonical `LAYERS.md`.

### 5. Documentation inconsistency: docs/MANIFEST.md

- `docs/MANIFEST.md` lacks the bridge-note/advisory status used in `docs/PROJECT.md` and `docs/LAYERS.md`.
- It appears to describe a TinyMUX-specific or older runtime layout.
- It contains `Owner: TODO`, references `scripts/` that may not exist, and `/opt/tinymux/...` paths.
- Root `MANIFEST.md` points to a different repo anchor, `/home/sin/docker/noesis`.
- Mark this as a source-of-truth conflict.

### 6. Startup read order inconsistency

- `AGENTS.md` references `project_memory/00_project_facts.md` and default `03_...`.
- Existing `project_memory` files appear to include `01`, `02`, and `04` but not `00` or `03`.
- Mark this as a continuity/read-order gap.

### 7. Concrete code issue: elias_mux_bot.py

- `main()` calls `bot.loop()`, but `loop` is not defined.
- `login_and_settle` appears incomplete.
- `SAY_PATTERNS`, `CALL_ELIAS`, and `parse_say` are defined but unused.
- Mark this file as an incomplete prototype or broken runtime entry point.

### 8. Concrete code issue: renderer_v0.py

- `os.getpid()` is used in heartbeat context without a normal top-level import.
- There is a local `import os as _os` workaround inside a loop/try.
- Config path is hardcoded to `/opt/tinymux/...` while `bridge.py` uses `NOESIS_BRIDGE_CONFIG`.
- Mark this as config-pattern inconsistency and runtime fragility.

### 9. Operational gap: deploy workflow

- `.github/workflows/deploy.yml` deploys on push to `main`.
- There is no test/lint/build gate before deployment.
- `tests/` and `tests/fixtures/` currently contain only `.gitkeep`.
- ADR-0001 recommends deterministic command/replay testing with muxscript, but no such tests exist yet.
- Mark this as an operational risk.

## Recommended Remediation Order

1. Classify existing `bridge.py` and `elias_mux_bot.py` as prototype/fallback in documentation.
2. Add non-runtime JSONL fixture validation tests for TinyMUX log event v0.
3. Add CI check that runs JSONL fixture validation and basic lint/syntax checks.
4. Reconcile `docs/LAYERS-ATTRS.md` with canonical `LAYERS.md` or deprecate it.
5. Reconcile `docs/MANIFEST.md` with root `MANIFEST.md` or mark it historical.
6. Add a telemetry alignment spec or migration note for `bridge.py`.
7. Only then begin implementation changes.

## Non-Goals

This audit must not:

- change implementation
- modify `bridge.py`
- modify `elias_mux_bot.py`
- modify `renderer_v0.py`
- modify deployment workflow
- create tests
- create validator code
- connect to TinyMUX
- touch PLLuM prompts

## References

- `docs/adr/ADR-0001-tinymux-read-side-integration-softcode-log.md`
- `docs/tinymux/event-schema-v0.md`
- `fixtures/tinymux/log_events/v0/`
- `docs/telemetry-contract.md`
- `docs/LAYERS.md`
- `docs/LAYERS-ATTRS.md`
- `docs/MANIFEST.md`
- `MANIFEST.md`
- `AGENTS.md`
- `project_memory/02_current_state.md`
- `bridge.py`
- `elias_mux_bot.py`
- `renderer_v0.py`
- `.github/workflows/deploy.yml`
