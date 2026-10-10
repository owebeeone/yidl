# Generated code cache input audit

Status: source audit completed; the standalone cache and opt-in Lifecycle adapter
are implemented in the isolated lane. Fresh-process tests prove compiled-builder
reuse and current-value binding. No representative application speedup is measured
yet. See [integration evidence](../../yidl-lifecycle/dev-docs/LifecycleCodeCache.md).
Policy: operator-selected timestamp-and-size dependency invalidation, including
editable checkouts. This is not an immutable-source or exact-content guarantee.

Scope amendment: the cache will be a standalone `yidl-cache` project. YIDL core
must remain independent of it. The data-record audit below is retained as
read-only reference; it no longer proposes a YIDL integration. The active reuse
proof is an independent standard-library-only test producer in the cache project.

Source baseline: YIDL `1731f1de64422463356201aa65b4925b97b752c9`, Lifecycle
`c2502f1a7a565624f20cf930fde92f581b123e9f`, Astichi
`1c47f781d3804130fdd61cbee07a3b2e4529158a`. The pending plan amendment is the
controlling policy. Paths below are relative to the repository owning each file.

## Lifecycle insertion boundary

`src/yidl_lifecycle/lifecycle.py:35` currently harvests, generates an executable
AST, compiles/executes it in a new namespace, then calls `build_lifecycle_class`
with the current decorated class and harvested builder arguments.

Cache lookup belongs after harvesting and before `_generate_lifecycle_ast`.
Harvesting and definition validation must run on every decoration. Only compiled
module code is reusable. Namespace execution and builder invocation stay fresh;
their failures retain the existing AST-execution and class-build diagnostics.
Generation failures on misses retain the AST-generation diagnostic.

`_build_lifecycle_container` passes class facts, field records filtered by their
generated slots, and transaction-method records to the generated assembly.
Fingerprinting must not import that generated module just to discover its slots.
Use an explicit producer schema covering harvested inputs; unknown schema keys
require bypass or a schema-version change, never silently ignoring them.

## Lifecycle input classification

| Input | Code-generation contribution | Cache treatment |
| --- | --- | --- |
| Class module, name, qualified ID, generated class names, class order | Names, assembly ownership, namespace/diagnostic identity | Include all class facts, including ordered lifecycle field names and builder parameter names. |
| Field ID, owner, name, order, kind | Record routing, generated storage and declaration order | Include all; preserve field order after inheritance and overrides. |
| Binding shape, comparison policy, mutable/init flags | Select emitted operations and branches | Include their normalized exact values. |
| Default/factory/working-factory presence and self-factory policy | Select parameter, assignment and evaluation paths | Include flags and parameter names. |
| Factory and working-factory parameter-name tuples | Dependency graph, evaluation order and emitted keyword arguments | Include ordered tuples; changing a callable signature can require a miss even if its object is rebound. |
| Actual defaults, default factories, working factories | Supplied through builder arguments, not literal default payloads | Exclude actual objects after retaining all presence/signature-derived facts; bind current objects on every execution. |
| Freeze/thaw presence and generated parameter names | Select conversion branches and references | Include presence/names and optional-None decisions. |
| Actual freeze/thaw functions | Builder parameters called at runtime | Exclude function identity/body; bind the current functions. |
| Annotation | Passed as an external assembly binding into generated constructor annotations; also drives binding shape and optional None | Include its emitted literal representation, not merely its derived shape. Initial cacheable case: exact string annotations. Other supported literal forms need explicit encoding; unknown live types bypass rather than use repr. |
| Value/current/working/staged slot names | Generated slotted layout and field access | Include all names, including empty names. |
| Transaction-key objects | Equality/hash grouping selects generated transaction indexes; objects also supplied live through builder arguments | Exclude object identity only after encoding the ordered key-equivalence/index structure. Include default-group membership, field assignments and method indexes. |
| Transaction method ID/owner/name/kind/declaration order/index | Hook routing and order, generated calls into decorated class | Include all except the live key object after encoding group topology. Method implementation remains on the current decorated class. |
| Decorated class, metadata mapping, annotations mapping, key tuple | Live arguments to builder; class bases and methods retained dynamically | Do not persist; rebuild from current harvesting. Their generation-relevant projections above still belong in the key. |

Conservative initial projection: retain every primitive/tuple class and field
fact except `default_value`, `default_factory`, `working_default_factory`,
`freeze`, `thaw`, and the live `tx_key_key`. Encode annotations separately and
replace keys with topology indexes. Apply equivalent treatment to method facts.
Use typed normalization so `False`, `0`, strings, absent values and empty tuples
do not accidentally share an encoding. Do not sort semantically ordered tuples.

Transaction topology needs both views, not an assumed single index map:
`lifecycle_harvester.py:65` accumulates inherited keys and fields, whereas
`yidl/lifecycle_managed.yidl:77` derives transaction facts by first appearance
in sorted fields starting with the default key. Include the harvested key tuple's
equivalence structure, field grouping and explicit method indexes so changes in
either derivation cannot collide. Do not serialize arbitrary key objects or run
an unrelated repr protocol. Normal harvesting already performs key validation.

Evidence: `lifecycle_harvester.py:44` harvesting/inheritance, `:196` class facts,
`:210` field facts, `:299` inherited remapping, `:359` method facts, `:462`
factory-signature projection, `:527` optional-None and binding shape. The authored
layers under `src/yidl_lifecycle/yidl/` show annotation external bindings,
builder-name references, factory dependency derivation and key indexing.

## Data-record reference audit (not an integration target)

`src/yidl/generation/data_schema.py:1672` materializes a record AST and executes
compiled module code. `RecordSpec.record_class` already memoizes the live class
inside one schema instance. The original proposal explored compiled-code reuse
across new instances and processes without replacing that instance-level
behavior; the revised plan does not change this YIDL path.

| Input | Generation effect | Cache treatment |
| --- | --- | --- |
| Record name | Class name, repr, diagnostics and bytecode filename | Include exact name. |
| Ordered properties | Slots, signature, assignments, validation and repr order | Include ordered property list. |
| Property public name and storage name | Property specs, annotations, identifiers and errors | Include both. |
| Required versus defaulted property | Selects property and constructor templates | Include sentinel as a distinct required marker. |
| Property default value | Embedded in both property-spec and constructor AST | Include typed literal value recursively; unlike Lifecycle, it is not purely rebound. |
| Value type | Builtin reference path and whether a runtime type check exists | Include supported builtin type path; `object` differs from other types. |
| Schema/system identity and existing live record class | Not read by the materialization loop for code emission | Do not persist either; execute cached code into the current fresh namespace. |

Current `_value_type_ref_path` rejects tuple types and non-builtin types. The
cache must not widen support or swallow those errors. Unsupported default
encodings bypass and follow normal materialization rather than inventing a key.
Astichi external literals support None, bool, int, float, str, tuple, list and
dict, with depth/cycle checks. Preserve sequence kinds and dictionary insertion
order. Float normalization must preserve distinctions such as signed zero;
non-finite values need explicit semantics or bypass.

Evidence: `data_schema.py:1684` materialization, `:1730` property emission,
`:1815` compilation/execution and `:1830` type constraints;
Astichi `src/astichi/model/external_values.py:16` literal conversion.

This reference path has an import-boundary cost: `data_schema.py:1560` builds
templates through Astichi during module import. Caching only
`_execute_record_class` is too late: AST materialization has already occurred.
Lookup must precede `_materialize_record_class`, and template initialization
would need lazy access to claim generation-free startup. This is audit evidence,
not authorization to change YIDL or add parser work to the cache.

## Dependency inventory and process policy

Definition fingerprints and file invalidation are separate. File identity uses
the accepted timestamp-and-size policy, not content hashing as a correctness
upgrade. Resolve inventory paths at runtime; never store machine-specific paths
in repository documents or generated sources. Namespace entries by producer and
explicit generator/cache revision, interpreter compatibility and compile options.

Lifecycle's inventory starts with its decorator/harvester/markers, generated
base and relevant transaction support. YIDL assembly depends on
`assembly_plan.py`, `assembly_runtime.py`, `matcher_values.py`, matcher/container
and data-schema support, reached through `data_def_sys.py`. Astichi Python
assembly, materialization and external-literal code plus its selected native
extension also affect emitted code. Do not key only the Lifecycle repository.

For the first implementation, a conservative inventory of installed source files
in these small producer/support packages plus selected native extension files
is preferable to a brittle handpicked transitive list. Enumerate/stat once per
producer process identity, not per field. Missing files bypass. Rechecking on
miss publication is cold-path work; warm lookup must not rescan a package or
import generated templates. Measure inventory setup separately.

Authored YIDL layers explain generation, but decorator execution consumes the
already generated base module. Regenerating that module changes its metadata
and invalidates the cache. Editing only authored YIDL without regeneration does
not change the current executable generator; cache behavior should not imply it
does. Installed revisions and explicit adapter version handle schema changes.

Ordinary operation assumes generator modules are not edited/hot-reloaded during
a process. Capture identity before deferred generation, keep it fixed, and do
not relabel already-imported generators with later stat results. An observed
change before publication suppresses writes and subsequent persistent use for
that producer until restart. Timestamp-preserving edits and edit/restore races
invisible between checks remain accepted development limitations.

## Required implementation probes

1. Same shape, different default/factory/converter objects: reuse Lifecycle code
   but bind the new live objects and preserve canonical behavior.
2. Change annotation text, factory parameter names, field kind/order, storage,
   comparison/mutability/optional flags, inherited overrides or hook order:
   require distinct definition keys and canonical outputs.
3. Replace equal-topology transaction objects: preserve fresh key identity;
   alter grouping/indexes: require a miss. Include inherited keys and methods.
4. Independent test producer: change an embedded literal or generated record
   layout: miss; identical generation inputs reuse code while new execution
   namespaces create fresh classes. Different producer namespaces must not share
   entries even when their normalized definition input is identical.
5. Fresh process after an ordinary dependency edit: invalidate. Observable edit
   during a miss: no publication. Timestamp-preserving edit: document caveat,
   not a guaranteed-detection test.
6. Warm hit: zero producer AST/materialization/compile calls; no heavy-template
   import for request construction. Test diagnostics on bypass and misses.
7. Check code objects contain no unsupported external runtime payloads before
   persistence; unknown encodings take the ordinary generation path.

The adapter's canonical fresh-process fixture and focused fingerprint/failure
checks now cover Lifecycle reuse, rebinding, topology, schema/annotation bypass,
and diagnostic boundaries. The standalone suite covers artifact trust and
invalidation mechanics. The original source audit itself remains historical
evidence, not a benchmark. Separate
[startup measurements](../../yidl-lifecycle/dev-docs/LifecycleCodeCacheStartup.md)
now demonstrate fresh-process savings on the real thirteen-class context path
and Tk six-control startup without GUI creation. Cross-platform approval,
application rendering verification, review, and default activation remain pending.
