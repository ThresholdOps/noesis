# NOESIS Project Contract

## Purpose

NOESIS defines contract-governed boundaries for persistent worlds where:

- one selected world engine holds authoritative state and enforces rules;
- perception limits access to world information;
- cognition and narrative operate on bounded, derived inputs;
- interfaces present authorized projections and submit action intents;
- every boundary is versioned, fixture-tested and CI-enforced.

NOESIS is the contract and policy fabric joining the world engine, cognition
and interfaces. It is not a competing source of world truth.

## Current Reference Deployment

Black Signal selects SpacetimeDB as its authoritative world engine.

The initial reference stack is:

- SpacetimeDB TypeScript module for world state, rules and mechanical
  perception;
- NOESIS adapters and services for contracts, telemetry, memory, retrieval,
  cognition and direction;
- Vue as a diagnostic client;
- Unreal Engine as the intended rich client.

TinyMUX remains a legacy and research integration target. Its existing
contracts are retained within their declared TinyMUX compatibility scope.

## Invariants

### One world authority

The selected world engine is the only authority for mechanically relevant
state and accepted state transitions.

For Black Signal, SpacetimeDB decides:

- what exists;
- current entity and location state;
- who controls an entity;
- whether an action is legal;
- what mechanical effects occur;
- who is mechanically entitled to receive a state projection or event.

### No privileged external actor

A human, model, narrative director, operator and interface follow the same
contract-governed action boundary. None may write world state directly.

### Candidates are not facts

Model text, retrieval output, operator notes and narrative plans are not world
facts. They become world events only after validation and acceptance by the
world engine.

### Perception precedes cognition

The engine determines whether an observer was entitled to receive information
about an event. NOESIS may derive memory, belief or interpretation only from
authorized observations and explicit canon sources.

### Presentation is not authority

Vue, Unreal Engine, Discord and other clients render authorized projections.
They do not enforce secrets as a substitute for server-side access control.

## Source-of-Truth Hierarchy

1. The selected world engine's committed state and accepted world events.
2. Repository-level NOESIS contracts and accepted ADRs.
3. Authenticated action results and engine-to-NOESIS mappings.
4. Observer-specific perception records.
5. Derived memory, retrieval and narrative state.
6. Rendering, interface and model output.

If a lower layer conflicts with a higher layer, the higher layer wins.

## Boundary by Responsibility

### World Engine

The selected engine owns:

- entities, locations, containment and mechanically relevant relations;
- state transitions, refusals and domain rules;
- principal identity, control grants and capabilities;
- mechanical perception and safe projections;
- durable records of accepted world events;
- mechanical schedules and timers.

For Black Signal these responsibilities belong to SpacetimeDB reducers, tables
and views.

### Actions

External components submit intent through a versioned world-action contract.
The engine authenticates the principal, verifies control and capabilities,
checks state preconditions, applies rules and returns an authoritative result.

Only an accepted action may create world events.

### Telemetry and Chronicle

The engine's durable world-event stream is the factual chronicle.

NOESIS telemetry normalizes that chronicle for downstream consumers while
preserving order, causation, entity anchors and perception decisions.

Attempted, denied and invalid actions remain action-result or audit data unless
the world explicitly models the attempt itself as an observable event.

The existing `noesis.telemetry.v0` contract remains a TinyMUX compatibility
contract. Engine-neutral work proceeds in a new version rather than silently
changing v0 semantics.

### Perception

Mechanical observability belongs to the world engine. NOESIS consumes explicit
perception decisions and builds observer-bounded memory and context.

`LAYERS.md` defines the semantic 32 REALMS contract independently of engine
storage. Implementations may use TinyMUX Reality Levels, SpacetimeDB state or a
future mechanism without changing realm meaning.

### Cognition and RAG

NOESIS cognition owns:

- memory and retrieval;
- persona and canon context;
- provenance and epistemic status;
- bounded model requests;
- candidate validation and quarantine.

Models do not read world tables, telemetry files or memory stores directly and
do not issue engine commands.

### Narrative Direction

The director owns scenes, pacing, plot pressure and proposed NPC initiative.
It consumes chronicle and narrative state but acts only through legal world
actions.

### Canon

Authored lore, secrets, biographies and campaign structure live behind a
future `noesis.canon.v0` ingest boundary. Mechanically relevant projections may
enter the world engine; presentation assets may enter clients. Shared stable
identifiers connect the projections.

### Rendering

Rendering owns human-readable and audiovisual presentation, localization,
formatting and client interaction. It must not invent authoritative state or
expand perception rights.

## Foundational Design Primitives

NOESIS is organized around three primitives:

- Relations are primary.
- Information is the effect or record of change in relations.
- Structures define the bounded forms in which relations occur and information
  becomes legible.

Mapped onto NOESIS:

- the world engine provides authoritative structures and relational state;
- world events capture committed relational change;
- perception grants observer-relative access to information about change;
- cognition derives memory, belief and interpretation;
- interfaces render authorized projections.

## Engineering Method

Every new boundary follows:

```text
contract → fixtures → validator → CI → implementation
```

Architecture and transport decisions require measured evidence. Transitional
runtime paths must remain explicitly labeled and must evolve toward repository
contracts rather than redefining them.

## Governing Decisions

- `ADR-0001` governs the TinyMUX read-side compatibility boundary.
- `ADR-0002` establishes engine-neutral NOESIS boundaries and selects
  SpacetimeDB as the Black Signal reference world engine.
