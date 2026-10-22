# Expressions, comparison and evaluation order

Choose output shape from the required behavior. Tuple comparison evaluates its
operands differently from a sequence of short-circuit field comparisons. A
passing integer equality example does not establish callback or raw-result
semantics.

For a field-wise short-circuit algorithm, the intended Python sketch is:

```python
result = left.first == right.first
if not result:
    return result
return left.last == right.last
```

This sketch preserves a falsey non-bool intermediate object and returns the final
comparison result without an additional truth conversion. Actual resources must
bind direct read paths, preserve deliberate cross-scope locals and order the
contributions. Empty operands require an explicit consumer policy. Python minor
versions can change the dataclass reference algorithm; do not assume one shape
matches every minor.

## Status of the recorded nested chain

The inventory's nested indexed expression arrangement failed with `term_path`,
`next_term` and native-materialization symptoms. Its general cause remains
unresolved. A flat ordered alternative passed a bounded Dataclass differential
corpus; this does not prove the nested mechanism broken or the alternative
universally equivalent. No new nested-chain support is claimed here.

Bare statement-form `astichi_ref` is value-only and was rejected in the recorded
case. The consumer's static expression carrier (`read if True else None`) is a
bounded observed alternative. Its precise backend and overhead properties must
be qualified separately; `astichi_funcargs` is not automatically a scalar tuple
carrier.

Use collection/port ordering and explicit build indices; do not rely on fact
insertion for semantic evaluation order. Before promoting a new expression recipe,
check falsey non-bool results, the final raw object, nonreflexive/shared operands,
getter traces and callback counts. [Consumer excerpts](../examples/consumers.md)
link the qualified comparison authority. [Compatibility](../reference/compatibility.md)
keeps unresolved cases visible.

## Executable flat three-operand recipe

This new standalone recipe assembles two guarded intermediate comparisons and
one final direct return. It checks falsey non-bool identity, callback order,
truth-conversion counts, a shared/nonreflexive input and zero operands. It is a
bounded algorithm of its own, not an assertion of dataclass equivalence across
Python minors. It does not explain or fix the original D17 nested chain.

{{source:example/documentation/comparison.py|python}}

{{source:tests/data/goldens/materialized/documentation_classes/comparison_model.py|python}}
