# YIDL Generated Code Cache Plan

Status: proposed implementation plan. No cache implementation or new runtime
contract is accepted by this document. Initial consumer: YIDL Lifecycle;
second-consumer proof: YIDL data-record generation. Existing generation and
runtime semantics remain authoritative.

## Objective and evidence

Reuse compiled generated code across Python processes without persisting live
classes, state, namespaces, callbacks, factories, or transaction objects. Preserve
the direct AST-to-bytecode generation path and bind current runtime values after
loading cached code.

A warm Tk six-control startup probe in the neighboring Pyrolyze project measured
1.02 seconds, including 0.90 seconds generating ASTs for thirteen lifecycle
implementations. A separate profiler run attributed about 1.58 of 1.72 seconds
to the complete lifecycle decorator path. These are separate measurements;
profiler timings are not unprofiled latency estimates. Astichi's native engine
was active. The remaining cost is not Tk widget creation or a Python-engine
fallback.

Saving 0.7-0.85 seconds is a prototype target, not demonstrated performance.
Harvesting, fingerprinting, cache reads, imports, code execution, and final class
construction remain. Measure their costs independently before selecting default
policy or claiming that target.

## Ownership and package boundary

The YIDL project owns a small reusable code-artifact cache. Lifecycle owns the
adapter that determines its generation inputs and binds its current class.
Other YIDL generators provide their own adapters; the cache does not know field
kinds, transaction semantics, data-record properties, or Pyrolyze internals.

Proposed import surface: a lightweight `yidl_cache` package shipped with the
existing YIDL distribution. This avoids importing `yidl.__init__`, which
currently eagerly imports the parser, merely to read a cache entry. Verify wheel
and source-distribution inclusion explicitly. A separate distribution or new
repository is not required for the first checkpoint.

Keep storage, format validation, and neutral request/result carriers cohesive.
Handwritten carriers should be frozen dataclasses; do not use enums or string
status tags. Keep lifecycle-specific concrete adapters in `yidl-lifecycle`.
No changes to lifecycle markers, decorators, generated public APIs, transaction
completion, or Astichi's assembly semantics are in scope.

## Shared cache contract

A producer supplies an immutable request identifying its namespace, generation
revision, normalized input digest, and compilation context, plus a deferred
callback that returns compiled module code on a miss. The callback preserves
the producer's existing structural generation and compilation path. Crucially,
the request can be constructed without generating an AST or importing the
heavy generator templates.

The shared cache returns only a Python code object. It never executes it, owns
a class namespace, or stores a generated class. Neutral result types distinguish
a hit, a miss, and a deliberate bypass without changing producer behavior.
No callback receives a mutable cached AST.

The shared compatibility identity includes the cache-format revision, Python
implementation, bytecode magic/cache tag, supported interpreter version, and
optimization/compilation settings. Producer identity includes its complete
generation dependency revision, not only its package version. Source checkouts
must invalidate after unversioned generator or template edits. Compute shared
dependency hashes once per process, not once per field or cached class; a warm
hit must not load the expensive generated assembly module to obtain its hash.

On a valid hit, deserialize code. On a miss, call the producer, then store its
code if cacheable. Disabled, unavailable, incompatible, or unusable cache storage
must not prevent normal generation. Cache failures cannot swallow generation,
execution, class-binding, or definition-validation errors. Those remain ordinary
producer errors with the current diagnostic boundaries.

## Producer fingerprints and runtime binding

Before implementation, audit every input actually consumed by each producer's
generation path. Maintain a dependency table distinguishing embedded code,
generation-time branch decisions, and runtime builder arguments. A source-file
timestamp or class name alone is not a correct fingerprint.

For Lifecycle, audit `lifecycle.py`, `lifecycle_harvester.py`, the generated
lifecycle base, and its template dependencies in the Lifecycle repository.
Cover class/module/qualified names, inherited and overridden field layouts,
field order and kinds, initialization flags, storage/compare/mutability policies,
annotation-dependent shape decisions, transaction-group indices and ordering,
normalization/freeze/thaw presence, factory calling conventions, generated
parameter names, and transaction methods/hooks/validators. The audit must show
which values are embedded rather than assuming this list is complete.

Normalize an explicit schema of generation inputs. Do not hash arbitrary
`repr`, object addresses, invoke arbitrary user serialization, or use whole-class
pickling. Ordered data stays ordered; mappings are normalized only where order
is semantically irrelevant. Reject unknown input shapes from caching rather
than guessing. An explicitly uncacheable definition still generates normally.

Defaults, callback objects, factories, annotations, hooks, and transaction keys
may be excluded only when the audit proves they are supplied dynamically and
cannot affect generated code beyond already-keyed shape decisions. Group
relationships and generated indices remain keyed even when actual key objects
are bound later. Changed live values must be rebound on a hit, not retrieved
from old cache state. If an input affects both generation and binding, represent
its generation contribution explicitly and supply its live value separately.

Lifecycle's hit path executes the module code in a fresh namespace with the
current module identity, then calls `build_lifecycle_class` with the current
definition and freshly harvested `build_kwargs`. Harvesting and validation
still run. Preserve original module/qualified names, inheritance, fresh class
identity, diagnostics, and callback behavior across reloads and processes.

## Persistence, trust, and failure handling

Use Python's `marshal` to serialize only supported code objects. Wrap it in a
small, versioned envelope with the expected request identity, compatibility
metadata, declared payload length, and integrity digest. Validate bounded header
and payload sizes, exact length, compatibility, and integrity before unmarshalling;
then verify the decoded object is a code object. Do not rely on private
importlib bytecode-writer APIs or claim this is Python's automatic module cache.

The envelope is a cache format, not a custom bytecode instruction format.
Python owns the serialized code representation. No generated-source parsing is
introduced in decorator execution, and no AST is built merely to validate a hit.

Cache files are executable artifacts. Use an explicitly trusted per-user cache
location with restrictive access; define platform-specific trust checks before
enabling persistence there. Reject symlink/path-traversal surprises. A checksum
detects accidental corruption, not malicious replacement. Never unmarshal
untrusted entries. If trust cannot be established, bypass the persistent cache.

Publish one complete entry through a same-directory temporary file and atomic
replacement. A crash before replacement leaves the prior complete entry or a
miss. Readers do not wait for or consume partial entries. Concurrent misses may
generate redundantly, but writers must not corrupt or mix entries. Keep cache
I/O locks out of user generation/execution callbacks; test same-key reentry and
different-key recursion explicitly. Define ownership of temporary-file cleanup
and bounded behavior when replacement or cleanup fails.

Expose an explicit disable/configuration path, hit/miss/bypass counters, and
opt-in diagnostics without startup log spam. Do not silently fall back to a
shared insecure directory. Any in-process code cache must be bounded. No global
directory scans or pruning on each lookup; explicit maintenance can bound disk
retention separately. All-hit work should scale linearly in the number of
requests and fingerprint input size, not scan prior entries per request.

## Implementation checkpoints

1. **Input audit and contract proof.** Record generation-versus-binding dependency
   tables for Lifecycle and the existing data-record AST execution path in
   `src/yidl/generation/data_schema.py`. Pin baseline latency and generated
   behavior. Resolve unsupported inputs and trust policy before broad caching.
2. **Shared artifact cache.** Implement the lightweight package, request identity,
   compatibility envelope, deferred compilation, atomic publication, bypass and
   diagnostics. Prove fresh-process hits avoid the producer callback. Test format
   failures, disabled/unwritable storage, concurrency, reentry, and packaging.
3. **Lifecycle opt-in integration.** Integrate after harvesting and before AST
   generation/compilation. Preserve the existing execution and binding stages.
   Use canonical lifecycle golden/integration fixtures to compare hit and miss
   behavior, not a second handwritten lifecycle implementation.
4. **Second-consumer proof.** Exercise a representative generated data-record
   schema through the same cache with its own fingerprint and fresh namespace.
   Reuse current canonical fixture assertions. Do not broadly cache all data
   generators or change YIDL-generated classes into Python dataclasses.
5. **Performance and invalidation acceptance.** Run fresh processes with empty,
   warm, and disabled caches. Report at least five unprofiled repetitions,
   medians and spread, generation callback counts, phase times, cache size, and
   import overhead. Compare the real thirteen-class startup path without GUI
   creation, then check the relevant application separately. Keep profiler runs
   separate from latency benchmarks.
6. **Review and default policy.** Run relevant YIDL and Lifecycle suites and the
   supported Python/backend matrix. Review fingerprint completeness, trust,
   failures, and packaging before default activation. Commit accepted checkpoints
   only when requested; this plan does not authorize implementation or pushing.

Each behavioral checkpoint follows red/green/refactor. Use bespoke tests for
cache mechanics, diagnostics, and fault cases; use existing canonical/golden
coverage for successful generated behavior without duplicate success suites.

## Acceptance matrix

| Case | Required result |
| --- | --- |
| Fresh process, compatible warm entry | No AST generation/compilation callback; current class binds correctly. |
| Changed generation input or inherited layout | Miss and correct regeneration, even if the class name is unchanged. |
| Changed runtime-only default/factory/key | Safe code reuse only when proven independent; new live value is bound. |
| Changed generator/template or Python compatibility | Miss; no stale code execution or incompatible unmarshalling. |
| Malformed, truncated, corrupt, untrusted entry | Rejection/bypass before deserialization where applicable; normal generation. |
| Cache write failure or concurrent interrupted writer | Correct current result; no partial artifact becomes a valid hit. |
| User validation, generation, or binding exception | Original error propagates; no misleading cache-success report. |
| Definition reload or separate process | Fresh classes/namespaces; no retained callback or state from earlier execution. |
| Second generator namespace | Same storage mechanism; no accidental cross-producer reuse. |
| Increasing request count | Constant-time entry lookup plus bounded per-request fingerprint work; no quadratic scan. |

## References

- [YIDL coding rules](YidlCodingRules.md), especially dependency direction,
  generator architecture, and parser-free decorator execution.
- Lifecycle implementation: neighboring repository
  `../yidl-lifecycle/src/yidl_lifecycle/lifecycle.py` and
  `../yidl-lifecycle/src/yidl_lifecycle/lifecycle_harvester.py`.
- [Python code serialization and trust warning](https://docs.python.org/3.12/library/marshal.html).
- [Python bytecode magic](https://docs.python.org/3.12/library/importlib.html#importlib.util.MAGIC_NUMBER).
