# Runnable example catalog

**Choose one example for your next task.** These are independent recipes, not a
sequence of required exercises. For your first visit, follow the
[four-page learning path](../index.md#new-to-yidl-start-here) before using this catalog.

Run from the YIDL repository root with the [installed environment](../start/install.md).
All commands below use `ASTICHI_LOWER_ENGINE=python`; outputs go under ignored
`build/`. Existing canonical fixtures use their own assertions and one explicit
output argument. They do not require neighboring consumer checkouts.

| Example | Command argument after the Python interpreter | Expected outcome |
| --- | --- | --- |
| First class | `example/documentation/generate.py --out build/first` | Point(3,4), signature x/y, direct slots |
| Two owners | `example/documentation/generate.py --extended --out build/extended` | Point(x,y), Size(x), hidden/orphan filtered |
| Zero fields | `example/documentation/generate.py --empty --out build/empty` | Empty slots, callable zero-parameter init |
| Omitted init | `example/documentation/generate.py --disabled --out build/disabled` | No generated init in class dictionary |
| Independent captures | `example/documentation/captures.py` | Hostile-repr object identity and callback isolation |
| Compound constructs | `example/documentation/control_flow.py` | Ordered insertion under if/loop/with/try, zero/one/many actions |
| Raw comparison | `example/documentation/comparison.py` | Three operands, raw false/final results, short circuit and empty case |
| Logical imports | `tests/data/gold_src/yidl_imported_concepts.py build/imports.py` | Inherited plain/managed schema variants |
| Two-source filtering | `tests/data/gold_src/yidl_update_a_multi_source_from.py build/multi.py` | Two selected owner entries, ignored row excluded |
| Composite lookup | `tests/data/gold_src/dds_composite_identity_lookup.py build/lookup.py` | Composite identities projected to produced facts |
| Matcher projection | `tests/data/gold_src/dds_matcher_productions.py build/projection.py` | Original record and extracted tuple values distinguished |
| Callable facts | `tests/data/gold_src/dds_lifecycle_callable_facts.py build/callables.py` | Consumer-specific signature facts via operation |
| Template edges | `tests/data/gold_src/yidl_lark_v2_vertical.py build/vertical` | Resource selection and evaluated template edges |

The new tutorial's one source contains the behavior assertions. Its canonical
fixture snapshots final model source for inspection. Existing fixtures similarly
validate behavior before writing output. The displayed site includes source
extracted from those authorities; it does not maintain parallel executable code.

The installed standalone examples were run with CPython 3.12.12 / YIDL 0.1.0
candidate / Astichi 1.1.3. The broad repository suite also checks its source
contracts. Other versions/backends are [qualified separately](../reference/compatibility.md).

[Generated gallery](generated-gallery.md) · [Real consumer excerpts](consumers.md)
