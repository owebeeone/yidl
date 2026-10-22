# From declarations to Python

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

The first tutorial follows every stage explicitly. Data-producing operations run
before freeze; composable production runs after facts exist. A generic matcher
result carries original records and a positional extracted-value tuple. Those
are distinct inputs to later productions.

`MatcherGeneratedValue.to_generator()` lazily compiles an authored template and
caches its unbound composable. It does not cache a completed `Point` class or the
value of `Point.x`. Final `compile(ast, filename, "exec")` compiles already
materialized AST, not a fresh method string.

The implementation direction protects generated decorator/helper execution from
ad hoc Python parsing and per-field source compilation. The existing supported
source-template route still performs definition/build-time parsing and lazy
wrapper compilation. Do not promise that every generation stage is parser-free
or Rust-owned. See [caching](../reference/caching-and-performance.md).

When `Assignment` fails to target `stores`, inspect the chained exception and
both binding and destination. A target symptom alone cannot tell whether the
hole is absent, the selected instance is wrong, or its external binding collided.
