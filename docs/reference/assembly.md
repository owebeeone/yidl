# Contributions, productions and assembly

A resource is reusable code/data authority. A contribution describes one kind of
insertion. A live build instance has a name/index within the assembly. Sharing a
resource does not mean sharing a live instance identity.

| Field | Meaning | Tutorial value |
| --- | --- | --- |
| Resource name | Reusable authored snippet | `Parameter` |
| Contribution name | Binding/placement declaration | `Param` |
| `as` | Live build name | `Param` |
| `index` | Numeric instance index | `(ClassOrder, FieldOrder)` |
| `order` | Insertion ordering | `FieldOrder` |
| `target` hole | Receiving surface | `params` |
| `build` path | Build to locate | `/InitMethod` |
| `ident` | Identifier demand binding | `field_name = FieldName` |
| `external` | External literal/path binding | `slot = FieldName` |

Index accepts `int`, tuple of ints, or no index. A string collection identity is
not a valid build index. Orders and paths are evaluated from the current data
stack. Keep collection identity, owner relationship, index and order distinct.
Explicit numeric composites avoid repeated-field collisions across owners.

## Nested roots and addressing

`ModuleProduction` builds `/Root`, then class production contributions establish
`/ClassDef`. `InitProduction` establishes `/InitMethod`; its field contributions
target local mapped roots. A flat absolute-looking path is evaluated within the
current production/root mapping. For indexed siblings use the actual evaluated
index, as demonstrated by `yidl_update_a_scope_paths.py`.

The grammar allows target `build` and `owner` constraints, indexed segments and
selector segments. Accepted path syntax does not prove a destination exists.
A missing build, unresolved binding and wrong owner can produce different cause
chains. Low-level selector helpers are diagnostic tools, not a universal build
trace API.

## Order and empty behavior

Productions apply their declared edges/phases. Contributions carry independent
insertion order; root names and index identities must not collide. An empty-source
resource is suppressed. No match supplies nothing. Neither automatically fills a
mandatory hole. Explicit empty parameter payloads and pass statements fill the
tutorial's mandatory holes even for zero fields/disabled init.

An `assembly Name = Production` declaration produces `build_Name` in the emitted
runtime. `export concept` controls import visibility; it does not by itself name
all assembly functions. Diagnostic contributions fail explicitly with selected
messages instead of generating code. [Debugging](../guides/debugging-assembly.md)
shows how to inspect available builders and metadata.

Nested indexed expression propagation from D17 remains unresolved. Do not infer
support for that arrangement from successful nested class/method productions.
