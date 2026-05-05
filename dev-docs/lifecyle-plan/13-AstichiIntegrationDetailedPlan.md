# Astichi Integration Detailed Plan

## Purpose

Define the Astichi surfaces that lifecycle generation can rely on, and name
the active golden tests that prove them.

Lifecycle code generation should prefer improving Astichi over writing bespoke
string emitters. Generated class source should be assembled from Astichi
composables, holes, parameter holes, call-argument holes, generated resources,
imports, and comments.

## Proven Astichi Surfaces

These surfaces are available for lifecycle templates:

- `class C(astichi_hole(base))` and `class C(*astichi_hole(bases))`
- expression holes inside `__slots__` tuple/list values
- `name__astichi_param_hole__` function parameter insertion
- `astichi_funcargs(...)` call-argument payloads
- `astichi_ref(path)` and chained/nested `expr.astichi_ref(path)` lowering
- assignment through `astichi_ref(...)._`
- dynamic function/property names with `name__astichi_arg__`
- `astichi_bind_external(...)` for external literal/source values
- `astichi_pass(..., outer_bind=True)` and `astichi_import(...)` for explicit
  scope boundary access
- `astichi_pyimport(...)` import declarations, consolidated by Astichi
- `astichi_comment(...)` for inspectable generated-source comments

## Golden Proofs

Active Astichi goldens that back lifecycle assumptions:

- `astichi/tests/data/gold_src/class_head.py`
  - class-head expression holes
  - splatted multi-base class heads
  - metaclass/class keyword holes

- `astichi/tests/data/gold_src/lifecycle_template_surfaces.py`
  - lifecycle-shaped class/state/facade template
  - `__slots__` entries from expression inserts
  - parameter holes with annotation/default payloads
  - call-argument holes into a state constructor
  - dynamic property getter/setter names
  - `astichi_ref(...)._` assignment
  - `astichi_pyimport(...)`
  - `astichi_comment(...)` rendered through `emit_commented()`

The corresponding pre-materialized and materialized outputs live under
`astichi/tests/data/goldens/pre_materialized/` and
`astichi/tests/data/goldens/materialized/`, and are verified by Astichi's
golden test harness.

Lifecycle success tests should not duplicate these as bespoke Astichi unit
tests. Add a new Astichi golden only when a lifecycle template needs a new
surface or a new interaction between surfaces.

## Comment Markers

Astichi templates used by lifecycle generated resources should include useful
debug comments:

```python
astichi_comment("production PropertyTemplateToClassBody: managed property")
```

Good comment sites:

- production-generated class components
- matcher-selected resources
- operation phase blocks
- generated helper/decorator sections
- transaction commit/rollback phases

Executable output from `materialize()` strips comments. Inspectable output from
`emit_commented()` renders them as real `#` comments. Comments should explain
generated structure and provenance, not restate ordinary Python syntax.

## Scope Rule

Every inserted composable is its own Astichi hygiene scope. Free identifiers do
not implicitly bind outward. Templates must use explicit boundary markers:

- `astichi_import(name)` for whole-scope imported names
- `astichi_pass(name, outer_bind=True)` for value-form same-name reads
- identifier holes and edge/local binds for generated API names
- keep names only for deliberate public or builtin names

Function parameter names are API bindings. Astichi hygiene must not rename
function parameter definitions or their uses in that function scope.

## Implementation Rule

If lifecycle generation needs Python syntax that Astichi cannot currently
represent cleanly, fix Astichi first. Do not add lifecycle-specific source
string concatenation to work around missing Astichi lowering.

The expected workflow is:

1. Add or extend an Astichi `gold_src` success fixture for the missing surface.
2. Fix Astichi until the golden passes.
3. Use the surface in YIDL generated resources.
4. Cover the YIDL behavior with YIDL generated-source goldens.
