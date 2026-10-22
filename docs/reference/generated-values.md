# Generated-value resources

Import these factories from `yidl.generation.data_def_sys` (which reexports the
owning matcher-value module). A matcher resource must satisfy the generated-value
contract; a raw arbitrary object or raw composable is not interchangeable.

| Factory | Accepted input / result | Evaluation |
| --- | --- | --- |
| `from_literal(value)` | None, bool, int, float, complex, str; recursively tuple/list/dict/set | Rendered as Python literal source; other objects reject |
| `from_astichi_code(source, ..., arg_names=..., keep_names=...)` | String source and compile metadata | Dedented wrapper; lazy compile on `to_generator()` |
| `from_import(module, name)` | Dotted identifier module and identifier symbol | Import reference; composable conversion emits import surface |
| `astichi_template(template, arg_names=..., bind=..., keep_names=...)` | Generated-value template and optional generated-value edge expressions | Edge expressions evaluated against `record` |

The public factory here is **`astichi_template`**; do not assume a
`from_astichi_template` alias because an older plan used that phrase. The `.yidl`
`template` resource lowers to this wrapper contract.

`MatcherGeneratedValue` stores source, file/line/offset, identifier mappings and
keep names. Its first `to_generator()` lazily compiles and retains the unbound
composable; later calls return it. This is neither a class cache nor memoization
of a runtime callback.

## Template edges

`arg_names_for(record)` expects a mapping of string keys and string identifier
values. `bind_for(record)` expects a mapping with string keys. `keep_names_for`
expects strings. Edge expressions are materialized, compiled as an expression,
and evaluated with `record` in the local environment and normal Python builtins.
They do not get an implicit arbitrary surrounding production namespace. Supply
all required data explicitly; a missing provider is not repaired by a keep.

The canonical `yidl_lark_v2_vertical.py` example demonstrates generated resources,
edge bindings and matcher-result production. Multi-record generic evaluated fields
are a separate mechanism; the template edge API shown here receives one `record`
object. A universal nested two-record edge environment is not qualified.

Use a fresh namespace/capture for callbacks, live types and opaque defaults. The
factory's literal domain deliberately excludes arbitrary Python instances and
`bytes` in this candidate. Preserve import provenance and do not invoke callbacks
during generation to obtain something serializable.
