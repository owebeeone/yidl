# YIDL Runtime Class Model

This document is the normative design for the **generated class structure and
runtime model** created by YIDL.

It covers:

- physical stores
- logical facades/views
- proxy routing
- initialization sequencing
- commit/rollback structure
- native homing and evict-last behavior

See also:

- `docs/YIDLFrontendDesign.md`
- `docs/YIDLCodegenDesign.md`
- `docs/YIDLDesign.md` (historical reference only)

## 1. Core model

YIDL generates a multi-store / multi-facade class structure so method and field
access can be routed deterministically across current vs working state.

The generated object model should not depend on generic runtime descriptor
tables as its primary mechanism.

## 2. Physical stores

Stores hold the actual data. They contain memory/layout only, not business
logic.

Primary stores:

- **PublishedStore** — authoritative committed state
- **WorkingStore** — speculative transactional state
- **InstanceStore** — proxy-owned native/homed fields
- **HiddenStore** — init-only ephemeral storage such as InitVar-style values

The current intended implementation direction is that generated stores/classes
may use Python layout tools such as `__slots__` where the design calls for
them.

## 3. Logical facades

YIDL generates facade/view classes that inherit from the user base class so
user-defined methods resolve through the intended MRO.

Primary facades:

- **CurrentView** — reads committed/published state and enforces immutability
  rules where appropriate
- **WorkingView** — supports copy-on-read / thaw-on-read and routes writes into
  working state
- **Proxy** — main instantiated class that routes field access according to
  transaction state

## 4. Initialization model

Generated initialization follows the 3-phase rule:

1. allocate stores
2. wire views/facades and routing
3. unroll field initialization in declaration order

This ordering exists to make dependent default/default_factory behavior safe and
deterministic.

## 5. Commit / rollback model

Generated classes own explicit commit/rollback behavior rather than delegating
all write semantics to generic runtime tables.

The intended model includes:

- commit emission such as `_lc_commit`
- rollback emission
- transaction-group-aware behavior where required
- deterministic ordering for commit-sensitive features

## 5a. Transaction groups

YIDL supports named transaction keys as part of the generated runtime/class
model where helpers or hooks declare a `tx_key`.

The intended model is:

- each field, validator, order key, or hook belongs either to the default
  transaction key or to an explicitly named group
- begin/commit/rollback behavior is isolated per active group
- commit-sensitive features such as validators, order keys, and hooks execute
  within the semantics of their own group
- groups are separate by default; YIDL should not guess richer cross-group
  semantics that have not been made explicit
- if application code needs coordinated behavior across groups, the runtime may
  expose tools that let the application tie groups explicitly rather than
  inferring that policy automatically
- visibility rules across groups must be explicit; until further refined, the
  design should not assume implicit cross-group synchronization

The exact interaction between groups and cross-group reads remains an open
runtime-class-model issue, but `tx_key` itself is no longer an unowned design
concept.

### 5a.1 Transaction-group requirements

| Requirement area | Requirement |
|------------------|-------------|
| **Membership** | Fields, validators, order keys, and hooks may belong either to the default transaction key or to an explicitly named group. |
| **Activation** | Beginning a transaction for a named group activates transactional behavior for that group only; default-group behavior remains distinct unless explicitly included. |
| **Isolation** | Dirty tracking, validation, commit ordering, and rollback are defined per active transaction key. |
| **Default policy** | Transaction groups are separate by default; the design does not invent implicit coupling semantics across groups. |
| **Explicit tying** | If coordinated cross-group behavior is required, runtime tools may expose explicit mechanisms for application code to tie groups together rather than guessing that model automatically. |
| **Commit-sensitive execution** | Validators, order keys, and hooks execute within the semantics of their own transaction key rather than through one undifferentiated global pipeline. |
| **Visibility** | Cross-group visibility must be explicit. The design must not assume implicit synchronization or coherent reads across groups until that rule is written down. |
| **Rollback** | Rollback semantics are defined per group and must mirror the group’s own dirty/commit participation rather than acting as a global catch-all. |
| **Generated structure impact** | Generated classes/runtime support must carry enough group metadata to route writes, commit/rollback, validators, and hooks to the correct group. |
| **Open detail** | Cross-group reads and cross-group dependency rules remain open and must be specified before helpers that rely on them are treated as fully covered. |

## 6. Evict-last behavior

Binding/resource-sensitive updates require an evict-last sequence:

1. stage/increment new inbound references
2. update physical structures so the data tree is consistent
3. evict/decrement/close the orphaned value last

This ordering is part of runtime semantics, not an optimization detail.

## 7. Native homing

When a field is homed on the instance/proxy:

- the field may bypass published/working store indirection
- the field may be emitted directly into proxy layout
- views may delegate to the main instance for access

This is the intended home for LocalStore-style native performance behavior.

## 8. Runtime-class-model open issues

This document still needs continued clarification for:

- transaction-group visibility rules across groups
- exact ordering interaction among validators, hooks, order keys, and store
  writes
- initvar ordering against other field categories
- composed behavior when multiple field kinds interact

Those are runtime/class-model issues even when frontend or codegen changes are
also needed.
