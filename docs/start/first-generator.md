# Generate your first class

Build a two-field slotted class from facts. This example uses no Lifecycle,
Dataclass or Undoable package. Complete [installation](install.md) first.

## Run and inspect

From the YIDL repository root, with your installed interpreter:

```sh
ASTICHI_LOWER_ENGINE=python build/example-env/bin/python \
  example/documentation/generate.py --out build/first
```

The command asserts `Point(3, 4).x == 3`, `y == 4`, signature order `x, y`, direct
stores, and no instance `__dict__`. It writes `runtime.py` (the generated fact
schema and assembly library) and `model.py` (the final class). These are different
products of different stages.

## Author definitions

`classes.yidl` owns the schema and resources. Record entries are whitespace
separated; collection identity, field ownership and ordering are explicit.
`SlotNames` is already normalized by this tiny consumer; DDS does not infer slots
from field rows.

{{source:example/documentation/classes.yidl|text}}

Read it from the inside out: `Parameter` supplies a function-signature payload;
`Store` supplies a statement; `Init` exposes the parameter and store holes;
`ClassShell` exposes methods. Contributions bind values and identify destinations.
Matchers choose contributions. Productions establish the build tree. The final
`assembly Module` exports `build_Module` in the emitted library.

## Compile, fill facts and execute

The executable driver is the sole author of the tutorial's success assertions:

{{source:example/documentation/generate.py|python}}

The sequence is:

1. `compile_yidl_files` resolves the source map and builds a compiled concept.
2. `emit_concept_runtime_source` emits its data descriptors, resources and builds.
3. Execute that trusted library into a fresh schema namespace.
4. `new_builder()`, generated concrete record constructors, and `builder.add`
   populate facts using **storage names** such as `field_name`.
5. `freeze()` produces an immutable data container.
6. `build_Module(facts)` selects and wires contributions into a composable.
7. `to_executable_ast()` materializes Python; compile that AST and execute it in
   the consumer namespace. Construct `Point` only after this stage.

Source parsing at definition/template compilation differs from compiling the
final AST. A factory callback should run when the generated code calls it, not
while a literal's repr is being rendered. [Captures](../concepts/binding-and-ownership.md)
explain how to supply arbitrary Python objects.

## Change one thing

Run `--extended` to create `Point(x, y)` and `Size(x)`, `--empty` for zero fields,
or `--disabled` to omit `__init__`. See the [gallery](../examples/generated-gallery.md)
for the exact outputs. The modes are separate scenarios; do not combine them.
Continue to [data flow](../guides/matching-and-data-flow.md) to understand why the
reversed input rows still produce `x, y`.
