# Matcher contracts

YIDL has **generic resource matchers** over DDS inputs and **contribution
matchers** for assembly. Do not assume every expression/visibility rule is shared.

## Generic DDS matchers

Declare inputs in tuple order with `matcher.input("field", collection)`. Use
`input.prop(property)` to distinguish the same semantic property on different
inputs. Rules contain equality conditions; their extracted tuple schema consists
of referenced property/evaluated fields, not entire records.

Rules run in descending score. The default score is specificity (condition count)
scaled by weight. A default resource is used only when no rule matches.
No matching rule and no default yields no result. Equal-score overlapping rules
are rejected before runtime; contradictory constraints can make same-score rules
disjoint and legal. Use named rules and inspect `.rule`/`.score` when debugging.

`evaluated_field(name, inputs=(left, right), value=callable, value_type=...)`
adds a derived tuple entry. Its callable receives declared inputs in that order.
The in-memory API can accept a callable; emitted source requires an explicitly
named generated/importable evaluator. A closure that happens to work in memory
is not automatically source-emittable.

`MatcherResult` holds `resource`, `rule`, `score`, original concrete `records`
and extracted `values`. Matcher-result productions use `match.record("input")`
for the former and positional `match.value(index)` for the latter. Unknown input
names and out-of-range indices reject at definition time.

## Contribution selection

Contribution matchers select named contributions, not arbitrary resources.
Their input/context stack exposes semantic property names used by conditions and
bindings. Duplicate visible names are diagnosed; do not invent qualified syntax
from the DDS Python API. The tutorial deliberately uses ClassId and Owner to
avoid that collision.

Inherited rule names/defaults are checked during concept composition. Keep the
inherited default and add distinctly named weighted rules to specialize. A
conflicting default is not a Python override.

## Enumerating versus looking up

Multiple collection inputs enumerate combinations; relation filters such as
`Owner == ClassId` select relevant pairs. Empty inputs yield no combinations.
Use identity lookup when the requirement is retrieving one keyed row. Computed
views filter existing rows. See the [M01–M10 walkthrough](../guides/matching-and-data-flow.md)
for ownership, evaluated fields, projection and emitted parameter order.

Evidence: `test_matcher.py`, `test_data_matcher_productions.py`, contribution
diagnostics and canonical multi-source/matcher-production fixtures. These were
executed under the qualified Python tuple; native selection is a separate claim.
