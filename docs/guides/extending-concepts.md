# Extend a generator without copying its policy

First separate reusable mechanism from consumer facts. A neutral comparison
concept can own ordered operand surfaces. A consumer supplies its read paths,
selected fields, class metadata and comparison policy. Dataclass metadata should
not be required by a second consumer that only needs ordered reads.

Use exported concepts and explicit logical imports as in
[project layout](../start/project-layout.md). Add distinct names for consumer
productions and contributions. Preserve inherited matcher defaults and specialize
through distinctly named rules/weights. A duplicate production name or conflicting
default is an authoring error, not an override facility.

The tutorial itself separates the `ClassShell`, method production and field
contributions. You can add a method selection without replacing the entire class
emitter. The [composition reference](../concepts/composition.md) describes
extension boundaries; the current grammar also supports explicit production
phase extensions, which are separate from same-name replacement.

[Real consumer excerpts](../examples/consumers.md) identify neutral comparison
resources used by Dataclass and Undoable at fixed revisions. They are related
object-model examples, not evidence of unrelated-domain generality. Do not make
either checkout a prerequisite for the standalone tutorial. Reuse a packaged
resource with explicit authority, source-map keys and digests; generated bases
are derived artifacts, not the next author's editable source.

Before claiming an extension works, test a fallback case, a selected case and a
conflicting named declaration. Before removing a field, remove its local policy
with it and check remaining named consumers for a missing dependency. See the
[gallery](../examples/generated-gallery.md).
