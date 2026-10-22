# Share one authoritative resource

Keep one authored `.yidl` asset authoritative. Consumers import it under stable
logical keys and specialize through exported concepts/matchers. Avoid copying
editable resource text into every generated base.

The [two-file example](../start/project-layout.md) is the minimal import recipe.
For a distributable resource package:

1. Include the authoritative `.yidl` files in both wheel and sdist.
2. Read assets with `importlib.resources`, independently of the working directory.
3. Build a source map whose relative imports resolve within that map.
4. Record source digests and the qualified compiler/dependency versions.
5. Regenerate in check mode from a clean process; only explicit write mode
   updates a checked-in base.

If authority is absent, fail regeneration with the missing asset's logical name.
Do not silently substitute a neighbor checkout or a stale emitted module. If its
digest changes, treat the resulting generated diff as a review input, then run
behavior checks before refreshing goldens.

A runtime base can embed the selected source/resources. That does not prove that
the compiler, Astichi or YIDL runtime packages can be uninstalled; inspect its
imports and assembly-time calls. Separate build dependencies from generated
module runtime dependencies in your own package instructions.

Dataclass and Undoable now have consumer package/regeneration checkpoints. Their
qualified snippets are [reference examples](../examples/consumers.md), not
dependencies of this tutorial. This documentation run did not rebuild their
bases or edit their packages. A full two-consumer shared-resource wheel/sdist
reproduction remains separately qualified consumer evidence, not a new YIDL
package guarantee.
