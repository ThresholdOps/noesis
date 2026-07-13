# NOESIS

**Contract-governed persistent worlds where truth is centralized, perception
is distributed, and meaning is emergent.**

---

## Overview

NOESIS separates a persistent-world system into three replaceable layers:

1. a world engine that owns state, rules and mechanical perception;
2. cognition and narrative services that own memory, retrieval and direction;
3. interfaces that present authorized projections and submit action intents.

NOESIS is the versioned contract and policy fabric joining those layers. It is
not an additional source of world truth.

The core assumption is simple:

> A world should exist independently of what any single participant can
> perceive or believe.

## Core Concepts

### Centralized truth

Each deployed world has one authoritative engine. Facts and state transitions
are validated there, not by narration, model output or client presentation.

### Distributed perception

Each entity receives only the subset of state and events it is mechanically
entitled to perceive. Perception is explicit, auditable data.

### Bounded cognition

Models receive NOESIS-prepared context with provenance and visibility
decisions. A generated candidate is not a world fact and cannot issue engine
commands.

### Emergent meaning

Memory, belief and narrative meaning are derived from world events, perception,
canon and interpretation. They do not replace authoritative state.

## Current Reference Architecture

Black Signal selects **SpacetimeDB** as its authoritative world engine.

- **SpacetimeDB / TypeScript** — world state, reducers, authorization,
  mechanical perception, durable world events and safe projections.
- **NOESIS services and adapters** — contracts, telemetry normalization,
  memory, graph/RAG, cognition validation and narrative direction.
- **Vue** — diagnostic development console.
- **Unreal Engine / C++** — intended rich player interface.
- **LLMs** — bounded voices, interpreters and assistants; never arbiters of
  world truth.

TinyMUX remains a legacy and research adapter. Its read-side contracts,
fixtures, audits and 32 REALMS work remain valid within their declared scope.

## System Rule

Humans, models, directors, operators and interfaces have no privileged path
around the world engine.

```text
action intent
→ authenticated and capability-checked engine path
→ authoritative action result
→ committed world event
→ perception decision
→ NOESIS memory, cognition and presentation
```

## Repository Scope

This repository owns NOESIS architecture, contracts, fixtures, validators,
adapters and supporting services. It does not necessarily contain every world
runtime, client asset, deployment secret or operator environment.

The Black Signal SpacetimeDB implementation lives in:

- https://github.com/ThresholdOps/black-signal

## Canonical Documents

Start with:

- `PROJECT.md` — system boundary and source-of-truth hierarchy;
- `LAYERS.md` — engine-neutral 32 REALMS governance;
- `docs/telemetry-contract.md` — TinyMUX-compatible telemetry v0;
- `docs/adr/` — accepted architecture decisions.

Conceptual notes and runtime artifacts must not override these documents.

## Architecture Decisions

- `ADR-0001` — TinyMUX read-side integration through softcode relay and
  caller-controlled `@log`.
- `ADR-0002` — engine-neutral NOESIS boundaries and SpacetimeDB as the Black
  Signal reference world engine.

## Contract Direction

The contract method is:

```text
contract → fixtures → validator → CI → implementation
```

Current and planned contract families include:

- `noesis.telemetry.v0` — retained TinyMUX compatibility contract;
- `noesis.world_action.v0` and its authoritative result;
- `noesis.telemetry.v1` — planned engine-neutral facts and perception;
- `noesis.npc_context.v0` and `noesis.npc_candidate.v0`;
- cognition quarantine records;
- `noesis.canon.v0`.

## What NOESIS Is

- A contract architecture for persistent shared worlds.
- A system where perception is explicit data.
- A boundary between world truth, knowledge, interpretation and presentation.
- A foundation for hidden layers, partial knowledge and asymmetric awareness.

## What NOESIS Is Not

- A chatbot acting as game master and world authority.
- A presentation layer trusted to protect secrets.
- A model with direct access to world state or commands.
- A requirement that every world use the same engine or interface.

## Project Status

NOESIS is in active architectural rebaselining from a TinyMUX-specific
prototype toward engine-neutral contracts with SpacetimeDB as the Black Signal
reference implementation.

APIs remain versioned but unstable until their fixtures, validators and CI
checks establish repository truth.

## Philosophy

> A world becomes more believable when it knows more than any of its
> inhabitants.

## License

This project is licensed under the **Mozilla Public License 2.0 (MPL-2.0)**.

You may use, modify and distribute the software, including commercially. Any
modifications to MPL-licensed source files must remain open under the same
license terms.
