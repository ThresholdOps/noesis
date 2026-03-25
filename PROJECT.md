# NOESIS Project Contract

## Purpose

NOESIS defines the project-level contract for a persistent world where:

- TinyMUX holds authoritative world state
- perception is enforced against that state
- telemetry captures factual world-side events for downstream use
- rendering and AI operate only on derived inputs

## System Boundary

Inside NOESIS:

- world state and state transitions in TinyMUX
- realm and perception governance layered on TinyMUX Reality Levels
- event telemetry capture and storage
- downstream rendering, presentation, and observability tooling
- AI and retrieval layers that consume derived data

Outside NOESIS:

- human interpretation that attempts to override world truth
- clients or bots acting as world authority
- any presentation layer that bypasses world validation or perception limits

## Source-of-Truth Hierarchy

1. TinyMUX world state and rule enforcement
2. repository-level NOESIS contracts in `PROJECT.md`, `LAYERS.md`, and `docs/telemetry-contract.md`
3. conceptual architecture docs under `docs/`
4. bridge/runtime artifacts under `out/`
5. rendering, Discord, and AI outputs

If a lower layer conflicts with a higher layer, the higher layer wins.

## Boundary by Responsibility

### World State

Belongs to TinyMUX:

- objects, locations, exits, relations
- state transitions and refusals
- authoritative Rx/Tx / Reality Level mechanics
- any decision about whether an action actually occurred

### Telemetry

Belongs to NOESIS observability:

- factual capture of world-side attempts, accepted events, refusals, and emits
- append-only event records for downstream processing
- raw fields required for later perception enrichment

Telemetry is not authority. It reports authority.

### Rendering

Belongs to downstream presentation:

- human-readable projections
- Discord or other client outputs
- summaries, formatting, filtering, and localized phrasing

Rendering must not invent world facts or replace perception rules.

### AI / RAG

Belongs to downstream interpretation:

- narrative generation
- contextual retrieval
- summarization and explanation

AI / RAG is read-only with respect to world truth.

## Foundational Design Primitives

NOESIS is organized around three primitives:

- Relations are primary.
- Information is the effect or record of change in relations.
- Structures define the bounded forms in which relations occur and information becomes legible.

Mapped onto NOESIS:

- TinyMUX provides authoritative structures and the current relational world state.
- Telemetry is structured capture of relational change.
- Perception is observer-relative access to information about relational change.
- Renderer and AI layers are downstream consumers of information, not authors of world truth.

## Why TinyMUX Is Authoritative

NOESIS uses TinyMUX as the authoritative state engine because the current project direction already grounds world state, visibility, and Reality Level mechanics there. NOESIS adds observability, governance, semantics, and downstream rendering contracts on top of that mechanism.

In practical terms:

- TinyMUX decides what exists and what happened
- NOESIS defines how that reality is governed, observed, captured, and rendered
- bridge and AI layers remain downstream and non-authoritative
