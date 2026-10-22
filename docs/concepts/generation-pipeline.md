# Generation stages

After [How YIDL works](model.md), keep three moments separate: preparing a
generator, generating a particular class, and using that class. The same
prepared generator can receive different input rows for later generations.

## 1. Prepare the generator library

Author a `.yidl` concept describing input row shapes, reusable Python code pieces
and rules for assembling them. `compile_yidl_files` reads those definitions;
`emit_concept_runtime_source` emits a Python library. The tutorial calls that
library `runtime.py` and executes it into a fresh Python namespace.

This library supplies `ClassRow` and `FieldRow` input types, `new_builder()` to
collect their values, and `build_Module` to run its declared assembly. It is
reusable generator machinery. It is not yet the Point application class.

## 2. Generate the particular class

The Python driver creates rows describing Point and its fields. A **builder**
is the mutable container in which it adds them. `freeze()` turns that data into
a read-only **fact container**, so later matching and code assembly can use a
stable set of inputs. Data-producing operations, when a consumer needs them,
run before this freeze.

`build_Module(facts)` selects contributions, binds field names such as `x`, and
inserts the code pieces in their declared order. The result is an Astichi
**composable**, the intermediate code object defined in the introduction.
`to_executable_ast()` materializes it into a Python syntax tree. The driver saves
readable source as `model.py`, then uses Python's `compile(tree, ..., "exec")`
and `exec` to create the actual Point class in a namespace.

The tutorial's explicit source-template route can parse code while preparing
resources, including lazy template compilation during generation. The final
`compile` above compiles a Python tree; it does not reparse a handwritten method
string. These stages are not a promise that all generation is parser-free.

## 3. Use the generated class

Ordinary Python code calls `Point(3, 4)`. Its generated constructor assigns 3 to
`self.x` and 4 to `self.y`. Further instance creation uses that existing class;
it does not rerun the generator. Generation inputs specify names and behavior;
constructor arguments supply this instance's values.

## Locate an error by stage

| Stage | Input → output | Typical failure |
| --- | --- | --- |
| Parse/resolve | Source map → compiled concepts | Grammar, missing import/export, duplicate inherited name |
| Emit library | Data definition and assembly metadata → Python runtime source | Unsupported evaluator/source expression |
| Fill/produce facts | Concrete records → mutable builder | Wrong storage keyword/type, identity or cardinality conflict |
| Freeze/snapshot | Builder → resolved data | Operation/provider diagnostics before freeze |
| Match | Input combinations → selected resource/contribution | Missing property, ambiguous visible name, no match |
| Build/bind | Selected instances → wired composable | Duplicate instance, unresolved identifier, absent target |
| Materialize | Composable → Python AST | Mandatory hole, unsupported target context, backend failure |
| Execute | AST and namespace → class → instances | Missing capture, user callback exception, wrong behavior |

For example, `Assignment` failing to target `stores` is a generation failure.
Inspect its exception chain, selected input row, binding and destination. It is
not a failure of `Point(3, 4)`'s later field assignment. The
[debugging guide](../guides/debugging-assembly.md) supplies the inspection route.

`MatcherGeneratedValue.to_generator()` lazily compiles and caches an **unbound
code template**. It does not cache a completed Point class or Point.x's runtime
value. Protected generated decorator/helper paths are intended to avoid fresh
ad hoc source parsing; that implementation rule differs from the explicit
compiler/build boundary above. See [caching and performance](../reference/caching-and-performance.md)
for those lifetimes and the limits of native-backend claims.

Next, [install the environment](../start/install.md) and
[generate your first class](../start/first-generator.md).
