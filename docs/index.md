# Build a Python generator with YIDL

YIDL turns **definitions and facts into Python code**. Define the records your
generator needs, reusable Astichi resources, rules that select those resources,
and assembly instructions that bind and insert them. The result can be a plain
slotted class with direct field stores.

**Development documentation — 0.1.0 candidate, qualified 2026-10-23.** This site
teaches the current braced concept/DDS/assembly compiler. The initial release plan
has been reviewed; packaging and publication are separate gates. Start with the
explicit Python backend and installation route below. Other configurations need
their own qualification.

[Generate your first class](start/first-generator.md){ .md-button .md-button--primary }
[Install the candidate](start/install.md){ .md-button }
[Language reference](reference/language.md){ .md-button }

## What you will build

The first tutorial creates `Point(3, 4)`, whose `x` and `y` are direct slots:

{{source:tests/data/goldens/materialized/documentation_classes/first_model.py|python}}

The displayed source is extracted from the canonical executable example. Its
assertions check values, signature order, direct stores and absence of an instance
dictionary. Source snapshots help inspection; behavior assertions establish the
intended result.

## Choose a route

| You want to… | Read |
| --- | --- |
| Build something useful first | [First generator](start/first-generator.md) |
| Understand concepts, facts and generated objects | [The model](concepts/model.md) |
| Follow a property into a generated parameter | [Matching and data flow](guides/matching-and-data-flow.md) |
| Extend a generator | [Inheritance and specialization](concepts/composition.md) |
| Diagnose generation | [Debugging assembly](guides/debugging-assembly.md) |
| Find exact contracts | [APIs](reference/apis-and-cli.md), [compatibility](reference/compatibility.md) |
| Run or inspect examples | [Example catalog](examples/index.md) |

YIDL is the generic compiler. Lifecycle, Dataclass and Undoable are consumers that
supply their own object-model policy. Astichi owns Python stitching and hygiene.
Do not infer transaction, factory-injection or dataclass semantics from a generic
YIDL collection. [Consumer examples](examples/consumers.md) show the boundary.
