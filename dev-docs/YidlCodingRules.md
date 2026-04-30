# YIDL Coding Rules

Active implementation and process rules for YIDL.

`dev-docs/YidlDesignSummary.md` is the canonical semantic/design source. This
file is the definitive coding-rules and implementation-rules companion. It
captures architectural guardrails, generator rules, and development process
expectations that should stay stable across individual feature plans.

Archived material under `dev-docs/history/` is reference-only. Do not maintain
or revive historical rules in place.

## 1. Authority And Hierarchy

1. `dev-docs/YidlDesignSummary.md` is authoritative for YIDL semantics, public
   design, and locked architectural decisions.
2. This file is authoritative for coding rules, implementation guardrails, and
   recurring process rules.
3. `AGENTS.md` is the operational shorthand for agents working in the repo. It
   should stay aligned with this file rather than becoming a second full rules
   document.
4. History under `dev-docs/history/` is archaeology only. Read it only when a
   concrete historical question requires it.

## 2. Dependency And Ownership Direction

1. YIDL is intended to become authoritative for its own runtime and compiler
   behavior.
2. Do not design YIDL modules around long-term dependence on
   `pyrolyze.lifecycle`.
3. Product code, generated code, public runtime code, and normal tests must not
   import `pyrolyze`.
4. If parity/reference behavior is needed, use YIDL-owned runtime code or
   YIDL-controlled `test-deps/` copies as described in the design summary.
5. `pyrolyze/` is read-only during this phase. If reference behavior is wrong,
   document the issue and normalize the skip/workaround on the YIDL side rather
   than patching `pyrolyze/`.

## 3. Generated Surface Rules

1. Generated YIDL classes must be emitted as plain Python classes, not
   dataclasses.
2. Do not blur generated YIDL object-model semantics with Python dataclass
   semantics.
3. Generated code should look like deliberate compiler output: explicit layout,
   explicit stores/helpers, and readable direct behavior.
4. The generator is part of the implementation path for every supported slice.
   Do not treat handwritten baselines or validation probes as permission to
   defer generator work until later.
5. Unsupported features must fail explicitly and locally. Do not silently
   degrade or widen behavior through fallback magic.

## 4. YIDL / Astichi Boundary

1. Use Astichi where structural composition is the right tool; do not collapse
   YIDL generator design into ad hoc string templating when Astichi already
   models the surface cleanly.
2. Keep the YIDL-vs-Astichi boundary explicit. YIDL owns lifecycle semantics;
   Astichi owns AST stitching/lowering mechanics.
3. Generated decorator paths and generated field-spec/helper runtime paths must
   not invoke the Python parser.
4. In particular, do not call `ast.parse(...)`, `astichi.compile(...)`, or
   Python `compile(...)` on fresh ad hoc source fragments from inside generated
   decorator execution or generated field-spec/helper functions.
5. Do not create per-field Astichi composables from source text in those
   runtime paths.
6. Repeated field contributions in generator/runtime code should come from
   precompiled templates, direct structural AST construction, or other
   parser-free specialization mechanisms.
7. If a parser boundary is still needed in the system, it must be one explicit
   compiler/build boundary outside generated decorator and generated
   field-spec/helper execution, not a per-field or incremental runtime habit.
8. Astichi is new and YIDL is its first real production use case. When clean
   YIDL generation needs an Astichi bug fix or a missing Astichi surface,
   prefer improving Astichi over encoding a YIDL-side workaround.
9. Do not hide Astichi gaps behind long-term YIDL kludges such as bespoke
   string formatting, feature-specific AST surgery, or semantic shortcuts.
   Missing Python construct surfaces such as exceptions, `match`, `elif`,
   `else`, or `for`-`else` should be added to Astichi when YIDL needs them.
10. A workaround for an Astichi limitation is allowed only as a temporary,
   documented stopgap with an explicit follow-up to remove it from the
   long-term generator path.

## 5. Generator Architecture

1. YIDL generation is composable-resource driven. Features define the tools
   needed to generate them: Astichi composables, holes/ports, construct
   surfaces, spec properties, filters/selectors, and rules.
2. The compiler connects those declared resources by evaluating rules over
   resolved specs and wiring matching contributions into surfaces. It should
   not grow bespoke per-feature emitter loops for each new capability.
3. For common Python constructs, prefer canonical Astichi class/function/
   component recipes with standardized hole names over parallel YIDL-only
   metadata.
4. Class constructs are part of the same model. Methods, class variables,
   slots, helper declarations, and future class-body constructs should expose
   named surfaces that rules can target.
5. Field/spec-specific behavior should be expressed as rule selection and
   binding into reusable composable resources, not as feature-specific source
   formatting or one-off AST assembly scattered through emitters.
6. A small amount of hand-coded assembly is acceptable only as a transitional
   discovery surface. Once a construct is understood, promote it into the
   declarative construct/resource/rule model.
7. The desired direction for surfaces such as slots is construct based. A
   human-facing fluent spelling such as
   `builder.classvar.add.Main.named("__slots__").items` may explain the shape,
   but the generator/mapper path must use Astichi's data-driven builder API
   rather than synthesizing attribute chains. A rule over selected `field_spec`
   instances then contributes one slot item into the named `items` surface.

## 6. Support-Code Style

1. In compiler-only, parser/frontend, IR, spec, and other non-generated support
   paths, strongly prefer `@dataclass` for classes that primarily hold state.
2. Prefer `frozen=True` for those dataclasses when mutation is not required by
   the design.
3. In tests, prefer dataclasses for named structured test state over unnamed
   tuples or ad hoc lists.
4. Prefer `abc.ABC` plus `@abstractmethod` for explicit shared contracts when
   nominal inheritance is practical. Use `typing.Protocol` when an ABC is
   awkward or impossible.
5. Do not introduce enums without explicit project-owner approval. Do not
   replace them with magic strings, magic integers, or passive sentinel tags
   when the concept has semantics that should live on an object.
6. Keep type annotations complete and precise.
7. Organize modules by cohesive responsibility and stable change boundary.
8. Keep generic/shared modules limited to neutral abstractions, stable data
   carriers, and utilities that are genuinely shared across subsystems.
9. If implementation reveals that a planned boundary is wrong, update the plan
   and adopt the cleaner boundary rather than widening the mistake.

## 7. Validation And Repository Hygiene

1. Validation-only experiments, probes, generated examples, and performance
   checks belong under `docs/validation/` until deliberately promoted.
2. Do not treat scratch paths or validation artifacts as stable dependency
   locations for committed product code unless the docs explicitly promote them.
3. Do not store absolute filesystem paths in committed files; use paths
   relative to the `yidl` repository root.

## 8. Development Process

1. Use strict red/green/refactor for behavior changes.
   1. Red: add or update the test first and confirm it fails.
   2. Green: implement the minimal change required to pass.
   3. Refactor: clean up structure without changing behavior.
   4. Verify targeted scope.
   5. Verify the broader regression scope before finalizing.
2. Do not quietly change public semantics, runtime semantics, code-generation
   semantics, or source-container semantics merely to satisfy a convenient test.
3. If a failure indicates a real semantic change rather than a bug fix, stop
   and ratify the change before implementing it.
4. The reference backend is not an oracle. A parity mismatch can indicate an
   implementation bug, a design gap, or a design conflict.
5. Use these classifications consistently when design friction appears:
   - `implementation_bug`
   - `design_gap`
   - `design_conflict`
6. Prefer clarifying or simplifying the model over adding generic flags,
   escape hatches, or cross-cutting special cases to force one slice through.

## 9. Test Guidance

1. Prefer explicit assertions over golden strings unless the output shape
   itself is the behavior under test.
2. When a canonical fixture, golden, snapshot, or integration-style harness
   already exists for successful end-to-end behavior, prefer that harness over
   bespoke unit tests.
3. Prefer `gold_src` / generated-output coverage for successful codegen and
   other success-path end-to-end behavior when that harness already exists.
4. Keep bespoke unit tests focused on narrow mechanics, recognition/parsing
   checks, diagnostics, and failure-mode behavior that the canonical harness
   does not express cleanly.
5. Avoid duplicating the same success-path assertions in both bespoke tests and
   canonical output tests.
6. Keep codegen-output verification honest: when generated source shape matters,
   test the generated source shape directly.
7. Test names and test file names should describe stable behavior/surfaces, not
   phase ids, plan step ids, or dates.
