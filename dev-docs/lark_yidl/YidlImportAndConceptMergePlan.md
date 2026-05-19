# YIDL Import And Concept Merge Plan

## Goal

Make Lark YIDL files genuinely split-able so a larger compiler concept can be
factored across multiple `.yidl` files and recomposed through imports and
concept inheritance.

The immediate proof target is a split dataclasses example:

- one YIDL file owns the shared dataclass input schema
- one or more YIDL files extend that schema with generation resources,
  matchers, contributions, productions, and assemblies
- the generated decorator/runtime output is equivalent to the current
  single-file dataclasses defaults golden

## Current State

The grammar already accepts:

- `module <qname>`
- `import "path.yidl" as alias`
- `from "path.yidl" import <kind> <Name> [as Alias]`
- `export <kind> <Name>`
- `concept Child extends base.Concept`
- `use qname [as Name]`

The compiler currently implements only part of that surface.

Working today:

- alias imports through `import "core.yidl" as core`
- relative import path resolution
- import-cycle detection
- concept inheritance through `extends core.Core`
- schema inheritance/merge for properties, schema families, records, and
  collections
- imported resource references in some resource-expression contexts, such as
  template edge options

Known gaps:

- `from "x.yidl" import ...` parses but is not lowered
- `export ...` is recorded but not enforced
- `use ...` parses but lowering is not implemented
- inherited resources, matchers, contributions, composable productions,
  assembly edges, and assemblies are visible to some resolver paths but are not
  merged into the compiled child concept runtime maps
- imported resources can resolve during compile but may fail later at assembly
  runtime because the runtime only sees the child concept's local resource map

## Target Semantics

### Modules And Paths

Import paths are source-relative POSIX paths. Absolute import paths remain
rejected because committed YIDL files must not contain machine-local paths.

`module <qname>` is descriptive metadata. Import resolution is path-based for
now; module-name based lookup is out of scope for this slice.

### Export Metadata

`export` remains parsed metadata in this slice. Cross-file access does not
require an exported symbol yet.

Authors may still write:

```yidl
export concept Core
export resource FieldTemplate
export contribution FieldContribution
```

but the compiler should not enforce visibility from those declarations in the
next implementation slice. This keeps the import/merge work focused on concept
composition rather than module privacy.

Within one file, all local concept members remain visible to that concept.
Across files, alias-qualified references may resolve to any symbol in the
imported module according to the existing symbol rules.

Future export enforcement can be designed later if module-boundary privacy
becomes important.

### Alias Imports

Alias imports keep their current syntax:

```yidl
import "core.yidl" as core
```

Alias-qualified references continue to use `core.Name`. For this slice, the
compiler resolves `core.Name` by searching visible names in the imported
module, not by filtering through `export` declarations.

If more than one concept in a module contains the same member name and the
reference does not identify the concept, the compiler should reject the
reference as ambiguous rather than guessing.

### From Imports

Implement the grammar that already exists:

```yidl
from "core.yidl" import concept Core
from "core.yidl" import resource FieldTemplate as BaseFieldTemplate
```

Imported names are added to an explicit imported-symbol table for the current
file. They should behave like alias-qualified references with a local alias.

Resolution order for unqualified names becomes:

1. local concept definitions
2. extended concept definitions
3. explicit `from ... import ...` aliases

Alias imports remain available only through their import alias.

### Use Declarations

Keep `use` out of the implementation slice unless it becomes the smallest way
to make split concepts readable.

For now, `use` should continue to produce a clear "not implemented" diagnostic.
Do not let it silently behave like an import or an inheritance merge.

## Concept Inheritance Merge

`extends` is concept composition. A child concept inherits the usable compiled
surface of each parent concept and may add local definitions.

The child compiled concept should expose merged maps for:

- properties
- schema families
- records
- collections
- resources
- resource matchers
- data productions
- operations
- contribution specs
- contribution matchers
- composable productions
- assembly edges
- assemblies

The existing `CapsuleConceptPlan` already receives `extends=...` and handles
schema inheritance for the DDS plan. The Lark compiler must also merge the
non-schema maps it stores on `YidlCompiledConcept`, because the assembly runtime
uses those maps directly.

## Collision And Matcher Merge Rules

Start conservative.

Do not add replacement-style override syntax in this slice. Behavior
specialization should come from matcher merge: a child concept adds matcher
rules that select different resources or contributions, and the merged matcher
runtime chooses the winning rule by the normal rule precedence model.

Local definitions may not redefine inherited names for non-mergeable symbol
kinds.

Current behavior already rejects inherited property redefinition. Extend that
principle to:

- resources
- productions
- contributions
- composable productions
- assembly edges
- assemblies

Matcher-like definitions are the exception:

- resource matchers with the same inherited name merge their rule entries
- contribution matchers with the same inherited name merge their rule entries
- inherited defaults remain in force unless there is an explicit future design
  for default replacement
- two defaults for the same matcher should reject in this slice
- duplicate rule names in the same merged matcher should reject unless they are
  the exact same inherited rule from a common ancestor

This is the intended "override" mechanism: a child supplies a more specific or
higher-weight rule that selects a new resource/contribution while the inherited
production, assembly edge, and target topology remain reusable.

If two parents provide the same symbol kind and name, the child concept should
reject the inheritance as ambiguous unless both inherited values are exactly the
same object from a common ancestor. Diamond inheritance should not duplicate or
silently fork definitions.

Cross-kind name collisions should follow existing resolver behavior:

- a resource consumer that names a property reports "property, not resource"
- a contribution consumer that names a resource reports "resource, not
  contribution"
- ambiguous names should identify the conflicting symbol kinds

## Runtime Assembly Lookup

The assembly runtime must be able to execute inherited generation graphs.

When a child concept extends a parent concept:

- `concept.resources` must include inherited resources
- `concept.contributions` must include inherited contributions
- `concept.contribution_matchers` must include inherited contribution matchers
- `concept.composable_productions` must include inherited composable productions
- `concept.assembly_edges` and `concept.assemblies` must include inherited
  edges and assemblies where applicable

This lets a child assembly use a parent production root, and lets a child
production apply parent contribution matchers.

The runtime should not need to know whether a resource came from a local or
inherited file. That should be resolved before `YidlCompiledConcept` is handed
to `run_assembly(...)` or emitted into the generated decorator source.

## Export Handling

Do not enforce exports in this slice.

`export` declarations should continue to parse and remain recorded on
`YidlCompiledModule`, but no resolver should reject a symbol because it lacks an
export declaration.

If future code needs a stable public/private boundary, add export enforcement as
a separate slice with its own tests. That later slice should also decide how to
name assembler-specific symbol kinds such as composable productions, assembly
edges, and contribution matchers.

## Implementation Slices

### Slice 1: From Imports

Lower `from "path" import <kind> <Name> [as Alias]`.

Tasks:

- compile imported modules for `import_from` declarations
- build a local imported-symbol table keyed by alias
- validate the imported symbol exists in the imported module
- resolve unqualified imported aliases after local and inherited names
- reject alias collisions with local declarations and other imported aliases

Tests:

- `from "core.yidl" import concept Core` then `extends Core`
- `from "core.yidl" import resource Bind as BaseBind` in a template edge
- importing a missing symbol rejects
- two `from` imports with the same alias reject
- local definition shadowing an imported alias rejects or is explicitly
  diagnosed

### Slice 2: Merge Non-Schema Concept Maps

Merge inherited non-schema maps into `YidlCompiledConcept`.

Tasks:

- add a map merge helper with same-kind collision detection
- merge same-name resource matchers and contribution matchers by combining
  their rule entries
- keep inherited matcher defaults unless a duplicate default is introduced,
  which should reject
- merge resources, matchers, productions, operations, contributions,
  contribution matchers, composable productions, assembly edges, and assemblies
- keep local definitions available through the same maps
- preserve existing schema merge behavior through `CapsuleConceptPlan`
- update resolvers to prefer merged maps where that avoids duplicated extension
  scans

Tests:

- child concept can run an assembly inherited from a parent
- child production can use an inherited resource as root
- child contribution can use an inherited resource
- child production can apply an inherited contribution matcher
- child can add a contribution-matcher rule that wins over an inherited rule by
  specificity or weight
- child can add a resource-matcher rule that wins over an inherited rule by
  specificity or weight
- duplicate defaults in a merged matcher reject
- inherited name collision across two parents rejects
- local redefinition of inherited resource rejects

### Slice 3: Layered Dataclasses Golden

Create a canonical success-path golden that proves practical layered
composition. This should not be a simple "schema file plus generation file"
split; that would prove imports but not the feature layering model YIDL needs.

Suggested file shape:

```text
tests/data/yidl/dataclasses_base.yidl
tests/data/yidl/dataclasses_initvar_base.yidl
tests/data/yidl/dataclasses_classvar_base.yidl
tests/data/yidl/dataclasses_combined.yidl
tests/data/gold_src/yidl_update_a_dataclasses_split.py
tests/data/goldens/materialized/yidl_update_a_dataclasses_split/
```

The base file should own:

- the common dataclass facade schema
- the common field schema/family
- the plain instance-field variant
- the stable module/class/method production topology
- base resources and contributions for plain instance fields
- matcher names that act as extension points

The initvar layer should:

- import and extend the base concept
- add an initvar field variant to the inherited field family
- add resources/contributions only for initvar-specific behavior
- add matcher rules to inherited matcher names, especially init parameters and
  post-init arguments

The classvar layer should:

- import and extend the base concept
- add a classvar field variant to the inherited field family
- add resources/contributions only for classvar-specific behavior
- add matcher rules for annotation/default/class metadata behavior while
  deliberately not participating in init/repr/compare/hash storage behavior

The combined file should:

- import the base, initvar, and classvar concepts
- extend the initvar and classvar concepts together
- exercise diamond inheritance through the shared base concept
- deduplicate the common inherited base symbols
- merge matcher rules from all layers into the same production topology

This split is intentionally close to how the DDS schema model already works:
schema families and unions can be extended by adding variants in child concepts.
The new work is making the Lark compiler do the same for generation concepts:
resources remain non-mergeable definitions, while matchers are merge points that
select those resources/contributions.

Tests:

- generated decorator source is golden-checked
- generated output source is golden-checked
- decorator-time defaults/default factories still work
- diagnostic resources still fire through matcher-selected contributions
- plain instance fields produce stored instance attributes
- initvars produce init parameters and post-init arguments without stored
  instance attributes
- classvars produce class-level/annotation behavior without init/repr/compare/
  hash participation
- the combined concept can extend multiple feature layers that share the same
  base without duplicate inherited symbol failures

## Diagnostics

Diagnostics should name:

- importing file
- imported path
- import alias or imported local alias
- symbol kind
- symbol name
- whether the failure is missing, ambiguous, or wrong-kind

Examples:

```text
child.yidl: imported symbol core.Missing is not a concept in core.yidl
child.yidl: from import resource FieldTemplate is ambiguous in core.yidl
child.yidl: resource Root shadows imported resource Root
```

Exact wording can differ, but the tests should pin the important terms.

## Non-Goals

- No replacement-style override syntax such as `replace resource` or
  `override matcher`.
- No module-name package loader.
- No filesystem access outside the `compile_yidl_files(...)` source map.
- No implicit import search over all imported modules.
- No export enforcement.
- No lifecycle-specific shortcut behavior.

## Open Questions

1. Should inherited assemblies be callable from the child by default, or should
   child concepts explicitly re-export/root them?
2. Do we need explicit syntax for disabling an inherited matcher rule, or is
   additive rule precedence rich enough?
3. If export enforcement is added later, should assembler-specific names such
   as composable productions and contribution matchers become exportable symbol
   kinds?

For the next slice, choose conservative answers: inherit usable maps, reject
non-mergeable collisions, merge matcher rules, and do not enforce exports.
