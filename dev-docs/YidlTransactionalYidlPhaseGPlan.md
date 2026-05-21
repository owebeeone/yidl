# YIDL Transactional Base Phase G Plan

## Scope

Phase G defines and implements `transient` fields.

This phase is design-sensitive because existing design notes describe
transient as transaction-scoped working state, while the old umbrella Phase C
draft treated it as plain state with a semantic marker. Resolve that before
implementation.

## Goals

1. Lock transient storage semantics.
2. Add marker, harvester facts, YIDL facts, generated slots, and properties.
3. Define interaction with default factories.
4. Define visibility across default/current/working facades.

## Non-Goals

1. Do not add owned or binding fields.
2. Do not add commit validators or hooks unless Phase F has already landed and
   transient needs to interact with them.
3. Do not use transient as a generic scratch namespace.

## Semantics To Decide

Questions:

- Is transient state transaction-local, state-local, or facade-local?
- Does rollback clear transient values?
- Does commit clear transient values?
- Does transient require an active transaction to write?
- Can transient values be default_factory providers?
- Is current facade allowed to read transient values?

The implementation should not start until these are answered.

## Verification

Goldens should show successful generated source and runtime behavior for the
chosen policy. Focused tests should cover invalid combinations.

## Roll-Build

Suggested tag prefix:

```text
txphaseG-transient/
```
