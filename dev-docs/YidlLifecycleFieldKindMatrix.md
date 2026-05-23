# YIDL Lifecycle Field-Kind Matrix

This matrix records the lifecycle field semantics used by the current YIDL
transactional lifecycle path. It is intentionally descriptive rather than a new
design surface: later close-the-gap slices should update this document when a
field kind gains new behavior.

`tx_key` is the canonical name for the transaction partition key. The older
`tx_group` wording should not be reintroduced.

## Field Kinds

| Kind | Stored In State? | Constructor Parameter? | Settable After Construction? | Default / Factory Support | Retained Initvar Support | Transaction State | Facade Visibility | Factory Evaluation Timing | Commit / Rollback | Teardown / Close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `field` | Yes, as a plain state value. | Yes when `init=True`; otherwise initialized from default source. | Yes, non-transactional, through the default facade/property path. | Literal defaults and default factories, including parameterized factories from the Phase C dependency plan. | Factories can read retained initvars when the fact model exposes them. | None. | Default facade reads/writes the stored value; current/working facades do not add transaction meaning. | During construction unless a future lazy policy explicitly says otherwise. | No transaction participation. | No generated close behavior. |
| `initvar` | Not as a user-visible field. It may be retained in state as hidden construction/input data when another feature needs it later. | Yes when `init=True`; `init=False` requires a default source before it can be retained as a provider. | No facade setter or getter. | Literal defaults and default factories are allowed for provider values. | This is the source kind for retained initvar support. | None directly. | Not visible on facades. | During construction, or retained for later feature factories such as transient working defaults. | No transaction participation. | No generated close behavior. |
| `classvar` | No instance state. | No. | Class attribute semantics only. | Literal default is materialized on the generated common base / facade class; factories are not a normal instance field path. | Not applicable. | None. | Visible by normal class lookup, including `self.NAME` inside generated code. | At class generation time. | No transaction participation. | No generated close behavior. |
| `const` | Yes, as immutable instance state. | Yes when `init=True`; otherwise initialized from default source. | No. A post-construction write is a lifecycle error. | Literal defaults and default factories. | Factories can read retained initvars when available. | None. | Readable from facades; no generated setter. | During construction. | No transaction participation. | No generated close behavior. |
| `static` | Yes, as non-transactional instance state, usually with a sentinel for uninitialized/lazy state. | Usually no constructor parameter unless the marker requests one. | Yes, non-transactional. Static is not write-once in the close-gap model. | Literal defaults and factories; lazy first-read factory evaluation is allowed. | Factories can read retained initvars when available. | None. | Readable and writable through the default facade/property path. | Lazy first read when no explicit value has been assigned; otherwise construction/assignment supplies the value. | No transaction participation. | No generated close behavior. |
| `managed` | Yes, with current, working, and staged slots per managed field. | Yes when `init=True`; otherwise initialized from default source. | Default/working facade writes stage a working value when an active transaction is available. Current facade writes remain governed by the current setter policy. | Literal defaults, default factories, optional thaw/freeze conversion, and parameterized factory dependencies. | Factories and transaction-local helpers can use retained initvars when exposed. | Current / working / staged. | Default facade reads the visible value; current facade reads committed current; working facade reads working overlay with current fallback. | Construction initializes current; later working values may be thawed on access and frozen during commit prepare. | Commit prepare freezes/converts working to staged; commit moves staged to current; rollback clears working/staged for the token. | No generated close behavior yet. |
| `transient` | Yes, as transaction-local state and any retained provider data it needs. | Usually no user constructor parameter unless explicitly modeled as an init input. | Writes are transaction-local and enlist the object in the corresponding transaction. | Working-default factories are supported and may read `self`, current/working facades, and retained initvars. | Yes. Transient is the first user of retained initvars after construction. | Working transaction-local value; no committed current value. | Default/working facade access initializes/enlists the transient value for the active transaction. Current facade exposure is not meaningful. | Per transaction, on first access or first write for that transaction. | Commit and rollback clear the transaction-local value. Commit does not create a committed current value. | No generated close behavior. |
| `owned` | Yes, using the managed storage model in the narrowed YIDL implementation. | Same as `managed`. | Same as `managed`. | Same as `managed`, with a marker-level type expectation for binding-style objects where applicable. | Same as `managed`. | Same as `managed`. | Same as `managed`. | Same as `managed`. | Same as `managed`; no extra explicit reference-count protocol in the narrowed implementation. | No generated close behavior; Python references own cleanup for now. |
| `binding` | Yes, as a plain non-transactional binding value in the narrowed YIDL implementation. | Yes when `init=True`; otherwise initialized from default source. | Yes, non-transactional. | Literal defaults and default factories. | Factories can read retained initvars when available. | None. | Default facade reads/writes the binding value. | During construction unless a future lazy policy explicitly says otherwise. | No transaction participation in the narrowed implementation. | No generated close behavior; no explicit Pyro-style reference count yet. |
| `local_store` | Planned (Slice 5). Expected to be stored in state as non-transactional scratch. | Planned. Likely initialized from default source rather than required as a constructor input. | Planned as mutable non-transactional scratch. | Planned minimal literal/default-factory support. | Not planned for the first slice. | None. | Default facade only unless a later design exposes it elsewhere. | Planned during construction or first access, depending on the minimal implementation choice. | Planned to survive commit and rollback unchanged. | No close protocol in this plan; teardown remains deferred. |

## Transaction Infrastructure

`transaction_manager` is generated infrastructure, not a user field kind in this
plan.

- The generated constructor accepts `transaction_manager=None`.
- The generated state object stores `_y_transaction_manager`.
- Generated facade methods delegate `begin`, commit, rollback, validation, and
  hook dispatch to that manager-facing state machinery.
- Transaction keys are supplied as the generated `_Class_tx_keys` tuple, with
  `DEFAULT_TRANSACTION` first when present.
- The mapping from transaction key to transaction index is generated from that
  tuple and should be stable across inheritance: parent keys keep their indexes;
  child-only keys append in first-use order.

Infrastructure rows that would normally be field-specific are not applicable:
there is no user-facing constructor field marker, facade property, retained
initvar behavior, or close hook owned by `transaction_manager` itself.

## Maintenance Rule

Whenever a lifecycle slice changes storage, initialization, facade visibility,
or transaction behavior for a field kind, update this matrix in the same slice.
