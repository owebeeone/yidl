# YIDL Transactional Base Phase J Plan

## Scope

Phase J is productionization and replacement readiness.

Earlier phases add semantics. Phase J should make lifecycle suitable to replace
the old `pyrolyze.lifecycle` implementation in supported cases.

## Goals

1. Emit/import generated lifecycle classes as Python modules instead of
   decorator-time `exec`.
2. Define packaging for checked-in or build-time generated YIDL artifacts.
3. Establish parity tests against supported `pyrolyze.lifecycle` behavior.
4. Benchmark construction and common access paths against the performance
   target.
5. Document migration limits and supported API surface.

## Non-Goals

1. Do not add new semantics in this phase.
2. Do not patch `pyrolyze.lifecycle`.
3. Do not support unsupported Phase C-I features just for parity.

## Productionization Work

- generated module cache / import policy
- source map or diagnostics back to decorated class and YIDL source
- packaging hook for generated decorator artifacts
- benchmark harness for construction, property reads/writes, begin/commit, and
  rollback
- migration guide and compatibility table

## Verification

- full yidl regression suite
- lifecycle parity suite
- performance benchmarks with recorded baselines
- packaging smoke test from a built wheel/sdist

## Roll-Build

Suggested tag prefix:

```text
txphaseJ-production/
```
