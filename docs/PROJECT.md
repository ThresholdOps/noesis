# NOESIS Project Bridge Note

The canonical NOESIS project contract now lives at the repository root in `PROJECT.md`.

Use root `PROJECT.md` for:

- system boundary
- source-of-truth hierarchy
- the split between TinyMUX authority, telemetry, rendering, and AI

This `docs/` note remains only as a public-facing bridge.

Public repo handling remains unchanged:

- example configuration may live in git
- live local configuration must not live in git
- `services/noesis-bridge/config.example.yaml` is example-only
- a real local `services/noesis-bridge/config.yaml` must remain outside version control
