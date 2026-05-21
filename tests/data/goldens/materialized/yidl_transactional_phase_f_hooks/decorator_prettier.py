from yidl.generation.data_def_sys import (
    AddIfAbsent,
    AssemblyDiagnosticError,
    DDSContainerBuilder,
    DDSOperationContext,
    NOT_PROVIDED,
    REQUIRED,
    RejectDuplicate,
    ReplaceExisting,
    RuntimeCollection,
    RuntimeComputedCollection,
    RuntimeContainerSpec,
    RuntimePort,
    RuntimePortIndex,
    RuntimeProperty,
    RuntimeRecord,
    RuntimeUnion,
)

_ClassIdProperty = RuntimeProperty(
    "ClassId", str, default=REQUIRED, storage_name="class_id"
)
_ClassNameProperty = RuntimeProperty(
    "ClassName", str, default=REQUIRED, storage_name="class_name"
)
_ClassOrderProperty = RuntimeProperty(
    "ClassOrder", int, default=0, storage_name="class_order"
)
_ModuleNameProperty = RuntimeProperty(
    "ModuleName", str, default="__main__", storage_name="module_name"
)
_StateClassNameProperty = RuntimeProperty(
    "StateClassName", str, default=REQUIRED, storage_name="state_class_name"
)
_FacadeBaseClassNameProperty = RuntimeProperty(
    "FacadeBaseClassName", str, default=REQUIRED, storage_name="facade_base_class_name"
)
_CurrentFacadeClassNameProperty = RuntimeProperty(
    "CurrentFacadeClassName",
    str,
    default=REQUIRED,
    storage_name="current_facade_class_name",
)
_WorkingFacadeClassNameProperty = RuntimeProperty(
    "WorkingFacadeClassName",
    str,
    default=REQUIRED,
    storage_name="working_facade_class_name",
)
_LifecycleDefinitionParamNameProperty = RuntimeProperty(
    "LifecycleDefinitionParamName",
    str,
    default="",
    storage_name="lifecycle_definition_param_name",
)
_AnnotationsParamNameProperty = RuntimeProperty(
    "AnnotationsParamName", str, default="", storage_name="annotations_param_name"
)
_TxGroupsParamNameProperty = RuntimeProperty(
    "TxGroupsParamName", str, default="", storage_name="tx_groups_param_name"
)
_LifecycleFieldNamesProperty = RuntimeProperty(
    "LifecycleFieldNames", object, default=(), storage_name="lifecycle_field_names"
)
_FieldIdProperty = RuntimeProperty(
    "FieldId", str, default=REQUIRED, storage_name="field_id"
)
_FieldOwnerProperty = RuntimeProperty(
    "FieldOwner", str, default=REQUIRED, storage_name="field_owner"
)
_FieldNameProperty = RuntimeProperty(
    "FieldName", str, default=REQUIRED, storage_name="field_name"
)
_FieldOrderProperty = RuntimeProperty(
    "FieldOrder", int, default=REQUIRED, storage_name="field_order"
)
_FieldKindProperty = RuntimeProperty(
    "FieldKind", str, default="field", storage_name="field_kind"
)
_AnnotationProperty = RuntimeProperty(
    "Annotation", object, default=object, storage_name="annotation"
)
_InitProperty = RuntimeProperty("Init", bool, default=True, storage_name="init")
_HasDefaultProperty = RuntimeProperty(
    "HasDefault", bool, default=False, storage_name="has_default"
)
_DefaultValueProperty = RuntimeProperty(
    "DefaultValue", object, default=None, storage_name="default_value"
)
_DefaultValueParamNameProperty = RuntimeProperty(
    "DefaultValueParamName", str, default="", storage_name="default_value_param_name"
)
_HasDefaultFactoryProperty = RuntimeProperty(
    "HasDefaultFactory", bool, default=False, storage_name="has_default_factory"
)
_DefaultFactoryProperty = RuntimeProperty(
    "DefaultFactory", object, default=None, storage_name="default_factory"
)
_DefaultFactoryParamNameProperty = RuntimeProperty(
    "DefaultFactoryParamName",
    str,
    default="",
    storage_name="default_factory_param_name",
)
_DefaultFactoryParamNamesProperty = RuntimeProperty(
    "DefaultFactoryParamNames",
    object,
    default=(),
    storage_name="default_factory_param_names",
)
_TxGroupKeyProperty = RuntimeProperty(
    "TxGroupKey", object, default=None, storage_name="tx_group_key"
)
_ValueSlotNameProperty = RuntimeProperty(
    "ValueSlotName", str, default="", storage_name="value_slot_name"
)
_CurrentSlotNameProperty = RuntimeProperty(
    "CurrentSlotName", str, default="", storage_name="current_slot_name"
)
_WorkingSlotNameProperty = RuntimeProperty(
    "WorkingSlotName", str, default="", storage_name="working_slot_name"
)
_StagedSlotNameProperty = RuntimeProperty(
    "StagedSlotName", str, default="", storage_name="staged_slot_name"
)
_HasFreezeProperty = RuntimeProperty(
    "HasFreeze", bool, default=False, storage_name="has_freeze"
)
_FreezeProperty = RuntimeProperty("Freeze", object, default=None, storage_name="freeze")
_FreezeParamNameProperty = RuntimeProperty(
    "FreezeParamName", str, default="", storage_name="freeze_param_name"
)
_HasThawProperty = RuntimeProperty(
    "HasThaw", bool, default=False, storage_name="has_thaw"
)
_ThawProperty = RuntimeProperty("Thaw", object, default=None, storage_name="thaw")
_ThawParamNameProperty = RuntimeProperty(
    "ThawParamName", str, default="", storage_name="thaw_param_name"
)
_HasOptionalNoneProperty = RuntimeProperty(
    "HasOptionalNone", bool, default=False, storage_name="has_optional_none"
)
_MethodIdProperty = RuntimeProperty(
    "MethodId", str, default=REQUIRED, storage_name="method_id"
)
_MethodOwnerProperty = RuntimeProperty(
    "MethodOwner", str, default=REQUIRED, storage_name="method_owner"
)
_MethodNameProperty = RuntimeProperty(
    "MethodName", str, default=REQUIRED, storage_name="method_name"
)
_MethodKindProperty = RuntimeProperty(
    "MethodKind", str, default=REQUIRED, storage_name="method_kind"
)
_DeclarationOrderProperty = RuntimeProperty(
    "DeclarationOrder", int, default=0, storage_name="declaration_order"
)
_TxIndexProperty = RuntimeProperty("TxIndex", int, default=0, storage_name="tx_index")
_FacadeIdProperty = RuntimeProperty(
    "FacadeId", str, default=REQUIRED, storage_name="facade_id"
)
_FacadeOwnerProperty = RuntimeProperty(
    "FacadeOwner", str, default=REQUIRED, storage_name="facade_owner"
)
_FacadeKindProperty = RuntimeProperty(
    "FacadeKind", str, default=REQUIRED, storage_name="facade_kind"
)
_FacadeModeProperty = RuntimeProperty(
    "FacadeMode", str, default=REQUIRED, storage_name="facade_mode"
)
_FacadeClassNameProperty = RuntimeProperty(
    "FacadeClassName", str, default=REQUIRED, storage_name="facade_class_name"
)
_FacadeOrderProperty = RuntimeProperty(
    "FacadeOrder", int, default=0, storage_name="facade_order"
)
_OwnerFacadeIdProperty = RuntimeProperty(
    "OwnerFacadeId", str, default=REQUIRED, storage_name="owner_facade_id"
)
_TargetFacadeIdProperty = RuntimeProperty(
    "TargetFacadeId", str, default=REQUIRED, storage_name="target_facade_id"
)
_ExposureOrderProperty = RuntimeProperty(
    "ExposureOrder", int, default=0, storage_name="exposure_order"
)
_InitParameterIdProperty = RuntimeProperty(
    "InitParameterId", str, default=REQUIRED, storage_name="init_parameter_id"
)
_InitParameterOwnerProperty = RuntimeProperty(
    "InitParameterOwner", str, default=REQUIRED, storage_name="init_parameter_owner"
)
_InitParameterNameProperty = RuntimeProperty(
    "InitParameterName", str, default=REQUIRED, storage_name="init_parameter_name"
)
_InitParameterOrderProperty = RuntimeProperty(
    "InitParameterOrder", int, default=0, storage_name="init_parameter_order"
)
_InitParameterKindProperty = RuntimeProperty(
    "InitParameterKind", str, default="field", storage_name="init_parameter_kind"
)
_InitAssignmentIdProperty = RuntimeProperty(
    "InitAssignmentId", str, default=REQUIRED, storage_name="init_assignment_id"
)
_InitAssignmentOwnerProperty = RuntimeProperty(
    "InitAssignmentOwner", str, default=REQUIRED, storage_name="init_assignment_owner"
)
_InitAssignmentFieldIdProperty = RuntimeProperty(
    "InitAssignmentFieldId",
    str,
    default=REQUIRED,
    storage_name="init_assignment_field_id",
)
_InitAssignmentFieldNameProperty = RuntimeProperty(
    "InitAssignmentFieldName",
    str,
    default=REQUIRED,
    storage_name="init_assignment_field_name",
)
_InitAssignmentOrderProperty = RuntimeProperty(
    "InitAssignmentOrder", int, default=0, storage_name="init_assignment_order"
)
_InitAssignmentKindProperty = RuntimeProperty(
    "InitAssignmentKind", str, default="plain", storage_name="init_assignment_kind"
)
_ClassVarAssignmentIdProperty = RuntimeProperty(
    "ClassVarAssignmentId",
    str,
    default=REQUIRED,
    storage_name="class_var_assignment_id",
)
_ClassVarAssignmentOwnerProperty = RuntimeProperty(
    "ClassVarAssignmentOwner",
    str,
    default=REQUIRED,
    storage_name="class_var_assignment_owner",
)
_ClassVarAssignmentNameProperty = RuntimeProperty(
    "ClassVarAssignmentName",
    str,
    default=REQUIRED,
    storage_name="class_var_assignment_name",
)
_ClassVarAssignmentOrderProperty = RuntimeProperty(
    "ClassVarAssignmentOrder", int, default=0, storage_name="class_var_assignment_order"
)
_TxGroupOrderProperty = RuntimeProperty(
    "TxGroupOrder", int, default=0, storage_name="tx_group_order"
)
_TxOwnerProperty = RuntimeProperty("TxOwner", str, default="", storage_name="tx_owner")
_PrepareCommitFieldsFunctionNameProperty = RuntimeProperty(
    "PrepareCommitFieldsFunctionName",
    str,
    default="",
    storage_name="prepare_commit_fields_function_name",
)
_ApplyPreparedCommitFieldsFunctionNameProperty = RuntimeProperty(
    "ApplyPreparedCommitFieldsFunctionName",
    str,
    default="",
    storage_name="apply_prepared_commit_fields_function_name",
)
_RollbackFieldsFunctionNameProperty = RuntimeProperty(
    "RollbackFieldsFunctionName",
    str,
    default="",
    storage_name="rollback_fields_function_name",
)
_DependencyOwnerProperty = RuntimeProperty(
    "DependencyOwner", str, default=REQUIRED, storage_name="dependency_owner"
)
_ConsumerFieldIdProperty = RuntimeProperty(
    "ConsumerFieldId", str, default=REQUIRED, storage_name="consumer_field_id"
)
_ConsumerFieldNameProperty = RuntimeProperty(
    "ConsumerFieldName", str, default="", storage_name="consumer_field_name"
)
_ProviderNameProperty = RuntimeProperty(
    "ProviderName", str, default=REQUIRED, storage_name="provider_name"
)
_ProviderFieldIdProperty = RuntimeProperty(
    "ProviderFieldId", str, default="", storage_name="provider_field_id"
)
_ProviderFieldKindProperty = RuntimeProperty(
    "ProviderFieldKind", str, default="", storage_name="provider_field_kind"
)
_ProviderInitProperty = RuntimeProperty(
    "ProviderInit", bool, default=True, storage_name="provider_init"
)
_ProviderHasDefaultProperty = RuntimeProperty(
    "ProviderHasDefault", bool, default=False, storage_name="provider_has_default"
)
_ProviderHasDefaultFactoryProperty = RuntimeProperty(
    "ProviderHasDefaultFactory",
    bool,
    default=False,
    storage_name="provider_has_default_factory",
)
_ParamNameProperty = RuntimeProperty(
    "ParamName", str, default=REQUIRED, storage_name="param_name"
)
_ParamOrderProperty = RuntimeProperty(
    "ParamOrder", int, default=0, storage_name="param_order"
)
_ConsumerEvalOrderProperty = RuntimeProperty(
    "ConsumerEvalOrder", int, default=0, storage_name="consumer_eval_order"
)
_EvalStepIdProperty = RuntimeProperty(
    "EvalStepId", str, default=REQUIRED, storage_name="eval_step_id"
)
_EvalOwnerProperty = RuntimeProperty(
    "EvalOwner", str, default=REQUIRED, storage_name="eval_owner"
)
_EvalFieldIdProperty = RuntimeProperty(
    "EvalFieldId", str, default=REQUIRED, storage_name="eval_field_id"
)
_EvalFieldNameProperty = RuntimeProperty(
    "EvalFieldName", str, default=REQUIRED, storage_name="eval_field_name"
)
_EvalFieldKindProperty = RuntimeProperty(
    "EvalFieldKind", str, default="", storage_name="eval_field_kind"
)
_EvalInitProperty = RuntimeProperty(
    "EvalInit", bool, default=True, storage_name="eval_init"
)
_EvalStateSlotNameProperty = RuntimeProperty(
    "EvalStateSlotName", str, default="", storage_name="eval_state_slot_name"
)
_EvalDefaultFactoryParamNameProperty = RuntimeProperty(
    "EvalDefaultFactoryParamName",
    str,
    default="",
    storage_name="eval_default_factory_param_name",
)
_EvalOrderProperty = RuntimeProperty(
    "EvalOrder", int, default=0, storage_name="eval_order"
)
_EvalStatementOrderProperty = RuntimeProperty(
    "EvalStatementOrder", int, default=0, storage_name="eval_statement_order"
)
_DiagnosticIdProperty = RuntimeProperty(
    "DiagnosticId", str, default=REQUIRED, storage_name="diagnostic_id"
)
_DiagnosticOwnerProperty = RuntimeProperty(
    "DiagnosticOwner", str, default=REQUIRED, storage_name="diagnostic_owner"
)
_DiagnosticFieldIdProperty = RuntimeProperty(
    "DiagnosticFieldId", str, default="", storage_name="diagnostic_field_id"
)
_DiagnosticMessageProperty = RuntimeProperty(
    "DiagnosticMessage", str, default=REQUIRED, storage_name="diagnostic_message"
)
_LifecycleClassSpec = RuntimeRecord(
    "LifecycleClass",
    (
        _ClassIdProperty,
        _ClassNameProperty,
        _ClassOrderProperty,
        _ModuleNameProperty,
        _StateClassNameProperty,
        _FacadeBaseClassNameProperty,
        _CurrentFacadeClassNameProperty,
        _WorkingFacadeClassNameProperty,
        _LifecycleDefinitionParamNameProperty,
        _AnnotationsParamNameProperty,
        _TxGroupsParamNameProperty,
        _LifecycleFieldNamesProperty,
    ),
)
_TransactionMethodSpec = RuntimeRecord(
    "TransactionMethod",
    (
        _MethodIdProperty,
        _MethodOwnerProperty,
        _MethodNameProperty,
        _MethodKindProperty,
        _TxGroupKeyProperty,
        _TxIndexProperty,
        _DeclarationOrderProperty,
    ),
)
_FacadeClassSpec = RuntimeRecord(
    "FacadeClass",
    (
        _FacadeOwnerProperty,
        _FacadeIdProperty,
        _FacadeKindProperty,
        _FacadeModeProperty,
        _FacadeClassNameProperty,
        _FacadeOrderProperty,
    ),
)
_FacadeExposureSpec = RuntimeRecord(
    "FacadeExposure",
    (
        _FacadeOwnerProperty,
        _OwnerFacadeIdProperty,
        _FieldNameProperty,
        _TargetFacadeIdProperty,
        _ExposureOrderProperty,
    ),
)
_InitParameterSpec = RuntimeRecord(
    "InitParameter",
    (
        _InitParameterIdProperty,
        _InitParameterOwnerProperty,
        _InitParameterNameProperty,
        _InitParameterOrderProperty,
        _InitParameterKindProperty,
    ),
)
_InitAssignmentSpec = RuntimeRecord(
    "InitAssignment",
    (
        _InitAssignmentIdProperty,
        _InitAssignmentOwnerProperty,
        _InitAssignmentFieldIdProperty,
        _InitAssignmentFieldNameProperty,
        _InitAssignmentOrderProperty,
        _InitAssignmentKindProperty,
    ),
)
_ClassVarAssignmentSpec = RuntimeRecord(
    "ClassVarAssignment",
    (
        _ClassVarAssignmentIdProperty,
        _ClassVarAssignmentOwnerProperty,
        _ClassVarAssignmentNameProperty,
        _ClassVarAssignmentOrderProperty,
    ),
)
_PlainFieldSpec = RuntimeRecord(
    "PlainField",
    (
        _FieldIdProperty,
        _FieldOwnerProperty,
        _FieldNameProperty,
        _FieldOrderProperty,
        _FieldKindProperty,
        _AnnotationProperty,
        _InitProperty,
        _HasDefaultProperty,
        _DefaultValueProperty,
        _DefaultValueParamNameProperty,
        _HasDefaultFactoryProperty,
        _DefaultFactoryProperty,
        _DefaultFactoryParamNameProperty,
        _DefaultFactoryParamNamesProperty,
        _TxGroupKeyProperty,
        _ValueSlotNameProperty,
        _CurrentSlotNameProperty,
        _WorkingSlotNameProperty,
        _StagedSlotNameProperty,
        _HasFreezeProperty,
        _FreezeProperty,
        _FreezeParamNameProperty,
        _HasThawProperty,
        _ThawProperty,
        _ThawParamNameProperty,
        _HasOptionalNoneProperty,
    ),
)
_InitVarFieldSpec = RuntimeRecord(
    "InitVarField",
    (
        _FieldIdProperty,
        _FieldOwnerProperty,
        _FieldNameProperty,
        _FieldOrderProperty,
        _FieldKindProperty,
        _AnnotationProperty,
        _InitProperty,
        _HasDefaultProperty,
        _DefaultValueProperty,
        _DefaultValueParamNameProperty,
        _HasDefaultFactoryProperty,
        _DefaultFactoryProperty,
        _DefaultFactoryParamNameProperty,
        _DefaultFactoryParamNamesProperty,
        _TxGroupKeyProperty,
        _ValueSlotNameProperty,
        _CurrentSlotNameProperty,
        _WorkingSlotNameProperty,
        _StagedSlotNameProperty,
        _HasFreezeProperty,
        _FreezeProperty,
        _FreezeParamNameProperty,
        _HasThawProperty,
        _ThawProperty,
        _ThawParamNameProperty,
        _HasOptionalNoneProperty,
    ),
)
_ClassVarFieldSpec = RuntimeRecord(
    "ClassVarField",
    (
        _FieldIdProperty,
        _FieldOwnerProperty,
        _FieldNameProperty,
        _FieldOrderProperty,
        _FieldKindProperty,
        _AnnotationProperty,
        _InitProperty,
        _HasDefaultProperty,
        _DefaultValueProperty,
        _DefaultValueParamNameProperty,
        _HasDefaultFactoryProperty,
        _DefaultFactoryProperty,
        _DefaultFactoryParamNameProperty,
        _DefaultFactoryParamNamesProperty,
        _TxGroupKeyProperty,
        _ValueSlotNameProperty,
        _CurrentSlotNameProperty,
        _WorkingSlotNameProperty,
        _StagedSlotNameProperty,
        _HasFreezeProperty,
        _FreezeProperty,
        _FreezeParamNameProperty,
        _HasThawProperty,
        _ThawProperty,
        _ThawParamNameProperty,
        _HasOptionalNoneProperty,
    ),
)
_TransactionalFieldSpec = RuntimeRecord(
    "TransactionalField",
    (
        _FieldIdProperty,
        _FieldOwnerProperty,
        _FieldNameProperty,
        _FieldOrderProperty,
        _TxGroupKeyProperty,
    ),
)
_TxGroupSpec = RuntimeRecord(
    "TxGroup",
    (
        _TxOwnerProperty,
        _TxGroupKeyProperty,
        _TxIndexProperty,
        _TxGroupOrderProperty,
        _PrepareCommitFieldsFunctionNameProperty,
        _ApplyPreparedCommitFieldsFunctionNameProperty,
        _RollbackFieldsFunctionNameProperty,
    ),
)
_IndexedTransactionalFieldSpec = RuntimeRecord(
    "IndexedTransactionalField",
    (
        _FieldIdProperty,
        _FieldOwnerProperty,
        _FieldNameProperty,
        _FieldOrderProperty,
        _TxGroupKeyProperty,
        _TxIndexProperty,
        _CurrentSlotNameProperty,
        _WorkingSlotNameProperty,
        _StagedSlotNameProperty,
        _HasFreezeProperty,
        _FreezeParamNameProperty,
        _HasThawProperty,
        _ThawParamNameProperty,
        _HasOptionalNoneProperty,
    ),
)
_ManagedFieldSpec = RuntimeRecord(
    "ManagedField",
    (
        _FieldIdProperty,
        _FieldOwnerProperty,
        _FieldNameProperty,
        _FieldOrderProperty,
        _FieldKindProperty,
        _AnnotationProperty,
        _InitProperty,
        _HasDefaultProperty,
        _DefaultValueProperty,
        _DefaultValueParamNameProperty,
        _HasDefaultFactoryProperty,
        _DefaultFactoryProperty,
        _DefaultFactoryParamNameProperty,
        _DefaultFactoryParamNamesProperty,
        _TxGroupKeyProperty,
        _ValueSlotNameProperty,
        _CurrentSlotNameProperty,
        _WorkingSlotNameProperty,
        _StagedSlotNameProperty,
        _HasFreezeProperty,
        _FreezeProperty,
        _FreezeParamNameProperty,
        _HasThawProperty,
        _ThawProperty,
        _ThawParamNameProperty,
        _HasOptionalNoneProperty,
    ),
)
_DefaultFactoryDependencySpec = RuntimeRecord(
    "DefaultFactoryDependency",
    (
        _DependencyOwnerProperty,
        _ConsumerFieldIdProperty,
        _ConsumerFieldNameProperty,
        _ProviderNameProperty,
        _ProviderFieldIdProperty,
        _ProviderFieldKindProperty,
        _ProviderInitProperty,
        _ProviderHasDefaultProperty,
        _ProviderHasDefaultFactoryProperty,
        _ParamNameProperty,
        _ParamOrderProperty,
        _ConsumerEvalOrderProperty,
    ),
)
_DefaultFactoryEvaluationStepSpec = RuntimeRecord(
    "DefaultFactoryEvaluationStep",
    (
        _EvalStepIdProperty,
        _EvalOwnerProperty,
        _EvalFieldIdProperty,
        _EvalFieldNameProperty,
        _EvalFieldKindProperty,
        _EvalInitProperty,
        _EvalStateSlotNameProperty,
        _EvalDefaultFactoryParamNameProperty,
        _EvalOrderProperty,
        _EvalStatementOrderProperty,
    ),
)
_DefaultFactoryDiagnosticSpec = RuntimeRecord(
    "DefaultFactoryDiagnostic",
    (
        _DiagnosticIdProperty,
        _DiagnosticOwnerProperty,
        _DiagnosticFieldIdProperty,
        _DiagnosticMessageProperty,
    ),
)
_LifecycleFieldSpecUnion = RuntimeUnion(
    "LifecycleFieldSpec",
    (_PlainFieldSpec, _InitVarFieldSpec, _ClassVarFieldSpec, _ManagedFieldSpec),
)


class LifecycleClass:
    __slots__ = (
        "class_id",
        "class_name",
        "class_order",
        "module_name",
        "state_class_name",
        "facade_base_class_name",
        "current_facade_class_name",
        "working_facade_class_name",
        "lifecycle_definition_param_name",
        "annotations_param_name",
        "tx_groups_param_name",
        "lifecycle_field_names",
    )
    __dds_record_spec__ = _LifecycleClassSpec
    class_id: str
    class_name: str
    class_order: int
    module_name: str
    state_class_name: str
    facade_base_class_name: str
    current_facade_class_name: str
    working_facade_class_name: str
    lifecycle_definition_param_name: str
    annotations_param_name: str
    tx_groups_param_name: str
    lifecycle_field_names: object

    def __init__(
        self,
        *,
        class_id: str,
        class_name: str,
        class_order: int = 0,
        module_name: str = "__main__",
        state_class_name: str,
        facade_base_class_name: str,
        current_facade_class_name: str,
        working_facade_class_name: str,
        lifecycle_definition_param_name: str = "",
        annotations_param_name: str = "",
        tx_groups_param_name: str = "",
        lifecycle_field_names: object = (),
    ):
        if not isinstance(class_id, str):
            raise TypeError("ClassId must be str, got " + type(class_id).__name__)
        object.__setattr__(self, "class_id", class_id)
        if not isinstance(class_name, str):
            raise TypeError("ClassName must be str, got " + type(class_name).__name__)
        object.__setattr__(self, "class_name", class_name)
        if not isinstance(class_order, int):
            raise TypeError("ClassOrder must be int, got " + type(class_order).__name__)
        object.__setattr__(self, "class_order", class_order)
        if not isinstance(module_name, str):
            raise TypeError("ModuleName must be str, got " + type(module_name).__name__)
        object.__setattr__(self, "module_name", module_name)
        if not isinstance(state_class_name, str):
            raise TypeError(
                "StateClassName must be str, got " + type(state_class_name).__name__
            )
        object.__setattr__(self, "state_class_name", state_class_name)
        if not isinstance(facade_base_class_name, str):
            raise TypeError(
                "FacadeBaseClassName must be str, got "
                + type(facade_base_class_name).__name__
            )
        object.__setattr__(self, "facade_base_class_name", facade_base_class_name)
        if not isinstance(current_facade_class_name, str):
            raise TypeError(
                "CurrentFacadeClassName must be str, got "
                + type(current_facade_class_name).__name__
            )
        object.__setattr__(self, "current_facade_class_name", current_facade_class_name)
        if not isinstance(working_facade_class_name, str):
            raise TypeError(
                "WorkingFacadeClassName must be str, got "
                + type(working_facade_class_name).__name__
            )
        object.__setattr__(self, "working_facade_class_name", working_facade_class_name)
        if not isinstance(lifecycle_definition_param_name, str):
            raise TypeError(
                "LifecycleDefinitionParamName must be str, got "
                + type(lifecycle_definition_param_name).__name__
            )
        object.__setattr__(
            self, "lifecycle_definition_param_name", lifecycle_definition_param_name
        )
        if not isinstance(annotations_param_name, str):
            raise TypeError(
                "AnnotationsParamName must be str, got "
                + type(annotations_param_name).__name__
            )
        object.__setattr__(self, "annotations_param_name", annotations_param_name)
        if not isinstance(tx_groups_param_name, str):
            raise TypeError(
                "TxGroupsParamName must be str, got "
                + type(tx_groups_param_name).__name__
            )
        object.__setattr__(self, "tx_groups_param_name", tx_groups_param_name)
        object.__setattr__(self, "lifecycle_field_names", lifecycle_field_names)

    def __setattr__(self, name, value):
        if name in (
            "class_id",
            "class_name",
            "class_order",
            "module_name",
            "state_class_name",
            "facade_base_class_name",
            "current_facade_class_name",
            "working_facade_class_name",
            "lifecycle_definition_param_name",
            "annotations_param_name",
            "tx_groups_param_name",
            "lifecycle_field_names",
        ):
            raise AttributeError("LifecycleClass records are immutable")
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append("class_id=" + repr(self.class_id))
        pieces.append("class_name=" + repr(self.class_name))
        pieces.append("class_order=" + repr(self.class_order))
        pieces.append("module_name=" + repr(self.module_name))
        pieces.append("state_class_name=" + repr(self.state_class_name))
        pieces.append("facade_base_class_name=" + repr(self.facade_base_class_name))
        pieces.append(
            "current_facade_class_name=" + repr(self.current_facade_class_name)
        )
        pieces.append(
            "working_facade_class_name=" + repr(self.working_facade_class_name)
        )
        pieces.append(
            "lifecycle_definition_param_name="
            + repr(self.lifecycle_definition_param_name)
        )
        pieces.append("annotations_param_name=" + repr(self.annotations_param_name))
        pieces.append("tx_groups_param_name=" + repr(self.tx_groups_param_name))
        pieces.append("lifecycle_field_names=" + repr(self.lifecycle_field_names))
        return "LifecycleClass" + "(" + ", ".join(pieces) + ")"


_LifecycleClassSpec.bind_record_class(LifecycleClass)


class TransactionMethod:
    __slots__ = (
        "method_id",
        "method_owner",
        "method_name",
        "method_kind",
        "tx_group_key",
        "tx_index",
        "declaration_order",
    )
    __dds_record_spec__ = _TransactionMethodSpec
    method_id: str
    method_owner: str
    method_name: str
    method_kind: str
    tx_group_key: object
    tx_index: int
    declaration_order: int

    def __init__(
        self,
        *,
        method_id: str,
        method_owner: str,
        method_name: str,
        method_kind: str,
        tx_group_key: object = None,
        tx_index: int = 0,
        declaration_order: int = 0,
    ):
        if not isinstance(method_id, str):
            raise TypeError("MethodId must be str, got " + type(method_id).__name__)
        object.__setattr__(self, "method_id", method_id)
        if not isinstance(method_owner, str):
            raise TypeError(
                "MethodOwner must be str, got " + type(method_owner).__name__
            )
        object.__setattr__(self, "method_owner", method_owner)
        if not isinstance(method_name, str):
            raise TypeError("MethodName must be str, got " + type(method_name).__name__)
        object.__setattr__(self, "method_name", method_name)
        if not isinstance(method_kind, str):
            raise TypeError("MethodKind must be str, got " + type(method_kind).__name__)
        object.__setattr__(self, "method_kind", method_kind)
        object.__setattr__(self, "tx_group_key", tx_group_key)
        if not isinstance(tx_index, int):
            raise TypeError("TxIndex must be int, got " + type(tx_index).__name__)
        object.__setattr__(self, "tx_index", tx_index)
        if not isinstance(declaration_order, int):
            raise TypeError(
                "DeclarationOrder must be int, got " + type(declaration_order).__name__
            )
        object.__setattr__(self, "declaration_order", declaration_order)

    def __setattr__(self, name, value):
        if name in (
            "method_id",
            "method_owner",
            "method_name",
            "method_kind",
            "tx_group_key",
            "tx_index",
            "declaration_order",
        ):
            raise AttributeError("TransactionMethod records are immutable")
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append("method_id=" + repr(self.method_id))
        pieces.append("method_owner=" + repr(self.method_owner))
        pieces.append("method_name=" + repr(self.method_name))
        pieces.append("method_kind=" + repr(self.method_kind))
        pieces.append("tx_group_key=" + repr(self.tx_group_key))
        pieces.append("tx_index=" + repr(self.tx_index))
        pieces.append("declaration_order=" + repr(self.declaration_order))
        return "TransactionMethod" + "(" + ", ".join(pieces) + ")"


_TransactionMethodSpec.bind_record_class(TransactionMethod)


class FacadeClass:
    __slots__ = (
        "facade_owner",
        "facade_id",
        "facade_kind",
        "facade_mode",
        "facade_class_name",
        "facade_order",
    )
    __dds_record_spec__ = _FacadeClassSpec
    facade_owner: str
    facade_id: str
    facade_kind: str
    facade_mode: str
    facade_class_name: str
    facade_order: int

    def __init__(
        self,
        *,
        facade_owner: str,
        facade_id: str,
        facade_kind: str,
        facade_mode: str,
        facade_class_name: str,
        facade_order: int = 0,
    ):
        if not isinstance(facade_owner, str):
            raise TypeError(
                "FacadeOwner must be str, got " + type(facade_owner).__name__
            )
        object.__setattr__(self, "facade_owner", facade_owner)
        if not isinstance(facade_id, str):
            raise TypeError("FacadeId must be str, got " + type(facade_id).__name__)
        object.__setattr__(self, "facade_id", facade_id)
        if not isinstance(facade_kind, str):
            raise TypeError("FacadeKind must be str, got " + type(facade_kind).__name__)
        object.__setattr__(self, "facade_kind", facade_kind)
        if not isinstance(facade_mode, str):
            raise TypeError("FacadeMode must be str, got " + type(facade_mode).__name__)
        object.__setattr__(self, "facade_mode", facade_mode)
        if not isinstance(facade_class_name, str):
            raise TypeError(
                "FacadeClassName must be str, got " + type(facade_class_name).__name__
            )
        object.__setattr__(self, "facade_class_name", facade_class_name)
        if not isinstance(facade_order, int):
            raise TypeError(
                "FacadeOrder must be int, got " + type(facade_order).__name__
            )
        object.__setattr__(self, "facade_order", facade_order)

    def __setattr__(self, name, value):
        if name in (
            "facade_owner",
            "facade_id",
            "facade_kind",
            "facade_mode",
            "facade_class_name",
            "facade_order",
        ):
            raise AttributeError("FacadeClass records are immutable")
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append("facade_owner=" + repr(self.facade_owner))
        pieces.append("facade_id=" + repr(self.facade_id))
        pieces.append("facade_kind=" + repr(self.facade_kind))
        pieces.append("facade_mode=" + repr(self.facade_mode))
        pieces.append("facade_class_name=" + repr(self.facade_class_name))
        pieces.append("facade_order=" + repr(self.facade_order))
        return "FacadeClass" + "(" + ", ".join(pieces) + ")"


_FacadeClassSpec.bind_record_class(FacadeClass)


class FacadeExposure:
    __slots__ = (
        "facade_owner",
        "owner_facade_id",
        "field_name",
        "target_facade_id",
        "exposure_order",
    )
    __dds_record_spec__ = _FacadeExposureSpec
    facade_owner: str
    owner_facade_id: str
    field_name: str
    target_facade_id: str
    exposure_order: int

    def __init__(
        self,
        *,
        facade_owner: str,
        owner_facade_id: str,
        field_name: str,
        target_facade_id: str,
        exposure_order: int = 0,
    ):
        if not isinstance(facade_owner, str):
            raise TypeError(
                "FacadeOwner must be str, got " + type(facade_owner).__name__
            )
        object.__setattr__(self, "facade_owner", facade_owner)
        if not isinstance(owner_facade_id, str):
            raise TypeError(
                "OwnerFacadeId must be str, got " + type(owner_facade_id).__name__
            )
        object.__setattr__(self, "owner_facade_id", owner_facade_id)
        if not isinstance(field_name, str):
            raise TypeError("FieldName must be str, got " + type(field_name).__name__)
        object.__setattr__(self, "field_name", field_name)
        if not isinstance(target_facade_id, str):
            raise TypeError(
                "TargetFacadeId must be str, got " + type(target_facade_id).__name__
            )
        object.__setattr__(self, "target_facade_id", target_facade_id)
        if not isinstance(exposure_order, int):
            raise TypeError(
                "ExposureOrder must be int, got " + type(exposure_order).__name__
            )
        object.__setattr__(self, "exposure_order", exposure_order)

    def __setattr__(self, name, value):
        if name in (
            "facade_owner",
            "owner_facade_id",
            "field_name",
            "target_facade_id",
            "exposure_order",
        ):
            raise AttributeError("FacadeExposure records are immutable")
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append("facade_owner=" + repr(self.facade_owner))
        pieces.append("owner_facade_id=" + repr(self.owner_facade_id))
        pieces.append("field_name=" + repr(self.field_name))
        pieces.append("target_facade_id=" + repr(self.target_facade_id))
        pieces.append("exposure_order=" + repr(self.exposure_order))
        return "FacadeExposure" + "(" + ", ".join(pieces) + ")"


_FacadeExposureSpec.bind_record_class(FacadeExposure)


class InitParameter:
    __slots__ = (
        "init_parameter_id",
        "init_parameter_owner",
        "init_parameter_name",
        "init_parameter_order",
        "init_parameter_kind",
    )
    __dds_record_spec__ = _InitParameterSpec
    init_parameter_id: str
    init_parameter_owner: str
    init_parameter_name: str
    init_parameter_order: int
    init_parameter_kind: str

    def __init__(
        self,
        *,
        init_parameter_id: str,
        init_parameter_owner: str,
        init_parameter_name: str,
        init_parameter_order: int = 0,
        init_parameter_kind: str = "field",
    ):
        if not isinstance(init_parameter_id, str):
            raise TypeError(
                "InitParameterId must be str, got " + type(init_parameter_id).__name__
            )
        object.__setattr__(self, "init_parameter_id", init_parameter_id)
        if not isinstance(init_parameter_owner, str):
            raise TypeError(
                "InitParameterOwner must be str, got "
                + type(init_parameter_owner).__name__
            )
        object.__setattr__(self, "init_parameter_owner", init_parameter_owner)
        if not isinstance(init_parameter_name, str):
            raise TypeError(
                "InitParameterName must be str, got "
                + type(init_parameter_name).__name__
            )
        object.__setattr__(self, "init_parameter_name", init_parameter_name)
        if not isinstance(init_parameter_order, int):
            raise TypeError(
                "InitParameterOrder must be int, got "
                + type(init_parameter_order).__name__
            )
        object.__setattr__(self, "init_parameter_order", init_parameter_order)
        if not isinstance(init_parameter_kind, str):
            raise TypeError(
                "InitParameterKind must be str, got "
                + type(init_parameter_kind).__name__
            )
        object.__setattr__(self, "init_parameter_kind", init_parameter_kind)

    def __setattr__(self, name, value):
        if name in (
            "init_parameter_id",
            "init_parameter_owner",
            "init_parameter_name",
            "init_parameter_order",
            "init_parameter_kind",
        ):
            raise AttributeError("InitParameter records are immutable")
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append("init_parameter_id=" + repr(self.init_parameter_id))
        pieces.append("init_parameter_owner=" + repr(self.init_parameter_owner))
        pieces.append("init_parameter_name=" + repr(self.init_parameter_name))
        pieces.append("init_parameter_order=" + repr(self.init_parameter_order))
        pieces.append("init_parameter_kind=" + repr(self.init_parameter_kind))
        return "InitParameter" + "(" + ", ".join(pieces) + ")"


_InitParameterSpec.bind_record_class(InitParameter)


class InitAssignment:
    __slots__ = (
        "init_assignment_id",
        "init_assignment_owner",
        "init_assignment_field_id",
        "init_assignment_field_name",
        "init_assignment_order",
        "init_assignment_kind",
    )
    __dds_record_spec__ = _InitAssignmentSpec
    init_assignment_id: str
    init_assignment_owner: str
    init_assignment_field_id: str
    init_assignment_field_name: str
    init_assignment_order: int
    init_assignment_kind: str

    def __init__(
        self,
        *,
        init_assignment_id: str,
        init_assignment_owner: str,
        init_assignment_field_id: str,
        init_assignment_field_name: str,
        init_assignment_order: int = 0,
        init_assignment_kind: str = "plain",
    ):
        if not isinstance(init_assignment_id, str):
            raise TypeError(
                "InitAssignmentId must be str, got " + type(init_assignment_id).__name__
            )
        object.__setattr__(self, "init_assignment_id", init_assignment_id)
        if not isinstance(init_assignment_owner, str):
            raise TypeError(
                "InitAssignmentOwner must be str, got "
                + type(init_assignment_owner).__name__
            )
        object.__setattr__(self, "init_assignment_owner", init_assignment_owner)
        if not isinstance(init_assignment_field_id, str):
            raise TypeError(
                "InitAssignmentFieldId must be str, got "
                + type(init_assignment_field_id).__name__
            )
        object.__setattr__(self, "init_assignment_field_id", init_assignment_field_id)
        if not isinstance(init_assignment_field_name, str):
            raise TypeError(
                "InitAssignmentFieldName must be str, got "
                + type(init_assignment_field_name).__name__
            )
        object.__setattr__(
            self, "init_assignment_field_name", init_assignment_field_name
        )
        if not isinstance(init_assignment_order, int):
            raise TypeError(
                "InitAssignmentOrder must be int, got "
                + type(init_assignment_order).__name__
            )
        object.__setattr__(self, "init_assignment_order", init_assignment_order)
        if not isinstance(init_assignment_kind, str):
            raise TypeError(
                "InitAssignmentKind must be str, got "
                + type(init_assignment_kind).__name__
            )
        object.__setattr__(self, "init_assignment_kind", init_assignment_kind)

    def __setattr__(self, name, value):
        if name in (
            "init_assignment_id",
            "init_assignment_owner",
            "init_assignment_field_id",
            "init_assignment_field_name",
            "init_assignment_order",
            "init_assignment_kind",
        ):
            raise AttributeError("InitAssignment records are immutable")
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append("init_assignment_id=" + repr(self.init_assignment_id))
        pieces.append("init_assignment_owner=" + repr(self.init_assignment_owner))
        pieces.append("init_assignment_field_id=" + repr(self.init_assignment_field_id))
        pieces.append(
            "init_assignment_field_name=" + repr(self.init_assignment_field_name)
        )
        pieces.append("init_assignment_order=" + repr(self.init_assignment_order))
        pieces.append("init_assignment_kind=" + repr(self.init_assignment_kind))
        return "InitAssignment" + "(" + ", ".join(pieces) + ")"


_InitAssignmentSpec.bind_record_class(InitAssignment)


class ClassVarAssignment:
    __slots__ = (
        "class_var_assignment_id",
        "class_var_assignment_owner",
        "class_var_assignment_name",
        "class_var_assignment_order",
    )
    __dds_record_spec__ = _ClassVarAssignmentSpec
    class_var_assignment_id: str
    class_var_assignment_owner: str
    class_var_assignment_name: str
    class_var_assignment_order: int

    def __init__(
        self,
        *,
        class_var_assignment_id: str,
        class_var_assignment_owner: str,
        class_var_assignment_name: str,
        class_var_assignment_order: int = 0,
    ):
        if not isinstance(class_var_assignment_id, str):
            raise TypeError(
                "ClassVarAssignmentId must be str, got "
                + type(class_var_assignment_id).__name__
            )
        object.__setattr__(self, "class_var_assignment_id", class_var_assignment_id)
        if not isinstance(class_var_assignment_owner, str):
            raise TypeError(
                "ClassVarAssignmentOwner must be str, got "
                + type(class_var_assignment_owner).__name__
            )
        object.__setattr__(
            self, "class_var_assignment_owner", class_var_assignment_owner
        )
        if not isinstance(class_var_assignment_name, str):
            raise TypeError(
                "ClassVarAssignmentName must be str, got "
                + type(class_var_assignment_name).__name__
            )
        object.__setattr__(self, "class_var_assignment_name", class_var_assignment_name)
        if not isinstance(class_var_assignment_order, int):
            raise TypeError(
                "ClassVarAssignmentOrder must be int, got "
                + type(class_var_assignment_order).__name__
            )
        object.__setattr__(
            self, "class_var_assignment_order", class_var_assignment_order
        )

    def __setattr__(self, name, value):
        if name in (
            "class_var_assignment_id",
            "class_var_assignment_owner",
            "class_var_assignment_name",
            "class_var_assignment_order",
        ):
            raise AttributeError("ClassVarAssignment records are immutable")
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append("class_var_assignment_id=" + repr(self.class_var_assignment_id))
        pieces.append(
            "class_var_assignment_owner=" + repr(self.class_var_assignment_owner)
        )
        pieces.append(
            "class_var_assignment_name=" + repr(self.class_var_assignment_name)
        )
        pieces.append(
            "class_var_assignment_order=" + repr(self.class_var_assignment_order)
        )
        return "ClassVarAssignment" + "(" + ", ".join(pieces) + ")"


_ClassVarAssignmentSpec.bind_record_class(ClassVarAssignment)


class PlainField:
    __slots__ = (
        "field_id",
        "field_owner",
        "field_name",
        "field_order",
        "field_kind",
        "annotation",
        "init",
        "has_default",
        "default_value",
        "default_value_param_name",
        "has_default_factory",
        "default_factory",
        "default_factory_param_name",
        "default_factory_param_names",
        "tx_group_key",
        "value_slot_name",
        "current_slot_name",
        "working_slot_name",
        "staged_slot_name",
        "has_freeze",
        "freeze",
        "freeze_param_name",
        "has_thaw",
        "thaw",
        "thaw_param_name",
        "has_optional_none",
    )
    __dds_record_spec__ = _PlainFieldSpec
    field_id: str
    field_owner: str
    field_name: str
    field_order: int
    field_kind: str
    annotation: object
    init: bool
    has_default: bool
    default_value: object
    default_value_param_name: str
    has_default_factory: bool
    default_factory: object
    default_factory_param_name: str
    default_factory_param_names: object
    tx_group_key: object
    value_slot_name: str
    current_slot_name: str
    working_slot_name: str
    staged_slot_name: str
    has_freeze: bool
    freeze: object
    freeze_param_name: str
    has_thaw: bool
    thaw: object
    thaw_param_name: str
    has_optional_none: bool

    def __init__(
        self,
        *,
        field_id: str,
        field_owner: str,
        field_name: str,
        field_order: int,
        field_kind: str = "field",
        annotation: object = object,
        init: bool = True,
        has_default: bool = False,
        default_value: object = None,
        default_value_param_name: str = "",
        has_default_factory: bool = False,
        default_factory: object = None,
        default_factory_param_name: str = "",
        default_factory_param_names: object = (),
        tx_group_key: object = None,
        value_slot_name: str = "",
        current_slot_name: str = "",
        working_slot_name: str = "",
        staged_slot_name: str = "",
        has_freeze: bool = False,
        freeze: object = None,
        freeze_param_name: str = "",
        has_thaw: bool = False,
        thaw: object = None,
        thaw_param_name: str = "",
        has_optional_none: bool = False,
    ):
        if not isinstance(field_id, str):
            raise TypeError("FieldId must be str, got " + type(field_id).__name__)
        object.__setattr__(self, "field_id", field_id)
        if not isinstance(field_owner, str):
            raise TypeError("FieldOwner must be str, got " + type(field_owner).__name__)
        object.__setattr__(self, "field_owner", field_owner)
        if not isinstance(field_name, str):
            raise TypeError("FieldName must be str, got " + type(field_name).__name__)
        object.__setattr__(self, "field_name", field_name)
        if not isinstance(field_order, int):
            raise TypeError("FieldOrder must be int, got " + type(field_order).__name__)
        object.__setattr__(self, "field_order", field_order)
        if not isinstance(field_kind, str):
            raise TypeError("FieldKind must be str, got " + type(field_kind).__name__)
        object.__setattr__(self, "field_kind", field_kind)
        object.__setattr__(self, "annotation", annotation)
        if not isinstance(init, bool):
            raise TypeError("Init must be bool, got " + type(init).__name__)
        object.__setattr__(self, "init", init)
        if not isinstance(has_default, bool):
            raise TypeError(
                "HasDefault must be bool, got " + type(has_default).__name__
            )
        object.__setattr__(self, "has_default", has_default)
        object.__setattr__(self, "default_value", default_value)
        if not isinstance(default_value_param_name, str):
            raise TypeError(
                "DefaultValueParamName must be str, got "
                + type(default_value_param_name).__name__
            )
        object.__setattr__(self, "default_value_param_name", default_value_param_name)
        if not isinstance(has_default_factory, bool):
            raise TypeError(
                "HasDefaultFactory must be bool, got "
                + type(has_default_factory).__name__
            )
        object.__setattr__(self, "has_default_factory", has_default_factory)
        object.__setattr__(self, "default_factory", default_factory)
        if not isinstance(default_factory_param_name, str):
            raise TypeError(
                "DefaultFactoryParamName must be str, got "
                + type(default_factory_param_name).__name__
            )
        object.__setattr__(
            self, "default_factory_param_name", default_factory_param_name
        )
        object.__setattr__(
            self, "default_factory_param_names", default_factory_param_names
        )
        object.__setattr__(self, "tx_group_key", tx_group_key)
        if not isinstance(value_slot_name, str):
            raise TypeError(
                "ValueSlotName must be str, got " + type(value_slot_name).__name__
            )
        object.__setattr__(self, "value_slot_name", value_slot_name)
        if not isinstance(current_slot_name, str):
            raise TypeError(
                "CurrentSlotName must be str, got " + type(current_slot_name).__name__
            )
        object.__setattr__(self, "current_slot_name", current_slot_name)
        if not isinstance(working_slot_name, str):
            raise TypeError(
                "WorkingSlotName must be str, got " + type(working_slot_name).__name__
            )
        object.__setattr__(self, "working_slot_name", working_slot_name)
        if not isinstance(staged_slot_name, str):
            raise TypeError(
                "StagedSlotName must be str, got " + type(staged_slot_name).__name__
            )
        object.__setattr__(self, "staged_slot_name", staged_slot_name)
        if not isinstance(has_freeze, bool):
            raise TypeError("HasFreeze must be bool, got " + type(has_freeze).__name__)
        object.__setattr__(self, "has_freeze", has_freeze)
        object.__setattr__(self, "freeze", freeze)
        if not isinstance(freeze_param_name, str):
            raise TypeError(
                "FreezeParamName must be str, got " + type(freeze_param_name).__name__
            )
        object.__setattr__(self, "freeze_param_name", freeze_param_name)
        if not isinstance(has_thaw, bool):
            raise TypeError("HasThaw must be bool, got " + type(has_thaw).__name__)
        object.__setattr__(self, "has_thaw", has_thaw)
        object.__setattr__(self, "thaw", thaw)
        if not isinstance(thaw_param_name, str):
            raise TypeError(
                "ThawParamName must be str, got " + type(thaw_param_name).__name__
            )
        object.__setattr__(self, "thaw_param_name", thaw_param_name)
        if not isinstance(has_optional_none, bool):
            raise TypeError(
                "HasOptionalNone must be bool, got " + type(has_optional_none).__name__
            )
        object.__setattr__(self, "has_optional_none", has_optional_none)

    def __setattr__(self, name, value):
        if name in (
            "field_id",
            "field_owner",
            "field_name",
            "field_order",
            "field_kind",
            "annotation",
            "init",
            "has_default",
            "default_value",
            "default_value_param_name",
            "has_default_factory",
            "default_factory",
            "default_factory_param_name",
            "default_factory_param_names",
            "tx_group_key",
            "value_slot_name",
            "current_slot_name",
            "working_slot_name",
            "staged_slot_name",
            "has_freeze",
            "freeze",
            "freeze_param_name",
            "has_thaw",
            "thaw",
            "thaw_param_name",
            "has_optional_none",
        ):
            raise AttributeError("PlainField records are immutable")
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append("field_id=" + repr(self.field_id))
        pieces.append("field_owner=" + repr(self.field_owner))
        pieces.append("field_name=" + repr(self.field_name))
        pieces.append("field_order=" + repr(self.field_order))
        pieces.append("field_kind=" + repr(self.field_kind))
        pieces.append("annotation=" + repr(self.annotation))
        pieces.append("init=" + repr(self.init))
        pieces.append("has_default=" + repr(self.has_default))
        pieces.append("default_value=" + repr(self.default_value))
        pieces.append("default_value_param_name=" + repr(self.default_value_param_name))
        pieces.append("has_default_factory=" + repr(self.has_default_factory))
        pieces.append("default_factory=" + repr(self.default_factory))
        pieces.append(
            "default_factory_param_name=" + repr(self.default_factory_param_name)
        )
        pieces.append(
            "default_factory_param_names=" + repr(self.default_factory_param_names)
        )
        pieces.append("tx_group_key=" + repr(self.tx_group_key))
        pieces.append("value_slot_name=" + repr(self.value_slot_name))
        pieces.append("current_slot_name=" + repr(self.current_slot_name))
        pieces.append("working_slot_name=" + repr(self.working_slot_name))
        pieces.append("staged_slot_name=" + repr(self.staged_slot_name))
        pieces.append("has_freeze=" + repr(self.has_freeze))
        pieces.append("freeze=" + repr(self.freeze))
        pieces.append("freeze_param_name=" + repr(self.freeze_param_name))
        pieces.append("has_thaw=" + repr(self.has_thaw))
        pieces.append("thaw=" + repr(self.thaw))
        pieces.append("thaw_param_name=" + repr(self.thaw_param_name))
        pieces.append("has_optional_none=" + repr(self.has_optional_none))
        return "PlainField" + "(" + ", ".join(pieces) + ")"


_PlainFieldSpec.bind_record_class(PlainField)


class InitVarField:
    __slots__ = (
        "field_id",
        "field_owner",
        "field_name",
        "field_order",
        "field_kind",
        "annotation",
        "init",
        "has_default",
        "default_value",
        "default_value_param_name",
        "has_default_factory",
        "default_factory",
        "default_factory_param_name",
        "default_factory_param_names",
        "tx_group_key",
        "value_slot_name",
        "current_slot_name",
        "working_slot_name",
        "staged_slot_name",
        "has_freeze",
        "freeze",
        "freeze_param_name",
        "has_thaw",
        "thaw",
        "thaw_param_name",
        "has_optional_none",
    )
    __dds_record_spec__ = _InitVarFieldSpec
    field_id: str
    field_owner: str
    field_name: str
    field_order: int
    field_kind: str
    annotation: object
    init: bool
    has_default: bool
    default_value: object
    default_value_param_name: str
    has_default_factory: bool
    default_factory: object
    default_factory_param_name: str
    default_factory_param_names: object
    tx_group_key: object
    value_slot_name: str
    current_slot_name: str
    working_slot_name: str
    staged_slot_name: str
    has_freeze: bool
    freeze: object
    freeze_param_name: str
    has_thaw: bool
    thaw: object
    thaw_param_name: str
    has_optional_none: bool

    def __init__(
        self,
        *,
        field_id: str,
        field_owner: str,
        field_name: str,
        field_order: int,
        field_kind: str = "field",
        annotation: object = object,
        init: bool = True,
        has_default: bool = False,
        default_value: object = None,
        default_value_param_name: str = "",
        has_default_factory: bool = False,
        default_factory: object = None,
        default_factory_param_name: str = "",
        default_factory_param_names: object = (),
        tx_group_key: object = None,
        value_slot_name: str = "",
        current_slot_name: str = "",
        working_slot_name: str = "",
        staged_slot_name: str = "",
        has_freeze: bool = False,
        freeze: object = None,
        freeze_param_name: str = "",
        has_thaw: bool = False,
        thaw: object = None,
        thaw_param_name: str = "",
        has_optional_none: bool = False,
    ):
        if not isinstance(field_id, str):
            raise TypeError("FieldId must be str, got " + type(field_id).__name__)
        object.__setattr__(self, "field_id", field_id)
        if not isinstance(field_owner, str):
            raise TypeError("FieldOwner must be str, got " + type(field_owner).__name__)
        object.__setattr__(self, "field_owner", field_owner)
        if not isinstance(field_name, str):
            raise TypeError("FieldName must be str, got " + type(field_name).__name__)
        object.__setattr__(self, "field_name", field_name)
        if not isinstance(field_order, int):
            raise TypeError("FieldOrder must be int, got " + type(field_order).__name__)
        object.__setattr__(self, "field_order", field_order)
        if not isinstance(field_kind, str):
            raise TypeError("FieldKind must be str, got " + type(field_kind).__name__)
        object.__setattr__(self, "field_kind", field_kind)
        object.__setattr__(self, "annotation", annotation)
        if not isinstance(init, bool):
            raise TypeError("Init must be bool, got " + type(init).__name__)
        object.__setattr__(self, "init", init)
        if not isinstance(has_default, bool):
            raise TypeError(
                "HasDefault must be bool, got " + type(has_default).__name__
            )
        object.__setattr__(self, "has_default", has_default)
        object.__setattr__(self, "default_value", default_value)
        if not isinstance(default_value_param_name, str):
            raise TypeError(
                "DefaultValueParamName must be str, got "
                + type(default_value_param_name).__name__
            )
        object.__setattr__(self, "default_value_param_name", default_value_param_name)
        if not isinstance(has_default_factory, bool):
            raise TypeError(
                "HasDefaultFactory must be bool, got "
                + type(has_default_factory).__name__
            )
        object.__setattr__(self, "has_default_factory", has_default_factory)
        object.__setattr__(self, "default_factory", default_factory)
        if not isinstance(default_factory_param_name, str):
            raise TypeError(
                "DefaultFactoryParamName must be str, got "
                + type(default_factory_param_name).__name__
            )
        object.__setattr__(
            self, "default_factory_param_name", default_factory_param_name
        )
        object.__setattr__(
            self, "default_factory_param_names", default_factory_param_names
        )
        object.__setattr__(self, "tx_group_key", tx_group_key)
        if not isinstance(value_slot_name, str):
            raise TypeError(
                "ValueSlotName must be str, got " + type(value_slot_name).__name__
            )
        object.__setattr__(self, "value_slot_name", value_slot_name)
        if not isinstance(current_slot_name, str):
            raise TypeError(
                "CurrentSlotName must be str, got " + type(current_slot_name).__name__
            )
        object.__setattr__(self, "current_slot_name", current_slot_name)
        if not isinstance(working_slot_name, str):
            raise TypeError(
                "WorkingSlotName must be str, got " + type(working_slot_name).__name__
            )
        object.__setattr__(self, "working_slot_name", working_slot_name)
        if not isinstance(staged_slot_name, str):
            raise TypeError(
                "StagedSlotName must be str, got " + type(staged_slot_name).__name__
            )
        object.__setattr__(self, "staged_slot_name", staged_slot_name)
        if not isinstance(has_freeze, bool):
            raise TypeError("HasFreeze must be bool, got " + type(has_freeze).__name__)
        object.__setattr__(self, "has_freeze", has_freeze)
        object.__setattr__(self, "freeze", freeze)
        if not isinstance(freeze_param_name, str):
            raise TypeError(
                "FreezeParamName must be str, got " + type(freeze_param_name).__name__
            )
        object.__setattr__(self, "freeze_param_name", freeze_param_name)
        if not isinstance(has_thaw, bool):
            raise TypeError("HasThaw must be bool, got " + type(has_thaw).__name__)
        object.__setattr__(self, "has_thaw", has_thaw)
        object.__setattr__(self, "thaw", thaw)
        if not isinstance(thaw_param_name, str):
            raise TypeError(
                "ThawParamName must be str, got " + type(thaw_param_name).__name__
            )
        object.__setattr__(self, "thaw_param_name", thaw_param_name)
        if not isinstance(has_optional_none, bool):
            raise TypeError(
                "HasOptionalNone must be bool, got " + type(has_optional_none).__name__
            )
        object.__setattr__(self, "has_optional_none", has_optional_none)

    def __setattr__(self, name, value):
        if name in (
            "field_id",
            "field_owner",
            "field_name",
            "field_order",
            "field_kind",
            "annotation",
            "init",
            "has_default",
            "default_value",
            "default_value_param_name",
            "has_default_factory",
            "default_factory",
            "default_factory_param_name",
            "default_factory_param_names",
            "tx_group_key",
            "value_slot_name",
            "current_slot_name",
            "working_slot_name",
            "staged_slot_name",
            "has_freeze",
            "freeze",
            "freeze_param_name",
            "has_thaw",
            "thaw",
            "thaw_param_name",
            "has_optional_none",
        ):
            raise AttributeError("InitVarField records are immutable")
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append("field_id=" + repr(self.field_id))
        pieces.append("field_owner=" + repr(self.field_owner))
        pieces.append("field_name=" + repr(self.field_name))
        pieces.append("field_order=" + repr(self.field_order))
        pieces.append("field_kind=" + repr(self.field_kind))
        pieces.append("annotation=" + repr(self.annotation))
        pieces.append("init=" + repr(self.init))
        pieces.append("has_default=" + repr(self.has_default))
        pieces.append("default_value=" + repr(self.default_value))
        pieces.append("default_value_param_name=" + repr(self.default_value_param_name))
        pieces.append("has_default_factory=" + repr(self.has_default_factory))
        pieces.append("default_factory=" + repr(self.default_factory))
        pieces.append(
            "default_factory_param_name=" + repr(self.default_factory_param_name)
        )
        pieces.append(
            "default_factory_param_names=" + repr(self.default_factory_param_names)
        )
        pieces.append("tx_group_key=" + repr(self.tx_group_key))
        pieces.append("value_slot_name=" + repr(self.value_slot_name))
        pieces.append("current_slot_name=" + repr(self.current_slot_name))
        pieces.append("working_slot_name=" + repr(self.working_slot_name))
        pieces.append("staged_slot_name=" + repr(self.staged_slot_name))
        pieces.append("has_freeze=" + repr(self.has_freeze))
        pieces.append("freeze=" + repr(self.freeze))
        pieces.append("freeze_param_name=" + repr(self.freeze_param_name))
        pieces.append("has_thaw=" + repr(self.has_thaw))
        pieces.append("thaw=" + repr(self.thaw))
        pieces.append("thaw_param_name=" + repr(self.thaw_param_name))
        pieces.append("has_optional_none=" + repr(self.has_optional_none))
        return "InitVarField" + "(" + ", ".join(pieces) + ")"


_InitVarFieldSpec.bind_record_class(InitVarField)


class ClassVarField:
    __slots__ = (
        "field_id",
        "field_owner",
        "field_name",
        "field_order",
        "field_kind",
        "annotation",
        "init",
        "has_default",
        "default_value",
        "default_value_param_name",
        "has_default_factory",
        "default_factory",
        "default_factory_param_name",
        "default_factory_param_names",
        "tx_group_key",
        "value_slot_name",
        "current_slot_name",
        "working_slot_name",
        "staged_slot_name",
        "has_freeze",
        "freeze",
        "freeze_param_name",
        "has_thaw",
        "thaw",
        "thaw_param_name",
        "has_optional_none",
    )
    __dds_record_spec__ = _ClassVarFieldSpec
    field_id: str
    field_owner: str
    field_name: str
    field_order: int
    field_kind: str
    annotation: object
    init: bool
    has_default: bool
    default_value: object
    default_value_param_name: str
    has_default_factory: bool
    default_factory: object
    default_factory_param_name: str
    default_factory_param_names: object
    tx_group_key: object
    value_slot_name: str
    current_slot_name: str
    working_slot_name: str
    staged_slot_name: str
    has_freeze: bool
    freeze: object
    freeze_param_name: str
    has_thaw: bool
    thaw: object
    thaw_param_name: str
    has_optional_none: bool

    def __init__(
        self,
        *,
        field_id: str,
        field_owner: str,
        field_name: str,
        field_order: int,
        field_kind: str = "field",
        annotation: object = object,
        init: bool = True,
        has_default: bool = False,
        default_value: object = None,
        default_value_param_name: str = "",
        has_default_factory: bool = False,
        default_factory: object = None,
        default_factory_param_name: str = "",
        default_factory_param_names: object = (),
        tx_group_key: object = None,
        value_slot_name: str = "",
        current_slot_name: str = "",
        working_slot_name: str = "",
        staged_slot_name: str = "",
        has_freeze: bool = False,
        freeze: object = None,
        freeze_param_name: str = "",
        has_thaw: bool = False,
        thaw: object = None,
        thaw_param_name: str = "",
        has_optional_none: bool = False,
    ):
        if not isinstance(field_id, str):
            raise TypeError("FieldId must be str, got " + type(field_id).__name__)
        object.__setattr__(self, "field_id", field_id)
        if not isinstance(field_owner, str):
            raise TypeError("FieldOwner must be str, got " + type(field_owner).__name__)
        object.__setattr__(self, "field_owner", field_owner)
        if not isinstance(field_name, str):
            raise TypeError("FieldName must be str, got " + type(field_name).__name__)
        object.__setattr__(self, "field_name", field_name)
        if not isinstance(field_order, int):
            raise TypeError("FieldOrder must be int, got " + type(field_order).__name__)
        object.__setattr__(self, "field_order", field_order)
        if not isinstance(field_kind, str):
            raise TypeError("FieldKind must be str, got " + type(field_kind).__name__)
        object.__setattr__(self, "field_kind", field_kind)
        object.__setattr__(self, "annotation", annotation)
        if not isinstance(init, bool):
            raise TypeError("Init must be bool, got " + type(init).__name__)
        object.__setattr__(self, "init", init)
        if not isinstance(has_default, bool):
            raise TypeError(
                "HasDefault must be bool, got " + type(has_default).__name__
            )
        object.__setattr__(self, "has_default", has_default)
        object.__setattr__(self, "default_value", default_value)
        if not isinstance(default_value_param_name, str):
            raise TypeError(
                "DefaultValueParamName must be str, got "
                + type(default_value_param_name).__name__
            )
        object.__setattr__(self, "default_value_param_name", default_value_param_name)
        if not isinstance(has_default_factory, bool):
            raise TypeError(
                "HasDefaultFactory must be bool, got "
                + type(has_default_factory).__name__
            )
        object.__setattr__(self, "has_default_factory", has_default_factory)
        object.__setattr__(self, "default_factory", default_factory)
        if not isinstance(default_factory_param_name, str):
            raise TypeError(
                "DefaultFactoryParamName must be str, got "
                + type(default_factory_param_name).__name__
            )
        object.__setattr__(
            self, "default_factory_param_name", default_factory_param_name
        )
        object.__setattr__(
            self, "default_factory_param_names", default_factory_param_names
        )
        object.__setattr__(self, "tx_group_key", tx_group_key)
        if not isinstance(value_slot_name, str):
            raise TypeError(
                "ValueSlotName must be str, got " + type(value_slot_name).__name__
            )
        object.__setattr__(self, "value_slot_name", value_slot_name)
        if not isinstance(current_slot_name, str):
            raise TypeError(
                "CurrentSlotName must be str, got " + type(current_slot_name).__name__
            )
        object.__setattr__(self, "current_slot_name", current_slot_name)
        if not isinstance(working_slot_name, str):
            raise TypeError(
                "WorkingSlotName must be str, got " + type(working_slot_name).__name__
            )
        object.__setattr__(self, "working_slot_name", working_slot_name)
        if not isinstance(staged_slot_name, str):
            raise TypeError(
                "StagedSlotName must be str, got " + type(staged_slot_name).__name__
            )
        object.__setattr__(self, "staged_slot_name", staged_slot_name)
        if not isinstance(has_freeze, bool):
            raise TypeError("HasFreeze must be bool, got " + type(has_freeze).__name__)
        object.__setattr__(self, "has_freeze", has_freeze)
        object.__setattr__(self, "freeze", freeze)
        if not isinstance(freeze_param_name, str):
            raise TypeError(
                "FreezeParamName must be str, got " + type(freeze_param_name).__name__
            )
        object.__setattr__(self, "freeze_param_name", freeze_param_name)
        if not isinstance(has_thaw, bool):
            raise TypeError("HasThaw must be bool, got " + type(has_thaw).__name__)
        object.__setattr__(self, "has_thaw", has_thaw)
        object.__setattr__(self, "thaw", thaw)
        if not isinstance(thaw_param_name, str):
            raise TypeError(
                "ThawParamName must be str, got " + type(thaw_param_name).__name__
            )
        object.__setattr__(self, "thaw_param_name", thaw_param_name)
        if not isinstance(has_optional_none, bool):
            raise TypeError(
                "HasOptionalNone must be bool, got " + type(has_optional_none).__name__
            )
        object.__setattr__(self, "has_optional_none", has_optional_none)

    def __setattr__(self, name, value):
        if name in (
            "field_id",
            "field_owner",
            "field_name",
            "field_order",
            "field_kind",
            "annotation",
            "init",
            "has_default",
            "default_value",
            "default_value_param_name",
            "has_default_factory",
            "default_factory",
            "default_factory_param_name",
            "default_factory_param_names",
            "tx_group_key",
            "value_slot_name",
            "current_slot_name",
            "working_slot_name",
            "staged_slot_name",
            "has_freeze",
            "freeze",
            "freeze_param_name",
            "has_thaw",
            "thaw",
            "thaw_param_name",
            "has_optional_none",
        ):
            raise AttributeError("ClassVarField records are immutable")
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append("field_id=" + repr(self.field_id))
        pieces.append("field_owner=" + repr(self.field_owner))
        pieces.append("field_name=" + repr(self.field_name))
        pieces.append("field_order=" + repr(self.field_order))
        pieces.append("field_kind=" + repr(self.field_kind))
        pieces.append("annotation=" + repr(self.annotation))
        pieces.append("init=" + repr(self.init))
        pieces.append("has_default=" + repr(self.has_default))
        pieces.append("default_value=" + repr(self.default_value))
        pieces.append("default_value_param_name=" + repr(self.default_value_param_name))
        pieces.append("has_default_factory=" + repr(self.has_default_factory))
        pieces.append("default_factory=" + repr(self.default_factory))
        pieces.append(
            "default_factory_param_name=" + repr(self.default_factory_param_name)
        )
        pieces.append(
            "default_factory_param_names=" + repr(self.default_factory_param_names)
        )
        pieces.append("tx_group_key=" + repr(self.tx_group_key))
        pieces.append("value_slot_name=" + repr(self.value_slot_name))
        pieces.append("current_slot_name=" + repr(self.current_slot_name))
        pieces.append("working_slot_name=" + repr(self.working_slot_name))
        pieces.append("staged_slot_name=" + repr(self.staged_slot_name))
        pieces.append("has_freeze=" + repr(self.has_freeze))
        pieces.append("freeze=" + repr(self.freeze))
        pieces.append("freeze_param_name=" + repr(self.freeze_param_name))
        pieces.append("has_thaw=" + repr(self.has_thaw))
        pieces.append("thaw=" + repr(self.thaw))
        pieces.append("thaw_param_name=" + repr(self.thaw_param_name))
        pieces.append("has_optional_none=" + repr(self.has_optional_none))
        return "ClassVarField" + "(" + ", ".join(pieces) + ")"


_ClassVarFieldSpec.bind_record_class(ClassVarField)


class TransactionalField:
    __slots__ = ("field_id", "field_owner", "field_name", "field_order", "tx_group_key")
    __dds_record_spec__ = _TransactionalFieldSpec
    field_id: str
    field_owner: str
    field_name: str
    field_order: int
    tx_group_key: object

    def __init__(
        self,
        *,
        field_id: str,
        field_owner: str,
        field_name: str,
        field_order: int,
        tx_group_key: object = None,
    ):
        if not isinstance(field_id, str):
            raise TypeError("FieldId must be str, got " + type(field_id).__name__)
        object.__setattr__(self, "field_id", field_id)
        if not isinstance(field_owner, str):
            raise TypeError("FieldOwner must be str, got " + type(field_owner).__name__)
        object.__setattr__(self, "field_owner", field_owner)
        if not isinstance(field_name, str):
            raise TypeError("FieldName must be str, got " + type(field_name).__name__)
        object.__setattr__(self, "field_name", field_name)
        if not isinstance(field_order, int):
            raise TypeError("FieldOrder must be int, got " + type(field_order).__name__)
        object.__setattr__(self, "field_order", field_order)
        object.__setattr__(self, "tx_group_key", tx_group_key)

    def __setattr__(self, name, value):
        if name in (
            "field_id",
            "field_owner",
            "field_name",
            "field_order",
            "tx_group_key",
        ):
            raise AttributeError("TransactionalField records are immutable")
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append("field_id=" + repr(self.field_id))
        pieces.append("field_owner=" + repr(self.field_owner))
        pieces.append("field_name=" + repr(self.field_name))
        pieces.append("field_order=" + repr(self.field_order))
        pieces.append("tx_group_key=" + repr(self.tx_group_key))
        return "TransactionalField" + "(" + ", ".join(pieces) + ")"


_TransactionalFieldSpec.bind_record_class(TransactionalField)


class TxGroup:
    __slots__ = (
        "tx_owner",
        "tx_group_key",
        "tx_index",
        "tx_group_order",
        "prepare_commit_fields_function_name",
        "apply_prepared_commit_fields_function_name",
        "rollback_fields_function_name",
    )
    __dds_record_spec__ = _TxGroupSpec
    tx_owner: str
    tx_group_key: object
    tx_index: int
    tx_group_order: int
    prepare_commit_fields_function_name: str
    apply_prepared_commit_fields_function_name: str
    rollback_fields_function_name: str

    def __init__(
        self,
        *,
        tx_owner: str = "",
        tx_group_key: object = None,
        tx_index: int = 0,
        tx_group_order: int = 0,
        prepare_commit_fields_function_name: str = "",
        apply_prepared_commit_fields_function_name: str = "",
        rollback_fields_function_name: str = "",
    ):
        if not isinstance(tx_owner, str):
            raise TypeError("TxOwner must be str, got " + type(tx_owner).__name__)
        object.__setattr__(self, "tx_owner", tx_owner)
        object.__setattr__(self, "tx_group_key", tx_group_key)
        if not isinstance(tx_index, int):
            raise TypeError("TxIndex must be int, got " + type(tx_index).__name__)
        object.__setattr__(self, "tx_index", tx_index)
        if not isinstance(tx_group_order, int):
            raise TypeError(
                "TxGroupOrder must be int, got " + type(tx_group_order).__name__
            )
        object.__setattr__(self, "tx_group_order", tx_group_order)
        if not isinstance(prepare_commit_fields_function_name, str):
            raise TypeError(
                "PrepareCommitFieldsFunctionName must be str, got "
                + type(prepare_commit_fields_function_name).__name__
            )
        object.__setattr__(
            self,
            "prepare_commit_fields_function_name",
            prepare_commit_fields_function_name,
        )
        if not isinstance(apply_prepared_commit_fields_function_name, str):
            raise TypeError(
                "ApplyPreparedCommitFieldsFunctionName must be str, got "
                + type(apply_prepared_commit_fields_function_name).__name__
            )
        object.__setattr__(
            self,
            "apply_prepared_commit_fields_function_name",
            apply_prepared_commit_fields_function_name,
        )
        if not isinstance(rollback_fields_function_name, str):
            raise TypeError(
                "RollbackFieldsFunctionName must be str, got "
                + type(rollback_fields_function_name).__name__
            )
        object.__setattr__(
            self, "rollback_fields_function_name", rollback_fields_function_name
        )

    def __setattr__(self, name, value):
        if name in (
            "tx_owner",
            "tx_group_key",
            "tx_index",
            "tx_group_order",
            "prepare_commit_fields_function_name",
            "apply_prepared_commit_fields_function_name",
            "rollback_fields_function_name",
        ):
            raise AttributeError("TxGroup records are immutable")
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append("tx_owner=" + repr(self.tx_owner))
        pieces.append("tx_group_key=" + repr(self.tx_group_key))
        pieces.append("tx_index=" + repr(self.tx_index))
        pieces.append("tx_group_order=" + repr(self.tx_group_order))
        pieces.append(
            "prepare_commit_fields_function_name="
            + repr(self.prepare_commit_fields_function_name)
        )
        pieces.append(
            "apply_prepared_commit_fields_function_name="
            + repr(self.apply_prepared_commit_fields_function_name)
        )
        pieces.append(
            "rollback_fields_function_name=" + repr(self.rollback_fields_function_name)
        )
        return "TxGroup" + "(" + ", ".join(pieces) + ")"


_TxGroupSpec.bind_record_class(TxGroup)


class IndexedTransactionalField:
    __slots__ = (
        "field_id",
        "field_owner",
        "field_name",
        "field_order",
        "tx_group_key",
        "tx_index",
        "current_slot_name",
        "working_slot_name",
        "staged_slot_name",
        "has_freeze",
        "freeze_param_name",
        "has_thaw",
        "thaw_param_name",
        "has_optional_none",
    )
    __dds_record_spec__ = _IndexedTransactionalFieldSpec
    field_id: str
    field_owner: str
    field_name: str
    field_order: int
    tx_group_key: object
    tx_index: int
    current_slot_name: str
    working_slot_name: str
    staged_slot_name: str
    has_freeze: bool
    freeze_param_name: str
    has_thaw: bool
    thaw_param_name: str
    has_optional_none: bool

    def __init__(
        self,
        *,
        field_id: str,
        field_owner: str,
        field_name: str,
        field_order: int,
        tx_group_key: object = None,
        tx_index: int = 0,
        current_slot_name: str = "",
        working_slot_name: str = "",
        staged_slot_name: str = "",
        has_freeze: bool = False,
        freeze_param_name: str = "",
        has_thaw: bool = False,
        thaw_param_name: str = "",
        has_optional_none: bool = False,
    ):
        if not isinstance(field_id, str):
            raise TypeError("FieldId must be str, got " + type(field_id).__name__)
        object.__setattr__(self, "field_id", field_id)
        if not isinstance(field_owner, str):
            raise TypeError("FieldOwner must be str, got " + type(field_owner).__name__)
        object.__setattr__(self, "field_owner", field_owner)
        if not isinstance(field_name, str):
            raise TypeError("FieldName must be str, got " + type(field_name).__name__)
        object.__setattr__(self, "field_name", field_name)
        if not isinstance(field_order, int):
            raise TypeError("FieldOrder must be int, got " + type(field_order).__name__)
        object.__setattr__(self, "field_order", field_order)
        object.__setattr__(self, "tx_group_key", tx_group_key)
        if not isinstance(tx_index, int):
            raise TypeError("TxIndex must be int, got " + type(tx_index).__name__)
        object.__setattr__(self, "tx_index", tx_index)
        if not isinstance(current_slot_name, str):
            raise TypeError(
                "CurrentSlotName must be str, got " + type(current_slot_name).__name__
            )
        object.__setattr__(self, "current_slot_name", current_slot_name)
        if not isinstance(working_slot_name, str):
            raise TypeError(
                "WorkingSlotName must be str, got " + type(working_slot_name).__name__
            )
        object.__setattr__(self, "working_slot_name", working_slot_name)
        if not isinstance(staged_slot_name, str):
            raise TypeError(
                "StagedSlotName must be str, got " + type(staged_slot_name).__name__
            )
        object.__setattr__(self, "staged_slot_name", staged_slot_name)
        if not isinstance(has_freeze, bool):
            raise TypeError("HasFreeze must be bool, got " + type(has_freeze).__name__)
        object.__setattr__(self, "has_freeze", has_freeze)
        if not isinstance(freeze_param_name, str):
            raise TypeError(
                "FreezeParamName must be str, got " + type(freeze_param_name).__name__
            )
        object.__setattr__(self, "freeze_param_name", freeze_param_name)
        if not isinstance(has_thaw, bool):
            raise TypeError("HasThaw must be bool, got " + type(has_thaw).__name__)
        object.__setattr__(self, "has_thaw", has_thaw)
        if not isinstance(thaw_param_name, str):
            raise TypeError(
                "ThawParamName must be str, got " + type(thaw_param_name).__name__
            )
        object.__setattr__(self, "thaw_param_name", thaw_param_name)
        if not isinstance(has_optional_none, bool):
            raise TypeError(
                "HasOptionalNone must be bool, got " + type(has_optional_none).__name__
            )
        object.__setattr__(self, "has_optional_none", has_optional_none)

    def __setattr__(self, name, value):
        if name in (
            "field_id",
            "field_owner",
            "field_name",
            "field_order",
            "tx_group_key",
            "tx_index",
            "current_slot_name",
            "working_slot_name",
            "staged_slot_name",
            "has_freeze",
            "freeze_param_name",
            "has_thaw",
            "thaw_param_name",
            "has_optional_none",
        ):
            raise AttributeError("IndexedTransactionalField records are immutable")
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append("field_id=" + repr(self.field_id))
        pieces.append("field_owner=" + repr(self.field_owner))
        pieces.append("field_name=" + repr(self.field_name))
        pieces.append("field_order=" + repr(self.field_order))
        pieces.append("tx_group_key=" + repr(self.tx_group_key))
        pieces.append("tx_index=" + repr(self.tx_index))
        pieces.append("current_slot_name=" + repr(self.current_slot_name))
        pieces.append("working_slot_name=" + repr(self.working_slot_name))
        pieces.append("staged_slot_name=" + repr(self.staged_slot_name))
        pieces.append("has_freeze=" + repr(self.has_freeze))
        pieces.append("freeze_param_name=" + repr(self.freeze_param_name))
        pieces.append("has_thaw=" + repr(self.has_thaw))
        pieces.append("thaw_param_name=" + repr(self.thaw_param_name))
        pieces.append("has_optional_none=" + repr(self.has_optional_none))
        return "IndexedTransactionalField" + "(" + ", ".join(pieces) + ")"


_IndexedTransactionalFieldSpec.bind_record_class(IndexedTransactionalField)


class ManagedField:
    __slots__ = (
        "field_id",
        "field_owner",
        "field_name",
        "field_order",
        "field_kind",
        "annotation",
        "init",
        "has_default",
        "default_value",
        "default_value_param_name",
        "has_default_factory",
        "default_factory",
        "default_factory_param_name",
        "default_factory_param_names",
        "tx_group_key",
        "value_slot_name",
        "current_slot_name",
        "working_slot_name",
        "staged_slot_name",
        "has_freeze",
        "freeze",
        "freeze_param_name",
        "has_thaw",
        "thaw",
        "thaw_param_name",
        "has_optional_none",
    )
    __dds_record_spec__ = _ManagedFieldSpec
    field_id: str
    field_owner: str
    field_name: str
    field_order: int
    field_kind: str
    annotation: object
    init: bool
    has_default: bool
    default_value: object
    default_value_param_name: str
    has_default_factory: bool
    default_factory: object
    default_factory_param_name: str
    default_factory_param_names: object
    tx_group_key: object
    value_slot_name: str
    current_slot_name: str
    working_slot_name: str
    staged_slot_name: str
    has_freeze: bool
    freeze: object
    freeze_param_name: str
    has_thaw: bool
    thaw: object
    thaw_param_name: str
    has_optional_none: bool

    def __init__(
        self,
        *,
        field_id: str,
        field_owner: str,
        field_name: str,
        field_order: int,
        field_kind: str = "field",
        annotation: object = object,
        init: bool = True,
        has_default: bool = False,
        default_value: object = None,
        default_value_param_name: str = "",
        has_default_factory: bool = False,
        default_factory: object = None,
        default_factory_param_name: str = "",
        default_factory_param_names: object = (),
        tx_group_key: object = None,
        value_slot_name: str = "",
        current_slot_name: str = "",
        working_slot_name: str = "",
        staged_slot_name: str = "",
        has_freeze: bool = False,
        freeze: object = None,
        freeze_param_name: str = "",
        has_thaw: bool = False,
        thaw: object = None,
        thaw_param_name: str = "",
        has_optional_none: bool = False,
    ):
        if not isinstance(field_id, str):
            raise TypeError("FieldId must be str, got " + type(field_id).__name__)
        object.__setattr__(self, "field_id", field_id)
        if not isinstance(field_owner, str):
            raise TypeError("FieldOwner must be str, got " + type(field_owner).__name__)
        object.__setattr__(self, "field_owner", field_owner)
        if not isinstance(field_name, str):
            raise TypeError("FieldName must be str, got " + type(field_name).__name__)
        object.__setattr__(self, "field_name", field_name)
        if not isinstance(field_order, int):
            raise TypeError("FieldOrder must be int, got " + type(field_order).__name__)
        object.__setattr__(self, "field_order", field_order)
        if not isinstance(field_kind, str):
            raise TypeError("FieldKind must be str, got " + type(field_kind).__name__)
        object.__setattr__(self, "field_kind", field_kind)
        object.__setattr__(self, "annotation", annotation)
        if not isinstance(init, bool):
            raise TypeError("Init must be bool, got " + type(init).__name__)
        object.__setattr__(self, "init", init)
        if not isinstance(has_default, bool):
            raise TypeError(
                "HasDefault must be bool, got " + type(has_default).__name__
            )
        object.__setattr__(self, "has_default", has_default)
        object.__setattr__(self, "default_value", default_value)
        if not isinstance(default_value_param_name, str):
            raise TypeError(
                "DefaultValueParamName must be str, got "
                + type(default_value_param_name).__name__
            )
        object.__setattr__(self, "default_value_param_name", default_value_param_name)
        if not isinstance(has_default_factory, bool):
            raise TypeError(
                "HasDefaultFactory must be bool, got "
                + type(has_default_factory).__name__
            )
        object.__setattr__(self, "has_default_factory", has_default_factory)
        object.__setattr__(self, "default_factory", default_factory)
        if not isinstance(default_factory_param_name, str):
            raise TypeError(
                "DefaultFactoryParamName must be str, got "
                + type(default_factory_param_name).__name__
            )
        object.__setattr__(
            self, "default_factory_param_name", default_factory_param_name
        )
        object.__setattr__(
            self, "default_factory_param_names", default_factory_param_names
        )
        object.__setattr__(self, "tx_group_key", tx_group_key)
        if not isinstance(value_slot_name, str):
            raise TypeError(
                "ValueSlotName must be str, got " + type(value_slot_name).__name__
            )
        object.__setattr__(self, "value_slot_name", value_slot_name)
        if not isinstance(current_slot_name, str):
            raise TypeError(
                "CurrentSlotName must be str, got " + type(current_slot_name).__name__
            )
        object.__setattr__(self, "current_slot_name", current_slot_name)
        if not isinstance(working_slot_name, str):
            raise TypeError(
                "WorkingSlotName must be str, got " + type(working_slot_name).__name__
            )
        object.__setattr__(self, "working_slot_name", working_slot_name)
        if not isinstance(staged_slot_name, str):
            raise TypeError(
                "StagedSlotName must be str, got " + type(staged_slot_name).__name__
            )
        object.__setattr__(self, "staged_slot_name", staged_slot_name)
        if not isinstance(has_freeze, bool):
            raise TypeError("HasFreeze must be bool, got " + type(has_freeze).__name__)
        object.__setattr__(self, "has_freeze", has_freeze)
        object.__setattr__(self, "freeze", freeze)
        if not isinstance(freeze_param_name, str):
            raise TypeError(
                "FreezeParamName must be str, got " + type(freeze_param_name).__name__
            )
        object.__setattr__(self, "freeze_param_name", freeze_param_name)
        if not isinstance(has_thaw, bool):
            raise TypeError("HasThaw must be bool, got " + type(has_thaw).__name__)
        object.__setattr__(self, "has_thaw", has_thaw)
        object.__setattr__(self, "thaw", thaw)
        if not isinstance(thaw_param_name, str):
            raise TypeError(
                "ThawParamName must be str, got " + type(thaw_param_name).__name__
            )
        object.__setattr__(self, "thaw_param_name", thaw_param_name)
        if not isinstance(has_optional_none, bool):
            raise TypeError(
                "HasOptionalNone must be bool, got " + type(has_optional_none).__name__
            )
        object.__setattr__(self, "has_optional_none", has_optional_none)

    def __setattr__(self, name, value):
        if name in (
            "field_id",
            "field_owner",
            "field_name",
            "field_order",
            "field_kind",
            "annotation",
            "init",
            "has_default",
            "default_value",
            "default_value_param_name",
            "has_default_factory",
            "default_factory",
            "default_factory_param_name",
            "default_factory_param_names",
            "tx_group_key",
            "value_slot_name",
            "current_slot_name",
            "working_slot_name",
            "staged_slot_name",
            "has_freeze",
            "freeze",
            "freeze_param_name",
            "has_thaw",
            "thaw",
            "thaw_param_name",
            "has_optional_none",
        ):
            raise AttributeError("ManagedField records are immutable")
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append("field_id=" + repr(self.field_id))
        pieces.append("field_owner=" + repr(self.field_owner))
        pieces.append("field_name=" + repr(self.field_name))
        pieces.append("field_order=" + repr(self.field_order))
        pieces.append("field_kind=" + repr(self.field_kind))
        pieces.append("annotation=" + repr(self.annotation))
        pieces.append("init=" + repr(self.init))
        pieces.append("has_default=" + repr(self.has_default))
        pieces.append("default_value=" + repr(self.default_value))
        pieces.append("default_value_param_name=" + repr(self.default_value_param_name))
        pieces.append("has_default_factory=" + repr(self.has_default_factory))
        pieces.append("default_factory=" + repr(self.default_factory))
        pieces.append(
            "default_factory_param_name=" + repr(self.default_factory_param_name)
        )
        pieces.append(
            "default_factory_param_names=" + repr(self.default_factory_param_names)
        )
        pieces.append("tx_group_key=" + repr(self.tx_group_key))
        pieces.append("value_slot_name=" + repr(self.value_slot_name))
        pieces.append("current_slot_name=" + repr(self.current_slot_name))
        pieces.append("working_slot_name=" + repr(self.working_slot_name))
        pieces.append("staged_slot_name=" + repr(self.staged_slot_name))
        pieces.append("has_freeze=" + repr(self.has_freeze))
        pieces.append("freeze=" + repr(self.freeze))
        pieces.append("freeze_param_name=" + repr(self.freeze_param_name))
        pieces.append("has_thaw=" + repr(self.has_thaw))
        pieces.append("thaw=" + repr(self.thaw))
        pieces.append("thaw_param_name=" + repr(self.thaw_param_name))
        pieces.append("has_optional_none=" + repr(self.has_optional_none))
        return "ManagedField" + "(" + ", ".join(pieces) + ")"


_ManagedFieldSpec.bind_record_class(ManagedField)


class DefaultFactoryDependency:
    __slots__ = (
        "dependency_owner",
        "consumer_field_id",
        "consumer_field_name",
        "provider_name",
        "provider_field_id",
        "provider_field_kind",
        "provider_init",
        "provider_has_default",
        "provider_has_default_factory",
        "param_name",
        "param_order",
        "consumer_eval_order",
    )
    __dds_record_spec__ = _DefaultFactoryDependencySpec
    dependency_owner: str
    consumer_field_id: str
    consumer_field_name: str
    provider_name: str
    provider_field_id: str
    provider_field_kind: str
    provider_init: bool
    provider_has_default: bool
    provider_has_default_factory: bool
    param_name: str
    param_order: int
    consumer_eval_order: int

    def __init__(
        self,
        *,
        dependency_owner: str,
        consumer_field_id: str,
        consumer_field_name: str = "",
        provider_name: str,
        provider_field_id: str = "",
        provider_field_kind: str = "",
        provider_init: bool = True,
        provider_has_default: bool = False,
        provider_has_default_factory: bool = False,
        param_name: str,
        param_order: int = 0,
        consumer_eval_order: int = 0,
    ):
        if not isinstance(dependency_owner, str):
            raise TypeError(
                "DependencyOwner must be str, got " + type(dependency_owner).__name__
            )
        object.__setattr__(self, "dependency_owner", dependency_owner)
        if not isinstance(consumer_field_id, str):
            raise TypeError(
                "ConsumerFieldId must be str, got " + type(consumer_field_id).__name__
            )
        object.__setattr__(self, "consumer_field_id", consumer_field_id)
        if not isinstance(consumer_field_name, str):
            raise TypeError(
                "ConsumerFieldName must be str, got "
                + type(consumer_field_name).__name__
            )
        object.__setattr__(self, "consumer_field_name", consumer_field_name)
        if not isinstance(provider_name, str):
            raise TypeError(
                "ProviderName must be str, got " + type(provider_name).__name__
            )
        object.__setattr__(self, "provider_name", provider_name)
        if not isinstance(provider_field_id, str):
            raise TypeError(
                "ProviderFieldId must be str, got " + type(provider_field_id).__name__
            )
        object.__setattr__(self, "provider_field_id", provider_field_id)
        if not isinstance(provider_field_kind, str):
            raise TypeError(
                "ProviderFieldKind must be str, got "
                + type(provider_field_kind).__name__
            )
        object.__setattr__(self, "provider_field_kind", provider_field_kind)
        if not isinstance(provider_init, bool):
            raise TypeError(
                "ProviderInit must be bool, got " + type(provider_init).__name__
            )
        object.__setattr__(self, "provider_init", provider_init)
        if not isinstance(provider_has_default, bool):
            raise TypeError(
                "ProviderHasDefault must be bool, got "
                + type(provider_has_default).__name__
            )
        object.__setattr__(self, "provider_has_default", provider_has_default)
        if not isinstance(provider_has_default_factory, bool):
            raise TypeError(
                "ProviderHasDefaultFactory must be bool, got "
                + type(provider_has_default_factory).__name__
            )
        object.__setattr__(
            self, "provider_has_default_factory", provider_has_default_factory
        )
        if not isinstance(param_name, str):
            raise TypeError("ParamName must be str, got " + type(param_name).__name__)
        object.__setattr__(self, "param_name", param_name)
        if not isinstance(param_order, int):
            raise TypeError("ParamOrder must be int, got " + type(param_order).__name__)
        object.__setattr__(self, "param_order", param_order)
        if not isinstance(consumer_eval_order, int):
            raise TypeError(
                "ConsumerEvalOrder must be int, got "
                + type(consumer_eval_order).__name__
            )
        object.__setattr__(self, "consumer_eval_order", consumer_eval_order)

    def __setattr__(self, name, value):
        if name in (
            "dependency_owner",
            "consumer_field_id",
            "consumer_field_name",
            "provider_name",
            "provider_field_id",
            "provider_field_kind",
            "provider_init",
            "provider_has_default",
            "provider_has_default_factory",
            "param_name",
            "param_order",
            "consumer_eval_order",
        ):
            raise AttributeError("DefaultFactoryDependency records are immutable")
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append("dependency_owner=" + repr(self.dependency_owner))
        pieces.append("consumer_field_id=" + repr(self.consumer_field_id))
        pieces.append("consumer_field_name=" + repr(self.consumer_field_name))
        pieces.append("provider_name=" + repr(self.provider_name))
        pieces.append("provider_field_id=" + repr(self.provider_field_id))
        pieces.append("provider_field_kind=" + repr(self.provider_field_kind))
        pieces.append("provider_init=" + repr(self.provider_init))
        pieces.append("provider_has_default=" + repr(self.provider_has_default))
        pieces.append(
            "provider_has_default_factory=" + repr(self.provider_has_default_factory)
        )
        pieces.append("param_name=" + repr(self.param_name))
        pieces.append("param_order=" + repr(self.param_order))
        pieces.append("consumer_eval_order=" + repr(self.consumer_eval_order))
        return "DefaultFactoryDependency" + "(" + ", ".join(pieces) + ")"


_DefaultFactoryDependencySpec.bind_record_class(DefaultFactoryDependency)


class DefaultFactoryEvaluationStep:
    __slots__ = (
        "eval_step_id",
        "eval_owner",
        "eval_field_id",
        "eval_field_name",
        "eval_field_kind",
        "eval_init",
        "eval_state_slot_name",
        "eval_default_factory_param_name",
        "eval_order",
        "eval_statement_order",
    )
    __dds_record_spec__ = _DefaultFactoryEvaluationStepSpec
    eval_step_id: str
    eval_owner: str
    eval_field_id: str
    eval_field_name: str
    eval_field_kind: str
    eval_init: bool
    eval_state_slot_name: str
    eval_default_factory_param_name: str
    eval_order: int
    eval_statement_order: int

    def __init__(
        self,
        *,
        eval_step_id: str,
        eval_owner: str,
        eval_field_id: str,
        eval_field_name: str,
        eval_field_kind: str = "",
        eval_init: bool = True,
        eval_state_slot_name: str = "",
        eval_default_factory_param_name: str = "",
        eval_order: int = 0,
        eval_statement_order: int = 0,
    ):
        if not isinstance(eval_step_id, str):
            raise TypeError(
                "EvalStepId must be str, got " + type(eval_step_id).__name__
            )
        object.__setattr__(self, "eval_step_id", eval_step_id)
        if not isinstance(eval_owner, str):
            raise TypeError("EvalOwner must be str, got " + type(eval_owner).__name__)
        object.__setattr__(self, "eval_owner", eval_owner)
        if not isinstance(eval_field_id, str):
            raise TypeError(
                "EvalFieldId must be str, got " + type(eval_field_id).__name__
            )
        object.__setattr__(self, "eval_field_id", eval_field_id)
        if not isinstance(eval_field_name, str):
            raise TypeError(
                "EvalFieldName must be str, got " + type(eval_field_name).__name__
            )
        object.__setattr__(self, "eval_field_name", eval_field_name)
        if not isinstance(eval_field_kind, str):
            raise TypeError(
                "EvalFieldKind must be str, got " + type(eval_field_kind).__name__
            )
        object.__setattr__(self, "eval_field_kind", eval_field_kind)
        if not isinstance(eval_init, bool):
            raise TypeError("EvalInit must be bool, got " + type(eval_init).__name__)
        object.__setattr__(self, "eval_init", eval_init)
        if not isinstance(eval_state_slot_name, str):
            raise TypeError(
                "EvalStateSlotName must be str, got "
                + type(eval_state_slot_name).__name__
            )
        object.__setattr__(self, "eval_state_slot_name", eval_state_slot_name)
        if not isinstance(eval_default_factory_param_name, str):
            raise TypeError(
                "EvalDefaultFactoryParamName must be str, got "
                + type(eval_default_factory_param_name).__name__
            )
        object.__setattr__(
            self, "eval_default_factory_param_name", eval_default_factory_param_name
        )
        if not isinstance(eval_order, int):
            raise TypeError("EvalOrder must be int, got " + type(eval_order).__name__)
        object.__setattr__(self, "eval_order", eval_order)
        if not isinstance(eval_statement_order, int):
            raise TypeError(
                "EvalStatementOrder must be int, got "
                + type(eval_statement_order).__name__
            )
        object.__setattr__(self, "eval_statement_order", eval_statement_order)

    def __setattr__(self, name, value):
        if name in (
            "eval_step_id",
            "eval_owner",
            "eval_field_id",
            "eval_field_name",
            "eval_field_kind",
            "eval_init",
            "eval_state_slot_name",
            "eval_default_factory_param_name",
            "eval_order",
            "eval_statement_order",
        ):
            raise AttributeError("DefaultFactoryEvaluationStep records are immutable")
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append("eval_step_id=" + repr(self.eval_step_id))
        pieces.append("eval_owner=" + repr(self.eval_owner))
        pieces.append("eval_field_id=" + repr(self.eval_field_id))
        pieces.append("eval_field_name=" + repr(self.eval_field_name))
        pieces.append("eval_field_kind=" + repr(self.eval_field_kind))
        pieces.append("eval_init=" + repr(self.eval_init))
        pieces.append("eval_state_slot_name=" + repr(self.eval_state_slot_name))
        pieces.append(
            "eval_default_factory_param_name="
            + repr(self.eval_default_factory_param_name)
        )
        pieces.append("eval_order=" + repr(self.eval_order))
        pieces.append("eval_statement_order=" + repr(self.eval_statement_order))
        return "DefaultFactoryEvaluationStep" + "(" + ", ".join(pieces) + ")"


_DefaultFactoryEvaluationStepSpec.bind_record_class(DefaultFactoryEvaluationStep)


class DefaultFactoryDiagnostic:
    __slots__ = (
        "diagnostic_id",
        "diagnostic_owner",
        "diagnostic_field_id",
        "diagnostic_message",
    )
    __dds_record_spec__ = _DefaultFactoryDiagnosticSpec
    diagnostic_id: str
    diagnostic_owner: str
    diagnostic_field_id: str
    diagnostic_message: str

    def __init__(
        self,
        *,
        diagnostic_id: str,
        diagnostic_owner: str,
        diagnostic_field_id: str = "",
        diagnostic_message: str,
    ):
        if not isinstance(diagnostic_id, str):
            raise TypeError(
                "DiagnosticId must be str, got " + type(diagnostic_id).__name__
            )
        object.__setattr__(self, "diagnostic_id", diagnostic_id)
        if not isinstance(diagnostic_owner, str):
            raise TypeError(
                "DiagnosticOwner must be str, got " + type(diagnostic_owner).__name__
            )
        object.__setattr__(self, "diagnostic_owner", diagnostic_owner)
        if not isinstance(diagnostic_field_id, str):
            raise TypeError(
                "DiagnosticFieldId must be str, got "
                + type(diagnostic_field_id).__name__
            )
        object.__setattr__(self, "diagnostic_field_id", diagnostic_field_id)
        if not isinstance(diagnostic_message, str):
            raise TypeError(
                "DiagnosticMessage must be str, got "
                + type(diagnostic_message).__name__
            )
        object.__setattr__(self, "diagnostic_message", diagnostic_message)

    def __setattr__(self, name, value):
        if name in (
            "diagnostic_id",
            "diagnostic_owner",
            "diagnostic_field_id",
            "diagnostic_message",
        ):
            raise AttributeError("DefaultFactoryDiagnostic records are immutable")
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append("diagnostic_id=" + repr(self.diagnostic_id))
        pieces.append("diagnostic_owner=" + repr(self.diagnostic_owner))
        pieces.append("diagnostic_field_id=" + repr(self.diagnostic_field_id))
        pieces.append("diagnostic_message=" + repr(self.diagnostic_message))
        return "DefaultFactoryDiagnostic" + "(" + ", ".join(pieces) + ")"


_DefaultFactoryDiagnosticSpec.bind_record_class(DefaultFactoryDiagnostic)
ClassesCollection = RuntimeCollection(
    "Classes", _LifecycleClassSpec, allows_multiple=True, identity=_ClassIdProperty
)
FieldsCollection = RuntimeCollection(
    "Fields", _LifecycleFieldSpecUnion, allows_multiple=True, identity=_FieldIdProperty
)
TransactionMethodsCollection = RuntimeCollection(
    "TransactionMethods",
    _TransactionMethodSpec,
    allows_multiple=True,
    identity=_MethodIdProperty,
)
FacadeClassesCollection = RuntimeCollection(
    "FacadeClasses",
    _FacadeClassSpec,
    allows_multiple=True,
    identity=(_FacadeOwnerProperty, _FacadeIdProperty),
)
FacadeExposuresCollection = RuntimeCollection(
    "FacadeExposures",
    _FacadeExposureSpec,
    allows_multiple=True,
    identity=(_FacadeOwnerProperty, _OwnerFacadeIdProperty, _FieldNameProperty),
)
InitParametersCollection = RuntimeCollection(
    "InitParameters",
    _InitParameterSpec,
    allows_multiple=True,
    identity=_InitParameterIdProperty,
)
InitAssignmentsCollection = RuntimeCollection(
    "InitAssignments",
    _InitAssignmentSpec,
    allows_multiple=True,
    identity=_InitAssignmentIdProperty,
)
ClassVarAssignmentsCollection = RuntimeCollection(
    "ClassVarAssignments",
    _ClassVarAssignmentSpec,
    allows_multiple=True,
    identity=_ClassVarAssignmentIdProperty,
)
TransactionalFieldsCollection = RuntimeCollection(
    "TransactionalFields",
    _TransactionalFieldSpec,
    allows_multiple=True,
    identity=_FieldIdProperty,
)
TxGroupsCollection = RuntimeCollection(
    "TxGroups",
    _TxGroupSpec,
    allows_multiple=True,
    identity=(_TxOwnerProperty, _TxGroupKeyProperty),
)
IndexedTransactionalFieldsCollection = RuntimeCollection(
    "IndexedTransactionalFields",
    _IndexedTransactionalFieldSpec,
    allows_multiple=True,
    identity=_FieldIdProperty,
)
DefaultFactoryDependenciesCollection = RuntimeCollection(
    "DefaultFactoryDependencies",
    _DefaultFactoryDependencySpec,
    allows_multiple=True,
    identity=(_ConsumerFieldIdProperty, _ParamNameProperty),
)
DefaultFactoryEvaluationStepsCollection = RuntimeCollection(
    "DefaultFactoryEvaluationSteps",
    _DefaultFactoryEvaluationStepSpec,
    allows_multiple=True,
    identity=_EvalStepIdProperty,
)
DefaultFactoryDiagnosticsCollection = RuntimeCollection(
    "DefaultFactoryDiagnostics",
    _DefaultFactoryDiagnosticSpec,
    allows_multiple=True,
    identity=_DiagnosticIdProperty,
)
PlainFieldsCollection = RuntimeComputedCollection(
    "PlainFields", source=FieldsCollection, when=(_FieldKindProperty.eq("field"),)
)
InitVarFieldsCollection = RuntimeComputedCollection(
    "InitVarFields", source=FieldsCollection, when=(_FieldKindProperty.eq("initvar"),)
)
ClassVarFieldsCollection = RuntimeComputedCollection(
    "ClassVarFields", source=FieldsCollection, when=(_FieldKindProperty.eq("classvar"),)
)
CommitOrderKeyProvidersCollection = RuntimeComputedCollection(
    "CommitOrderKeyProviders",
    source=TransactionMethodsCollection,
    when=(_MethodKindProperty.eq("commit_order_key"),),
)
CommitValidatorsCollection = RuntimeComputedCollection(
    "CommitValidators",
    source=TransactionMethodsCollection,
    when=(_MethodKindProperty.eq("validate_commit"),),
)
BeforeCommitHooksCollection = RuntimeComputedCollection(
    "BeforeCommitHooks",
    source=TransactionMethodsCollection,
    when=(_MethodKindProperty.eq("before_commit"),),
)
AfterCommitHooksCollection = RuntimeComputedCollection(
    "AfterCommitHooks",
    source=TransactionMethodsCollection,
    when=(_MethodKindProperty.eq("after_commit"),),
)
AfterRollbackHooksCollection = RuntimeComputedCollection(
    "AfterRollbackHooks",
    source=TransactionMethodsCollection,
    when=(_MethodKindProperty.eq("after_rollback"),),
)
ManagedFieldsCollection = RuntimeComputedCollection(
    "ManagedFields", source=FieldsCollection, when=(_FieldKindProperty.eq("managed"),)
)
_RUNTIME_SPEC = RuntimeContainerSpec(
    collections=(
        ClassesCollection,
        FieldsCollection,
        TransactionMethodsCollection,
        FacadeClassesCollection,
        FacadeExposuresCollection,
        InitParametersCollection,
        InitAssignmentsCollection,
        ClassVarAssignmentsCollection,
        TransactionalFieldsCollection,
        TxGroupsCollection,
        IndexedTransactionalFieldsCollection,
        DefaultFactoryDependenciesCollection,
        DefaultFactoryEvaluationStepsCollection,
        DefaultFactoryDiagnosticsCollection,
    ),
    computed_collections=(
        PlainFieldsCollection,
        InitVarFieldsCollection,
        ClassVarFieldsCollection,
        CommitOrderKeyProvidersCollection,
        CommitValidatorsCollection,
        BeforeCommitHooksCollection,
        AfterCommitHooksCollection,
        AfterRollbackHooksCollection,
        ManagedFieldsCollection,
    ),
    ports=(),
    port_index=None,
)


def run_build_transaction_facts(builder):
    ctx = DDSOperationContext(builder, "BuildTransactionFacts", ordered_inputs={})
    from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION

    classes = sorted(ctx.records(ClassesCollection), key=lambda item: item.class_order)
    fields = sorted(ctx.records(FieldsCollection), key=lambda item: item.field_order)
    for lifecycle_class in classes:
        seen = {DEFAULT_TRANSACTION: 0}
        ctx.write(
            TxGroupsCollection,
            TxGroup(
                tx_owner=lifecycle_class.class_id,
                tx_group_key=DEFAULT_TRANSACTION,
                tx_index=0,
                tx_group_order=0,
                prepare_commit_fields_function_name="_prepare_commit_tx_0_fields",
                apply_prepared_commit_fields_function_name="_apply_prepared_commit_tx_0_fields",
                rollback_fields_function_name="_rollback_tx_0_fields",
            ),
            policy=RejectDuplicate,
        )
        for field in fields:
            if field.field_owner != lifecycle_class.class_id:
                continue
            if field.field_kind != "managed":
                continue
            tx_group = field.tx_group_key
            if tx_group is None:
                tx_group = DEFAULT_TRANSACTION
            if tx_group not in seen:
                seen[tx_group] = len(seen)
                ctx.write(
                    TxGroupsCollection,
                    TxGroup(
                        tx_owner=lifecycle_class.class_id,
                        tx_group_key=tx_group,
                        tx_index=seen[tx_group],
                        tx_group_order=field.field_order,
                        prepare_commit_fields_function_name=f"_prepare_commit_tx_{seen[tx_group]}_fields",
                        apply_prepared_commit_fields_function_name=f"_apply_prepared_commit_tx_{seen[tx_group]}_fields",
                        rollback_fields_function_name=f"_rollback_tx_{seen[tx_group]}_fields",
                    ),
                    policy=RejectDuplicate,
                )
            tx_index = seen[tx_group]
            ctx.write(
                TransactionalFieldsCollection,
                TransactionalField(
                    field_id=field.field_id,
                    field_owner=field.field_owner,
                    field_name=field.field_name,
                    field_order=field.field_order,
                    tx_group_key=tx_group,
                ),
                policy=RejectDuplicate,
            )
            ctx.write(
                IndexedTransactionalFieldsCollection,
                IndexedTransactionalField(
                    field_id=field.field_id,
                    field_owner=field.field_owner,
                    field_name=field.field_name,
                    field_order=field.field_order,
                    tx_group_key=tx_group,
                    tx_index=tx_index,
                    current_slot_name=field.current_slot_name,
                    working_slot_name=field.working_slot_name,
                    staged_slot_name=field.staged_slot_name,
                    has_freeze=field.has_freeze,
                    freeze_param_name=field.freeze_param_name,
                    has_thaw=field.has_thaw,
                    thaw_param_name=field.thaw_param_name,
                    has_optional_none=field.has_optional_none,
                ),
                policy=RejectDuplicate,
            )


def run_build_default_factory_facts(builder):
    ctx = DDSOperationContext(builder, "BuildDefaultFactoryFacts", ordered_inputs={})
    classes = sorted(ctx.records(ClassesCollection), key=lambda item: item.class_order)
    fields = sorted(ctx.records(FieldsCollection), key=lambda item: item.field_order)
    for lifecycle_class in classes:
        class_fields = [
            field for field in fields if field.field_owner == lifecycle_class.class_id
        ]
        by_name = {field.field_name: field for field in class_fields}
        by_id = {field.field_id: field for field in class_fields}
        factory_fields = [field for field in class_fields if field.has_default_factory]
        graph = {field.field_id: set() for field in factory_fields}
        deps = []
        diagnostic_count = 0

        def add_diagnostic(field, suffix, message):
            nonlocal diagnostic_count
            diagnostic_count += 1
            ctx.write(
                DefaultFactoryDiagnosticsCollection,
                DefaultFactoryDiagnostic(
                    diagnostic_id=f"{field.field_id}.{suffix}.{diagnostic_count}",
                    diagnostic_owner=lifecycle_class.class_id,
                    diagnostic_field_id=field.field_id,
                    diagnostic_message=message,
                ),
                policy=ReplaceExisting,
            )

        def provider_is_available(provider):
            if provider.init:
                return True
            return provider.has_default or provider.has_default_factory

        for consumer in factory_fields:
            for param_order, param_name in enumerate(
                consumer.default_factory_param_names
            ):
                provider = by_name.get(param_name)
                if provider is None:
                    add_diagnostic(
                        consumer,
                        f"unknown.{param_name}",
                        f"{lifecycle_class.class_name}.{consumer.field_name}: default_factory references unknown name {param_name!r}",
                    )
                    continue
                if not provider_is_available(provider):
                    add_diagnostic(
                        consumer,
                        f"unavailable.{param_name}",
                        f"{lifecycle_class.class_name}.{consumer.field_name}: default_factory cannot reference {param_name!r} (value is unavailable before factory evaluation)",
                    )
                    continue
                deps.append((consumer, provider, param_name, param_order))
                if provider.field_id in graph:
                    graph[consumer.field_id].add(provider.field_id)
        field_order = {field.field_id: field.field_order for field in class_fields}
        visiting = set()
        visited = set()
        ordered_field_ids = []
        cycle_found = False

        def visit(field_id, path):
            nonlocal cycle_found
            if cycle_found or field_id in visited:
                return
            if field_id in visiting:
                cycle = path[path.index(field_id) :]
                names = " -> ".join((by_id[item].field_name for item in cycle))
                add_diagnostic(
                    by_id[field_id],
                    "cycle",
                    f"{lifecycle_class.class_name}: default_factory dependency cycle: {names}",
                )
                cycle_found = True
                return
            visiting.add(field_id)
            for provider_id in sorted(
                graph.get(field_id, ()), key=lambda item: field_order[item]
            ):
                visit(provider_id, [*path, provider_id])
            visiting.remove(field_id)
            visited.add(field_id)
            ordered_field_ids.append(field_id)

        for field in factory_fields:
            visit(field.field_id, [field.field_id])
            if cycle_found:
                break
        if diagnostic_count:
            continue
        eval_order_by_id = {
            field_id: eval_order
            for eval_order, field_id in enumerate(ordered_field_ids)
        }
        for consumer, provider, param_name, param_order in deps:
            ctx.write(
                DefaultFactoryDependenciesCollection,
                DefaultFactoryDependency(
                    dependency_owner=lifecycle_class.class_id,
                    consumer_field_id=consumer.field_id,
                    consumer_field_name=consumer.field_name,
                    provider_name=provider.field_name,
                    provider_field_id=provider.field_id,
                    provider_field_kind=provider.field_kind,
                    provider_init=provider.init,
                    provider_has_default=provider.has_default,
                    provider_has_default_factory=provider.has_default_factory,
                    param_name=param_name,
                    param_order=param_order,
                    consumer_eval_order=eval_order_by_id[consumer.field_id],
                ),
                policy=RejectDuplicate,
            )
        for eval_order, field_id in enumerate(ordered_field_ids):
            field = by_id[field_id]
            state_slot = ""
            if field.field_kind == "field":
                state_slot = field.value_slot_name
            elif field.field_kind == "managed":
                state_slot = field.current_slot_name
            ctx.write(
                DefaultFactoryEvaluationStepsCollection,
                DefaultFactoryEvaluationStep(
                    eval_step_id=field.field_id,
                    eval_owner=lifecycle_class.class_id,
                    eval_field_id=field.field_id,
                    eval_field_name=field.field_name,
                    eval_field_kind=field.field_kind,
                    eval_init=field.init,
                    eval_state_slot_name=state_slot,
                    eval_default_factory_param_name=field.default_factory_param_name,
                    eval_order=eval_order,
                    eval_statement_order=100000 + eval_order,
                ),
                policy=RejectDuplicate,
            )


def run_raise_default_factory_diagnostics(builder):
    ctx = DDSOperationContext(
        builder, "RaiseDefaultFactoryDiagnostics", ordered_inputs={}
    )
    for diagnostic in ctx.records(DefaultFactoryDiagnosticsCollection):
        raise AssemblyDiagnosticError(diagnostic.diagnostic_message)


def run_operations(builder):
    run_build_transaction_facts(builder)
    run_build_default_factory_facts(builder)
    run_raise_default_factory_diagnostics(builder)
    return builder


def build_container(builder):
    run_operations(builder)
    return builder.freeze()


class _GeneratedMatcherNamespace:

    def __init__(self, container):
        pass


class _GeneratedContainerBuilder:

    def __init__(self):
        self._builder = DDSContainerBuilder(_RUNTIME_SPEC)

    def add(self, *args, **kwargs):
        self._builder.add(*args, **kwargs)
        return self

    def write(self, *args, **kwargs):
        self._builder.write(*args, **kwargs)
        return self

    def children_at(self, port_address):
        return self._builder.children_at(port_address)

    def _snapshot(self):
        container = self._builder._snapshot()
        container.matchers = _GeneratedMatcherNamespace(container)
        return container

    def record(self, *args, **kwargs):
        return self._builder.record(*args, **kwargs)

    def freeze(self):
        container = self._builder.freeze()
        container.matchers = _GeneratedMatcherNamespace(container)
        return container

    def __getattr__(self, name):
        return getattr(self._builder, name)


def new_builder():
    return _GeneratedContainerBuilder()


from types import SimpleNamespace as _YidlSimpleNamespace
from yidl.generation.assembly_plan import (
    AndConditionSpec,
    AssemblyEdgeSpec,
    AssemblyInputSpec,
    AssemblySpec,
    BindingSpec,
    ComposableProductionSpec,
    ContributionMatcherSpec,
    ContributionRuleSpec,
    ContributionSpec,
    EdgeApplySpec,
    EqConditionSpec,
    InlineApplySpec,
    LiteralValueRef,
    PathSegmentSpec,
    PathSpec,
    RootSpec,
    TargetPathSpec,
    TargetSpec,
    TupleValueRef,
    ValueRef,
)
from yidl.generation.assembly_runtime import run_assembly
from yidl.generation.matcher_values import (
    astichi_template,
    from_astichi_code,
    from_import,
)

ASSEMBLY_PROPERTIES = {
    "ClassId": _YidlSimpleNamespace(name="ClassId", storage_name="class_id"),
    "ClassName": _YidlSimpleNamespace(name="ClassName", storage_name="class_name"),
    "ClassOrder": _YidlSimpleNamespace(name="ClassOrder", storage_name="class_order"),
    "ModuleName": _YidlSimpleNamespace(name="ModuleName", storage_name="module_name"),
    "StateClassName": _YidlSimpleNamespace(
        name="StateClassName", storage_name="state_class_name"
    ),
    "FacadeBaseClassName": _YidlSimpleNamespace(
        name="FacadeBaseClassName", storage_name="facade_base_class_name"
    ),
    "CurrentFacadeClassName": _YidlSimpleNamespace(
        name="CurrentFacadeClassName", storage_name="current_facade_class_name"
    ),
    "WorkingFacadeClassName": _YidlSimpleNamespace(
        name="WorkingFacadeClassName", storage_name="working_facade_class_name"
    ),
    "LifecycleDefinitionParamName": _YidlSimpleNamespace(
        name="LifecycleDefinitionParamName",
        storage_name="lifecycle_definition_param_name",
    ),
    "AnnotationsParamName": _YidlSimpleNamespace(
        name="AnnotationsParamName", storage_name="annotations_param_name"
    ),
    "TxGroupsParamName": _YidlSimpleNamespace(
        name="TxGroupsParamName", storage_name="tx_groups_param_name"
    ),
    "LifecycleFieldNames": _YidlSimpleNamespace(
        name="LifecycleFieldNames", storage_name="lifecycle_field_names"
    ),
    "FieldId": _YidlSimpleNamespace(name="FieldId", storage_name="field_id"),
    "FieldOwner": _YidlSimpleNamespace(name="FieldOwner", storage_name="field_owner"),
    "FieldName": _YidlSimpleNamespace(name="FieldName", storage_name="field_name"),
    "FieldOrder": _YidlSimpleNamespace(name="FieldOrder", storage_name="field_order"),
    "FieldKind": _YidlSimpleNamespace(name="FieldKind", storage_name="field_kind"),
    "Annotation": _YidlSimpleNamespace(name="Annotation", storage_name="annotation"),
    "Init": _YidlSimpleNamespace(name="Init", storage_name="init"),
    "HasDefault": _YidlSimpleNamespace(name="HasDefault", storage_name="has_default"),
    "DefaultValue": _YidlSimpleNamespace(
        name="DefaultValue", storage_name="default_value"
    ),
    "DefaultValueParamName": _YidlSimpleNamespace(
        name="DefaultValueParamName", storage_name="default_value_param_name"
    ),
    "HasDefaultFactory": _YidlSimpleNamespace(
        name="HasDefaultFactory", storage_name="has_default_factory"
    ),
    "DefaultFactory": _YidlSimpleNamespace(
        name="DefaultFactory", storage_name="default_factory"
    ),
    "DefaultFactoryParamName": _YidlSimpleNamespace(
        name="DefaultFactoryParamName", storage_name="default_factory_param_name"
    ),
    "DefaultFactoryParamNames": _YidlSimpleNamespace(
        name="DefaultFactoryParamNames", storage_name="default_factory_param_names"
    ),
    "TxGroupKey": _YidlSimpleNamespace(name="TxGroupKey", storage_name="tx_group_key"),
    "ValueSlotName": _YidlSimpleNamespace(
        name="ValueSlotName", storage_name="value_slot_name"
    ),
    "CurrentSlotName": _YidlSimpleNamespace(
        name="CurrentSlotName", storage_name="current_slot_name"
    ),
    "WorkingSlotName": _YidlSimpleNamespace(
        name="WorkingSlotName", storage_name="working_slot_name"
    ),
    "StagedSlotName": _YidlSimpleNamespace(
        name="StagedSlotName", storage_name="staged_slot_name"
    ),
    "HasFreeze": _YidlSimpleNamespace(name="HasFreeze", storage_name="has_freeze"),
    "Freeze": _YidlSimpleNamespace(name="Freeze", storage_name="freeze"),
    "FreezeParamName": _YidlSimpleNamespace(
        name="FreezeParamName", storage_name="freeze_param_name"
    ),
    "HasThaw": _YidlSimpleNamespace(name="HasThaw", storage_name="has_thaw"),
    "Thaw": _YidlSimpleNamespace(name="Thaw", storage_name="thaw"),
    "ThawParamName": _YidlSimpleNamespace(
        name="ThawParamName", storage_name="thaw_param_name"
    ),
    "HasOptionalNone": _YidlSimpleNamespace(
        name="HasOptionalNone", storage_name="has_optional_none"
    ),
    "MethodId": _YidlSimpleNamespace(name="MethodId", storage_name="method_id"),
    "MethodOwner": _YidlSimpleNamespace(
        name="MethodOwner", storage_name="method_owner"
    ),
    "MethodName": _YidlSimpleNamespace(name="MethodName", storage_name="method_name"),
    "MethodKind": _YidlSimpleNamespace(name="MethodKind", storage_name="method_kind"),
    "DeclarationOrder": _YidlSimpleNamespace(
        name="DeclarationOrder", storage_name="declaration_order"
    ),
    "TxIndex": _YidlSimpleNamespace(name="TxIndex", storage_name="tx_index"),
    "FacadeId": _YidlSimpleNamespace(name="FacadeId", storage_name="facade_id"),
    "FacadeOwner": _YidlSimpleNamespace(
        name="FacadeOwner", storage_name="facade_owner"
    ),
    "FacadeKind": _YidlSimpleNamespace(name="FacadeKind", storage_name="facade_kind"),
    "FacadeMode": _YidlSimpleNamespace(name="FacadeMode", storage_name="facade_mode"),
    "FacadeClassName": _YidlSimpleNamespace(
        name="FacadeClassName", storage_name="facade_class_name"
    ),
    "FacadeOrder": _YidlSimpleNamespace(
        name="FacadeOrder", storage_name="facade_order"
    ),
    "OwnerFacadeId": _YidlSimpleNamespace(
        name="OwnerFacadeId", storage_name="owner_facade_id"
    ),
    "TargetFacadeId": _YidlSimpleNamespace(
        name="TargetFacadeId", storage_name="target_facade_id"
    ),
    "ExposureOrder": _YidlSimpleNamespace(
        name="ExposureOrder", storage_name="exposure_order"
    ),
    "InitParameterId": _YidlSimpleNamespace(
        name="InitParameterId", storage_name="init_parameter_id"
    ),
    "InitParameterOwner": _YidlSimpleNamespace(
        name="InitParameterOwner", storage_name="init_parameter_owner"
    ),
    "InitParameterName": _YidlSimpleNamespace(
        name="InitParameterName", storage_name="init_parameter_name"
    ),
    "InitParameterOrder": _YidlSimpleNamespace(
        name="InitParameterOrder", storage_name="init_parameter_order"
    ),
    "InitParameterKind": _YidlSimpleNamespace(
        name="InitParameterKind", storage_name="init_parameter_kind"
    ),
    "InitAssignmentId": _YidlSimpleNamespace(
        name="InitAssignmentId", storage_name="init_assignment_id"
    ),
    "InitAssignmentOwner": _YidlSimpleNamespace(
        name="InitAssignmentOwner", storage_name="init_assignment_owner"
    ),
    "InitAssignmentFieldId": _YidlSimpleNamespace(
        name="InitAssignmentFieldId", storage_name="init_assignment_field_id"
    ),
    "InitAssignmentFieldName": _YidlSimpleNamespace(
        name="InitAssignmentFieldName", storage_name="init_assignment_field_name"
    ),
    "InitAssignmentOrder": _YidlSimpleNamespace(
        name="InitAssignmentOrder", storage_name="init_assignment_order"
    ),
    "InitAssignmentKind": _YidlSimpleNamespace(
        name="InitAssignmentKind", storage_name="init_assignment_kind"
    ),
    "ClassVarAssignmentId": _YidlSimpleNamespace(
        name="ClassVarAssignmentId", storage_name="class_var_assignment_id"
    ),
    "ClassVarAssignmentOwner": _YidlSimpleNamespace(
        name="ClassVarAssignmentOwner", storage_name="class_var_assignment_owner"
    ),
    "ClassVarAssignmentName": _YidlSimpleNamespace(
        name="ClassVarAssignmentName", storage_name="class_var_assignment_name"
    ),
    "ClassVarAssignmentOrder": _YidlSimpleNamespace(
        name="ClassVarAssignmentOrder", storage_name="class_var_assignment_order"
    ),
    "TxGroupOrder": _YidlSimpleNamespace(
        name="TxGroupOrder", storage_name="tx_group_order"
    ),
    "TxOwner": _YidlSimpleNamespace(name="TxOwner", storage_name="tx_owner"),
    "PrepareCommitFieldsFunctionName": _YidlSimpleNamespace(
        name="PrepareCommitFieldsFunctionName",
        storage_name="prepare_commit_fields_function_name",
    ),
    "ApplyPreparedCommitFieldsFunctionName": _YidlSimpleNamespace(
        name="ApplyPreparedCommitFieldsFunctionName",
        storage_name="apply_prepared_commit_fields_function_name",
    ),
    "RollbackFieldsFunctionName": _YidlSimpleNamespace(
        name="RollbackFieldsFunctionName", storage_name="rollback_fields_function_name"
    ),
    "DependencyOwner": _YidlSimpleNamespace(
        name="DependencyOwner", storage_name="dependency_owner"
    ),
    "ConsumerFieldId": _YidlSimpleNamespace(
        name="ConsumerFieldId", storage_name="consumer_field_id"
    ),
    "ConsumerFieldName": _YidlSimpleNamespace(
        name="ConsumerFieldName", storage_name="consumer_field_name"
    ),
    "ProviderName": _YidlSimpleNamespace(
        name="ProviderName", storage_name="provider_name"
    ),
    "ProviderFieldId": _YidlSimpleNamespace(
        name="ProviderFieldId", storage_name="provider_field_id"
    ),
    "ProviderFieldKind": _YidlSimpleNamespace(
        name="ProviderFieldKind", storage_name="provider_field_kind"
    ),
    "ProviderInit": _YidlSimpleNamespace(
        name="ProviderInit", storage_name="provider_init"
    ),
    "ProviderHasDefault": _YidlSimpleNamespace(
        name="ProviderHasDefault", storage_name="provider_has_default"
    ),
    "ProviderHasDefaultFactory": _YidlSimpleNamespace(
        name="ProviderHasDefaultFactory", storage_name="provider_has_default_factory"
    ),
    "ParamName": _YidlSimpleNamespace(name="ParamName", storage_name="param_name"),
    "ParamOrder": _YidlSimpleNamespace(name="ParamOrder", storage_name="param_order"),
    "ConsumerEvalOrder": _YidlSimpleNamespace(
        name="ConsumerEvalOrder", storage_name="consumer_eval_order"
    ),
    "EvalStepId": _YidlSimpleNamespace(name="EvalStepId", storage_name="eval_step_id"),
    "EvalOwner": _YidlSimpleNamespace(name="EvalOwner", storage_name="eval_owner"),
    "EvalFieldId": _YidlSimpleNamespace(
        name="EvalFieldId", storage_name="eval_field_id"
    ),
    "EvalFieldName": _YidlSimpleNamespace(
        name="EvalFieldName", storage_name="eval_field_name"
    ),
    "EvalFieldKind": _YidlSimpleNamespace(
        name="EvalFieldKind", storage_name="eval_field_kind"
    ),
    "EvalInit": _YidlSimpleNamespace(name="EvalInit", storage_name="eval_init"),
    "EvalStateSlotName": _YidlSimpleNamespace(
        name="EvalStateSlotName", storage_name="eval_state_slot_name"
    ),
    "EvalDefaultFactoryParamName": _YidlSimpleNamespace(
        name="EvalDefaultFactoryParamName",
        storage_name="eval_default_factory_param_name",
    ),
    "EvalOrder": _YidlSimpleNamespace(name="EvalOrder", storage_name="eval_order"),
    "EvalStatementOrder": _YidlSimpleNamespace(
        name="EvalStatementOrder", storage_name="eval_statement_order"
    ),
    "DiagnosticId": _YidlSimpleNamespace(
        name="DiagnosticId", storage_name="diagnostic_id"
    ),
    "DiagnosticOwner": _YidlSimpleNamespace(
        name="DiagnosticOwner", storage_name="diagnostic_owner"
    ),
    "DiagnosticFieldId": _YidlSimpleNamespace(
        name="DiagnosticFieldId", storage_name="diagnostic_field_id"
    ),
    "DiagnosticMessage": _YidlSimpleNamespace(
        name="DiagnosticMessage", storage_name="diagnostic_message"
    ),
}
ASSEMBLY_RESOURCES = {
    "ModuleRoot": from_astichi_code(
        """\
from __future__ import annotations

import weakref

from yidl.runtime.lifecycle import _HAS_DEFAULT_FACTORY
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION
from yidl.runtime.transaction_yidl import TransactionManager


VOID = object()


def build_lifecycle_class(decorated_cls, builder_params__astichi_param_hole__):
    astichi_hole(function_body)
    astichi_hole(return_statement)""",
        file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl",
        line_number=205,
    ),
    "BuilderParam": astichi_template(
        from_astichi_code(
            """\
def astichi_params(*, value_name__astichi_arg__):
    pass""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl",
            line_number=223,
        )
    ),
    "TransactionManagerParam": astichi_template(
        from_astichi_code(
            """\
def astichi_params(*, transaction_manager=None):
    pass""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl",
            line_number=228,
        )
    ),
    "StateSlotEntry": astichi_template(
        from_astichi_code(
            "astichi_bind_external(slot_name)",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl",
            line_number=233,
        )
    ),
    "InitParamRequired": astichi_template(
        from_astichi_code(
            """\
def astichi_params(param_name__astichi_arg__: astichi_bind_external(annotation)):
    pass""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl",
            line_number=237,
        )
    ),
    "InitParamDefault": astichi_template(
        from_astichi_code(
            """\
def astichi_params(
    param_name__astichi_arg__: astichi_bind_external(annotation)
    = default_value_name__astichi_arg__
):
    pass""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl",
            line_number=242,
        )
    ),
    "PlainStateAssignment": astichi_template(
        from_astichi_code(
            """\
astichi_pass(state, outer_bind=True).astichi_ref(external=state_slot)._ = astichi_pass(
    init_value_name__astichi_arg__,
    outer_bind=True,
)""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl",
            line_number=250,
        )
    ),
    "InitVarLocalDefaultAssignment": astichi_template(
        from_astichi_code(
            """\
init_value_name__astichi_arg__ = astichi_pass(
    default_value_name__astichi_arg__,
    outer_bind=True,
)""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl",
            line_number=257,
        )
    ),
    "PlainProperty": astichi_template(
        from_astichi_code(
            """\
@property
def property_getter_name__astichi_arg__(self):
    return self._y_state.astichi_ref(external=state_slot)

@property_setter_target_name__astichi_arg__.setter
def property_setter_name__astichi_arg__(self, value):
    self._y_state.astichi_ref(external=state_slot)._ = value""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl",
            line_number=264,
        )
    ),
    "ClassVarDefaultAssignment": astichi_template(
        from_astichi_code(
            """\
classvar_name__astichi_arg__ = astichi_pass(
    classvar_value_name__astichi_arg__,
    outer_bind=True,
)""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl",
            line_number=274,
        )
    ),
    "CommitOrderKeyBranch": astichi_template(
        from_astichi_code(
            """\
if astichi_pass(tx_index, outer_bind=True) == astichi_bind_external(tx_index_value):
    return astichi_pass(
        self,
        outer_bind=True,
    )._y_get_default_facade().astichi_ref(external=method_name)()""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl",
            line_number=281,
        )
    ),
    "RequiresValidationBranch": astichi_template(
        from_astichi_code(
            """\
if astichi_pass(tx_index, outer_bind=True) == astichi_bind_external(tx_index_value):
    return True""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl",
            line_number=289,
        )
    ),
    "ValidateCommitBranch": astichi_template(
        from_astichi_code(
            """\
if astichi_pass(tx_index, outer_bind=True) == astichi_bind_external(tx_index_value):
    result = astichi_pass(
        self,
        outer_bind=True,
    )._y_get_default_facade().astichi_ref(external=method_name)()
    if result is False:
        return False""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl",
            line_number=294,
        )
    ),
    "TransactionHookCall": astichi_template(
        from_astichi_code(
            """\
if astichi_pass(tx_index, outer_bind=True) == astichi_bind_external(tx_index_value):
    astichi_pass(
        self,
        outer_bind=True,
    )._y_get_default_facade().astichi_ref(external=method_name)()""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl",
            line_number=304,
        )
    ),
    "ClassBundle": astichi_template(
        from_astichi_code(
            """\
class state_class_decl_name__astichi_arg__:
    __slots__ = (
        "_y_transaction_manager",
        "_y_default_ref",
        "_y_current_ref",
        "_y_working_ref",
        *astichi_hole(state_slots),
        "_y_working_tx_ids",
    )
    __yidl_tx_index_to_group__ = astichi_pass(
        tx_groups_for_index_name__astichi_arg__,
        outer_bind=True,
    )
    __yidl_tx_group_to_index__ = {
        group: index for index, group in enumerate(
            astichi_pass(tx_groups_for_map_name__astichi_arg__, outer_bind=True)
        )
    }

    def _y_get_default_facade(self):
        ref = self._y_default_ref
        facade = None if ref is None else ref()
        if facade is None:
            facade = object.__new__(default_facade_class_ref__astichi_arg__)
            object.__setattr__(facade, "_y_state", self)
            current_ref = self._y_current_ref
            working_ref = self._y_working_ref
            object.__setattr__(
                facade,
                "_y_current_facade",
                None if current_ref is None else current_ref(),
            )
            object.__setattr__(
                facade,
                "_y_working_facade",
                None if working_ref is None else working_ref(),
            )
            self._y_default_ref = weakref.ref(facade)
        return facade

    def _y_get_current_facade(self):
        default_ref = self._y_default_ref
        default = None if default_ref is None else default_ref()
        if default is not None:
            facade = default._y_current_facade
            if facade is None:
                facade = object.__new__(current_facade_class_ref__astichi_arg__)
                object.__setattr__(facade, "_y_state", self)
                object.__setattr__(default, "_y_current_facade", facade)
                self._y_current_ref = weakref.ref(facade)
            return facade
        ref = self._y_current_ref
        facade = None if ref is None else ref()
        if facade is None:
            facade = object.__new__(current_facade_class_ref__astichi_arg__)
            object.__setattr__(facade, "_y_state", self)
            self._y_current_ref = weakref.ref(facade)
        return facade

    def _y_get_working_facade(self):
        default_ref = self._y_default_ref
        default = None if default_ref is None else default_ref()
        if default is not None:
            facade = default._y_working_facade
            if facade is None:
                facade = object.__new__(working_facade_class_ref__astichi_arg__)
                object.__setattr__(facade, "_y_state", self)
                object.__setattr__(default, "_y_working_facade", facade)
                self._y_working_ref = weakref.ref(facade)
            return facade
        ref = self._y_working_ref
        facade = None if ref is None else ref()
        if facade is None:
            facade = object.__new__(working_facade_class_ref__astichi_arg__)
            object.__setattr__(facade, "_y_state", self)
            self._y_working_ref = weakref.ref(facade)
        return facade

    def _y_require_active_transaction(self, tx_index):
        tx_group = self.__yidl_tx_index_to_group__[tx_index]
        transaction = self._y_transaction_manager.active_transaction_for(tx_group)
        if transaction is None:
            if self._y_working_tx_ids[tx_index] is not None:
                raise RuntimeError(
                    "stale yidl working value without an active transaction"
                )
            raise RuntimeError("writes require an active yidl transaction")
        existing_tx_id = self._y_working_tx_ids[tx_index]
        if existing_tx_id is not None and existing_tx_id != transaction.tx_id:
            raise RuntimeError(
                "working value belongs to a different yidl transaction"
            )
        return transaction

    def _y_ensure_working_transaction(self, tx_index):
        transaction = self._y_require_active_transaction(tx_index)
        if self._y_working_tx_ids[tx_index] is None:
            tx_group = self.__yidl_tx_index_to_group__[tx_index]
            self._y_working_tx_ids[tx_index] = (
                self._y_transaction_manager.enlist(self, tx_group)
            )
        return transaction

    def commit_order_key_for(self, tx_group=DEFAULT_TRANSACTION):
        tx_index = self.__yidl_tx_group_to_index__[tx_group]
        astichi_hole(commit_order_key_body)
        return ()

    def requires_validation_for(self, tx_group=DEFAULT_TRANSACTION):
        tx_index = self.__yidl_tx_group_to_index__[tx_group]
        astichi_hole(requires_validation_body)
        return False

    def validate_commit_for(self, tx_group=DEFAULT_TRANSACTION):
        tx_index = self.__yidl_tx_group_to_index__[tx_group]
        astichi_hole(validate_commit_body)
        return True

    def _prepare_commit_tx_by_key(self, tx_group=DEFAULT_TRANSACTION, tx_token=None):
        tx_index = self.__yidl_tx_group_to_index__[tx_group]
        if self._y_working_tx_ids[tx_index] != tx_token:
            raise RuntimeError("stale yidl transaction token")
        astichi_hole(before_commit_body)
        astichi_hole(prepare_commit_transaction_dispatch_body)
        return self._y_get_default_facade()

    def _apply_prepared_commit_tx_by_key(self, tx_group=DEFAULT_TRANSACTION, tx_token=None):
        tx_index = self.__yidl_tx_group_to_index__[tx_group]
        if self._y_working_tx_ids[tx_index] != tx_token:
            raise RuntimeError("stale yidl transaction token")
        astichi_hole(commit_transaction_dispatch_body)
        astichi_hole(commit_transaction_body)
        self._y_working_tx_ids[tx_index] = None
        return self._y_get_default_facade()

    def _after_commit_tx_by_key(self, tx_group=DEFAULT_TRANSACTION, tx_token=None):
        del tx_token
        tx_index = self.__yidl_tx_group_to_index__[tx_group]
        astichi_hole(after_commit_body)
        return self._y_get_default_facade()

    def _rollback_tx_by_key(self, tx_group=DEFAULT_TRANSACTION, tx_token=None):
        tx_index = self.__yidl_tx_group_to_index__[tx_group]
        del tx_token
        astichi_hole(rollback_transaction_dispatch_body)
        astichi_hole(rollback_transaction_body)
        self._y_working_tx_ids[tx_index] = None
        return self._y_get_default_facade()

    def _after_rollback_tx_by_key(self, tx_group=DEFAULT_TRANSACTION, tx_token=None):
        del tx_token
        tx_index = self.__yidl_tx_group_to_index__[tx_group]
        astichi_hole(after_rollback_body)
        return self._y_get_default_facade()

    astichi_hole(commit_transaction_helpers)
    astichi_hole(rollback_transaction_helpers)


class facade_base_decl_name__astichi_arg__(
    astichi_pass(decorated_cls, outer_bind=True)
):
    __slots__ = ("_y_state",)
    _y_lifecycle_field_names = frozenset(
        astichi_bind_external(lifecycle_field_names)
    )

    def __setattr__(self, name, value):
        if name in self._y_lifecycle_field_names:
            descriptor = getattr(type(self), name, None)
            if descriptor is None or not hasattr(descriptor, "__set__"):
                raise AttributeError(
                    f"lifecycle field {name!r} is not assignable"
                )
            descriptor.__set__(self, value)
            return
        if name.startswith("_y_") or name.startswith("__yidl_"):
            raise AttributeError(
                f"{name!r} is reserved for generated lifecycle state"
            )
        object.__setattr__(self, name, value)

    def __delattr__(self, name):
        if name in self._y_lifecycle_field_names:
            raise AttributeError(f"lifecycle field {name!r} cannot be deleted")
        if name.startswith("_y_") or name.startswith("__yidl_"):
            raise AttributeError(
                f"{name!r} is reserved for generated lifecycle state"
            )
        object.__delattr__(self, name)

    @property
    def default(self):
        return self._y_state._y_get_default_facade()

    @property
    def current(self):
        return self._y_state._y_get_current_facade()

    @property
    def working(self):
        return self._y_state._y_get_working_facade()

    def begin(self, *tx_groups):
        return self._y_state._y_transaction_manager.begin(*tx_groups)

    def validate(self, *tx_groups):
        return self._y_state._y_transaction_manager.validate(*tx_groups)

    def commit_only(self, *tx_groups):
        return self._y_state._y_transaction_manager.commit_only(*tx_groups)

    def commit(self, *tx_groups):
        return self._y_state._y_transaction_manager.commit(*tx_groups)

    def rollback(self, *tx_groups):
        return self._y_state._y_transaction_manager.rollback(*tx_groups)

    astichi_hole(facade_base_body)
    astichi_hole(facade_properties)


class default_facade_class_decl_name__astichi_arg__(
    facade_base_default_base_name__astichi_arg__
):
    __slots__ = ("_y_current_facade", "_y_working_facade")
    __annotations__ = astichi_pass(
        annotations_name__astichi_arg__,
        outer_bind=True,
    )
    __yidl_lifecycle_generated__ = True
    __yidl_lifecycle_user_class__ = astichi_pass(
        decorated_cls,
        outer_bind=True,
    )
    __yidl_lifecycle_definition__ = astichi_pass(
        lifecycle_definition_name__astichi_arg__,
        outer_bind=True,
    )
    __yidl_tx_index_to_group__ = astichi_pass(
        tx_groups_for_class_index_name__astichi_arg__,
        outer_bind=True,
    )
    __yidl_tx_group_to_index__ = {
        group: index for index, group in enumerate(
            astichi_pass(
                tx_groups_for_class_map_name__astichi_arg__,
                outer_bind=True,
            )
        )
    }

    astichi_hole(default_facade_properties)

    def __init__(self, init_params__astichi_param_hole__):
        state = object.__new__(state_class_ref__astichi_arg__)
        object.__setattr__(self, "_y_state", state)
        object.__setattr__(self, "_y_current_facade", None)
        object.__setattr__(self, "_y_working_facade", None)
        state._y_transaction_manager = transaction_manager or TransactionManager(
            tx_groups=tuple(
                group for group in astichi_pass(
                    tx_groups_for_manager_name__astichi_arg__,
                    outer_bind=True,
                )
                if group != DEFAULT_TRANSACTION
            )
        )
        state._y_default_ref = weakref.ref(self)
        state._y_current_ref = None
        state._y_working_ref = None
        astichi_hole(state_init_body)
        state._y_working_tx_ids = [
            None
            for _group in astichi_pass(
                tx_groups_for_slots_name__astichi_arg__,
                outer_bind=True,
            )
        ]


class current_facade_class_decl_name__astichi_arg__(
    facade_base_current_base_name__astichi_arg__
):
    __slots__ = ()
    astichi_hole(current_facade_properties)


class working_facade_class_decl_name__astichi_arg__(
    facade_base_working_base_name__astichi_arg__
):
    __slots__ = ()
    astichi_hole(working_facade_properties)""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl",
            line_number=312,
            keep_names=(
                "DEFAULT_TRANSACTION",
                "TransactionManager",
                "VOID",
                "weakref",
                "_HAS_DEFAULT_FACTORY",
            ),
        )
    ),
    "ReturnClass": astichi_template(
        from_astichi_code(
            """\
return_class_name_ref__astichi_arg__.__name__ = astichi_pass(
    decorated_cls,
    outer_bind=True,
).__name__
return_class_qualname_ref__astichi_arg__.__qualname__ = astichi_pass(
    decorated_cls,
    outer_bind=True,
).__qualname__
return_class_module_ref__astichi_arg__.__module__ = astichi_pass(
    decorated_cls,
    outer_bind=True,
).__module__
return return_class_result_ref__astichi_arg__""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl",
            line_number=611,
        )
    ),
    "PassStatement": astichi_template(
        from_astichi_code(
            "pass",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl",
            line_number=627,
        )
    ),
    "BuildTransactionFactsBody": from_astichi_code(
        """\
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION

classes = sorted(
    ctx.records(ClassesCollection),
    key=lambda item: item.class_order,
)
fields = sorted(
    ctx.records(FieldsCollection),
    key=lambda item: item.field_order,
)

for lifecycle_class in classes:
    seen = {DEFAULT_TRANSACTION: 0}
    ctx.write(
        TxGroupsCollection,
        TxGroup(
            tx_owner=lifecycle_class.class_id,
            tx_group_key=DEFAULT_TRANSACTION,
            tx_index=0,
            tx_group_order=0,
            prepare_commit_fields_function_name="_prepare_commit_tx_0_fields",
            apply_prepared_commit_fields_function_name="_apply_prepared_commit_tx_0_fields",
            rollback_fields_function_name="_rollback_tx_0_fields",
        ),
        policy=RejectDuplicate,
    )

    for field in fields:
        if field.field_owner != lifecycle_class.class_id:
            continue
        if field.field_kind != "managed":
            continue

        tx_group = field.tx_group_key
        if tx_group is None:
            tx_group = DEFAULT_TRANSACTION
        if tx_group not in seen:
            seen[tx_group] = len(seen)
            ctx.write(
                TxGroupsCollection,
                TxGroup(
                    tx_owner=lifecycle_class.class_id,
                    tx_group_key=tx_group,
                    tx_index=seen[tx_group],
                    tx_group_order=field.field_order,
                    prepare_commit_fields_function_name=(
                        f"_prepare_commit_tx_{seen[tx_group]}_fields"
                    ),
                    apply_prepared_commit_fields_function_name=(
                        f"_apply_prepared_commit_tx_{seen[tx_group]}_fields"
                    ),
                    rollback_fields_function_name=(
                        f"_rollback_tx_{seen[tx_group]}_fields"
                    ),
                ),
                policy=RejectDuplicate,
            )

        tx_index = seen[tx_group]
        ctx.write(
            TransactionalFieldsCollection,
            TransactionalField(
                field_id=field.field_id,
                field_owner=field.field_owner,
                field_name=field.field_name,
                field_order=field.field_order,
                tx_group_key=tx_group,
            ),
            policy=RejectDuplicate,
        )
        ctx.write(
            IndexedTransactionalFieldsCollection,
            IndexedTransactionalField(
                field_id=field.field_id,
                field_owner=field.field_owner,
                field_name=field.field_name,
                field_order=field.field_order,
                tx_group_key=tx_group,
                tx_index=tx_index,
                current_slot_name=field.current_slot_name,
                working_slot_name=field.working_slot_name,
                staged_slot_name=field.staged_slot_name,
                has_freeze=field.has_freeze,
                freeze_param_name=field.freeze_param_name,
                has_thaw=field.has_thaw,
                thaw_param_name=field.thaw_param_name,
                has_optional_none=field.has_optional_none,
            ),
            policy=RejectDuplicate,
        )""",
        file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl",
        line_number=65,
        keep_names=(
            "ctx",
            "ClassesCollection",
            "FieldsCollection",
            "TxGroupsCollection",
            "TransactionalFieldsCollection",
            "IndexedTransactionalFieldsCollection",
            "TxGroup",
            "TransactionalField",
            "IndexedTransactionalField",
            "RejectDuplicate",
        ),
    ),
    "ManagedCurrentStateAssignment": astichi_template(
        from_astichi_code(
            """\
astichi_pass(state, outer_bind=True).astichi_ref(external=current_slot)._ = astichi_pass(
    init_value_name__astichi_arg__,
    outer_bind=True,
)""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl",
            line_number=173,
        )
    ),
    "ManagedWorkingStateAssignment": astichi_template(
        from_astichi_code(
            "astichi_pass(state, outer_bind=True).astichi_ref(external=working_slot)._ = VOID",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl",
            line_number=180,
            keep_names=("VOID",),
        )
    ),
    "ManagedStagedStateAssignment": astichi_template(
        from_astichi_code(
            "astichi_pass(state, outer_bind=True).astichi_ref(external=staged_slot)._ = VOID",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl",
            line_number=186,
            keep_names=("VOID",),
        )
    ),
    "ManagedDefaultProperty": astichi_template(
        from_astichi_code(
            """\
@property
def property_getter_name__astichi_arg__(self):
    state = self._y_state
    if state.astichi_ref(external=working_slot) is not VOID:
        return state.astichi_ref(external=working_slot)
    return state.astichi_ref(external=current_slot)

@property_setter_target_name__astichi_arg__.setter
def property_setter_name__astichi_arg__(self, value):
    state = self._y_state
    state._y_ensure_working_transaction(astichi_bind_external(tx_index))
    state.astichi_ref(external=working_slot)._ = value""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl",
            line_number=192,
            keep_names=("VOID",),
        )
    ),
    "ManagedCurrentProperty": astichi_template(
        from_astichi_code(
            """\
@property
def property_getter_name__astichi_arg__(self):
    return self._y_state.astichi_ref(external=current_slot)

@property_setter_target_name__astichi_arg__.setter
def property_setter_name__astichi_arg__(self, value):
    del value
    raise AttributeError(
        "current facade is read-only for transactional field "
        + astichi_bind_external(field_name)
    )""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl",
            line_number=209,
        )
    ),
    "ManagedWorkingProperty": astichi_template(
        from_astichi_code(
            """\
@property
def property_getter_name__astichi_arg__(self):
    state = self._y_state
    if state.astichi_ref(external=working_slot) is not VOID:
        return state.astichi_ref(external=working_slot)
    return state.astichi_ref(external=current_slot)

@property_setter_target_name__astichi_arg__.setter
def property_setter_name__astichi_arg__(self, value):
    state = self._y_state
    state._y_ensure_working_transaction(astichi_bind_external(tx_index))
    state.astichi_ref(external=working_slot)._ = value""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl",
            line_number=223,
            keep_names=("VOID",),
        )
    ),
    "ManagedThawWorkingProperty": astichi_template(
        from_astichi_code(
            """\
@property
def property_getter_name__astichi_arg__(self):
    state = self._y_state
    if state.astichi_ref(external=working_slot) is not VOID:
        return state.astichi_ref(external=working_slot)
    tx_group = state.__yidl_tx_index_to_group__[
        astichi_bind_external(working_tx_index)
    ]
    if state._y_transaction_manager.active_transaction_for(tx_group) is None:
        return state.astichi_ref(external=current_slot)
    state._y_ensure_working_transaction(astichi_bind_external(working_tx_index))
    next_value = thaw_func_name__astichi_arg__(
        state.astichi_ref(external=current_slot)
    )
    state.astichi_ref(external=working_slot)._ = next_value
    return next_value

@property_setter_target_name__astichi_arg__.setter
def property_setter_name__astichi_arg__(self, value):
    state = self._y_state
    state._y_ensure_working_transaction(astichi_bind_external(working_tx_index))
    state.astichi_ref(external=working_slot)._ = value""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl",
            line_number=240,
            keep_names=("VOID",),
        )
    ),
    "ManagedOptionalThawWorkingProperty": astichi_template(
        from_astichi_code(
            """\
@property
def property_getter_name__astichi_arg__(self):
    state = self._y_state
    if state.astichi_ref(external=working_slot) is not VOID:
        return state.astichi_ref(external=working_slot)
    tx_group = state.__yidl_tx_index_to_group__[
        astichi_bind_external(working_tx_index)
    ]
    if state._y_transaction_manager.active_transaction_for(tx_group) is None:
        return state.astichi_ref(external=current_slot)
    state._y_ensure_working_transaction(astichi_bind_external(working_tx_index))
    current_value = state.astichi_ref(external=current_slot)
    next_value = (
        None
        if current_value is None
        else thaw_func_name__astichi_arg__(current_value)
    )
    state.astichi_ref(external=working_slot)._ = next_value
    return next_value

@property_setter_target_name__astichi_arg__.setter
def property_setter_name__astichi_arg__(self, value):
    state = self._y_state
    state._y_ensure_working_transaction(astichi_bind_external(working_tx_index))
    state.astichi_ref(external=working_slot)._ = value""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl",
            line_number=267,
            keep_names=("VOID",),
        )
    ),
    "ManagedPlainPrepareBranch": astichi_template(
        from_astichi_code(
            """\
if astichi_pass(self, outer_bind=True).astichi_ref(external=working_slot) is not VOID:
    astichi_pass(self, outer_bind=True).astichi_ref(external=staged_slot)._ = (
        astichi_pass(self, outer_bind=True).astichi_ref(external=working_slot)
    )""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl",
            line_number=297,
            keep_names=("VOID",),
        )
    ),
    "ManagedFreezePrepareBranch": astichi_template(
        from_astichi_code(
            """\
if astichi_pass(self, outer_bind=True).astichi_ref(external=working_slot) is not VOID:
    astichi_pass(self, outer_bind=True).astichi_ref(external=staged_slot)._ = (
        freeze_func_name__astichi_arg__(
            astichi_pass(self, outer_bind=True).astichi_ref(external=working_slot)
        )
    )""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl",
            line_number=306,
            keep_names=("VOID",),
        )
    ),
    "ManagedOptionalFreezePrepareBranch": astichi_template(
        from_astichi_code(
            """\
if astichi_pass(self, outer_bind=True).astichi_ref(external=working_slot) is not VOID:
    astichi_pass(self, outer_bind=True).astichi_ref(external=staged_slot)._ = (
        None
        if astichi_pass(self, outer_bind=True).astichi_ref(external=working_slot) is None
        else freeze_func_name__astichi_arg__(
            astichi_pass(self, outer_bind=True).astichi_ref(external=working_slot)
        )
    )""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl",
            line_number=317,
            keep_names=("VOID",),
        )
    ),
    "ManagedApplyPreparedCommitBranch": astichi_template(
        from_astichi_code(
            """\
if astichi_pass(self, outer_bind=True).astichi_ref(external=staged_slot) is not VOID:
    astichi_pass(self, outer_bind=True).astichi_ref(external=current_slot)._ = (
        astichi_pass(self, outer_bind=True).astichi_ref(external=staged_slot)
    )
    astichi_pass(self, outer_bind=True).astichi_ref(external=staged_slot)._ = VOID
    astichi_pass(self, outer_bind=True).astichi_ref(external=working_slot)._ = VOID""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl",
            line_number=330,
            keep_names=("VOID",),
        )
    ),
    "ManagedRollbackBranch": astichi_template(
        from_astichi_code(
            """\
astichi_pass(self, outer_bind=True).astichi_ref(external=staged_slot)._ = VOID
astichi_pass(self, outer_bind=True).astichi_ref(external=working_slot)._ = VOID""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl",
            line_number=341,
            keep_names=("VOID",),
        )
    ),
    "PrepareCommitFieldsFunction": astichi_template(
        from_astichi_code(
            """\
def prepare_commit_fields_function_name__astichi_arg__(self):
    astichi_hole(prepare_commit_fields_body)""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl",
            line_number=348,
        )
    ),
    "ApplyPreparedCommitFieldsFunction": astichi_template(
        from_astichi_code(
            """\
def apply_prepared_commit_fields_function_name__astichi_arg__(self):
    astichi_hole(apply_prepared_commit_fields_body)""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl",
            line_number=353,
        )
    ),
    "RollbackFieldsFunction": astichi_template(
        from_astichi_code(
            """\
def rollback_fields_function_name__astichi_arg__(self):
    astichi_hole(rollback_fields_body)""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl",
            line_number=358,
        )
    ),
    "ApplyPreparedCommitDispatchBranch": astichi_template(
        from_astichi_code(
            """\
if astichi_pass(tx_index, outer_bind=True) == astichi_bind_external(tx_index_value):
    astichi_pass(
        self,
        outer_bind=True,
    ).astichi_ref(external=apply_prepared_commit_fields_function_name)()""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl",
            line_number=363,
        )
    ),
    "PrepareCommitDispatchBranch": astichi_template(
        from_astichi_code(
            """\
if astichi_pass(tx_index, outer_bind=True) == astichi_bind_external(tx_index_value):
    astichi_pass(
        self,
        outer_bind=True,
    ).astichi_ref(external=prepare_commit_fields_function_name)()""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl",
            line_number=371,
        )
    ),
    "RollbackDispatchBranch": astichi_template(
        from_astichi_code(
            """\
if astichi_pass(tx_index, outer_bind=True) == astichi_bind_external(tx_index_value):
    astichi_pass(
        self,
        outer_bind=True,
    ).astichi_ref(external=rollback_fields_function_name)()""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl",
            line_number=379,
        )
    ),
    "BuildDefaultFactoryFactsBody": from_astichi_code(
        """\
classes = sorted(
    ctx.records(ClassesCollection),
    key=lambda item: item.class_order,
)
fields = sorted(
    ctx.records(FieldsCollection),
    key=lambda item: item.field_order,
)

for lifecycle_class in classes:
    class_fields = [
        field for field in fields
        if field.field_owner == lifecycle_class.class_id
    ]
    by_name = {field.field_name: field for field in class_fields}
    by_id = {field.field_id: field for field in class_fields}
    factory_fields = [
        field for field in class_fields
        if field.has_default_factory
    ]
    graph = {field.field_id: set() for field in factory_fields}
    deps = []
    diagnostic_count = 0

    def add_diagnostic(field, suffix, message):
        nonlocal diagnostic_count
        diagnostic_count += 1
        ctx.write(
            DefaultFactoryDiagnosticsCollection,
            DefaultFactoryDiagnostic(
                diagnostic_id=(
                    f"{field.field_id}.{suffix}.{diagnostic_count}"
                ),
                diagnostic_owner=lifecycle_class.class_id,
                diagnostic_field_id=field.field_id,
                diagnostic_message=message,
            ),
            policy=ReplaceExisting,
        )

    def provider_is_available(provider):
        if provider.init:
            return True
        return provider.has_default or provider.has_default_factory

    for consumer in factory_fields:
        for param_order, param_name in enumerate(
            consumer.default_factory_param_names
        ):
            provider = by_name.get(param_name)
            if provider is None:
                add_diagnostic(
                    consumer,
                    f"unknown.{param_name}",
                    (
                        f"{lifecycle_class.class_name}."
                        f"{consumer.field_name}: default_factory "
                        f"references unknown name {param_name!r}"
                    ),
                )
                continue
            if not provider_is_available(provider):
                add_diagnostic(
                    consumer,
                    f"unavailable.{param_name}",
                    (
                        f"{lifecycle_class.class_name}."
                        f"{consumer.field_name}: default_factory "
                        f"cannot reference {param_name!r} "
                        "(value is unavailable before factory evaluation)"
                    ),
                )
                continue
            deps.append((consumer, provider, param_name, param_order))
            if provider.field_id in graph:
                graph[consumer.field_id].add(provider.field_id)

    field_order = {
        field.field_id: field.field_order for field in class_fields
    }
    visiting = set()
    visited = set()
    ordered_field_ids = []
    cycle_found = False

    def visit(field_id, path):
        nonlocal cycle_found
        if cycle_found or field_id in visited:
            return
        if field_id in visiting:
            cycle = path[path.index(field_id):]
            names = " -> ".join(by_id[item].field_name for item in cycle)
            add_diagnostic(
                by_id[field_id],
                "cycle",
                (
                    f"{lifecycle_class.class_name}: default_factory "
                    f"dependency cycle: {names}"
                ),
            )
            cycle_found = True
            return
        visiting.add(field_id)
        for provider_id in sorted(
            graph.get(field_id, ()),
            key=lambda item: field_order[item],
        ):
            visit(provider_id, [*path, provider_id])
        visiting.remove(field_id)
        visited.add(field_id)
        ordered_field_ids.append(field_id)

    for field in factory_fields:
        visit(field.field_id, [field.field_id])
        if cycle_found:
            break

    if diagnostic_count:
        continue

    eval_order_by_id = {
        field_id: eval_order
        for eval_order, field_id in enumerate(ordered_field_ids)
    }

    for consumer, provider, param_name, param_order in deps:
        ctx.write(
            DefaultFactoryDependenciesCollection,
            DefaultFactoryDependency(
                dependency_owner=lifecycle_class.class_id,
                consumer_field_id=consumer.field_id,
                consumer_field_name=consumer.field_name,
                provider_name=provider.field_name,
                provider_field_id=provider.field_id,
                provider_field_kind=provider.field_kind,
                provider_init=provider.init,
                provider_has_default=provider.has_default,
                provider_has_default_factory=provider.has_default_factory,
                param_name=param_name,
                param_order=param_order,
                consumer_eval_order=eval_order_by_id[consumer.field_id],
            ),
            policy=RejectDuplicate,
        )

    for eval_order, field_id in enumerate(ordered_field_ids):
        field = by_id[field_id]
        state_slot = ""
        if field.field_kind == "field":
            state_slot = field.value_slot_name
        elif field.field_kind == "managed":
            state_slot = field.current_slot_name
        ctx.write(
            DefaultFactoryEvaluationStepsCollection,
            DefaultFactoryEvaluationStep(
                eval_step_id=field.field_id,
                eval_owner=lifecycle_class.class_id,
                eval_field_id=field.field_id,
                eval_field_name=field.field_name,
                eval_field_kind=field.field_kind,
                eval_init=field.init,
                eval_state_slot_name=state_slot,
                eval_default_factory_param_name=(
                    field.default_factory_param_name
                ),
                eval_order=eval_order,
                eval_statement_order=100000 + eval_order,
            ),
            policy=RejectDuplicate,
        )""",
        file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_default_factories.yidl",
        line_number=85,
        keep_names=(
            "ctx",
            "ClassesCollection",
            "FieldsCollection",
            "DefaultFactoryDependenciesCollection",
            "DefaultFactoryEvaluationStepsCollection",
            "DefaultFactoryDiagnosticsCollection",
            "DefaultFactoryDependency",
            "DefaultFactoryEvaluationStep",
            "DefaultFactoryDiagnostic",
            "RejectDuplicate",
            "ReplaceExisting",
        ),
    ),
    "RaiseDefaultFactoryDiagnosticsBody": from_astichi_code(
        """\
for diagnostic in ctx.records(DefaultFactoryDiagnosticsCollection):
    raise AssemblyDiagnosticError(diagnostic.diagnostic_message)""",
        file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_default_factories.yidl",
        line_number=270,
        keep_names=(
            "ctx",
            "DefaultFactoryDiagnosticsCollection",
            "AssemblyDiagnosticError",
        ),
    ),
    "InitParamDefaultFactory": astichi_template(
        from_astichi_code(
            """\
def astichi_params(
    param_name__astichi_arg__: astichi_bind_external(annotation)
    = _HAS_DEFAULT_FACTORY
):
    pass""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_default_factories.yidl",
            line_number=286,
            keep_names=("_HAS_DEFAULT_FACTORY",),
        )
    ),
    "StoredDefaultFactoryEvalInit": astichi_template(
        from_astichi_code(
            """\
if astichi_pass(field_name__astichi_arg__, outer_bind=True) is _HAS_DEFAULT_FACTORY:
    astichi_pass(field_name__astichi_arg__, outer_bind=True)._ = (
        default_factory_name__astichi_arg__(
            **astichi_hole(default_factory_args)
        )
    )
astichi_pass(state, outer_bind=True).astichi_ref(external=state_slot)._ = astichi_pass(
    field_name__astichi_arg__,
    outer_bind=True,
)""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_default_factories.yidl",
            line_number=296,
            keep_names=("_HAS_DEFAULT_FACTORY",),
        )
    ),
    "StoredDefaultFactoryEvalNoInit": astichi_template(
        from_astichi_code(
            """\
field_name__astichi_arg__ = default_factory_name__astichi_arg__(
    **astichi_hole(default_factory_args)
)
astichi_pass(state, outer_bind=True).astichi_ref(external=state_slot)._ = astichi_pass(
    field_name__astichi_arg__,
    outer_bind=True,
)""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_default_factories.yidl",
            line_number=311,
        )
    ),
    "InitVarDefaultFactoryEvalInit": astichi_template(
        from_astichi_code(
            """\
if astichi_pass(field_name__astichi_arg__, outer_bind=True) is _HAS_DEFAULT_FACTORY:
    astichi_pass(field_name__astichi_arg__, outer_bind=True)._ = (
        default_factory_name__astichi_arg__(
            **astichi_hole(default_factory_args)
        )
    )""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_default_factories.yidl",
            line_number=321,
            keep_names=("_HAS_DEFAULT_FACTORY",),
        )
    ),
    "InitVarDefaultFactoryEvalNoInit": astichi_template(
        from_astichi_code(
            """\
field_name__astichi_arg__ = default_factory_name__astichi_arg__(
    **astichi_hole(default_factory_args)
)""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_default_factories.yidl",
            line_number=332,
        )
    ),
    "DefaultFactoryStoredArg": astichi_template(
        from_astichi_code(
            """\
astichi_funcargs(
    param_name__astichi_arg__=astichi_pass(
        self,
        outer_bind=True,
    ).astichi_ref(external=provider_name)
)""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_default_factories.yidl",
            line_number=338,
        )
    ),
    "DefaultFactoryLocalArg": astichi_template(
        from_astichi_code(
            """\
astichi_funcargs(
    param_name__astichi_arg__=astichi_pass(
        provider_name__astichi_arg__,
        outer_bind=True,
    )
)""",
            file_name="tests/data/yidl/yidl_transactional_lifecycle/lifecycle_default_factories.yidl",
            line_number=347,
        )
    ),
}
ASSEMBLY_CONTRIBUTIONS = {
    "LifecycleDefinitionBuilderParam": ContributionSpec(
        name="LifecycleDefinitionBuilderParam",
        source_name="BuilderParam",
        source_kind="resource",
        build_name="LifecycleDefinitionBuilderParam",
        index=ValueRef("ClassOrder"),
        order=ValueRef("ClassOrder"),
        target=TargetSpec(
            name="builder_params",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="Root", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident",
                name="value_name",
                value=ValueRef("LifecycleDefinitionParamName"),
            ),
        ),
    ),
    "AnnotationsBuilderParam": ContributionSpec(
        name="AnnotationsBuilderParam",
        source_name="BuilderParam",
        source_kind="resource",
        build_name="AnnotationsBuilderParam",
        index=ValueRef("ClassOrder"),
        order=ValueRef("ClassOrder"),
        target=TargetSpec(
            name="builder_params",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="Root", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident", name="value_name", value=ValueRef("AnnotationsParamName")
            ),
        ),
    ),
    "TxGroupsBuilderParam": ContributionSpec(
        name="TxGroupsBuilderParam",
        source_name="BuilderParam",
        source_kind="resource",
        build_name="TxGroupsBuilderParam",
        index=ValueRef("ClassOrder"),
        order=ValueRef("ClassOrder"),
        target=TargetSpec(
            name="builder_params",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="Root", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident", name="value_name", value=ValueRef("TxGroupsParamName")
            ),
        ),
    ),
    "FieldDefaultBuilderParam": ContributionSpec(
        name="FieldDefaultBuilderParam",
        source_name="BuilderParam",
        source_kind="resource",
        build_name="FieldDefaultBuilderParam",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="builder_params",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="Root", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident", name="value_name", value=ValueRef("DefaultValueParamName")
            ),
        ),
    ),
    "FacadeBaseBodyPass": ContributionSpec(
        name="FacadeBaseBodyPass",
        source_name="PassStatement",
        source_kind="resource",
        build_name="FacadeBaseBodyPass",
        index=LiteralValueRef(0),
        order=LiteralValueRef(0),
        target=TargetSpec(
            name="facade_base_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "FacadePropertiesPass": ContributionSpec(
        name="FacadePropertiesPass",
        source_name="PassStatement",
        source_kind="resource",
        build_name="FacadePropertiesPass",
        index=LiteralValueRef(0),
        order=LiteralValueRef(0),
        target=TargetSpec(
            name="facade_properties",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "DefaultFacadePropertiesPass": ContributionSpec(
        name="DefaultFacadePropertiesPass",
        source_name="PassStatement",
        source_kind="resource",
        build_name="DefaultFacadePropertiesPass",
        index=LiteralValueRef(0),
        order=LiteralValueRef(0),
        target=TargetSpec(
            name="default_facade_properties",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "CurrentFacadePropertiesPass": ContributionSpec(
        name="CurrentFacadePropertiesPass",
        source_name="PassStatement",
        source_kind="resource",
        build_name="CurrentFacadePropertiesPass",
        index=LiteralValueRef(0),
        order=LiteralValueRef(0),
        target=TargetSpec(
            name="current_facade_properties",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "WorkingFacadePropertiesPass": ContributionSpec(
        name="WorkingFacadePropertiesPass",
        source_name="PassStatement",
        source_kind="resource",
        build_name="WorkingFacadePropertiesPass",
        index=LiteralValueRef(0),
        order=LiteralValueRef(0),
        target=TargetSpec(
            name="working_facade_properties",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "StateInitBodyPass": ContributionSpec(
        name="StateInitBodyPass",
        source_name="PassStatement",
        source_kind="resource",
        build_name="StateInitBodyPass",
        index=LiteralValueRef(0),
        order=LiteralValueRef(0),
        target=TargetSpec(
            name="state_init_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "CommitTransactionBodyPass": ContributionSpec(
        name="CommitTransactionBodyPass",
        source_name="PassStatement",
        source_kind="resource",
        build_name="CommitTransactionBodyPass",
        index=LiteralValueRef(0),
        order=LiteralValueRef(0),
        target=TargetSpec(
            name="commit_transaction_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "CommitTransactionDispatchBodyPass": ContributionSpec(
        name="CommitTransactionDispatchBodyPass",
        source_name="PassStatement",
        source_kind="resource",
        build_name="CommitTransactionDispatchBodyPass",
        index=LiteralValueRef(0),
        order=LiteralValueRef(0),
        target=TargetSpec(
            name="commit_transaction_dispatch_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "PrepareCommitTransactionDispatchBodyPass": ContributionSpec(
        name="PrepareCommitTransactionDispatchBodyPass",
        source_name="PassStatement",
        source_kind="resource",
        build_name="PrepareCommitTransactionDispatchBodyPass",
        index=LiteralValueRef(0),
        order=LiteralValueRef(0),
        target=TargetSpec(
            name="prepare_commit_transaction_dispatch_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "RollbackTransactionBodyPass": ContributionSpec(
        name="RollbackTransactionBodyPass",
        source_name="PassStatement",
        source_kind="resource",
        build_name="RollbackTransactionBodyPass",
        index=LiteralValueRef(0),
        order=LiteralValueRef(0),
        target=TargetSpec(
            name="rollback_transaction_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "RollbackTransactionDispatchBodyPass": ContributionSpec(
        name="RollbackTransactionDispatchBodyPass",
        source_name="PassStatement",
        source_kind="resource",
        build_name="RollbackTransactionDispatchBodyPass",
        index=LiteralValueRef(0),
        order=LiteralValueRef(0),
        target=TargetSpec(
            name="rollback_transaction_dispatch_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "CommitOrderKeyBodyPass": ContributionSpec(
        name="CommitOrderKeyBodyPass",
        source_name="PassStatement",
        source_kind="resource",
        build_name="CommitOrderKeyBodyPass",
        index=LiteralValueRef(0),
        order=LiteralValueRef(0),
        target=TargetSpec(
            name="commit_order_key_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "RequiresValidationBodyPass": ContributionSpec(
        name="RequiresValidationBodyPass",
        source_name="PassStatement",
        source_kind="resource",
        build_name="RequiresValidationBodyPass",
        index=LiteralValueRef(0),
        order=LiteralValueRef(0),
        target=TargetSpec(
            name="requires_validation_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "ValidateCommitBodyPass": ContributionSpec(
        name="ValidateCommitBodyPass",
        source_name="PassStatement",
        source_kind="resource",
        build_name="ValidateCommitBodyPass",
        index=LiteralValueRef(0),
        order=LiteralValueRef(0),
        target=TargetSpec(
            name="validate_commit_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "BeforeCommitBodyPass": ContributionSpec(
        name="BeforeCommitBodyPass",
        source_name="PassStatement",
        source_kind="resource",
        build_name="BeforeCommitBodyPass",
        index=LiteralValueRef(0),
        order=LiteralValueRef(0),
        target=TargetSpec(
            name="before_commit_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "AfterCommitBodyPass": ContributionSpec(
        name="AfterCommitBodyPass",
        source_name="PassStatement",
        source_kind="resource",
        build_name="AfterCommitBodyPass",
        index=LiteralValueRef(0),
        order=LiteralValueRef(0),
        target=TargetSpec(
            name="after_commit_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "AfterRollbackBodyPass": ContributionSpec(
        name="AfterRollbackBodyPass",
        source_name="PassStatement",
        source_kind="resource",
        build_name="AfterRollbackBodyPass",
        index=LiteralValueRef(0),
        order=LiteralValueRef(0),
        target=TargetSpec(
            name="after_rollback_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "ReturnClassContribution": ContributionSpec(
        name="ReturnClassContribution",
        source_name="ReturnClass",
        source_kind="resource",
        build_name="ReturnClass",
        index=ValueRef("ClassOrder"),
        order=ValueRef("ClassOrder"),
        target=TargetSpec(
            name="return_statement",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="Root", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident", name="return_class_name_ref", value=ValueRef("ClassName")
            ),
            BindingSpec(
                kind="ident",
                name="return_class_qualname_ref",
                value=ValueRef("ClassName"),
            ),
            BindingSpec(
                kind="ident",
                name="return_class_module_ref",
                value=ValueRef("ClassName"),
            ),
            BindingSpec(
                kind="ident",
                name="return_class_result_ref",
                value=ValueRef("ClassName"),
            ),
        ),
    ),
    "TransactionManagerInitParam": ContributionSpec(
        name="TransactionManagerInitParam",
        source_name="TransactionManagerParam",
        source_kind="resource",
        build_name="TransactionManagerInitParam",
        index=ValueRef("ClassOrder"),
        order=LiteralValueRef(0),
        target=TargetSpec(
            name="init_params",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "PlainStateSlot": ContributionSpec(
        name="PlainStateSlot",
        source_name="StateSlotEntry",
        source_kind="resource",
        build_name="PlainStateSlot",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="state_slots",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="slot_name", value=ValueRef("ValueSlotName")
            ),
        ),
    ),
    "PlainInitParamRequired": ContributionSpec(
        name="PlainInitParamRequired",
        source_name="InitParamRequired",
        source_kind="resource",
        build_name="PlainInitParam",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="init_params",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(kind="ident", name="param_name", value=ValueRef("FieldName")),
            BindingSpec(
                kind="external", name="annotation", value=ValueRef("Annotation")
            ),
        ),
    ),
    "PlainInitParamDefault": ContributionSpec(
        name="PlainInitParamDefault",
        source_name="InitParamDefault",
        source_kind="resource",
        build_name="PlainInitParam",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="init_params",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(kind="ident", name="param_name", value=ValueRef("FieldName")),
            BindingSpec(
                kind="external", name="annotation", value=ValueRef("Annotation")
            ),
            BindingSpec(
                kind="ident",
                name="default_value_name",
                value=ValueRef("DefaultValueParamName"),
            ),
        ),
    ),
    "InitVarParamRequired": ContributionSpec(
        name="InitVarParamRequired",
        source_name="InitParamRequired",
        source_kind="resource",
        build_name="InitVarParam",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="init_params",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(kind="ident", name="param_name", value=ValueRef("FieldName")),
            BindingSpec(
                kind="external", name="annotation", value=ValueRef("Annotation")
            ),
        ),
    ),
    "InitVarParamDefault": ContributionSpec(
        name="InitVarParamDefault",
        source_name="InitParamDefault",
        source_kind="resource",
        build_name="InitVarParam",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="init_params",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(kind="ident", name="param_name", value=ValueRef("FieldName")),
            BindingSpec(
                kind="external", name="annotation", value=ValueRef("Annotation")
            ),
            BindingSpec(
                kind="ident",
                name="default_value_name",
                value=ValueRef("DefaultValueParamName"),
            ),
        ),
    ),
    "InitVarLocalDefault": ContributionSpec(
        name="InitVarLocalDefault",
        source_name="InitVarLocalDefaultAssignment",
        source_kind="resource",
        build_name="InitVarLocalDefault",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="state_init_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident", name="init_value_name", value=ValueRef("FieldName")
            ),
            BindingSpec(
                kind="ident",
                name="default_value_name",
                value=ValueRef("DefaultValueParamName"),
            ),
        ),
    ),
    "PlainInitAssignment": ContributionSpec(
        name="PlainInitAssignment",
        source_name="PlainStateAssignment",
        source_kind="resource",
        build_name="PlainInitAssignment",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="state_init_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident", name="init_value_name", value=ValueRef("FieldName")
            ),
            BindingSpec(
                kind="external", name="state_slot", value=ValueRef("ValueSlotName")
            ),
        ),
    ),
    "PlainDefaultAssignment": ContributionSpec(
        name="PlainDefaultAssignment",
        source_name="PlainStateAssignment",
        source_kind="resource",
        build_name="PlainDefaultAssignment",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="state_init_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident",
                name="init_value_name",
                value=ValueRef("DefaultValueParamName"),
            ),
            BindingSpec(
                kind="external", name="state_slot", value=ValueRef("ValueSlotName")
            ),
        ),
    ),
    "PlainFieldProperty": ContributionSpec(
        name="PlainFieldProperty",
        source_name="PlainProperty",
        source_kind="resource",
        build_name="PlainFieldProperty",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="facade_properties",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident", name="property_getter_name", value=ValueRef("FieldName")
            ),
            BindingSpec(
                kind="ident",
                name="property_setter_target_name",
                value=ValueRef("FieldName"),
            ),
            BindingSpec(
                kind="ident", name="property_setter_name", value=ValueRef("FieldName")
            ),
            BindingSpec(
                kind="external", name="state_slot", value=ValueRef("ValueSlotName")
            ),
        ),
    ),
    "ClassVarDefault": ContributionSpec(
        name="ClassVarDefault",
        source_name="ClassVarDefaultAssignment",
        source_kind="resource",
        build_name="ClassVarDefault",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="facade_base_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident", name="classvar_name", value=ValueRef("FieldName")
            ),
            BindingSpec(
                kind="ident",
                name="classvar_value_name",
                value=ValueRef("DefaultValueParamName"),
            ),
        ),
    ),
    "CommitOrderKeyBranchContribution": ContributionSpec(
        name="CommitOrderKeyBranchContribution",
        source_name="CommitOrderKeyBranch",
        source_kind="resource",
        build_name="CommitOrderKeyBranch",
        index=ValueRef("DeclarationOrder"),
        order=ValueRef("DeclarationOrder"),
        target=TargetSpec(
            name="commit_order_key_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="method_name", value=ValueRef("MethodName")
            ),
            BindingSpec(
                kind="external", name="tx_index_value", value=ValueRef("TxIndex")
            ),
        ),
    ),
    "RequiresValidationBranchContribution": ContributionSpec(
        name="RequiresValidationBranchContribution",
        source_name="RequiresValidationBranch",
        source_kind="resource",
        build_name="RequiresValidationBranch",
        index=ValueRef("DeclarationOrder"),
        order=ValueRef("DeclarationOrder"),
        target=TargetSpec(
            name="requires_validation_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="tx_index_value", value=ValueRef("TxIndex")
            ),
        ),
    ),
    "ValidateCommitBranchContribution": ContributionSpec(
        name="ValidateCommitBranchContribution",
        source_name="ValidateCommitBranch",
        source_kind="resource",
        build_name="ValidateCommitBranch",
        index=ValueRef("DeclarationOrder"),
        order=ValueRef("DeclarationOrder"),
        target=TargetSpec(
            name="validate_commit_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="method_name", value=ValueRef("MethodName")
            ),
            BindingSpec(
                kind="external", name="tx_index_value", value=ValueRef("TxIndex")
            ),
        ),
    ),
    "BeforeCommitHookContribution": ContributionSpec(
        name="BeforeCommitHookContribution",
        source_name="TransactionHookCall",
        source_kind="resource",
        build_name="BeforeCommitHook",
        index=ValueRef("DeclarationOrder"),
        order=ValueRef("DeclarationOrder"),
        target=TargetSpec(
            name="before_commit_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="method_name", value=ValueRef("MethodName")
            ),
            BindingSpec(
                kind="external", name="tx_index_value", value=ValueRef("TxIndex")
            ),
        ),
    ),
    "AfterCommitHookContribution": ContributionSpec(
        name="AfterCommitHookContribution",
        source_name="TransactionHookCall",
        source_kind="resource",
        build_name="AfterCommitHook",
        index=ValueRef("DeclarationOrder"),
        order=ValueRef("DeclarationOrder"),
        target=TargetSpec(
            name="after_commit_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="method_name", value=ValueRef("MethodName")
            ),
            BindingSpec(
                kind="external", name="tx_index_value", value=ValueRef("TxIndex")
            ),
        ),
    ),
    "AfterRollbackHookContribution": ContributionSpec(
        name="AfterRollbackHookContribution",
        source_name="TransactionHookCall",
        source_kind="resource",
        build_name="AfterRollbackHook",
        index=ValueRef("DeclarationOrder"),
        order=ValueRef("DeclarationOrder"),
        target=TargetSpec(
            name="after_rollback_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="method_name", value=ValueRef("MethodName")
            ),
            BindingSpec(
                kind="external", name="tx_index_value", value=ValueRef("TxIndex")
            ),
        ),
    ),
    "CoreClassDefinition": ContributionSpec(
        name="CoreClassDefinition",
        source_name="CoreClassProduction",
        source_kind="production",
        build_name="ClassDef",
        index=ValueRef("ClassOrder"),
        order=ValueRef("ClassOrder"),
        target=TargetSpec(
            name="function_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="Root", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "ManagedCurrentStateSlot": ContributionSpec(
        name="ManagedCurrentStateSlot",
        source_name="StateSlotEntry",
        source_kind="resource",
        build_name="ManagedCurrentStateSlot",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="state_slots",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="slot_name", value=ValueRef("CurrentSlotName")
            ),
        ),
    ),
    "ManagedWorkingStateSlot": ContributionSpec(
        name="ManagedWorkingStateSlot",
        source_name="StateSlotEntry",
        source_kind="resource",
        build_name="ManagedWorkingStateSlot",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="state_slots",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="slot_name", value=ValueRef("WorkingSlotName")
            ),
        ),
    ),
    "ManagedStagedStateSlot": ContributionSpec(
        name="ManagedStagedStateSlot",
        source_name="StateSlotEntry",
        source_kind="resource",
        build_name="ManagedStagedStateSlot",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="state_slots",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="slot_name", value=ValueRef("StagedSlotName")
            ),
        ),
    ),
    "ManagedFreezeBuilderParam": ContributionSpec(
        name="ManagedFreezeBuilderParam",
        source_name="BuilderParam",
        source_kind="resource",
        build_name="ManagedFreezeBuilderParam",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="builder_params",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="Root", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident", name="value_name", value=ValueRef("FreezeParamName")
            ),
        ),
    ),
    "ManagedThawBuilderParam": ContributionSpec(
        name="ManagedThawBuilderParam",
        source_name="BuilderParam",
        source_kind="resource",
        build_name="ManagedThawBuilderParam",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="builder_params",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="Root", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident", name="value_name", value=ValueRef("ThawParamName")
            ),
        ),
    ),
    "ManagedInitParamDefault": ContributionSpec(
        name="ManagedInitParamDefault",
        source_name="InitParamDefault",
        source_kind="resource",
        build_name="ManagedInitParam",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="init_params",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(kind="ident", name="param_name", value=ValueRef("FieldName")),
            BindingSpec(
                kind="external", name="annotation", value=ValueRef("Annotation")
            ),
            BindingSpec(
                kind="ident",
                name="default_value_name",
                value=ValueRef("DefaultValueParamName"),
            ),
        ),
    ),
    "ManagedInitParamRequired": ContributionSpec(
        name="ManagedInitParamRequired",
        source_name="InitParamRequired",
        source_kind="resource",
        build_name="ManagedInitParam",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="init_params",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(kind="ident", name="param_name", value=ValueRef("FieldName")),
            BindingSpec(
                kind="external", name="annotation", value=ValueRef("Annotation")
            ),
        ),
    ),
    "ManagedCurrentInitAssignment": ContributionSpec(
        name="ManagedCurrentInitAssignment",
        source_name="ManagedCurrentStateAssignment",
        source_kind="resource",
        build_name="ManagedCurrentInitAssignment",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="state_init_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident", name="init_value_name", value=ValueRef("FieldName")
            ),
            BindingSpec(
                kind="external", name="current_slot", value=ValueRef("CurrentSlotName")
            ),
        ),
    ),
    "ManagedCurrentDefaultAssignment": ContributionSpec(
        name="ManagedCurrentDefaultAssignment",
        source_name="ManagedCurrentStateAssignment",
        source_kind="resource",
        build_name="ManagedCurrentDefaultAssignment",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="state_init_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident",
                name="init_value_name",
                value=ValueRef("DefaultValueParamName"),
            ),
            BindingSpec(
                kind="external", name="current_slot", value=ValueRef("CurrentSlotName")
            ),
        ),
    ),
    "ManagedWorkingInitAssignment": ContributionSpec(
        name="ManagedWorkingInitAssignment",
        source_name="ManagedWorkingStateAssignment",
        source_kind="resource",
        build_name="ManagedWorkingInitAssignment",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="state_init_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="working_slot", value=ValueRef("WorkingSlotName")
            ),
        ),
    ),
    "ManagedStagedInitAssignment": ContributionSpec(
        name="ManagedStagedInitAssignment",
        source_name="ManagedStagedStateAssignment",
        source_kind="resource",
        build_name="ManagedStagedInitAssignment",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="state_init_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="staged_slot", value=ValueRef("StagedSlotName")
            ),
        ),
    ),
    "ManagedDefaultFacadeProperty": ContributionSpec(
        name="ManagedDefaultFacadeProperty",
        source_name="ManagedDefaultProperty",
        source_kind="resource",
        build_name="ManagedDefaultFacadeProperty",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="default_facade_properties",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident", name="property_getter_name", value=ValueRef("FieldName")
            ),
            BindingSpec(
                kind="ident",
                name="property_setter_target_name",
                value=ValueRef("FieldName"),
            ),
            BindingSpec(
                kind="ident", name="property_setter_name", value=ValueRef("FieldName")
            ),
            BindingSpec(
                kind="external", name="current_slot", value=ValueRef("CurrentSlotName")
            ),
            BindingSpec(
                kind="external", name="working_slot", value=ValueRef("WorkingSlotName")
            ),
            BindingSpec(kind="external", name="tx_index", value=ValueRef("TxIndex")),
        ),
    ),
    "ManagedCurrentFacadeProperty": ContributionSpec(
        name="ManagedCurrentFacadeProperty",
        source_name="ManagedCurrentProperty",
        source_kind="resource",
        build_name="ManagedCurrentFacadeProperty",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="current_facade_properties",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident", name="property_getter_name", value=ValueRef("FieldName")
            ),
            BindingSpec(
                kind="ident",
                name="property_setter_target_name",
                value=ValueRef("FieldName"),
            ),
            BindingSpec(
                kind="ident", name="property_setter_name", value=ValueRef("FieldName")
            ),
            BindingSpec(
                kind="external", name="current_slot", value=ValueRef("CurrentSlotName")
            ),
            BindingSpec(
                kind="external", name="field_name", value=ValueRef("FieldName")
            ),
        ),
    ),
    "ManagedWorkingFacadeProperty": ContributionSpec(
        name="ManagedWorkingFacadeProperty",
        source_name="ManagedWorkingProperty",
        source_kind="resource",
        build_name="ManagedWorkingFacadeProperty",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="working_facade_properties",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident", name="property_getter_name", value=ValueRef("FieldName")
            ),
            BindingSpec(
                kind="ident",
                name="property_setter_target_name",
                value=ValueRef("FieldName"),
            ),
            BindingSpec(
                kind="ident", name="property_setter_name", value=ValueRef("FieldName")
            ),
            BindingSpec(
                kind="external", name="current_slot", value=ValueRef("CurrentSlotName")
            ),
            BindingSpec(
                kind="external", name="working_slot", value=ValueRef("WorkingSlotName")
            ),
            BindingSpec(kind="external", name="tx_index", value=ValueRef("TxIndex")),
        ),
    ),
    "ManagedThawWorkingFacadeProperty": ContributionSpec(
        name="ManagedThawWorkingFacadeProperty",
        source_name="ManagedThawWorkingProperty",
        source_kind="resource",
        build_name="ManagedWorkingFacadeProperty",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="working_facade_properties",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident", name="property_getter_name", value=ValueRef("FieldName")
            ),
            BindingSpec(
                kind="ident",
                name="property_setter_target_name",
                value=ValueRef("FieldName"),
            ),
            BindingSpec(
                kind="ident", name="property_setter_name", value=ValueRef("FieldName")
            ),
            BindingSpec(
                kind="external", name="current_slot", value=ValueRef("CurrentSlotName")
            ),
            BindingSpec(
                kind="external", name="working_slot", value=ValueRef("WorkingSlotName")
            ),
            BindingSpec(
                kind="external", name="working_tx_index", value=ValueRef("TxIndex")
            ),
            BindingSpec(
                kind="ident", name="thaw_func_name", value=ValueRef("ThawParamName")
            ),
        ),
    ),
    "ManagedOptionalThawWorkingFacadeProperty": ContributionSpec(
        name="ManagedOptionalThawWorkingFacadeProperty",
        source_name="ManagedOptionalThawWorkingProperty",
        source_kind="resource",
        build_name="ManagedWorkingFacadeProperty",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="working_facade_properties",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident", name="property_getter_name", value=ValueRef("FieldName")
            ),
            BindingSpec(
                kind="ident",
                name="property_setter_target_name",
                value=ValueRef("FieldName"),
            ),
            BindingSpec(
                kind="ident", name="property_setter_name", value=ValueRef("FieldName")
            ),
            BindingSpec(
                kind="external", name="current_slot", value=ValueRef("CurrentSlotName")
            ),
            BindingSpec(
                kind="external", name="working_slot", value=ValueRef("WorkingSlotName")
            ),
            BindingSpec(
                kind="external", name="working_tx_index", value=ValueRef("TxIndex")
            ),
            BindingSpec(
                kind="ident", name="thaw_func_name", value=ValueRef("ThawParamName")
            ),
        ),
    ),
    "ManagedPlainPrepareCommit": ContributionSpec(
        name="ManagedPlainPrepareCommit",
        source_name="ManagedPlainPrepareBranch",
        source_kind="resource",
        build_name="ManagedPrepareCommit",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="prepare_commit_fields_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                            PathSegmentSpec(
                                kind="name",
                                name="PrepareCommitFields",
                                indexes=(ValueRef("TxIndex"),),
                            ),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="working_slot", value=ValueRef("WorkingSlotName")
            ),
            BindingSpec(
                kind="external", name="staged_slot", value=ValueRef("StagedSlotName")
            ),
        ),
    ),
    "ManagedFreezePrepareCommit": ContributionSpec(
        name="ManagedFreezePrepareCommit",
        source_name="ManagedFreezePrepareBranch",
        source_kind="resource",
        build_name="ManagedPrepareCommit",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="prepare_commit_fields_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                            PathSegmentSpec(
                                kind="name",
                                name="PrepareCommitFields",
                                indexes=(ValueRef("TxIndex"),),
                            ),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="working_slot", value=ValueRef("WorkingSlotName")
            ),
            BindingSpec(
                kind="external", name="staged_slot", value=ValueRef("StagedSlotName")
            ),
            BindingSpec(
                kind="ident", name="freeze_func_name", value=ValueRef("FreezeParamName")
            ),
        ),
    ),
    "ManagedOptionalFreezePrepareCommit": ContributionSpec(
        name="ManagedOptionalFreezePrepareCommit",
        source_name="ManagedOptionalFreezePrepareBranch",
        source_kind="resource",
        build_name="ManagedPrepareCommit",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="prepare_commit_fields_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                            PathSegmentSpec(
                                kind="name",
                                name="PrepareCommitFields",
                                indexes=(ValueRef("TxIndex"),),
                            ),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="working_slot", value=ValueRef("WorkingSlotName")
            ),
            BindingSpec(
                kind="external", name="staged_slot", value=ValueRef("StagedSlotName")
            ),
            BindingSpec(
                kind="ident", name="freeze_func_name", value=ValueRef("FreezeParamName")
            ),
        ),
    ),
    "ManagedApplyPreparedCommit": ContributionSpec(
        name="ManagedApplyPreparedCommit",
        source_name="ManagedApplyPreparedCommitBranch",
        source_kind="resource",
        build_name="ManagedApplyPreparedCommit",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="apply_prepared_commit_fields_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                            PathSegmentSpec(
                                kind="name",
                                name="ApplyPreparedCommitFields",
                                indexes=(ValueRef("TxIndex"),),
                            ),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="current_slot", value=ValueRef("CurrentSlotName")
            ),
            BindingSpec(
                kind="external", name="working_slot", value=ValueRef("WorkingSlotName")
            ),
            BindingSpec(
                kind="external", name="staged_slot", value=ValueRef("StagedSlotName")
            ),
        ),
    ),
    "ManagedRollback": ContributionSpec(
        name="ManagedRollback",
        source_name="ManagedRollbackBranch",
        source_kind="resource",
        build_name="ManagedRollback",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="rollback_fields_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                            PathSegmentSpec(
                                kind="name",
                                name="RollbackFields",
                                indexes=(ValueRef("TxIndex"),),
                            ),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="working_slot", value=ValueRef("WorkingSlotName")
            ),
            BindingSpec(
                kind="external", name="staged_slot", value=ValueRef("StagedSlotName")
            ),
        ),
    ),
    "PrepareCommitFieldsBodyPass": ContributionSpec(
        name="PrepareCommitFieldsBodyPass",
        source_name="PassStatement",
        source_kind="resource",
        build_name="PrepareCommitFieldsBodyPass",
        index=ValueRef("TxIndex"),
        order=LiteralValueRef(0),
        target=TargetSpec(
            name="prepare_commit_fields_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                            PathSegmentSpec(
                                kind="name",
                                name="PrepareCommitFields",
                                indexes=(ValueRef("TxIndex"),),
                            ),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "ApplyPreparedCommitFieldsBodyPass": ContributionSpec(
        name="ApplyPreparedCommitFieldsBodyPass",
        source_name="PassStatement",
        source_kind="resource",
        build_name="ApplyPreparedCommitFieldsBodyPass",
        index=ValueRef("TxIndex"),
        order=LiteralValueRef(0),
        target=TargetSpec(
            name="apply_prepared_commit_fields_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                            PathSegmentSpec(
                                kind="name",
                                name="ApplyPreparedCommitFields",
                                indexes=(ValueRef("TxIndex"),),
                            ),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "RollbackFieldsBodyPass": ContributionSpec(
        name="RollbackFieldsBodyPass",
        source_name="PassStatement",
        source_kind="resource",
        build_name="RollbackFieldsBodyPass",
        index=ValueRef("TxIndex"),
        order=LiteralValueRef(0),
        target=TargetSpec(
            name="rollback_fields_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                            PathSegmentSpec(
                                kind="name",
                                name="RollbackFields",
                                indexes=(ValueRef("TxIndex"),),
                            ),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "PrepareCommitFields": ContributionSpec(
        name="PrepareCommitFields",
        source_name="PrepareCommitFieldsFunction",
        source_kind="resource",
        build_name="PrepareCommitFields",
        index=ValueRef("TxIndex"),
        order=ValueRef("TxIndex"),
        target=TargetSpec(
            name="commit_transaction_helpers",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident",
                name="prepare_commit_fields_function_name",
                value=ValueRef("PrepareCommitFieldsFunctionName"),
            ),
        ),
    ),
    "ApplyPreparedCommitFields": ContributionSpec(
        name="ApplyPreparedCommitFields",
        source_name="ApplyPreparedCommitFieldsFunction",
        source_kind="resource",
        build_name="ApplyPreparedCommitFields",
        index=ValueRef("TxIndex"),
        order=ValueRef("TxIndex"),
        target=TargetSpec(
            name="commit_transaction_helpers",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident",
                name="apply_prepared_commit_fields_function_name",
                value=ValueRef("ApplyPreparedCommitFieldsFunctionName"),
            ),
        ),
    ),
    "RollbackFields": ContributionSpec(
        name="RollbackFields",
        source_name="RollbackFieldsFunction",
        source_kind="resource",
        build_name="RollbackFields",
        index=ValueRef("TxIndex"),
        order=ValueRef("TxIndex"),
        target=TargetSpec(
            name="rollback_transaction_helpers",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident",
                name="rollback_fields_function_name",
                value=ValueRef("RollbackFieldsFunctionName"),
            ),
        ),
    ),
    "PrepareCommitDispatch": ContributionSpec(
        name="PrepareCommitDispatch",
        source_name="PrepareCommitDispatchBranch",
        source_kind="resource",
        build_name="PrepareCommitDispatch",
        index=ValueRef("TxIndex"),
        order=ValueRef("TxIndex"),
        target=TargetSpec(
            name="prepare_commit_transaction_dispatch_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external",
                name="prepare_commit_fields_function_name",
                value=ValueRef("PrepareCommitFieldsFunctionName"),
            ),
            BindingSpec(
                kind="external", name="tx_index_value", value=ValueRef("TxIndex")
            ),
        ),
    ),
    "ApplyPreparedCommitDispatch": ContributionSpec(
        name="ApplyPreparedCommitDispatch",
        source_name="ApplyPreparedCommitDispatchBranch",
        source_kind="resource",
        build_name="ApplyPreparedCommitDispatch",
        index=ValueRef("TxIndex"),
        order=ValueRef("TxIndex"),
        target=TargetSpec(
            name="commit_transaction_dispatch_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external",
                name="apply_prepared_commit_fields_function_name",
                value=ValueRef("ApplyPreparedCommitFieldsFunctionName"),
            ),
            BindingSpec(
                kind="external", name="tx_index_value", value=ValueRef("TxIndex")
            ),
        ),
    ),
    "RollbackDispatch": ContributionSpec(
        name="RollbackDispatch",
        source_name="RollbackDispatchBranch",
        source_kind="resource",
        build_name="RollbackDispatch",
        index=ValueRef("TxIndex"),
        order=ValueRef("TxIndex"),
        target=TargetSpec(
            name="rollback_transaction_dispatch_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external",
                name="rollback_fields_function_name",
                value=ValueRef("RollbackFieldsFunctionName"),
            ),
            BindingSpec(
                kind="external", name="tx_index_value", value=ValueRef("TxIndex")
            ),
        ),
    ),
    "FieldDefaultFactoryBuilderParam": ContributionSpec(
        name="FieldDefaultFactoryBuilderParam",
        source_name="BuilderParam",
        source_kind="resource",
        build_name="FieldDefaultFactoryBuilderParam",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="builder_params",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="Root", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident",
                name="value_name",
                value=ValueRef("DefaultFactoryParamName"),
            ),
        ),
    ),
    "PlainInitParamDefaultFactory": ContributionSpec(
        name="PlainInitParamDefaultFactory",
        source_name="InitParamDefaultFactory",
        source_kind="resource",
        build_name="PlainInitParam",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="init_params",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(kind="ident", name="param_name", value=ValueRef("FieldName")),
            BindingSpec(
                kind="external", name="annotation", value=ValueRef("Annotation")
            ),
        ),
    ),
    "InitVarParamDefaultFactory": ContributionSpec(
        name="InitVarParamDefaultFactory",
        source_name="InitParamDefaultFactory",
        source_kind="resource",
        build_name="InitVarParam",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="init_params",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(kind="ident", name="param_name", value=ValueRef("FieldName")),
            BindingSpec(
                kind="external", name="annotation", value=ValueRef("Annotation")
            ),
        ),
    ),
    "ManagedInitParamDefaultFactory": ContributionSpec(
        name="ManagedInitParamDefaultFactory",
        source_name="InitParamDefaultFactory",
        source_kind="resource",
        build_name="ManagedInitParam",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="init_params",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(kind="ident", name="param_name", value=ValueRef("FieldName")),
            BindingSpec(
                kind="external", name="annotation", value=ValueRef("Annotation")
            ),
        ),
    ),
    "StoredDefaultFactoryEvalInitContribution": ContributionSpec(
        name="StoredDefaultFactoryEvalInitContribution",
        source_name="StoredDefaultFactoryEvalInit",
        source_kind="resource",
        build_name="DefaultFactoryEval",
        index=ValueRef("EvalOrder"),
        order=ValueRef("EvalStatementOrder"),
        target=TargetSpec(
            name="state_init_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident", name="field_name", value=ValueRef("EvalFieldName")
            ),
            BindingSpec(
                kind="ident",
                name="default_factory_name",
                value=ValueRef("EvalDefaultFactoryParamName"),
            ),
            BindingSpec(
                kind="external", name="state_slot", value=ValueRef("EvalStateSlotName")
            ),
        ),
    ),
    "StoredDefaultFactoryEvalNoInitContribution": ContributionSpec(
        name="StoredDefaultFactoryEvalNoInitContribution",
        source_name="StoredDefaultFactoryEvalNoInit",
        source_kind="resource",
        build_name="DefaultFactoryEval",
        index=ValueRef("EvalOrder"),
        order=ValueRef("EvalStatementOrder"),
        target=TargetSpec(
            name="state_init_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident", name="field_name", value=ValueRef("EvalFieldName")
            ),
            BindingSpec(
                kind="ident",
                name="default_factory_name",
                value=ValueRef("EvalDefaultFactoryParamName"),
            ),
            BindingSpec(
                kind="external", name="state_slot", value=ValueRef("EvalStateSlotName")
            ),
        ),
    ),
    "InitVarDefaultFactoryEvalInitContribution": ContributionSpec(
        name="InitVarDefaultFactoryEvalInitContribution",
        source_name="InitVarDefaultFactoryEvalInit",
        source_kind="resource",
        build_name="DefaultFactoryEval",
        index=ValueRef("EvalOrder"),
        order=ValueRef("EvalStatementOrder"),
        target=TargetSpec(
            name="state_init_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident", name="field_name", value=ValueRef("EvalFieldName")
            ),
            BindingSpec(
                kind="ident",
                name="default_factory_name",
                value=ValueRef("EvalDefaultFactoryParamName"),
            ),
        ),
    ),
    "InitVarDefaultFactoryEvalNoInitContribution": ContributionSpec(
        name="InitVarDefaultFactoryEvalNoInitContribution",
        source_name="InitVarDefaultFactoryEvalNoInit",
        source_kind="resource",
        build_name="DefaultFactoryEval",
        index=ValueRef("EvalOrder"),
        order=ValueRef("EvalStatementOrder"),
        target=TargetSpec(
            name="state_init_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="ident", name="field_name", value=ValueRef("EvalFieldName")
            ),
            BindingSpec(
                kind="ident",
                name="default_factory_name",
                value=ValueRef("EvalDefaultFactoryParamName"),
            ),
        ),
    ),
    "DefaultFactoryStoredArgContribution": ContributionSpec(
        name="DefaultFactoryStoredArgContribution",
        source_name="DefaultFactoryStoredArg",
        source_kind="resource",
        build_name="DefaultFactoryArg",
        index=TupleValueRef((ValueRef("ConsumerEvalOrder"), ValueRef("ParamOrder"))),
        order=ValueRef("ParamOrder"),
        target=TargetSpec(
            name="default_factory_args",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                            PathSegmentSpec(
                                kind="name",
                                name="DefaultFactoryEval",
                                indexes=(ValueRef("ConsumerEvalOrder"),),
                            ),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(kind="ident", name="param_name", value=ValueRef("ParamName")),
            BindingSpec(
                kind="external", name="provider_name", value=ValueRef("ProviderName")
            ),
        ),
    ),
    "DefaultFactoryLocalArgContribution": ContributionSpec(
        name="DefaultFactoryLocalArgContribution",
        source_name="DefaultFactoryLocalArg",
        source_kind="resource",
        build_name="DefaultFactoryArg",
        index=TupleValueRef((ValueRef("ConsumerEvalOrder"), ValueRef("ParamOrder"))),
        order=ValueRef("ParamOrder"),
        target=TargetSpec(
            name="default_factory_args",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                            PathSegmentSpec(
                                kind="name",
                                name="DefaultFactoryEval",
                                indexes=(ValueRef("ConsumerEvalOrder"),),
                            ),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(kind="ident", name="param_name", value=ValueRef("ParamName")),
            BindingSpec(
                kind="ident", name="provider_name", value=ValueRef("ProviderName")
            ),
        ),
    ),
    "ClassDefinition": ContributionSpec(
        name="ClassDefinition",
        source_name="ClassProduction",
        source_kind="production",
        build_name="ClassDef",
        index=ValueRef("ClassOrder"),
        order=ValueRef("ClassOrder"),
        target=TargetSpec(
            name="function_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="Root", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
}
ASSEMBLY_MATCHERS = {
    "BuilderParamContributions": ContributionMatcherSpec(
        name="BuilderParamContributions",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        default_contribution_name="LifecycleDefinitionBuilderParam",
        rules=(),
    ),
    "AnnotationsBuilderParamContributions": ContributionMatcherSpec(
        name="AnnotationsBuilderParamContributions",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        default_contribution_name="AnnotationsBuilderParam",
        rules=(),
    ),
    "TxGroupsBuilderParamContributions": ContributionMatcherSpec(
        name="TxGroupsBuilderParamContributions",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        default_contribution_name="TxGroupsBuilderParam",
        rules=(),
    ),
    "ReturnClassContributions": ContributionMatcherSpec(
        name="ReturnClassContributions",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        default_contribution_name="ReturnClassContribution",
        rules=(),
    ),
    "TransactionManagerInitParamContributions": ContributionMatcherSpec(
        name="TransactionManagerInitParamContributions",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        default_contribution_name="TransactionManagerInitParam",
        rules=(),
    ),
    "FacadeBaseBodyPassContributions": ContributionMatcherSpec(
        name="FacadeBaseBodyPassContributions",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        default_contribution_name="FacadeBaseBodyPass",
        rules=(),
    ),
    "FacadePropertiesPassContributions": ContributionMatcherSpec(
        name="FacadePropertiesPassContributions",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        default_contribution_name="FacadePropertiesPass",
        rules=(),
    ),
    "DefaultFacadePropertiesPassContributions": ContributionMatcherSpec(
        name="DefaultFacadePropertiesPassContributions",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        default_contribution_name="DefaultFacadePropertiesPass",
        rules=(),
    ),
    "CurrentFacadePropertiesPassContributions": ContributionMatcherSpec(
        name="CurrentFacadePropertiesPassContributions",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        default_contribution_name="CurrentFacadePropertiesPass",
        rules=(),
    ),
    "WorkingFacadePropertiesPassContributions": ContributionMatcherSpec(
        name="WorkingFacadePropertiesPassContributions",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        default_contribution_name="WorkingFacadePropertiesPass",
        rules=(),
    ),
    "StateInitBodyPassContributions": ContributionMatcherSpec(
        name="StateInitBodyPassContributions",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        default_contribution_name="StateInitBodyPass",
        rules=(),
    ),
    "CommitTransactionBodyPassContributions": ContributionMatcherSpec(
        name="CommitTransactionBodyPassContributions",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        default_contribution_name="CommitTransactionBodyPass",
        rules=(),
    ),
    "CommitTransactionDispatchBodyPassContributions": ContributionMatcherSpec(
        name="CommitTransactionDispatchBodyPassContributions",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        default_contribution_name="CommitTransactionDispatchBodyPass",
        rules=(),
    ),
    "PrepareCommitTransactionDispatchBodyPassContributions": ContributionMatcherSpec(
        name="PrepareCommitTransactionDispatchBodyPassContributions",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        default_contribution_name="PrepareCommitTransactionDispatchBodyPass",
        rules=(),
    ),
    "RollbackTransactionBodyPassContributions": ContributionMatcherSpec(
        name="RollbackTransactionBodyPassContributions",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        default_contribution_name="RollbackTransactionBodyPass",
        rules=(),
    ),
    "RollbackTransactionDispatchBodyPassContributions": ContributionMatcherSpec(
        name="RollbackTransactionDispatchBodyPassContributions",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        default_contribution_name="RollbackTransactionDispatchBodyPass",
        rules=(),
    ),
    "CommitOrderKeyBodyPassContributions": ContributionMatcherSpec(
        name="CommitOrderKeyBodyPassContributions",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        default_contribution_name="CommitOrderKeyBodyPass",
        rules=(),
    ),
    "RequiresValidationBodyPassContributions": ContributionMatcherSpec(
        name="RequiresValidationBodyPassContributions",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        default_contribution_name="RequiresValidationBodyPass",
        rules=(),
    ),
    "ValidateCommitBodyPassContributions": ContributionMatcherSpec(
        name="ValidateCommitBodyPassContributions",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        default_contribution_name="ValidateCommitBodyPass",
        rules=(),
    ),
    "BeforeCommitBodyPassContributions": ContributionMatcherSpec(
        name="BeforeCommitBodyPassContributions",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        default_contribution_name="BeforeCommitBodyPass",
        rules=(),
    ),
    "AfterCommitBodyPassContributions": ContributionMatcherSpec(
        name="AfterCommitBodyPassContributions",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        default_contribution_name="AfterCommitBodyPass",
        rules=(),
    ),
    "AfterRollbackBodyPassContributions": ContributionMatcherSpec(
        name="AfterRollbackBodyPassContributions",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        default_contribution_name="AfterRollbackBodyPass",
        rules=(),
    ),
    "PlainStateSlotContributions": ContributionMatcherSpec(
        name="PlainStateSlotContributions",
        inputs=(
            AssemblyInputSpec(
                name="field", collection_name="PlainFields", collection=None
            ),
        ),
        default_contribution_name="PlainStateSlot",
        rules=(),
    ),
    "InitVarLocalDefaultContributions": ContributionMatcherSpec(
        name="InitVarLocalDefaultContributions",
        inputs=(
            AssemblyInputSpec(
                name="field", collection_name="InitVarFields", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="default_value",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("Init"), right=LiteralValueRef(False)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefault"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefaultFactory"),
                            right=LiteralValueRef(False),
                        ),
                    )
                ),
                contribution_name="InitVarLocalDefault",
                weight=1.0,
            ),
        ),
    ),
    "PlainInitAssignmentContributions": ContributionMatcherSpec(
        name="PlainInitAssignmentContributions",
        inputs=(
            AssemblyInputSpec(
                name="field", collection_name="PlainFields", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="init_field",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("Init"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefaultFactory"),
                            right=LiteralValueRef(False),
                        ),
                    )
                ),
                contribution_name="PlainInitAssignment",
                weight=1.0,
            ),
            ContributionRuleSpec(
                name="default_value",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("Init"), right=LiteralValueRef(False)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefault"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefaultFactory"),
                            right=LiteralValueRef(False),
                        ),
                    )
                ),
                contribution_name="PlainDefaultAssignment",
                weight=1.0,
            ),
        ),
    ),
    "PlainPropertyContributions": ContributionMatcherSpec(
        name="PlainPropertyContributions",
        inputs=(
            AssemblyInputSpec(
                name="field", collection_name="PlainFields", collection=None
            ),
        ),
        default_contribution_name="PlainFieldProperty",
        rules=(),
    ),
    "ClassVarDefaultContributions": ContributionMatcherSpec(
        name="ClassVarDefaultContributions",
        inputs=(
            AssemblyInputSpec(
                name="field", collection_name="ClassVarFields", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="has_default",
                condition=EqConditionSpec(
                    left=ValueRef("HasDefault"), right=LiteralValueRef(True)
                ),
                contribution_name="ClassVarDefault",
                weight=1.0,
            ),
        ),
    ),
    "CommitOrderKeyContributions": ContributionMatcherSpec(
        name="CommitOrderKeyContributions",
        inputs=(
            AssemblyInputSpec(
                name="method",
                collection_name="CommitOrderKeyProviders",
                collection=None,
            ),
        ),
        default_contribution_name="CommitOrderKeyBranchContribution",
        rules=(),
    ),
    "RequiresValidationContributions": ContributionMatcherSpec(
        name="RequiresValidationContributions",
        inputs=(
            AssemblyInputSpec(
                name="method", collection_name="CommitValidators", collection=None
            ),
        ),
        default_contribution_name="RequiresValidationBranchContribution",
        rules=(),
    ),
    "ValidateCommitContributions": ContributionMatcherSpec(
        name="ValidateCommitContributions",
        inputs=(
            AssemblyInputSpec(
                name="method", collection_name="CommitValidators", collection=None
            ),
        ),
        default_contribution_name="ValidateCommitBranchContribution",
        rules=(),
    ),
    "BeforeCommitHookContributions": ContributionMatcherSpec(
        name="BeforeCommitHookContributions",
        inputs=(
            AssemblyInputSpec(
                name="method", collection_name="BeforeCommitHooks", collection=None
            ),
        ),
        default_contribution_name="BeforeCommitHookContribution",
        rules=(),
    ),
    "AfterCommitHookContributions": ContributionMatcherSpec(
        name="AfterCommitHookContributions",
        inputs=(
            AssemblyInputSpec(
                name="method", collection_name="AfterCommitHooks", collection=None
            ),
        ),
        default_contribution_name="AfterCommitHookContribution",
        rules=(),
    ),
    "AfterRollbackHookContributions": ContributionMatcherSpec(
        name="AfterRollbackHookContributions",
        inputs=(
            AssemblyInputSpec(
                name="method", collection_name="AfterRollbackHooks", collection=None
            ),
        ),
        default_contribution_name="AfterRollbackHookContribution",
        rules=(),
    ),
    "FieldDefaultBuilderParamContributions": ContributionMatcherSpec(
        name="FieldDefaultBuilderParamContributions",
        inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="has_default",
                condition=EqConditionSpec(
                    left=ValueRef("HasDefault"), right=LiteralValueRef(True)
                ),
                contribution_name="FieldDefaultBuilderParam",
                weight=1.0,
            ),
            ContributionRuleSpec(
                name="has_default_factory",
                condition=EqConditionSpec(
                    left=ValueRef("HasDefaultFactory"), right=LiteralValueRef(True)
                ),
                contribution_name="FieldDefaultFactoryBuilderParam",
                weight=1.0,
            ),
        ),
    ),
    "CoreClassDefinitionContributions": ContributionMatcherSpec(
        name="CoreClassDefinitionContributions",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        default_contribution_name="CoreClassDefinition",
        rules=(),
    ),
    "PlainInitParamContributions": ContributionMatcherSpec(
        name="PlainInitParamContributions",
        inputs=(
            AssemblyInputSpec(
                name="field", collection_name="PlainFields", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="required",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("Init"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefault"), right=LiteralValueRef(False)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefaultFactory"),
                            right=LiteralValueRef(False),
                        ),
                    )
                ),
                contribution_name="PlainInitParamRequired",
                weight=1.0,
            ),
            ContributionRuleSpec(
                name="default_value",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("Init"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefault"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefaultFactory"),
                            right=LiteralValueRef(False),
                        ),
                    )
                ),
                contribution_name="PlainInitParamDefault",
                weight=1.0,
            ),
            ContributionRuleSpec(
                name="default_factory",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("Init"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefaultFactory"),
                            right=LiteralValueRef(True),
                        ),
                    )
                ),
                contribution_name="PlainInitParamDefaultFactory",
                weight=1.0,
            ),
        ),
    ),
    "InitVarParamContributions": ContributionMatcherSpec(
        name="InitVarParamContributions",
        inputs=(
            AssemblyInputSpec(
                name="field", collection_name="InitVarFields", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="required",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("Init"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefault"), right=LiteralValueRef(False)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefaultFactory"),
                            right=LiteralValueRef(False),
                        ),
                    )
                ),
                contribution_name="InitVarParamRequired",
                weight=1.0,
            ),
            ContributionRuleSpec(
                name="default_value",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("Init"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefault"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefaultFactory"),
                            right=LiteralValueRef(False),
                        ),
                    )
                ),
                contribution_name="InitVarParamDefault",
                weight=1.0,
            ),
            ContributionRuleSpec(
                name="default_factory",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("Init"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefaultFactory"),
                            right=LiteralValueRef(True),
                        ),
                    )
                ),
                contribution_name="InitVarParamDefaultFactory",
                weight=1.0,
            ),
        ),
    ),
    "ManagedCurrentStateSlotContributions": ContributionMatcherSpec(
        name="ManagedCurrentStateSlotContributions",
        inputs=(
            AssemblyInputSpec(
                name="field", collection_name="ManagedFields", collection=None
            ),
        ),
        default_contribution_name="ManagedCurrentStateSlot",
        rules=(),
    ),
    "ManagedWorkingStateSlotContributions": ContributionMatcherSpec(
        name="ManagedWorkingStateSlotContributions",
        inputs=(
            AssemblyInputSpec(
                name="field", collection_name="ManagedFields", collection=None
            ),
        ),
        default_contribution_name="ManagedWorkingStateSlot",
        rules=(),
    ),
    "ManagedStagedStateSlotContributions": ContributionMatcherSpec(
        name="ManagedStagedStateSlotContributions",
        inputs=(
            AssemblyInputSpec(
                name="field", collection_name="ManagedFields", collection=None
            ),
        ),
        default_contribution_name="ManagedStagedStateSlot",
        rules=(),
    ),
    "ManagedFreezeBuilderParamContributions": ContributionMatcherSpec(
        name="ManagedFreezeBuilderParamContributions",
        inputs=(
            AssemblyInputSpec(
                name="field", collection_name="ManagedFields", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="has_freeze",
                condition=EqConditionSpec(
                    left=ValueRef("HasFreeze"), right=LiteralValueRef(True)
                ),
                contribution_name="ManagedFreezeBuilderParam",
                weight=1.0,
            ),
        ),
    ),
    "ManagedThawBuilderParamContributions": ContributionMatcherSpec(
        name="ManagedThawBuilderParamContributions",
        inputs=(
            AssemblyInputSpec(
                name="field", collection_name="ManagedFields", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="has_thaw",
                condition=EqConditionSpec(
                    left=ValueRef("HasThaw"), right=LiteralValueRef(True)
                ),
                contribution_name="ManagedThawBuilderParam",
                weight=1.0,
            ),
        ),
    ),
    "ManagedCurrentInitAssignmentContributions": ContributionMatcherSpec(
        name="ManagedCurrentInitAssignmentContributions",
        inputs=(
            AssemblyInputSpec(
                name="field", collection_name="ManagedFields", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="init_field",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("Init"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefaultFactory"),
                            right=LiteralValueRef(False),
                        ),
                    )
                ),
                contribution_name="ManagedCurrentInitAssignment",
                weight=1.0,
            ),
            ContributionRuleSpec(
                name="default_value",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("Init"), right=LiteralValueRef(False)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefault"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefaultFactory"),
                            right=LiteralValueRef(False),
                        ),
                    )
                ),
                contribution_name="ManagedCurrentDefaultAssignment",
                weight=1.0,
            ),
        ),
    ),
    "ManagedWorkingInitAssignmentContributions": ContributionMatcherSpec(
        name="ManagedWorkingInitAssignmentContributions",
        inputs=(
            AssemblyInputSpec(
                name="field", collection_name="ManagedFields", collection=None
            ),
        ),
        default_contribution_name="ManagedWorkingInitAssignment",
        rules=(),
    ),
    "ManagedStagedInitAssignmentContributions": ContributionMatcherSpec(
        name="ManagedStagedInitAssignmentContributions",
        inputs=(
            AssemblyInputSpec(
                name="field", collection_name="ManagedFields", collection=None
            ),
        ),
        default_contribution_name="ManagedStagedInitAssignment",
        rules=(),
    ),
    "ManagedDefaultFacadePropertyContributions": ContributionMatcherSpec(
        name="ManagedDefaultFacadePropertyContributions",
        inputs=(
            AssemblyInputSpec(
                name="field",
                collection_name="IndexedTransactionalFields",
                collection=None,
            ),
        ),
        default_contribution_name="ManagedDefaultFacadeProperty",
        rules=(),
    ),
    "ManagedCurrentFacadePropertyContributions": ContributionMatcherSpec(
        name="ManagedCurrentFacadePropertyContributions",
        inputs=(
            AssemblyInputSpec(
                name="field",
                collection_name="IndexedTransactionalFields",
                collection=None,
            ),
        ),
        default_contribution_name="ManagedCurrentFacadeProperty",
        rules=(),
    ),
    "ManagedWorkingFacadePropertyContributions": ContributionMatcherSpec(
        name="ManagedWorkingFacadePropertyContributions",
        inputs=(
            AssemblyInputSpec(
                name="field",
                collection_name="IndexedTransactionalFields",
                collection=None,
            ),
        ),
        default_contribution_name="ManagedWorkingFacadeProperty",
        rules=(
            ContributionRuleSpec(
                name="with_optional_thaw",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("HasThaw"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasOptionalNone"),
                            right=LiteralValueRef(True),
                        ),
                    )
                ),
                contribution_name="ManagedOptionalThawWorkingFacadeProperty",
                weight=1.0,
            ),
            ContributionRuleSpec(
                name="with_thaw",
                condition=EqConditionSpec(
                    left=ValueRef("HasThaw"), right=LiteralValueRef(True)
                ),
                contribution_name="ManagedThawWorkingFacadeProperty",
                weight=1.0,
            ),
        ),
    ),
    "ManagedPrepareCommitContributions": ContributionMatcherSpec(
        name="ManagedPrepareCommitContributions",
        inputs=(
            AssemblyInputSpec(
                name="field",
                collection_name="IndexedTransactionalFields",
                collection=None,
            ),
        ),
        default_contribution_name="ManagedPlainPrepareCommit",
        rules=(
            ContributionRuleSpec(
                name="with_optional_freeze",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("HasFreeze"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasOptionalNone"),
                            right=LiteralValueRef(True),
                        ),
                    )
                ),
                contribution_name="ManagedOptionalFreezePrepareCommit",
                weight=1.0,
            ),
            ContributionRuleSpec(
                name="with_freeze",
                condition=EqConditionSpec(
                    left=ValueRef("HasFreeze"), right=LiteralValueRef(True)
                ),
                contribution_name="ManagedFreezePrepareCommit",
                weight=1.0,
            ),
        ),
    ),
    "ManagedApplyPreparedCommitContributions": ContributionMatcherSpec(
        name="ManagedApplyPreparedCommitContributions",
        inputs=(
            AssemblyInputSpec(
                name="field",
                collection_name="IndexedTransactionalFields",
                collection=None,
            ),
        ),
        default_contribution_name="ManagedApplyPreparedCommit",
        rules=(),
    ),
    "ManagedRollbackContributions": ContributionMatcherSpec(
        name="ManagedRollbackContributions",
        inputs=(
            AssemblyInputSpec(
                name="field",
                collection_name="IndexedTransactionalFields",
                collection=None,
            ),
        ),
        default_contribution_name="ManagedRollback",
        rules=(),
    ),
    "PrepareCommitFieldsBodyPassContributions": ContributionMatcherSpec(
        name="PrepareCommitFieldsBodyPassContributions",
        inputs=(
            AssemblyInputSpec(
                name="tx_group", collection_name="TxGroups", collection=None
            ),
        ),
        default_contribution_name="PrepareCommitFieldsBodyPass",
        rules=(),
    ),
    "ApplyPreparedCommitFieldsBodyPassContributions": ContributionMatcherSpec(
        name="ApplyPreparedCommitFieldsBodyPassContributions",
        inputs=(
            AssemblyInputSpec(
                name="tx_group", collection_name="TxGroups", collection=None
            ),
        ),
        default_contribution_name="ApplyPreparedCommitFieldsBodyPass",
        rules=(),
    ),
    "RollbackFieldsBodyPassContributions": ContributionMatcherSpec(
        name="RollbackFieldsBodyPassContributions",
        inputs=(
            AssemblyInputSpec(
                name="tx_group", collection_name="TxGroups", collection=None
            ),
        ),
        default_contribution_name="RollbackFieldsBodyPass",
        rules=(),
    ),
    "ApplyPreparedCommitFieldsContributions": ContributionMatcherSpec(
        name="ApplyPreparedCommitFieldsContributions",
        inputs=(
            AssemblyInputSpec(
                name="tx_group", collection_name="TxGroups", collection=None
            ),
        ),
        default_contribution_name="ApplyPreparedCommitFields",
        rules=(),
    ),
    "PrepareCommitFieldsContributions": ContributionMatcherSpec(
        name="PrepareCommitFieldsContributions",
        inputs=(
            AssemblyInputSpec(
                name="tx_group", collection_name="TxGroups", collection=None
            ),
        ),
        default_contribution_name="PrepareCommitFields",
        rules=(),
    ),
    "RollbackFieldsContributions": ContributionMatcherSpec(
        name="RollbackFieldsContributions",
        inputs=(
            AssemblyInputSpec(
                name="tx_group", collection_name="TxGroups", collection=None
            ),
        ),
        default_contribution_name="RollbackFields",
        rules=(),
    ),
    "PrepareCommitDispatchContributions": ContributionMatcherSpec(
        name="PrepareCommitDispatchContributions",
        inputs=(
            AssemblyInputSpec(
                name="tx_group", collection_name="TxGroups", collection=None
            ),
        ),
        default_contribution_name="PrepareCommitDispatch",
        rules=(),
    ),
    "ApplyPreparedCommitDispatchContributions": ContributionMatcherSpec(
        name="ApplyPreparedCommitDispatchContributions",
        inputs=(
            AssemblyInputSpec(
                name="tx_group", collection_name="TxGroups", collection=None
            ),
        ),
        default_contribution_name="ApplyPreparedCommitDispatch",
        rules=(),
    ),
    "RollbackDispatchContributions": ContributionMatcherSpec(
        name="RollbackDispatchContributions",
        inputs=(
            AssemblyInputSpec(
                name="tx_group", collection_name="TxGroups", collection=None
            ),
        ),
        default_contribution_name="RollbackDispatch",
        rules=(),
    ),
    "ManagedInitParamContributions": ContributionMatcherSpec(
        name="ManagedInitParamContributions",
        inputs=(
            AssemblyInputSpec(
                name="field", collection_name="ManagedFields", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="required",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("Init"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefault"), right=LiteralValueRef(False)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefaultFactory"),
                            right=LiteralValueRef(False),
                        ),
                    )
                ),
                contribution_name="ManagedInitParamRequired",
                weight=1.0,
            ),
            ContributionRuleSpec(
                name="default_value",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("Init"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefault"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefaultFactory"),
                            right=LiteralValueRef(False),
                        ),
                    )
                ),
                contribution_name="ManagedInitParamDefault",
                weight=1.0,
            ),
            ContributionRuleSpec(
                name="default_factory",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("Init"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefaultFactory"),
                            right=LiteralValueRef(True),
                        ),
                    )
                ),
                contribution_name="ManagedInitParamDefaultFactory",
                weight=1.0,
            ),
        ),
    ),
    "DefaultFactoryEvalContributions": ContributionMatcherSpec(
        name="DefaultFactoryEvalContributions",
        inputs=(
            AssemblyInputSpec(
                name="step",
                collection_name="DefaultFactoryEvaluationSteps",
                collection=None,
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="field_init",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("EvalFieldKind"),
                            right=LiteralValueRef("field"),
                        ),
                        EqConditionSpec(
                            left=ValueRef("EvalInit"), right=LiteralValueRef(True)
                        ),
                    )
                ),
                contribution_name="StoredDefaultFactoryEvalInitContribution",
                weight=1.0,
            ),
            ContributionRuleSpec(
                name="field_no_init",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("EvalFieldKind"),
                            right=LiteralValueRef("field"),
                        ),
                        EqConditionSpec(
                            left=ValueRef("EvalInit"), right=LiteralValueRef(False)
                        ),
                    )
                ),
                contribution_name="StoredDefaultFactoryEvalNoInitContribution",
                weight=1.0,
            ),
            ContributionRuleSpec(
                name="managed_init",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("EvalFieldKind"),
                            right=LiteralValueRef("managed"),
                        ),
                        EqConditionSpec(
                            left=ValueRef("EvalInit"), right=LiteralValueRef(True)
                        ),
                    )
                ),
                contribution_name="StoredDefaultFactoryEvalInitContribution",
                weight=1.0,
            ),
            ContributionRuleSpec(
                name="managed_no_init",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("EvalFieldKind"),
                            right=LiteralValueRef("managed"),
                        ),
                        EqConditionSpec(
                            left=ValueRef("EvalInit"), right=LiteralValueRef(False)
                        ),
                    )
                ),
                contribution_name="StoredDefaultFactoryEvalNoInitContribution",
                weight=1.0,
            ),
            ContributionRuleSpec(
                name="initvar_init",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("EvalFieldKind"),
                            right=LiteralValueRef("initvar"),
                        ),
                        EqConditionSpec(
                            left=ValueRef("EvalInit"), right=LiteralValueRef(True)
                        ),
                    )
                ),
                contribution_name="InitVarDefaultFactoryEvalInitContribution",
                weight=1.0,
            ),
            ContributionRuleSpec(
                name="initvar_no_init",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("EvalFieldKind"),
                            right=LiteralValueRef("initvar"),
                        ),
                        EqConditionSpec(
                            left=ValueRef("EvalInit"), right=LiteralValueRef(False)
                        ),
                    )
                ),
                contribution_name="InitVarDefaultFactoryEvalNoInitContribution",
                weight=1.0,
            ),
        ),
    ),
    "DefaultFactoryArgContributions": ContributionMatcherSpec(
        name="DefaultFactoryArgContributions",
        inputs=(
            AssemblyInputSpec(
                name="dep",
                collection_name="DefaultFactoryDependencies",
                collection=None,
            ),
        ),
        default_contribution_name="DefaultFactoryStoredArgContribution",
        rules=(
            ContributionRuleSpec(
                name="local_provider",
                condition=EqConditionSpec(
                    left=ValueRef("ProviderFieldKind"), right=LiteralValueRef("initvar")
                ),
                contribution_name="DefaultFactoryLocalArgContribution",
                weight=1.0,
            ),
        ),
    ),
    "ClassDefinitionContributions": ContributionMatcherSpec(
        name="ClassDefinitionContributions",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        default_contribution_name="ClassDefinition",
        rules=(),
    ),
}
ASSEMBLY_EDGES = {
    "CoreModuleProduction.lifecycle_definition_params": AssemblyEdgeSpec(
        name="CoreModuleProduction.lifecycle_definition_params",
        context_inputs=(),
        from_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        condition=None,
        matcher_name="BuilderParamContributions",
    ),
    "CoreModuleProduction.annotations_params": AssemblyEdgeSpec(
        name="CoreModuleProduction.annotations_params",
        context_inputs=(),
        from_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        condition=None,
        matcher_name="AnnotationsBuilderParamContributions",
    ),
    "CoreModuleProduction.tx_groups_params": AssemblyEdgeSpec(
        name="CoreModuleProduction.tx_groups_params",
        context_inputs=(),
        from_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        condition=None,
        matcher_name="TxGroupsBuilderParamContributions",
    ),
    "CoreModuleProduction.field_default_params": AssemblyEdgeSpec(
        name="CoreModuleProduction.field_default_params",
        context_inputs=(),
        from_inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
        ),
        condition=None,
        matcher_name="FieldDefaultBuilderParamContributions",
    ),
    "CoreModuleProduction.classes": AssemblyEdgeSpec(
        name="CoreModuleProduction.classes",
        context_inputs=(),
        from_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        condition=None,
        matcher_name="CoreClassDefinitionContributions",
    ),
    "CoreModuleProduction.return_class": AssemblyEdgeSpec(
        name="CoreModuleProduction.return_class",
        context_inputs=(),
        from_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        condition=None,
        matcher_name="ReturnClassContributions",
    ),
    "CoreClassProduction.state_slots": AssemblyEdgeSpec(
        name="CoreClassProduction.state_slots",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field", collection_name="PlainFields", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="PlainStateSlotContributions",
    ),
    "CoreClassProduction.transaction_manager_param": AssemblyEdgeSpec(
        name="CoreClassProduction.transaction_manager_param",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="TransactionManagerInitParamContributions",
    ),
    "CoreClassProduction.facade_base_body_pass": AssemblyEdgeSpec(
        name="CoreClassProduction.facade_base_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="FacadeBaseBodyPassContributions",
    ),
    "CoreClassProduction.facade_properties_pass": AssemblyEdgeSpec(
        name="CoreClassProduction.facade_properties_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="FacadePropertiesPassContributions",
    ),
    "CoreClassProduction.default_facade_properties_pass": AssemblyEdgeSpec(
        name="CoreClassProduction.default_facade_properties_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="DefaultFacadePropertiesPassContributions",
    ),
    "CoreClassProduction.current_facade_properties_pass": AssemblyEdgeSpec(
        name="CoreClassProduction.current_facade_properties_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="CurrentFacadePropertiesPassContributions",
    ),
    "CoreClassProduction.working_facade_properties_pass": AssemblyEdgeSpec(
        name="CoreClassProduction.working_facade_properties_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="WorkingFacadePropertiesPassContributions",
    ),
    "CoreClassProduction.state_init_body_pass": AssemblyEdgeSpec(
        name="CoreClassProduction.state_init_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="StateInitBodyPassContributions",
    ),
    "CoreClassProduction.commit_transaction_body_pass": AssemblyEdgeSpec(
        name="CoreClassProduction.commit_transaction_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="CommitTransactionBodyPassContributions",
    ),
    "CoreClassProduction.commit_transaction_dispatch_body_pass": AssemblyEdgeSpec(
        name="CoreClassProduction.commit_transaction_dispatch_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="CommitTransactionDispatchBodyPassContributions",
    ),
    "CoreClassProduction.prepare_commit_transaction_dispatch_body_pass": AssemblyEdgeSpec(
        name="CoreClassProduction.prepare_commit_transaction_dispatch_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="PrepareCommitTransactionDispatchBodyPassContributions",
    ),
    "CoreClassProduction.rollback_transaction_body_pass": AssemblyEdgeSpec(
        name="CoreClassProduction.rollback_transaction_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="RollbackTransactionBodyPassContributions",
    ),
    "CoreClassProduction.rollback_transaction_dispatch_body_pass": AssemblyEdgeSpec(
        name="CoreClassProduction.rollback_transaction_dispatch_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="RollbackTransactionDispatchBodyPassContributions",
    ),
    "CoreClassProduction.commit_order_key_body_pass": AssemblyEdgeSpec(
        name="CoreClassProduction.commit_order_key_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="CommitOrderKeyBodyPassContributions",
    ),
    "CoreClassProduction.requires_validation_body_pass": AssemblyEdgeSpec(
        name="CoreClassProduction.requires_validation_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="RequiresValidationBodyPassContributions",
    ),
    "CoreClassProduction.validate_commit_body_pass": AssemblyEdgeSpec(
        name="CoreClassProduction.validate_commit_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="ValidateCommitBodyPassContributions",
    ),
    "CoreClassProduction.before_commit_body_pass": AssemblyEdgeSpec(
        name="CoreClassProduction.before_commit_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="BeforeCommitBodyPassContributions",
    ),
    "CoreClassProduction.after_commit_body_pass": AssemblyEdgeSpec(
        name="CoreClassProduction.after_commit_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="AfterCommitBodyPassContributions",
    ),
    "CoreClassProduction.after_rollback_body_pass": AssemblyEdgeSpec(
        name="CoreClassProduction.after_rollback_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="AfterRollbackBodyPassContributions",
    ),
    "CoreClassProduction.classvars": AssemblyEdgeSpec(
        name="CoreClassProduction.classvars",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field", collection_name="ClassVarFields", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="ClassVarDefaultContributions",
    ),
    "CoreClassProduction.commit_order_keys": AssemblyEdgeSpec(
        name="CoreClassProduction.commit_order_keys",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="method",
                collection_name="CommitOrderKeyProviders",
                collection=None,
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("MethodOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="CommitOrderKeyContributions",
    ),
    "CoreClassProduction.validation_flags": AssemblyEdgeSpec(
        name="CoreClassProduction.validation_flags",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="method", collection_name="CommitValidators", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("MethodOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="RequiresValidationContributions",
    ),
    "CoreClassProduction.validators": AssemblyEdgeSpec(
        name="CoreClassProduction.validators",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="method", collection_name="CommitValidators", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("MethodOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="ValidateCommitContributions",
    ),
    "CoreClassProduction.before_commit_hooks": AssemblyEdgeSpec(
        name="CoreClassProduction.before_commit_hooks",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="method", collection_name="BeforeCommitHooks", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("MethodOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="BeforeCommitHookContributions",
    ),
    "CoreClassProduction.after_commit_hooks": AssemblyEdgeSpec(
        name="CoreClassProduction.after_commit_hooks",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="method", collection_name="AfterCommitHooks", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("MethodOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="AfterCommitHookContributions",
    ),
    "CoreClassProduction.after_rollback_hooks": AssemblyEdgeSpec(
        name="CoreClassProduction.after_rollback_hooks",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="method", collection_name="AfterRollbackHooks", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("MethodOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="AfterRollbackHookContributions",
    ),
    "CoreClassProduction.plain_init_params": AssemblyEdgeSpec(
        name="CoreClassProduction.plain_init_params",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field", collection_name="PlainFields", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="PlainInitParamContributions",
    ),
    "CoreClassProduction.initvar_params": AssemblyEdgeSpec(
        name="CoreClassProduction.initvar_params",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field", collection_name="InitVarFields", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="InitVarParamContributions",
    ),
    "CoreClassProduction.initvar_local_defaults": AssemblyEdgeSpec(
        name="CoreClassProduction.initvar_local_defaults",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field", collection_name="InitVarFields", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="InitVarLocalDefaultContributions",
    ),
    "CoreClassProduction.plain_init_assignments": AssemblyEdgeSpec(
        name="CoreClassProduction.plain_init_assignments",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field", collection_name="PlainFields", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="PlainInitAssignmentContributions",
    ),
    "CoreClassProduction.plain_properties": AssemblyEdgeSpec(
        name="CoreClassProduction.plain_properties",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field", collection_name="PlainFields", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="PlainPropertyContributions",
    ),
    "ModuleProduction.lifecycle_definition_params": AssemblyEdgeSpec(
        name="ModuleProduction.lifecycle_definition_params",
        context_inputs=(),
        from_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        condition=None,
        matcher_name="BuilderParamContributions",
    ),
    "ModuleProduction.annotations_params": AssemblyEdgeSpec(
        name="ModuleProduction.annotations_params",
        context_inputs=(),
        from_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        condition=None,
        matcher_name="AnnotationsBuilderParamContributions",
    ),
    "ModuleProduction.tx_groups_params": AssemblyEdgeSpec(
        name="ModuleProduction.tx_groups_params",
        context_inputs=(),
        from_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        condition=None,
        matcher_name="TxGroupsBuilderParamContributions",
    ),
    "ModuleProduction.field_default_params": AssemblyEdgeSpec(
        name="ModuleProduction.field_default_params",
        context_inputs=(),
        from_inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
        ),
        condition=None,
        matcher_name="FieldDefaultBuilderParamContributions",
    ),
    "ModuleProduction.managed_freeze_params": AssemblyEdgeSpec(
        name="ModuleProduction.managed_freeze_params",
        context_inputs=(),
        from_inputs=(
            AssemblyInputSpec(
                name="field", collection_name="ManagedFields", collection=None
            ),
        ),
        condition=None,
        matcher_name="ManagedFreezeBuilderParamContributions",
    ),
    "ModuleProduction.managed_thaw_params": AssemblyEdgeSpec(
        name="ModuleProduction.managed_thaw_params",
        context_inputs=(),
        from_inputs=(
            AssemblyInputSpec(
                name="field", collection_name="ManagedFields", collection=None
            ),
        ),
        condition=None,
        matcher_name="ManagedThawBuilderParamContributions",
    ),
    "ModuleProduction.classes": AssemblyEdgeSpec(
        name="ModuleProduction.classes",
        context_inputs=(),
        from_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        condition=None,
        matcher_name="ClassDefinitionContributions",
    ),
    "ModuleProduction.return_class": AssemblyEdgeSpec(
        name="ModuleProduction.return_class",
        context_inputs=(),
        from_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        condition=None,
        matcher_name="ReturnClassContributions",
    ),
    "ClassProduction.state_slots": AssemblyEdgeSpec(
        name="ClassProduction.state_slots",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field", collection_name="PlainFields", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="PlainStateSlotContributions",
    ),
    "ClassProduction.managed_current_state_slots": AssemblyEdgeSpec(
        name="ClassProduction.managed_current_state_slots",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field", collection_name="ManagedFields", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="ManagedCurrentStateSlotContributions",
    ),
    "ClassProduction.managed_working_state_slots": AssemblyEdgeSpec(
        name="ClassProduction.managed_working_state_slots",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field", collection_name="ManagedFields", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="ManagedWorkingStateSlotContributions",
    ),
    "ClassProduction.managed_staged_state_slots": AssemblyEdgeSpec(
        name="ClassProduction.managed_staged_state_slots",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field", collection_name="ManagedFields", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="ManagedStagedStateSlotContributions",
    ),
    "ClassProduction.transaction_manager_param": AssemblyEdgeSpec(
        name="ClassProduction.transaction_manager_param",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="TransactionManagerInitParamContributions",
    ),
    "ClassProduction.facade_base_body_pass": AssemblyEdgeSpec(
        name="ClassProduction.facade_base_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="FacadeBaseBodyPassContributions",
    ),
    "ClassProduction.facade_properties_pass": AssemblyEdgeSpec(
        name="ClassProduction.facade_properties_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="FacadePropertiesPassContributions",
    ),
    "ClassProduction.default_facade_properties_pass": AssemblyEdgeSpec(
        name="ClassProduction.default_facade_properties_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="DefaultFacadePropertiesPassContributions",
    ),
    "ClassProduction.current_facade_properties_pass": AssemblyEdgeSpec(
        name="ClassProduction.current_facade_properties_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="CurrentFacadePropertiesPassContributions",
    ),
    "ClassProduction.working_facade_properties_pass": AssemblyEdgeSpec(
        name="ClassProduction.working_facade_properties_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="WorkingFacadePropertiesPassContributions",
    ),
    "ClassProduction.state_init_body_pass": AssemblyEdgeSpec(
        name="ClassProduction.state_init_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="StateInitBodyPassContributions",
    ),
    "ClassProduction.commit_transaction_body_pass": AssemblyEdgeSpec(
        name="ClassProduction.commit_transaction_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="CommitTransactionBodyPassContributions",
    ),
    "ClassProduction.commit_transaction_dispatch_body_pass": AssemblyEdgeSpec(
        name="ClassProduction.commit_transaction_dispatch_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="CommitTransactionDispatchBodyPassContributions",
    ),
    "ClassProduction.prepare_commit_transaction_dispatch_body_pass": AssemblyEdgeSpec(
        name="ClassProduction.prepare_commit_transaction_dispatch_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="PrepareCommitTransactionDispatchBodyPassContributions",
    ),
    "ClassProduction.rollback_transaction_body_pass": AssemblyEdgeSpec(
        name="ClassProduction.rollback_transaction_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="RollbackTransactionBodyPassContributions",
    ),
    "ClassProduction.rollback_transaction_dispatch_body_pass": AssemblyEdgeSpec(
        name="ClassProduction.rollback_transaction_dispatch_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="RollbackTransactionDispatchBodyPassContributions",
    ),
    "ClassProduction.commit_order_key_body_pass": AssemblyEdgeSpec(
        name="ClassProduction.commit_order_key_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="CommitOrderKeyBodyPassContributions",
    ),
    "ClassProduction.requires_validation_body_pass": AssemblyEdgeSpec(
        name="ClassProduction.requires_validation_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="RequiresValidationBodyPassContributions",
    ),
    "ClassProduction.validate_commit_body_pass": AssemblyEdgeSpec(
        name="ClassProduction.validate_commit_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="ValidateCommitBodyPassContributions",
    ),
    "ClassProduction.before_commit_body_pass": AssemblyEdgeSpec(
        name="ClassProduction.before_commit_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="BeforeCommitBodyPassContributions",
    ),
    "ClassProduction.after_commit_body_pass": AssemblyEdgeSpec(
        name="ClassProduction.after_commit_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="AfterCommitBodyPassContributions",
    ),
    "ClassProduction.after_rollback_body_pass": AssemblyEdgeSpec(
        name="ClassProduction.after_rollback_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="AfterRollbackBodyPassContributions",
    ),
    "ClassProduction.classvars": AssemblyEdgeSpec(
        name="ClassProduction.classvars",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field", collection_name="ClassVarFields", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="ClassVarDefaultContributions",
    ),
    "ClassProduction.commit_order_keys": AssemblyEdgeSpec(
        name="ClassProduction.commit_order_keys",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="method",
                collection_name="CommitOrderKeyProviders",
                collection=None,
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("MethodOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="CommitOrderKeyContributions",
    ),
    "ClassProduction.validation_flags": AssemblyEdgeSpec(
        name="ClassProduction.validation_flags",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="method", collection_name="CommitValidators", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("MethodOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="RequiresValidationContributions",
    ),
    "ClassProduction.validators": AssemblyEdgeSpec(
        name="ClassProduction.validators",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="method", collection_name="CommitValidators", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("MethodOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="ValidateCommitContributions",
    ),
    "ClassProduction.before_commit_hooks": AssemblyEdgeSpec(
        name="ClassProduction.before_commit_hooks",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="method", collection_name="BeforeCommitHooks", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("MethodOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="BeforeCommitHookContributions",
    ),
    "ClassProduction.after_commit_hooks": AssemblyEdgeSpec(
        name="ClassProduction.after_commit_hooks",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="method", collection_name="AfterCommitHooks", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("MethodOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="AfterCommitHookContributions",
    ),
    "ClassProduction.after_rollback_hooks": AssemblyEdgeSpec(
        name="ClassProduction.after_rollback_hooks",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="method", collection_name="AfterRollbackHooks", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("MethodOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="AfterRollbackHookContributions",
    ),
    "ClassProduction.plain_init_params": AssemblyEdgeSpec(
        name="ClassProduction.plain_init_params",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field", collection_name="PlainFields", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="PlainInitParamContributions",
    ),
    "ClassProduction.initvar_params": AssemblyEdgeSpec(
        name="ClassProduction.initvar_params",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field", collection_name="InitVarFields", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="InitVarParamContributions",
    ),
    "ClassProduction.managed_init_params": AssemblyEdgeSpec(
        name="ClassProduction.managed_init_params",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field", collection_name="ManagedFields", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="ManagedInitParamContributions",
    ),
    "ClassProduction.initvar_local_defaults": AssemblyEdgeSpec(
        name="ClassProduction.initvar_local_defaults",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field", collection_name="InitVarFields", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="InitVarLocalDefaultContributions",
    ),
    "ClassProduction.plain_init_assignments": AssemblyEdgeSpec(
        name="ClassProduction.plain_init_assignments",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field", collection_name="PlainFields", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="PlainInitAssignmentContributions",
    ),
    "ClassProduction.managed_current_init_assignments": AssemblyEdgeSpec(
        name="ClassProduction.managed_current_init_assignments",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field", collection_name="ManagedFields", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="ManagedCurrentInitAssignmentContributions",
    ),
    "ClassProduction.managed_working_init_assignments": AssemblyEdgeSpec(
        name="ClassProduction.managed_working_init_assignments",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field", collection_name="ManagedFields", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="ManagedWorkingInitAssignmentContributions",
    ),
    "ClassProduction.managed_staged_init_assignments": AssemblyEdgeSpec(
        name="ClassProduction.managed_staged_init_assignments",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field", collection_name="ManagedFields", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="ManagedStagedInitAssignmentContributions",
    ),
    "ClassProduction.default_factory_evals": AssemblyEdgeSpec(
        name="ClassProduction.default_factory_evals",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="step",
                collection_name="DefaultFactoryEvaluationSteps",
                collection=None,
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("EvalOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="DefaultFactoryEvalContributions",
    ),
    "ClassProduction.default_factory_args": AssemblyEdgeSpec(
        name="ClassProduction.default_factory_args",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="dep",
                collection_name="DefaultFactoryDependencies",
                collection=None,
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("DependencyOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="DefaultFactoryArgContributions",
    ),
    "ClassProduction.plain_properties": AssemblyEdgeSpec(
        name="ClassProduction.plain_properties",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field", collection_name="PlainFields", collection=None
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="PlainPropertyContributions",
    ),
    "ClassProduction.managed_default_properties": AssemblyEdgeSpec(
        name="ClassProduction.managed_default_properties",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field",
                collection_name="IndexedTransactionalFields",
                collection=None,
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="ManagedDefaultFacadePropertyContributions",
    ),
    "ClassProduction.managed_current_properties": AssemblyEdgeSpec(
        name="ClassProduction.managed_current_properties",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field",
                collection_name="IndexedTransactionalFields",
                collection=None,
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="ManagedCurrentFacadePropertyContributions",
    ),
    "ClassProduction.managed_working_properties": AssemblyEdgeSpec(
        name="ClassProduction.managed_working_properties",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field",
                collection_name="IndexedTransactionalFields",
                collection=None,
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="ManagedWorkingFacadePropertyContributions",
    ),
    "ClassProduction.apply_prepared_commit_helpers": AssemblyEdgeSpec(
        name="ClassProduction.apply_prepared_commit_helpers",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="tx_group", collection_name="TxGroups", collection=None
            ),
        ),
        condition=EqConditionSpec(left=ValueRef("TxOwner"), right=ValueRef("ClassId")),
        matcher_name="ApplyPreparedCommitFieldsContributions",
    ),
    "ClassProduction.prepare_commit_helpers": AssemblyEdgeSpec(
        name="ClassProduction.prepare_commit_helpers",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="tx_group", collection_name="TxGroups", collection=None
            ),
        ),
        condition=EqConditionSpec(left=ValueRef("TxOwner"), right=ValueRef("ClassId")),
        matcher_name="PrepareCommitFieldsContributions",
    ),
    "ClassProduction.rollback_helpers": AssemblyEdgeSpec(
        name="ClassProduction.rollback_helpers",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="tx_group", collection_name="TxGroups", collection=None
            ),
        ),
        condition=EqConditionSpec(left=ValueRef("TxOwner"), right=ValueRef("ClassId")),
        matcher_name="RollbackFieldsContributions",
    ),
    "ClassProduction.apply_prepared_commit_helper_body_pass": AssemblyEdgeSpec(
        name="ClassProduction.apply_prepared_commit_helper_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="tx_group", collection_name="TxGroups", collection=None
            ),
        ),
        condition=EqConditionSpec(left=ValueRef("TxOwner"), right=ValueRef("ClassId")),
        matcher_name="ApplyPreparedCommitFieldsBodyPassContributions",
    ),
    "ClassProduction.prepare_commit_helper_body_pass": AssemblyEdgeSpec(
        name="ClassProduction.prepare_commit_helper_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="tx_group", collection_name="TxGroups", collection=None
            ),
        ),
        condition=EqConditionSpec(left=ValueRef("TxOwner"), right=ValueRef("ClassId")),
        matcher_name="PrepareCommitFieldsBodyPassContributions",
    ),
    "ClassProduction.rollback_helper_body_pass": AssemblyEdgeSpec(
        name="ClassProduction.rollback_helper_body_pass",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="tx_group", collection_name="TxGroups", collection=None
            ),
        ),
        condition=EqConditionSpec(left=ValueRef("TxOwner"), right=ValueRef("ClassId")),
        matcher_name="RollbackFieldsBodyPassContributions",
    ),
    "ClassProduction.prepare_commit_dispatch": AssemblyEdgeSpec(
        name="ClassProduction.prepare_commit_dispatch",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="tx_group", collection_name="TxGroups", collection=None
            ),
        ),
        condition=EqConditionSpec(left=ValueRef("TxOwner"), right=ValueRef("ClassId")),
        matcher_name="PrepareCommitDispatchContributions",
    ),
    "ClassProduction.apply_prepared_commit_dispatch": AssemblyEdgeSpec(
        name="ClassProduction.apply_prepared_commit_dispatch",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="tx_group", collection_name="TxGroups", collection=None
            ),
        ),
        condition=EqConditionSpec(left=ValueRef("TxOwner"), right=ValueRef("ClassId")),
        matcher_name="ApplyPreparedCommitDispatchContributions",
    ),
    "ClassProduction.rollback_dispatch": AssemblyEdgeSpec(
        name="ClassProduction.rollback_dispatch",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="tx_group", collection_name="TxGroups", collection=None
            ),
        ),
        condition=EqConditionSpec(left=ValueRef("TxOwner"), right=ValueRef("ClassId")),
        matcher_name="RollbackDispatchContributions",
    ),
    "ClassProduction.managed_prepare_commit": AssemblyEdgeSpec(
        name="ClassProduction.managed_prepare_commit",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field",
                collection_name="IndexedTransactionalFields",
                collection=None,
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="ManagedPrepareCommitContributions",
    ),
    "ClassProduction.managed_apply_prepared_commit": AssemblyEdgeSpec(
        name="ClassProduction.managed_apply_prepared_commit",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field",
                collection_name="IndexedTransactionalFields",
                collection=None,
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="ManagedApplyPreparedCommitContributions",
    ),
    "ClassProduction.managed_rollback": AssemblyEdgeSpec(
        name="ClassProduction.managed_rollback",
        context_inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(
                name="field",
                collection_name="IndexedTransactionalFields",
                collection=None,
            ),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="ManagedRollbackContributions",
    ),
}
ASSEMBLY_PRODUCTIONS = {
    "CoreModuleProduction": ComposableProductionSpec(
        name="CoreModuleProduction",
        inputs=(),
        root=RootSpec(build_name="Root", resource_name="ModuleRoot", bindings=()),
        applies=(
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreModuleProduction.lifecycle_definition_params",
                    context_inputs=(),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    condition=None,
                    matcher_name="BuilderParamContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreModuleProduction.annotations_params",
                    context_inputs=(),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    condition=None,
                    matcher_name="AnnotationsBuilderParamContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreModuleProduction.tx_groups_params",
                    context_inputs=(),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    condition=None,
                    matcher_name="TxGroupsBuilderParamContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreModuleProduction.field_default_params",
                    context_inputs=(),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="Fields", collection=None
                        ),
                    ),
                    condition=None,
                    matcher_name="FieldDefaultBuilderParamContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreModuleProduction.classes",
                    context_inputs=(),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    condition=None,
                    matcher_name="CoreClassDefinitionContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreModuleProduction.return_class",
                    context_inputs=(),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    condition=None,
                    matcher_name="ReturnClassContributions",
                )
            ),
        ),
    ),
    "CoreClassProduction": ComposableProductionSpec(
        name="CoreClassProduction",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        root=RootSpec(
            build_name="ClassDef",
            resource_name="ClassBundle",
            bindings=(
                BindingSpec(
                    kind="ident",
                    name="state_class_decl_name",
                    value=ValueRef("StateClassName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="state_class_ref",
                    value=ValueRef("StateClassName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="default_facade_class_decl_name",
                    value=ValueRef("ClassName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="default_facade_class_ref",
                    value=ValueRef("ClassName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="facade_base_decl_name",
                    value=ValueRef("FacadeBaseClassName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="facade_base_default_base_name",
                    value=ValueRef("FacadeBaseClassName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="facade_base_current_base_name",
                    value=ValueRef("FacadeBaseClassName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="facade_base_working_base_name",
                    value=ValueRef("FacadeBaseClassName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="current_facade_class_decl_name",
                    value=ValueRef("CurrentFacadeClassName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="current_facade_class_ref",
                    value=ValueRef("CurrentFacadeClassName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="working_facade_class_decl_name",
                    value=ValueRef("WorkingFacadeClassName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="working_facade_class_ref",
                    value=ValueRef("WorkingFacadeClassName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="tx_groups_for_index_name",
                    value=ValueRef("TxGroupsParamName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="tx_groups_for_map_name",
                    value=ValueRef("TxGroupsParamName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="tx_groups_for_class_index_name",
                    value=ValueRef("TxGroupsParamName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="tx_groups_for_class_map_name",
                    value=ValueRef("TxGroupsParamName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="tx_groups_for_manager_name",
                    value=ValueRef("TxGroupsParamName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="tx_groups_for_slots_name",
                    value=ValueRef("TxGroupsParamName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="lifecycle_definition_name",
                    value=ValueRef("LifecycleDefinitionParamName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="annotations_name",
                    value=ValueRef("AnnotationsParamName"),
                ),
                BindingSpec(
                    kind="external",
                    name="lifecycle_field_names",
                    value=ValueRef("LifecycleFieldNames"),
                ),
            ),
        ),
        applies=(
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.state_slots",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="PlainFields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="PlainStateSlotContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.transaction_manager_param",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="TransactionManagerInitParamContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.facade_base_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="FacadeBaseBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.facade_properties_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="FacadePropertiesPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.default_facade_properties_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="DefaultFacadePropertiesPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.current_facade_properties_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="CurrentFacadePropertiesPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.working_facade_properties_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="WorkingFacadePropertiesPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.state_init_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="StateInitBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.commit_transaction_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="CommitTransactionBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.commit_transaction_dispatch_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="CommitTransactionDispatchBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.prepare_commit_transaction_dispatch_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="PrepareCommitTransactionDispatchBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.rollback_transaction_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="RollbackTransactionBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.rollback_transaction_dispatch_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="RollbackTransactionDispatchBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.commit_order_key_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="CommitOrderKeyBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.requires_validation_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="RequiresValidationBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.validate_commit_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="ValidateCommitBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.before_commit_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="BeforeCommitBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.after_commit_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="AfterCommitBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.after_rollback_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="AfterRollbackBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.classvars",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field",
                            collection_name="ClassVarFields",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="ClassVarDefaultContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.commit_order_keys",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="method",
                            collection_name="CommitOrderKeyProviders",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("MethodOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="CommitOrderKeyContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.validation_flags",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="method",
                            collection_name="CommitValidators",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("MethodOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="RequiresValidationContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.validators",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="method",
                            collection_name="CommitValidators",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("MethodOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="ValidateCommitContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.before_commit_hooks",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="method",
                            collection_name="BeforeCommitHooks",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("MethodOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="BeforeCommitHookContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.after_commit_hooks",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="method",
                            collection_name="AfterCommitHooks",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("MethodOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="AfterCommitHookContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.after_rollback_hooks",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="method",
                            collection_name="AfterRollbackHooks",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("MethodOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="AfterRollbackHookContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.plain_init_params",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="PlainFields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="PlainInitParamContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.initvar_params",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field",
                            collection_name="InitVarFields",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="InitVarParamContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.initvar_local_defaults",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field",
                            collection_name="InitVarFields",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="InitVarLocalDefaultContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.plain_init_assignments",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="PlainFields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="PlainInitAssignmentContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="CoreClassProduction.plain_properties",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="PlainFields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="PlainPropertyContributions",
                )
            ),
        ),
    ),
    "ModuleProduction": ComposableProductionSpec(
        name="ModuleProduction",
        inputs=(),
        root=RootSpec(build_name="Root", resource_name="ModuleRoot", bindings=()),
        applies=(
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ModuleProduction.lifecycle_definition_params",
                    context_inputs=(),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    condition=None,
                    matcher_name="BuilderParamContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ModuleProduction.annotations_params",
                    context_inputs=(),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    condition=None,
                    matcher_name="AnnotationsBuilderParamContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ModuleProduction.tx_groups_params",
                    context_inputs=(),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    condition=None,
                    matcher_name="TxGroupsBuilderParamContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ModuleProduction.field_default_params",
                    context_inputs=(),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="Fields", collection=None
                        ),
                    ),
                    condition=None,
                    matcher_name="FieldDefaultBuilderParamContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ModuleProduction.managed_freeze_params",
                    context_inputs=(),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field",
                            collection_name="ManagedFields",
                            collection=None,
                        ),
                    ),
                    condition=None,
                    matcher_name="ManagedFreezeBuilderParamContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ModuleProduction.managed_thaw_params",
                    context_inputs=(),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field",
                            collection_name="ManagedFields",
                            collection=None,
                        ),
                    ),
                    condition=None,
                    matcher_name="ManagedThawBuilderParamContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ModuleProduction.classes",
                    context_inputs=(),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    condition=None,
                    matcher_name="ClassDefinitionContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ModuleProduction.return_class",
                    context_inputs=(),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    condition=None,
                    matcher_name="ReturnClassContributions",
                )
            ),
        ),
    ),
    "ClassProduction": ComposableProductionSpec(
        name="ClassProduction",
        inputs=(
            AssemblyInputSpec(
                name="lifecycle_class", collection_name="Classes", collection=None
            ),
        ),
        root=RootSpec(
            build_name="ClassDef",
            resource_name="ClassBundle",
            bindings=(
                BindingSpec(
                    kind="ident",
                    name="state_class_decl_name",
                    value=ValueRef("StateClassName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="state_class_ref",
                    value=ValueRef("StateClassName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="default_facade_class_decl_name",
                    value=ValueRef("ClassName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="default_facade_class_ref",
                    value=ValueRef("ClassName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="facade_base_decl_name",
                    value=ValueRef("FacadeBaseClassName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="facade_base_default_base_name",
                    value=ValueRef("FacadeBaseClassName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="facade_base_current_base_name",
                    value=ValueRef("FacadeBaseClassName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="facade_base_working_base_name",
                    value=ValueRef("FacadeBaseClassName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="current_facade_class_decl_name",
                    value=ValueRef("CurrentFacadeClassName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="current_facade_class_ref",
                    value=ValueRef("CurrentFacadeClassName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="working_facade_class_decl_name",
                    value=ValueRef("WorkingFacadeClassName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="working_facade_class_ref",
                    value=ValueRef("WorkingFacadeClassName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="tx_groups_for_index_name",
                    value=ValueRef("TxGroupsParamName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="tx_groups_for_map_name",
                    value=ValueRef("TxGroupsParamName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="tx_groups_for_class_index_name",
                    value=ValueRef("TxGroupsParamName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="tx_groups_for_class_map_name",
                    value=ValueRef("TxGroupsParamName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="tx_groups_for_manager_name",
                    value=ValueRef("TxGroupsParamName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="tx_groups_for_slots_name",
                    value=ValueRef("TxGroupsParamName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="lifecycle_definition_name",
                    value=ValueRef("LifecycleDefinitionParamName"),
                ),
                BindingSpec(
                    kind="ident",
                    name="annotations_name",
                    value=ValueRef("AnnotationsParamName"),
                ),
                BindingSpec(
                    kind="external",
                    name="lifecycle_field_names",
                    value=ValueRef("LifecycleFieldNames"),
                ),
            ),
        ),
        applies=(
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.state_slots",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="PlainFields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="PlainStateSlotContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.managed_current_state_slots",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field",
                            collection_name="ManagedFields",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="ManagedCurrentStateSlotContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.managed_working_state_slots",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field",
                            collection_name="ManagedFields",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="ManagedWorkingStateSlotContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.managed_staged_state_slots",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field",
                            collection_name="ManagedFields",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="ManagedStagedStateSlotContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.transaction_manager_param",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="TransactionManagerInitParamContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.facade_base_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="FacadeBaseBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.facade_properties_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="FacadePropertiesPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.default_facade_properties_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="DefaultFacadePropertiesPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.current_facade_properties_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="CurrentFacadePropertiesPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.working_facade_properties_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="WorkingFacadePropertiesPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.state_init_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="StateInitBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.commit_transaction_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="CommitTransactionBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.commit_transaction_dispatch_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="CommitTransactionDispatchBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.prepare_commit_transaction_dispatch_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="PrepareCommitTransactionDispatchBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.rollback_transaction_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="RollbackTransactionBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.rollback_transaction_dispatch_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="RollbackTransactionDispatchBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.commit_order_key_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="CommitOrderKeyBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.requires_validation_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="RequiresValidationBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.validate_commit_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="ValidateCommitBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.before_commit_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="BeforeCommitBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.after_commit_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="AfterCommitBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.after_rollback_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="AfterRollbackBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.classvars",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field",
                            collection_name="ClassVarFields",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="ClassVarDefaultContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.commit_order_keys",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="method",
                            collection_name="CommitOrderKeyProviders",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("MethodOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="CommitOrderKeyContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.validation_flags",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="method",
                            collection_name="CommitValidators",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("MethodOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="RequiresValidationContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.validators",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="method",
                            collection_name="CommitValidators",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("MethodOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="ValidateCommitContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.before_commit_hooks",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="method",
                            collection_name="BeforeCommitHooks",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("MethodOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="BeforeCommitHookContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.after_commit_hooks",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="method",
                            collection_name="AfterCommitHooks",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("MethodOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="AfterCommitHookContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.after_rollback_hooks",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="method",
                            collection_name="AfterRollbackHooks",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("MethodOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="AfterRollbackHookContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.plain_init_params",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="PlainFields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="PlainInitParamContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.initvar_params",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field",
                            collection_name="InitVarFields",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="InitVarParamContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.managed_init_params",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field",
                            collection_name="ManagedFields",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="ManagedInitParamContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.initvar_local_defaults",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field",
                            collection_name="InitVarFields",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="InitVarLocalDefaultContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.plain_init_assignments",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="PlainFields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="PlainInitAssignmentContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.managed_current_init_assignments",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field",
                            collection_name="ManagedFields",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="ManagedCurrentInitAssignmentContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.managed_working_init_assignments",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field",
                            collection_name="ManagedFields",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="ManagedWorkingInitAssignmentContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.managed_staged_init_assignments",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field",
                            collection_name="ManagedFields",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="ManagedStagedInitAssignmentContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.default_factory_evals",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="step",
                            collection_name="DefaultFactoryEvaluationSteps",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("EvalOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="DefaultFactoryEvalContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.default_factory_args",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="dep",
                            collection_name="DefaultFactoryDependencies",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("DependencyOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="DefaultFactoryArgContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.plain_properties",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="PlainFields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="PlainPropertyContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.managed_default_properties",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field",
                            collection_name="IndexedTransactionalFields",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="ManagedDefaultFacadePropertyContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.managed_current_properties",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field",
                            collection_name="IndexedTransactionalFields",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="ManagedCurrentFacadePropertyContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.managed_working_properties",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field",
                            collection_name="IndexedTransactionalFields",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="ManagedWorkingFacadePropertyContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.apply_prepared_commit_helpers",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="tx_group", collection_name="TxGroups", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("TxOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="ApplyPreparedCommitFieldsContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.prepare_commit_helpers",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="tx_group", collection_name="TxGroups", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("TxOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="PrepareCommitFieldsContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.rollback_helpers",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="tx_group", collection_name="TxGroups", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("TxOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="RollbackFieldsContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.apply_prepared_commit_helper_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="tx_group", collection_name="TxGroups", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("TxOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="ApplyPreparedCommitFieldsBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.prepare_commit_helper_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="tx_group", collection_name="TxGroups", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("TxOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="PrepareCommitFieldsBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.rollback_helper_body_pass",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="tx_group", collection_name="TxGroups", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("TxOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="RollbackFieldsBodyPassContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.prepare_commit_dispatch",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="tx_group", collection_name="TxGroups", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("TxOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="PrepareCommitDispatchContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.apply_prepared_commit_dispatch",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="tx_group", collection_name="TxGroups", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("TxOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="ApplyPreparedCommitDispatchContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.rollback_dispatch",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="tx_group", collection_name="TxGroups", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("TxOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="RollbackDispatchContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.managed_prepare_commit",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field",
                            collection_name="IndexedTransactionalFields",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="ManagedPrepareCommitContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.managed_apply_prepared_commit",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field",
                            collection_name="IndexedTransactionalFields",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="ManagedApplyPreparedCommitContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.managed_rollback",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="lifecycle_class",
                            collection_name="Classes",
                            collection=None,
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field",
                            collection_name="IndexedTransactionalFields",
                            collection=None,
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="ManagedRollbackContributions",
                )
            ),
        ),
    ),
}
ASSEMBLY_ASSEMBLIES = {
    "LifecycleCoreModule": AssemblySpec(
        name="LifecycleCoreModule", production_name="CoreModuleProduction"
    ),
    "LifecycleModule": AssemblySpec(
        name="LifecycleModule", production_name="ModuleProduction"
    ),
}

ASSEMBLY_CONCEPT = _YidlSimpleNamespace(
    properties=ASSEMBLY_PROPERTIES,
    resources=ASSEMBLY_RESOURCES,
    contributions=ASSEMBLY_CONTRIBUTIONS,
    contribution_matchers=ASSEMBLY_MATCHERS,
    assembly_edges=ASSEMBLY_EDGES,
    composable_productions=ASSEMBLY_PRODUCTIONS,
    assemblies=ASSEMBLY_ASSEMBLIES,
)

_YIDL_BASE_BUILD_CONTAINER = globals().get("build_container")


def build_container(builder):
    if _YIDL_BASE_BUILD_CONTAINER is not None:
        return _YIDL_BASE_BUILD_CONTAINER(builder)
    return builder.freeze()


def build_assembly(entrypoint, container, *, unroll="auto"):
    return run_assembly(ASSEMBLY_CONCEPT, entrypoint, container, unroll=unroll)


def build_LifecycleCoreModule(container, *, unroll="auto"):
    return build_assembly("LifecycleCoreModule", container, unroll=unroll)


def build_LifecycleModule(container, *, unroll="auto"):
    return build_assembly("LifecycleModule", container, unroll=unroll)
