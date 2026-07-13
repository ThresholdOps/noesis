# ADR-0002: Engine-Neutral NOESIS Boundaries and SpacetimeDB Reference Engine

- Status: Accepted
- Date: 2026-07-13

## Context

NOESIS began with TinyMUX as the available authoritative world runtime. That
work established useful contracts, fixtures, validators, CI enforcement, a
semantic 32 REALMS model, and a supported TinyMUX read-side boundary through
softcode relay plus caller-controlled `@log`.

The implementation audit also showed that the running TinyMUX bridge remained
transitional: it parsed player-facing transport, covered only a small event
subset, did not implement the intended perception model, and did not provide a
contract-governed write side.

The project direction has since been clarified as three independently
replaceable layers:

1. a world engine that owns state, rules, action legality and mechanical
   perception;
2. cognition and narrative services that own memory, retrieval, bounded
   generation and direction;
3. interfaces that present authorized projections and submit action intents.

NOESIS is the versioned contract and policy fabric joining these layers. It is
not an additional source of world truth.

A SpacetimeDB TypeScript module, Maincloud database and Vue diagnostic client
have been created for Black Signal. Publishing, persistence, generated client
bindings, subscriptions, contract fixtures, local validation and GitHub Actions
validation have all been demonstrated.

## Decision

SpacetimeDB is the selected authoritative world engine and current reference
implementation for Black Signal.

NOESIS repository contracts remain engine-neutral. A deployment's selected
world engine is authoritative for that deployment; no cognition component,
interface, adapter, director or operator may bypass its validated action path.

The active reference architecture is:

```text
SpacetimeDB world engine
↕ versioned NOESIS action, event and perception contracts
NOESIS cognition, memory, canon and direction
↕ authorized projections and action intents
Vue diagnostics / Unreal Engine / other interfaces
```

### World authority

SpacetimeDB owns:

- mechanically relevant entity and location state;
- legal state transitions and refusals;
- authenticated principals, control grants and capabilities;
- mechanical perception and safe state projections;
- durable accepted world events;
- mechanical schedules and timers.

All state mutation occurs through reducers. Reducers derive the authenticated
caller from the connection context and do not trust caller-supplied actor or
principal identifiers.

An accepted state transition and its durable world-event record must commit in
the same transaction.

### NOESIS authority

NOESIS owns:

- engine-neutral boundary contracts;
- telemetry normalization and adapter behavior;
- canon ingest and stable cross-layer identity;
- graph memory and retrieval;
- observer-bounded context construction;
- cognition candidates, validation and quarantine;
- narrative direction and pacing.

NOESIS may propose actions but may not write world tables directly. A
model-generated candidate is not a world fact.

### Interface authority

Interfaces may subscribe to authorized projections, render presentation assets
and submit action intents. They do not decide truth, legality or access to
secrets.

Vue remains a diagnostic client. Unreal Engine is the intended rich client and
will use C++ bindings independently of the TypeScript module language.

## Contract Consequences

The write boundary is formalized as the `noesis.world_action.v0` family:

```text
intent
→ authenticated engine validation
→ action result
→ accepted state transition
→ durable world event
→ normalized telemetry
```

The existing `noesis.telemetry.v0` contract is retained as TinyMUX-compatible
repository history. It contains TinyMUX-specific identifiers and event types
and must not be silently redefined as engine-neutral.

An engine-neutral successor, `noesis.telemetry.v1`, will use stable entity
identifiers and distinguish:

- attempted actions;
- authoritative action decisions;
- committed world facts;
- observer-relative perception records;
- technical failures.

The 32 REALMS contract in `LAYERS.md` remains semantic repository truth. Its
mechanism will be implemented in SpacetimeDB rather than tied to TinyMUX
Reality Level storage.

## Adapter Consequences

A `noesis-spacetime` adapter is required because cognition and memory services
remain outside the database module.

The adapter will:

- consume ordered durable world events;
- resume from a stored event cursor;
- map engine records to NOESIS telemetry;
- translate authorized NOESIS action envelopes into reducer calls;
- preserve idempotency and causation identifiers.

The world continues to function when cognition services are unavailable.

## TinyMUX Status

TinyMUX is no longer the selected engine for the active Black Signal path.

TinyMUX work remains valuable as:

- a supported legacy and research adapter;
- evidence for observability boundaries;
- the origin of the 32 REALMS semantic model;
- a compatibility producer for `noesis.telemetry.v0`;
- implementation-gap evidence that informs the new architecture.

ADR-0001 remains accepted for TinyMUX read-side integration. ADR-0002 limits
its scope: ADR-0001 does not select the project-wide or Black Signal engine.

## Implementation Language

The reference SpacetimeDB module uses TypeScript for the initial implementation.
A migration to Rust, C# or C++ requires measured evidence of a concrete
limitation. Client language choices remain independent.

## Consequences

- Canonical NOESIS documents must stop naming TinyMUX as universal authority.
- Existing TinyMUX contracts and fixtures remain valid within their declared
  compatibility scope.
- New cross-engine contracts use stable `entity_id` values rather than dbrefs.
- Authoritative tables are private by default; clients consume safe projections.
- Further work follows contract → fixtures → validator → CI.
- The current Black Signal demonstration schema is bootstrap evidence, not the
  production ontology.
- This ADR may be superseded only by a later evidence-backed decision.

## Non-Decisions

This ADR does not yet define:

- the complete Black Signal ontology;
- the final authentication provider;
- all world-action variants;
- the storage representation of 32 REALMS;
- `noesis.telemetry.v1` fields;
- the canon ingest schema;
- the production Unreal client architecture.

Those decisions follow as separately versioned contracts and ADRs.
