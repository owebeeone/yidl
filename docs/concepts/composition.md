# Inheritance and specialization

An extending concept shares definitions; it does not use Python's method-override
rules. Give additions distinct semantic names and select replacements through
matchers when the inherited contract supports it.

| Declaration | Practical extension contract |
| --- | --- |
| Properties/records/collections | Reuse compatible definitions; incompatible shapes reject |
| Family/union | Add concrete variants through the existing family |
| Resource | Reuse authoritative resource; do not assume arbitrary same-name replacement |
| Composable production | Inherited names cannot be silently redefined; explicit phase extension is a separate surface |
| Contribution matcher | Add distinctly named weighted rules; conflicting default or duplicate rule rejects |
| Assembly | Export a named production build; an unexported production alone does not create every expected entrypoint |

For an inherited `ClassProduction`, define `ConsumerClassProduction` and a
matching contribution, then specialize the relevant selection rule. Reusing the
name yields `composable production 'ClassProduction' is already inherited`.
An inherited default is not an ordinary override: changing it can produce
`duplicate default`. Retain it and add a narrower rule with a distinct name and
appropriate weight.

The [split example](../start/project-layout.md) demonstrates compatible schema
extension. [Real consumers](../examples/consumers.md) demonstrate neutral
comparison reuse without claiming that the consumer's field policies are YIDL
semantics.

Generic DDS rules use condition specificity and weight; equal-score overlapping
conditions reject before execution. Contribution selection has its own evaluator
and visibility rules. Read [matchers](../reference/matchers.md) before transferring
assumptions between the two.

Resource reuse and build-instance reuse also differ. The same empty/pass resource
can serve several contributions, but each live insertion needs a noncolliding
build name/index. The tutorial uses `(ClassOrder, FieldOrder)` for field builds;
a field name alone is not a legal numeric build index.
