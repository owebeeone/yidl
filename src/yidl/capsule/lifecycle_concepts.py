"""Recorded lifecycle concept assembly for the first state/facade split."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

import astichi

from yidl.capsule.build_mapper import ChildPortPlan
from yidl.capsule.build_mapper import TemplateEdgePlan
from yidl.capsule.recorded_builder import CapsuleConceptPlan
from yidl.capsule.recorded_builder import capsule_concept
from yidl.capsule.recorded_builder import match
from yidl.generation.data_def_sys import AddIfAbsent
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import astichi_template
from yidl.generation.data_def_sys import call
from yidl.generation.data_def_sys import from_astichi_code


MANAGED_KIND = "managed"
CONST_KIND = "const"
OWNED_KIND = "owned"
BINDING_KIND = "binding"

STATE_CLASS = "state"
MAIN_FACADE = "main_facade"

PROPERTY_PHASE = "property"
GET_OPERATION = "get"

COMMIT_VALIDATOR = "commit_validator"
COMMIT_ORDER_KEY = "commit_order_key"
BEFORE_COMMIT_HOOK = "before_commit"
AFTER_COMMIT_HOOK = "after_commit"
AFTER_ROLLBACK_HOOK = "after_rollback"


_MODULE_TEMPLATE = from_astichi_code("astichi_hole(module_body)")
_CLASS_TEMPLATE = from_astichi_code(
    """
    class class_name__astichi_arg__:
        astichi_hole(class_body)
    """
)


def property_order_for(result: object) -> int:
    """Place facade property methods after class vars and ``__init__``."""

    return 100 + result.records[0].order


def current_slot_for_result(result: object) -> str:
    return f"_{result.records[0].name}_current"


def working_slot_for_result(result: object) -> str:
    return f"_{result.records[0].name}_working"


def published_slot_for_result(result: object) -> str:
    return f"_{result.records[0].name}_value"


def _build_field_family_concept() -> CapsuleConceptPlan:
    builder = capsule_concept("lifecycle-field-family")
    name = builder.props.Name(str, REQUIRED)
    kind = builder.props.Kind(str, REQUIRED)
    annotation_path = builder.props.AnnotationPath(str, "")
    defaulted = builder.props.Defaulted(bool, False)
    default_value = builder.props.DefaultValue(object, None)
    order = builder.props.Order(int, 0)
    tx_group = builder.props.TxGroup(str, "")

    fields = builder.schema_family("FieldSpecs")
    fields.common(
        name,
        kind,
        annotation_path,
        defaulted,
        default_value,
        order,
        tx_group,
    )
    fields.variant("ManagedField")
    fields.variant("ConstField")
    builder.collections.Fields(
        fields.handle,
        cardinality=builder.many,
        identity=name,
    )
    return builder.build()


LifecycleFieldFamilyConcept: CapsuleConceptPlan = _build_field_family_concept()


def _build_transaction_index_concept() -> CapsuleConceptPlan:
    builder = capsule_concept(
        "lifecycle-transaction-index",
        extends=(LifecycleFieldFamilyConcept,),
    )
    fields = builder.use(LifecycleFieldFamilyConcept)
    tx_group = fields.props.TxGroup
    tx_index = builder.props.TxIndex(int, REQUIRED)

    tx_group_record = builder.records.TxGroupRecord(tx_group, tx_index)
    tx_groups = builder.collections.TxGroups(
        tx_group_record,
        cardinality=builder.many,
        identity=tx_group,
    )
    builder.operations.BuildTxGroups(
        inputs=(fields.collections.Fields,),
        outputs=(tx_groups,),
        resource=from_astichi_code(
            """
            seen = set()
            next_index = 0
            for field in sorted(
                ctx.records(FieldsCollection),
                key=lambda record: (record.order, ctx.write_order(record)),
            ):
                if field.kind != "managed":
                    continue
                if field.tx_group in seen:
                    continue
                seen.add(field.tx_group)
                ctx.write(
                    TxGroupsCollection,
                    TxGroupRecord(
                        tx_group=field.tx_group,
                        tx_index=next_index,
                    ),
                    policy=AddIfAbsent,
                )
                next_index += 1
            """,
            keep_names=(
                "AddIfAbsent",
                "FieldsCollection",
                "TxGroupRecord",
                "TxGroupsCollection",
                "ctx",
                "sorted",
            ),
        ),
    ).in_group("Transactions")
    return builder.build()


LifecycleTransactionIndexConcept: CapsuleConceptPlan = _build_transaction_index_concept()


def _build_class_structure_concept() -> CapsuleConceptPlan:
    builder = capsule_concept(
        "lifecycle-class-structure",
        extends=(LifecycleTransactionIndexConcept,),
    )
    fields = builder.use(LifecycleFieldFamilyConcept)
    name = fields.props.Name
    annotation_path = fields.props.AnnotationPath
    defaulted = fields.props.Defaulted
    default_value = fields.props.DefaultValue
    order = fields.props.Order

    class_role = builder.props.ClassRole(str, REQUIRED)
    class_name = builder.props.ClassName(str, REQUIRED)
    state_class_name = builder.props.StateClassName(str, "")
    target_port = builder.props.TargetPort(object, REQUIRED)
    template = builder.props.Template(object, REQUIRED)
    runtime_value = builder.props.RuntimeValue(object, REQUIRED)
    slot_name = builder.props.SlotName(str, "")
    source_name = builder.props.SourceName(str, "")
    target_name = builder.props.TargetName(str, "")
    field_name = builder.props.FieldName(str, "")
    current_slot = builder.props.CurrentSlot(str, "")
    working_slot = builder.props.WorkingSlot(str, "")
    published_slot = builder.props.PublishedSlot(str, "")
    phase = builder.props.Phase(str, "")
    operation_kind = builder.props.OperationKind(str, "")

    class_input = builder.records.ClassInput(class_name, state_class_name)
    class_name_contribution = builder.records.ClassNameContribution(
        class_role,
        target_port,
        order,
        runtime_value,
    )
    class_component = builder.records.ClassComponent(
        class_role,
        name,
        target_port,
        order,
        template,
        field_name,
        current_slot,
        working_slot,
        published_slot,
        source_name,
        target_name,
        state_class_name,
    )
    module_component = builder.records.ModuleComponent(
        name,
        target_port,
        order,
        template,
    )
    slot_item = builder.records.SlotItem(
        class_role,
        name,
        target_port,
        order,
        template,
        slot_name,
    )
    init_param = builder.records.InitParam(
        class_role,
        name,
        target_port,
        order,
        template,
        annotation_path,
        defaulted,
        default_value,
    )
    state_ctor_arg = builder.records.StateCtorArg(
        class_role,
        name,
        target_port,
        order,
        template,
    )
    operation_contribution = builder.records.OperationContribution(
        class_role,
        name,
        phase,
        operation_kind,
        target_port,
        order,
        template,
        field_name,
        current_slot,
        working_slot,
        published_slot,
    )

    class_inputs = builder.collections.ClassInputs(
        class_input,
        cardinality=builder.single,
        identity=class_name,
    )
    class_names = builder.collections.ClassNames(
        class_name_contribution,
        cardinality=builder.many,
        identity=class_role,
    )
    class_components = builder.collections.ClassComponents(
        class_component,
        cardinality=builder.many,
        identity=(class_role, name),
    )
    module_components = builder.collections.ModuleComponents(
        module_component,
        cardinality=builder.many,
        identity=name,
    )
    slot_items = builder.collections.SlotItems(
        slot_item,
        cardinality=builder.many,
        identity=(class_role, slot_name),
    )
    init_param_records = builder.collections.InitParams(
        init_param,
        cardinality=builder.many,
        identity=(class_role, name),
    )
    state_ctor_arg_records = builder.collections.StateCtorArgs(
        state_ctor_arg,
        cardinality=builder.many,
        identity=(class_role, name),
    )
    operation_contributions = builder.collections.OperationContributions(
        operation_contribution,
        cardinality=builder.many,
        identity=(class_role, name, phase),
    )

    module_body = builder.ports.Module.body(cardinality=builder.many)
    class_name_port = builder.ports.Class.name(cardinality=builder.single)
    class_body = builder.ports.Class.body(cardinality=builder.many)
    slots_items = builder.ports.Slots.items(cardinality=builder.many)
    init_params = builder.ports.Init.params(cardinality=builder.many)
    init_body = builder.ports.Init.body(cardinality=builder.many)
    state_ctor_args = builder.ports.StateCtor.args(cardinality=builder.many)
    builder.port_index(target=target_port, order=order)

    builder.operations.BuildLifecycleScaffold(
        inputs=(class_inputs, fields.collections.Fields),
        outputs=(
            class_names,
            class_components,
            module_components,
            slot_items,
            init_param_records,
            state_ctor_arg_records,
        ),
        resource=from_astichi_code(
            """
            astichi_pyimport(
                module=yidl.generation.data_def_sys,
                names=(from_astichi_code,),
            )

            module_sentinel_template = from_astichi_code(
                "_NO_WORKING_VALUE = object()",
            )
            slots_template = from_astichi_code(
                "__slots__ = (*astichi_hole(items),)",
                keep_names=("__slots__",),
            )
            init_template = from_astichi_code(
                "def __init__(self, params__astichi_param_hole__):\\n"
                "    astichi_hole(body)",
                keep_names=("self",),
            )
            init_param_template = from_astichi_code(
                "def astichi_params(*, field_name__astichi_arg__):\\n"
                "    pass",
            )
            defaulted_param_template = from_astichi_code(
                "def astichi_params(\\n"
                "    *,\\n"
                "    field_name__astichi_arg__=astichi_bind_external(default_value),\\n"
                "):\\n"
                "    pass",
            )
            annotated_param_template = from_astichi_code(
                "def astichi_params(\\n"
                "    *,\\n"
                "    field_name__astichi_arg__: astichi_ref(external=annotation_path),\\n"
                "):\\n"
                "    pass",
            )
            annotated_defaulted_param_template = from_astichi_code(
                "def astichi_params(\\n"
                "    *,\\n"
                "    field_name__astichi_arg__: astichi_ref(external=annotation_path)\\n"
                "    = astichi_bind_external(default_value),\\n"
                "):\\n"
                "    pass",
            )
            slot_item_template = from_astichi_code(
                "astichi_bind_external(slot_name)\\nslot_name",
            )
            current_assign_template = from_astichi_code(
                "astichi_import(self)\\n"
                "self.astichi_ref(external=target_path)._ = "
                "astichi_pass(source_name, outer_bind=True)",
            )
            working_assign_template = from_astichi_code(
                "astichi_import(self)\\n"
                "self.astichi_ref(external=target_path)._ = _NO_WORKING_VALUE",
                keep_names=("_NO_WORKING_VALUE",),
            )
            state_ctor_template = from_astichi_code(
                "self._state = state_class__astichi_arg__("
                "astichi_hole(state_ctor_args))",
                keep_names=("self",),
            )
            state_ctor_arg_template = from_astichi_code(
                "astichi_funcargs("
                "field_name__astichi_arg__=field_name__astichi_arg__)",
            )

            class_inputs = tuple(ctx.records(ClassInputsCollection))
            if len(class_inputs) != 1:
                raise ValueError("expected exactly one lifecycle class input")
            class_input = class_inputs[0]
            fields = sorted(
                ctx.records(FieldsCollection),
                key=lambda record: (record.order, ctx.write_order(record)),
            )
            state_role = "state"
            facade_role = "main_facade"

            ctx.write(
                ModuleComponentsCollection,
                ModuleComponent(
                    name="_NO_WORKING_VALUE",
                    target_port=ModuleBodyPort.of("runtime"),
                    order=-100,
                    template=module_sentinel_template,
                ),
                policy=AddIfAbsent,
            )
            ctx.write(
                ClassNamesCollection,
                ClassNameContribution(
                    class_role=state_role,
                    target_port=ClassNamePort.of(state_role),
                    order=0,
                    runtime_value=class_input.state_class_name,
                ),
                policy=AddIfAbsent,
            )
            ctx.write(
                ClassNamesCollection,
                ClassNameContribution(
                    class_role=facade_role,
                    target_port=ClassNamePort.of(facade_role),
                    order=10,
                    runtime_value=class_input.class_name,
                ),
                policy=AddIfAbsent,
            )
            for role in (state_role, facade_role):
                ctx.write(
                    ClassComponentsCollection,
                    ClassComponent(
                        class_role=role,
                        name="__slots__",
                        target_port=ClassBodyPort.of(role),
                        order=-10,
                        template=slots_template,
                    ),
                    policy=AddIfAbsent,
                )
                ctx.write(
                    ClassComponentsCollection,
                    ClassComponent(
                        class_role=role,
                        name="__init__",
                        target_port=ClassBodyPort.of(role),
                        order=0,
                        template=init_template,
                    ),
                    policy=AddIfAbsent,
                )

            ctx.write(
                SlotItemsCollection,
                SlotItem(
                    class_role=facade_role,
                    name="_state",
                    target_port=SlotsItemsPort.of((facade_role, "__slots__")),
                    order=0,
                    template=slot_item_template,
                    slot_name="_state",
                ),
                policy=AddIfAbsent,
            )
            ctx.write(
                ClassComponentsCollection,
                ClassComponent(
                    class_role=facade_role,
                    name="state_ctor",
                    target_port=InitBodyPort.of((facade_role, "__init__")),
                    order=0,
                    template=state_ctor_template,
                    state_class_name=class_input.state_class_name,
                ),
                policy=AddIfAbsent,
            )

            for field in fields:
                if field.annotation_path and field.defaulted:
                    param_template = annotated_defaulted_param_template
                elif field.annotation_path:
                    param_template = annotated_param_template
                elif field.defaulted:
                    param_template = defaulted_param_template
                else:
                    param_template = init_param_template
                ctx.write(
                    InitParamsCollection,
                    InitParam(
                        class_role=state_role,
                        name=field.name,
                        target_port=InitParamsPort.of((state_role, "__init__")),
                        order=field.order,
                        template=param_template,
                        annotation_path=field.annotation_path,
                        defaulted=field.defaulted,
                        default_value=field.default_value,
                    ),
                    policy=AddIfAbsent,
                )
                ctx.write(
                    InitParamsCollection,
                    InitParam(
                        class_role=facade_role,
                        name=field.name,
                        target_port=InitParamsPort.of((facade_role, "__init__")),
                        order=field.order,
                        template=param_template,
                        annotation_path=field.annotation_path,
                        defaulted=field.defaulted,
                        default_value=field.default_value,
                    ),
                    policy=AddIfAbsent,
                )
                ctx.write(
                    StateCtorArgsCollection,
                    StateCtorArg(
                        class_role=facade_role,
                        name=field.name,
                        target_port=StateCtorArgsPort.of(
                            (facade_role, "state_ctor")
                        ),
                        order=field.order,
                        template=state_ctor_arg_template,
                    ),
                    policy=AddIfAbsent,
                )
                if field.kind == "managed":
                    current_slot = f"_{field.name}_current"
                    working_slot = f"_{field.name}_working"
                    slot_specs = (
                        (current_slot, field.order * 2),
                        (working_slot, field.order * 2 + 1),
                    )
                    assignments = (
                        (f"{field.name}_current", current_slot, field.name, current_assign_template, field.order * 2),
                        (f"{field.name}_working", working_slot, "", working_assign_template, field.order * 2 + 1),
                    )
                else:
                    published_slot = f"_{field.name}_value"
                    slot_specs = ((published_slot, field.order * 2),)
                    assignments = (
                        (f"{field.name}_value", published_slot, field.name, current_assign_template, field.order * 2),
                    )
                for slot_name, slot_order in slot_specs:
                    ctx.write(
                        SlotItemsCollection,
                        SlotItem(
                            class_role=state_role,
                            name=slot_name,
                            target_port=SlotsItemsPort.of((state_role, "__slots__")),
                            order=slot_order,
                            template=slot_item_template,
                            slot_name=slot_name,
                        ),
                        policy=AddIfAbsent,
                    )
                for assign_name, target, source, assign_template, assign_order in assignments:
                    ctx.write(
                        ClassComponentsCollection,
                        ClassComponent(
                            class_role=state_role,
                            name=assign_name,
                            target_port=InitBodyPort.of((state_role, "__init__")),
                            order=assign_order,
                            template=assign_template,
                            source_name=source,
                            target_name=target,
                        ),
                        policy=AddIfAbsent,
                    )
            """,
            keep_names=(
                "AddIfAbsent",
                "ClassComponent",
                "ClassComponentsCollection",
                "ClassInput",
                "ClassInputsCollection",
                "ClassNameContribution",
                "ClassNamePort",
                "ClassNamesCollection",
                "ClassBodyPort",
                "FieldsCollection",
                "InitBodyPort",
                "InitParamsCollection",
                "InitParamsPort",
                "ModuleBodyPort",
                "ModuleComponent",
                "ModuleComponentsCollection",
                "SlotItem",
                "SlotItemsCollection",
                "SlotsItemsPort",
                "StateCtorArg",
                "StateCtorArgsCollection",
                "StateCtorArgsPort",
                "ValueError",
                "ctx",
                "from_astichi_code",
                "len",
                "sorted",
                "tuple",
            ),
        ),
    ).in_group("Scaffold")

    builder.productions.OperationContributionComponent(
        source=operation_contributions,
        target=class_components,
        values={
            class_role: class_role.read(),
            name: name.read(),
            target_port: target_port.read(),
            order: order.read(),
            template: template.read(),
            field_name: field_name.read(),
            current_slot: current_slot.read(),
            working_slot: working_slot.read(),
            published_slot: published_slot.read(),
        },
        policy=AddIfAbsent,
    ).in_group("ClassProjection")

    return builder.build()


LifecycleClassStructureConcept: CapsuleConceptPlan = _build_class_structure_concept()


def _build_property_concept() -> CapsuleConceptPlan:
    builder = capsule_concept(
        "lifecycle-property-contributions",
        extends=(LifecycleClassStructureConcept,),
    )
    fields = builder.use(LifecycleFieldFamilyConcept)
    classes = builder.use(LifecycleClassStructureConcept)

    name = fields.props.Name
    kind = fields.props.Kind
    order = fields.props.Order
    class_role = classes.props.ClassRole
    phase = classes.props.Phase
    operation_kind = classes.props.OperationKind
    target_port = classes.props.TargetPort
    template = classes.props.Template
    field_name = classes.props.FieldName
    current_slot = classes.props.CurrentSlot
    working_slot = classes.props.WorkingSlot
    published_slot = classes.props.PublishedSlot
    class_body = classes.ports.Class.body
    operation_contributions = classes.collections.OperationContributions

    property_template = builder.matchers.PropertyTemplate()
    field = property_template.input.field(fields.collections.Fields)
    property_template.default(
        astichi_template(
            from_astichi_code(
                """
                astichi_comment("property template: const value")

                @property
                def field_name__astichi_arg__(self):
                    return self._state.astichi_ref(external=published_slot)
                """
            ),
            arg_names=from_astichi_code(
                """
                {"field_name": astichi_pass(record, outer_bind=True).field_name}
                """
            ),
            bind=from_astichi_code(
                """
                {
                    "published_slot": (
                        astichi_pass(record, outer_bind=True).published_slot
                    )
                }
                """
            ),
        )
    )
    property_template.rule.managed_property(
        when=(field.prop(kind).eq(MANAGED_KIND),),
        resource=astichi_template(
            from_astichi_code(
                """
                astichi_comment("property template: managed value")

                @property
                def field_name__astichi_arg__(self):
                    state = self._state
                    if state.astichi_ref(external=working_slot) is not _NO_WORKING_VALUE:
                        return state.astichi_ref(external=working_slot)
                    return state.astichi_ref(external=current_slot)

                @field_name__astichi_arg__.setter
                def field_name__astichi_arg__(self, value):
                    self._state.astichi_ref(external=working_slot)._ = value
                """,
                keep_names=("_NO_WORKING_VALUE",),
            ),
            arg_names=from_astichi_code(
                """
                {"field_name": astichi_pass(record, outer_bind=True).field_name}
                """
            ),
            bind=from_astichi_code(
                """
                {
                    "current_slot": (
                        astichi_pass(record, outer_bind=True).current_slot
                    ),
                    "working_slot": (
                        astichi_pass(record, outer_bind=True).working_slot
                    ),
                }
                """
            ),
        ),
    )

    builder.productions.PropertyContribution(
        source=property_template.results(),
        target=operation_contributions,
        values={
            class_role: MAIN_FACADE,
            name: match.record("field").prop(name),
            phase: PROPERTY_PHASE,
            operation_kind: GET_OPERATION,
            target_port: class_body.of(MAIN_FACADE),
            order: call("property-order", property_order_for),
            template: match.resource(),
            field_name: match.record("field").prop(name),
            current_slot: call("current-slot", current_slot_for_result),
            working_slot: call("working-slot", working_slot_for_result),
            published_slot: call("published-slot", published_slot_for_result),
        },
        policy=AddIfAbsent,
    ).in_group("Properties")
    builder.runtime.evaluator(property_order_for)
    builder.runtime.evaluator(current_slot_for_result)
    builder.runtime.evaluator(working_slot_for_result)
    builder.runtime.evaluator(published_slot_for_result)
    return builder.build()


LifecyclePropertyConcept: CapsuleConceptPlan = _build_property_concept()


def _build_lifecycle_concept() -> CapsuleConceptPlan:
    return capsule_concept(
        "lifecycle-concepts",
        extends=(LifecyclePropertyConcept,),
    ).build()


LifecycleConcept: CapsuleConceptPlan = _build_lifecycle_concept()


def _build_transaction_methods_concept() -> CapsuleConceptPlan:
    builder = capsule_concept(
        "lifecycle-transaction-methods",
        extends=(LifecycleConcept,),
    )
    fields = builder.use(LifecycleFieldFamilyConcept)
    classes = builder.use(LifecycleClassStructureConcept)

    class_role = classes.props.ClassRole
    name = fields.props.Name
    target_port = classes.props.TargetPort
    order = fields.props.Order
    template = classes.props.Template
    current_slot = classes.props.CurrentSlot
    working_slot = classes.props.WorkingSlot
    class_body = classes.ports.Class.body

    method_statement = builder.records.MethodStatement(
        class_role,
        name,
        target_port,
        order,
        template,
        current_slot,
        working_slot,
    )
    method_statements = builder.collections.MethodStatements(
        method_statement,
        cardinality=builder.many,
        identity=(class_role, name),
    )
    method_body = builder.ports.Method.body(cardinality=builder.many)

    builder.operations.BuildTransactionMethods(
        inputs=(fields.collections.Fields,),
        outputs=(classes.collections.ClassComponents, method_statements),
        resource=from_astichi_code(
            """
            astichi_pyimport(
                module=yidl.generation.data_def_sys,
                names=(from_astichi_code,),
            )

            commit_template = from_astichi_code(
                "def commit(self):\\n"
                "    state = self._state\\n"
                "    astichi_hole(body)",
                keep_names=("self",),
            )
            rollback_template = from_astichi_code(
                "def rollback(self):\\n"
                "    state = self._state\\n"
                "    astichi_hole(body)",
                keep_names=("self",),
            )
            commit_statement_template = from_astichi_code(
                "if astichi_pass(state, outer_bind=True).astichi_ref("
                "external=working_slot) is not _NO_WORKING_VALUE:\\n"
                "    astichi_pass(state, outer_bind=True).astichi_ref("
                "external=current_slot)._ = astichi_pass("
                "state, outer_bind=True).astichi_ref(external=working_slot)\\n"
                "    astichi_pass(state, outer_bind=True).astichi_ref("
                "external=working_slot)._ = _NO_WORKING_VALUE",
                keep_names=("_NO_WORKING_VALUE",),
            )
            rollback_statement_template = from_astichi_code(
                "astichi_pass(state, outer_bind=True).astichi_ref("
                "external=working_slot)._ = _NO_WORKING_VALUE",
                keep_names=("_NO_WORKING_VALUE",),
            )

            managed_fields = [
                field
                for field in sorted(
                    ctx.records(FieldsCollection),
                    key=lambda record: (record.order, ctx.write_order(record)),
                )
                if field.kind == "managed"
            ]
            if not managed_fields:
                return

            facade_role = "main_facade"
            ctx.write(
                ClassComponentsCollection,
                ClassComponent(
                    class_role=facade_role,
                    name="commit",
                    target_port=ClassBodyPort.of(facade_role),
                    order=1000,
                    template=commit_template,
                ),
                policy=AddIfAbsent,
            )
            ctx.write(
                ClassComponentsCollection,
                ClassComponent(
                    class_role=facade_role,
                    name="rollback",
                    target_port=ClassBodyPort.of(facade_role),
                    order=1010,
                    template=rollback_template,
                ),
                policy=AddIfAbsent,
            )
            for field in managed_fields:
                current_slot = f"_{field.name}_current"
                working_slot = f"_{field.name}_working"
                ctx.write(
                    MethodStatementsCollection,
                    MethodStatement(
                        class_role=facade_role,
                        name=f"commit_{field.name}",
                        target_port=MethodBodyPort.of((facade_role, "commit")),
                        order=field.order,
                        template=commit_statement_template,
                        current_slot=current_slot,
                        working_slot=working_slot,
                    ),
                    policy=AddIfAbsent,
                )
                ctx.write(
                    MethodStatementsCollection,
                    MethodStatement(
                        class_role=facade_role,
                        name=f"rollback_{field.name}",
                        target_port=MethodBodyPort.of((facade_role, "rollback")),
                        order=field.order,
                        template=rollback_statement_template,
                        current_slot=current_slot,
                        working_slot=working_slot,
                    ),
                    policy=AddIfAbsent,
                )
            """,
            keep_names=(
                "AddIfAbsent",
                "ClassBodyPort",
                "ClassComponent",
                "ClassComponentsCollection",
                "FieldsCollection",
                "MethodBodyPort",
                "MethodStatement",
                "MethodStatementsCollection",
                "ctx",
                "from_astichi_code",
                "sorted",
            ),
        ),
    ).in_group("LifecycleMethods")
    del method_body
    return builder.build()


LifecycleTransactionMethodsConcept: CapsuleConceptPlan = (
    _build_transaction_methods_concept()
)


def _build_lifecycle_staircase_concept() -> CapsuleConceptPlan:
    return capsule_concept(
        "lifecycle-staircase",
        extends=(LifecycleTransactionMethodsConcept,),
    ).build()


LifecycleStaircaseConcept: CapsuleConceptPlan = _build_lifecycle_staircase_concept()


def _define_callable_fact_surface(
    builder: object,
    name: object,
) -> tuple[object, object, object, object, object, object, object, object]:
    source_label = builder.props.SourceLabel(str, "")
    callable_object = builder.props.CallableObject(object, REQUIRED)
    callable_role = builder.props.CallableRole(str, REQUIRED)
    allowed_injections = builder.props.AllowedInjections(tuple, ())
    accepts_varargs = builder.props.AcceptsVarArgs(bool, False)
    accepts_varkwargs = builder.props.AcceptsVarKwargs(bool, False)
    callable_name = builder.props.CallableName(str, REQUIRED)
    param_name = builder.props.ParamName(str, REQUIRED)
    param_kind = builder.props.ParamKind(str, REQUIRED)
    param_order = builder.props.ParamOrder(int, 0)
    injection_kind = builder.props.InjectionKind(str, REQUIRED)
    required = builder.props.Required(bool, True)

    callable_declaration = builder.records.CallableDeclaration(
        name,
        source_label,
        callable_object,
        callable_role,
        allowed_injections,
    )
    callable_spec = builder.records.CallableSpec(
        name,
        source_label,
        callable_role,
        accepts_varargs,
        accepts_varkwargs,
    )
    callable_param = builder.records.CallableParam(
        callable_name,
        param_name,
        param_kind,
        param_order,
    )
    callable_injection = builder.records.CallableInjection(
        callable_name,
        param_name,
        injection_kind,
        required,
    )

    declarations = builder.collections.CallableDeclarations(
        callable_declaration,
        cardinality=builder.many,
        identity=name,
    )
    specs = builder.collections.CallableSpecs(
        callable_spec,
        cardinality=builder.many,
        identity=name,
    )
    params = builder.collections.CallableParams(
        callable_param,
        cardinality=builder.many,
        identity=(callable_name, param_name),
    )
    injections = builder.collections.CallableInjections(
        callable_injection,
        cardinality=builder.many,
        identity=(callable_name, param_name),
    )
    return (
        source_label,
        callable_object,
        callable_role,
        allowed_injections,
        declarations,
        specs,
        params,
        injections,
    )


def _add_produce_callable_facts_operation(
    builder: object,
    *,
    declarations: object,
    specs: object,
    params: object,
    injections: object,
) -> None:

    builder.operations.ProduceCallableFacts(
        inputs=(declarations,),
        outputs=(specs, params, injections),
        resource=from_astichi_code(
            """
            astichi_comment("operation: produce callable facts")
            astichi_pyimport(
                module=yidl.generation.lifecycle_facts,
                names=(analyze_callable,),
            )

            for declaration in ctx.records(CallableDeclarationsCollection):
                result = analyze_callable(
                    name=declaration.name,
                    source_label=declaration.source_label,
                    role=declaration.callable_role,
                    callable_obj=declaration.callable_object,
                    allowed_injections=declaration.allowed_injections,
                )
                ctx.write(
                    CallableSpecsCollection,
                    CallableSpec(**result.spec),
                    policy=ReplaceExisting,
                )
                for param in result.params:
                    ctx.write(
                        CallableParamsCollection,
                        CallableParam(**param),
                        policy=RejectDuplicate,
                    )
                for injection in result.injections:
                    ctx.write(
                        CallableInjectionsCollection,
                        CallableInjection(**injection),
                        policy=RejectDuplicate,
                    )
            """,
            keep_names=(
                "CallableDeclarationsCollection",
                "CallableInjection",
                "CallableInjectionsCollection",
                "CallableParam",
                "CallableParamsCollection",
                "CallableSpec",
                "CallableSpecsCollection",
                "RejectDuplicate",
                "ReplaceExisting",
                "analyze_callable",
                "ctx",
            ),
        ),
    ).in_group("CallableFacts")


def _build_callable_facts_concept() -> CapsuleConceptPlan:
    builder = capsule_concept(
        "lifecycle-callable-facts",
        extends=(LifecycleFieldFamilyConcept,),
    )
    fields = builder.use(LifecycleFieldFamilyConcept)
    (
        _source_label,
        _callable_object,
        _callable_role,
        _allowed_injections,
        declarations,
        specs,
        params,
        injections,
    ) = _define_callable_fact_surface(
        builder,
        fields.props.Name,
    )
    _add_produce_callable_facts_operation(
        builder,
        declarations=declarations,
        specs=specs,
        params=params,
        injections=injections,
    )
    return builder.build()


LifecycleCallableFactsConcept: CapsuleConceptPlan = _build_callable_facts_concept()


def _build_resource_hooks_concept() -> CapsuleConceptPlan:
    builder = capsule_concept(
        "lifecycle-resource-hooks",
        extends=(LifecycleStaircaseConcept,),
    )
    fields = builder.use(LifecycleFieldFamilyConcept)
    classes = builder.use(LifecycleClassStructureConcept)

    name = fields.props.Name
    kind = fields.props.Kind
    tx_group = fields.props.TxGroup
    order = fields.props.Order
    target_port = classes.props.TargetPort
    template = classes.props.Template
    class_role = classes.props.ClassRole
    phase = classes.props.Phase
    published_slot = classes.props.PublishedSlot

    callable_path = builder.props.CallablePath(str, REQUIRED)
    release_path = builder.props.ReleasePath(str, "")
    resource_policy = builder.props.ResourcePolicy(str, "")

    builder.extend_schema_family(fields.families.FieldSpecs).variant(
        "OwnedField",
        release_path,
        resource_policy,
    )
    builder.extend_schema_family(fields.families.FieldSpecs).variant(
        "BindingField",
        release_path,
        resource_policy,
    )

    (
        source_label,
        callable_object,
        callable_role,
        allowed_injections,
        declarations,
        specs,
        params,
        injections,
    ) = _define_callable_fact_surface(
        builder,
        name,
    )

    commit_validator = builder.records.CommitValidator(
        name,
        source_label,
        callable_object,
        callable_role,
        tx_group,
        order,
        allowed_injections,
        callable_path,
    )
    commit_order_key = builder.records.CommitOrderKey(
        name,
        source_label,
        callable_object,
        callable_role,
        tx_group,
        order,
        allowed_injections,
        callable_path,
    )
    hook_declaration = builder.records.HookDeclaration(
        name,
        source_label,
        callable_object,
        callable_role,
        tx_group,
        phase,
        order,
        allowed_injections,
        callable_path,
    )
    hook_statement = builder.records.HookMethodStatement(
        class_role,
        name,
        target_port,
        order,
        template,
        callable_path,
    )
    cleanup_statement = builder.records.ResourceCleanupStatement(
        class_role,
        name,
        target_port,
        order,
        template,
        release_path,
        published_slot,
    )

    validators = builder.collections.CommitValidators(
        commit_validator,
        cardinality=builder.many,
        identity=tx_group,
    )
    order_keys = builder.collections.CommitOrderKeys(
        commit_order_key,
        cardinality=builder.many,
        identity=tx_group,
    )
    hooks = builder.collections.HookDeclarations(
        hook_declaration,
        cardinality=builder.many,
        identity=(phase, tx_group, name),
    )
    hook_statements = builder.collections.HookMethodStatements(
        hook_statement,
        cardinality=builder.many,
        identity=(class_role, name),
    )
    cleanup_statements = builder.collections.ResourceCleanupStatements(
        cleanup_statement,
        cardinality=builder.many,
        identity=(class_role, name),
    )

    method_body = builder.ports.Method.body

    builder.operations.BuildSpecialCallableDeclarations(
        inputs=(validators, order_keys, hooks),
        outputs=(declarations,),
        resource=from_astichi_code(
            """
            astichi_comment("operation: special lifecycle callable declarations")

            for declaration in (
                *ctx.records(CommitValidatorsCollection),
                *ctx.records(CommitOrderKeysCollection),
                *ctx.records(HookDeclarationsCollection),
            ):
                ctx.write(
                    CallableDeclarationsCollection,
                    CallableDeclaration(
                        name=declaration.name,
                        source_label=declaration.source_label,
                        callable_object=declaration.callable_object,
                        callable_role=declaration.callable_role,
                        allowed_injections=declaration.allowed_injections,
                    ),
                    policy=RejectDuplicate,
                )
            """,
            keep_names=(
                "CallableDeclaration",
                "CallableDeclarationsCollection",
                "CommitOrderKeysCollection",
                "CommitValidatorsCollection",
                "HookDeclarationsCollection",
                "RejectDuplicate",
                "ctx",
            ),
        ),
    ).in_group("CallableFacts")
    _add_produce_callable_facts_operation(
        builder,
        declarations=declarations,
        specs=specs,
        params=params,
        injections=injections,
    )

    builder.operations.BuildHookMethodStatements(
        inputs=(validators, hooks),
        outputs=(hook_statements,),
        resource=from_astichi_code(
            """
            astichi_pyimport(
                module=yidl.generation.data_def_sys,
                names=(from_astichi_code,),
            )

            call_template = from_astichi_code(
                "astichi_ref(external=callable_path)(current=self)",
                keep_names=("self",),
            )

            for validator in ctx.records(CommitValidatorsCollection):
                ctx.write(
                    HookMethodStatementsCollection,
                    HookMethodStatement(
                        class_role="main_facade",
                        name=f"validate_{validator.tx_group}",
                        target_port=MethodBodyPort.of(("main_facade", "commit")),
                        order=-500 + validator.order,
                        template=call_template,
                        callable_path=validator.callable_path,
                    ),
                    policy=AddIfAbsent,
                )
            for hook in ctx.records(HookDeclarationsCollection):
                if hook.callable_role == "before_commit":
                    method_name = "commit"
                    offset = -1000
                elif hook.callable_role == "after_commit":
                    method_name = "commit"
                    offset = 500
                elif hook.callable_role == "after_rollback":
                    method_name = "rollback"
                    offset = 500
                else:
                    continue
                ctx.write(
                    HookMethodStatementsCollection,
                    HookMethodStatement(
                        class_role="main_facade",
                        name=f"{hook.callable_role}_{hook.name}",
                        target_port=MethodBodyPort.of(("main_facade", method_name)),
                        order=offset + hook.order,
                        template=call_template,
                        callable_path=hook.callable_path,
                    ),
                    policy=AddIfAbsent,
                )
            """,
            keep_names=(
                "AddIfAbsent",
                "CommitValidatorsCollection",
                "HookDeclarationsCollection",
                "HookMethodStatement",
                "HookMethodStatementsCollection",
                "MethodBodyPort",
                "ctx",
                "from_astichi_code",
            ),
        ),
    ).in_group("Hooks")

    builder.operations.BuildResourceCleanupMethods(
        inputs=(fields.collections.Fields,),
        outputs=(classes.collections.ClassComponents, cleanup_statements),
        resource=from_astichi_code(
            """
            astichi_pyimport(
                module=yidl.generation.data_def_sys,
                names=(from_astichi_code,),
            )

            close_template = from_astichi_code(
                "def close(self):\\n"
                "    state = self._state\\n"
                "    astichi_hole(body)",
                keep_names=("self",),
            )
            cleanup_template = from_astichi_code(
                "value = astichi_pass(state, outer_bind=True).astichi_ref("
                "external=published_slot)\\n"
                "if value is not None:\\n"
                "    astichi_ref(external=release_path)(value)",
            )
            resource_fields = [
                field
                for field in ctx.records(FieldsCollection)
                if field.kind in ("owned", "binding")
            ]
            for field in resource_fields:
                if field.resource_policy not in ("owned_scalar", "binding_scalar"):
                    raise TypeError(
                        "unsupported resource policy "
                        f"{field.resource_policy!r} for field {field.name!r}"
                    )
            cleanup_fields = [
                field
                for field in resource_fields
                if field.release_path
            ]
            if not cleanup_fields:
                return
            ctx.write(
                ClassComponentsCollection,
                ClassComponent(
                    class_role="main_facade",
                    name="close",
                    target_port=ClassBodyPort.of("main_facade"),
                    order=1020,
                    template=close_template,
                ),
                policy=AddIfAbsent,
            )
            for field in cleanup_fields:
                ctx.write(
                    ResourceCleanupStatementsCollection,
                    ResourceCleanupStatement(
                        class_role="main_facade",
                        name=f"close_{field.name}",
                        target_port=MethodBodyPort.of(("main_facade", "close")),
                        order=field.order,
                        template=cleanup_template,
                        release_path=field.release_path,
                        published_slot=f"_{field.name}_value",
                    ),
                    policy=AddIfAbsent,
                )
            """,
            keep_names=(
                "AddIfAbsent",
                "ClassBodyPort",
                "ClassComponent",
                "ClassComponentsCollection",
                "FieldsCollection",
                "MethodBodyPort",
                "ResourceCleanupStatement",
                "ResourceCleanupStatementsCollection",
                "ctx",
                "from_astichi_code",
            ),
        ),
    ).in_group("Hooks")
    del method_body
    return builder.build()


LifecycleResourceHooksConcept: CapsuleConceptPlan = _build_resource_hooks_concept()


def render_lifecycle_module(
    container: object,
    namespace: Mapping[str, object],
    *,
    class_roles: Sequence[str] = (STATE_CLASS, MAIN_FACADE),
) -> str:
    """Render lifecycle module source from generated contribution records."""

    builder = astichi.build()
    builder.add("Module", _MODULE_TEMPLATE.to_generator())
    module_target = builder.instance("Module").target("module_body")
    module_records = container.children_at(namespace["ModuleBodyPort"].of("runtime"))
    _insert_records(
        builder,
        container,
        namespace,
        target_instance="Module",
        target_hole="module_body",
        records=module_records,
        edge=TemplateEdgePlan("ModuleBody"),
        child_ports=(),
    )

    for role in class_roles:
        class_name_record = _single_record(
            container.children_at(namespace["ClassNamePort"].of(role))
        )
        class_name = class_name_record.runtime_value
        _require_identifier(class_name, "class name")
        class_instance = _instance_name("Class", role)
        builder.add(
            class_instance,
            _CLASS_TEMPLATE.to_generator(),
            arg_names={"class_name": class_name},
            keep_names=[class_name],
        )
        module_target.add(class_instance, order=class_name_record.order)
        class_records = container.children_at(namespace["ClassBodyPort"].of(role))
        _insert_records(
            builder,
            container,
            namespace,
            target_instance=class_instance,
            target_hole="class_body",
            records=class_records,
            edge=TemplateEdgePlan("ClassBody"),
            child_ports=_LIFECYCLE_CHILD_PORTS,
        )

    return builder.build().materialize().emit(provenance=False)


def _insert_records(
    builder: object,
    container: object,
    namespace: Mapping[str, object],
    *,
    target_instance: str,
    target_hole: str,
    records: Sequence[object],
    edge: TemplateEdgePlan,
    child_ports: Sequence[ChildPortPlan],
) -> None:
    target = builder.instance(target_instance).target(target_hole)
    for index, record in enumerate(records):
        instance_name = f"{target_instance}_{edge.family_name}_{index}"
        builder.add(instance_name, edge.template_for(record).to_generator())
        target.add(
            instance_name,
            order=edge.order_for(record),
            arg_names=edge.arg_names_for(record),
            bind=edge.bind_for(record),
            keep_names=edge.keep_names_for(record),
        )
        for child_port in child_ports:
            if record.name != child_port.parent_name:
                continue
            port = namespace[child_port.port_name]
            child_records = container.children_at(port.of(child_port.owner_for(record)))
            _insert_records(
                builder,
                container,
                namespace,
                target_instance=instance_name,
                target_hole=child_port.target_hole,
                records=child_records,
                edge=child_port.edge,
                child_ports=child_ports,
            )


def _single_record(records: Sequence[object]) -> object:
    if len(records) != 1:
        raise ValueError(f"expected exactly one record, found {len(records)}")
    return records[0]


def _init_body_arg_names(record: object) -> dict[str, str]:
    values: dict[str, str] = {}
    if record.source_name:
        values["source_name"] = record.source_name
    if record.state_class_name:
        values["state_class"] = record.state_class_name
    return values


def _init_body_bind(record: object) -> dict[str, object]:
    if not record.target_name:
        return {}
    return {"target_path": record.target_name}


def _init_param_bind(record: object) -> dict[str, object]:
    values: dict[str, object] = {}
    if record.annotation_path:
        values["annotation_path"] = record.annotation_path
    if record.defaulted:
        values["default_value"] = record.default_value
    return values


def _method_body_bind(record: object) -> dict[str, object]:
    values: dict[str, object] = {}
    current_slot = getattr(record, "current_slot", "")
    working_slot = getattr(record, "working_slot", "")
    callable_path = getattr(record, "callable_path", "")
    release_path = getattr(record, "release_path", "")
    published_slot = getattr(record, "published_slot", "")
    if record.name.startswith("commit_") and current_slot:
        values["current_slot"] = current_slot
    if working_slot:
        values["working_slot"] = working_slot
    if callable_path:
        values["callable_path"] = callable_path
    if release_path:
        values["release_path"] = release_path
    if published_slot:
        values["published_slot"] = published_slot
    return values


def _instance_name(prefix: str, value: object) -> str:
    text = str(value).replace("-", "_").replace(".", "_")
    if not text.isidentifier():
        text = "value"
    return f"{prefix}_{text}"


def _require_identifier(value: object, label: str) -> None:
    if not isinstance(value, str) or not value.isidentifier():
        raise ValueError(f"{label} must be a Python identifier, got {value!r}")


_LIFECYCLE_CHILD_PORTS = (
    ChildPortPlan(
        parent_name="__slots__",
        port_name="SlotsItemsPort",
        target_hole="items",
        edge=TemplateEdgePlan(
            "SlotItem",
            bind=lambda record: {"slot_name": record.slot_name},
        ),
        owner=lambda record: (record.class_role, record.name),
    ),
    ChildPortPlan(
        parent_name="__init__",
        port_name="InitParamsPort",
        target_hole="params",
        edge=TemplateEdgePlan(
            "InitParam",
            arg_names=lambda record: {"field_name": record.name},
            bind=_init_param_bind,
            keep_names=lambda record: (record.name,),
        ),
        owner=lambda record: (record.class_role, record.name),
    ),
    ChildPortPlan(
        parent_name="__init__",
        port_name="InitBodyPort",
        target_hole="body",
        edge=TemplateEdgePlan(
            "InitBody",
            arg_names=_init_body_arg_names,
            bind=_init_body_bind,
        ),
        owner=lambda record: (record.class_role, record.name),
    ),
    ChildPortPlan(
        parent_name="state_ctor",
        port_name="StateCtorArgsPort",
        target_hole="state_ctor_args",
        edge=TemplateEdgePlan(
            "StateCtorArg",
            arg_names=lambda record: {"field_name": record.name},
            keep_names=lambda record: (record.name,),
        ),
        owner=lambda record: (record.class_role, record.name),
    ),
    ChildPortPlan(
        parent_name="commit",
        port_name="MethodBodyPort",
        target_hole="body",
        edge=TemplateEdgePlan(
            "MethodBody",
            bind=_method_body_bind,
        ),
        owner=lambda record: (record.class_role, record.name),
    ),
    ChildPortPlan(
        parent_name="rollback",
        port_name="MethodBodyPort",
        target_hole="body",
        edge=TemplateEdgePlan(
            "MethodBody",
            bind=_method_body_bind,
        ),
        owner=lambda record: (record.class_role, record.name),
    ),
    ChildPortPlan(
        parent_name="close",
        port_name="MethodBodyPort",
        target_hole="body",
        edge=TemplateEdgePlan(
            "MethodBody",
            bind=_method_body_bind,
        ),
        owner=lambda record: (record.class_role, record.name),
    ),
)


__all__ = [
    "CONST_KIND",
    "AFTER_COMMIT_HOOK",
    "AFTER_ROLLBACK_HOOK",
    "BEFORE_COMMIT_HOOK",
    "BINDING_KIND",
    "COMMIT_ORDER_KEY",
    "COMMIT_VALIDATOR",
    "GET_OPERATION",
    "LifecycleClassStructureConcept",
    "LifecycleCallableFactsConcept",
    "LifecycleConcept",
    "LifecycleFieldFamilyConcept",
    "LifecyclePropertyConcept",
    "LifecycleResourceHooksConcept",
    "LifecycleStaircaseConcept",
    "LifecycleTransactionIndexConcept",
    "LifecycleTransactionMethodsConcept",
    "MAIN_FACADE",
    "MANAGED_KIND",
    "OWNED_KIND",
    "PROPERTY_PHASE",
    "STATE_CLASS",
    "current_slot_for_result",
    "published_slot_for_result",
    "property_order_for",
    "render_lifecycle_module",
    "working_slot_for_result",
]
