# Debug an assembly failure

Find the first failing stage before changing the code. Preserve exception causes;
`failed to target 'stores'` can wrap an external-binding collision, not just an
absent hole.

## A repeatable inspection route

1. Re-run the smallest input in a new process with an explicit engine.
2. Print package versions/import origins and actual engine selection.
3. Inspect the source map and compiled concept's `contributions`, `assembly_edges`
   and `assemblies`. Check available generated `build_*` names.
4. Inspect concrete facts through `container.Fields.sequence()` and identities.
   Compare owner and selection values before considering generated Python.
5. Inspect selected rule/resource and, for generic DDS, `MatcherResult.records`,
   `.values`, `.rule`, `.score` and `matcher.tuple_schema`.
6. Check contribution build name/index/order, its evaluated binding and target.
7. Save emitted library and final AST source; compile and execute only after
   remaining demands are resolved. Run independent behavior assertions.

For scoped path diagnosis, the current implementation exposes `DataStack`,
`path_selector_tuple` and `render_path_selector` in `assembly_runtime`. These are
low-level diagnostic helpers, not a promised tracing CLI. The canonical
`yidl_update_a_scope_paths.py` fixture demonstrates them without executing a
consumer application.

## Three distinct failures

**Missing binding:** a selected template still has an identifier/external demand.
Trace the property supplying it; a `keep` cannot provide a missing value.

**Duplicate build identity:** two selected contributions share a name/index.
Share the resource but distinguish live insertion identities. In the tutorial,
`(ClassOrder, FieldOrder)` keeps Point.x and Size.x distinct.

**Missing target:** the target instance or hole was never built, or its root
mapping/index is different. Verify selection and production order before
changing the path. A syntactically valid path need not resolve to a live build.

The [symptom index](../troubleshooting/index.md) gives specific remedies. Narrow
original nested-expression failures separately; passing a flat arrangement does
not identify their cause. Report confirmed out-of-scope compiler defects with a
minimal reproducer, impact and whether they block the documented supported route.
