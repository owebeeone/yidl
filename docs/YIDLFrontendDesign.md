# YIDL Frontend Design

This document is the normative design for the **frontend** portion of YIDL:

- author-facing helper / schema surface
- harvester behavior
- YIDL source parsing
- typed AST production
- source-level snippet handling before code generation

See also:

- `docs/YIDLCodegenDesign.md`
- `docs/YIDLRuntimeClassModel.md`
- `docs/YIDLDesign.md` (historical reference only)

## 1. Scope

The frontend is responsible for turning:

1. author-facing Python declarations and helper calls, and
2. YIDL source files / embedded YIDL source

into structured inputs for the generator.

It should not itself define the final generated class shape. That belongs to
the runtime/class-model and codegen docs.

## 2. Harvester

The harvester runs over the user-authored Python class surface.

Responsibilities:

- scan the user base class for lifecycle field declarations
- collect annotations and helper-returned FieldSpec-style objects
- extract explicit helper arguments (`default`, `freeze`, `thaw`, etc.)
- resolve class MRO for inherited field-spec composition
- bind the harvested information into the spec-like structure consumed by later
  compilation/codegen stages

Output:

- an unbound or partially bound structured field specification suitable for
  generator input

The harvester owns source-level composition and schema extraction. It does not
own the full runtime layout.

### 2.1 Harvested `tx_key`

When a helper or related source declaration includes `tx_key`, the harvester
must preserve that value in harvested/spec metadata so later codegen and the
runtime/class model can place the field or hook into the correct transaction
group.

At the frontend layer, `tx_key` is:

- harvested source/spec metadata
- not itself a runtime execution rule
- expected to survive binding into the spec-like structure consumed by codegen

## 3. YIDL source parsing

The parser reads YIDL source into a strict typed AST.

### 3.1 Lexer

The lexer is an indentation-aware scanner.

Responsibilities:

- tokenize YIDL structure
- preserve fenced raw Python code blocks
- strip YIDL comments without damaging embedded code

### 3.2 Parser

The parser is a pure Python recursive-descent parser.

Responsibilities:

- convert the token stream into a strongly typed AST
- preserve the hierarchical structure of transducers, behaviors, and code
  snippets

Expected node categories include:

- transducer nodes
- behavior nodes
- code nodes

Output:

- a strict typed AST representing YIDL source semantics prior to contextual
  lowering

## 4. Source containers

During the bootstrap phase, YIDL may also be embedded in `_yidl.py` containers
via the documented `yidl.embed(...)` path.

Frontend responsibilities for source containers include:

- recognizing whether the source came from embedded Python or standalone YIDL
- preserving enough source metadata for line remapping and diagnostics
- exposing embedded source and line-offset metadata when required by the
  bootstrap contract

The bootstrap container format is a temporary development path, not the
long-term normative source format.

## 5. Typed frontend outputs

The frontend should produce enough structured output for later stages to avoid
stringly-typed compilation logic.

At minimum, later stages should be able to inspect:

- harvested field/spec metadata
- parsed YIDL AST
- code-snippet nodes prior to transformation

## 6. Frontend open issues

The frontend design is still expected to clarify:

- explicit injectable-name rules for factories/hooks
- exact helper/spec shape produced by the harvester
- exact bootstrap source-container detection rules
- how far annotation-driven behavior belongs in frontend vs later compilation

These are design topics for ongoing PRE_IMPL and follow-on work; they do not
change the frontend boundary itself.
