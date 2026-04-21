# Package Structure Rules

## Purpose

These rules define what belongs in the `yidl` package repository and what
should live in separate packages or repositories.

## Core Principle

`yidl` should contain:

- the YIDL compiler and related tooling
- YIDL-owned runtime modules
- source-loading/bootstrap support that is part of the supported distribution
- tests, examples, validation material, and working documentation for those
  reusable pieces

`yidl` should not become the long-term home of one large application or one
project-specific integration that distorts the core package shape.

## Rules

### Keep the core package focused

The main package should primarily contain reusable framework/compiler/runtime
code:

- `src/yidl/`
- compiler
- parser/frontend
- generator
- YIDL-owned runtime
- public API helpers
- test support

Large application implementations should not be added under the top-level repo
unless they are explicitly temporary experiments.

### Examples are working documentation

The `example/` directory is for:

- concise end-to-end examples
- working documentation
- demonstration of supported patterns
- small probes that explain a technique or architecture

Examples should stay:

- readable
- contained
- instructional

They may use multiple files if the technique being demonstrated genuinely
requires multiple files, but the purpose must remain documentation and
demonstration.

### Validation artifacts stay separate from product code

`docs/validation/` is for:

- empirical probes
- generated-example validation
- representability experiments
- performance checks
- Python-version investigations

That material is intentionally not the same thing as supported product source.
Do not silently promote validation experiments into `src/` or the main parity
test surface.

### Full applications or product integrations should live elsewhere

A substantial application or project-specific integration with its own:

- architecture
- services
- persistence
- domain model
- large UI or API surface
- dedicated roadmap

should be split into a separate package or repository.

### Avoid product code in the core repo when it distorts package design

If project-specific code starts to force:

- special-case runtime hooks
- large app-specific directories
- app-specific public APIs
- product-specific source conventions

into the core repo, that is a sign it should move out.

### Runtime and frontend boundaries should stay explicit

Keep the boundaries between:

- source container/loading logic
- parser/frontend logic
- code-generation logic
- runtime support

clear enough that one layer can evolve without quietly owning the others.

## Allowed Exceptions

Exceptions are acceptable when the goal is clearly one of:

- proving a compiler or runtime technique
- capturing a bounded parity exploration
- creating working documentation for a recommended structure
- running a temporary empirical validation effort

In those cases:

- keep the scope intentionally bounded
- document why it lives here
- avoid letting it silently become permanent product code

## Review Checklist

Before adding a new top-level directory or significant subtree, check:

1. Is this reusable compiler/runtime/framework code or project/application code?
2. Is this here to demonstrate a technique, or to ship product logic?
3. Would this be cleaner as a separate package?
4. Will this distort the public API or package layout of core?
5. Does it belong in `example/` or `docs/validation/` instead?
6. If it is multi-file example code, is the multi-file structure essential to
   the teaching goal?
