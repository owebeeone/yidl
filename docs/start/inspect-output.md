# Inspect generated output

Keep these artifacts separate:

| Artifact | Meaning | What to inspect |
| --- | --- | --- |
| `classes.yidl` | Authored definition authority | Property names, resource shape, target paths |
| `runtime.py` | Generated schema/assembly library | Record constructor storage names, `build_Module`, `ASSEMBLY_*` metadata |
| `model.py` | Final generated Python | Direct slots/stores, signature, surviving markers |
| Executed class | User-visible behavior | Values, callbacks, ordering, exceptions |

Run the first-generator driver with `--out build/first`, then open those two
Python files. `ast.unparse(composable.to_executable_ast())` provides readable
Python without requiring you to evaluate a second handwritten code sample.
`composable.emit_commented()` is another inspection surface; comments and
hygiene spellings can differ from final AST display.

The tutorial records the actual engine selection in its JSON output. A variable
requesting native execution is not evidence of native dispatch. Keep package
versions and import origins with reproduction logs.

## Questions to answer before refreshing a golden

Does each field have a slot? Does each selected parameter have a store? Are
unselected and orphan fields absent? Is `x` before `y` despite reversed fact
insertion? Can you instantiate the result with the expected signature?

The canonical `documentation_classes.py` fixture calls the tutorial's behavioral
assertions and snapshots its model source. A snapshot matching yesterday is not
an independent oracle. Intentional changes must first satisfy the behavior
requirement, then receive an inspected output refresh.

For failures, preserve the traceback chain and locate its stage with
[debugging assembly](../guides/debugging-assembly.md). There is no promised
all-in-one trace flag.

## Keep authority, remove disposable output

`runtime.py` and `model.py` are generated files in your selected `--out`
directory. Remove that destination if it belongs only to this experiment; retain
`classes.yidl` and `generate.py`, which are the authored inputs needed to rebuild
it. The [installation cleanup steps](install.md#clean-up-the-walkthrough) also
cover the created environment and wheel directory without deleting authored files.
