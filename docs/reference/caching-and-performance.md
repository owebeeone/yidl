# Caches, ownership and performance

| Thing retained | Owner / lifetime | What it does not prove |
| --- | --- | --- |
| Unbound template composable | `MatcherGeneratedValue`, lazy `_generator` cache | Completed class caching or runtime value memoization |
| Frozen fact container | One generation's resolved data | Mutable build handles are safe to reuse |
| Materialized AST / compiled code | Consumer's explicit build result | A parser-free first generation |
| Completed class | Consumer namespace/cache if one is implemented | Independent captures without deliberate ownership |
| Runtime factory result | Generated object/consumer policy | Template caching runs or memoizes factories |

A wrapper's repeated `to_generator()` returns its cached template. Editing its
source file after import does not mutate that wrapper. Start a fresh process or
rebuild the authoritative library to pick up changes. Reuse unbound templates
through the SDK's supported composition operations; do not assume arbitrary
mutation, repeated materialization, failed native handle reuse or cross-engine
copy semantics are safe.

The new tutorial creates fresh schema/build/namespace state per variant. Existing
consumer capture probes verify bounded isolation of different defaults/callbacks;
this is not a general concurrency proof. Arbitrary object captures use private
identifiers and live namespaces, not literal serialization.

## Measure the property you need

Cold generation includes definition/source parsing and template compilation.
Repeated generation may reuse templates. Final AST compilation and class creation
are separate costs. Hot field reads/stores depend on generated code shape;
`self.x = x` can be direct even when the generator parses source at build time.
Memory depends on emitted layout and live object graphs.

No benchmark or performance ratio is claimed by these docs. Native selection
means a qualified composition backend; it does not assert that all analysis,
normalization, Python callbacks or final execution run in Rust. Verify actual
engine selection and dispatch before attributing a measurement.

Generated decorator/helper paths are intended to avoid fresh ad hoc parsing;
existing lazy wrapper compilation at the explicit compiler/build boundary is a
different interval. Improving dependencies or adding artifact caches requires
its own scope and evidence, rather than becoming a prerequisite for direct slots.
