# Generate your first class

**Learning path · Step 4 of 4.** Use the environment from
[Installation](install.md). Run the example first, then follow the explanation
of one field. The complete source listings at the end are optional reference.

Build a two-field slotted Point class. The beginner sequence is
[How YIDL works](../concepts/model.md) →
[generation stages](../concepts/generation-pipeline.md) →
[installation](install.md) → this tutorial. Those first pages explain the parts;
the walkthrough below connects them before the complete source listings.

## What happens in this example

You author `classes.yidl` to describe input rows, reusable Python pieces and
rules for putting them together. The driver `generate.py` runs three stages:

1. **Prepare:** compile those definitions into `runtime.py`, a generator library
   with `ClassRow`/`FieldRow` input types and `build_Module`.
2. **Generate:** supply rows describing Point, x and y; the library selects
   parameters/stores and assembles Point code. The driver saves that code as
   `model.py` and executes its Python syntax tree to obtain the Point class.
3. **Use:** call `Point(3, 4)`. Its constructor assigns this instance's values;
   the generator is not rerun for each instance.

The input fact `field_name="x"` tells the generator which name to emit. It is
not the value 3. The `.yidl` file describes how to generate classes; `runtime.py`
is the generated generator library; `model.py` is generated application code.
YIDL selects/binds/places pieces, Astichi combines their Python syntax and scopes,
and this small consumer's driver supplies field policy and input values.

## Run and inspect

Experienced readers can start here after installation. From the YIDL repository
root, with your installed interpreter:

```sh
ASTICHI_LOWER_ENGINE=python build/example-env/bin/python \
  example/documentation/generate.py --out build/first
```

The command checks that `Point(3, 4)` has x=3 and y=4, a signature ordered x/y,
direct stores, and no instance `__dict__`. It writes `runtime.py` and `model.py`
inside `build/first/`. These are generated outputs; keep `classes.yidl` and
`generate.py` as the editable source.

## Follow one field through the generator

### 1. Describe the inputs

A **property** describes a fact such as a field's name. A **record** groups facts
into a row; a **collection** holds those rows. These declarations are excerpts
from the complete concept, not separate runnable files:

{{source:example/documentation/classes.yidl@10:19|text}}

The generated Python constructor uses storage spelling `field_name`; declarations
refer to semantic property `FieldName`. The driver supplies a row for x with
owner `point` and order 10, and another for y with order 20. It also supplies a
class row naming Point and a slot tuple `("x", "y")`. Computing that tuple is
this driver's policy; the data layer does not infer it from field rows.

### 2. Write reusable code pieces

A **resource** holds a Python code piece. The parameter resource has a name to
fill in; the store resource has a parameter read and an attribute path to fill in:

{{source:example/documentation/classes.yidl@34:40|text}}

The unusual names and marker calls are Astichi's composition instructions.
Binding x into these pieces eventually produces a parameter `x` and the direct
statement `self.x = x`. The `astichi_pass` expressions refer to the containing
constructor's self/parameter; the trailing `._` marks a valid assignment target.
These instructions disappear from final application code.

### 3. Choose, bind and place a piece

A **contribution** adds the binding and destination to a resource. This one binds
the selected FieldName as a Python identifier and targets the constructor's
parameter hole:

{{source:example/documentation/classes.yidl@83:89|text}}

A **matcher** selects it only when the field belongs to the current class and is
enabled. The nested constructor **production** groups parameter/store insertion
steps. Its root is the constructor code piece, exposing named holes for those
insertions. The final **assembly** declaration exposes the build function
`build_Module` in the generated library.

Collection identity, owner, build index and output order are separate. The
composite integer index distinguishes insertions across classes; FieldOrder
orders the parameters. The driver deliberately inserts y before x, yet the
result's signature is x/y. The [data-flow guide](../guides/matching-and-data-flow.md)
traces those decisions across two owners.

## How the Python driver runs the stages

Before reading the full driver, recognize these operations:

| Operation | Result |
| --- | --- |
| `compile_yidl_files(source_map, entry_name)` | Compiled concept definitions from explicitly named source text |
| `emit_concept_runtime_source(...)` | `runtime.py` library source for those definitions |
| Execute that library in a fresh namespace | Row classes, builder and assembly functions |
| `new_builder()` and `builder.add(...)` | Mutable collection of this generation's input facts |
| `freeze()` | Read-only fact container; input preparation is complete |
| `build_Module(facts)` | Selected/bound pieces in an Astichi composable, its intermediate code object |
| `to_executable_ast()` | Final Python syntax tree for Point |
| `compile(tree, ..., "exec")` and `exec` | Executable Point class in the consumer namespace |
| `Point(3, 4)` | User instance with x=3 and y=4 |

Source/template parsing during preparation or lazy resource compilation differs
from compiling this final tree. Live defaults/callbacks need explicit captures;
see [binding and ownership](../concepts/binding-and-ownership.md) after this example.

## Options, defaults and a small change

With no scenario flag, the script generates the two-field Point. Every scenario
switch defaults to false; choose at most one. With no `--out`, it writes
`runtime.py` and `model.py` to **`build/documentation/` relative to your current
working directory**. `--out` overrides that directory; it does not change the
`.yidl` authority. The run above explicitly chooses `build/first` instead.

| Option | Effect | Default |
| --- | --- | --- |
| `--out DIR` | Destination for the two generated Python files | `build/documentation` under the current directory |
| `--extended` | Generate Point(x, y) and Size(x) | False |
| `--empty` | Generate zero-field Point with a zero-parameter constructor | False |
| `--disabled` | Generate Point slots while omitting its init method | False |
| `--help` | Describe the command and options, then exit | Runs only when requested |

```sh
build/example-env/bin/python example/documentation/generate.py --help
```

Use `--extended` to explore a second owner, or inspect the
[gallery](../examples/generated-gallery.md) for all modes. For an authoring
change, alter the field facts and matching slot tuple together to request another
field, and update the example's constructor call and behavior checks accordingly.
To change the generated store behavior, edit the resource in `.yidl` and
regenerate; editing `model.py` alone will be overwritten.

## Remove the experiment's outputs

If `build/first/` was created only for this walkthrough, remove that directory to
discard its generated Python files. If you used the default destination instead,
its disposable output directory is `build/documentation/`. Keep authored
`example/documentation/classes.yidl` and `generate.py`. Environment/wheel removal
and outside-copy cleanup are listed in the installation page's
[cleanup steps](install.md#clean-up-the-walkthrough).

## Continue after the tutorial

You have completed the four-page learning path. Next,
[inspect the generated files](inspect-output.md) to distinguish your editable
inputs from the two outputs. To explore selection across two classes, follow
[Matching and data flow](../guides/matching-and-data-flow.md). These are follow-up
choices; the full listings below are available when you want to inspect the
complete example.

## Optional: complete source listings { #complete-source-for-reference }

You do not need to retype these listings or run them as additional steps. The
command above already uses these repository files. The complete source adds
class/method shells, explicit empty contributions for mandatory holes, the other
selections and the executable checks.

### Declarations: classes.yidl

{{source:example/documentation/classes.yidl|text}}

### Driver: generate.py

{{source:example/documentation/generate.py|python}}
