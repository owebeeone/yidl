# YIDL Import And Concept Merge Detailed Plan

## Purpose

This document expands `YidlImportAndConceptMergePlan.md` into an
implementation-level plan.

The target is not just "a schema file plus a generation file". The target is
layered concept construction:

- a base concept owns the common dataclass model and the stable production graph
- feature concepts add field variants, resources, contributions, and matcher
  rules
- a combined concept extends multiple feature concepts at once
- diamond inheritance through the shared base deduplicates inherited members
- matcher merge is the behavior override mechanism

The proof fixture is a split dataclasses-like compiler whose combined generated
decorator and generated class output match the current single-file defaults
fixture, then additionally prove `InitVar` and `ClassVar` behavior.

## Current Compiler Touch Points

The implementation work is concentrated in the Lark compiler and its generated
assembly/runtime surfaces:

- `src/yidl/concept_grammar.lark`
- `src/yidl/concept_parser.py`
- `src/yidl/generation/assembly_plan.py`
- `src/yidl/generation/assembly_runtime.py`
- `src/yidl/generation/assembly_source.py`
- `tests/generation/test_yidl_lark_parser.py`
- `tests/data/yidl/*.yidl`
- `tests/data/gold_src/*.py`
- `tests/data/goldens/materialized/*`

The existing grammar already parses alias imports, from imports, exports,
concept inheritance, matchers, contributions, composable productions, assembly
edges, and assemblies.

The important current gap is that `_ConceptCompiler.compile(...)` returns
`YidlCompiledConcept` with mostly local maps:

```python
return YidlCompiledConcept(
    name=name,
    plan=plan,
    properties=dict(self._local_properties),
    families=dict(self._local_families),
    records=dict(self._local_records),
    collections=dict(self._local_collections),
    resources=dict(self._local_resources),
    matchers=dict(self._local_matchers),
    productions=dict(self._local_productions),
    operations=dict(self._local_operations),
    contributions=dict(self._local_contributions),
    contribution_matchers=dict(self._local_contribution_matchers),
    composable_productions=dict(self._local_composable_productions),
    assembly_edges=dict(self._local_assembly_edges),
    assemblies=dict(self._local_assemblies),
)
```

That is insufficient for layered concepts. A child concept must expose a merged
surface to both compile-time resolvers and generated runtime source.

## Required Semantics

### Import Resolution

Alias imports keep their current behavior:

```yidl
import "dataclasses_base.yidl" as base
```

The compiler resolves `base.DataclassesBase` by looking in the imported module.
Export declarations are metadata only in this slice; they do not restrict
access.

From imports must be lowered:

```yidl
from "dataclasses_base.yidl" import concept DataclassesBase
from "dataclasses_base.yidl" import resource EmptyStatement
```

The imported local alias participates in unqualified name resolution after local
and inherited names:

1. local concept names
2. inherited concept names
3. explicit from-import aliases

Alias imports remain qualified only.

From-import aliases are file-local. They do not leak through `extends`, and a
child concept cannot use aliases declared in a parent concept's source file.

`use` declarations remain out of scope for this slice. They should continue to
produce a clear "not implemented" diagnostic.

Inherited assemblies are callable by name from a child concept's generated
runtime without re-declaring or re-exporting the assembly in the child.

### Concept Map Merge

`extends` means the child inherits the usable compiled surface of each parent.
For a child concept, merge these maps into `YidlCompiledConcept`:

- `properties`
- `families`
- `records`
- `collections`
- `resources`
- `matchers`
- `productions`
- `operations`
- `contributions`
- `contribution_matchers`
- `composable_productions`
- `assembly_edges`
- `assemblies`

The DDS `CapsuleConceptPlan` remains the structural authority for schema
inheritance and validation. The child `YidlCompiledConcept` still exposes
`properties`, `families`, `records`, and `collections` as the union of local and
extension-closure entries so YIDL resolvers, assembly validation, and generated
runtime source all see the same surface. Identity dedupe applies to schema maps
the same way it applies to non-schema maps.

### Non-Mergeable Names

These names are not override points:

- resources
- data productions
- operations
- contributions
- composable productions
- assembly edges
- assemblies

If a child defines the same name locally, reject it unless the duplicate is the
same inherited object reached through a diamond.

Example rejection:

```text
dataclasses_child.yidl: resource 'ClassShell' is already inherited from
DataclassesBase
```

### Matcher Merge

Matchers are the intended extension points.

Resource matchers with the same name merge their inputs, defaults, and rules.
Contribution matchers with the same name merge their inputs, defaults, and
rules.

Rules:

- a child may add rules to an inherited matcher
- a feature layer may add rules to an inherited matcher
- two parents may contribute different rules to the same inherited matcher
- duplicate rule names reject unless they are the exact same inherited rule from
  a common ancestor
- two distinct defaults for the same merged matcher reject; the exact same
  default inherited through a diamond is deduped
- inherited inputs must be structurally compatible by input name and collection
- a child may not change the source collection of an inherited input name
- a child matcher declaration may declare a subset, the same set, or additional
  inputs; the merged matcher input list is the union in parents-first order
- duplicate input names are compatible only when they reference the same
  collection name

This is the override model. If a feature wants to change behavior, it adds a
more specific or higher-weight matcher rule that selects a different resource or
contribution. It does not replace the resource, contribution, or production
definition.

## Implementation Steps

### Step 1: Add Imported Symbol Structures

Add a small internal structure in `concept_parser.py`:

```python
@dataclass(frozen=True, slots=True)
class _ImportedSymbol:
    alias: str
    kind: str
    name: str
    module_path: str
    module: YidlCompiledModule
    target: object
```

Change `_YidlCompiler._compile_imports(...)` to return an object containing:

- alias imports: `dict[str, YidlCompiledModule]`
- from imports: `dict[str, _ImportedSymbol]`

Suggested shape:

```python
@dataclass(frozen=True, slots=True)
class _CompiledImports:
    aliases: Mapping[str, YidlCompiledModule]
    symbols: Mapping[str, _ImportedSymbol]
```

Validation:

- imported path must exist in the source map
- absolute import paths stay rejected by `_resolve_import_path(...)`
- alias names cannot collide with other aliases
- from-import aliases cannot collide with alias-import names
- from-import aliases cannot collide with other from-import aliases
- from-import aliases cannot collide with local declarations in the same file
- missing imported symbol reports path, kind, and name
- wrong-kind imported symbol reports the found kind
- ambiguous unqualified member in an imported module rejects

### Step 2: Implement From-Import Lookup By Kind

Add a helper that searches imported modules by symbol kind:

```python
def _find_imported_symbol(
    module: YidlCompiledModule,
    *,
    kind: str,
    name: str,
) -> object:
    ...
```

Kind mapping:

| Import kind | Search location or V0 policy |
| --- | --- |
| `concept` | `module.concepts` |
| `property` | each concept's `properties` |
| `record` | each concept's `records` |
| `union` | reject with "from-import of union is not implemented" |
| `collection` | each concept's `collections` |
| `port` | reject with "from-import of port is not implemented" |
| `resource` | each concept's `resources` |
| `matcher` | each concept's `matchers` and `contribution_matchers` |
| `production` | each concept's `productions` and `composable_productions` |
| `contribution` | each concept's `contributions` |
| `assembly` | each concept's `assemblies` |
| `operation` | each concept's `operations` |

If a module has more than one concept containing a same-kind member with the
same name, reject an unqualified from import as ambiguous. A future syntax can
add concept-qualified imports if needed; this slice does not need it.

The `production` keyword covers both data productions and Update A composable
productions because that is the current grammar. `_ImportedSymbol.target` carries
the actual object, and downstream resolvers must branch by target type. If both
a data production and a composable production with the requested name are
visible, the from-import is ambiguous and rejects.

### Step 3: Thread Imports Into Concept Resolution

Update `_ConceptCompiler.__init__(...)` to receive `_CompiledImports`.

Resolvers that need from-import support:

- `_resolve_concept`
- `_resolve_resource`
- `_resolve_matcher`
- `_resolve_collection`
- `_resolve_record_shape`
- `_resolve_contribution_name`
- `_composable_production_exists`
- `_resolve_contribution_matcher_name`
- `_compile_assembly`
- `_compile_composable_production`

Use the same resolution order consistently:

1. local declarations/maps
2. inherited extension-visible maps
3. explicit from-import aliases
4. alias-qualified imports such as `base.Name`

Do not add broad implicit search over all alias imports.

During member compilation, resolvers may keep the current extension-walking
style because local merged maps are not complete until all local members are
compiled. After local compilation, materialize the merged maps once, store them
on the returned `YidlCompiledConcept`, and use those merged maps for assembly
validation and runtime source emission.

### Step 4: Build Inheritance Closure

Add a deterministic closure helper:

```python
def _concept_extension_closure(
    concepts: Iterable[YidlCompiledConcept],
) -> tuple[YidlCompiledConcept, ...]:
    ...
```

The closure must:

- walk parents before children
- preserve declared `extends` order
- dedupe by concept identity, not just by concept name
- handle diamonds without duplicating the shared base

Identity dedupe relies on `_YidlCompiler` path-normalizing imports and reusing
cached `YidlCompiledModule` / `YidlCompiledConcept` instances. If two different
source keys represent the same logical concept but compile to different concept
objects, treat them as distinct definitions and let normal collision detection
reject conflicts. Do not add structural equality dedupe in this slice.

Import cycles are already caught by `_YidlCompiler._active`, and ordinary
concept cycles are not expressible through current prior-concept resolution. The
closure helper does not need speculative cycle detection beyond defensive
visited-set handling.

Example:

```yidl
concept InitVarDataclasses extends base.DataclassesBase { ... }
concept ClassVarDataclasses extends base.DataclassesBase { ... }
concept Combined extends initvar.InitVarDataclasses, classvar.ClassVarDataclasses { ... }
```

The combined closure order should be:

```text
DataclassesBase
InitVarDataclasses
ClassVarDataclasses
Combined
```

### Step 5: Merge Non-Matcher Maps

Add a generic helper:

```python
def _merge_named_maps(
    *,
    kind: str,
    inherited: Iterable[Mapping[str, object]],
    local: Mapping[str, object],
    concept_name: str,
) -> dict[str, object]:
    ...
```

Behavior:

- insert inherited entries in closure order
- if the same inherited name maps to the exact same object, keep one copy
- if the same inherited name maps to different objects, reject
- if a local name already exists inherited, reject
- otherwise add local entries

Use it for:

- properties
- families
- records
- collections
- resources
- productions
- operations
- contributions
- composable productions
- assembly edges
- assemblies

For schema maps, this helper only builds the `YidlCompiledConcept` lookup maps.
It must not replace DDS structural validation. `CapsuleConceptPlan` continues to
own property, family, record, and collection validity.

Operation merge is map-only. The child compiler does not emit new
`builder.operations.<name>(...)` calls for inherited operations; it only exposes
inherited `OperationHandle` objects through the merged `operations` map.

### Step 6: Merge Contribution Matchers

Add a contribution matcher merge helper:

```python
def _merge_contribution_matchers(
    *,
    inherited: Iterable[Mapping[str, ContributionMatcherSpec]],
    local: Mapping[str, ContributionMatcherSpec],
) -> dict[str, ContributionMatcherSpec]:
    ...
```

For same-name matchers:

- inputs with the same name must reference the same collection name
- a child declaration may omit inherited inputs, repeat inherited inputs, or add
  new inputs
- add missing inputs in parents-first, first-seen order
- at most one distinct default contribution name may exist; a common inherited
  default reached twice through a diamond is one default
- rules concatenate in first-seen order
- duplicate rule names reject unless the duplicate rule object is identical

The merged matcher should be a new `ContributionMatcherSpec` with:

```python
ContributionMatcherSpec(
    name=name,
    inputs=merged_inputs,
    default_contribution_name=merged_default,
    rules=merged_rules,
)
```

For contribution matchers, this is straightforward because the specs are plain
dataclasses.

### Step 7: Merge Resource Matchers

Resource matchers are stored as `MatcherHandle` objects in the compiled concept,
but the real rules live inside `CapsuleConceptPlan`.

Use the existing capsule builder extension mechanism rather than copying a built
DDS matcher spec by hand:

- resolving an inherited matcher for local extension should call
  `builder.use_matcher(handle)`
- local matcher declarations with an inherited name should not call
  `builder.matchers.<name>()`
- when compiling a matcher declaration with an inherited name, reuse the
  inherited handle and add rules to it
- if a child does not locally declare the inherited matcher, do not call
  `builder.use_matcher(...)` just to surface it
- inherited rules from parents and siblings are not re-added by the child; they
  live in the DDS plan through the normal `extends` closure

Implementation sketch:

```python
def _compile_matcher(self, builder: Any, tree: Tree) -> MatcherHandle:
    name = _token_text(tree.children[0])
    inherited = self._resolve_inherited_resource_matcher(name)
    if inherited is None:
        editor = getattr(builder.matchers, name)()
        handle = editor.handle
    else:
        editor = builder.use_matcher(inherited)
        handle = inherited
    ...
    return handle
```

Validation:

- if a local contribution matcher has the same name, reject wrong kind
- duplicate defaults reject
- a `default -> ...` clause on an inherited resource matcher rejects when the
  inherited matcher already has a default; this is checked by the YIDL compiler
  before calling `MatcherEditor.default(...)`
- duplicate rule names reject
- inherited input names must match collection names
- new local inputs may be added only if all new rules using them are valid

The DDS builder already validates matcher collision if the compiler tries to
create a new matcher with an inherited name. The compiler should produce the
clear YIDL diagnostic before that point.

For inherited resource matcher defaults, the YIDL compiler should inspect the
extension closure's recorded matcher-default operations or another equivalent
compiled-plan view. Do not rely on `MatcherEditor.default(...)` to catch this,
because the current editor path does not enforce one default across an extension
closure.

In the diamond case, `Combined extends Left, Right` does not replay matcher
rules from either parent. `Left` and `Right` each extended the base matcher in
their own `CapsuleConceptPlan`; `Combined` inherits those plans through
`extends`. The merged `YidlCompiledConcept.matchers` map should expose the
single inherited matcher handle for lookup, while DDS build-time extension
closure supplies the accumulated inherited rules.

### Step 8: Use Merged Maps For Assembly Validation

Change validation to operate on merged maps:

- `_validate_assembly_value_contexts(...)`
- `_validate_static_assembly_scopes(...)`
- `_validate_contribution_targets(...)`
- `_validate_composable_production_cycles(...)`

Specific changes:

- an inherited production can apply an inherited or local merged assembly edge
- a local production can apply an inherited assembly edge
- an inherited assembly can reference an inherited production root
- a local contribution can target an inherited composable production path
- a merged contribution matcher can select both inherited and local
  contributions

Do not re-validate every inherited production in every child. Parent concepts
were already validated when compiled. Validate local productions, local assembly
edges, local assemblies, and any local use of inherited edges or productions
against the merged maps. For diagnostics, name both the local member being
validated and the inherited member it references.

Production cycle detection should cover local additions plus their reachable
merged references. It should not repeatedly traverse and re-diagnose a wholly
inherited cycle-free parent graph. If a new local contribution or production
creates a cycle through inherited members, report the first repeated production
name in that local reachable cycle.

### Step 9: Emit Runtime From Merged Concept

Generated decorator source must include inherited members in:

- `ASSEMBLY_RESOURCES`
- `ASSEMBLY_CONTRIBUTIONS`
- `ASSEMBLY_MATCHERS`
- `ASSEMBLY_PRODUCTIONS`
- `ASSEMBLY_EDGES`
- `ASSEMBLY_ASSEMBLIES`

Do not change the emitter API for this slice. Today callers use:

```python
emit_concept_runtime_source(
    concept.plan.build_data_definition(),
    resources=concept.resources,
    assembly_plan=concept,
)
```

The merge happens upstream on `YidlCompiledConcept`. Once that object exposes
merged maps, the existing emitter can serialize inherited and local members
without knowing where each member came from.

Add or keep one focused regression before the large split golden: compile a
child concept that inherits all runtime assembly members from a parent and
assert the emitted source can execute the inherited `build_<AssemblyName>`
function. This catches runtime-map merge failures without waiting for the large
dataclasses fixture.

## Diagnostic Terms

Tests should pin stable diagnostic terms without overfitting full prose:

- missing symbol: `missing`, kind, symbol name, and source path
- ambiguous symbol: `ambiguous`, kind, symbol name, and source path
- wrong kind: `wrong kind` or the found kind plus the expected kind
- duplicate import alias: `already`, `import`, and alias name
- duplicate inherited symbol: kind, symbol name, and both contributing concepts
- unsupported accepted grammar: `not implemented` plus the accepted symbol kind

## Detailed Tests

### Parser And Import Unit Tests

Add focused parser/compiler tests to `tests/generation/test_yidl_lark_parser.py`.

1. From-import concept:

```yidl
from "core.yidl" import concept Core

concept Child extends Core {
    property ChildName: str
}
```

Expected:

- `compile_yidl_files(...)` succeeds
- `Child.plan.build_data_definition()` contains inherited and local properties

2. From-import resource alias:

```yidl
from "core.yidl" import resource Bind as BaseBind

concept Child {
    resource Getter = template `pass` {
        edge bind = BaseBind
    }
}
```

Expected:

- `Getter.edge_bind` is the imported resource object

3. From-import missing symbol:

```yidl
from "core.yidl" import resource Missing
```

Expected diagnostic terms:

- `core.yidl`
- `resource`
- `Missing`

4. Duplicate from-import alias:

```yidl
from "a.yidl" import resource Root
from "b.yidl" import resource Other as Root
```

Expected diagnostic terms:

- `Root`
- `import`
- `already`

5. Local shadow of from-import alias:

```yidl
from "core.yidl" import resource Root

concept Child {
    resource Root = code `pass`
}
```

Expected diagnostic terms:

- `Root`
- `already`
- `import`

6. From-import alias collides with alias import:

```yidl
import "a.yidl" as core
from "b.yidl" import resource Root as core
```

Expected diagnostic terms:

- `core`
- `import`
- `already`

7. Unsupported from-import kind:

```yidl
from "core.yidl" import port FieldPort
from "core.yidl" import union FieldUnion
```

Expected diagnostic terms:

- `from-import`
- `port` or `union`
- `not implemented`

### Inheritance Merge Tests

Add focused compiler/runtime tests.

1. Child can run inherited assembly:

```yidl
module parent

concept Parent {
    property Name: str
    record Item { Name }
    collection Items: Item identity Name many

    resource RootTemplate = code `astichi_hole(body)`
    resource ItemTemplate = template `{astichi_bind_external(name): "ok"}`

    contribution ItemContribution = ItemTemplate {
        as ItemNode
        index Name
        order Name
        target body { build /Root }
        external name = Name
    }

    matcher ItemContributions(item: Items) -> contribution {
        default -> ItemContribution
    }

    production ModuleProduction -> composable {
        root Root = RootTemplate
        apply items from item: Items using ItemContributions
    }

    assembly Module = ModuleProduction
}
```

```yidl
module child
import "parent.yidl" as parent

concept Child extends parent.Parent {
    property Extra: str = "x"
}
```

Expected:

- `Child.assemblies["Module"]` exists
- generated runtime exposes `build_Module`
- running `build_Module` emits the inherited output

2. Child can add contribution matcher rule:

Parent:

```yidl
matcher FieldInfoContributions(field: Fields, facade: Facades) -> contribution {
    rule plain when FieldKind == "field" -> FieldInfoContribution
}
```

Child:

```yidl
matcher FieldInfoContributions(field: Fields, facade: Facades) -> contribution {
    rule special when FieldKind == "special" -> SpecialFieldInfoContribution weight 10
}
```

Expected:

- merged matcher has both `plain` and `special`
- a `special` field selects `SpecialFieldInfoContribution`

3. Diamond dedupe:

```yidl
concept Base { ... }
concept Left extends Base { ... }
concept Right extends Base { ... }
concept Combined extends Left, Right { ... }
```

Expected:

- inherited `Base` resources appear once
- inherited `Base` productions appear once
- inherited `Base` matcher rules appear once
- no duplicate inherited symbol failure

4. True inherited collision:

```yidl
concept Left { resource Root = code `1` }
concept Right { resource Root = code `2` }
concept Combined extends Left, Right {}
```

Expected diagnostic terms:

- `resource`
- `Root`
- `Left`
- `Right`

5. Duplicate matcher default:

```yidl
concept Left {
    matcher Select(field: Fields) -> contribution {
        default -> LeftContribution
    }
}

concept Right {
    matcher Select(field: Fields) -> contribution {
        default -> RightContribution
    }
}
```

Expected diagnostic terms:

- `matcher`
- `Select`
- `default`

6. Resource matcher rule merge through diamond:

```yidl
concept Base {
    matcher ResourceFor(field: Fields) {
        default -> PlainResource
    }
}
concept Left extends Base {
    matcher ResourceFor(field: Fields) {
        rule left when FieldKind == "left" -> LeftResource weight 10
    }
}
concept Right extends Base {
    matcher ResourceFor(field: Fields) {
        rule right when FieldKind == "right" -> RightResource weight 10
    }
}
concept Combined extends Left, Right {}
```

Expected:

- `Combined.matchers["ResourceFor"]` resolves
- the built DDS matcher has the base default plus both sibling rules
- neither sibling rule is duplicated
- no child re-add of inherited rules is required

## Split Dataclasses Fixture

The final success test should use golden files, not a pile of bespoke output
assertions.

Create one YIDL fixture directory and two product goldens:

```text
tests/data/yidl/yidl_update_a_dataclasses_split/
    dataclasses_base.yidl
    dataclasses_initvar_base.yidl
    dataclasses_classvar_base.yidl
    dataclasses_combined.yidl

tests/data/gold_src/yidl_update_a_dataclasses_base.py
tests/data/gold_src/yidl_update_a_dataclasses_split.py

tests/data/goldens/materialized/yidl_update_a_dataclasses_base/decorator.py
tests/data/goldens/materialized/yidl_update_a_dataclasses_base/decorator_prettier.py
tests/data/goldens/materialized/yidl_update_a_dataclasses_base/generated_output.py
tests/data/goldens/materialized/yidl_update_a_dataclasses_base/generated_output_prettier.py

tests/data/goldens/materialized/yidl_update_a_dataclasses_split/decorator.py
tests/data/goldens/materialized/yidl_update_a_dataclasses_split/decorator_prettier.py
tests/data/goldens/materialized/yidl_update_a_dataclasses_split/generated_output.py
tests/data/goldens/materialized/yidl_update_a_dataclasses_split/generated_output_prettier.py
```

Do not place `.yidl` files in `tests/data/goldens/materialized/...`. The
current golden harness treats materialized files as Python source and parses
them with `ast.parse(...)`. Multi-file YIDL inputs should live under
`tests/data/yidl/...`; generated Python outputs remain under
`tests/data/goldens/materialized/...`.

The two product cases are:

- `yidl_update_a_dataclasses_base.py`: compiles `dataclasses_base.yidl` and
  golden-checks the plain stored-field decorator/output.
- `yidl_update_a_dataclasses_split.py`: compiles `dataclasses_combined.yidl`
  with all four YIDL source files loaded and golden-checks the full layered
  decorator/output.

`dataclasses_initvar_base.yidl` and `dataclasses_classvar_base.yidl` should
compile individually in focused parser/compiler tests, but they do not need
their own generated-output goldens unless they become standalone product
surfaces.

### `dataclasses_base.yidl`

This file is the stable production graph and the plain stored field behavior.
It should contain most of the current monolithic file, but with `InitVar` and
`ClassVar` rules removed.

Expected shape. This is illustrative and intentionally elides repeated resource
and contribution definitions that are copied unchanged from the monolithic
fixture:

```yidl
module tests.dataclasses_base

export concept DataclassesBase

concept DataclassesBase {
    property ClassId: str
    property ClassName: str
    property ClassOrder: int = 0
    property ModuleName: str = "__main__"
    property Bases: object = ()
    property DecoratorInit: bool = True
    property DecoratorRepr: bool = True
    property DecoratorEq: bool = True
    property DecoratorOrder: bool = False
    property DecoratorUnsafeHash: bool = False
    property DecoratorFrozen: bool = False
    property DecoratorSlots: bool = False
    property DecoratorWeakrefSlot: bool = False
    property DecoratorMatchArgs: bool = True
    property DecoratorKwOnly: bool = False
    property HasPostInit: bool = False
    property HasKwOnlyInitFields: bool = False
    property KwOnlyFenceOrder: int = 0
    property DataclassParams: object = None
    property SlotNames: object = ()
    property MatchArgs: object = ()

    property FieldId: str
    property FieldOwner: str
    property FieldName: str
    property FieldOrder: int
    property FieldKind: str = "field"
    property Annotation: object = object
    property HasDefault: bool = False
    property DefaultValue: object = None
    property HasDefaultFactory: bool = False
    property DefaultFactory: object = None
    property Init: bool = True
    property Repr: bool = True
    property Compare: bool = True
    property Hash: object = None
    property KwOnly: bool = False
    property Metadata: object = None

    record DataclassFacade {
        ClassId
        ClassName
        ClassOrder
        ModuleName
        Bases
        DecoratorInit
        DecoratorRepr
        DecoratorEq
        DecoratorOrder
        DecoratorUnsafeHash
        DecoratorFrozen
        DecoratorSlots
        DecoratorWeakrefSlot
        DecoratorMatchArgs
        DecoratorKwOnly
        HasPostInit
        HasKwOnlyInitFields
        KwOnlyFenceOrder
        DataclassParams
        SlotNames
        MatchArgs
    }

    family DataclassFieldSpec {
        common FieldId, FieldOwner, FieldName, FieldOrder, FieldKind, Annotation
        common HasDefault, DefaultValue, HasDefaultFactory, DefaultFactory
        common Init, Repr, Compare, Hash, KwOnly, Metadata

        variant InstanceField {}
    }

    collection Facades: DataclassFacade identity ClassId many
    collection Fields: DataclassFieldSpec identity FieldId many

    resource ModuleRoot = code $[
        from __future__ import annotations

        _MISSING = object()
        _HAS_DEFAULT_FACTORY = object()


        class FrozenInstanceError(AttributeError):
            pass


        def _field_info(**kw):
            return kw


        def build_generated_dataclasses(*, defaults=None, default_factories=None):
            _yidl_defaults = {} if defaults is None else defaults
            _yidl_default_factories = (
                {} if default_factories is None else default_factories
            )

            astichi_hole(module_body)

            return {**astichi_hole(class_exports)}
    ]$ {
        keep _yidl_defaults, _yidl_default_factories
    }

    resource ClassShell = template $[
        class class_name__astichi_arg__:
            __module__ = astichi_bind_external(module_name)
            __dataclass_params__ = astichi_bind_external(dataclass_params)
            __dataclass_fields__ = {**astichi_hole(field_info_entries)}
            __annotations__ = {**astichi_hole(annotation_entries)}

            astichi_hole(slots_decl)
            astichi_hole(field_defaults)
            astichi_hole(match_args_decl)
            astichi_hole(init_method)
            astichi_hole(repr_method)
            astichi_hole(eq_method)
            astichi_hole(order_methods)
            astichi_hole(hash_method)
            astichi_hole(frozen_methods)
    ]$

    resource EmptyStatement = template `pass`

    contribution ClassDefinition = ClassProduction {
        as ClassDef
        index ClassOrder
        order ClassOrder
        target module_body { build /Root }
    }

    matcher ClassDefinitionContribution(facade: Facades) -> contribution {
        default -> ClassDefinition
    }

    # Metadata resources/contributions from the monolithic fixture:
    # SlotsDecl, MatchArgsDecl, AnnotationEntry, FieldInfoEntry,
    # FieldInfoDefaultEntry, FieldInfoDefaultFactoryEntry,
    # DefaultValueAssignment, DefaultAndFactoryDiagnosticMessage.

    matcher AnnotationContributions(field: Fields, facade: Facades) -> contribution {
        rule plain when FieldOwner == ClassId
                  and FieldKind == "field"
                  -> AnnotationContribution
    }

    matcher FieldInfoContributions(field: Fields, facade: Facades) -> contribution {
        rule plain when FieldOwner == ClassId
                  and FieldKind == "field"
                  and HasDefault == False
                  and HasDefaultFactory == False
                  -> FieldInfoContribution

        rule default_value when FieldOwner == ClassId
                           and FieldKind == "field"
                           and HasDefault == True
                           and HasDefaultFactory == False
                           -> FieldInfoDefaultContribution

        rule default_factory when FieldOwner == ClassId
                             and FieldKind == "field"
                             and HasDefault == False
                             and HasDefaultFactory == True
                             -> FieldInfoDefaultFactoryContribution
    }

    matcher FieldDiagnostics(field: Fields, facade: Facades) -> contribution {
        rule default_and_factory when FieldOwner == ClassId
                                  and HasDefault == True
                                  and HasDefaultFactory == True
                                  -> DefaultAndFactoryDiagnostic
    }

    # Init resources/contributions from the monolithic fixture:
    # InitMethodTemplate, RequiredParam, KwOnlyFence, DefaultParam,
    # DefaultFactoryParam, PlainInitAssign, FrozenInitAssign,
    # DefaultFactoryGuard, PostInitCall, PostInitArg.

    matcher InitParamContribution(field: Fields, facade: Facades) -> contribution {
        rule required when DecoratorInit == True
                      and FieldOwner == ClassId
                      and FieldKind == "field"
                      and Init == True
                      and HasDefault == False
                      and HasDefaultFactory == False
                      -> RequiredParamContribution

        rule default_value when DecoratorInit == True
                           and FieldOwner == ClassId
                           and FieldKind == "field"
                           and Init == True
                           and HasDefault == True
                           -> DefaultParamContribution

        rule default_factory when DecoratorInit == True
                             and FieldOwner == ClassId
                             and FieldKind == "field"
                             and Init == True
                             and HasDefaultFactory == True
                             -> DefaultFactoryParamContribution
    }

    matcher InitAssignContribution(field: Fields, facade: Facades) -> contribution {
        rule plain when DecoratorFrozen == False
                   and FieldOwner == ClassId
                   and FieldKind == "field"
                   and Init == True
                   -> PlainInitAssignContribution

        rule frozen when DecoratorFrozen == True
                    and FieldOwner == ClassId
                    and FieldKind == "field"
                    and Init == True
                    -> FrozenInitAssignContribution
    }

    matcher PostInitArgContributions(field: Fields, facade: Facades) -> contribution {
    }

    # Repr, eq, order, hash, and frozen matchers only select FieldKind == "field".

    production ModuleProduction -> composable {
        root Root = ModuleRoot

        apply diagnostics
            from facade: Facades, field: Fields
            where FieldOwner == ClassId
            using FieldDiagnostics

        apply classes
            from facade: Facades
            using ClassDefinitionContribution

        apply exports
            from facade: Facades
            using ClassExportContribution
    }

    production ClassProduction(facade: Facades) -> composable {
        root ClassDef = ClassShell {
            ident class_name = ClassName
            external module_name = ModuleName
            external dataclass_params = DataclassParams
        }

        apply slots using SlotsContribution
        apply match_args using MatchArgsContributions

        apply annotations
            from field: Fields
            where FieldOwner == ClassId
            using AnnotationContributions

        apply field_info
            from field: Fields
            where FieldOwner == ClassId
            using FieldInfoContributions

        apply field_defaults
            from field: Fields
            where FieldOwner == ClassId
            using DefaultValueContributions

        apply init_method using InitMethodContributions
        apply repr_method using ReprMethodContributions
        apply eq_method using EqMethodContributions
        apply lt_method using LtMethodContributions
        apply le_method using LeMethodContributions
        apply gt_method using GtMethodContributions
        apply ge_method using GeMethodContributions
        apply hash_method using HashMethodContributions
        apply frozen_setattr using FrozenSetattrContributions
        apply frozen_delattr using FrozenDelattrContributions
    }

    # Method productions from the monolithic fixture remain in base:
    # InitMethodProduction, ReprMethodProduction, EqMethodProduction,
    # LtMethodProduction, LeMethodProduction, GtMethodProduction,
    # GeMethodProduction, HashMethodProduction.

    assembly DataclassModule = ModuleProduction
}
```

The base concept intentionally declares an empty
`PostInitArgContributions` matcher. That gives feature layers a named matcher
merge point without requiring the base to know about `InitVar`.

The `family base.DataclassFieldSpec { ... }` form used by feature layers is not
new work. `_compile_family(...)` already supports extending an inherited dotted
family name, and property resolution for family variants already walks
`self._extensions`.

### `dataclasses_initvar_base.yidl`

This file adds `InitVar` as a field variant and contributes only the behavior
that differs from plain stored fields.

Expected shape:

```yidl
module tests.dataclasses_initvar_base

import "dataclasses_base.yidl" as base

export concept DataclassesInitVarBase

concept DataclassesInitVarBase extends base.DataclassesBase {
    family base.DataclassFieldSpec {
        variant InitVarField {
            FieldKind
        }
    }

    matcher AnnotationContributions(field: Fields, facade: Facades) -> contribution {
        rule initvar_annotation when FieldOwner == ClassId
                                and FieldKind == "initvar"
                                -> AnnotationContribution
    }

    matcher FieldInfoContributions(field: Fields, facade: Facades) -> contribution {
        rule initvar_info when FieldOwner == ClassId
                          and FieldKind == "initvar"
                          -> FieldInfoContribution
    }

    matcher InitParamContribution(field: Fields, facade: Facades) -> contribution {
        rule initvar_required when DecoratorInit == True
                              and FieldOwner == ClassId
                              and FieldKind == "initvar"
                              and HasDefault == False
                              and HasDefaultFactory == False
                              -> RequiredParamContribution

        rule initvar_default when DecoratorInit == True
                             and FieldOwner == ClassId
                             and FieldKind == "initvar"
                             and HasDefault == True
                             -> DefaultParamContribution
    }

    matcher PostInitContribution(facade: Facades) -> contribution {
        rule post_init when DecoratorInit == True
                       and HasPostInit == True
                       -> PostInitCallContribution
    }

    matcher PostInitArgContributions(field: Fields, facade: Facades) -> contribution {
        rule initvar when DecoratorInit == True
                     and HasPostInit == True
                     and FieldOwner == ClassId
                     and FieldKind == "initvar"
                     -> PostInitArgContribution
    }
}
```

Important negative behavior:

- no init assignment rule for `FieldKind == "initvar"`
- no repr part rule
- no compare value rule
- no hash value rule
- no default class assignment unless the chosen dataclass behavior requires it

The golden should verify these through runtime/source assertions: `scale` is
accepted by `__init__`, no `scale` instance attribute is created, repr/equality/
hash ignore `scale`, and generated output does not contain a stored assignment
for `scale`.

### `dataclasses_classvar_base.yidl`

This file adds `ClassVar` as a field variant. A class variable appears in
annotations and class metadata, but it is not an instance init/repr/compare/hash
participant.

Expected shape:

```yidl
module tests.dataclasses_classvar_base

import "dataclasses_base.yidl" as base

export concept DataclassesClassVarBase

concept DataclassesClassVarBase extends base.DataclassesBase {
    family base.DataclassFieldSpec {
        variant ClassVarField {
            FieldKind
        }
    }

    resource ClassVarFieldInfoEntry = template $[
        {
            astichi_bind_external(field_name): _field_info(
                name=astichi_bind_external(field_name),
                type=astichi_bind_external(annotation),
                default=_MISSING,
                default_factory=_MISSING,
                init=False,
                repr=False,
                compare=False,
                hash=None,
                kw_only=False,
                metadata=astichi_bind_external(metadata),
                kind="classvar",
            )
        }
    ]$ {
        keep _field_info, _MISSING
    }

    contribution ClassVarFieldInfoContribution = ClassVarFieldInfoEntry {
        as FieldInfoEntry
        index FieldOrder
        order FieldOrder
        target field_info_entries { build /ClassDef }

        external field_name = FieldName
        external annotation = Annotation
        external metadata = Metadata
    }

    matcher AnnotationContributions(field: Fields, facade: Facades) -> contribution {
        rule classvar_annotation when FieldOwner == ClassId
                                  and FieldKind == "classvar"
                                  -> AnnotationContribution
    }

    matcher FieldInfoContributions(field: Fields, facade: Facades) -> contribution {
        rule classvar_info when FieldOwner == ClassId
                           and FieldKind == "classvar"
                           -> ClassVarFieldInfoContribution
    }

    matcher DefaultValueContributions(field: Fields, facade: Facades) -> contribution {
        rule classvar_default when FieldOwner == ClassId
                              and FieldKind == "classvar"
                              and HasDefault == True
                              -> DefaultValueContribution
    }
}
```

Important negative behavior:

- no init parameter rule
- no init assignment rule
- no repr part rule
- no compare value rule
- no order value rule
- no hash value rule

The golden should verify these through runtime/source assertions: `kind` is not
an `__init__` parameter, is present as class-level/annotation metadata, does not
appear in repr/equality/hash behavior, and generated output does not contain
`self.kind` assignment.

### `dataclasses_combined.yidl`

This file proves feature layering and diamond dedupe.

Expected shape:

```yidl
module tests.dataclasses_combined

import "dataclasses_base.yidl" as base
import "dataclasses_initvar_base.yidl" as initvar
import "dataclasses_classvar_base.yidl" as classvar

export concept DataclassSubstitute

concept DataclassSubstitute extends
    initvar.DataclassesInitVarBase,
    classvar.DataclassesClassVarBase
{
}
```

`base` is imported intentionally even if only the two feature concepts are
extended. The test should prove the combined file can import the shared base
without requiring direct extension and without causing duplicate inherited base
symbols.

## Split Dataclasses Golden Source

Create `tests/data/gold_src/yidl_update_a_dataclasses_base.py` and
`tests/data/gold_src/yidl_update_a_dataclasses_split.py` by forking the current
defaults golden source.

Both golden sources should load YIDL inputs from:

```python
YIDL_FIXTURE_DIR = Path("tests/data/yidl/yidl_update_a_dataclasses_split")
```

The base golden compiles only the base YIDL file:

```python
BASE_YIDL_PATH = YIDL_FIXTURE_DIR / "dataclasses_base.yidl"


def _compile_base_concept() -> object:
    return compile_yidl_files(
        {BASE_YIDL_PATH.as_posix(): BASE_YIDL_PATH.read_text(encoding="utf-8")},
        BASE_YIDL_PATH.as_posix(),
    ).concepts["DataclassesBase"]
```

The base fixture data should prove only plain stored-field behavior. It should
still include defaults, default factories, frozen behavior, and inherited
diagnostics from the base concept, but it should not include `InitVar` or
`ClassVar` rows.

The split golden compiles all four YIDL files and enters through
`dataclasses_combined.yidl`:

```python
YIDL_FIXTURE_DIR = Path("tests/data/yidl/yidl_update_a_dataclasses_split")
YIDL_PATHS = (
    YIDL_FIXTURE_DIR / "dataclasses_base.yidl",
    YIDL_FIXTURE_DIR / "dataclasses_initvar_base.yidl",
    YIDL_FIXTURE_DIR / "dataclasses_classvar_base.yidl",
    YIDL_FIXTURE_DIR / "dataclasses_combined.yidl",
)
ENTRY_PATH = YIDL_FIXTURE_DIR / "dataclasses_combined.yidl"
```

Compile all sources:

```python
def _compile_concept() -> object:
    sources = {
        path.as_posix(): path.read_text(encoding="utf-8")
        for path in YIDL_PATHS
    }
    return compile_yidl_files(sources, ENTRY_PATH.as_posix()).concepts[
        "DataclassSubstitute"
    ]
```

The fixture data should include at least:

- stored required field: `count`
- stored default field: `level`
- stored default factory field: `tags`
- stored non-init hidden field: `hidden`
- init-only field: `scale`
- class variable: `kind`

Expected container sketch:

```python
defaults = {
    "Widget.level": 7,
    "Widget.hidden": "secret",
    "Widget.kind": "widget",
}
default_factories = {"Widget.tags": list}
```

```python
builder.add(
    facades,
    facade(
        class_id="Widget",
        class_name="Widget",
        module_name="generated_dataclasses",
        decorator_frozen=True,
        dataclass_params={"frozen": True},
        match_args=("count", "level", "tags", "scale"),
    ),
)

builder.add(
    fields,
    field(
        field_id="Widget.count",
        field_owner="Widget",
        field_name="count",
        field_order=10,
        field_kind="field",
        annotation="int",
    ),
)

builder.add(
    fields,
    field(
        field_id="Widget.scale",
        field_owner="Widget",
        field_name="scale",
        field_order=35,
        field_kind="initvar",
        annotation="int",
        compare=False,
    ),
)

builder.add(
    fields,
    field(
        field_id="Widget.kind",
        field_owner="Widget",
        field_name="kind",
        field_order=50,
        field_kind="classvar",
        annotation="str",
        has_default=True,
        init=False,
        repr=False,
        compare=False,
    ),
)
```

The generated class needs a real `__post_init__` target if the current YIDL
example only emits a call. The executable `Widget` case above should keep
`HasPostInit` false unless the fixture also contributes a method body. That
still proves the first required `InitVar` behavior: the value is accepted by
`__init__` and is not stored. A separate source-level assertion can prove
post-init argument assembly by compiling a second facade with `HasPostInit`
true, or the fixture can add a test-only `__post_init__` method contribution.

Validation assertions:

```python
widget = widget_class(3, scale=5)

assert widget.count == 3
assert widget.level == 7
assert widget.tags == []
assert not hasattr(widget, "scale")
assert widget_class.kind == "widget"
assert "kind" in widget_class.__annotations__
assert "kind" in widget_class.__dataclass_fields__
assert "kind" not in widget_class.__match_args__
assert "scale" in widget_class.__match_args__
assert "scale" not in repr(widget)
assert widget == widget_class(3, scale=99)
assert hash(widget) == hash((3, 7))
```

The exact signature assertion can use `inspect.signature(widget_class)` or
`inspect.signature(widget_class.__init__)` after the generated output is
executed.

The split golden must also keep the existing diagnostic proof from the
monolithic defaults fixture. Build an invalid container with one field where
`HasDefault == True` and `HasDefaultFactory == True`, then assert the inherited
diagnostic contribution raises `AssemblyDiagnosticError` with the field-specific
message generated by the YIDL diagnostic resource.

Add source-level negative checks only for properties that are hard to prove by
runtime behavior:

```python
assert "object.__setattr__(self, 'scale'" not in source
assert "setattr(self, 'scale'" not in source
assert "object.__setattr__(self, 'kind'" not in source
assert "setattr(self, 'kind'" not in source
```

## Expected Output Properties

The split golden must produce four materialized files:

- `decorator.py`: raw generated decorator/runtime source
- `decorator_prettier.py`: Black-formatted decorator source for inspection
- `generated_output.py`: raw emitted generated class source
- `generated_output_prettier.py`: Black-formatted generated class source

The golden validation should execute both raw and formatted versions:

```python
decorator_namespace: dict[str, object] = {}
exec(sources["decorator.py"], decorator_namespace)

pretty_decorator_namespace: dict[str, object] = {}
exec(sources["decorator_prettier.py"], pretty_decorator_namespace)

generated_namespace: dict[str, object] = {}
exec(sources["generated_output.py"], generated_namespace)

pretty_generated_namespace: dict[str, object] = {}
exec(sources["generated_output_prettier.py"], pretty_generated_namespace)
```

Do not assert `OUTPUT = "..."` style wrappers. The golden files must contain the
actual generated file contents.

## Rollout Order

### Slice A: From Imports

Implement:

- `_CompiledImports`
- `_ImportedSymbol`
- `import_from` lowering
- from-import resolver integration
- from-import diagnostics
- alias-import/from-import namespace collision checks
- explicit not-implemented diagnostics for accepted but unsupported from-import
  kinds such as `union` and `port`

Run:

```text
pytest tests/generation/test_yidl_lark_parser.py -k "from_import or import"
```

### Slice B: Non-Schema Map Merge

Implement:

- extension closure
- non-mergeable map merge
- schema lookup map merge while leaving DDS structural validation in
  `CapsuleConceptPlan`
- contribution matcher merge
- resolver updates to use merged maps
- assembly validation against merged maps
- inherited assembly runtime emission

Run:

```text
pytest tests/generation/test_yidl_lark_parser.py -k "inherit or merge or assembly"
```

### Slice C: Resource Matcher Merge

Implement inherited resource matcher extension through `builder.use_matcher`,
including inherited-default checks and diamond rule dedupe.

Run:

```text
pytest tests/generation/test_yidl_lark_parser.py -k "matcher"
```

### Slice D: Layered Dataclasses Goldens

Add the split dataclasses YIDL fixture directory and both product goldens:

- base-only golden for `dataclasses_base.yidl`
- combined golden for all four YIDL files

The combined golden should include the inherited diagnostic assertion and
`InitVar` / `ClassVar` negative behavior checks.

Run:

```text
pytest tests/test_yidl_goldens.py -k "yidl_update_a_dataclasses_base or yidl_update_a_dataclasses_split"
pytest tests/generation/test_yidl_lark_parser.py
```

### Slice E: Full Local Check

Run the focused YIDL suite:

```text
pytest tests/generation/test_yidl_lark_parser.py tests/test_yidl_goldens.py
```

If time allows, run all tests.

## Completion Criteria

The slice is complete when:

- from-import declarations are lowered and validated
- exports are still parsed but not enforced
- child concepts expose inherited runtime assembly members in
  `YidlCompiledConcept`
- child concepts can add matcher rules to inherited matchers
- duplicate non-mergeable inherited symbols reject
- diamond inheritance dedupes shared base symbols
- generated decorator source contains inherited and local generation members
- base dataclasses golden emits and executes plain stored-field behavior
- combined split dataclasses golden emits and executes layered behavior
- both dataclasses product goldens prove the diagnostic contribution still fires
- `InitVar` and `ClassVar` behavior is proven by the combined split golden

## Known Non-Goals

- no replacement-style override syntax
- no export visibility enforcement
- no `use` lowering
- no module-name package loader
- no implicit search through every imported module
- no `union` or `port` from-import lowering
- no lifecycle-specific shortcuts
- no disabling inherited matcher rules in this slice
