# Build a Python generator with YIDL

YIDL helps you build **Python code generators**. You supply reusable Python code
pieces, inputs describing what to generate, and rules for combining them. The
resulting classes and functions run as ordinary Python.

This page is a guide to the documentation. Start with the learning path below;
the later sections preview its outcome and explain where to go for specific tasks.

## New to YIDL? Start here

Follow these four pages in order. The first two explain the ideas; the last two
set up your environment and walk through a working generator.

[Start learning: How YIDL works](concepts/model.md){ .md-button .md-button--primary }

1. [How YIDL works](concepts/model.md) — understand what you supply and what YIDL generates.
2. [Generation stages](concepts/generation-pipeline.md) — follow the definitions through to a usable Python class.
3. [Installation](start/install.md) — prepare and check the example environment.
4. [Generate your first class](start/first-generator.md) — run the generator, then follow how its parts fit together.

These pages are also grouped under **Start Here** in the sidebar. After the
tutorial, [Inspect output](start/inspect-output.md) helps you examine the files
you generated. You do not need to work through every guide or reference page to
finish the tutorial.

Already familiar with Python code generation? After
[installation](start/install.md), take the
[direct run route](start/first-generator.md#run-and-inspect).

## Tutorial preview: a generated Point class

The learning path leads to a generator that produces a two-field `Point` class.
You describe the class and fields, run generation, then use the resulting class
with `Point(3, 4)` to make an object whose `x` and `y` values are 3 and 4.

This is the tutorial's destination, not an instruction to start writing a Point
class here. The tutorial explains the authored inputs and shows the generated
Python. It saves two files: `runtime.py`, the generator library, and `model.py`,
the generated Point code. [How YIDL works](concepts/model.md) explains why those
are separate products.

## After the tutorial: find a specific task

Use these shortcuts when you know what you want to do. They are alternative
destinations, not another sequence to complete after the four steps above.

| You want to… | Read |
| --- | --- |
| Understand the generated files | [Inspect output](start/inspect-output.md) |
| Follow a field name into a constructor parameter | [Matching and data flow](guides/matching-and-data-flow.md) |
| Split definitions across files | [Split a project and regenerate](start/project-layout.md) |
| Extend an existing generator | [Inheritance and specialization](concepts/composition.md) |
| Diagnose a generation failure | [Debugging assembly](guides/debugging-assembly.md) |
| Look up exact syntax or an API | [Language reference](reference/language.md) or [APIs and CLI](reference/apis-and-cli.md) |
| Try another runnable example | [Example catalog](examples/index.md) |

The **Concepts** pages explain individual mechanisms in more depth. **Guides and
Recipes** help with particular changes, and **Reference** pages are for lookup.
Under **Examples**, the catalog contains commands you can run, the gallery shows
generated output, and **Used in practice** explains fixed-revision excerpts from
larger applications. Those excerpts are optional reading, not extra packages
needed for the first tutorial.

## Version and example scope

**Development documentation — 0.1.0 candidate, CPython 3.12+.** Exact executed
example environments and remaining limits are recorded in
[compatibility](reference/compatibility.md). Packaging and publication are
separate gates. The current tutorial uses the explicit Python backend.
