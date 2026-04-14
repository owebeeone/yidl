# YIDL Code Generation Design

This document is the normative design for the **generator/codegen** portion of
YIDL.

It covers:

- contextual lowering of typed YIDL inputs
- AST transform of behavior snippets
- string/factory generation
- closure capture and execution model
- emitted helper/schema layer generation

See also:

- `docs/YIDLFrontendDesign.md`
- `docs/YIDLRuntimeClassModel.md`
- `docs/YIDLDesign.md` (historical reference only)

## 1. Scope

The generator turns harvested/spec inputs plus parsed YIDL AST into emitted
Python.

Its responsibilities include:

- contextual lowering of snippets
- selection of emitted class/factory structure
- deterministic code generation
- explicit handling of unsupported features

## 2. Contextual snippet lowering

YIDL behavior snippets are not emitted by raw string substitution.

Instead:

1. isolated code snippets are parsed into Python AST
2. a contextual transformer rewrites abstract store/view operations into
   physical accesses based on the active generation context
3. the lowered AST is emitted back into Python source form

Examples of transformed concepts include:

- abstract reads
- abstract writes
- abstract existence checks

The output of this stage is context-aware Python suitable for insertion into
generated classes/factories.

## 3. Helper/schema emission

YIDL emits helper/schema-layer artifacts from transducer definitions.

These include:

- FieldSpec-style helper constructors
- helper callables such as `managed(...)`, `binding(...)`, etc.

This layer defines:

- which inputs exist
- which surfaces/stores apply
- which source-level options are accepted

It should not itself encode the full runtime memory layout.

## 4. Factory emission

The generator emits a Python factory function that builds the concrete managed
class shape for a user-authored class/spec.

The factory is responsible for emitting:

- store classes
- facade/view classes
- proxy class
- generated initialization path
- commit/rollback methods

The intended target shape is exemplified by
`example/generated_factory_sample.py`, subject to PRE_IMPL review and
correction.

## 5. Closure capture and execution

The emitted factory source is executed via `exec()`.

Execution model:

- the generated factory receives a spec dict or equivalent structured input
- spec components are unpacked into locals
- nested emitted functions/classes close over those locals
- per-field callables (`freeze`, `thaw`, `default_factory`, etc.) are captured
  as native closures rather than stored in generic descriptor tables

This closure-capture model is part of the intended emitted architecture.

## 6. Determinism and explicit failure

The generator should:

- emit deterministic structure for equivalent inputs
- fail explicitly for unsupported features or slices
- avoid silently degrading into approximate behavior

Generated output should remain inspectable enough that failures can be
understood without reverse-engineering opaque string concatenation.

## 7. Codegen open issues

The generator design is still expected to clarify:

- exact IR boundaries between frontend output and final emission
- unsupported-feature signaling
- exact emitted helper/factory split for early slices
- exact migration path from hand-crafted target shapes to generated output

Those are ongoing design topics, but they belong to codegen, not to frontend
or runtime-class-model semantics.
