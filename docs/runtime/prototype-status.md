# Runtime Prototype Status

## Status

Draft / Current State

## Purpose

This document classifies current runtime/service files so contributors do not treat prototype code as canonical architecture.

## Canonical Boundary

References:

- `docs/adr/ADR-0001-tinymux-read-side-integration-softcode-log.md`
- `docs/tinymux/event-schema-v0.md`
- `docs/audits/2026-07-09-contract-implementation-gap.md`

Canonical TinyMUX read-side integration is:

```text
TinyMUX softcode relay
→ caller-controlled @log
→ structured records
→ NOESIS ingestion
```

Player-visible transcript parsing is fallback/debug only.

## Current Runtime Classification

| File | Current classification | Reason |
|---|---|---|
| `services/noesis-bridge/src/bridge.py` | Prototype / fallback read-side bridge | Uses player-login/raw stream/`NOESIS:` line extraction rather than canonical `@log` records; emits ad hoc telemetry shape. |
| `services/elias-bot/elias_mux_bot.py` | Incomplete prototype | `main()` calls missing `loop()`; parsing helpers appear unused; runtime path appears unfinished. |
| `services/noesis-bridge/src/renderer_v0.py` | Prototype renderer / operational experiment | Contains hardcoded config/runtime path patterns and local import workaround; not canonical contract implementation. |
| `.github/workflows/deploy.yml` | Existing deployment workflow / operational risk | Deploys on push to `main` without broad test/lint/build gate; separate CI fixture validation now exists but deploy hardening is not yet done. |

## What This Means

- These files may be useful as experiments, fallback tools, diagnostics, or historical prototypes.
- They are not evidence that the canonical integration boundary has been implemented.
- They should not be extended as canonical architecture without an explicit migration plan.
- Future implementation should align with ADR-0001, `event-schema-v0`, `telemetry-contract`, and the perception model.

## Near-Term Remediation

1. Add deploy gating or at least document deploy risk.
2. Reconcile telemetry contract with bridge output.
3. Replace or isolate transcript-scraping bridge as fallback/debug.
4. Define adapter from `@log` JSONL records to NOESIS ingestion.
5. Replace `perceived_by: [actor]` stub with explicit unresolved perception handling or real Rx/Tx resolution.
6. Repair or quarantine `elias_mux_bot.py` if it remains in repo.

## Non-Goals

This document does not:

- change runtime behavior
- modify `bridge.py`
- modify `elias_mux_bot.py`
- modify `renderer_v0.py`
- modify deployment workflows
- implement ingestion
- implement adapter logic
- connect to TinyMUX
- modify PLLuM prompts
