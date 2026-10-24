# Used in practice: qualified consumer excerpts

**Optional reading after the [standalone tutorial](../start/first-generator.md).**
These larger applications show how the same mechanisms are used in practice.
You do not need to install or build these packages to complete the tutorial;
use the [example catalog](index.md) for examples you can run in YIDL itself.

For using the current standalone libraries, start with
[Lifecycle installation and transactions](https://github.com/owebeeone/yidl-lifecycle/blob/main/docs/GettingStarted.md)
or [Cache installation and its consumer example](https://github.com/owebeeone/yidl-cache/blob/main/README.md).
Those guides describe their own package boundaries; the excerpts below remain
historical, revision-pinned evidence.

These are fixed-revision excerpts of consumer-authored resources, facts and
canonical generated output. They are attributed to their owning repositories;
this documentation does not select or change a license. The snapshots include
source/excerpt hashes and links. Building this site needs no consumer checkout.
They explain generic mechanisms alongside the runnable standalone tutorial.

**Qualification boundary:** Dataclass `202b01c` and Undoable `ca68b82` have accepted
local functional/package checkpoints and original SDK-wheel evidence. Separately
recorded Mac Python functional reruns passed 259 tests/3 skips and 350 tests,
respectively. Those source/workspace runs are not a new installed-package
qualification by this documentation task. Lifecycle `ee5ba63` is the pre-annotation-
fix baseline; native core behavior passed in the separate operational run, while
Python had a known owned-field source-hygiene golden mismatch. This page does not
claim all consumer tests pass or live-type annotations work. Source links below
identify exact authority rather than mutable working-tree bytes.

## Dataclass: facts to constructor parameters

Requirement: generate a direct-slot constructor with a required count and
captured defaults, keeping parameter order separate from field processing order.
The consumer harvester creates `DataclassField` facts containing FieldName,
AnnotationName, default/factory flags and ParamOrder:

{{consumer:dataclass_facts|python}}

A required field has IncludeParam true, KwOnly/HasDefault/HasFactory false, so
`ParamContributions.required` selects RequiredParamContribution. A defaulted field
selects the distinct defaulted rule. Annotation/default values are **identifier
names of captures**, not serialized live Python objects:

{{consumer:dataclass_rules|text}}
{{consumer:dataclass_resources|text}}
{{consumer:dataclass_binding|text}}

The target is the nested `/InitMethod` parameter hole. ParamOrder sets parameter
order; FieldOrder independently sets store order. Here is actual CPython 3.12
canonical output and the author's behavior assertions:

{{consumer:dataclass_output|python}}
{{consumer:dataclass_behavior|python}}

The same generic flow is explained without consumer metadata by the
[two-owner tutorial](../guides/matching-and-data-flow.md). Dataclass's richer
factory/provider/policy semantics remain consumer-owned. Its fixed-revision
[`dataclass_field_removal` fixture](https://github.com/owebeeone/yidl-dataclass/tree/202b01c879eb0ffb724158efe783b379fe522031/tests/data/goldens/materialized/dataclass_field_removal)
contains before/after removal and retained-reference checks; its
[`comparison_neutral` fixture](https://github.com/owebeeone/yidl-dataclass/tree/202b01c879eb0ffb724158efe783b379fe522031/tests/data/goldens/materialized/comparison_neutral)
illustrates read specialization without Dataclass field metadata.

## Undoable: select transactional access resources

Requirement: a managed field uses Undoable's history-aware read/write protocol.
The normalized schema supplies a concrete field variant; build facts preserve
FieldName and FieldOrder. A computed ManagedFields view filters FieldKind, then
the default matcher selects the accessor contribution:

{{consumer:undoable_facts|python}}
{{consumer:undoable_resource|text}}

The contribution binds three public identifier spellings (getter, setter target,
setter) and a literal field-name argument, orders by FieldOrder and targets the
class properties surface. Actual generated output calls the consumer's protocol:

{{consumer:undoable_output|python}}
{{consumer:undoable_behavior|python}}

The generic mechanism is resource selection/binding/insertion. Undo history,
transaction requirements and thaw/freeze policy belong to Undoable. This is a
related object-model consumer, not independent evidence of unrelated-domain
applicability.

## Lifecycle: property paths from produced facts

Requirement: a default facade reads working storage when present and otherwise
current storage. A generated analysis operation produces IndexedTransactionalField
records with CurrentSlotName, WorkingSlotName and TxIndex. The selected matcher
uses those records; the contribution binds identifier names and storage paths:

{{consumer:lifecycle_rule|text}}
{{consumer:lifecycle_binding|text}}
{{consumer:lifecycle_resource|text}}

This is compiler resource source, including consumer-owned internal naming. Its
actual output specializes the paths and transaction index:

{{consumer:lifecycle_output|python}}

The full fixed-revision
[`phase_f_hooks` canonical fixture](https://github.com/owebeeone/yidl-lifecycle/tree/ee5ba633efdeac9fbdd74cfe67ecd975eab8a26d/tests/data/goldens/materialized/yidl_transactional_phase_f_hooks)
and
[callable-fact resource](https://github.com/owebeeone/yidl-lifecycle/blob/ee5ba633efdeac9fbdd74cfe67ecd975eab8a26d/src/yidl_lifecycle/yidl/lifecycle_managed.yidl)
record the surrounding facts, captures, generated library and output. These
snippets are read-only explanatory evidence; the annotation fix in another task
is not incorporated. Generic DDS does not know what a transaction slot means.
