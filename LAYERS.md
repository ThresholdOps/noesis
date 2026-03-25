# NOESIS Realms Contract

## Scope

This document defines the intended NOESIS contract for 32 REALMS.

TinyMUX Reality Levels are the underlying mechanism.
NOESIS adds taxonomy, governance, and semantic meaning on top of that mechanism.

This document defines repository truth for governance.
It does not claim that all runtime presets, softcode helpers, or reset commands are implemented today.

## Inventory

NOESIS reserves 32 realm slots:

### WORLD

1. `WORLD.PRIME`
2. `WORLD.SHADOW`
3. `WORLD.UMBRAL`
4. `WORLD.DEAD`
5. `WORLD.DREAM`
6. `WORLD.MACHINE`
7. `WORLD.FAE`
8. `WORLD.CHALK`

### OVERLAY

9. `OVERLAY.COVER`
10. `OVERLAY.OBFUSCATED`
11. `OVERLAY.SCRY`
12. `OVERLAY.TRACE`
13. `OVERLAY.ECHO`
14. `OVERLAY.RESONANCE`
15. `OVERLAY.MARK`
16. `OVERLAY.SIMULATED`

### SENSE

17. `SENSE.SIGHT`
18. `SENSE.HEARING`
19. `SENSE.TOUCH`
20. `SENSE.PRESENCE`
21. `SENSE.AURA`
22. `SENSE.SPIRIT`
23. `SENSE.TECH`
24. `SENSE.DREAM`

### GATE

25. `GATE.UMBRA`
26. `GATE.SHROUD`
27. `GATE.MATRIX`
28. `GATE.FAE`
29. `GATE.CHALK`
30. `GATE.PEERING`

### ADMIN

31. `ADMIN.STAFF`
32. `ADMIN.RESET`

## Taxonomy Meaning

- `WORLD`: stable world-presence strata
- `OVERLAY`: temporary or contextual modifiers layered over world presence
- `SENSE`: observer-side access channels relevant to perception evaluation
- `GATE`: traversal, boundary, and cross-realm mediation slots
- `ADMIN`: operational and recovery slots reserved for staff and reset behavior

## Governance Rules

- All 32 slots are reserved project-wide even if only a subset is active in an implementation phase.
- Realm meaning is governed at the NOESIS contract layer, not ad hoc by individual bots, bridge code, or client rendering.
- TinyMUX Reality Levels remain the mechanism of enforcement; NOESIS names the semantic intent of each reserved slot.
- Runtime implementations may map these slots onto TinyMUX flags, levels, or softcode conventions, but must not silently repurpose a reserved slot to unrelated semantics.
- `ADMIN.*` slots are not gameplay affordances. They exist for staff visibility, diagnostics, recovery, or reset workflows.
- Splat-specific default Rx/Tx presets are intentionally deferred until grounded in dedicated repo truth.

## Intended Use Model

- WORLD and OVERLAY define what layer or condition an entity occupies.
- SENSE defines what kinds of access an observer may use when perception is evaluated.
- GATE defines cross-layer passage, mediation, or boundary exceptions.
- ADMIN defines privileged visibility and operational escape hatches.

This contract is semantic and governance-oriented.
It does not require that every event payload include all 32 realms.

## Saturation Rule

32/32 saturation means all reserved realm slots are already allocated meaningful semantics.

Operational consequence:

- no new realm semantics should be introduced by improvising unused labels
- any new proposal requires governance review and either slot reuse by explicit replacement or a redesign of the allocation model
- downstream schema and tooling should treat the 32-slot inventory as closed for v0 contract purposes

## Pseudo-ALL Reset Direction

NOESIS intends a pseudo-ALL reset direction in which non-admin realm occupancy can be cleared or normalized through governed reset behavior.

Direction only:

- user-facing pseudo-ALL reset semantics belong to `ADMIN.RESET`
- this document does not claim that a runtime command, softcode helper, or bridge control path already implements that reset
- until implementation exists, reset remains a contract-level direction rather than an available operation

## Relation to Existing TinyMUX REALMS

The bundled TinyMUX REALMS support remains relevant as mechanism and precedent, especially for visibility gating and staff override behavior.

NOESIS differs in that:

- it reserves a 32-slot contract
- it adds taxonomy and governance semantics
- it treats the contract as repository truth for future telemetry and perception enrichment
