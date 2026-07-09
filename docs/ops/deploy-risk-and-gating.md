# Deploy Risk and Gating

## Status

Draft / Current State

## Purpose

This document records current deploy risk and intended gating direction before runtime implementation work continues.

## Current State

- `.github/workflows/deploy.yml` exists and deploys on push to `main`.
- A separate CI workflow now validates TinyMUX JSONL replay fixtures.
- The repository does not yet have a broad runtime test/lint/build gate.
- Current runtime files are documented as prototype/fallback in `docs/runtime/prototype-status.md`.

## Risk

- Deploying directly from `main` without broad validation can promote broken prototype/runtime code.
- Existing fixture validation is useful but narrow.
- It validates the TinyMUX `@log` JSONL fixture contract only.
- It does not prove that `bridge.py`, `renderer_v0.py`, `elias_mux_bot.py`, ingestion, TinyMUX live integration, or PLLuM routing work.

## Intended Direction

Runtime implementation changes should not proceed as if deploy is fully gated.

Before substantive runtime changes, deploy should either:

1. depend on CI success, or
2. be manually triggered, or
3. be constrained to documentation-only and explicitly safe changes.

Recommended future direction:

- keep CI separate and fast
- add syntax checks for committed Python files
- add JSONL fixture validation
- add runtime unit tests when runtime behavior is clarified
- make deploy require successful CI before production deployment

## Current Minimum Gate

The current minimum automated gate is:

```bash
python3 tests/test_tinymux_log_event_fixtures.py
```

This is not sufficient as a production deploy gate.

## Non-Goals

This document does not:

- modify deployment behavior
- modify CI
- modify runtime code
- add tests
- connect to TinyMUX
- modify PLLuM prompts
- implement adapter or ingestion logic

## References

- `.github/workflows/deploy.yml`
- `.github/workflows/ci.yml`
- `tests/test_tinymux_log_event_fixtures.py`
- `docs/runtime/prototype-status.md`
- `docs/audits/2026-07-09-contract-implementation-gap.md`
- `docs/adr/ADR-0001-tinymux-read-side-integration-softcode-log.md`
