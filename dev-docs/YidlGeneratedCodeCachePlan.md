# YIDL Generated Code Cache Plan

Status: implementation plan accepted by the operator, including the amended
development invalidation policy; another review cycle was explicitly waived.
No runtime implementation or default activation is accepted. Initial consumer:
YIDL Lifecycle; reuse proof: an independent standard-library-only test producer.
Existing generation and runtime semantics remain authoritative.

Implementation checkpoint: the standalone shared cache and Lifecycle's initial opt-in
adapter are implemented in the isolated GWZ lane, including fresh-process
reuse tests. The operator subsequently directed default-on automatic placement,
specified in the separately dual-reviewed
[location policy](../../yidl-cache/dev-docs/CacheLocationPolicyPlan.md).
That policy supersedes this plan's initial opt-in clauses for Lifecycle only;
shared-cache activation stays explicit and YIDL core stays independent.
Implementation remains uncommitted. See
[Lifecycle integration](../../yidl-lifecycle/dev-docs/LifecycleCodeCache.md) and
[shared-cache evidence](../../yidl-cache/dev-docs/SharedCacheCheckpoint.md).
Representative non-GUI startup measurements are now recorded in
[Lifecycle startup evidence](../../yidl-lifecycle/dev-docs/LifecycleCodeCacheStartup.md):
five fresh-process samples per configuration, with thirteen warm hits and no
generation. The normal-context median falls from 1.346 to 0.175 seconds; Tk
six-control startup falls from 1.781 to 0.256 seconds. These local Python
3.14/macOS measurements include cache setup and do not cover GUI/render latency.
Implementation review and cross-platform approval remain pending;
implementation and performance evidence do not supersede those gates.

Operator packaging amendment: the shared cache belongs in a standalone
`yidl-cache` repository and Python distribution, imported as `yidl_cache`.
This supersedes the original proposal to ship it inside the YIDL distribution.
The amendment changes ownership and packaging, not generation or cache semantics;
this plan edit does not create the repository or activate caching.

Operator dependency amendment: YIDL core must not depend on or invoke
`yidl-cache`. Its data-record generation is no longer an integration target in
this plan. Generator applications may use YIDL and the cache independently;
their adapters, not YIDL core, connect the two.

Operator amendment: timestamp-and-size dependency invalidation is selected,
including editable installations. This supersedes the immutable-provenance
restriction reviewed at `1731f1de64422463356201aa65b4925b97b752c9`.
Earlier reports remain historical evidence, not approval of this amendment.
The operator explicitly accepted this amendment without another review cycle.

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

The standalone `yidl-cache` project owns the reusable code-artifact cache.
Lifecycle owns the adapter that determines its generation inputs and binds its
current class. Other generator applications provide their own adapters; the
cache does not know field kinds, transaction semantics, data-record properties,
or Pyrolyze internals. It is not a cache of arbitrary decorator results or live
classes.

The import surface is a lightweight `yidl_cache` package in its own Python
distribution. Its runtime implementation depends only on the standard library;
it must not import or depend on YIDL, Astichi, YIDL Lifecycle, or Pyrolyze.
Retrieving an entry therefore cannot import `yidl.__init__`, the parser, or
generator resources through the cache package. Consumer adapters must also keep
their expensive generation imports deferred until a miss.

Dependency direction is consumer to cache:

```text
yidl-lifecycle -> yidl-cache
future code-generating consumers -> yidl-cache
```

Lifecycle separately depends on YIDL for generation. There is no dependency
edge in either direction between YIDL core and `yidl-cache`. No YIDL runtime,
compiler, or dependency-metadata change is required for this integration.

Each consumer declares an explicit runtime dependency when its integration
lands. Installing the cache package does not enable caching; initial integrations
remain consumer-owned. Lifecycle's default-on amendment is linked above; it does
not set other consumers' defaults. A future YIDL FastAPI or other generator can supply the same
request and deferred code-producing callback without adding domain-specific
behavior to the cache. Additional production integrations are not part of this
plan.

Create a sibling `yidl-cache` member in the isolated GWZ lane through GWZ
membership operations before implementing the shared cache; do not manually
edit workspace configuration. Give it independent project instructions,
`pyproject.toml`, README, `src/yidl_cache/`, and tests. The independent repository
and distribution must build, install, and test without neighboring checkouts.
Verify its wheel and source distribution separately, then verify consumer
dependency installation and imports. Repository creation is an implementation
preflight, not an action performed by approving this document edit.

Keep storage, format validation, and neutral request/result carriers cohesive.
Handwritten carriers should be frozen dataclasses; do not use enums or string
status tags. Keep lifecycle-specific concrete adapters in `yidl-lifecycle`.
Future standalone data-class or FastAPI generator applications would own their
own adapters. Consumers supply their dependency inventories and generation
fingerprints; the cache may provide neutral inventory mechanics but must not
hard-code consumer package names or discover their generation schemas. Execution,
namespaces, validation, and live-value binding remain entirely consumer-owned.

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
generation dependency revision, not only its package version. Editable and
ordinary installations may cache. For generator code, templates, and native
dependencies, use a deterministic inventory of file modification timestamps and
sizes, plus an explicit generator/cache revision. Stat dependencies once when
establishing the process identity, not once per field or decorated class. This
is a Python-style practical invalidation policy, not exact content identity.

Timestamp-and-size-preserving edits may reuse stale entries. This limitation is
explicitly accepted for development; document a cache-clear/disable mechanism
and restarting the process after generator changes. Definition fingerprints
still include normalized generation inputs, not only source-file metadata.
Bytecode compatibility and private-cache trust checks remain required.

Do not silently relabel already-loaded generators using later disk metadata.
Supported operation assumes generator dependencies stay unchanged during a
process, as with ordinary imported Python modules. No automatic hot reload is
promised. Before publishing a miss, recheck the dependency inventory once; an
observed change disables persistent use for that producer for the remainder of
the process, while normal uncached generation continues. Missing dependencies
also bypass caching. Changes that occur and restore identical metadata between
checks are an accepted limitation, not a strict race-safety guarantee.

Tests must cover fresh-process invalidation after ordinary edits and detected
changes around deferred imports. A warm hit must not import expensive templates
to construct its identity. No per-class whole-dependency scan is permitted.

On a valid hit, deserialize code. On a miss, call the producer, then store its
code if cacheable. Disabled, unavailable, incompatible, or unusable cache storage
must not prevent normal generation. Cache failures cannot swallow generation,
execution, class-binding, or definition-validation errors. Those remain ordinary
producer errors with the current diagnostic boundaries.

## Producer fingerprints and runtime binding

Before implementation, audit every input actually consumed by each producer's
generation path. Maintain a dependency table distinguishing embedded code,
generation-time branch decisions, and runtime builder arguments. A source-file
timestamp or class name alone does not represent definition-generation inputs;
dependency invalidation uses the separately accepted timestamp-and-size policy.

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

1. **Repository preflight, input audit and contract proof.** Establish the
   independent `yidl-cache` repository/distribution and GWZ membership in the
   isolated lane without changing the active LCM workspace. Record
   generation-versus-binding dependency tables for Lifecycle and the independent
   test producer. Keep the existing `src/yidl/generation/data_schema.py` audit as
   read-only reference, not a requirement to integrate caching into YIDL core.
   Pin baseline latency and generated behavior. Resolve unsupported inputs and
   trust policy before broad caching.
2. **Shared artifact cache.** Implement `src/yidl_cache/` in the standalone
   repository: request identity, compatibility envelope, deferred compilation,
   atomic publication, bypass and diagnostics. Prove fresh-process hits avoid the
   producer callback. Test format
   failures, disabled/unwritable storage, concurrency, reentry, and independent
   wheel/source-distribution packaging. In an isolated installation with no
   consumers present, prove the cache imports and works without YIDL, Astichi,
   Lifecycle, or Pyrolyze. Cache tests belong in `yidl-cache`; they do not require
   those projects or their generator fixtures.
3. **Lifecycle opt-in integration.** Integrate after harvesting and before AST
   generation/compilation. Preserve the existing execution and binding stages.
   Add Lifecycle's explicit dependency and keep its fingerprint/compile adapter
   in the Lifecycle repository, not in `yidl-cache`.
   Use canonical lifecycle golden/integration fixtures to compare hit and miss
   behavior, not a second handwritten lifecycle implementation.
4. **Independent-producer proof.** Exercise a small standard-library-only
   generated plain-record example in `yidl-cache` tests through the same contract
   with its own namespace/fingerprint and fresh execution namespace. Its deferred
   callback builds and compiles a structural AST; it does not import YIDL,
   Astichi, or Lifecycle. Use a canonical fixture to prove code reuse, fresh
   classes, binding, and cross-producer isolation. This is a test consumer, not
   a new production decorator framework or a claim of a second production
   integration. Do not modify YIDL's data-record generation or package metadata.
5. **Performance and invalidation acceptance.** Run fresh processes with empty,
   warm, and disabled caches. Report at least five unprofiled repetitions,
   medians and spread, generation callback counts, phase times, cache size, and
   import overhead. Compare the real thirteen-class startup path without GUI
   creation, then check the relevant application separately. Keep profiler runs
   separate from latency benchmarks.
6. **Review and default policy.** Run the standalone cache suite, relevant YIDL
   and Lifecycle suites, and the supported Python/backend matrix. Review
   fingerprint completeness, trust,
   failures, and packaging before default activation. Commit accepted checkpoints
   only when requested; this plan does not authorize implementation or pushing.
   Validate cache and Lifecycle distributions and dependency direction, including
   YIDL core's continued independence from the cache. Independent cache
   releases and format revisions must not require synchronized consumer releases;
   unsupported cache formats are misses, not producer-generation failures.

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
| Observable dependency edit during a miss | Do not publish; disable persistent use for this producer until process restart. |
| Generator edited while already imported | No automatic hot reload; restart after edits, without relabeling the process identity from later disk metadata. |
| Editable checkout, unchanged timestamp/size inventory | Persistent hits are allowed; no blanket editable-install bypass. |
| Edit preserving timestamps and sizes | Document accepted stale-cache limitation and cache clearing; no guaranteed detection. |
| Malformed, truncated, corrupt, untrusted entry | Rejection/bypass before deserialization where applicable; normal generation. |
| Cache write failure or concurrent interrupted writer | Correct current result; no partial artifact becomes a valid hit. |
| User validation, generation, or binding exception | Original error propagates; no misleading cache-success report. |
| Definition reload or separate process | Fresh classes/namespaces; no retained callback or state from earlier execution. |
| Second generator namespace | Same storage mechanism; no accidental cross-producer reuse. |
| Standalone cache installation | Works with the standard library only; no consumer package or template import is required. |
| Consumer integration installation | Explicit cache dependency resolves; adapters remain consumer-owned; Lifecycle alone adopts the reviewed default-on policy. |
| YIDL core installation and execution | No dependency on, import of, or invocation of `yidl_cache` is introduced. |
| Increasing request count | Constant-time entry lookup plus bounded per-request fingerprint work; no quadratic scan. |

## References

- [YIDL coding rules](YidlCodingRules.md), especially dependency direction,
  generator architecture, and parser-free decorator execution.
- Lifecycle implementation: neighboring repository
  `../yidl-lifecycle/src/yidl_lifecycle/lifecycle.py` and
  `../yidl-lifecycle/src/yidl_lifecycle/lifecycle_harvester.py`.
- [Python code serialization and trust warning](https://docs.python.org/3.12/library/marshal.html).
- [Python bytecode magic](https://docs.python.org/3.12/library/importlib.html#importlib.util.MAGIC_NUMBER).
