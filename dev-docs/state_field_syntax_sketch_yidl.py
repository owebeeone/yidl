# YIDL state-field syntax sketch.
#
# This is a design specimen, not an input accepted by the current parser.
# It explores target-class + transducer syntax for:
#
# 1. State classes per field / per transaction key.
# 2. Functions on state classes.
# 3. Contributing functions to facade and transaction event stages.
# 4. Default exposure of fields on all facades.
# 5. Transaction as an introduced concept, not a root primitive.
#
# Naming note:
# - `@on.construct` means generated construction behavior.
# - field-spec `init=True/False` means whether a user constructor parameter is
#   exposed for a field. That is a separate concept and is not spelled
#   `@on.init` here.
# - `state_slot(default=...)` declares generated storage and its initial slot
#   value. It does not mean "expose this field in __init__".
#
# Composition note:
# - A target class declaration contributes global class facts: facades, facade
#   classes/capabilities, default exposure, and class-wide construction policy.
# - A transducer contributes field/helper facts: stores, event handlers,
#   facade bindings, invariants, and requirements against target facts.
# - A state-class method with an `@on...` marker is a stage contribution.
#   It may become an Astichi Composable during lowering, but the YIDL source
#   concept is "insert this behavior into this canonical pipeline stage", not
#   "inherit", "override", or "own the whole operation".
# - No contribution means no code is emitted for that stage. Dumb fields only
#   pay for the stages they use.
# - Multiple contributions in the same stage run by explicit `order=...`.
# - Contributions may have compile-time selectors with `.when(...)`. A
#   contribution whose selector is false for a field is not added to the
#   generated pipeline.
# - Construction is a staged pipeline: `construct.slots`,
#   `construct.init_values`, `construct.defaults`, `construct.factories`, then
#   `construct.required_checks`, then `construct.finish`.
#
# Parameter model note:
# - `parameters:` declares typed, normalized compile-time parameter objects for
#   a transducer expansion. A selector must read these objects; it must not
#   invent ad hoc flags like `field.has_default`.
# - `None` is a real field value. `UNSPECIFIED` means a spec parameter or
#   constructor argument was omitted.
# - Type expressions such as `T`, `T | None`, and callable signatures are
#   parameter data. They are not passive enum/string tags; parameter classes own
#   validation, selector helpers, and lowering behavior.
# - Constructor exposure is represented by an `InitParameter`, not by
#   `@on.construct`. `@on.construct...` only says when generated code runs.
# - Constructor signatures lower through Astichi parameter holes. The generated
#   constructor template owns a target such as
#   `_y_init_params__astichi_param_hole__`; each field that exposes an init
#   value contributes a `def astichi_params(*, field_name=...): pass` payload.
#   Prefer keyword-only field parameters. Literal defaults live directly in
#   the signature. Factory defaults and required values use `UNSPECIFIED`.
# - `InitialValuePlan` is not a generic runtime `if/elif` ladder. It resolves
#   to a concrete plan such as `InitDefaultValue`, `InitRequired`,
#   `InitFactoryFallback`, `HiddenDefaultValue`, `HiddenFactoryDefault`,
#   `HiddenUninitializedAllowed`, or `MissingInitialValueError`. Each plan
#   contributes only the parameter payload and construction snippet it needs.
# - Callable parameters lower to named callable runners before snippets run.
#   Snippets call those runners; Astichi lowering later turns runner refs into
#   scope-safe `astichi_pass(...)` / bind references.
# - Transducers compose by unifying compatible parameter objects by name and
#   rejecting incompatible declarations. A helper such as `managed` is the API
#   artifact that assembles the transducers and supplies their parameters.


# ---------------------------------------------------------------------------
# Target class facades and facade classes
# ---------------------------------------------------------------------------

target_class LifecycleTarget:
    facade Main(MainValueFacade, FieldExposingFacade)
    facade Current(CurrentValueFacade, FieldExposingFacade)
    facade Working(WorkingValueFacade, FieldExposingFacade)
    facade Transaction(TransactionServiceFacade)

    # Default field exposure. A field transducer can override this, but
    # unqualified "all facades" is not allowed: every broad target must name a
    # facade class/capability.
    exposure default:
        expose field on facades(FieldExposingFacade)


# ---------------------------------------------------------------------------
# Basic value storage
# ---------------------------------------------------------------------------

transducer ValueStorage:
    requires facades(FieldExposingFacade)

    parameters:
        field_name: FieldName = required()
        value_type: Type[T] = required()
        init_value: InitParameter[T] = constructor_parameter()
        default_value: ValueParameter[T] = optional_value()
        default_factory_runner: CallableRunner[T] = optional_callable(signature=DefaultFactory[T])
        initial_value: InitialValuePlan[T] = initial_value_plan(
            init_value,
            default_value,
            default_factory_runner,
        )

    state ValueStore per field:
        %%
        class ValueStore(Generic[T]):
            value: T = state_slot(default=VOID)

            @on.construct.slots(order=10)
            def construct_slot(self) -> None:
                self.value = VOID

            @on.construct.init_values(order=10).when(params.initial_value.constructor_value_always_bound)
            def construct_from_init_value(self, init_value: T) -> None:
                self.value = init_value

            @on.construct.init_values(order=20).when(params.initial_value.constructor_value_may_be_unspecified)
            def construct_from_optional_init_value(self, init_value: T | UnspecifiedType) -> None:
                if init_value is not UNSPECIFIED:
                    self.value = init_value

            @on.construct.defaults(order=10).when(params.initial_value.assigns_default_value)
            def construct_from_default(self, default_value: T) -> None:
                self.value = default_value

            @on.construct.factories(order=10).when(params.initial_value.calls_default_factory)
            def construct_from_default_factory(self) -> None:
                self.value = default_factory_runner()

            @on.construct.required_checks(order=10).when(params.initial_value.requires_runtime_value)
            def require_constructed_value(self) -> None:
                if self.value is VOID:
                    raise RuntimeError("field requires an initial value")

            @on.facades(FieldExposingFacade).get.resolve(order=10)
            def resolve_value(self) -> T:
                return self.value

            @on.facades(FieldExposingFacade).get.return_value(order=10)
            def return_value(self, resolved: T) -> T:
                return resolved

            @on.facades(FieldExposingFacade).set.assign(order=10)
            def assign_value(self, value: T) -> None:
                self.value = value
        %%


# ---------------------------------------------------------------------------
# Transaction group lifecycle concept
# ---------------------------------------------------------------------------

transducer TransactionGroupLifecycle:
    # This is not the runtime TransactionManager class. The runtime
    # TransactionManager already exists and drives begin/commit/rollback.
    #
    # This transducer is trying to accomplish these compile-time tasks:
    # 1. Introduce per-transaction-group state on the generated instance.
    # 2. Introduce transaction lifecycle events that runtime callbacks can
    #    target: tx.begin, tx.validate, tx.commit, and tx.rollback.
    # 3. Provide helper functions that field transducers can bind to, such as
    #    require_active().
    # 4. Define the bridge between user tx names, compile-time tx indexes, and
    #    runtime tx iteration ids.
    #
    # `requires` is a compile-time requirement against the target model. It is
    # not inheritance and does not create a runtime object by itself.
    requires facade(Transaction)
    requires facades(TransactionServiceFacade)

    parameters:
        tx_name: TxName = required()

    compile_state:
        # Stable compile-time id for this transaction key.
        tx_index: int = tx_index_for(tx_name)

    state TxKeyStore per tx_key:
        %%
        class TxKeyStore:
            current_tx_iteration_id: int = state_slot(default=VOID)
            begin_depth: int = state_slot(default=0)
            rollback_errors: list[BaseException] = state_slot(default_factory=list)

            @on.construct.slots(order=10)
            def construct_slot(self) -> None:
                self.current_tx_iteration_id = VOID
                self.begin_depth = 0
                self.rollback_errors = []

            @on.tx.begin
            def begin(self) -> None:
                if self.begin_depth == 0:
                    self.current_tx_iteration_id = next_tx_iteration_id()
                self.begin_depth += 1

            def require_active(self) -> int:
                if self.begin_depth <= 0 or self.current_tx_iteration_id is VOID:
                    raise RuntimeError("writes require an active transaction")
                return self.current_tx_iteration_id

            @on.tx.finish.apply(order=10)
            def finish(self) -> None:
                self.current_tx_iteration_id = VOID
                self.begin_depth = 0
                self.rollback_errors = []
        %%

    event tx.begin:
        source transaction_manager

    event tx.validate:
        source transaction_manager

    event tx.commit:
        source transaction_manager

    event tx.rollback:
        source transaction_manager


# ---------------------------------------------------------------------------
# Transactional working value
# ---------------------------------------------------------------------------

transducer TransactionalValue:
    depends TransactionGroupLifecycle
    requires facades(CurrentValueFacade)
    requires facades(MainValueFacade)
    requires facades(WorkingValueFacade)

    parameters:
        tx_name: TxName = required()
        init_value: InitParameter[T] = constructor_parameter()
        default_value: ValueParameter[T] = optional_value()
        default_factory_runner: CallableRunner[T] = optional_callable(signature=DefaultFactory[T])
        freeze_runner: CallableRunner[T] = optional_callable(signature=Freeze[T], default=identity_runner())
        thaw_runner: CallableRunner[T] = optional_callable(signature=Thaw[T], default=identity_runner())
        initial_value: InitialValuePlan[T] = initial_value_plan(
            init_value,
            default_value,
            default_factory_runner,
        )

    compile_state:
        tx_index: int = tx_index_for(tx_name)

    state CommittedStore per field:
        %%
        class CommittedStore(Generic[T]):
            value: T = state_slot(default=VOID)

            @on.construct.slots(order=10)
            def construct_slot(self) -> None:
                self.value = VOID

            @on.construct.init_values(order=10).when(params.initial_value.constructor_value_always_bound)
            def construct_from_init_value(self, init_value: T) -> None:
                self.value = init_value

            @on.construct.init_values(order=20).when(params.initial_value.constructor_value_may_be_unspecified)
            def construct_from_optional_init_value(self, init_value: T | UnspecifiedType) -> None:
                if init_value is not UNSPECIFIED:
                    self.value = init_value

            @on.construct.defaults(order=10).when(params.initial_value.assigns_default_value)
            def construct_from_default(self, default_value: T) -> None:
                self.value = default_value

            @on.construct.factories(order=10).when(params.initial_value.calls_default_factory)
            def construct_from_default_factory(self) -> None:
                self.value = default_factory_runner()

            @on.construct.required_checks(order=10).when(params.initial_value.requires_runtime_value)
            def require_constructed_value(self) -> None:
                if self.value is VOID:
                    raise RuntimeError("field requires an initial value")

            @on.facades(CurrentValueFacade).get.resolve(order=10)
            @on.facades(MainValueFacade).get.resolve(order=10)
            def resolve_value(self) -> T:
                return self.value

            @on.facades(CurrentValueFacade).get.return_value(order=10)
            @on.facades(MainValueFacade).get.return_value(order=10)
            def return_value(self, resolved: T) -> T:
                return resolved

            def set(self, value: T) -> None:
                self.value = value
        %%

    state PendingStore per field scoped_by tx_name:
        %%
        class PendingStore(Generic[T]):
            working_value: T = state_slot(default=VOID)
            working_tx_iteration_id: int = state_slot(default=VOID)

            @on.construct.slots(order=10)
            def construct_slot(self) -> None:
                self.working_value = VOID
                self.working_tx_iteration_id = VOID

            def has_working(self) -> bool:
                return self.working_value is not VOID

            def require_current_iteration(self, tx: TxKeyStore) -> int:
                tx_iteration_id = tx.require_active()
                if self.has_working() and self.working_tx_iteration_id != tx_iteration_id:
                    raise RuntimeError("working state belongs to another transaction iteration")
                return tx_iteration_id

            @on.facades(WorkingValueFacade).get.resolve(order=10)
            def resolve_value(self, committed: CommittedStore[T], tx: TxKeyStore) -> T:
                if self.has_working():
                    self.require_current_iteration(tx)
                    return self.working_value
                return committed.resolve_value()

            @on.facades(WorkingValueFacade).get.return_value(order=10)
            def return_value(self, resolved: T) -> T:
                return resolved

            @on.facades(WorkingValueFacade).set.prepare(order=10)
            def require_transaction(self, tx: TxKeyStore) -> None:
                tx.require_active()

            @on.facades(WorkingValueFacade).set.stage(order=10)
            def thaw_value(self, value: T) -> T:
                return thaw_runner(value)

            @on.facades(WorkingValueFacade).set.assign(order=10)
            def assign_working(self, staged: T, tx: TxKeyStore) -> None:
                self.working_tx_iteration_id = self.require_current_iteration(tx)
                self.working_value = staged

            @on.facades(WorkingValueFacade).set.finish(order=10)
            def mark_field_mutated(self) -> None:
                mark_mutated()

            @on.tx.commit.apply(mutated_fields(tx_name), order=10)
            def commit_to(self, committed: CommittedStore[T], tx: TxKeyStore) -> None:
                if not self.has_working():
                    return
                self.require_current_iteration(tx)
                committed.set(freeze_runner(self.working_value))
                self.working_value = VOID
                self.working_tx_iteration_id = VOID

            @on.tx.rollback.apply(mutated_fields(tx_name), order=10)
            def rollback(self) -> None:
                self.working_value = VOID
                self.working_tx_iteration_id = VOID
        %%


# ---------------------------------------------------------------------------
# Managed helper composition
# ---------------------------------------------------------------------------

transducer ManagedField:
    fieldhelper managed

    depends TransactionalValue

    parameters:
        field_name: FieldName = required()
        value_type: Type[T] = required()
        init_value: InitParameter[T] = constructor_parameter()
        default_value: ValueParameter[T] = optional_value()
        default_factory_runner: CallableRunner[T] = optional_callable(signature=DefaultFactory[T])
        freeze_runner: CallableRunner[T] = optional_callable(signature=Freeze[T], default=identity_runner())
        thaw_runner: CallableRunner[T] = optional_callable(signature=Thaw[T], default=identity_runner())
        tx_name: TxName = DEFAULT_TRANSACTION

    invariant:
        default_value and default_factory_runner cannot both be specified for the same initial-value source
        freeze_runner and thaw_runner are paired unless both are identity runners

    bind facades(CurrentValueFacade).set.prepare(order=10):
        %%
        raise RuntimeError("cannot mutate managed field through Current facade")
        %%

    bind facades(MainValueFacade).set.assign(order=10):
        %%
        # Main facade writes route to Working while a transaction is active.
        Working.set(value)
        %%


# ---------------------------------------------------------------------------
# Non-transactional field composition
# ---------------------------------------------------------------------------

transducer LocalValue:
    fieldhelper local_store

    requires facades(FieldExposingFacade)

    parameters:
        field_name: FieldName = required()
        value_type: Type[T] = required()
        default_factory_runner: CallableRunner[T] = required_callable(signature=DefaultFactory[T])

    state LocalStore per field:
        %%
        class LocalStore(Generic[T]):
            value: T = state_slot(default=VOID)

            @on.construct.slots(order=10)
            def construct_slot(self) -> None:
                self.value = VOID

            @on.construct.factories(order=10)
            def construct_from_default_factory(self) -> None:
                self.value = default_factory_runner()

            @on.facades(FieldExposingFacade).get.resolve(order=10)
            def resolve_value(self) -> T:
                return self.value

            @on.facades(FieldExposingFacade).get.return_value(order=10)
            def return_value(self, resolved: T) -> T:
                return resolved

            @on.facades(FieldExposingFacade).set.assign(order=10)
            def assign_value(self, value: T) -> None:
                self.value = value
        %%


# ---------------------------------------------------------------------------
# Open syntax questions captured by this sketch
# ---------------------------------------------------------------------------

syntax_questions:
    what the final IR names are for target facts and transducer contributions
    how transducer dependencies pass state classes into bound methods
    whether depends imports transducer contributions while requires only checks target facts
    whether bind arguments are symbolic or Python-call syntax
    whether facade classes are capability objects, inheritance policies, or both
    whether mutated_fields(tx_name) is introduced by TransactionGroupLifecycle or TransactionalValue
    how stage conflicts are diagnosed when two contributions require exclusive ownership
    whether equal order is rejected or stable-append within one stage
    which parameter object types and InitialValuePlan selectors are canonical
    whether construct.init_values is generated per field or by a central constructor transducer
    how class constants and compile_state differ in emitted Python
