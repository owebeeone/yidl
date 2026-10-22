# Build a Python generator with YIDL

YIDL helps you build **Python code generators**. You supply reusable Python code
pieces, structured inputs describing what to generate, and rules for combining
them. A generator can produce plain classes with direct field stores, select
property accessors, or assemble ordered method statements. The generated classes
then run as ordinary Python.

There are two products to understand. YIDL first turns your definitions into a
**generator library** with input-row types and assembly functions. Your program
supplies rows to that library to produce **application code**, such as Point.
Only after executing that generated code do you call `Point(3, 4)` to make an
object. A field-name input `x` describes code to generate; 3 is an instance value.

## Start with the model

For your first visit, follow **How YIDL works → Generation stages → Installation
→ First generator**. This is also the Start Here navigation and footer sequence.
It introduces the vocabulary and YIDL/Astichi/application responsibilities before
the complete tutorial source.

[How YIDL works](concepts/model.md){ .md-button .md-button--primary }
[Generation stages](concepts/generation-pipeline.md){ .md-button }

Already familiar with Python generators? After
[installation](start/install.md), take the
[direct run route](start/first-generator.md#run-and-inspect).

## What you will build

The first tutorial creates `Point(3, 4)`, whose `x` and `y` are direct slots:

{{source:tests/data/goldens/materialized/documentation_classes/first_model.py|python}}

The tutorial explains which definitions, input rows and assembly steps produce
this code before showing its full source. YIDL selects and places the pieces;
its Astichi dependency combines Python syntax trees and manages names/scopes.
Your application decides field policy and supplies the instance values.

**Development documentation — 0.1.0 candidate, CPython 3.12+.** Exact executed
example environments and remaining limits are recorded in
[compatibility](reference/compatibility.md). Packaging and publication are
separate gates. The current tutorial uses the explicit Python backend.

## Choose a task

| You want to… | Read |
| --- | --- |
| Learn the parts and their responsibilities | [How YIDL works](concepts/model.md), then [generation stages](concepts/generation-pipeline.md) |
| Generate and inspect the first result | [First generator](start/first-generator.md) |
| Follow a property into a generated parameter | [Matching and data flow](guides/matching-and-data-flow.md) |
| Extend a generator | [Inheritance and specialization](concepts/composition.md) |
| Diagnose generation | [Debugging assembly](guides/debugging-assembly.md) |
| Find exact contracts | [Language](reference/language.md), [APIs](reference/apis-and-cli.md), [compatibility](reference/compatibility.md) |
| Run other examples | [Example catalog](examples/index.md) |

Lifecycle, Dataclass and Undoable are larger applications of the generic
compiler. Their transaction and field policies are their own;
[qualified consumer excerpts](examples/consumers.md) illustrate their uses after
the standalone tutorial.
