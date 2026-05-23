from yidl.generation.data_def_sys import AddIfAbsent, AssemblyDiagnosticError, DDSContainerBuilder, DDSOperationContext, NOT_PROVIDED, REQUIRED, RejectDuplicate, ReplaceExisting, RuntimeCollection, RuntimeComputedCollection, RuntimeContainerSpec, RuntimePort, RuntimePortIndex, RuntimeProperty, RuntimeRecord, RuntimeUnion
_ClassIdProperty = RuntimeProperty('ClassId', str, default=REQUIRED, storage_name='class_id')
_ClassNameProperty = RuntimeProperty('ClassName', str, default=REQUIRED, storage_name='class_name')
_ClassOrderProperty = RuntimeProperty('ClassOrder', int, default=0, storage_name='class_order')
_ModuleNameProperty = RuntimeProperty('ModuleName', str, default='__main__', storage_name='module_name')
_StateClassNameProperty = RuntimeProperty('StateClassName', str, default=REQUIRED, storage_name='state_class_name')
_FacadeBaseClassNameProperty = RuntimeProperty('FacadeBaseClassName', str, default=REQUIRED, storage_name='facade_base_class_name')
_CurrentFacadeClassNameProperty = RuntimeProperty('CurrentFacadeClassName', str, default=REQUIRED, storage_name='current_facade_class_name')
_WorkingFacadeClassNameProperty = RuntimeProperty('WorkingFacadeClassName', str, default=REQUIRED, storage_name='working_facade_class_name')
_LifecycleDefinitionParamNameProperty = RuntimeProperty('LifecycleDefinitionParamName', str, default='', storage_name='lifecycle_definition_param_name')
_AnnotationsParamNameProperty = RuntimeProperty('AnnotationsParamName', str, default='', storage_name='annotations_param_name')
_TxKeysParamNameProperty = RuntimeProperty('TxKeysParamName', str, default='', storage_name='tx_keys_param_name')
_LifecycleFieldNamesProperty = RuntimeProperty('LifecycleFieldNames', object, default=(), storage_name='lifecycle_field_names')
_FieldIdProperty = RuntimeProperty('FieldId', str, default=REQUIRED, storage_name='field_id')
_FieldOwnerProperty = RuntimeProperty('FieldOwner', str, default=REQUIRED, storage_name='field_owner')
_FieldNameProperty = RuntimeProperty('FieldName', str, default=REQUIRED, storage_name='field_name')
_FieldOrderProperty = RuntimeProperty('FieldOrder', int, default=REQUIRED, storage_name='field_order')
_FieldKindProperty = RuntimeProperty('FieldKind', str, default='field', storage_name='field_kind')
_BindingShapeProperty = RuntimeProperty('BindingShape', str, default='scalar', storage_name='binding_shape')
_AnnotationProperty = RuntimeProperty('Annotation', object, default=object, storage_name='annotation')
_InitProperty = RuntimeProperty('Init', bool, default=True, storage_name='init')
_HasDefaultProperty = RuntimeProperty('HasDefault', bool, default=False, storage_name='has_default')
_DefaultValueProperty = RuntimeProperty('DefaultValue', object, default=None, storage_name='default_value')
_DefaultValueParamNameProperty = RuntimeProperty('DefaultValueParamName', str, default='', storage_name='default_value_param_name')
_HasDefaultFactoryProperty = RuntimeProperty('HasDefaultFactory', bool, default=False, storage_name='has_default_factory')
_DefaultFactoryProperty = RuntimeProperty('DefaultFactory', object, default=None, storage_name='default_factory')
_DefaultFactoryParamNameProperty = RuntimeProperty('DefaultFactoryParamName', str, default='', storage_name='default_factory_param_name')
_DefaultFactoryParamNamesProperty = RuntimeProperty('DefaultFactoryParamNames', object, default=(), storage_name='default_factory_param_names')
_HasWorkingDefaultFactoryProperty = RuntimeProperty('HasWorkingDefaultFactory', bool, default=False, storage_name='has_working_default_factory')
_WorkingDefaultFactoryProperty = RuntimeProperty('WorkingDefaultFactory', object, default=None, storage_name='working_default_factory')
_WorkingDefaultFactoryParamNameProperty = RuntimeProperty('WorkingDefaultFactoryParamName', str, default='', storage_name='working_default_factory_param_name')
_WorkingDefaultFactoryParamNamesProperty = RuntimeProperty('WorkingDefaultFactoryParamNames', object, default=(), storage_name='working_default_factory_param_names')
_TxKeyKeyProperty = RuntimeProperty('TxKeyKey', object, default=None, storage_name='tx_key_key')
_ValueSlotNameProperty = RuntimeProperty('ValueSlotName', str, default='', storage_name='value_slot_name')
_CurrentSlotNameProperty = RuntimeProperty('CurrentSlotName', str, default='', storage_name='current_slot_name')
_WorkingSlotNameProperty = RuntimeProperty('WorkingSlotName', str, default='', storage_name='working_slot_name')
_StagedSlotNameProperty = RuntimeProperty('StagedSlotName', str, default='', storage_name='staged_slot_name')
_HasFreezeProperty = RuntimeProperty('HasFreeze', bool, default=False, storage_name='has_freeze')
_FreezeProperty = RuntimeProperty('Freeze', object, default=None, storage_name='freeze')
_FreezeParamNameProperty = RuntimeProperty('FreezeParamName', str, default='', storage_name='freeze_param_name')
_HasThawProperty = RuntimeProperty('HasThaw', bool, default=False, storage_name='has_thaw')
_ThawProperty = RuntimeProperty('Thaw', object, default=None, storage_name='thaw')
_ThawParamNameProperty = RuntimeProperty('ThawParamName', str, default='', storage_name='thaw_param_name')
_HasOptionalNoneProperty = RuntimeProperty('HasOptionalNone', bool, default=False, storage_name='has_optional_none')
_MethodIdProperty = RuntimeProperty('MethodId', str, default=REQUIRED, storage_name='method_id')
_MethodOwnerProperty = RuntimeProperty('MethodOwner', str, default=REQUIRED, storage_name='method_owner')
_MethodNameProperty = RuntimeProperty('MethodName', str, default=REQUIRED, storage_name='method_name')
_MethodKindProperty = RuntimeProperty('MethodKind', str, default=REQUIRED, storage_name='method_kind')
_DeclarationOrderProperty = RuntimeProperty('DeclarationOrder', int, default=0, storage_name='declaration_order')
_TxIndexProperty = RuntimeProperty('TxIndex', int, default=0, storage_name='tx_index')
_FacadeIdProperty = RuntimeProperty('FacadeId', str, default=REQUIRED, storage_name='facade_id')
_FacadeOwnerProperty = RuntimeProperty('FacadeOwner', str, default=REQUIRED, storage_name='facade_owner')
_FacadeKindProperty = RuntimeProperty('FacadeKind', str, default=REQUIRED, storage_name='facade_kind')
_FacadeModeProperty = RuntimeProperty('FacadeMode', str, default=REQUIRED, storage_name='facade_mode')
_FacadeClassNameProperty = RuntimeProperty('FacadeClassName', str, default=REQUIRED, storage_name='facade_class_name')
_FacadeOrderProperty = RuntimeProperty('FacadeOrder', int, default=0, storage_name='facade_order')
_OwnerFacadeIdProperty = RuntimeProperty('OwnerFacadeId', str, default=REQUIRED, storage_name='owner_facade_id')
_TargetFacadeIdProperty = RuntimeProperty('TargetFacadeId', str, default=REQUIRED, storage_name='target_facade_id')
_ExposureOrderProperty = RuntimeProperty('ExposureOrder', int, default=0, storage_name='exposure_order')
_InitParameterIdProperty = RuntimeProperty('InitParameterId', str, default=REQUIRED, storage_name='init_parameter_id')
_InitParameterOwnerProperty = RuntimeProperty('InitParameterOwner', str, default=REQUIRED, storage_name='init_parameter_owner')
_InitParameterNameProperty = RuntimeProperty('InitParameterName', str, default=REQUIRED, storage_name='init_parameter_name')
_InitParameterOrderProperty = RuntimeProperty('InitParameterOrder', int, default=0, storage_name='init_parameter_order')
_InitParameterKindProperty = RuntimeProperty('InitParameterKind', str, default='field', storage_name='init_parameter_kind')
_InitAssignmentIdProperty = RuntimeProperty('InitAssignmentId', str, default=REQUIRED, storage_name='init_assignment_id')
_InitAssignmentOwnerProperty = RuntimeProperty('InitAssignmentOwner', str, default=REQUIRED, storage_name='init_assignment_owner')
_InitAssignmentFieldIdProperty = RuntimeProperty('InitAssignmentFieldId', str, default=REQUIRED, storage_name='init_assignment_field_id')
_InitAssignmentFieldNameProperty = RuntimeProperty('InitAssignmentFieldName', str, default=REQUIRED, storage_name='init_assignment_field_name')
_InitAssignmentOrderProperty = RuntimeProperty('InitAssignmentOrder', int, default=0, storage_name='init_assignment_order')
_InitAssignmentKindProperty = RuntimeProperty('InitAssignmentKind', str, default='plain', storage_name='init_assignment_kind')
_ClassVarAssignmentIdProperty = RuntimeProperty('ClassVarAssignmentId', str, default=REQUIRED, storage_name='class_var_assignment_id')
_ClassVarAssignmentOwnerProperty = RuntimeProperty('ClassVarAssignmentOwner', str, default=REQUIRED, storage_name='class_var_assignment_owner')
_ClassVarAssignmentNameProperty = RuntimeProperty('ClassVarAssignmentName', str, default=REQUIRED, storage_name='class_var_assignment_name')
_ClassVarAssignmentOrderProperty = RuntimeProperty('ClassVarAssignmentOrder', int, default=0, storage_name='class_var_assignment_order')
_TxKeyOrderProperty = RuntimeProperty('TxKeyOrder', int, default=0, storage_name='tx_key_order')
_TxOwnerProperty = RuntimeProperty('TxOwner', str, default='', storage_name='tx_owner')
_CommitOrderKeyFunctionNameProperty = RuntimeProperty('CommitOrderKeyFunctionName', str, default='', storage_name='commit_order_key_function_name')
_RequiresValidationFunctionNameProperty = RuntimeProperty('RequiresValidationFunctionName', str, default='', storage_name='requires_validation_function_name')
_ValidateCommitFunctionNameProperty = RuntimeProperty('ValidateCommitFunctionName', str, default='', storage_name='validate_commit_function_name')
_BeforeCommitFunctionNameProperty = RuntimeProperty('BeforeCommitFunctionName', str, default='', storage_name='before_commit_function_name')
_AfterCommitFunctionNameProperty = RuntimeProperty('AfterCommitFunctionName', str, default='', storage_name='after_commit_function_name')
_AfterRollbackFunctionNameProperty = RuntimeProperty('AfterRollbackFunctionName', str, default='', storage_name='after_rollback_function_name')
_PrepareCommitFieldsFunctionNameProperty = RuntimeProperty('PrepareCommitFieldsFunctionName', str, default='', storage_name='prepare_commit_fields_function_name')
_ApplyPreparedCommitFieldsFunctionNameProperty = RuntimeProperty('ApplyPreparedCommitFieldsFunctionName', str, default='', storage_name='apply_prepared_commit_fields_function_name')
_RollbackFieldsFunctionNameProperty = RuntimeProperty('RollbackFieldsFunctionName', str, default='', storage_name='rollback_fields_function_name')
_DependencyOwnerProperty = RuntimeProperty('DependencyOwner', str, default=REQUIRED, storage_name='dependency_owner')
_ConsumerFieldIdProperty = RuntimeProperty('ConsumerFieldId', str, default=REQUIRED, storage_name='consumer_field_id')
_ConsumerFieldNameProperty = RuntimeProperty('ConsumerFieldName', str, default='', storage_name='consumer_field_name')
_ConsumerFieldKindProperty = RuntimeProperty('ConsumerFieldKind', str, default='', storage_name='consumer_field_kind')
_ConsumerFieldOrderProperty = RuntimeProperty('ConsumerFieldOrder', int, default=0, storage_name='consumer_field_order')
_ProviderNameProperty = RuntimeProperty('ProviderName', str, default=REQUIRED, storage_name='provider_name')
_ProviderFieldIdProperty = RuntimeProperty('ProviderFieldId', str, default='', storage_name='provider_field_id')
_ProviderFieldKindProperty = RuntimeProperty('ProviderFieldKind', str, default='', storage_name='provider_field_kind')
_ProviderInitProperty = RuntimeProperty('ProviderInit', bool, default=True, storage_name='provider_init')
_ProviderHasDefaultProperty = RuntimeProperty('ProviderHasDefault', bool, default=False, storage_name='provider_has_default')
_ProviderHasDefaultFactoryProperty = RuntimeProperty('ProviderHasDefaultFactory', bool, default=False, storage_name='provider_has_default_factory')
_ParamNameProperty = RuntimeProperty('ParamName', str, default=REQUIRED, storage_name='param_name')
_ParamOrderProperty = RuntimeProperty('ParamOrder', int, default=0, storage_name='param_order')
_ConsumerEvalOrderProperty = RuntimeProperty('ConsumerEvalOrder', int, default=0, storage_name='consumer_eval_order')
_EvalStepIdProperty = RuntimeProperty('EvalStepId', str, default=REQUIRED, storage_name='eval_step_id')
_EvalOwnerProperty = RuntimeProperty('EvalOwner', str, default=REQUIRED, storage_name='eval_owner')
_EvalFieldIdProperty = RuntimeProperty('EvalFieldId', str, default=REQUIRED, storage_name='eval_field_id')
_EvalFieldNameProperty = RuntimeProperty('EvalFieldName', str, default=REQUIRED, storage_name='eval_field_name')
_EvalFieldKindProperty = RuntimeProperty('EvalFieldKind', str, default='', storage_name='eval_field_kind')
_EvalBindingShapeProperty = RuntimeProperty('EvalBindingShape', str, default='scalar', storage_name='eval_binding_shape')
_EvalInitProperty = RuntimeProperty('EvalInit', bool, default=True, storage_name='eval_init')
_EvalStateSlotNameProperty = RuntimeProperty('EvalStateSlotName', str, default='', storage_name='eval_state_slot_name')
_EvalDefaultFactoryParamNameProperty = RuntimeProperty('EvalDefaultFactoryParamName', str, default='', storage_name='eval_default_factory_param_name')
_EvalOrderProperty = RuntimeProperty('EvalOrder', int, default=0, storage_name='eval_order')
_EvalStatementOrderProperty = RuntimeProperty('EvalStatementOrder', int, default=0, storage_name='eval_statement_order')
_DiagnosticIdProperty = RuntimeProperty('DiagnosticId', str, default=REQUIRED, storage_name='diagnostic_id')
_DiagnosticOwnerProperty = RuntimeProperty('DiagnosticOwner', str, default=REQUIRED, storage_name='diagnostic_owner')
_DiagnosticFieldIdProperty = RuntimeProperty('DiagnosticFieldId', str, default='', storage_name='diagnostic_field_id')
_DiagnosticMessageProperty = RuntimeProperty('DiagnosticMessage', str, default=REQUIRED, storage_name='diagnostic_message')
_RetainedSlotNameProperty = RuntimeProperty('RetainedSlotName', str, default='', storage_name='retained_slot_name')
_RetainOrderProperty = RuntimeProperty('RetainOrder', int, default=0, storage_name='retain_order')
_WorkingFactoryArgIdProperty = RuntimeProperty('WorkingFactoryArgId', str, default=REQUIRED, storage_name='working_factory_arg_id')
_WorkingFactoryArgOwnerProperty = RuntimeProperty('WorkingFactoryArgOwner', str, default=REQUIRED, storage_name='working_factory_arg_owner')
_WorkingFactoryConsumerFieldIdProperty = RuntimeProperty('WorkingFactoryConsumerFieldId', str, default=REQUIRED, storage_name='working_factory_consumer_field_id')
_WorkingFactoryConsumerFieldOrderProperty = RuntimeProperty('WorkingFactoryConsumerFieldOrder', int, default=0, storage_name='working_factory_consumer_field_order')
_WorkingFactoryArgKindProperty = RuntimeProperty('WorkingFactoryArgKind', str, default='', storage_name='working_factory_arg_kind')
_LifecycleClassSpec = RuntimeRecord('LifecycleClass', (_ClassIdProperty, _ClassNameProperty, _ClassOrderProperty, _ModuleNameProperty, _StateClassNameProperty, _FacadeBaseClassNameProperty, _CurrentFacadeClassNameProperty, _WorkingFacadeClassNameProperty, _LifecycleDefinitionParamNameProperty, _AnnotationsParamNameProperty, _TxKeysParamNameProperty, _LifecycleFieldNamesProperty))
_TransactionMethodSpec = RuntimeRecord('TransactionMethod', (_MethodIdProperty, _MethodOwnerProperty, _MethodNameProperty, _MethodKindProperty, _TxKeyKeyProperty, _TxIndexProperty, _DeclarationOrderProperty))
_FacadeClassSpec = RuntimeRecord('FacadeClass', (_FacadeOwnerProperty, _FacadeIdProperty, _FacadeKindProperty, _FacadeModeProperty, _FacadeClassNameProperty, _FacadeOrderProperty))
_FacadeExposureSpec = RuntimeRecord('FacadeExposure', (_FacadeOwnerProperty, _OwnerFacadeIdProperty, _FieldNameProperty, _TargetFacadeIdProperty, _ExposureOrderProperty))
_InitParameterSpec = RuntimeRecord('InitParameter', (_InitParameterIdProperty, _InitParameterOwnerProperty, _InitParameterNameProperty, _InitParameterOrderProperty, _InitParameterKindProperty))
_InitAssignmentSpec = RuntimeRecord('InitAssignment', (_InitAssignmentIdProperty, _InitAssignmentOwnerProperty, _InitAssignmentFieldIdProperty, _InitAssignmentFieldNameProperty, _InitAssignmentOrderProperty, _InitAssignmentKindProperty))
_ClassVarAssignmentSpec = RuntimeRecord('ClassVarAssignment', (_ClassVarAssignmentIdProperty, _ClassVarAssignmentOwnerProperty, _ClassVarAssignmentNameProperty, _ClassVarAssignmentOrderProperty))
_PlainFieldSpec = RuntimeRecord('PlainField', (_FieldIdProperty, _FieldOwnerProperty, _FieldNameProperty, _FieldOrderProperty, _FieldKindProperty, _BindingShapeProperty, _AnnotationProperty, _InitProperty, _HasDefaultProperty, _DefaultValueProperty, _DefaultValueParamNameProperty, _HasDefaultFactoryProperty, _DefaultFactoryProperty, _DefaultFactoryParamNameProperty, _DefaultFactoryParamNamesProperty, _HasWorkingDefaultFactoryProperty, _WorkingDefaultFactoryProperty, _WorkingDefaultFactoryParamNameProperty, _WorkingDefaultFactoryParamNamesProperty, _TxKeyKeyProperty, _ValueSlotNameProperty, _CurrentSlotNameProperty, _WorkingSlotNameProperty, _StagedSlotNameProperty, _HasFreezeProperty, _FreezeProperty, _FreezeParamNameProperty, _HasThawProperty, _ThawProperty, _ThawParamNameProperty, _HasOptionalNoneProperty))
_InitVarFieldSpec = RuntimeRecord('InitVarField', (_FieldIdProperty, _FieldOwnerProperty, _FieldNameProperty, _FieldOrderProperty, _FieldKindProperty, _BindingShapeProperty, _AnnotationProperty, _InitProperty, _HasDefaultProperty, _DefaultValueProperty, _DefaultValueParamNameProperty, _HasDefaultFactoryProperty, _DefaultFactoryProperty, _DefaultFactoryParamNameProperty, _DefaultFactoryParamNamesProperty, _HasWorkingDefaultFactoryProperty, _WorkingDefaultFactoryProperty, _WorkingDefaultFactoryParamNameProperty, _WorkingDefaultFactoryParamNamesProperty, _TxKeyKeyProperty, _ValueSlotNameProperty, _CurrentSlotNameProperty, _WorkingSlotNameProperty, _StagedSlotNameProperty, _HasFreezeProperty, _FreezeProperty, _FreezeParamNameProperty, _HasThawProperty, _ThawProperty, _ThawParamNameProperty, _HasOptionalNoneProperty))
_ClassVarFieldSpec = RuntimeRecord('ClassVarField', (_FieldIdProperty, _FieldOwnerProperty, _FieldNameProperty, _FieldOrderProperty, _FieldKindProperty, _BindingShapeProperty, _AnnotationProperty, _InitProperty, _HasDefaultProperty, _DefaultValueProperty, _DefaultValueParamNameProperty, _HasDefaultFactoryProperty, _DefaultFactoryProperty, _DefaultFactoryParamNameProperty, _DefaultFactoryParamNamesProperty, _HasWorkingDefaultFactoryProperty, _WorkingDefaultFactoryProperty, _WorkingDefaultFactoryParamNameProperty, _WorkingDefaultFactoryParamNamesProperty, _TxKeyKeyProperty, _ValueSlotNameProperty, _CurrentSlotNameProperty, _WorkingSlotNameProperty, _StagedSlotNameProperty, _HasFreezeProperty, _FreezeProperty, _FreezeParamNameProperty, _HasThawProperty, _ThawProperty, _ThawParamNameProperty, _HasOptionalNoneProperty))
_TransactionalFieldSpec = RuntimeRecord('TransactionalField', (_FieldIdProperty, _FieldOwnerProperty, _FieldNameProperty, _FieldOrderProperty, _TxKeyKeyProperty))
_TxKeySpec = RuntimeRecord('TxKey', (_TxOwnerProperty, _TxKeyKeyProperty, _TxIndexProperty, _TxKeyOrderProperty, _CommitOrderKeyFunctionNameProperty, _RequiresValidationFunctionNameProperty, _ValidateCommitFunctionNameProperty, _BeforeCommitFunctionNameProperty, _AfterCommitFunctionNameProperty, _AfterRollbackFunctionNameProperty, _PrepareCommitFieldsFunctionNameProperty, _ApplyPreparedCommitFieldsFunctionNameProperty, _RollbackFieldsFunctionNameProperty))
_IndexedTransactionalFieldSpec = RuntimeRecord('IndexedTransactionalField', (_FieldIdProperty, _FieldOwnerProperty, _FieldNameProperty, _FieldOrderProperty, _TxKeyKeyProperty, _TxIndexProperty, _CurrentSlotNameProperty, _WorkingSlotNameProperty, _StagedSlotNameProperty, _HasFreezeProperty, _FreezeParamNameProperty, _HasThawProperty, _ThawParamNameProperty, _HasOptionalNoneProperty))
_ManagedFieldSpec = RuntimeRecord('ManagedField', (_FieldIdProperty, _FieldOwnerProperty, _FieldNameProperty, _FieldOrderProperty, _FieldKindProperty, _BindingShapeProperty, _AnnotationProperty, _InitProperty, _HasDefaultProperty, _DefaultValueProperty, _DefaultValueParamNameProperty, _HasDefaultFactoryProperty, _DefaultFactoryProperty, _DefaultFactoryParamNameProperty, _DefaultFactoryParamNamesProperty, _HasWorkingDefaultFactoryProperty, _WorkingDefaultFactoryProperty, _WorkingDefaultFactoryParamNameProperty, _WorkingDefaultFactoryParamNamesProperty, _TxKeyKeyProperty, _ValueSlotNameProperty, _CurrentSlotNameProperty, _WorkingSlotNameProperty, _StagedSlotNameProperty, _HasFreezeProperty, _FreezeProperty, _FreezeParamNameProperty, _HasThawProperty, _ThawProperty, _ThawParamNameProperty, _HasOptionalNoneProperty))
_DefaultFactoryDependencySpec = RuntimeRecord('DefaultFactoryDependency', (_DependencyOwnerProperty, _ConsumerFieldIdProperty, _ConsumerFieldNameProperty, _ConsumerFieldKindProperty, _ConsumerFieldOrderProperty, _ProviderNameProperty, _ProviderFieldIdProperty, _ProviderFieldKindProperty, _ProviderInitProperty, _ProviderHasDefaultProperty, _ProviderHasDefaultFactoryProperty, _ParamNameProperty, _ParamOrderProperty, _ConsumerEvalOrderProperty))
_DefaultFactoryEvaluationStepSpec = RuntimeRecord('DefaultFactoryEvaluationStep', (_EvalStepIdProperty, _EvalOwnerProperty, _EvalFieldIdProperty, _EvalFieldNameProperty, _EvalFieldKindProperty, _EvalBindingShapeProperty, _EvalInitProperty, _EvalStateSlotNameProperty, _EvalDefaultFactoryParamNameProperty, _EvalOrderProperty, _EvalStatementOrderProperty))
_DefaultFactoryDiagnosticSpec = RuntimeRecord('DefaultFactoryDiagnostic', (_DiagnosticIdProperty, _DiagnosticOwnerProperty, _DiagnosticFieldIdProperty, _DiagnosticMessageProperty))
_IndexedTransientFieldSpec = RuntimeRecord('IndexedTransientField', (_FieldIdProperty, _FieldOwnerProperty, _FieldNameProperty, _FieldOrderProperty, _TxKeyKeyProperty, _TxIndexProperty, _CurrentSlotNameProperty, _WorkingSlotNameProperty, _HasWorkingDefaultFactoryProperty, _WorkingDefaultFactoryParamNameProperty))
_RetainedInitVarSpec = RuntimeRecord('RetainedInitVar', (_FieldIdProperty, _FieldOwnerProperty, _FieldNameProperty, _FieldOrderProperty, _RetainedSlotNameProperty, _RetainOrderProperty))
_TransientWorkingFactoryArgSpec = RuntimeRecord('TransientWorkingFactoryArg', (_WorkingFactoryArgIdProperty, _WorkingFactoryArgOwnerProperty, _WorkingFactoryConsumerFieldIdProperty, _WorkingFactoryConsumerFieldOrderProperty, _ParamNameProperty, _ParamOrderProperty, _ProviderNameProperty, _WorkingFactoryArgKindProperty, _RetainedSlotNameProperty))
_TransientFieldSpec = RuntimeRecord('TransientField', (_FieldIdProperty, _FieldOwnerProperty, _FieldNameProperty, _FieldOrderProperty, _FieldKindProperty, _BindingShapeProperty, _AnnotationProperty, _InitProperty, _HasDefaultProperty, _DefaultValueProperty, _DefaultValueParamNameProperty, _HasDefaultFactoryProperty, _DefaultFactoryProperty, _DefaultFactoryParamNameProperty, _DefaultFactoryParamNamesProperty, _HasWorkingDefaultFactoryProperty, _WorkingDefaultFactoryProperty, _WorkingDefaultFactoryParamNameProperty, _WorkingDefaultFactoryParamNamesProperty, _TxKeyKeyProperty, _ValueSlotNameProperty, _CurrentSlotNameProperty, _WorkingSlotNameProperty, _StagedSlotNameProperty, _HasFreezeProperty, _FreezeProperty, _FreezeParamNameProperty, _HasThawProperty, _ThawProperty, _ThawParamNameProperty, _HasOptionalNoneProperty))
_IndexedOwnedFieldSpec = RuntimeRecord('IndexedOwnedField', (_FieldIdProperty, _FieldOwnerProperty, _FieldNameProperty, _FieldOrderProperty, _BindingShapeProperty, _TxKeyKeyProperty, _TxIndexProperty, _CurrentSlotNameProperty, _WorkingSlotNameProperty, _StagedSlotNameProperty))
_BindingFieldSpec = RuntimeRecord('BindingField', (_FieldIdProperty, _FieldOwnerProperty, _FieldNameProperty, _FieldOrderProperty, _FieldKindProperty, _BindingShapeProperty, _AnnotationProperty, _InitProperty, _HasDefaultProperty, _DefaultValueProperty, _DefaultValueParamNameProperty, _HasDefaultFactoryProperty, _DefaultFactoryProperty, _DefaultFactoryParamNameProperty, _DefaultFactoryParamNamesProperty, _HasWorkingDefaultFactoryProperty, _WorkingDefaultFactoryProperty, _WorkingDefaultFactoryParamNameProperty, _WorkingDefaultFactoryParamNamesProperty, _TxKeyKeyProperty, _ValueSlotNameProperty, _CurrentSlotNameProperty, _WorkingSlotNameProperty, _StagedSlotNameProperty, _HasFreezeProperty, _FreezeProperty, _FreezeParamNameProperty, _HasThawProperty, _ThawProperty, _ThawParamNameProperty, _HasOptionalNoneProperty))
_OwnedFieldSpec = RuntimeRecord('OwnedField', (_FieldIdProperty, _FieldOwnerProperty, _FieldNameProperty, _FieldOrderProperty, _FieldKindProperty, _BindingShapeProperty, _AnnotationProperty, _InitProperty, _HasDefaultProperty, _DefaultValueProperty, _DefaultValueParamNameProperty, _HasDefaultFactoryProperty, _DefaultFactoryProperty, _DefaultFactoryParamNameProperty, _DefaultFactoryParamNamesProperty, _HasWorkingDefaultFactoryProperty, _WorkingDefaultFactoryProperty, _WorkingDefaultFactoryParamNameProperty, _WorkingDefaultFactoryParamNamesProperty, _TxKeyKeyProperty, _ValueSlotNameProperty, _CurrentSlotNameProperty, _WorkingSlotNameProperty, _StagedSlotNameProperty, _HasFreezeProperty, _FreezeProperty, _FreezeParamNameProperty, _HasThawProperty, _ThawProperty, _ThawParamNameProperty, _HasOptionalNoneProperty))
_ConstFieldSpec = RuntimeRecord('ConstField', (_FieldIdProperty, _FieldOwnerProperty, _FieldNameProperty, _FieldOrderProperty, _FieldKindProperty, _BindingShapeProperty, _AnnotationProperty, _InitProperty, _HasDefaultProperty, _DefaultValueProperty, _DefaultValueParamNameProperty, _HasDefaultFactoryProperty, _DefaultFactoryProperty, _DefaultFactoryParamNameProperty, _DefaultFactoryParamNamesProperty, _HasWorkingDefaultFactoryProperty, _WorkingDefaultFactoryProperty, _WorkingDefaultFactoryParamNameProperty, _WorkingDefaultFactoryParamNamesProperty, _TxKeyKeyProperty, _ValueSlotNameProperty, _CurrentSlotNameProperty, _WorkingSlotNameProperty, _StagedSlotNameProperty, _HasFreezeProperty, _FreezeProperty, _FreezeParamNameProperty, _HasThawProperty, _ThawProperty, _ThawParamNameProperty, _HasOptionalNoneProperty))
_StaticFieldSpec = RuntimeRecord('StaticField', (_FieldIdProperty, _FieldOwnerProperty, _FieldNameProperty, _FieldOrderProperty, _FieldKindProperty, _BindingShapeProperty, _AnnotationProperty, _InitProperty, _HasDefaultProperty, _DefaultValueProperty, _DefaultValueParamNameProperty, _HasDefaultFactoryProperty, _DefaultFactoryProperty, _DefaultFactoryParamNameProperty, _DefaultFactoryParamNamesProperty, _HasWorkingDefaultFactoryProperty, _WorkingDefaultFactoryProperty, _WorkingDefaultFactoryParamNameProperty, _WorkingDefaultFactoryParamNamesProperty, _TxKeyKeyProperty, _ValueSlotNameProperty, _CurrentSlotNameProperty, _WorkingSlotNameProperty, _StagedSlotNameProperty, _HasFreezeProperty, _FreezeProperty, _FreezeParamNameProperty, _HasThawProperty, _ThawProperty, _ThawParamNameProperty, _HasOptionalNoneProperty))
_LifecycleFieldSpecUnion = RuntimeUnion('LifecycleFieldSpec', (_PlainFieldSpec, _InitVarFieldSpec, _ClassVarFieldSpec, _ManagedFieldSpec, _TransientFieldSpec, _BindingFieldSpec, _OwnedFieldSpec, _ConstFieldSpec, _StaticFieldSpec))

class LifecycleClass:
    __slots__ = ('class_id', 'class_name', 'class_order', 'module_name', 'state_class_name', 'facade_base_class_name', 'current_facade_class_name', 'working_facade_class_name', 'lifecycle_definition_param_name', 'annotations_param_name', 'tx_keys_param_name', 'lifecycle_field_names')
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
    tx_keys_param_name: str
    lifecycle_field_names: object

    def __init__(self, *, class_id: str, class_name: str, class_order: int=0, module_name: str='__main__', state_class_name: str, facade_base_class_name: str, current_facade_class_name: str, working_facade_class_name: str, lifecycle_definition_param_name: str='', annotations_param_name: str='', tx_keys_param_name: str='', lifecycle_field_names: object=()):
        if not isinstance(class_id, str):
            raise TypeError('ClassId must be str, got ' + type(class_id).__name__)
        object.__setattr__(self, 'class_id', class_id)
        if not isinstance(class_name, str):
            raise TypeError('ClassName must be str, got ' + type(class_name).__name__)
        object.__setattr__(self, 'class_name', class_name)
        if not isinstance(class_order, int):
            raise TypeError('ClassOrder must be int, got ' + type(class_order).__name__)
        object.__setattr__(self, 'class_order', class_order)
        if not isinstance(module_name, str):
            raise TypeError('ModuleName must be str, got ' + type(module_name).__name__)
        object.__setattr__(self, 'module_name', module_name)
        if not isinstance(state_class_name, str):
            raise TypeError('StateClassName must be str, got ' + type(state_class_name).__name__)
        object.__setattr__(self, 'state_class_name', state_class_name)
        if not isinstance(facade_base_class_name, str):
            raise TypeError('FacadeBaseClassName must be str, got ' + type(facade_base_class_name).__name__)
        object.__setattr__(self, 'facade_base_class_name', facade_base_class_name)
        if not isinstance(current_facade_class_name, str):
            raise TypeError('CurrentFacadeClassName must be str, got ' + type(current_facade_class_name).__name__)
        object.__setattr__(self, 'current_facade_class_name', current_facade_class_name)
        if not isinstance(working_facade_class_name, str):
            raise TypeError('WorkingFacadeClassName must be str, got ' + type(working_facade_class_name).__name__)
        object.__setattr__(self, 'working_facade_class_name', working_facade_class_name)
        if not isinstance(lifecycle_definition_param_name, str):
            raise TypeError('LifecycleDefinitionParamName must be str, got ' + type(lifecycle_definition_param_name).__name__)
        object.__setattr__(self, 'lifecycle_definition_param_name', lifecycle_definition_param_name)
        if not isinstance(annotations_param_name, str):
            raise TypeError('AnnotationsParamName must be str, got ' + type(annotations_param_name).__name__)
        object.__setattr__(self, 'annotations_param_name', annotations_param_name)
        if not isinstance(tx_keys_param_name, str):
            raise TypeError('TxKeysParamName must be str, got ' + type(tx_keys_param_name).__name__)
        object.__setattr__(self, 'tx_keys_param_name', tx_keys_param_name)
        object.__setattr__(self, 'lifecycle_field_names', lifecycle_field_names)

    def __setattr__(self, name, value):
        if name in ('class_id', 'class_name', 'class_order', 'module_name', 'state_class_name', 'facade_base_class_name', 'current_facade_class_name', 'working_facade_class_name', 'lifecycle_definition_param_name', 'annotations_param_name', 'tx_keys_param_name', 'lifecycle_field_names'):
            raise AttributeError('LifecycleClass records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('class_id=' + repr(self.class_id))
        pieces.append('class_name=' + repr(self.class_name))
        pieces.append('class_order=' + repr(self.class_order))
        pieces.append('module_name=' + repr(self.module_name))
        pieces.append('state_class_name=' + repr(self.state_class_name))
        pieces.append('facade_base_class_name=' + repr(self.facade_base_class_name))
        pieces.append('current_facade_class_name=' + repr(self.current_facade_class_name))
        pieces.append('working_facade_class_name=' + repr(self.working_facade_class_name))
        pieces.append('lifecycle_definition_param_name=' + repr(self.lifecycle_definition_param_name))
        pieces.append('annotations_param_name=' + repr(self.annotations_param_name))
        pieces.append('tx_keys_param_name=' + repr(self.tx_keys_param_name))
        pieces.append('lifecycle_field_names=' + repr(self.lifecycle_field_names))
        return 'LifecycleClass' + '(' + ', '.join(pieces) + ')'
_LifecycleClassSpec.bind_record_class(LifecycleClass)

class TransactionMethod:
    __slots__ = ('method_id', 'method_owner', 'method_name', 'method_kind', 'tx_key_key', 'tx_index', 'declaration_order')
    __dds_record_spec__ = _TransactionMethodSpec
    method_id: str
    method_owner: str
    method_name: str
    method_kind: str
    tx_key_key: object
    tx_index: int
    declaration_order: int

    def __init__(self, *, method_id: str, method_owner: str, method_name: str, method_kind: str, tx_key_key: object=None, tx_index: int=0, declaration_order: int=0):
        if not isinstance(method_id, str):
            raise TypeError('MethodId must be str, got ' + type(method_id).__name__)
        object.__setattr__(self, 'method_id', method_id)
        if not isinstance(method_owner, str):
            raise TypeError('MethodOwner must be str, got ' + type(method_owner).__name__)
        object.__setattr__(self, 'method_owner', method_owner)
        if not isinstance(method_name, str):
            raise TypeError('MethodName must be str, got ' + type(method_name).__name__)
        object.__setattr__(self, 'method_name', method_name)
        if not isinstance(method_kind, str):
            raise TypeError('MethodKind must be str, got ' + type(method_kind).__name__)
        object.__setattr__(self, 'method_kind', method_kind)
        object.__setattr__(self, 'tx_key_key', tx_key_key)
        if not isinstance(tx_index, int):
            raise TypeError('TxIndex must be int, got ' + type(tx_index).__name__)
        object.__setattr__(self, 'tx_index', tx_index)
        if not isinstance(declaration_order, int):
            raise TypeError('DeclarationOrder must be int, got ' + type(declaration_order).__name__)
        object.__setattr__(self, 'declaration_order', declaration_order)

    def __setattr__(self, name, value):
        if name in ('method_id', 'method_owner', 'method_name', 'method_kind', 'tx_key_key', 'tx_index', 'declaration_order'):
            raise AttributeError('TransactionMethod records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('method_id=' + repr(self.method_id))
        pieces.append('method_owner=' + repr(self.method_owner))
        pieces.append('method_name=' + repr(self.method_name))
        pieces.append('method_kind=' + repr(self.method_kind))
        pieces.append('tx_key_key=' + repr(self.tx_key_key))
        pieces.append('tx_index=' + repr(self.tx_index))
        pieces.append('declaration_order=' + repr(self.declaration_order))
        return 'TransactionMethod' + '(' + ', '.join(pieces) + ')'
_TransactionMethodSpec.bind_record_class(TransactionMethod)

class FacadeClass:
    __slots__ = ('facade_owner', 'facade_id', 'facade_kind', 'facade_mode', 'facade_class_name', 'facade_order')
    __dds_record_spec__ = _FacadeClassSpec
    facade_owner: str
    facade_id: str
    facade_kind: str
    facade_mode: str
    facade_class_name: str
    facade_order: int

    def __init__(self, *, facade_owner: str, facade_id: str, facade_kind: str, facade_mode: str, facade_class_name: str, facade_order: int=0):
        if not isinstance(facade_owner, str):
            raise TypeError('FacadeOwner must be str, got ' + type(facade_owner).__name__)
        object.__setattr__(self, 'facade_owner', facade_owner)
        if not isinstance(facade_id, str):
            raise TypeError('FacadeId must be str, got ' + type(facade_id).__name__)
        object.__setattr__(self, 'facade_id', facade_id)
        if not isinstance(facade_kind, str):
            raise TypeError('FacadeKind must be str, got ' + type(facade_kind).__name__)
        object.__setattr__(self, 'facade_kind', facade_kind)
        if not isinstance(facade_mode, str):
            raise TypeError('FacadeMode must be str, got ' + type(facade_mode).__name__)
        object.__setattr__(self, 'facade_mode', facade_mode)
        if not isinstance(facade_class_name, str):
            raise TypeError('FacadeClassName must be str, got ' + type(facade_class_name).__name__)
        object.__setattr__(self, 'facade_class_name', facade_class_name)
        if not isinstance(facade_order, int):
            raise TypeError('FacadeOrder must be int, got ' + type(facade_order).__name__)
        object.__setattr__(self, 'facade_order', facade_order)

    def __setattr__(self, name, value):
        if name in ('facade_owner', 'facade_id', 'facade_kind', 'facade_mode', 'facade_class_name', 'facade_order'):
            raise AttributeError('FacadeClass records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('facade_owner=' + repr(self.facade_owner))
        pieces.append('facade_id=' + repr(self.facade_id))
        pieces.append('facade_kind=' + repr(self.facade_kind))
        pieces.append('facade_mode=' + repr(self.facade_mode))
        pieces.append('facade_class_name=' + repr(self.facade_class_name))
        pieces.append('facade_order=' + repr(self.facade_order))
        return 'FacadeClass' + '(' + ', '.join(pieces) + ')'
_FacadeClassSpec.bind_record_class(FacadeClass)

class FacadeExposure:
    __slots__ = ('facade_owner', 'owner_facade_id', 'field_name', 'target_facade_id', 'exposure_order')
    __dds_record_spec__ = _FacadeExposureSpec
    facade_owner: str
    owner_facade_id: str
    field_name: str
    target_facade_id: str
    exposure_order: int

    def __init__(self, *, facade_owner: str, owner_facade_id: str, field_name: str, target_facade_id: str, exposure_order: int=0):
        if not isinstance(facade_owner, str):
            raise TypeError('FacadeOwner must be str, got ' + type(facade_owner).__name__)
        object.__setattr__(self, 'facade_owner', facade_owner)
        if not isinstance(owner_facade_id, str):
            raise TypeError('OwnerFacadeId must be str, got ' + type(owner_facade_id).__name__)
        object.__setattr__(self, 'owner_facade_id', owner_facade_id)
        if not isinstance(field_name, str):
            raise TypeError('FieldName must be str, got ' + type(field_name).__name__)
        object.__setattr__(self, 'field_name', field_name)
        if not isinstance(target_facade_id, str):
            raise TypeError('TargetFacadeId must be str, got ' + type(target_facade_id).__name__)
        object.__setattr__(self, 'target_facade_id', target_facade_id)
        if not isinstance(exposure_order, int):
            raise TypeError('ExposureOrder must be int, got ' + type(exposure_order).__name__)
        object.__setattr__(self, 'exposure_order', exposure_order)

    def __setattr__(self, name, value):
        if name in ('facade_owner', 'owner_facade_id', 'field_name', 'target_facade_id', 'exposure_order'):
            raise AttributeError('FacadeExposure records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('facade_owner=' + repr(self.facade_owner))
        pieces.append('owner_facade_id=' + repr(self.owner_facade_id))
        pieces.append('field_name=' + repr(self.field_name))
        pieces.append('target_facade_id=' + repr(self.target_facade_id))
        pieces.append('exposure_order=' + repr(self.exposure_order))
        return 'FacadeExposure' + '(' + ', '.join(pieces) + ')'
_FacadeExposureSpec.bind_record_class(FacadeExposure)

class InitParameter:
    __slots__ = ('init_parameter_id', 'init_parameter_owner', 'init_parameter_name', 'init_parameter_order', 'init_parameter_kind')
    __dds_record_spec__ = _InitParameterSpec
    init_parameter_id: str
    init_parameter_owner: str
    init_parameter_name: str
    init_parameter_order: int
    init_parameter_kind: str

    def __init__(self, *, init_parameter_id: str, init_parameter_owner: str, init_parameter_name: str, init_parameter_order: int=0, init_parameter_kind: str='field'):
        if not isinstance(init_parameter_id, str):
            raise TypeError('InitParameterId must be str, got ' + type(init_parameter_id).__name__)
        object.__setattr__(self, 'init_parameter_id', init_parameter_id)
        if not isinstance(init_parameter_owner, str):
            raise TypeError('InitParameterOwner must be str, got ' + type(init_parameter_owner).__name__)
        object.__setattr__(self, 'init_parameter_owner', init_parameter_owner)
        if not isinstance(init_parameter_name, str):
            raise TypeError('InitParameterName must be str, got ' + type(init_parameter_name).__name__)
        object.__setattr__(self, 'init_parameter_name', init_parameter_name)
        if not isinstance(init_parameter_order, int):
            raise TypeError('InitParameterOrder must be int, got ' + type(init_parameter_order).__name__)
        object.__setattr__(self, 'init_parameter_order', init_parameter_order)
        if not isinstance(init_parameter_kind, str):
            raise TypeError('InitParameterKind must be str, got ' + type(init_parameter_kind).__name__)
        object.__setattr__(self, 'init_parameter_kind', init_parameter_kind)

    def __setattr__(self, name, value):
        if name in ('init_parameter_id', 'init_parameter_owner', 'init_parameter_name', 'init_parameter_order', 'init_parameter_kind'):
            raise AttributeError('InitParameter records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('init_parameter_id=' + repr(self.init_parameter_id))
        pieces.append('init_parameter_owner=' + repr(self.init_parameter_owner))
        pieces.append('init_parameter_name=' + repr(self.init_parameter_name))
        pieces.append('init_parameter_order=' + repr(self.init_parameter_order))
        pieces.append('init_parameter_kind=' + repr(self.init_parameter_kind))
        return 'InitParameter' + '(' + ', '.join(pieces) + ')'
_InitParameterSpec.bind_record_class(InitParameter)

class InitAssignment:
    __slots__ = ('init_assignment_id', 'init_assignment_owner', 'init_assignment_field_id', 'init_assignment_field_name', 'init_assignment_order', 'init_assignment_kind')
    __dds_record_spec__ = _InitAssignmentSpec
    init_assignment_id: str
    init_assignment_owner: str
    init_assignment_field_id: str
    init_assignment_field_name: str
    init_assignment_order: int
    init_assignment_kind: str

    def __init__(self, *, init_assignment_id: str, init_assignment_owner: str, init_assignment_field_id: str, init_assignment_field_name: str, init_assignment_order: int=0, init_assignment_kind: str='plain'):
        if not isinstance(init_assignment_id, str):
            raise TypeError('InitAssignmentId must be str, got ' + type(init_assignment_id).__name__)
        object.__setattr__(self, 'init_assignment_id', init_assignment_id)
        if not isinstance(init_assignment_owner, str):
            raise TypeError('InitAssignmentOwner must be str, got ' + type(init_assignment_owner).__name__)
        object.__setattr__(self, 'init_assignment_owner', init_assignment_owner)
        if not isinstance(init_assignment_field_id, str):
            raise TypeError('InitAssignmentFieldId must be str, got ' + type(init_assignment_field_id).__name__)
        object.__setattr__(self, 'init_assignment_field_id', init_assignment_field_id)
        if not isinstance(init_assignment_field_name, str):
            raise TypeError('InitAssignmentFieldName must be str, got ' + type(init_assignment_field_name).__name__)
        object.__setattr__(self, 'init_assignment_field_name', init_assignment_field_name)
        if not isinstance(init_assignment_order, int):
            raise TypeError('InitAssignmentOrder must be int, got ' + type(init_assignment_order).__name__)
        object.__setattr__(self, 'init_assignment_order', init_assignment_order)
        if not isinstance(init_assignment_kind, str):
            raise TypeError('InitAssignmentKind must be str, got ' + type(init_assignment_kind).__name__)
        object.__setattr__(self, 'init_assignment_kind', init_assignment_kind)

    def __setattr__(self, name, value):
        if name in ('init_assignment_id', 'init_assignment_owner', 'init_assignment_field_id', 'init_assignment_field_name', 'init_assignment_order', 'init_assignment_kind'):
            raise AttributeError('InitAssignment records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('init_assignment_id=' + repr(self.init_assignment_id))
        pieces.append('init_assignment_owner=' + repr(self.init_assignment_owner))
        pieces.append('init_assignment_field_id=' + repr(self.init_assignment_field_id))
        pieces.append('init_assignment_field_name=' + repr(self.init_assignment_field_name))
        pieces.append('init_assignment_order=' + repr(self.init_assignment_order))
        pieces.append('init_assignment_kind=' + repr(self.init_assignment_kind))
        return 'InitAssignment' + '(' + ', '.join(pieces) + ')'
_InitAssignmentSpec.bind_record_class(InitAssignment)

class ClassVarAssignment:
    __slots__ = ('class_var_assignment_id', 'class_var_assignment_owner', 'class_var_assignment_name', 'class_var_assignment_order')
    __dds_record_spec__ = _ClassVarAssignmentSpec
    class_var_assignment_id: str
    class_var_assignment_owner: str
    class_var_assignment_name: str
    class_var_assignment_order: int

    def __init__(self, *, class_var_assignment_id: str, class_var_assignment_owner: str, class_var_assignment_name: str, class_var_assignment_order: int=0):
        if not isinstance(class_var_assignment_id, str):
            raise TypeError('ClassVarAssignmentId must be str, got ' + type(class_var_assignment_id).__name__)
        object.__setattr__(self, 'class_var_assignment_id', class_var_assignment_id)
        if not isinstance(class_var_assignment_owner, str):
            raise TypeError('ClassVarAssignmentOwner must be str, got ' + type(class_var_assignment_owner).__name__)
        object.__setattr__(self, 'class_var_assignment_owner', class_var_assignment_owner)
        if not isinstance(class_var_assignment_name, str):
            raise TypeError('ClassVarAssignmentName must be str, got ' + type(class_var_assignment_name).__name__)
        object.__setattr__(self, 'class_var_assignment_name', class_var_assignment_name)
        if not isinstance(class_var_assignment_order, int):
            raise TypeError('ClassVarAssignmentOrder must be int, got ' + type(class_var_assignment_order).__name__)
        object.__setattr__(self, 'class_var_assignment_order', class_var_assignment_order)

    def __setattr__(self, name, value):
        if name in ('class_var_assignment_id', 'class_var_assignment_owner', 'class_var_assignment_name', 'class_var_assignment_order'):
            raise AttributeError('ClassVarAssignment records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('class_var_assignment_id=' + repr(self.class_var_assignment_id))
        pieces.append('class_var_assignment_owner=' + repr(self.class_var_assignment_owner))
        pieces.append('class_var_assignment_name=' + repr(self.class_var_assignment_name))
        pieces.append('class_var_assignment_order=' + repr(self.class_var_assignment_order))
        return 'ClassVarAssignment' + '(' + ', '.join(pieces) + ')'
_ClassVarAssignmentSpec.bind_record_class(ClassVarAssignment)

class PlainField:
    __slots__ = ('field_id', 'field_owner', 'field_name', 'field_order', 'field_kind', 'binding_shape', 'annotation', 'init', 'has_default', 'default_value', 'default_value_param_name', 'has_default_factory', 'default_factory', 'default_factory_param_name', 'default_factory_param_names', 'has_working_default_factory', 'working_default_factory', 'working_default_factory_param_name', 'working_default_factory_param_names', 'tx_key_key', 'value_slot_name', 'current_slot_name', 'working_slot_name', 'staged_slot_name', 'has_freeze', 'freeze', 'freeze_param_name', 'has_thaw', 'thaw', 'thaw_param_name', 'has_optional_none')
    __dds_record_spec__ = _PlainFieldSpec
    field_id: str
    field_owner: str
    field_name: str
    field_order: int
    field_kind: str
    binding_shape: str
    annotation: object
    init: bool
    has_default: bool
    default_value: object
    default_value_param_name: str
    has_default_factory: bool
    default_factory: object
    default_factory_param_name: str
    default_factory_param_names: object
    has_working_default_factory: bool
    working_default_factory: object
    working_default_factory_param_name: str
    working_default_factory_param_names: object
    tx_key_key: object
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

    def __init__(self, *, field_id: str, field_owner: str, field_name: str, field_order: int, field_kind: str='field', binding_shape: str='scalar', annotation: object=object, init: bool=True, has_default: bool=False, default_value: object=None, default_value_param_name: str='', has_default_factory: bool=False, default_factory: object=None, default_factory_param_name: str='', default_factory_param_names: object=(), has_working_default_factory: bool=False, working_default_factory: object=None, working_default_factory_param_name: str='', working_default_factory_param_names: object=(), tx_key_key: object=None, value_slot_name: str='', current_slot_name: str='', working_slot_name: str='', staged_slot_name: str='', has_freeze: bool=False, freeze: object=None, freeze_param_name: str='', has_thaw: bool=False, thaw: object=None, thaw_param_name: str='', has_optional_none: bool=False):
        if not isinstance(field_id, str):
            raise TypeError('FieldId must be str, got ' + type(field_id).__name__)
        object.__setattr__(self, 'field_id', field_id)
        if not isinstance(field_owner, str):
            raise TypeError('FieldOwner must be str, got ' + type(field_owner).__name__)
        object.__setattr__(self, 'field_owner', field_owner)
        if not isinstance(field_name, str):
            raise TypeError('FieldName must be str, got ' + type(field_name).__name__)
        object.__setattr__(self, 'field_name', field_name)
        if not isinstance(field_order, int):
            raise TypeError('FieldOrder must be int, got ' + type(field_order).__name__)
        object.__setattr__(self, 'field_order', field_order)
        if not isinstance(field_kind, str):
            raise TypeError('FieldKind must be str, got ' + type(field_kind).__name__)
        object.__setattr__(self, 'field_kind', field_kind)
        if not isinstance(binding_shape, str):
            raise TypeError('BindingShape must be str, got ' + type(binding_shape).__name__)
        object.__setattr__(self, 'binding_shape', binding_shape)
        object.__setattr__(self, 'annotation', annotation)
        if not isinstance(init, bool):
            raise TypeError('Init must be bool, got ' + type(init).__name__)
        object.__setattr__(self, 'init', init)
        if not isinstance(has_default, bool):
            raise TypeError('HasDefault must be bool, got ' + type(has_default).__name__)
        object.__setattr__(self, 'has_default', has_default)
        object.__setattr__(self, 'default_value', default_value)
        if not isinstance(default_value_param_name, str):
            raise TypeError('DefaultValueParamName must be str, got ' + type(default_value_param_name).__name__)
        object.__setattr__(self, 'default_value_param_name', default_value_param_name)
        if not isinstance(has_default_factory, bool):
            raise TypeError('HasDefaultFactory must be bool, got ' + type(has_default_factory).__name__)
        object.__setattr__(self, 'has_default_factory', has_default_factory)
        object.__setattr__(self, 'default_factory', default_factory)
        if not isinstance(default_factory_param_name, str):
            raise TypeError('DefaultFactoryParamName must be str, got ' + type(default_factory_param_name).__name__)
        object.__setattr__(self, 'default_factory_param_name', default_factory_param_name)
        object.__setattr__(self, 'default_factory_param_names', default_factory_param_names)
        if not isinstance(has_working_default_factory, bool):
            raise TypeError('HasWorkingDefaultFactory must be bool, got ' + type(has_working_default_factory).__name__)
        object.__setattr__(self, 'has_working_default_factory', has_working_default_factory)
        object.__setattr__(self, 'working_default_factory', working_default_factory)
        if not isinstance(working_default_factory_param_name, str):
            raise TypeError('WorkingDefaultFactoryParamName must be str, got ' + type(working_default_factory_param_name).__name__)
        object.__setattr__(self, 'working_default_factory_param_name', working_default_factory_param_name)
        object.__setattr__(self, 'working_default_factory_param_names', working_default_factory_param_names)
        object.__setattr__(self, 'tx_key_key', tx_key_key)
        if not isinstance(value_slot_name, str):
            raise TypeError('ValueSlotName must be str, got ' + type(value_slot_name).__name__)
        object.__setattr__(self, 'value_slot_name', value_slot_name)
        if not isinstance(current_slot_name, str):
            raise TypeError('CurrentSlotName must be str, got ' + type(current_slot_name).__name__)
        object.__setattr__(self, 'current_slot_name', current_slot_name)
        if not isinstance(working_slot_name, str):
            raise TypeError('WorkingSlotName must be str, got ' + type(working_slot_name).__name__)
        object.__setattr__(self, 'working_slot_name', working_slot_name)
        if not isinstance(staged_slot_name, str):
            raise TypeError('StagedSlotName must be str, got ' + type(staged_slot_name).__name__)
        object.__setattr__(self, 'staged_slot_name', staged_slot_name)
        if not isinstance(has_freeze, bool):
            raise TypeError('HasFreeze must be bool, got ' + type(has_freeze).__name__)
        object.__setattr__(self, 'has_freeze', has_freeze)
        object.__setattr__(self, 'freeze', freeze)
        if not isinstance(freeze_param_name, str):
            raise TypeError('FreezeParamName must be str, got ' + type(freeze_param_name).__name__)
        object.__setattr__(self, 'freeze_param_name', freeze_param_name)
        if not isinstance(has_thaw, bool):
            raise TypeError('HasThaw must be bool, got ' + type(has_thaw).__name__)
        object.__setattr__(self, 'has_thaw', has_thaw)
        object.__setattr__(self, 'thaw', thaw)
        if not isinstance(thaw_param_name, str):
            raise TypeError('ThawParamName must be str, got ' + type(thaw_param_name).__name__)
        object.__setattr__(self, 'thaw_param_name', thaw_param_name)
        if not isinstance(has_optional_none, bool):
            raise TypeError('HasOptionalNone must be bool, got ' + type(has_optional_none).__name__)
        object.__setattr__(self, 'has_optional_none', has_optional_none)

    def __setattr__(self, name, value):
        if name in ('field_id', 'field_owner', 'field_name', 'field_order', 'field_kind', 'binding_shape', 'annotation', 'init', 'has_default', 'default_value', 'default_value_param_name', 'has_default_factory', 'default_factory', 'default_factory_param_name', 'default_factory_param_names', 'has_working_default_factory', 'working_default_factory', 'working_default_factory_param_name', 'working_default_factory_param_names', 'tx_key_key', 'value_slot_name', 'current_slot_name', 'working_slot_name', 'staged_slot_name', 'has_freeze', 'freeze', 'freeze_param_name', 'has_thaw', 'thaw', 'thaw_param_name', 'has_optional_none'):
            raise AttributeError('PlainField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('field_id=' + repr(self.field_id))
        pieces.append('field_owner=' + repr(self.field_owner))
        pieces.append('field_name=' + repr(self.field_name))
        pieces.append('field_order=' + repr(self.field_order))
        pieces.append('field_kind=' + repr(self.field_kind))
        pieces.append('binding_shape=' + repr(self.binding_shape))
        pieces.append('annotation=' + repr(self.annotation))
        pieces.append('init=' + repr(self.init))
        pieces.append('has_default=' + repr(self.has_default))
        pieces.append('default_value=' + repr(self.default_value))
        pieces.append('default_value_param_name=' + repr(self.default_value_param_name))
        pieces.append('has_default_factory=' + repr(self.has_default_factory))
        pieces.append('default_factory=' + repr(self.default_factory))
        pieces.append('default_factory_param_name=' + repr(self.default_factory_param_name))
        pieces.append('default_factory_param_names=' + repr(self.default_factory_param_names))
        pieces.append('has_working_default_factory=' + repr(self.has_working_default_factory))
        pieces.append('working_default_factory=' + repr(self.working_default_factory))
        pieces.append('working_default_factory_param_name=' + repr(self.working_default_factory_param_name))
        pieces.append('working_default_factory_param_names=' + repr(self.working_default_factory_param_names))
        pieces.append('tx_key_key=' + repr(self.tx_key_key))
        pieces.append('value_slot_name=' + repr(self.value_slot_name))
        pieces.append('current_slot_name=' + repr(self.current_slot_name))
        pieces.append('working_slot_name=' + repr(self.working_slot_name))
        pieces.append('staged_slot_name=' + repr(self.staged_slot_name))
        pieces.append('has_freeze=' + repr(self.has_freeze))
        pieces.append('freeze=' + repr(self.freeze))
        pieces.append('freeze_param_name=' + repr(self.freeze_param_name))
        pieces.append('has_thaw=' + repr(self.has_thaw))
        pieces.append('thaw=' + repr(self.thaw))
        pieces.append('thaw_param_name=' + repr(self.thaw_param_name))
        pieces.append('has_optional_none=' + repr(self.has_optional_none))
        return 'PlainField' + '(' + ', '.join(pieces) + ')'
_PlainFieldSpec.bind_record_class(PlainField)

class InitVarField:
    __slots__ = ('field_id', 'field_owner', 'field_name', 'field_order', 'field_kind', 'binding_shape', 'annotation', 'init', 'has_default', 'default_value', 'default_value_param_name', 'has_default_factory', 'default_factory', 'default_factory_param_name', 'default_factory_param_names', 'has_working_default_factory', 'working_default_factory', 'working_default_factory_param_name', 'working_default_factory_param_names', 'tx_key_key', 'value_slot_name', 'current_slot_name', 'working_slot_name', 'staged_slot_name', 'has_freeze', 'freeze', 'freeze_param_name', 'has_thaw', 'thaw', 'thaw_param_name', 'has_optional_none')
    __dds_record_spec__ = _InitVarFieldSpec
    field_id: str
    field_owner: str
    field_name: str
    field_order: int
    field_kind: str
    binding_shape: str
    annotation: object
    init: bool
    has_default: bool
    default_value: object
    default_value_param_name: str
    has_default_factory: bool
    default_factory: object
    default_factory_param_name: str
    default_factory_param_names: object
    has_working_default_factory: bool
    working_default_factory: object
    working_default_factory_param_name: str
    working_default_factory_param_names: object
    tx_key_key: object
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

    def __init__(self, *, field_id: str, field_owner: str, field_name: str, field_order: int, field_kind: str='field', binding_shape: str='scalar', annotation: object=object, init: bool=True, has_default: bool=False, default_value: object=None, default_value_param_name: str='', has_default_factory: bool=False, default_factory: object=None, default_factory_param_name: str='', default_factory_param_names: object=(), has_working_default_factory: bool=False, working_default_factory: object=None, working_default_factory_param_name: str='', working_default_factory_param_names: object=(), tx_key_key: object=None, value_slot_name: str='', current_slot_name: str='', working_slot_name: str='', staged_slot_name: str='', has_freeze: bool=False, freeze: object=None, freeze_param_name: str='', has_thaw: bool=False, thaw: object=None, thaw_param_name: str='', has_optional_none: bool=False):
        if not isinstance(field_id, str):
            raise TypeError('FieldId must be str, got ' + type(field_id).__name__)
        object.__setattr__(self, 'field_id', field_id)
        if not isinstance(field_owner, str):
            raise TypeError('FieldOwner must be str, got ' + type(field_owner).__name__)
        object.__setattr__(self, 'field_owner', field_owner)
        if not isinstance(field_name, str):
            raise TypeError('FieldName must be str, got ' + type(field_name).__name__)
        object.__setattr__(self, 'field_name', field_name)
        if not isinstance(field_order, int):
            raise TypeError('FieldOrder must be int, got ' + type(field_order).__name__)
        object.__setattr__(self, 'field_order', field_order)
        if not isinstance(field_kind, str):
            raise TypeError('FieldKind must be str, got ' + type(field_kind).__name__)
        object.__setattr__(self, 'field_kind', field_kind)
        if not isinstance(binding_shape, str):
            raise TypeError('BindingShape must be str, got ' + type(binding_shape).__name__)
        object.__setattr__(self, 'binding_shape', binding_shape)
        object.__setattr__(self, 'annotation', annotation)
        if not isinstance(init, bool):
            raise TypeError('Init must be bool, got ' + type(init).__name__)
        object.__setattr__(self, 'init', init)
        if not isinstance(has_default, bool):
            raise TypeError('HasDefault must be bool, got ' + type(has_default).__name__)
        object.__setattr__(self, 'has_default', has_default)
        object.__setattr__(self, 'default_value', default_value)
        if not isinstance(default_value_param_name, str):
            raise TypeError('DefaultValueParamName must be str, got ' + type(default_value_param_name).__name__)
        object.__setattr__(self, 'default_value_param_name', default_value_param_name)
        if not isinstance(has_default_factory, bool):
            raise TypeError('HasDefaultFactory must be bool, got ' + type(has_default_factory).__name__)
        object.__setattr__(self, 'has_default_factory', has_default_factory)
        object.__setattr__(self, 'default_factory', default_factory)
        if not isinstance(default_factory_param_name, str):
            raise TypeError('DefaultFactoryParamName must be str, got ' + type(default_factory_param_name).__name__)
        object.__setattr__(self, 'default_factory_param_name', default_factory_param_name)
        object.__setattr__(self, 'default_factory_param_names', default_factory_param_names)
        if not isinstance(has_working_default_factory, bool):
            raise TypeError('HasWorkingDefaultFactory must be bool, got ' + type(has_working_default_factory).__name__)
        object.__setattr__(self, 'has_working_default_factory', has_working_default_factory)
        object.__setattr__(self, 'working_default_factory', working_default_factory)
        if not isinstance(working_default_factory_param_name, str):
            raise TypeError('WorkingDefaultFactoryParamName must be str, got ' + type(working_default_factory_param_name).__name__)
        object.__setattr__(self, 'working_default_factory_param_name', working_default_factory_param_name)
        object.__setattr__(self, 'working_default_factory_param_names', working_default_factory_param_names)
        object.__setattr__(self, 'tx_key_key', tx_key_key)
        if not isinstance(value_slot_name, str):
            raise TypeError('ValueSlotName must be str, got ' + type(value_slot_name).__name__)
        object.__setattr__(self, 'value_slot_name', value_slot_name)
        if not isinstance(current_slot_name, str):
            raise TypeError('CurrentSlotName must be str, got ' + type(current_slot_name).__name__)
        object.__setattr__(self, 'current_slot_name', current_slot_name)
        if not isinstance(working_slot_name, str):
            raise TypeError('WorkingSlotName must be str, got ' + type(working_slot_name).__name__)
        object.__setattr__(self, 'working_slot_name', working_slot_name)
        if not isinstance(staged_slot_name, str):
            raise TypeError('StagedSlotName must be str, got ' + type(staged_slot_name).__name__)
        object.__setattr__(self, 'staged_slot_name', staged_slot_name)
        if not isinstance(has_freeze, bool):
            raise TypeError('HasFreeze must be bool, got ' + type(has_freeze).__name__)
        object.__setattr__(self, 'has_freeze', has_freeze)
        object.__setattr__(self, 'freeze', freeze)
        if not isinstance(freeze_param_name, str):
            raise TypeError('FreezeParamName must be str, got ' + type(freeze_param_name).__name__)
        object.__setattr__(self, 'freeze_param_name', freeze_param_name)
        if not isinstance(has_thaw, bool):
            raise TypeError('HasThaw must be bool, got ' + type(has_thaw).__name__)
        object.__setattr__(self, 'has_thaw', has_thaw)
        object.__setattr__(self, 'thaw', thaw)
        if not isinstance(thaw_param_name, str):
            raise TypeError('ThawParamName must be str, got ' + type(thaw_param_name).__name__)
        object.__setattr__(self, 'thaw_param_name', thaw_param_name)
        if not isinstance(has_optional_none, bool):
            raise TypeError('HasOptionalNone must be bool, got ' + type(has_optional_none).__name__)
        object.__setattr__(self, 'has_optional_none', has_optional_none)

    def __setattr__(self, name, value):
        if name in ('field_id', 'field_owner', 'field_name', 'field_order', 'field_kind', 'binding_shape', 'annotation', 'init', 'has_default', 'default_value', 'default_value_param_name', 'has_default_factory', 'default_factory', 'default_factory_param_name', 'default_factory_param_names', 'has_working_default_factory', 'working_default_factory', 'working_default_factory_param_name', 'working_default_factory_param_names', 'tx_key_key', 'value_slot_name', 'current_slot_name', 'working_slot_name', 'staged_slot_name', 'has_freeze', 'freeze', 'freeze_param_name', 'has_thaw', 'thaw', 'thaw_param_name', 'has_optional_none'):
            raise AttributeError('InitVarField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('field_id=' + repr(self.field_id))
        pieces.append('field_owner=' + repr(self.field_owner))
        pieces.append('field_name=' + repr(self.field_name))
        pieces.append('field_order=' + repr(self.field_order))
        pieces.append('field_kind=' + repr(self.field_kind))
        pieces.append('binding_shape=' + repr(self.binding_shape))
        pieces.append('annotation=' + repr(self.annotation))
        pieces.append('init=' + repr(self.init))
        pieces.append('has_default=' + repr(self.has_default))
        pieces.append('default_value=' + repr(self.default_value))
        pieces.append('default_value_param_name=' + repr(self.default_value_param_name))
        pieces.append('has_default_factory=' + repr(self.has_default_factory))
        pieces.append('default_factory=' + repr(self.default_factory))
        pieces.append('default_factory_param_name=' + repr(self.default_factory_param_name))
        pieces.append('default_factory_param_names=' + repr(self.default_factory_param_names))
        pieces.append('has_working_default_factory=' + repr(self.has_working_default_factory))
        pieces.append('working_default_factory=' + repr(self.working_default_factory))
        pieces.append('working_default_factory_param_name=' + repr(self.working_default_factory_param_name))
        pieces.append('working_default_factory_param_names=' + repr(self.working_default_factory_param_names))
        pieces.append('tx_key_key=' + repr(self.tx_key_key))
        pieces.append('value_slot_name=' + repr(self.value_slot_name))
        pieces.append('current_slot_name=' + repr(self.current_slot_name))
        pieces.append('working_slot_name=' + repr(self.working_slot_name))
        pieces.append('staged_slot_name=' + repr(self.staged_slot_name))
        pieces.append('has_freeze=' + repr(self.has_freeze))
        pieces.append('freeze=' + repr(self.freeze))
        pieces.append('freeze_param_name=' + repr(self.freeze_param_name))
        pieces.append('has_thaw=' + repr(self.has_thaw))
        pieces.append('thaw=' + repr(self.thaw))
        pieces.append('thaw_param_name=' + repr(self.thaw_param_name))
        pieces.append('has_optional_none=' + repr(self.has_optional_none))
        return 'InitVarField' + '(' + ', '.join(pieces) + ')'
_InitVarFieldSpec.bind_record_class(InitVarField)

class ClassVarField:
    __slots__ = ('field_id', 'field_owner', 'field_name', 'field_order', 'field_kind', 'binding_shape', 'annotation', 'init', 'has_default', 'default_value', 'default_value_param_name', 'has_default_factory', 'default_factory', 'default_factory_param_name', 'default_factory_param_names', 'has_working_default_factory', 'working_default_factory', 'working_default_factory_param_name', 'working_default_factory_param_names', 'tx_key_key', 'value_slot_name', 'current_slot_name', 'working_slot_name', 'staged_slot_name', 'has_freeze', 'freeze', 'freeze_param_name', 'has_thaw', 'thaw', 'thaw_param_name', 'has_optional_none')
    __dds_record_spec__ = _ClassVarFieldSpec
    field_id: str
    field_owner: str
    field_name: str
    field_order: int
    field_kind: str
    binding_shape: str
    annotation: object
    init: bool
    has_default: bool
    default_value: object
    default_value_param_name: str
    has_default_factory: bool
    default_factory: object
    default_factory_param_name: str
    default_factory_param_names: object
    has_working_default_factory: bool
    working_default_factory: object
    working_default_factory_param_name: str
    working_default_factory_param_names: object
    tx_key_key: object
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

    def __init__(self, *, field_id: str, field_owner: str, field_name: str, field_order: int, field_kind: str='field', binding_shape: str='scalar', annotation: object=object, init: bool=True, has_default: bool=False, default_value: object=None, default_value_param_name: str='', has_default_factory: bool=False, default_factory: object=None, default_factory_param_name: str='', default_factory_param_names: object=(), has_working_default_factory: bool=False, working_default_factory: object=None, working_default_factory_param_name: str='', working_default_factory_param_names: object=(), tx_key_key: object=None, value_slot_name: str='', current_slot_name: str='', working_slot_name: str='', staged_slot_name: str='', has_freeze: bool=False, freeze: object=None, freeze_param_name: str='', has_thaw: bool=False, thaw: object=None, thaw_param_name: str='', has_optional_none: bool=False):
        if not isinstance(field_id, str):
            raise TypeError('FieldId must be str, got ' + type(field_id).__name__)
        object.__setattr__(self, 'field_id', field_id)
        if not isinstance(field_owner, str):
            raise TypeError('FieldOwner must be str, got ' + type(field_owner).__name__)
        object.__setattr__(self, 'field_owner', field_owner)
        if not isinstance(field_name, str):
            raise TypeError('FieldName must be str, got ' + type(field_name).__name__)
        object.__setattr__(self, 'field_name', field_name)
        if not isinstance(field_order, int):
            raise TypeError('FieldOrder must be int, got ' + type(field_order).__name__)
        object.__setattr__(self, 'field_order', field_order)
        if not isinstance(field_kind, str):
            raise TypeError('FieldKind must be str, got ' + type(field_kind).__name__)
        object.__setattr__(self, 'field_kind', field_kind)
        if not isinstance(binding_shape, str):
            raise TypeError('BindingShape must be str, got ' + type(binding_shape).__name__)
        object.__setattr__(self, 'binding_shape', binding_shape)
        object.__setattr__(self, 'annotation', annotation)
        if not isinstance(init, bool):
            raise TypeError('Init must be bool, got ' + type(init).__name__)
        object.__setattr__(self, 'init', init)
        if not isinstance(has_default, bool):
            raise TypeError('HasDefault must be bool, got ' + type(has_default).__name__)
        object.__setattr__(self, 'has_default', has_default)
        object.__setattr__(self, 'default_value', default_value)
        if not isinstance(default_value_param_name, str):
            raise TypeError('DefaultValueParamName must be str, got ' + type(default_value_param_name).__name__)
        object.__setattr__(self, 'default_value_param_name', default_value_param_name)
        if not isinstance(has_default_factory, bool):
            raise TypeError('HasDefaultFactory must be bool, got ' + type(has_default_factory).__name__)
        object.__setattr__(self, 'has_default_factory', has_default_factory)
        object.__setattr__(self, 'default_factory', default_factory)
        if not isinstance(default_factory_param_name, str):
            raise TypeError('DefaultFactoryParamName must be str, got ' + type(default_factory_param_name).__name__)
        object.__setattr__(self, 'default_factory_param_name', default_factory_param_name)
        object.__setattr__(self, 'default_factory_param_names', default_factory_param_names)
        if not isinstance(has_working_default_factory, bool):
            raise TypeError('HasWorkingDefaultFactory must be bool, got ' + type(has_working_default_factory).__name__)
        object.__setattr__(self, 'has_working_default_factory', has_working_default_factory)
        object.__setattr__(self, 'working_default_factory', working_default_factory)
        if not isinstance(working_default_factory_param_name, str):
            raise TypeError('WorkingDefaultFactoryParamName must be str, got ' + type(working_default_factory_param_name).__name__)
        object.__setattr__(self, 'working_default_factory_param_name', working_default_factory_param_name)
        object.__setattr__(self, 'working_default_factory_param_names', working_default_factory_param_names)
        object.__setattr__(self, 'tx_key_key', tx_key_key)
        if not isinstance(value_slot_name, str):
            raise TypeError('ValueSlotName must be str, got ' + type(value_slot_name).__name__)
        object.__setattr__(self, 'value_slot_name', value_slot_name)
        if not isinstance(current_slot_name, str):
            raise TypeError('CurrentSlotName must be str, got ' + type(current_slot_name).__name__)
        object.__setattr__(self, 'current_slot_name', current_slot_name)
        if not isinstance(working_slot_name, str):
            raise TypeError('WorkingSlotName must be str, got ' + type(working_slot_name).__name__)
        object.__setattr__(self, 'working_slot_name', working_slot_name)
        if not isinstance(staged_slot_name, str):
            raise TypeError('StagedSlotName must be str, got ' + type(staged_slot_name).__name__)
        object.__setattr__(self, 'staged_slot_name', staged_slot_name)
        if not isinstance(has_freeze, bool):
            raise TypeError('HasFreeze must be bool, got ' + type(has_freeze).__name__)
        object.__setattr__(self, 'has_freeze', has_freeze)
        object.__setattr__(self, 'freeze', freeze)
        if not isinstance(freeze_param_name, str):
            raise TypeError('FreezeParamName must be str, got ' + type(freeze_param_name).__name__)
        object.__setattr__(self, 'freeze_param_name', freeze_param_name)
        if not isinstance(has_thaw, bool):
            raise TypeError('HasThaw must be bool, got ' + type(has_thaw).__name__)
        object.__setattr__(self, 'has_thaw', has_thaw)
        object.__setattr__(self, 'thaw', thaw)
        if not isinstance(thaw_param_name, str):
            raise TypeError('ThawParamName must be str, got ' + type(thaw_param_name).__name__)
        object.__setattr__(self, 'thaw_param_name', thaw_param_name)
        if not isinstance(has_optional_none, bool):
            raise TypeError('HasOptionalNone must be bool, got ' + type(has_optional_none).__name__)
        object.__setattr__(self, 'has_optional_none', has_optional_none)

    def __setattr__(self, name, value):
        if name in ('field_id', 'field_owner', 'field_name', 'field_order', 'field_kind', 'binding_shape', 'annotation', 'init', 'has_default', 'default_value', 'default_value_param_name', 'has_default_factory', 'default_factory', 'default_factory_param_name', 'default_factory_param_names', 'has_working_default_factory', 'working_default_factory', 'working_default_factory_param_name', 'working_default_factory_param_names', 'tx_key_key', 'value_slot_name', 'current_slot_name', 'working_slot_name', 'staged_slot_name', 'has_freeze', 'freeze', 'freeze_param_name', 'has_thaw', 'thaw', 'thaw_param_name', 'has_optional_none'):
            raise AttributeError('ClassVarField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('field_id=' + repr(self.field_id))
        pieces.append('field_owner=' + repr(self.field_owner))
        pieces.append('field_name=' + repr(self.field_name))
        pieces.append('field_order=' + repr(self.field_order))
        pieces.append('field_kind=' + repr(self.field_kind))
        pieces.append('binding_shape=' + repr(self.binding_shape))
        pieces.append('annotation=' + repr(self.annotation))
        pieces.append('init=' + repr(self.init))
        pieces.append('has_default=' + repr(self.has_default))
        pieces.append('default_value=' + repr(self.default_value))
        pieces.append('default_value_param_name=' + repr(self.default_value_param_name))
        pieces.append('has_default_factory=' + repr(self.has_default_factory))
        pieces.append('default_factory=' + repr(self.default_factory))
        pieces.append('default_factory_param_name=' + repr(self.default_factory_param_name))
        pieces.append('default_factory_param_names=' + repr(self.default_factory_param_names))
        pieces.append('has_working_default_factory=' + repr(self.has_working_default_factory))
        pieces.append('working_default_factory=' + repr(self.working_default_factory))
        pieces.append('working_default_factory_param_name=' + repr(self.working_default_factory_param_name))
        pieces.append('working_default_factory_param_names=' + repr(self.working_default_factory_param_names))
        pieces.append('tx_key_key=' + repr(self.tx_key_key))
        pieces.append('value_slot_name=' + repr(self.value_slot_name))
        pieces.append('current_slot_name=' + repr(self.current_slot_name))
        pieces.append('working_slot_name=' + repr(self.working_slot_name))
        pieces.append('staged_slot_name=' + repr(self.staged_slot_name))
        pieces.append('has_freeze=' + repr(self.has_freeze))
        pieces.append('freeze=' + repr(self.freeze))
        pieces.append('freeze_param_name=' + repr(self.freeze_param_name))
        pieces.append('has_thaw=' + repr(self.has_thaw))
        pieces.append('thaw=' + repr(self.thaw))
        pieces.append('thaw_param_name=' + repr(self.thaw_param_name))
        pieces.append('has_optional_none=' + repr(self.has_optional_none))
        return 'ClassVarField' + '(' + ', '.join(pieces) + ')'
_ClassVarFieldSpec.bind_record_class(ClassVarField)

class TransactionalField:
    __slots__ = ('field_id', 'field_owner', 'field_name', 'field_order', 'tx_key_key')
    __dds_record_spec__ = _TransactionalFieldSpec
    field_id: str
    field_owner: str
    field_name: str
    field_order: int
    tx_key_key: object

    def __init__(self, *, field_id: str, field_owner: str, field_name: str, field_order: int, tx_key_key: object=None):
        if not isinstance(field_id, str):
            raise TypeError('FieldId must be str, got ' + type(field_id).__name__)
        object.__setattr__(self, 'field_id', field_id)
        if not isinstance(field_owner, str):
            raise TypeError('FieldOwner must be str, got ' + type(field_owner).__name__)
        object.__setattr__(self, 'field_owner', field_owner)
        if not isinstance(field_name, str):
            raise TypeError('FieldName must be str, got ' + type(field_name).__name__)
        object.__setattr__(self, 'field_name', field_name)
        if not isinstance(field_order, int):
            raise TypeError('FieldOrder must be int, got ' + type(field_order).__name__)
        object.__setattr__(self, 'field_order', field_order)
        object.__setattr__(self, 'tx_key_key', tx_key_key)

    def __setattr__(self, name, value):
        if name in ('field_id', 'field_owner', 'field_name', 'field_order', 'tx_key_key'):
            raise AttributeError('TransactionalField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('field_id=' + repr(self.field_id))
        pieces.append('field_owner=' + repr(self.field_owner))
        pieces.append('field_name=' + repr(self.field_name))
        pieces.append('field_order=' + repr(self.field_order))
        pieces.append('tx_key_key=' + repr(self.tx_key_key))
        return 'TransactionalField' + '(' + ', '.join(pieces) + ')'
_TransactionalFieldSpec.bind_record_class(TransactionalField)

class TxKey:
    __slots__ = ('tx_owner', 'tx_key_key', 'tx_index', 'tx_key_order', 'commit_order_key_function_name', 'requires_validation_function_name', 'validate_commit_function_name', 'before_commit_function_name', 'after_commit_function_name', 'after_rollback_function_name', 'prepare_commit_fields_function_name', 'apply_prepared_commit_fields_function_name', 'rollback_fields_function_name')
    __dds_record_spec__ = _TxKeySpec
    tx_owner: str
    tx_key_key: object
    tx_index: int
    tx_key_order: int
    commit_order_key_function_name: str
    requires_validation_function_name: str
    validate_commit_function_name: str
    before_commit_function_name: str
    after_commit_function_name: str
    after_rollback_function_name: str
    prepare_commit_fields_function_name: str
    apply_prepared_commit_fields_function_name: str
    rollback_fields_function_name: str

    def __init__(self, *, tx_owner: str='', tx_key_key: object=None, tx_index: int=0, tx_key_order: int=0, commit_order_key_function_name: str='', requires_validation_function_name: str='', validate_commit_function_name: str='', before_commit_function_name: str='', after_commit_function_name: str='', after_rollback_function_name: str='', prepare_commit_fields_function_name: str='', apply_prepared_commit_fields_function_name: str='', rollback_fields_function_name: str=''):
        if not isinstance(tx_owner, str):
            raise TypeError('TxOwner must be str, got ' + type(tx_owner).__name__)
        object.__setattr__(self, 'tx_owner', tx_owner)
        object.__setattr__(self, 'tx_key_key', tx_key_key)
        if not isinstance(tx_index, int):
            raise TypeError('TxIndex must be int, got ' + type(tx_index).__name__)
        object.__setattr__(self, 'tx_index', tx_index)
        if not isinstance(tx_key_order, int):
            raise TypeError('TxKeyOrder must be int, got ' + type(tx_key_order).__name__)
        object.__setattr__(self, 'tx_key_order', tx_key_order)
        if not isinstance(commit_order_key_function_name, str):
            raise TypeError('CommitOrderKeyFunctionName must be str, got ' + type(commit_order_key_function_name).__name__)
        object.__setattr__(self, 'commit_order_key_function_name', commit_order_key_function_name)
        if not isinstance(requires_validation_function_name, str):
            raise TypeError('RequiresValidationFunctionName must be str, got ' + type(requires_validation_function_name).__name__)
        object.__setattr__(self, 'requires_validation_function_name', requires_validation_function_name)
        if not isinstance(validate_commit_function_name, str):
            raise TypeError('ValidateCommitFunctionName must be str, got ' + type(validate_commit_function_name).__name__)
        object.__setattr__(self, 'validate_commit_function_name', validate_commit_function_name)
        if not isinstance(before_commit_function_name, str):
            raise TypeError('BeforeCommitFunctionName must be str, got ' + type(before_commit_function_name).__name__)
        object.__setattr__(self, 'before_commit_function_name', before_commit_function_name)
        if not isinstance(after_commit_function_name, str):
            raise TypeError('AfterCommitFunctionName must be str, got ' + type(after_commit_function_name).__name__)
        object.__setattr__(self, 'after_commit_function_name', after_commit_function_name)
        if not isinstance(after_rollback_function_name, str):
            raise TypeError('AfterRollbackFunctionName must be str, got ' + type(after_rollback_function_name).__name__)
        object.__setattr__(self, 'after_rollback_function_name', after_rollback_function_name)
        if not isinstance(prepare_commit_fields_function_name, str):
            raise TypeError('PrepareCommitFieldsFunctionName must be str, got ' + type(prepare_commit_fields_function_name).__name__)
        object.__setattr__(self, 'prepare_commit_fields_function_name', prepare_commit_fields_function_name)
        if not isinstance(apply_prepared_commit_fields_function_name, str):
            raise TypeError('ApplyPreparedCommitFieldsFunctionName must be str, got ' + type(apply_prepared_commit_fields_function_name).__name__)
        object.__setattr__(self, 'apply_prepared_commit_fields_function_name', apply_prepared_commit_fields_function_name)
        if not isinstance(rollback_fields_function_name, str):
            raise TypeError('RollbackFieldsFunctionName must be str, got ' + type(rollback_fields_function_name).__name__)
        object.__setattr__(self, 'rollback_fields_function_name', rollback_fields_function_name)

    def __setattr__(self, name, value):
        if name in ('tx_owner', 'tx_key_key', 'tx_index', 'tx_key_order', 'commit_order_key_function_name', 'requires_validation_function_name', 'validate_commit_function_name', 'before_commit_function_name', 'after_commit_function_name', 'after_rollback_function_name', 'prepare_commit_fields_function_name', 'apply_prepared_commit_fields_function_name', 'rollback_fields_function_name'):
            raise AttributeError('TxKey records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('tx_owner=' + repr(self.tx_owner))
        pieces.append('tx_key_key=' + repr(self.tx_key_key))
        pieces.append('tx_index=' + repr(self.tx_index))
        pieces.append('tx_key_order=' + repr(self.tx_key_order))
        pieces.append('commit_order_key_function_name=' + repr(self.commit_order_key_function_name))
        pieces.append('requires_validation_function_name=' + repr(self.requires_validation_function_name))
        pieces.append('validate_commit_function_name=' + repr(self.validate_commit_function_name))
        pieces.append('before_commit_function_name=' + repr(self.before_commit_function_name))
        pieces.append('after_commit_function_name=' + repr(self.after_commit_function_name))
        pieces.append('after_rollback_function_name=' + repr(self.after_rollback_function_name))
        pieces.append('prepare_commit_fields_function_name=' + repr(self.prepare_commit_fields_function_name))
        pieces.append('apply_prepared_commit_fields_function_name=' + repr(self.apply_prepared_commit_fields_function_name))
        pieces.append('rollback_fields_function_name=' + repr(self.rollback_fields_function_name))
        return 'TxKey' + '(' + ', '.join(pieces) + ')'
_TxKeySpec.bind_record_class(TxKey)

class IndexedTransactionalField:
    __slots__ = ('field_id', 'field_owner', 'field_name', 'field_order', 'tx_key_key', 'tx_index', 'current_slot_name', 'working_slot_name', 'staged_slot_name', 'has_freeze', 'freeze_param_name', 'has_thaw', 'thaw_param_name', 'has_optional_none')
    __dds_record_spec__ = _IndexedTransactionalFieldSpec
    field_id: str
    field_owner: str
    field_name: str
    field_order: int
    tx_key_key: object
    tx_index: int
    current_slot_name: str
    working_slot_name: str
    staged_slot_name: str
    has_freeze: bool
    freeze_param_name: str
    has_thaw: bool
    thaw_param_name: str
    has_optional_none: bool

    def __init__(self, *, field_id: str, field_owner: str, field_name: str, field_order: int, tx_key_key: object=None, tx_index: int=0, current_slot_name: str='', working_slot_name: str='', staged_slot_name: str='', has_freeze: bool=False, freeze_param_name: str='', has_thaw: bool=False, thaw_param_name: str='', has_optional_none: bool=False):
        if not isinstance(field_id, str):
            raise TypeError('FieldId must be str, got ' + type(field_id).__name__)
        object.__setattr__(self, 'field_id', field_id)
        if not isinstance(field_owner, str):
            raise TypeError('FieldOwner must be str, got ' + type(field_owner).__name__)
        object.__setattr__(self, 'field_owner', field_owner)
        if not isinstance(field_name, str):
            raise TypeError('FieldName must be str, got ' + type(field_name).__name__)
        object.__setattr__(self, 'field_name', field_name)
        if not isinstance(field_order, int):
            raise TypeError('FieldOrder must be int, got ' + type(field_order).__name__)
        object.__setattr__(self, 'field_order', field_order)
        object.__setattr__(self, 'tx_key_key', tx_key_key)
        if not isinstance(tx_index, int):
            raise TypeError('TxIndex must be int, got ' + type(tx_index).__name__)
        object.__setattr__(self, 'tx_index', tx_index)
        if not isinstance(current_slot_name, str):
            raise TypeError('CurrentSlotName must be str, got ' + type(current_slot_name).__name__)
        object.__setattr__(self, 'current_slot_name', current_slot_name)
        if not isinstance(working_slot_name, str):
            raise TypeError('WorkingSlotName must be str, got ' + type(working_slot_name).__name__)
        object.__setattr__(self, 'working_slot_name', working_slot_name)
        if not isinstance(staged_slot_name, str):
            raise TypeError('StagedSlotName must be str, got ' + type(staged_slot_name).__name__)
        object.__setattr__(self, 'staged_slot_name', staged_slot_name)
        if not isinstance(has_freeze, bool):
            raise TypeError('HasFreeze must be bool, got ' + type(has_freeze).__name__)
        object.__setattr__(self, 'has_freeze', has_freeze)
        if not isinstance(freeze_param_name, str):
            raise TypeError('FreezeParamName must be str, got ' + type(freeze_param_name).__name__)
        object.__setattr__(self, 'freeze_param_name', freeze_param_name)
        if not isinstance(has_thaw, bool):
            raise TypeError('HasThaw must be bool, got ' + type(has_thaw).__name__)
        object.__setattr__(self, 'has_thaw', has_thaw)
        if not isinstance(thaw_param_name, str):
            raise TypeError('ThawParamName must be str, got ' + type(thaw_param_name).__name__)
        object.__setattr__(self, 'thaw_param_name', thaw_param_name)
        if not isinstance(has_optional_none, bool):
            raise TypeError('HasOptionalNone must be bool, got ' + type(has_optional_none).__name__)
        object.__setattr__(self, 'has_optional_none', has_optional_none)

    def __setattr__(self, name, value):
        if name in ('field_id', 'field_owner', 'field_name', 'field_order', 'tx_key_key', 'tx_index', 'current_slot_name', 'working_slot_name', 'staged_slot_name', 'has_freeze', 'freeze_param_name', 'has_thaw', 'thaw_param_name', 'has_optional_none'):
            raise AttributeError('IndexedTransactionalField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('field_id=' + repr(self.field_id))
        pieces.append('field_owner=' + repr(self.field_owner))
        pieces.append('field_name=' + repr(self.field_name))
        pieces.append('field_order=' + repr(self.field_order))
        pieces.append('tx_key_key=' + repr(self.tx_key_key))
        pieces.append('tx_index=' + repr(self.tx_index))
        pieces.append('current_slot_name=' + repr(self.current_slot_name))
        pieces.append('working_slot_name=' + repr(self.working_slot_name))
        pieces.append('staged_slot_name=' + repr(self.staged_slot_name))
        pieces.append('has_freeze=' + repr(self.has_freeze))
        pieces.append('freeze_param_name=' + repr(self.freeze_param_name))
        pieces.append('has_thaw=' + repr(self.has_thaw))
        pieces.append('thaw_param_name=' + repr(self.thaw_param_name))
        pieces.append('has_optional_none=' + repr(self.has_optional_none))
        return 'IndexedTransactionalField' + '(' + ', '.join(pieces) + ')'
_IndexedTransactionalFieldSpec.bind_record_class(IndexedTransactionalField)

class ManagedField:
    __slots__ = ('field_id', 'field_owner', 'field_name', 'field_order', 'field_kind', 'binding_shape', 'annotation', 'init', 'has_default', 'default_value', 'default_value_param_name', 'has_default_factory', 'default_factory', 'default_factory_param_name', 'default_factory_param_names', 'has_working_default_factory', 'working_default_factory', 'working_default_factory_param_name', 'working_default_factory_param_names', 'tx_key_key', 'value_slot_name', 'current_slot_name', 'working_slot_name', 'staged_slot_name', 'has_freeze', 'freeze', 'freeze_param_name', 'has_thaw', 'thaw', 'thaw_param_name', 'has_optional_none')
    __dds_record_spec__ = _ManagedFieldSpec
    field_id: str
    field_owner: str
    field_name: str
    field_order: int
    field_kind: str
    binding_shape: str
    annotation: object
    init: bool
    has_default: bool
    default_value: object
    default_value_param_name: str
    has_default_factory: bool
    default_factory: object
    default_factory_param_name: str
    default_factory_param_names: object
    has_working_default_factory: bool
    working_default_factory: object
    working_default_factory_param_name: str
    working_default_factory_param_names: object
    tx_key_key: object
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

    def __init__(self, *, field_id: str, field_owner: str, field_name: str, field_order: int, field_kind: str='field', binding_shape: str='scalar', annotation: object=object, init: bool=True, has_default: bool=False, default_value: object=None, default_value_param_name: str='', has_default_factory: bool=False, default_factory: object=None, default_factory_param_name: str='', default_factory_param_names: object=(), has_working_default_factory: bool=False, working_default_factory: object=None, working_default_factory_param_name: str='', working_default_factory_param_names: object=(), tx_key_key: object=None, value_slot_name: str='', current_slot_name: str='', working_slot_name: str='', staged_slot_name: str='', has_freeze: bool=False, freeze: object=None, freeze_param_name: str='', has_thaw: bool=False, thaw: object=None, thaw_param_name: str='', has_optional_none: bool=False):
        if not isinstance(field_id, str):
            raise TypeError('FieldId must be str, got ' + type(field_id).__name__)
        object.__setattr__(self, 'field_id', field_id)
        if not isinstance(field_owner, str):
            raise TypeError('FieldOwner must be str, got ' + type(field_owner).__name__)
        object.__setattr__(self, 'field_owner', field_owner)
        if not isinstance(field_name, str):
            raise TypeError('FieldName must be str, got ' + type(field_name).__name__)
        object.__setattr__(self, 'field_name', field_name)
        if not isinstance(field_order, int):
            raise TypeError('FieldOrder must be int, got ' + type(field_order).__name__)
        object.__setattr__(self, 'field_order', field_order)
        if not isinstance(field_kind, str):
            raise TypeError('FieldKind must be str, got ' + type(field_kind).__name__)
        object.__setattr__(self, 'field_kind', field_kind)
        if not isinstance(binding_shape, str):
            raise TypeError('BindingShape must be str, got ' + type(binding_shape).__name__)
        object.__setattr__(self, 'binding_shape', binding_shape)
        object.__setattr__(self, 'annotation', annotation)
        if not isinstance(init, bool):
            raise TypeError('Init must be bool, got ' + type(init).__name__)
        object.__setattr__(self, 'init', init)
        if not isinstance(has_default, bool):
            raise TypeError('HasDefault must be bool, got ' + type(has_default).__name__)
        object.__setattr__(self, 'has_default', has_default)
        object.__setattr__(self, 'default_value', default_value)
        if not isinstance(default_value_param_name, str):
            raise TypeError('DefaultValueParamName must be str, got ' + type(default_value_param_name).__name__)
        object.__setattr__(self, 'default_value_param_name', default_value_param_name)
        if not isinstance(has_default_factory, bool):
            raise TypeError('HasDefaultFactory must be bool, got ' + type(has_default_factory).__name__)
        object.__setattr__(self, 'has_default_factory', has_default_factory)
        object.__setattr__(self, 'default_factory', default_factory)
        if not isinstance(default_factory_param_name, str):
            raise TypeError('DefaultFactoryParamName must be str, got ' + type(default_factory_param_name).__name__)
        object.__setattr__(self, 'default_factory_param_name', default_factory_param_name)
        object.__setattr__(self, 'default_factory_param_names', default_factory_param_names)
        if not isinstance(has_working_default_factory, bool):
            raise TypeError('HasWorkingDefaultFactory must be bool, got ' + type(has_working_default_factory).__name__)
        object.__setattr__(self, 'has_working_default_factory', has_working_default_factory)
        object.__setattr__(self, 'working_default_factory', working_default_factory)
        if not isinstance(working_default_factory_param_name, str):
            raise TypeError('WorkingDefaultFactoryParamName must be str, got ' + type(working_default_factory_param_name).__name__)
        object.__setattr__(self, 'working_default_factory_param_name', working_default_factory_param_name)
        object.__setattr__(self, 'working_default_factory_param_names', working_default_factory_param_names)
        object.__setattr__(self, 'tx_key_key', tx_key_key)
        if not isinstance(value_slot_name, str):
            raise TypeError('ValueSlotName must be str, got ' + type(value_slot_name).__name__)
        object.__setattr__(self, 'value_slot_name', value_slot_name)
        if not isinstance(current_slot_name, str):
            raise TypeError('CurrentSlotName must be str, got ' + type(current_slot_name).__name__)
        object.__setattr__(self, 'current_slot_name', current_slot_name)
        if not isinstance(working_slot_name, str):
            raise TypeError('WorkingSlotName must be str, got ' + type(working_slot_name).__name__)
        object.__setattr__(self, 'working_slot_name', working_slot_name)
        if not isinstance(staged_slot_name, str):
            raise TypeError('StagedSlotName must be str, got ' + type(staged_slot_name).__name__)
        object.__setattr__(self, 'staged_slot_name', staged_slot_name)
        if not isinstance(has_freeze, bool):
            raise TypeError('HasFreeze must be bool, got ' + type(has_freeze).__name__)
        object.__setattr__(self, 'has_freeze', has_freeze)
        object.__setattr__(self, 'freeze', freeze)
        if not isinstance(freeze_param_name, str):
            raise TypeError('FreezeParamName must be str, got ' + type(freeze_param_name).__name__)
        object.__setattr__(self, 'freeze_param_name', freeze_param_name)
        if not isinstance(has_thaw, bool):
            raise TypeError('HasThaw must be bool, got ' + type(has_thaw).__name__)
        object.__setattr__(self, 'has_thaw', has_thaw)
        object.__setattr__(self, 'thaw', thaw)
        if not isinstance(thaw_param_name, str):
            raise TypeError('ThawParamName must be str, got ' + type(thaw_param_name).__name__)
        object.__setattr__(self, 'thaw_param_name', thaw_param_name)
        if not isinstance(has_optional_none, bool):
            raise TypeError('HasOptionalNone must be bool, got ' + type(has_optional_none).__name__)
        object.__setattr__(self, 'has_optional_none', has_optional_none)

    def __setattr__(self, name, value):
        if name in ('field_id', 'field_owner', 'field_name', 'field_order', 'field_kind', 'binding_shape', 'annotation', 'init', 'has_default', 'default_value', 'default_value_param_name', 'has_default_factory', 'default_factory', 'default_factory_param_name', 'default_factory_param_names', 'has_working_default_factory', 'working_default_factory', 'working_default_factory_param_name', 'working_default_factory_param_names', 'tx_key_key', 'value_slot_name', 'current_slot_name', 'working_slot_name', 'staged_slot_name', 'has_freeze', 'freeze', 'freeze_param_name', 'has_thaw', 'thaw', 'thaw_param_name', 'has_optional_none'):
            raise AttributeError('ManagedField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('field_id=' + repr(self.field_id))
        pieces.append('field_owner=' + repr(self.field_owner))
        pieces.append('field_name=' + repr(self.field_name))
        pieces.append('field_order=' + repr(self.field_order))
        pieces.append('field_kind=' + repr(self.field_kind))
        pieces.append('binding_shape=' + repr(self.binding_shape))
        pieces.append('annotation=' + repr(self.annotation))
        pieces.append('init=' + repr(self.init))
        pieces.append('has_default=' + repr(self.has_default))
        pieces.append('default_value=' + repr(self.default_value))
        pieces.append('default_value_param_name=' + repr(self.default_value_param_name))
        pieces.append('has_default_factory=' + repr(self.has_default_factory))
        pieces.append('default_factory=' + repr(self.default_factory))
        pieces.append('default_factory_param_name=' + repr(self.default_factory_param_name))
        pieces.append('default_factory_param_names=' + repr(self.default_factory_param_names))
        pieces.append('has_working_default_factory=' + repr(self.has_working_default_factory))
        pieces.append('working_default_factory=' + repr(self.working_default_factory))
        pieces.append('working_default_factory_param_name=' + repr(self.working_default_factory_param_name))
        pieces.append('working_default_factory_param_names=' + repr(self.working_default_factory_param_names))
        pieces.append('tx_key_key=' + repr(self.tx_key_key))
        pieces.append('value_slot_name=' + repr(self.value_slot_name))
        pieces.append('current_slot_name=' + repr(self.current_slot_name))
        pieces.append('working_slot_name=' + repr(self.working_slot_name))
        pieces.append('staged_slot_name=' + repr(self.staged_slot_name))
        pieces.append('has_freeze=' + repr(self.has_freeze))
        pieces.append('freeze=' + repr(self.freeze))
        pieces.append('freeze_param_name=' + repr(self.freeze_param_name))
        pieces.append('has_thaw=' + repr(self.has_thaw))
        pieces.append('thaw=' + repr(self.thaw))
        pieces.append('thaw_param_name=' + repr(self.thaw_param_name))
        pieces.append('has_optional_none=' + repr(self.has_optional_none))
        return 'ManagedField' + '(' + ', '.join(pieces) + ')'
_ManagedFieldSpec.bind_record_class(ManagedField)

class DefaultFactoryDependency:
    __slots__ = ('dependency_owner', 'consumer_field_id', 'consumer_field_name', 'consumer_field_kind', 'consumer_field_order', 'provider_name', 'provider_field_id', 'provider_field_kind', 'provider_init', 'provider_has_default', 'provider_has_default_factory', 'param_name', 'param_order', 'consumer_eval_order')
    __dds_record_spec__ = _DefaultFactoryDependencySpec
    dependency_owner: str
    consumer_field_id: str
    consumer_field_name: str
    consumer_field_kind: str
    consumer_field_order: int
    provider_name: str
    provider_field_id: str
    provider_field_kind: str
    provider_init: bool
    provider_has_default: bool
    provider_has_default_factory: bool
    param_name: str
    param_order: int
    consumer_eval_order: int

    def __init__(self, *, dependency_owner: str, consumer_field_id: str, consumer_field_name: str='', consumer_field_kind: str='', consumer_field_order: int=0, provider_name: str, provider_field_id: str='', provider_field_kind: str='', provider_init: bool=True, provider_has_default: bool=False, provider_has_default_factory: bool=False, param_name: str, param_order: int=0, consumer_eval_order: int=0):
        if not isinstance(dependency_owner, str):
            raise TypeError('DependencyOwner must be str, got ' + type(dependency_owner).__name__)
        object.__setattr__(self, 'dependency_owner', dependency_owner)
        if not isinstance(consumer_field_id, str):
            raise TypeError('ConsumerFieldId must be str, got ' + type(consumer_field_id).__name__)
        object.__setattr__(self, 'consumer_field_id', consumer_field_id)
        if not isinstance(consumer_field_name, str):
            raise TypeError('ConsumerFieldName must be str, got ' + type(consumer_field_name).__name__)
        object.__setattr__(self, 'consumer_field_name', consumer_field_name)
        if not isinstance(consumer_field_kind, str):
            raise TypeError('ConsumerFieldKind must be str, got ' + type(consumer_field_kind).__name__)
        object.__setattr__(self, 'consumer_field_kind', consumer_field_kind)
        if not isinstance(consumer_field_order, int):
            raise TypeError('ConsumerFieldOrder must be int, got ' + type(consumer_field_order).__name__)
        object.__setattr__(self, 'consumer_field_order', consumer_field_order)
        if not isinstance(provider_name, str):
            raise TypeError('ProviderName must be str, got ' + type(provider_name).__name__)
        object.__setattr__(self, 'provider_name', provider_name)
        if not isinstance(provider_field_id, str):
            raise TypeError('ProviderFieldId must be str, got ' + type(provider_field_id).__name__)
        object.__setattr__(self, 'provider_field_id', provider_field_id)
        if not isinstance(provider_field_kind, str):
            raise TypeError('ProviderFieldKind must be str, got ' + type(provider_field_kind).__name__)
        object.__setattr__(self, 'provider_field_kind', provider_field_kind)
        if not isinstance(provider_init, bool):
            raise TypeError('ProviderInit must be bool, got ' + type(provider_init).__name__)
        object.__setattr__(self, 'provider_init', provider_init)
        if not isinstance(provider_has_default, bool):
            raise TypeError('ProviderHasDefault must be bool, got ' + type(provider_has_default).__name__)
        object.__setattr__(self, 'provider_has_default', provider_has_default)
        if not isinstance(provider_has_default_factory, bool):
            raise TypeError('ProviderHasDefaultFactory must be bool, got ' + type(provider_has_default_factory).__name__)
        object.__setattr__(self, 'provider_has_default_factory', provider_has_default_factory)
        if not isinstance(param_name, str):
            raise TypeError('ParamName must be str, got ' + type(param_name).__name__)
        object.__setattr__(self, 'param_name', param_name)
        if not isinstance(param_order, int):
            raise TypeError('ParamOrder must be int, got ' + type(param_order).__name__)
        object.__setattr__(self, 'param_order', param_order)
        if not isinstance(consumer_eval_order, int):
            raise TypeError('ConsumerEvalOrder must be int, got ' + type(consumer_eval_order).__name__)
        object.__setattr__(self, 'consumer_eval_order', consumer_eval_order)

    def __setattr__(self, name, value):
        if name in ('dependency_owner', 'consumer_field_id', 'consumer_field_name', 'consumer_field_kind', 'consumer_field_order', 'provider_name', 'provider_field_id', 'provider_field_kind', 'provider_init', 'provider_has_default', 'provider_has_default_factory', 'param_name', 'param_order', 'consumer_eval_order'):
            raise AttributeError('DefaultFactoryDependency records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('dependency_owner=' + repr(self.dependency_owner))
        pieces.append('consumer_field_id=' + repr(self.consumer_field_id))
        pieces.append('consumer_field_name=' + repr(self.consumer_field_name))
        pieces.append('consumer_field_kind=' + repr(self.consumer_field_kind))
        pieces.append('consumer_field_order=' + repr(self.consumer_field_order))
        pieces.append('provider_name=' + repr(self.provider_name))
        pieces.append('provider_field_id=' + repr(self.provider_field_id))
        pieces.append('provider_field_kind=' + repr(self.provider_field_kind))
        pieces.append('provider_init=' + repr(self.provider_init))
        pieces.append('provider_has_default=' + repr(self.provider_has_default))
        pieces.append('provider_has_default_factory=' + repr(self.provider_has_default_factory))
        pieces.append('param_name=' + repr(self.param_name))
        pieces.append('param_order=' + repr(self.param_order))
        pieces.append('consumer_eval_order=' + repr(self.consumer_eval_order))
        return 'DefaultFactoryDependency' + '(' + ', '.join(pieces) + ')'
_DefaultFactoryDependencySpec.bind_record_class(DefaultFactoryDependency)

class DefaultFactoryEvaluationStep:
    __slots__ = ('eval_step_id', 'eval_owner', 'eval_field_id', 'eval_field_name', 'eval_field_kind', 'eval_binding_shape', 'eval_init', 'eval_state_slot_name', 'eval_default_factory_param_name', 'eval_order', 'eval_statement_order')
    __dds_record_spec__ = _DefaultFactoryEvaluationStepSpec
    eval_step_id: str
    eval_owner: str
    eval_field_id: str
    eval_field_name: str
    eval_field_kind: str
    eval_binding_shape: str
    eval_init: bool
    eval_state_slot_name: str
    eval_default_factory_param_name: str
    eval_order: int
    eval_statement_order: int

    def __init__(self, *, eval_step_id: str, eval_owner: str, eval_field_id: str, eval_field_name: str, eval_field_kind: str='', eval_binding_shape: str='scalar', eval_init: bool=True, eval_state_slot_name: str='', eval_default_factory_param_name: str='', eval_order: int=0, eval_statement_order: int=0):
        if not isinstance(eval_step_id, str):
            raise TypeError('EvalStepId must be str, got ' + type(eval_step_id).__name__)
        object.__setattr__(self, 'eval_step_id', eval_step_id)
        if not isinstance(eval_owner, str):
            raise TypeError('EvalOwner must be str, got ' + type(eval_owner).__name__)
        object.__setattr__(self, 'eval_owner', eval_owner)
        if not isinstance(eval_field_id, str):
            raise TypeError('EvalFieldId must be str, got ' + type(eval_field_id).__name__)
        object.__setattr__(self, 'eval_field_id', eval_field_id)
        if not isinstance(eval_field_name, str):
            raise TypeError('EvalFieldName must be str, got ' + type(eval_field_name).__name__)
        object.__setattr__(self, 'eval_field_name', eval_field_name)
        if not isinstance(eval_field_kind, str):
            raise TypeError('EvalFieldKind must be str, got ' + type(eval_field_kind).__name__)
        object.__setattr__(self, 'eval_field_kind', eval_field_kind)
        if not isinstance(eval_binding_shape, str):
            raise TypeError('EvalBindingShape must be str, got ' + type(eval_binding_shape).__name__)
        object.__setattr__(self, 'eval_binding_shape', eval_binding_shape)
        if not isinstance(eval_init, bool):
            raise TypeError('EvalInit must be bool, got ' + type(eval_init).__name__)
        object.__setattr__(self, 'eval_init', eval_init)
        if not isinstance(eval_state_slot_name, str):
            raise TypeError('EvalStateSlotName must be str, got ' + type(eval_state_slot_name).__name__)
        object.__setattr__(self, 'eval_state_slot_name', eval_state_slot_name)
        if not isinstance(eval_default_factory_param_name, str):
            raise TypeError('EvalDefaultFactoryParamName must be str, got ' + type(eval_default_factory_param_name).__name__)
        object.__setattr__(self, 'eval_default_factory_param_name', eval_default_factory_param_name)
        if not isinstance(eval_order, int):
            raise TypeError('EvalOrder must be int, got ' + type(eval_order).__name__)
        object.__setattr__(self, 'eval_order', eval_order)
        if not isinstance(eval_statement_order, int):
            raise TypeError('EvalStatementOrder must be int, got ' + type(eval_statement_order).__name__)
        object.__setattr__(self, 'eval_statement_order', eval_statement_order)

    def __setattr__(self, name, value):
        if name in ('eval_step_id', 'eval_owner', 'eval_field_id', 'eval_field_name', 'eval_field_kind', 'eval_binding_shape', 'eval_init', 'eval_state_slot_name', 'eval_default_factory_param_name', 'eval_order', 'eval_statement_order'):
            raise AttributeError('DefaultFactoryEvaluationStep records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('eval_step_id=' + repr(self.eval_step_id))
        pieces.append('eval_owner=' + repr(self.eval_owner))
        pieces.append('eval_field_id=' + repr(self.eval_field_id))
        pieces.append('eval_field_name=' + repr(self.eval_field_name))
        pieces.append('eval_field_kind=' + repr(self.eval_field_kind))
        pieces.append('eval_binding_shape=' + repr(self.eval_binding_shape))
        pieces.append('eval_init=' + repr(self.eval_init))
        pieces.append('eval_state_slot_name=' + repr(self.eval_state_slot_name))
        pieces.append('eval_default_factory_param_name=' + repr(self.eval_default_factory_param_name))
        pieces.append('eval_order=' + repr(self.eval_order))
        pieces.append('eval_statement_order=' + repr(self.eval_statement_order))
        return 'DefaultFactoryEvaluationStep' + '(' + ', '.join(pieces) + ')'
_DefaultFactoryEvaluationStepSpec.bind_record_class(DefaultFactoryEvaluationStep)

class DefaultFactoryDiagnostic:
    __slots__ = ('diagnostic_id', 'diagnostic_owner', 'diagnostic_field_id', 'diagnostic_message')
    __dds_record_spec__ = _DefaultFactoryDiagnosticSpec
    diagnostic_id: str
    diagnostic_owner: str
    diagnostic_field_id: str
    diagnostic_message: str

    def __init__(self, *, diagnostic_id: str, diagnostic_owner: str, diagnostic_field_id: str='', diagnostic_message: str):
        if not isinstance(diagnostic_id, str):
            raise TypeError('DiagnosticId must be str, got ' + type(diagnostic_id).__name__)
        object.__setattr__(self, 'diagnostic_id', diagnostic_id)
        if not isinstance(diagnostic_owner, str):
            raise TypeError('DiagnosticOwner must be str, got ' + type(diagnostic_owner).__name__)
        object.__setattr__(self, 'diagnostic_owner', diagnostic_owner)
        if not isinstance(diagnostic_field_id, str):
            raise TypeError('DiagnosticFieldId must be str, got ' + type(diagnostic_field_id).__name__)
        object.__setattr__(self, 'diagnostic_field_id', diagnostic_field_id)
        if not isinstance(diagnostic_message, str):
            raise TypeError('DiagnosticMessage must be str, got ' + type(diagnostic_message).__name__)
        object.__setattr__(self, 'diagnostic_message', diagnostic_message)

    def __setattr__(self, name, value):
        if name in ('diagnostic_id', 'diagnostic_owner', 'diagnostic_field_id', 'diagnostic_message'):
            raise AttributeError('DefaultFactoryDiagnostic records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('diagnostic_id=' + repr(self.diagnostic_id))
        pieces.append('diagnostic_owner=' + repr(self.diagnostic_owner))
        pieces.append('diagnostic_field_id=' + repr(self.diagnostic_field_id))
        pieces.append('diagnostic_message=' + repr(self.diagnostic_message))
        return 'DefaultFactoryDiagnostic' + '(' + ', '.join(pieces) + ')'
_DefaultFactoryDiagnosticSpec.bind_record_class(DefaultFactoryDiagnostic)

class IndexedTransientField:
    __slots__ = ('field_id', 'field_owner', 'field_name', 'field_order', 'tx_key_key', 'tx_index', 'current_slot_name', 'working_slot_name', 'has_working_default_factory', 'working_default_factory_param_name')
    __dds_record_spec__ = _IndexedTransientFieldSpec
    field_id: str
    field_owner: str
    field_name: str
    field_order: int
    tx_key_key: object
    tx_index: int
    current_slot_name: str
    working_slot_name: str
    has_working_default_factory: bool
    working_default_factory_param_name: str

    def __init__(self, *, field_id: str, field_owner: str, field_name: str, field_order: int, tx_key_key: object=None, tx_index: int=0, current_slot_name: str='', working_slot_name: str='', has_working_default_factory: bool=False, working_default_factory_param_name: str=''):
        if not isinstance(field_id, str):
            raise TypeError('FieldId must be str, got ' + type(field_id).__name__)
        object.__setattr__(self, 'field_id', field_id)
        if not isinstance(field_owner, str):
            raise TypeError('FieldOwner must be str, got ' + type(field_owner).__name__)
        object.__setattr__(self, 'field_owner', field_owner)
        if not isinstance(field_name, str):
            raise TypeError('FieldName must be str, got ' + type(field_name).__name__)
        object.__setattr__(self, 'field_name', field_name)
        if not isinstance(field_order, int):
            raise TypeError('FieldOrder must be int, got ' + type(field_order).__name__)
        object.__setattr__(self, 'field_order', field_order)
        object.__setattr__(self, 'tx_key_key', tx_key_key)
        if not isinstance(tx_index, int):
            raise TypeError('TxIndex must be int, got ' + type(tx_index).__name__)
        object.__setattr__(self, 'tx_index', tx_index)
        if not isinstance(current_slot_name, str):
            raise TypeError('CurrentSlotName must be str, got ' + type(current_slot_name).__name__)
        object.__setattr__(self, 'current_slot_name', current_slot_name)
        if not isinstance(working_slot_name, str):
            raise TypeError('WorkingSlotName must be str, got ' + type(working_slot_name).__name__)
        object.__setattr__(self, 'working_slot_name', working_slot_name)
        if not isinstance(has_working_default_factory, bool):
            raise TypeError('HasWorkingDefaultFactory must be bool, got ' + type(has_working_default_factory).__name__)
        object.__setattr__(self, 'has_working_default_factory', has_working_default_factory)
        if not isinstance(working_default_factory_param_name, str):
            raise TypeError('WorkingDefaultFactoryParamName must be str, got ' + type(working_default_factory_param_name).__name__)
        object.__setattr__(self, 'working_default_factory_param_name', working_default_factory_param_name)

    def __setattr__(self, name, value):
        if name in ('field_id', 'field_owner', 'field_name', 'field_order', 'tx_key_key', 'tx_index', 'current_slot_name', 'working_slot_name', 'has_working_default_factory', 'working_default_factory_param_name'):
            raise AttributeError('IndexedTransientField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('field_id=' + repr(self.field_id))
        pieces.append('field_owner=' + repr(self.field_owner))
        pieces.append('field_name=' + repr(self.field_name))
        pieces.append('field_order=' + repr(self.field_order))
        pieces.append('tx_key_key=' + repr(self.tx_key_key))
        pieces.append('tx_index=' + repr(self.tx_index))
        pieces.append('current_slot_name=' + repr(self.current_slot_name))
        pieces.append('working_slot_name=' + repr(self.working_slot_name))
        pieces.append('has_working_default_factory=' + repr(self.has_working_default_factory))
        pieces.append('working_default_factory_param_name=' + repr(self.working_default_factory_param_name))
        return 'IndexedTransientField' + '(' + ', '.join(pieces) + ')'
_IndexedTransientFieldSpec.bind_record_class(IndexedTransientField)

class RetainedInitVar:
    __slots__ = ('field_id', 'field_owner', 'field_name', 'field_order', 'retained_slot_name', 'retain_order')
    __dds_record_spec__ = _RetainedInitVarSpec
    field_id: str
    field_owner: str
    field_name: str
    field_order: int
    retained_slot_name: str
    retain_order: int

    def __init__(self, *, field_id: str, field_owner: str, field_name: str, field_order: int, retained_slot_name: str='', retain_order: int=0):
        if not isinstance(field_id, str):
            raise TypeError('FieldId must be str, got ' + type(field_id).__name__)
        object.__setattr__(self, 'field_id', field_id)
        if not isinstance(field_owner, str):
            raise TypeError('FieldOwner must be str, got ' + type(field_owner).__name__)
        object.__setattr__(self, 'field_owner', field_owner)
        if not isinstance(field_name, str):
            raise TypeError('FieldName must be str, got ' + type(field_name).__name__)
        object.__setattr__(self, 'field_name', field_name)
        if not isinstance(field_order, int):
            raise TypeError('FieldOrder must be int, got ' + type(field_order).__name__)
        object.__setattr__(self, 'field_order', field_order)
        if not isinstance(retained_slot_name, str):
            raise TypeError('RetainedSlotName must be str, got ' + type(retained_slot_name).__name__)
        object.__setattr__(self, 'retained_slot_name', retained_slot_name)
        if not isinstance(retain_order, int):
            raise TypeError('RetainOrder must be int, got ' + type(retain_order).__name__)
        object.__setattr__(self, 'retain_order', retain_order)

    def __setattr__(self, name, value):
        if name in ('field_id', 'field_owner', 'field_name', 'field_order', 'retained_slot_name', 'retain_order'):
            raise AttributeError('RetainedInitVar records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('field_id=' + repr(self.field_id))
        pieces.append('field_owner=' + repr(self.field_owner))
        pieces.append('field_name=' + repr(self.field_name))
        pieces.append('field_order=' + repr(self.field_order))
        pieces.append('retained_slot_name=' + repr(self.retained_slot_name))
        pieces.append('retain_order=' + repr(self.retain_order))
        return 'RetainedInitVar' + '(' + ', '.join(pieces) + ')'
_RetainedInitVarSpec.bind_record_class(RetainedInitVar)

class TransientWorkingFactoryArg:
    __slots__ = ('working_factory_arg_id', 'working_factory_arg_owner', 'working_factory_consumer_field_id', 'working_factory_consumer_field_order', 'param_name', 'param_order', 'provider_name', 'working_factory_arg_kind', 'retained_slot_name')
    __dds_record_spec__ = _TransientWorkingFactoryArgSpec
    working_factory_arg_id: str
    working_factory_arg_owner: str
    working_factory_consumer_field_id: str
    working_factory_consumer_field_order: int
    param_name: str
    param_order: int
    provider_name: str
    working_factory_arg_kind: str
    retained_slot_name: str

    def __init__(self, *, working_factory_arg_id: str, working_factory_arg_owner: str, working_factory_consumer_field_id: str, working_factory_consumer_field_order: int=0, param_name: str, param_order: int=0, provider_name: str, working_factory_arg_kind: str='', retained_slot_name: str=''):
        if not isinstance(working_factory_arg_id, str):
            raise TypeError('WorkingFactoryArgId must be str, got ' + type(working_factory_arg_id).__name__)
        object.__setattr__(self, 'working_factory_arg_id', working_factory_arg_id)
        if not isinstance(working_factory_arg_owner, str):
            raise TypeError('WorkingFactoryArgOwner must be str, got ' + type(working_factory_arg_owner).__name__)
        object.__setattr__(self, 'working_factory_arg_owner', working_factory_arg_owner)
        if not isinstance(working_factory_consumer_field_id, str):
            raise TypeError('WorkingFactoryConsumerFieldId must be str, got ' + type(working_factory_consumer_field_id).__name__)
        object.__setattr__(self, 'working_factory_consumer_field_id', working_factory_consumer_field_id)
        if not isinstance(working_factory_consumer_field_order, int):
            raise TypeError('WorkingFactoryConsumerFieldOrder must be int, got ' + type(working_factory_consumer_field_order).__name__)
        object.__setattr__(self, 'working_factory_consumer_field_order', working_factory_consumer_field_order)
        if not isinstance(param_name, str):
            raise TypeError('ParamName must be str, got ' + type(param_name).__name__)
        object.__setattr__(self, 'param_name', param_name)
        if not isinstance(param_order, int):
            raise TypeError('ParamOrder must be int, got ' + type(param_order).__name__)
        object.__setattr__(self, 'param_order', param_order)
        if not isinstance(provider_name, str):
            raise TypeError('ProviderName must be str, got ' + type(provider_name).__name__)
        object.__setattr__(self, 'provider_name', provider_name)
        if not isinstance(working_factory_arg_kind, str):
            raise TypeError('WorkingFactoryArgKind must be str, got ' + type(working_factory_arg_kind).__name__)
        object.__setattr__(self, 'working_factory_arg_kind', working_factory_arg_kind)
        if not isinstance(retained_slot_name, str):
            raise TypeError('RetainedSlotName must be str, got ' + type(retained_slot_name).__name__)
        object.__setattr__(self, 'retained_slot_name', retained_slot_name)

    def __setattr__(self, name, value):
        if name in ('working_factory_arg_id', 'working_factory_arg_owner', 'working_factory_consumer_field_id', 'working_factory_consumer_field_order', 'param_name', 'param_order', 'provider_name', 'working_factory_arg_kind', 'retained_slot_name'):
            raise AttributeError('TransientWorkingFactoryArg records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('working_factory_arg_id=' + repr(self.working_factory_arg_id))
        pieces.append('working_factory_arg_owner=' + repr(self.working_factory_arg_owner))
        pieces.append('working_factory_consumer_field_id=' + repr(self.working_factory_consumer_field_id))
        pieces.append('working_factory_consumer_field_order=' + repr(self.working_factory_consumer_field_order))
        pieces.append('param_name=' + repr(self.param_name))
        pieces.append('param_order=' + repr(self.param_order))
        pieces.append('provider_name=' + repr(self.provider_name))
        pieces.append('working_factory_arg_kind=' + repr(self.working_factory_arg_kind))
        pieces.append('retained_slot_name=' + repr(self.retained_slot_name))
        return 'TransientWorkingFactoryArg' + '(' + ', '.join(pieces) + ')'
_TransientWorkingFactoryArgSpec.bind_record_class(TransientWorkingFactoryArg)

class TransientField:
    __slots__ = ('field_id', 'field_owner', 'field_name', 'field_order', 'field_kind', 'binding_shape', 'annotation', 'init', 'has_default', 'default_value', 'default_value_param_name', 'has_default_factory', 'default_factory', 'default_factory_param_name', 'default_factory_param_names', 'has_working_default_factory', 'working_default_factory', 'working_default_factory_param_name', 'working_default_factory_param_names', 'tx_key_key', 'value_slot_name', 'current_slot_name', 'working_slot_name', 'staged_slot_name', 'has_freeze', 'freeze', 'freeze_param_name', 'has_thaw', 'thaw', 'thaw_param_name', 'has_optional_none')
    __dds_record_spec__ = _TransientFieldSpec
    field_id: str
    field_owner: str
    field_name: str
    field_order: int
    field_kind: str
    binding_shape: str
    annotation: object
    init: bool
    has_default: bool
    default_value: object
    default_value_param_name: str
    has_default_factory: bool
    default_factory: object
    default_factory_param_name: str
    default_factory_param_names: object
    has_working_default_factory: bool
    working_default_factory: object
    working_default_factory_param_name: str
    working_default_factory_param_names: object
    tx_key_key: object
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

    def __init__(self, *, field_id: str, field_owner: str, field_name: str, field_order: int, field_kind: str='field', binding_shape: str='scalar', annotation: object=object, init: bool=True, has_default: bool=False, default_value: object=None, default_value_param_name: str='', has_default_factory: bool=False, default_factory: object=None, default_factory_param_name: str='', default_factory_param_names: object=(), has_working_default_factory: bool=False, working_default_factory: object=None, working_default_factory_param_name: str='', working_default_factory_param_names: object=(), tx_key_key: object=None, value_slot_name: str='', current_slot_name: str='', working_slot_name: str='', staged_slot_name: str='', has_freeze: bool=False, freeze: object=None, freeze_param_name: str='', has_thaw: bool=False, thaw: object=None, thaw_param_name: str='', has_optional_none: bool=False):
        if not isinstance(field_id, str):
            raise TypeError('FieldId must be str, got ' + type(field_id).__name__)
        object.__setattr__(self, 'field_id', field_id)
        if not isinstance(field_owner, str):
            raise TypeError('FieldOwner must be str, got ' + type(field_owner).__name__)
        object.__setattr__(self, 'field_owner', field_owner)
        if not isinstance(field_name, str):
            raise TypeError('FieldName must be str, got ' + type(field_name).__name__)
        object.__setattr__(self, 'field_name', field_name)
        if not isinstance(field_order, int):
            raise TypeError('FieldOrder must be int, got ' + type(field_order).__name__)
        object.__setattr__(self, 'field_order', field_order)
        if not isinstance(field_kind, str):
            raise TypeError('FieldKind must be str, got ' + type(field_kind).__name__)
        object.__setattr__(self, 'field_kind', field_kind)
        if not isinstance(binding_shape, str):
            raise TypeError('BindingShape must be str, got ' + type(binding_shape).__name__)
        object.__setattr__(self, 'binding_shape', binding_shape)
        object.__setattr__(self, 'annotation', annotation)
        if not isinstance(init, bool):
            raise TypeError('Init must be bool, got ' + type(init).__name__)
        object.__setattr__(self, 'init', init)
        if not isinstance(has_default, bool):
            raise TypeError('HasDefault must be bool, got ' + type(has_default).__name__)
        object.__setattr__(self, 'has_default', has_default)
        object.__setattr__(self, 'default_value', default_value)
        if not isinstance(default_value_param_name, str):
            raise TypeError('DefaultValueParamName must be str, got ' + type(default_value_param_name).__name__)
        object.__setattr__(self, 'default_value_param_name', default_value_param_name)
        if not isinstance(has_default_factory, bool):
            raise TypeError('HasDefaultFactory must be bool, got ' + type(has_default_factory).__name__)
        object.__setattr__(self, 'has_default_factory', has_default_factory)
        object.__setattr__(self, 'default_factory', default_factory)
        if not isinstance(default_factory_param_name, str):
            raise TypeError('DefaultFactoryParamName must be str, got ' + type(default_factory_param_name).__name__)
        object.__setattr__(self, 'default_factory_param_name', default_factory_param_name)
        object.__setattr__(self, 'default_factory_param_names', default_factory_param_names)
        if not isinstance(has_working_default_factory, bool):
            raise TypeError('HasWorkingDefaultFactory must be bool, got ' + type(has_working_default_factory).__name__)
        object.__setattr__(self, 'has_working_default_factory', has_working_default_factory)
        object.__setattr__(self, 'working_default_factory', working_default_factory)
        if not isinstance(working_default_factory_param_name, str):
            raise TypeError('WorkingDefaultFactoryParamName must be str, got ' + type(working_default_factory_param_name).__name__)
        object.__setattr__(self, 'working_default_factory_param_name', working_default_factory_param_name)
        object.__setattr__(self, 'working_default_factory_param_names', working_default_factory_param_names)
        object.__setattr__(self, 'tx_key_key', tx_key_key)
        if not isinstance(value_slot_name, str):
            raise TypeError('ValueSlotName must be str, got ' + type(value_slot_name).__name__)
        object.__setattr__(self, 'value_slot_name', value_slot_name)
        if not isinstance(current_slot_name, str):
            raise TypeError('CurrentSlotName must be str, got ' + type(current_slot_name).__name__)
        object.__setattr__(self, 'current_slot_name', current_slot_name)
        if not isinstance(working_slot_name, str):
            raise TypeError('WorkingSlotName must be str, got ' + type(working_slot_name).__name__)
        object.__setattr__(self, 'working_slot_name', working_slot_name)
        if not isinstance(staged_slot_name, str):
            raise TypeError('StagedSlotName must be str, got ' + type(staged_slot_name).__name__)
        object.__setattr__(self, 'staged_slot_name', staged_slot_name)
        if not isinstance(has_freeze, bool):
            raise TypeError('HasFreeze must be bool, got ' + type(has_freeze).__name__)
        object.__setattr__(self, 'has_freeze', has_freeze)
        object.__setattr__(self, 'freeze', freeze)
        if not isinstance(freeze_param_name, str):
            raise TypeError('FreezeParamName must be str, got ' + type(freeze_param_name).__name__)
        object.__setattr__(self, 'freeze_param_name', freeze_param_name)
        if not isinstance(has_thaw, bool):
            raise TypeError('HasThaw must be bool, got ' + type(has_thaw).__name__)
        object.__setattr__(self, 'has_thaw', has_thaw)
        object.__setattr__(self, 'thaw', thaw)
        if not isinstance(thaw_param_name, str):
            raise TypeError('ThawParamName must be str, got ' + type(thaw_param_name).__name__)
        object.__setattr__(self, 'thaw_param_name', thaw_param_name)
        if not isinstance(has_optional_none, bool):
            raise TypeError('HasOptionalNone must be bool, got ' + type(has_optional_none).__name__)
        object.__setattr__(self, 'has_optional_none', has_optional_none)

    def __setattr__(self, name, value):
        if name in ('field_id', 'field_owner', 'field_name', 'field_order', 'field_kind', 'binding_shape', 'annotation', 'init', 'has_default', 'default_value', 'default_value_param_name', 'has_default_factory', 'default_factory', 'default_factory_param_name', 'default_factory_param_names', 'has_working_default_factory', 'working_default_factory', 'working_default_factory_param_name', 'working_default_factory_param_names', 'tx_key_key', 'value_slot_name', 'current_slot_name', 'working_slot_name', 'staged_slot_name', 'has_freeze', 'freeze', 'freeze_param_name', 'has_thaw', 'thaw', 'thaw_param_name', 'has_optional_none'):
            raise AttributeError('TransientField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('field_id=' + repr(self.field_id))
        pieces.append('field_owner=' + repr(self.field_owner))
        pieces.append('field_name=' + repr(self.field_name))
        pieces.append('field_order=' + repr(self.field_order))
        pieces.append('field_kind=' + repr(self.field_kind))
        pieces.append('binding_shape=' + repr(self.binding_shape))
        pieces.append('annotation=' + repr(self.annotation))
        pieces.append('init=' + repr(self.init))
        pieces.append('has_default=' + repr(self.has_default))
        pieces.append('default_value=' + repr(self.default_value))
        pieces.append('default_value_param_name=' + repr(self.default_value_param_name))
        pieces.append('has_default_factory=' + repr(self.has_default_factory))
        pieces.append('default_factory=' + repr(self.default_factory))
        pieces.append('default_factory_param_name=' + repr(self.default_factory_param_name))
        pieces.append('default_factory_param_names=' + repr(self.default_factory_param_names))
        pieces.append('has_working_default_factory=' + repr(self.has_working_default_factory))
        pieces.append('working_default_factory=' + repr(self.working_default_factory))
        pieces.append('working_default_factory_param_name=' + repr(self.working_default_factory_param_name))
        pieces.append('working_default_factory_param_names=' + repr(self.working_default_factory_param_names))
        pieces.append('tx_key_key=' + repr(self.tx_key_key))
        pieces.append('value_slot_name=' + repr(self.value_slot_name))
        pieces.append('current_slot_name=' + repr(self.current_slot_name))
        pieces.append('working_slot_name=' + repr(self.working_slot_name))
        pieces.append('staged_slot_name=' + repr(self.staged_slot_name))
        pieces.append('has_freeze=' + repr(self.has_freeze))
        pieces.append('freeze=' + repr(self.freeze))
        pieces.append('freeze_param_name=' + repr(self.freeze_param_name))
        pieces.append('has_thaw=' + repr(self.has_thaw))
        pieces.append('thaw=' + repr(self.thaw))
        pieces.append('thaw_param_name=' + repr(self.thaw_param_name))
        pieces.append('has_optional_none=' + repr(self.has_optional_none))
        return 'TransientField' + '(' + ', '.join(pieces) + ')'
_TransientFieldSpec.bind_record_class(TransientField)

class IndexedOwnedField:
    __slots__ = ('field_id', 'field_owner', 'field_name', 'field_order', 'binding_shape', 'tx_key_key', 'tx_index', 'current_slot_name', 'working_slot_name', 'staged_slot_name')
    __dds_record_spec__ = _IndexedOwnedFieldSpec
    field_id: str
    field_owner: str
    field_name: str
    field_order: int
    binding_shape: str
    tx_key_key: object
    tx_index: int
    current_slot_name: str
    working_slot_name: str
    staged_slot_name: str

    def __init__(self, *, field_id: str, field_owner: str, field_name: str, field_order: int, binding_shape: str='scalar', tx_key_key: object=None, tx_index: int=0, current_slot_name: str='', working_slot_name: str='', staged_slot_name: str=''):
        if not isinstance(field_id, str):
            raise TypeError('FieldId must be str, got ' + type(field_id).__name__)
        object.__setattr__(self, 'field_id', field_id)
        if not isinstance(field_owner, str):
            raise TypeError('FieldOwner must be str, got ' + type(field_owner).__name__)
        object.__setattr__(self, 'field_owner', field_owner)
        if not isinstance(field_name, str):
            raise TypeError('FieldName must be str, got ' + type(field_name).__name__)
        object.__setattr__(self, 'field_name', field_name)
        if not isinstance(field_order, int):
            raise TypeError('FieldOrder must be int, got ' + type(field_order).__name__)
        object.__setattr__(self, 'field_order', field_order)
        if not isinstance(binding_shape, str):
            raise TypeError('BindingShape must be str, got ' + type(binding_shape).__name__)
        object.__setattr__(self, 'binding_shape', binding_shape)
        object.__setattr__(self, 'tx_key_key', tx_key_key)
        if not isinstance(tx_index, int):
            raise TypeError('TxIndex must be int, got ' + type(tx_index).__name__)
        object.__setattr__(self, 'tx_index', tx_index)
        if not isinstance(current_slot_name, str):
            raise TypeError('CurrentSlotName must be str, got ' + type(current_slot_name).__name__)
        object.__setattr__(self, 'current_slot_name', current_slot_name)
        if not isinstance(working_slot_name, str):
            raise TypeError('WorkingSlotName must be str, got ' + type(working_slot_name).__name__)
        object.__setattr__(self, 'working_slot_name', working_slot_name)
        if not isinstance(staged_slot_name, str):
            raise TypeError('StagedSlotName must be str, got ' + type(staged_slot_name).__name__)
        object.__setattr__(self, 'staged_slot_name', staged_slot_name)

    def __setattr__(self, name, value):
        if name in ('field_id', 'field_owner', 'field_name', 'field_order', 'binding_shape', 'tx_key_key', 'tx_index', 'current_slot_name', 'working_slot_name', 'staged_slot_name'):
            raise AttributeError('IndexedOwnedField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('field_id=' + repr(self.field_id))
        pieces.append('field_owner=' + repr(self.field_owner))
        pieces.append('field_name=' + repr(self.field_name))
        pieces.append('field_order=' + repr(self.field_order))
        pieces.append('binding_shape=' + repr(self.binding_shape))
        pieces.append('tx_key_key=' + repr(self.tx_key_key))
        pieces.append('tx_index=' + repr(self.tx_index))
        pieces.append('current_slot_name=' + repr(self.current_slot_name))
        pieces.append('working_slot_name=' + repr(self.working_slot_name))
        pieces.append('staged_slot_name=' + repr(self.staged_slot_name))
        return 'IndexedOwnedField' + '(' + ', '.join(pieces) + ')'
_IndexedOwnedFieldSpec.bind_record_class(IndexedOwnedField)

class BindingField:
    __slots__ = ('field_id', 'field_owner', 'field_name', 'field_order', 'field_kind', 'binding_shape', 'annotation', 'init', 'has_default', 'default_value', 'default_value_param_name', 'has_default_factory', 'default_factory', 'default_factory_param_name', 'default_factory_param_names', 'has_working_default_factory', 'working_default_factory', 'working_default_factory_param_name', 'working_default_factory_param_names', 'tx_key_key', 'value_slot_name', 'current_slot_name', 'working_slot_name', 'staged_slot_name', 'has_freeze', 'freeze', 'freeze_param_name', 'has_thaw', 'thaw', 'thaw_param_name', 'has_optional_none')
    __dds_record_spec__ = _BindingFieldSpec
    field_id: str
    field_owner: str
    field_name: str
    field_order: int
    field_kind: str
    binding_shape: str
    annotation: object
    init: bool
    has_default: bool
    default_value: object
    default_value_param_name: str
    has_default_factory: bool
    default_factory: object
    default_factory_param_name: str
    default_factory_param_names: object
    has_working_default_factory: bool
    working_default_factory: object
    working_default_factory_param_name: str
    working_default_factory_param_names: object
    tx_key_key: object
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

    def __init__(self, *, field_id: str, field_owner: str, field_name: str, field_order: int, field_kind: str='field', binding_shape: str='scalar', annotation: object=object, init: bool=True, has_default: bool=False, default_value: object=None, default_value_param_name: str='', has_default_factory: bool=False, default_factory: object=None, default_factory_param_name: str='', default_factory_param_names: object=(), has_working_default_factory: bool=False, working_default_factory: object=None, working_default_factory_param_name: str='', working_default_factory_param_names: object=(), tx_key_key: object=None, value_slot_name: str='', current_slot_name: str='', working_slot_name: str='', staged_slot_name: str='', has_freeze: bool=False, freeze: object=None, freeze_param_name: str='', has_thaw: bool=False, thaw: object=None, thaw_param_name: str='', has_optional_none: bool=False):
        if not isinstance(field_id, str):
            raise TypeError('FieldId must be str, got ' + type(field_id).__name__)
        object.__setattr__(self, 'field_id', field_id)
        if not isinstance(field_owner, str):
            raise TypeError('FieldOwner must be str, got ' + type(field_owner).__name__)
        object.__setattr__(self, 'field_owner', field_owner)
        if not isinstance(field_name, str):
            raise TypeError('FieldName must be str, got ' + type(field_name).__name__)
        object.__setattr__(self, 'field_name', field_name)
        if not isinstance(field_order, int):
            raise TypeError('FieldOrder must be int, got ' + type(field_order).__name__)
        object.__setattr__(self, 'field_order', field_order)
        if not isinstance(field_kind, str):
            raise TypeError('FieldKind must be str, got ' + type(field_kind).__name__)
        object.__setattr__(self, 'field_kind', field_kind)
        if not isinstance(binding_shape, str):
            raise TypeError('BindingShape must be str, got ' + type(binding_shape).__name__)
        object.__setattr__(self, 'binding_shape', binding_shape)
        object.__setattr__(self, 'annotation', annotation)
        if not isinstance(init, bool):
            raise TypeError('Init must be bool, got ' + type(init).__name__)
        object.__setattr__(self, 'init', init)
        if not isinstance(has_default, bool):
            raise TypeError('HasDefault must be bool, got ' + type(has_default).__name__)
        object.__setattr__(self, 'has_default', has_default)
        object.__setattr__(self, 'default_value', default_value)
        if not isinstance(default_value_param_name, str):
            raise TypeError('DefaultValueParamName must be str, got ' + type(default_value_param_name).__name__)
        object.__setattr__(self, 'default_value_param_name', default_value_param_name)
        if not isinstance(has_default_factory, bool):
            raise TypeError('HasDefaultFactory must be bool, got ' + type(has_default_factory).__name__)
        object.__setattr__(self, 'has_default_factory', has_default_factory)
        object.__setattr__(self, 'default_factory', default_factory)
        if not isinstance(default_factory_param_name, str):
            raise TypeError('DefaultFactoryParamName must be str, got ' + type(default_factory_param_name).__name__)
        object.__setattr__(self, 'default_factory_param_name', default_factory_param_name)
        object.__setattr__(self, 'default_factory_param_names', default_factory_param_names)
        if not isinstance(has_working_default_factory, bool):
            raise TypeError('HasWorkingDefaultFactory must be bool, got ' + type(has_working_default_factory).__name__)
        object.__setattr__(self, 'has_working_default_factory', has_working_default_factory)
        object.__setattr__(self, 'working_default_factory', working_default_factory)
        if not isinstance(working_default_factory_param_name, str):
            raise TypeError('WorkingDefaultFactoryParamName must be str, got ' + type(working_default_factory_param_name).__name__)
        object.__setattr__(self, 'working_default_factory_param_name', working_default_factory_param_name)
        object.__setattr__(self, 'working_default_factory_param_names', working_default_factory_param_names)
        object.__setattr__(self, 'tx_key_key', tx_key_key)
        if not isinstance(value_slot_name, str):
            raise TypeError('ValueSlotName must be str, got ' + type(value_slot_name).__name__)
        object.__setattr__(self, 'value_slot_name', value_slot_name)
        if not isinstance(current_slot_name, str):
            raise TypeError('CurrentSlotName must be str, got ' + type(current_slot_name).__name__)
        object.__setattr__(self, 'current_slot_name', current_slot_name)
        if not isinstance(working_slot_name, str):
            raise TypeError('WorkingSlotName must be str, got ' + type(working_slot_name).__name__)
        object.__setattr__(self, 'working_slot_name', working_slot_name)
        if not isinstance(staged_slot_name, str):
            raise TypeError('StagedSlotName must be str, got ' + type(staged_slot_name).__name__)
        object.__setattr__(self, 'staged_slot_name', staged_slot_name)
        if not isinstance(has_freeze, bool):
            raise TypeError('HasFreeze must be bool, got ' + type(has_freeze).__name__)
        object.__setattr__(self, 'has_freeze', has_freeze)
        object.__setattr__(self, 'freeze', freeze)
        if not isinstance(freeze_param_name, str):
            raise TypeError('FreezeParamName must be str, got ' + type(freeze_param_name).__name__)
        object.__setattr__(self, 'freeze_param_name', freeze_param_name)
        if not isinstance(has_thaw, bool):
            raise TypeError('HasThaw must be bool, got ' + type(has_thaw).__name__)
        object.__setattr__(self, 'has_thaw', has_thaw)
        object.__setattr__(self, 'thaw', thaw)
        if not isinstance(thaw_param_name, str):
            raise TypeError('ThawParamName must be str, got ' + type(thaw_param_name).__name__)
        object.__setattr__(self, 'thaw_param_name', thaw_param_name)
        if not isinstance(has_optional_none, bool):
            raise TypeError('HasOptionalNone must be bool, got ' + type(has_optional_none).__name__)
        object.__setattr__(self, 'has_optional_none', has_optional_none)

    def __setattr__(self, name, value):
        if name in ('field_id', 'field_owner', 'field_name', 'field_order', 'field_kind', 'binding_shape', 'annotation', 'init', 'has_default', 'default_value', 'default_value_param_name', 'has_default_factory', 'default_factory', 'default_factory_param_name', 'default_factory_param_names', 'has_working_default_factory', 'working_default_factory', 'working_default_factory_param_name', 'working_default_factory_param_names', 'tx_key_key', 'value_slot_name', 'current_slot_name', 'working_slot_name', 'staged_slot_name', 'has_freeze', 'freeze', 'freeze_param_name', 'has_thaw', 'thaw', 'thaw_param_name', 'has_optional_none'):
            raise AttributeError('BindingField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('field_id=' + repr(self.field_id))
        pieces.append('field_owner=' + repr(self.field_owner))
        pieces.append('field_name=' + repr(self.field_name))
        pieces.append('field_order=' + repr(self.field_order))
        pieces.append('field_kind=' + repr(self.field_kind))
        pieces.append('binding_shape=' + repr(self.binding_shape))
        pieces.append('annotation=' + repr(self.annotation))
        pieces.append('init=' + repr(self.init))
        pieces.append('has_default=' + repr(self.has_default))
        pieces.append('default_value=' + repr(self.default_value))
        pieces.append('default_value_param_name=' + repr(self.default_value_param_name))
        pieces.append('has_default_factory=' + repr(self.has_default_factory))
        pieces.append('default_factory=' + repr(self.default_factory))
        pieces.append('default_factory_param_name=' + repr(self.default_factory_param_name))
        pieces.append('default_factory_param_names=' + repr(self.default_factory_param_names))
        pieces.append('has_working_default_factory=' + repr(self.has_working_default_factory))
        pieces.append('working_default_factory=' + repr(self.working_default_factory))
        pieces.append('working_default_factory_param_name=' + repr(self.working_default_factory_param_name))
        pieces.append('working_default_factory_param_names=' + repr(self.working_default_factory_param_names))
        pieces.append('tx_key_key=' + repr(self.tx_key_key))
        pieces.append('value_slot_name=' + repr(self.value_slot_name))
        pieces.append('current_slot_name=' + repr(self.current_slot_name))
        pieces.append('working_slot_name=' + repr(self.working_slot_name))
        pieces.append('staged_slot_name=' + repr(self.staged_slot_name))
        pieces.append('has_freeze=' + repr(self.has_freeze))
        pieces.append('freeze=' + repr(self.freeze))
        pieces.append('freeze_param_name=' + repr(self.freeze_param_name))
        pieces.append('has_thaw=' + repr(self.has_thaw))
        pieces.append('thaw=' + repr(self.thaw))
        pieces.append('thaw_param_name=' + repr(self.thaw_param_name))
        pieces.append('has_optional_none=' + repr(self.has_optional_none))
        return 'BindingField' + '(' + ', '.join(pieces) + ')'
_BindingFieldSpec.bind_record_class(BindingField)

class OwnedField:
    __slots__ = ('field_id', 'field_owner', 'field_name', 'field_order', 'field_kind', 'binding_shape', 'annotation', 'init', 'has_default', 'default_value', 'default_value_param_name', 'has_default_factory', 'default_factory', 'default_factory_param_name', 'default_factory_param_names', 'has_working_default_factory', 'working_default_factory', 'working_default_factory_param_name', 'working_default_factory_param_names', 'tx_key_key', 'value_slot_name', 'current_slot_name', 'working_slot_name', 'staged_slot_name', 'has_freeze', 'freeze', 'freeze_param_name', 'has_thaw', 'thaw', 'thaw_param_name', 'has_optional_none')
    __dds_record_spec__ = _OwnedFieldSpec
    field_id: str
    field_owner: str
    field_name: str
    field_order: int
    field_kind: str
    binding_shape: str
    annotation: object
    init: bool
    has_default: bool
    default_value: object
    default_value_param_name: str
    has_default_factory: bool
    default_factory: object
    default_factory_param_name: str
    default_factory_param_names: object
    has_working_default_factory: bool
    working_default_factory: object
    working_default_factory_param_name: str
    working_default_factory_param_names: object
    tx_key_key: object
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

    def __init__(self, *, field_id: str, field_owner: str, field_name: str, field_order: int, field_kind: str='field', binding_shape: str='scalar', annotation: object=object, init: bool=True, has_default: bool=False, default_value: object=None, default_value_param_name: str='', has_default_factory: bool=False, default_factory: object=None, default_factory_param_name: str='', default_factory_param_names: object=(), has_working_default_factory: bool=False, working_default_factory: object=None, working_default_factory_param_name: str='', working_default_factory_param_names: object=(), tx_key_key: object=None, value_slot_name: str='', current_slot_name: str='', working_slot_name: str='', staged_slot_name: str='', has_freeze: bool=False, freeze: object=None, freeze_param_name: str='', has_thaw: bool=False, thaw: object=None, thaw_param_name: str='', has_optional_none: bool=False):
        if not isinstance(field_id, str):
            raise TypeError('FieldId must be str, got ' + type(field_id).__name__)
        object.__setattr__(self, 'field_id', field_id)
        if not isinstance(field_owner, str):
            raise TypeError('FieldOwner must be str, got ' + type(field_owner).__name__)
        object.__setattr__(self, 'field_owner', field_owner)
        if not isinstance(field_name, str):
            raise TypeError('FieldName must be str, got ' + type(field_name).__name__)
        object.__setattr__(self, 'field_name', field_name)
        if not isinstance(field_order, int):
            raise TypeError('FieldOrder must be int, got ' + type(field_order).__name__)
        object.__setattr__(self, 'field_order', field_order)
        if not isinstance(field_kind, str):
            raise TypeError('FieldKind must be str, got ' + type(field_kind).__name__)
        object.__setattr__(self, 'field_kind', field_kind)
        if not isinstance(binding_shape, str):
            raise TypeError('BindingShape must be str, got ' + type(binding_shape).__name__)
        object.__setattr__(self, 'binding_shape', binding_shape)
        object.__setattr__(self, 'annotation', annotation)
        if not isinstance(init, bool):
            raise TypeError('Init must be bool, got ' + type(init).__name__)
        object.__setattr__(self, 'init', init)
        if not isinstance(has_default, bool):
            raise TypeError('HasDefault must be bool, got ' + type(has_default).__name__)
        object.__setattr__(self, 'has_default', has_default)
        object.__setattr__(self, 'default_value', default_value)
        if not isinstance(default_value_param_name, str):
            raise TypeError('DefaultValueParamName must be str, got ' + type(default_value_param_name).__name__)
        object.__setattr__(self, 'default_value_param_name', default_value_param_name)
        if not isinstance(has_default_factory, bool):
            raise TypeError('HasDefaultFactory must be bool, got ' + type(has_default_factory).__name__)
        object.__setattr__(self, 'has_default_factory', has_default_factory)
        object.__setattr__(self, 'default_factory', default_factory)
        if not isinstance(default_factory_param_name, str):
            raise TypeError('DefaultFactoryParamName must be str, got ' + type(default_factory_param_name).__name__)
        object.__setattr__(self, 'default_factory_param_name', default_factory_param_name)
        object.__setattr__(self, 'default_factory_param_names', default_factory_param_names)
        if not isinstance(has_working_default_factory, bool):
            raise TypeError('HasWorkingDefaultFactory must be bool, got ' + type(has_working_default_factory).__name__)
        object.__setattr__(self, 'has_working_default_factory', has_working_default_factory)
        object.__setattr__(self, 'working_default_factory', working_default_factory)
        if not isinstance(working_default_factory_param_name, str):
            raise TypeError('WorkingDefaultFactoryParamName must be str, got ' + type(working_default_factory_param_name).__name__)
        object.__setattr__(self, 'working_default_factory_param_name', working_default_factory_param_name)
        object.__setattr__(self, 'working_default_factory_param_names', working_default_factory_param_names)
        object.__setattr__(self, 'tx_key_key', tx_key_key)
        if not isinstance(value_slot_name, str):
            raise TypeError('ValueSlotName must be str, got ' + type(value_slot_name).__name__)
        object.__setattr__(self, 'value_slot_name', value_slot_name)
        if not isinstance(current_slot_name, str):
            raise TypeError('CurrentSlotName must be str, got ' + type(current_slot_name).__name__)
        object.__setattr__(self, 'current_slot_name', current_slot_name)
        if not isinstance(working_slot_name, str):
            raise TypeError('WorkingSlotName must be str, got ' + type(working_slot_name).__name__)
        object.__setattr__(self, 'working_slot_name', working_slot_name)
        if not isinstance(staged_slot_name, str):
            raise TypeError('StagedSlotName must be str, got ' + type(staged_slot_name).__name__)
        object.__setattr__(self, 'staged_slot_name', staged_slot_name)
        if not isinstance(has_freeze, bool):
            raise TypeError('HasFreeze must be bool, got ' + type(has_freeze).__name__)
        object.__setattr__(self, 'has_freeze', has_freeze)
        object.__setattr__(self, 'freeze', freeze)
        if not isinstance(freeze_param_name, str):
            raise TypeError('FreezeParamName must be str, got ' + type(freeze_param_name).__name__)
        object.__setattr__(self, 'freeze_param_name', freeze_param_name)
        if not isinstance(has_thaw, bool):
            raise TypeError('HasThaw must be bool, got ' + type(has_thaw).__name__)
        object.__setattr__(self, 'has_thaw', has_thaw)
        object.__setattr__(self, 'thaw', thaw)
        if not isinstance(thaw_param_name, str):
            raise TypeError('ThawParamName must be str, got ' + type(thaw_param_name).__name__)
        object.__setattr__(self, 'thaw_param_name', thaw_param_name)
        if not isinstance(has_optional_none, bool):
            raise TypeError('HasOptionalNone must be bool, got ' + type(has_optional_none).__name__)
        object.__setattr__(self, 'has_optional_none', has_optional_none)

    def __setattr__(self, name, value):
        if name in ('field_id', 'field_owner', 'field_name', 'field_order', 'field_kind', 'binding_shape', 'annotation', 'init', 'has_default', 'default_value', 'default_value_param_name', 'has_default_factory', 'default_factory', 'default_factory_param_name', 'default_factory_param_names', 'has_working_default_factory', 'working_default_factory', 'working_default_factory_param_name', 'working_default_factory_param_names', 'tx_key_key', 'value_slot_name', 'current_slot_name', 'working_slot_name', 'staged_slot_name', 'has_freeze', 'freeze', 'freeze_param_name', 'has_thaw', 'thaw', 'thaw_param_name', 'has_optional_none'):
            raise AttributeError('OwnedField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('field_id=' + repr(self.field_id))
        pieces.append('field_owner=' + repr(self.field_owner))
        pieces.append('field_name=' + repr(self.field_name))
        pieces.append('field_order=' + repr(self.field_order))
        pieces.append('field_kind=' + repr(self.field_kind))
        pieces.append('binding_shape=' + repr(self.binding_shape))
        pieces.append('annotation=' + repr(self.annotation))
        pieces.append('init=' + repr(self.init))
        pieces.append('has_default=' + repr(self.has_default))
        pieces.append('default_value=' + repr(self.default_value))
        pieces.append('default_value_param_name=' + repr(self.default_value_param_name))
        pieces.append('has_default_factory=' + repr(self.has_default_factory))
        pieces.append('default_factory=' + repr(self.default_factory))
        pieces.append('default_factory_param_name=' + repr(self.default_factory_param_name))
        pieces.append('default_factory_param_names=' + repr(self.default_factory_param_names))
        pieces.append('has_working_default_factory=' + repr(self.has_working_default_factory))
        pieces.append('working_default_factory=' + repr(self.working_default_factory))
        pieces.append('working_default_factory_param_name=' + repr(self.working_default_factory_param_name))
        pieces.append('working_default_factory_param_names=' + repr(self.working_default_factory_param_names))
        pieces.append('tx_key_key=' + repr(self.tx_key_key))
        pieces.append('value_slot_name=' + repr(self.value_slot_name))
        pieces.append('current_slot_name=' + repr(self.current_slot_name))
        pieces.append('working_slot_name=' + repr(self.working_slot_name))
        pieces.append('staged_slot_name=' + repr(self.staged_slot_name))
        pieces.append('has_freeze=' + repr(self.has_freeze))
        pieces.append('freeze=' + repr(self.freeze))
        pieces.append('freeze_param_name=' + repr(self.freeze_param_name))
        pieces.append('has_thaw=' + repr(self.has_thaw))
        pieces.append('thaw=' + repr(self.thaw))
        pieces.append('thaw_param_name=' + repr(self.thaw_param_name))
        pieces.append('has_optional_none=' + repr(self.has_optional_none))
        return 'OwnedField' + '(' + ', '.join(pieces) + ')'
_OwnedFieldSpec.bind_record_class(OwnedField)

class ConstField:
    __slots__ = ('field_id', 'field_owner', 'field_name', 'field_order', 'field_kind', 'binding_shape', 'annotation', 'init', 'has_default', 'default_value', 'default_value_param_name', 'has_default_factory', 'default_factory', 'default_factory_param_name', 'default_factory_param_names', 'has_working_default_factory', 'working_default_factory', 'working_default_factory_param_name', 'working_default_factory_param_names', 'tx_key_key', 'value_slot_name', 'current_slot_name', 'working_slot_name', 'staged_slot_name', 'has_freeze', 'freeze', 'freeze_param_name', 'has_thaw', 'thaw', 'thaw_param_name', 'has_optional_none')
    __dds_record_spec__ = _ConstFieldSpec
    field_id: str
    field_owner: str
    field_name: str
    field_order: int
    field_kind: str
    binding_shape: str
    annotation: object
    init: bool
    has_default: bool
    default_value: object
    default_value_param_name: str
    has_default_factory: bool
    default_factory: object
    default_factory_param_name: str
    default_factory_param_names: object
    has_working_default_factory: bool
    working_default_factory: object
    working_default_factory_param_name: str
    working_default_factory_param_names: object
    tx_key_key: object
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

    def __init__(self, *, field_id: str, field_owner: str, field_name: str, field_order: int, field_kind: str='field', binding_shape: str='scalar', annotation: object=object, init: bool=True, has_default: bool=False, default_value: object=None, default_value_param_name: str='', has_default_factory: bool=False, default_factory: object=None, default_factory_param_name: str='', default_factory_param_names: object=(), has_working_default_factory: bool=False, working_default_factory: object=None, working_default_factory_param_name: str='', working_default_factory_param_names: object=(), tx_key_key: object=None, value_slot_name: str='', current_slot_name: str='', working_slot_name: str='', staged_slot_name: str='', has_freeze: bool=False, freeze: object=None, freeze_param_name: str='', has_thaw: bool=False, thaw: object=None, thaw_param_name: str='', has_optional_none: bool=False):
        if not isinstance(field_id, str):
            raise TypeError('FieldId must be str, got ' + type(field_id).__name__)
        object.__setattr__(self, 'field_id', field_id)
        if not isinstance(field_owner, str):
            raise TypeError('FieldOwner must be str, got ' + type(field_owner).__name__)
        object.__setattr__(self, 'field_owner', field_owner)
        if not isinstance(field_name, str):
            raise TypeError('FieldName must be str, got ' + type(field_name).__name__)
        object.__setattr__(self, 'field_name', field_name)
        if not isinstance(field_order, int):
            raise TypeError('FieldOrder must be int, got ' + type(field_order).__name__)
        object.__setattr__(self, 'field_order', field_order)
        if not isinstance(field_kind, str):
            raise TypeError('FieldKind must be str, got ' + type(field_kind).__name__)
        object.__setattr__(self, 'field_kind', field_kind)
        if not isinstance(binding_shape, str):
            raise TypeError('BindingShape must be str, got ' + type(binding_shape).__name__)
        object.__setattr__(self, 'binding_shape', binding_shape)
        object.__setattr__(self, 'annotation', annotation)
        if not isinstance(init, bool):
            raise TypeError('Init must be bool, got ' + type(init).__name__)
        object.__setattr__(self, 'init', init)
        if not isinstance(has_default, bool):
            raise TypeError('HasDefault must be bool, got ' + type(has_default).__name__)
        object.__setattr__(self, 'has_default', has_default)
        object.__setattr__(self, 'default_value', default_value)
        if not isinstance(default_value_param_name, str):
            raise TypeError('DefaultValueParamName must be str, got ' + type(default_value_param_name).__name__)
        object.__setattr__(self, 'default_value_param_name', default_value_param_name)
        if not isinstance(has_default_factory, bool):
            raise TypeError('HasDefaultFactory must be bool, got ' + type(has_default_factory).__name__)
        object.__setattr__(self, 'has_default_factory', has_default_factory)
        object.__setattr__(self, 'default_factory', default_factory)
        if not isinstance(default_factory_param_name, str):
            raise TypeError('DefaultFactoryParamName must be str, got ' + type(default_factory_param_name).__name__)
        object.__setattr__(self, 'default_factory_param_name', default_factory_param_name)
        object.__setattr__(self, 'default_factory_param_names', default_factory_param_names)
        if not isinstance(has_working_default_factory, bool):
            raise TypeError('HasWorkingDefaultFactory must be bool, got ' + type(has_working_default_factory).__name__)
        object.__setattr__(self, 'has_working_default_factory', has_working_default_factory)
        object.__setattr__(self, 'working_default_factory', working_default_factory)
        if not isinstance(working_default_factory_param_name, str):
            raise TypeError('WorkingDefaultFactoryParamName must be str, got ' + type(working_default_factory_param_name).__name__)
        object.__setattr__(self, 'working_default_factory_param_name', working_default_factory_param_name)
        object.__setattr__(self, 'working_default_factory_param_names', working_default_factory_param_names)
        object.__setattr__(self, 'tx_key_key', tx_key_key)
        if not isinstance(value_slot_name, str):
            raise TypeError('ValueSlotName must be str, got ' + type(value_slot_name).__name__)
        object.__setattr__(self, 'value_slot_name', value_slot_name)
        if not isinstance(current_slot_name, str):
            raise TypeError('CurrentSlotName must be str, got ' + type(current_slot_name).__name__)
        object.__setattr__(self, 'current_slot_name', current_slot_name)
        if not isinstance(working_slot_name, str):
            raise TypeError('WorkingSlotName must be str, got ' + type(working_slot_name).__name__)
        object.__setattr__(self, 'working_slot_name', working_slot_name)
        if not isinstance(staged_slot_name, str):
            raise TypeError('StagedSlotName must be str, got ' + type(staged_slot_name).__name__)
        object.__setattr__(self, 'staged_slot_name', staged_slot_name)
        if not isinstance(has_freeze, bool):
            raise TypeError('HasFreeze must be bool, got ' + type(has_freeze).__name__)
        object.__setattr__(self, 'has_freeze', has_freeze)
        object.__setattr__(self, 'freeze', freeze)
        if not isinstance(freeze_param_name, str):
            raise TypeError('FreezeParamName must be str, got ' + type(freeze_param_name).__name__)
        object.__setattr__(self, 'freeze_param_name', freeze_param_name)
        if not isinstance(has_thaw, bool):
            raise TypeError('HasThaw must be bool, got ' + type(has_thaw).__name__)
        object.__setattr__(self, 'has_thaw', has_thaw)
        object.__setattr__(self, 'thaw', thaw)
        if not isinstance(thaw_param_name, str):
            raise TypeError('ThawParamName must be str, got ' + type(thaw_param_name).__name__)
        object.__setattr__(self, 'thaw_param_name', thaw_param_name)
        if not isinstance(has_optional_none, bool):
            raise TypeError('HasOptionalNone must be bool, got ' + type(has_optional_none).__name__)
        object.__setattr__(self, 'has_optional_none', has_optional_none)

    def __setattr__(self, name, value):
        if name in ('field_id', 'field_owner', 'field_name', 'field_order', 'field_kind', 'binding_shape', 'annotation', 'init', 'has_default', 'default_value', 'default_value_param_name', 'has_default_factory', 'default_factory', 'default_factory_param_name', 'default_factory_param_names', 'has_working_default_factory', 'working_default_factory', 'working_default_factory_param_name', 'working_default_factory_param_names', 'tx_key_key', 'value_slot_name', 'current_slot_name', 'working_slot_name', 'staged_slot_name', 'has_freeze', 'freeze', 'freeze_param_name', 'has_thaw', 'thaw', 'thaw_param_name', 'has_optional_none'):
            raise AttributeError('ConstField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('field_id=' + repr(self.field_id))
        pieces.append('field_owner=' + repr(self.field_owner))
        pieces.append('field_name=' + repr(self.field_name))
        pieces.append('field_order=' + repr(self.field_order))
        pieces.append('field_kind=' + repr(self.field_kind))
        pieces.append('binding_shape=' + repr(self.binding_shape))
        pieces.append('annotation=' + repr(self.annotation))
        pieces.append('init=' + repr(self.init))
        pieces.append('has_default=' + repr(self.has_default))
        pieces.append('default_value=' + repr(self.default_value))
        pieces.append('default_value_param_name=' + repr(self.default_value_param_name))
        pieces.append('has_default_factory=' + repr(self.has_default_factory))
        pieces.append('default_factory=' + repr(self.default_factory))
        pieces.append('default_factory_param_name=' + repr(self.default_factory_param_name))
        pieces.append('default_factory_param_names=' + repr(self.default_factory_param_names))
        pieces.append('has_working_default_factory=' + repr(self.has_working_default_factory))
        pieces.append('working_default_factory=' + repr(self.working_default_factory))
        pieces.append('working_default_factory_param_name=' + repr(self.working_default_factory_param_name))
        pieces.append('working_default_factory_param_names=' + repr(self.working_default_factory_param_names))
        pieces.append('tx_key_key=' + repr(self.tx_key_key))
        pieces.append('value_slot_name=' + repr(self.value_slot_name))
        pieces.append('current_slot_name=' + repr(self.current_slot_name))
        pieces.append('working_slot_name=' + repr(self.working_slot_name))
        pieces.append('staged_slot_name=' + repr(self.staged_slot_name))
        pieces.append('has_freeze=' + repr(self.has_freeze))
        pieces.append('freeze=' + repr(self.freeze))
        pieces.append('freeze_param_name=' + repr(self.freeze_param_name))
        pieces.append('has_thaw=' + repr(self.has_thaw))
        pieces.append('thaw=' + repr(self.thaw))
        pieces.append('thaw_param_name=' + repr(self.thaw_param_name))
        pieces.append('has_optional_none=' + repr(self.has_optional_none))
        return 'ConstField' + '(' + ', '.join(pieces) + ')'
_ConstFieldSpec.bind_record_class(ConstField)

class StaticField:
    __slots__ = ('field_id', 'field_owner', 'field_name', 'field_order', 'field_kind', 'binding_shape', 'annotation', 'init', 'has_default', 'default_value', 'default_value_param_name', 'has_default_factory', 'default_factory', 'default_factory_param_name', 'default_factory_param_names', 'has_working_default_factory', 'working_default_factory', 'working_default_factory_param_name', 'working_default_factory_param_names', 'tx_key_key', 'value_slot_name', 'current_slot_name', 'working_slot_name', 'staged_slot_name', 'has_freeze', 'freeze', 'freeze_param_name', 'has_thaw', 'thaw', 'thaw_param_name', 'has_optional_none')
    __dds_record_spec__ = _StaticFieldSpec
    field_id: str
    field_owner: str
    field_name: str
    field_order: int
    field_kind: str
    binding_shape: str
    annotation: object
    init: bool
    has_default: bool
    default_value: object
    default_value_param_name: str
    has_default_factory: bool
    default_factory: object
    default_factory_param_name: str
    default_factory_param_names: object
    has_working_default_factory: bool
    working_default_factory: object
    working_default_factory_param_name: str
    working_default_factory_param_names: object
    tx_key_key: object
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

    def __init__(self, *, field_id: str, field_owner: str, field_name: str, field_order: int, field_kind: str='field', binding_shape: str='scalar', annotation: object=object, init: bool=True, has_default: bool=False, default_value: object=None, default_value_param_name: str='', has_default_factory: bool=False, default_factory: object=None, default_factory_param_name: str='', default_factory_param_names: object=(), has_working_default_factory: bool=False, working_default_factory: object=None, working_default_factory_param_name: str='', working_default_factory_param_names: object=(), tx_key_key: object=None, value_slot_name: str='', current_slot_name: str='', working_slot_name: str='', staged_slot_name: str='', has_freeze: bool=False, freeze: object=None, freeze_param_name: str='', has_thaw: bool=False, thaw: object=None, thaw_param_name: str='', has_optional_none: bool=False):
        if not isinstance(field_id, str):
            raise TypeError('FieldId must be str, got ' + type(field_id).__name__)
        object.__setattr__(self, 'field_id', field_id)
        if not isinstance(field_owner, str):
            raise TypeError('FieldOwner must be str, got ' + type(field_owner).__name__)
        object.__setattr__(self, 'field_owner', field_owner)
        if not isinstance(field_name, str):
            raise TypeError('FieldName must be str, got ' + type(field_name).__name__)
        object.__setattr__(self, 'field_name', field_name)
        if not isinstance(field_order, int):
            raise TypeError('FieldOrder must be int, got ' + type(field_order).__name__)
        object.__setattr__(self, 'field_order', field_order)
        if not isinstance(field_kind, str):
            raise TypeError('FieldKind must be str, got ' + type(field_kind).__name__)
        object.__setattr__(self, 'field_kind', field_kind)
        if not isinstance(binding_shape, str):
            raise TypeError('BindingShape must be str, got ' + type(binding_shape).__name__)
        object.__setattr__(self, 'binding_shape', binding_shape)
        object.__setattr__(self, 'annotation', annotation)
        if not isinstance(init, bool):
            raise TypeError('Init must be bool, got ' + type(init).__name__)
        object.__setattr__(self, 'init', init)
        if not isinstance(has_default, bool):
            raise TypeError('HasDefault must be bool, got ' + type(has_default).__name__)
        object.__setattr__(self, 'has_default', has_default)
        object.__setattr__(self, 'default_value', default_value)
        if not isinstance(default_value_param_name, str):
            raise TypeError('DefaultValueParamName must be str, got ' + type(default_value_param_name).__name__)
        object.__setattr__(self, 'default_value_param_name', default_value_param_name)
        if not isinstance(has_default_factory, bool):
            raise TypeError('HasDefaultFactory must be bool, got ' + type(has_default_factory).__name__)
        object.__setattr__(self, 'has_default_factory', has_default_factory)
        object.__setattr__(self, 'default_factory', default_factory)
        if not isinstance(default_factory_param_name, str):
            raise TypeError('DefaultFactoryParamName must be str, got ' + type(default_factory_param_name).__name__)
        object.__setattr__(self, 'default_factory_param_name', default_factory_param_name)
        object.__setattr__(self, 'default_factory_param_names', default_factory_param_names)
        if not isinstance(has_working_default_factory, bool):
            raise TypeError('HasWorkingDefaultFactory must be bool, got ' + type(has_working_default_factory).__name__)
        object.__setattr__(self, 'has_working_default_factory', has_working_default_factory)
        object.__setattr__(self, 'working_default_factory', working_default_factory)
        if not isinstance(working_default_factory_param_name, str):
            raise TypeError('WorkingDefaultFactoryParamName must be str, got ' + type(working_default_factory_param_name).__name__)
        object.__setattr__(self, 'working_default_factory_param_name', working_default_factory_param_name)
        object.__setattr__(self, 'working_default_factory_param_names', working_default_factory_param_names)
        object.__setattr__(self, 'tx_key_key', tx_key_key)
        if not isinstance(value_slot_name, str):
            raise TypeError('ValueSlotName must be str, got ' + type(value_slot_name).__name__)
        object.__setattr__(self, 'value_slot_name', value_slot_name)
        if not isinstance(current_slot_name, str):
            raise TypeError('CurrentSlotName must be str, got ' + type(current_slot_name).__name__)
        object.__setattr__(self, 'current_slot_name', current_slot_name)
        if not isinstance(working_slot_name, str):
            raise TypeError('WorkingSlotName must be str, got ' + type(working_slot_name).__name__)
        object.__setattr__(self, 'working_slot_name', working_slot_name)
        if not isinstance(staged_slot_name, str):
            raise TypeError('StagedSlotName must be str, got ' + type(staged_slot_name).__name__)
        object.__setattr__(self, 'staged_slot_name', staged_slot_name)
        if not isinstance(has_freeze, bool):
            raise TypeError('HasFreeze must be bool, got ' + type(has_freeze).__name__)
        object.__setattr__(self, 'has_freeze', has_freeze)
        object.__setattr__(self, 'freeze', freeze)
        if not isinstance(freeze_param_name, str):
            raise TypeError('FreezeParamName must be str, got ' + type(freeze_param_name).__name__)
        object.__setattr__(self, 'freeze_param_name', freeze_param_name)
        if not isinstance(has_thaw, bool):
            raise TypeError('HasThaw must be bool, got ' + type(has_thaw).__name__)
        object.__setattr__(self, 'has_thaw', has_thaw)
        object.__setattr__(self, 'thaw', thaw)
        if not isinstance(thaw_param_name, str):
            raise TypeError('ThawParamName must be str, got ' + type(thaw_param_name).__name__)
        object.__setattr__(self, 'thaw_param_name', thaw_param_name)
        if not isinstance(has_optional_none, bool):
            raise TypeError('HasOptionalNone must be bool, got ' + type(has_optional_none).__name__)
        object.__setattr__(self, 'has_optional_none', has_optional_none)

    def __setattr__(self, name, value):
        if name in ('field_id', 'field_owner', 'field_name', 'field_order', 'field_kind', 'binding_shape', 'annotation', 'init', 'has_default', 'default_value', 'default_value_param_name', 'has_default_factory', 'default_factory', 'default_factory_param_name', 'default_factory_param_names', 'has_working_default_factory', 'working_default_factory', 'working_default_factory_param_name', 'working_default_factory_param_names', 'tx_key_key', 'value_slot_name', 'current_slot_name', 'working_slot_name', 'staged_slot_name', 'has_freeze', 'freeze', 'freeze_param_name', 'has_thaw', 'thaw', 'thaw_param_name', 'has_optional_none'):
            raise AttributeError('StaticField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('field_id=' + repr(self.field_id))
        pieces.append('field_owner=' + repr(self.field_owner))
        pieces.append('field_name=' + repr(self.field_name))
        pieces.append('field_order=' + repr(self.field_order))
        pieces.append('field_kind=' + repr(self.field_kind))
        pieces.append('binding_shape=' + repr(self.binding_shape))
        pieces.append('annotation=' + repr(self.annotation))
        pieces.append('init=' + repr(self.init))
        pieces.append('has_default=' + repr(self.has_default))
        pieces.append('default_value=' + repr(self.default_value))
        pieces.append('default_value_param_name=' + repr(self.default_value_param_name))
        pieces.append('has_default_factory=' + repr(self.has_default_factory))
        pieces.append('default_factory=' + repr(self.default_factory))
        pieces.append('default_factory_param_name=' + repr(self.default_factory_param_name))
        pieces.append('default_factory_param_names=' + repr(self.default_factory_param_names))
        pieces.append('has_working_default_factory=' + repr(self.has_working_default_factory))
        pieces.append('working_default_factory=' + repr(self.working_default_factory))
        pieces.append('working_default_factory_param_name=' + repr(self.working_default_factory_param_name))
        pieces.append('working_default_factory_param_names=' + repr(self.working_default_factory_param_names))
        pieces.append('tx_key_key=' + repr(self.tx_key_key))
        pieces.append('value_slot_name=' + repr(self.value_slot_name))
        pieces.append('current_slot_name=' + repr(self.current_slot_name))
        pieces.append('working_slot_name=' + repr(self.working_slot_name))
        pieces.append('staged_slot_name=' + repr(self.staged_slot_name))
        pieces.append('has_freeze=' + repr(self.has_freeze))
        pieces.append('freeze=' + repr(self.freeze))
        pieces.append('freeze_param_name=' + repr(self.freeze_param_name))
        pieces.append('has_thaw=' + repr(self.has_thaw))
        pieces.append('thaw=' + repr(self.thaw))
        pieces.append('thaw_param_name=' + repr(self.thaw_param_name))
        pieces.append('has_optional_none=' + repr(self.has_optional_none))
        return 'StaticField' + '(' + ', '.join(pieces) + ')'
_StaticFieldSpec.bind_record_class(StaticField)
ClassesCollection = RuntimeCollection('Classes', _LifecycleClassSpec, allows_multiple=True, identity=_ClassIdProperty)
FieldsCollection = RuntimeCollection('Fields', _LifecycleFieldSpecUnion, allows_multiple=True, identity=_FieldIdProperty)
TransactionMethodsCollection = RuntimeCollection('TransactionMethods', _TransactionMethodSpec, allows_multiple=True, identity=_MethodIdProperty)
FacadeClassesCollection = RuntimeCollection('FacadeClasses', _FacadeClassSpec, allows_multiple=True, identity=(_FacadeOwnerProperty, _FacadeIdProperty))
FacadeExposuresCollection = RuntimeCollection('FacadeExposures', _FacadeExposureSpec, allows_multiple=True, identity=(_FacadeOwnerProperty, _OwnerFacadeIdProperty, _FieldNameProperty))
InitParametersCollection = RuntimeCollection('InitParameters', _InitParameterSpec, allows_multiple=True, identity=_InitParameterIdProperty)
InitAssignmentsCollection = RuntimeCollection('InitAssignments', _InitAssignmentSpec, allows_multiple=True, identity=_InitAssignmentIdProperty)
ClassVarAssignmentsCollection = RuntimeCollection('ClassVarAssignments', _ClassVarAssignmentSpec, allows_multiple=True, identity=_ClassVarAssignmentIdProperty)
TransactionalFieldsCollection = RuntimeCollection('TransactionalFields', _TransactionalFieldSpec, allows_multiple=True, identity=_FieldIdProperty)
TxKeysCollection = RuntimeCollection('TxKeys', _TxKeySpec, allows_multiple=True, identity=(_TxOwnerProperty, _TxKeyKeyProperty))
IndexedTransactionalFieldsCollection = RuntimeCollection('IndexedTransactionalFields', _IndexedTransactionalFieldSpec, allows_multiple=True, identity=_FieldIdProperty)
DefaultFactoryDependenciesCollection = RuntimeCollection('DefaultFactoryDependencies', _DefaultFactoryDependencySpec, allows_multiple=True, identity=(_ConsumerFieldIdProperty, _ParamNameProperty))
DefaultFactoryEvaluationStepsCollection = RuntimeCollection('DefaultFactoryEvaluationSteps', _DefaultFactoryEvaluationStepSpec, allows_multiple=True, identity=_EvalStepIdProperty)
DefaultFactoryDiagnosticsCollection = RuntimeCollection('DefaultFactoryDiagnostics', _DefaultFactoryDiagnosticSpec, allows_multiple=True, identity=_DiagnosticIdProperty)
IndexedTransientFieldsCollection = RuntimeCollection('IndexedTransientFields', _IndexedTransientFieldSpec, allows_multiple=True, identity=_FieldIdProperty)
RetainedInitVarsCollection = RuntimeCollection('RetainedInitVars', _RetainedInitVarSpec, allows_multiple=True, identity=_FieldIdProperty)
TransientWorkingFactoryArgsCollection = RuntimeCollection('TransientWorkingFactoryArgs', _TransientWorkingFactoryArgSpec, allows_multiple=True, identity=_WorkingFactoryArgIdProperty)
IndexedOwnedFieldsCollection = RuntimeCollection('IndexedOwnedFields', _IndexedOwnedFieldSpec, allows_multiple=True, identity=_FieldIdProperty)
PlainFieldsCollection = RuntimeComputedCollection('PlainFields', source=FieldsCollection, when=(_FieldKindProperty.eq('field'),))
InitVarFieldsCollection = RuntimeComputedCollection('InitVarFields', source=FieldsCollection, when=(_FieldKindProperty.eq('initvar'),))
ClassVarFieldsCollection = RuntimeComputedCollection('ClassVarFields', source=FieldsCollection, when=(_FieldKindProperty.eq('classvar'),))
CommitOrderKeyProvidersCollection = RuntimeComputedCollection('CommitOrderKeyProviders', source=TransactionMethodsCollection, when=(_MethodKindProperty.eq('commit_order_key'),))
CommitValidatorsCollection = RuntimeComputedCollection('CommitValidators', source=TransactionMethodsCollection, when=(_MethodKindProperty.eq('validate_commit'),))
BeforeCommitHooksCollection = RuntimeComputedCollection('BeforeCommitHooks', source=TransactionMethodsCollection, when=(_MethodKindProperty.eq('before_commit'),))
AfterCommitHooksCollection = RuntimeComputedCollection('AfterCommitHooks', source=TransactionMethodsCollection, when=(_MethodKindProperty.eq('after_commit'),))
AfterRollbackHooksCollection = RuntimeComputedCollection('AfterRollbackHooks', source=TransactionMethodsCollection, when=(_MethodKindProperty.eq('after_rollback'),))
ManagedFieldsCollection = RuntimeComputedCollection('ManagedFields', source=FieldsCollection, when=(_FieldKindProperty.eq('managed'),))
TransientFieldsCollection = RuntimeComputedCollection('TransientFields', source=FieldsCollection, when=(_FieldKindProperty.eq('transient'),))
BindingFieldsCollection = RuntimeComputedCollection('BindingFields', source=FieldsCollection, when=(_FieldKindProperty.eq('binding'),))
OwnedFieldsCollection = RuntimeComputedCollection('OwnedFields', source=FieldsCollection, when=(_FieldKindProperty.eq('owned'),))
BindingScalarFieldsCollection = RuntimeComputedCollection('BindingScalarFields', source=FieldsCollection, when=(_FieldKindProperty.eq('binding'), _BindingShapeProperty.eq('scalar')))
BindingMapFieldsCollection = RuntimeComputedCollection('BindingMapFields', source=FieldsCollection, when=(_FieldKindProperty.eq('binding'), _BindingShapeProperty.eq('map')))
OwnedScalarFieldsCollection = RuntimeComputedCollection('OwnedScalarFields', source=FieldsCollection, when=(_FieldKindProperty.eq('owned'), _BindingShapeProperty.eq('scalar')))
OwnedMapFieldsCollection = RuntimeComputedCollection('OwnedMapFields', source=FieldsCollection, when=(_FieldKindProperty.eq('owned'), _BindingShapeProperty.eq('map')))
ConstFieldsCollection = RuntimeComputedCollection('ConstFields', source=FieldsCollection, when=(_FieldKindProperty.eq('const'),))
StaticFieldsCollection = RuntimeComputedCollection('StaticFields', source=FieldsCollection, when=(_FieldKindProperty.eq('static'),))
_RUNTIME_SPEC = RuntimeContainerSpec(collections=(ClassesCollection, FieldsCollection, TransactionMethodsCollection, FacadeClassesCollection, FacadeExposuresCollection, InitParametersCollection, InitAssignmentsCollection, ClassVarAssignmentsCollection, TransactionalFieldsCollection, TxKeysCollection, IndexedTransactionalFieldsCollection, DefaultFactoryDependenciesCollection, DefaultFactoryEvaluationStepsCollection, DefaultFactoryDiagnosticsCollection, IndexedTransientFieldsCollection, RetainedInitVarsCollection, TransientWorkingFactoryArgsCollection, IndexedOwnedFieldsCollection), computed_collections=(PlainFieldsCollection, InitVarFieldsCollection, ClassVarFieldsCollection, CommitOrderKeyProvidersCollection, CommitValidatorsCollection, BeforeCommitHooksCollection, AfterCommitHooksCollection, AfterRollbackHooksCollection, ManagedFieldsCollection, TransientFieldsCollection, BindingFieldsCollection, OwnedFieldsCollection, BindingScalarFieldsCollection, BindingMapFieldsCollection, OwnedScalarFieldsCollection, OwnedMapFieldsCollection, ConstFieldsCollection, StaticFieldsCollection), ports=(), port_index=None)

def run_build_transaction_facts(builder):
    ctx = DDSOperationContext(builder, 'BuildTransactionFacts', ordered_inputs={})
    from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION
    classes = sorted(ctx.records(ClassesCollection), key=lambda item: item.class_order)
    fields = sorted(ctx.records(FieldsCollection), key=lambda item: item.field_order)
    for lifecycle_class in classes:
        seen = {DEFAULT_TRANSACTION: 0}
        ctx.write(TxKeysCollection, TxKey(tx_owner=lifecycle_class.class_id, tx_key_key=DEFAULT_TRANSACTION, tx_index=0, tx_key_order=0, commit_order_key_function_name='_commit_order_key_tx_0', requires_validation_function_name='_requires_validation_tx_0', validate_commit_function_name='_validate_commit_tx_0', before_commit_function_name='_before_commit_tx_0', after_commit_function_name='_after_commit_tx_0', after_rollback_function_name='_after_rollback_tx_0', prepare_commit_fields_function_name='_prepare_commit_tx_0_fields', apply_prepared_commit_fields_function_name='_apply_prepared_commit_tx_0_fields', rollback_fields_function_name='_rollback_tx_0_fields'), policy=RejectDuplicate)
        for field in fields:
            if field.field_owner != lifecycle_class.class_id:
                continue
            if field.field_kind not in {'managed', 'owned', 'transient'}:
                continue
            tx_key = field.tx_key_key
            if tx_key is None:
                tx_key = DEFAULT_TRANSACTION
            if tx_key not in seen:
                seen[tx_key] = len(seen)
                ctx.write(TxKeysCollection, TxKey(tx_owner=lifecycle_class.class_id, tx_key_key=tx_key, tx_index=seen[tx_key], tx_key_order=field.field_order, commit_order_key_function_name=f'_commit_order_key_tx_{seen[tx_key]}', requires_validation_function_name=f'_requires_validation_tx_{seen[tx_key]}', validate_commit_function_name=f'_validate_commit_tx_{seen[tx_key]}', before_commit_function_name=f'_before_commit_tx_{seen[tx_key]}', after_commit_function_name=f'_after_commit_tx_{seen[tx_key]}', after_rollback_function_name=f'_after_rollback_tx_{seen[tx_key]}', prepare_commit_fields_function_name=f'_prepare_commit_tx_{seen[tx_key]}_fields', apply_prepared_commit_fields_function_name=f'_apply_prepared_commit_tx_{seen[tx_key]}_fields', rollback_fields_function_name=f'_rollback_tx_{seen[tx_key]}_fields'), policy=RejectDuplicate)
            tx_index = seen[tx_key]
            ctx.write(TransactionalFieldsCollection, TransactionalField(field_id=field.field_id, field_owner=field.field_owner, field_name=field.field_name, field_order=field.field_order, tx_key_key=tx_key), policy=RejectDuplicate)
            if field.field_kind != 'managed':
                continue
            ctx.write(IndexedTransactionalFieldsCollection, IndexedTransactionalField(field_id=field.field_id, field_owner=field.field_owner, field_name=field.field_name, field_order=field.field_order, tx_key_key=tx_key, tx_index=tx_index, current_slot_name=field.current_slot_name, working_slot_name=field.working_slot_name, staged_slot_name=field.staged_slot_name, has_freeze=field.has_freeze, freeze_param_name=field.freeze_param_name, has_thaw=field.has_thaw, thaw_param_name=field.thaw_param_name, has_optional_none=field.has_optional_none), policy=RejectDuplicate)

def run_build_default_factory_facts(builder):
    ctx = DDSOperationContext(builder, 'BuildDefaultFactoryFacts', ordered_inputs={})
    classes = sorted(ctx.records(ClassesCollection), key=lambda item: item.class_order)
    fields = sorted(ctx.records(FieldsCollection), key=lambda item: item.field_order)
    for lifecycle_class in classes:
        class_fields = [field for field in fields if field.field_owner == lifecycle_class.class_id]
        by_name = {field.field_name: field for field in class_fields}
        by_id = {field.field_id: field for field in class_fields}
        factory_fields = [field for field in class_fields if field.has_default_factory]
        graph = {field.field_id: set() for field in factory_fields}
        deps = []
        diagnostic_count = 0

        def add_diagnostic(field, suffix, message):
            nonlocal diagnostic_count
            diagnostic_count += 1
            ctx.write(DefaultFactoryDiagnosticsCollection, DefaultFactoryDiagnostic(diagnostic_id=f'{field.field_id}.{suffix}.{diagnostic_count}', diagnostic_owner=lifecycle_class.class_id, diagnostic_field_id=field.field_id, diagnostic_message=message), policy=ReplaceExisting)

        def provider_is_available(provider):
            if provider.init:
                return True
            return provider.has_default or provider.has_default_factory
        for consumer in factory_fields:
            for param_order, param_name in enumerate(consumer.default_factory_param_names):
                provider = by_name.get(param_name)
                if provider is None:
                    add_diagnostic(consumer, f'unknown.{param_name}', f'{lifecycle_class.class_name}.{consumer.field_name}: default_factory references unknown name {param_name!r}')
                    continue
                if consumer.field_kind == 'static' and provider.field_kind == 'initvar':
                    add_diagnostic(consumer, f'static_initvar.{param_name}', f'{lifecycle_class.class_name}.{consumer.field_name}: static default_factory cannot reference initvar {param_name!r} until retained initvar support is enabled')
                    continue
                if not provider_is_available(provider):
                    add_diagnostic(consumer, f'unavailable.{param_name}', f'{lifecycle_class.class_name}.{consumer.field_name}: default_factory cannot reference {param_name!r} (value is unavailable before factory evaluation)')
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
                cycle = path[path.index(field_id):]
                names = ' -> '.join((by_id[item].field_name for item in cycle))
                add_diagnostic(by_id[field_id], 'cycle', f'{lifecycle_class.class_name}: default_factory dependency cycle: {names}')
                cycle_found = True
                return
            visiting.add(field_id)
            for provider_id in sorted(graph.get(field_id, ()), key=lambda item: field_order[item]):
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
        eval_order_by_id = {field_id: eval_order for eval_order, field_id in enumerate(ordered_field_ids)}
        for consumer, provider, param_name, param_order in deps:
            ctx.write(DefaultFactoryDependenciesCollection, DefaultFactoryDependency(dependency_owner=lifecycle_class.class_id, consumer_field_id=consumer.field_id, consumer_field_name=consumer.field_name, consumer_field_kind=consumer.field_kind, consumer_field_order=consumer.field_order, provider_name=provider.field_name, provider_field_id=provider.field_id, provider_field_kind=provider.field_kind, provider_init=provider.init, provider_has_default=provider.has_default, provider_has_default_factory=provider.has_default_factory, param_name=param_name, param_order=param_order, consumer_eval_order=eval_order_by_id[consumer.field_id]), policy=RejectDuplicate)
        for field in factory_fields:
            if field.default_factory_param_names:
                continue
            ctx.write(DefaultFactoryDependenciesCollection, DefaultFactoryDependency(dependency_owner=lifecycle_class.class_id, consumer_field_id=field.field_id, consumer_field_name=field.field_name, consumer_field_kind=field.field_kind, consumer_field_order=field.field_order, provider_name='', provider_field_id='', provider_field_kind='', provider_init=True, provider_has_default=False, provider_has_default_factory=False, param_name='', param_order=-1, consumer_eval_order=eval_order_by_id[field.field_id]), policy=RejectDuplicate)
        for eval_order, field_id in enumerate(ordered_field_ids):
            field = by_id[field_id]
            state_slot = ''
            if field.value_slot_name:
                state_slot = field.value_slot_name
            elif field.field_kind == 'managed':
                state_slot = field.current_slot_name
            elif field.field_kind == 'owned':
                state_slot = field.current_slot_name
            elif field.field_kind == 'transient':
                state_slot = field.current_slot_name
            ctx.write(DefaultFactoryEvaluationStepsCollection, DefaultFactoryEvaluationStep(eval_step_id=field.field_id, eval_owner=lifecycle_class.class_id, eval_field_id=field.field_id, eval_field_name=field.field_name, eval_field_kind=field.field_kind, eval_binding_shape=field.binding_shape, eval_init=field.init, eval_state_slot_name=state_slot, eval_default_factory_param_name=field.default_factory_param_name, eval_order=eval_order, eval_statement_order=100000 + eval_order), policy=RejectDuplicate)

def run_raise_default_factory_diagnostics(builder):
    ctx = DDSOperationContext(builder, 'RaiseDefaultFactoryDiagnostics', ordered_inputs={})
    for diagnostic in ctx.records(DefaultFactoryDiagnosticsCollection):
        raise AssemblyDiagnosticError(diagnostic.diagnostic_message)

def run_build_transient_facts(builder):
    ctx = DDSOperationContext(builder, 'BuildTransientFacts', ordered_inputs={})
    from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION
    fields = list(ctx.records(FieldsCollection))
    by_owner_name = {(field.field_owner, field.field_name): field for field in fields}
    tx_keys = {(tx_key.tx_owner, tx_key.tx_key_key): tx_key.tx_index for tx_key in ctx.records(TxKeysCollection)}
    for field in fields:
        if field.field_kind != 'transient':
            continue
        tx_key = field.tx_key_key
        if tx_key is None:
            tx_key = DEFAULT_TRANSACTION
        tx_index = tx_keys[field.field_owner, tx_key]
        ctx.write(IndexedTransientFieldsCollection, IndexedTransientField(field_id=field.field_id, field_owner=field.field_owner, field_name=field.field_name, field_order=field.field_order, tx_key_key=tx_key, tx_index=tx_index, current_slot_name=field.current_slot_name, working_slot_name=field.working_slot_name, has_working_default_factory=field.has_working_default_factory, working_default_factory_param_name=field.working_default_factory_param_name), policy=RejectDuplicate)
        if field.has_working_default_factory and (not field.working_default_factory_param_names):
            ctx.write(TransientWorkingFactoryArgsCollection, TransientWorkingFactoryArg(working_factory_arg_id=f'{field.field_id}.__empty__', working_factory_arg_owner=field.field_owner, working_factory_consumer_field_id=field.field_id, working_factory_consumer_field_order=field.field_order, param_name='', param_order=-1, provider_name='', working_factory_arg_kind='empty', retained_slot_name=''), policy=RejectDuplicate)
        for param_order, param_name in enumerate(field.working_default_factory_param_names):
            arg_kind = ''
            provider_name = param_name
            retained_slot_name = ''
            if param_name in {'self', 'current', 'working'}:
                arg_kind = param_name
            else:
                provider = by_owner_name.get((field.field_owner, param_name))
                if provider is None:
                    raise AssemblyDiagnosticError(f'{field.field_name}: working_default_factory references unknown name {param_name!r}')
                if provider.field_kind != 'initvar':
                    raise AssemblyDiagnosticError(f'{field.field_name}: working_default_factory cannot retain non-initvar provider {param_name!r}')
                if not provider.init and (not provider.has_default) and (not provider.has_default_factory):
                    raise AssemblyDiagnosticError(f'{field.field_name}: working_default_factory cannot retain initvar {param_name!r} without a default or default_factory')
                arg_kind = 'retained_initvar'
                retained_slot_name = f'_y_{param_name}_initvar'
                ctx.write(RetainedInitVarsCollection, RetainedInitVar(field_id=provider.field_id, field_owner=provider.field_owner, field_name=provider.field_name, field_order=provider.field_order, retained_slot_name=retained_slot_name, retain_order=200000 + provider.field_order), policy=ReplaceExisting)
            ctx.write(TransientWorkingFactoryArgsCollection, TransientWorkingFactoryArg(working_factory_arg_id=f'{field.field_id}.{param_name}', working_factory_arg_owner=field.field_owner, working_factory_consumer_field_id=field.field_id, working_factory_consumer_field_order=field.field_order, param_name=param_name, param_order=param_order, provider_name=provider_name, working_factory_arg_kind=arg_kind, retained_slot_name=retained_slot_name), policy=RejectDuplicate)

def run_build_owned_facts(builder):
    ctx = DDSOperationContext(builder, 'BuildOwnedFacts', ordered_inputs={})
    from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION
    tx_keys = {(tx_key.tx_owner, tx_key.tx_key_key): tx_key.tx_index for tx_key in ctx.records(TxKeysCollection)}
    for field in ctx.records(FieldsCollection):
        if field.field_kind != 'owned':
            continue
        tx_key = field.tx_key_key
        if tx_key is None:
            tx_key = DEFAULT_TRANSACTION
        ctx.write(IndexedOwnedFieldsCollection, IndexedOwnedField(field_id=field.field_id, field_owner=field.field_owner, field_name=field.field_name, field_order=field.field_order, binding_shape=field.binding_shape, tx_key_key=tx_key, tx_index=tx_keys[field.field_owner, tx_key], current_slot_name=field.current_slot_name, working_slot_name=field.working_slot_name, staged_slot_name=field.staged_slot_name), policy=RejectDuplicate)

def run_operations(builder):
    run_build_transaction_facts(builder)
    run_build_default_factory_facts(builder)
    run_raise_default_factory_diagnostics(builder)
    run_build_transient_facts(builder)
    run_build_owned_facts(builder)
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
from yidl.generation.assembly_plan import AndConditionSpec, AssemblyEdgeSpec, AssemblyInputSpec, AssemblySpec, BindingSpec, ComposableProductionSpec, ContributionMatcherSpec, ContributionRuleSpec, ContributionSpec, EdgeApplySpec, EqConditionSpec, InlineApplySpec, LiteralValueRef, PathSegmentSpec, PathSpec, RootSpec, TargetPathSpec, TargetSpec, TupleValueRef, ValueRef
from yidl.generation.assembly_runtime import run_assembly
from yidl.generation.matcher_values import astichi_template, from_astichi_code, from_import

ASSEMBLY_PROPERTIES = {'ClassId': _YidlSimpleNamespace(name='ClassId', storage_name='class_id'), 'ClassName': _YidlSimpleNamespace(name='ClassName', storage_name='class_name'), 'ClassOrder': _YidlSimpleNamespace(name='ClassOrder', storage_name='class_order'), 'ModuleName': _YidlSimpleNamespace(name='ModuleName', storage_name='module_name'), 'StateClassName': _YidlSimpleNamespace(name='StateClassName', storage_name='state_class_name'), 'FacadeBaseClassName': _YidlSimpleNamespace(name='FacadeBaseClassName', storage_name='facade_base_class_name'), 'CurrentFacadeClassName': _YidlSimpleNamespace(name='CurrentFacadeClassName', storage_name='current_facade_class_name'), 'WorkingFacadeClassName': _YidlSimpleNamespace(name='WorkingFacadeClassName', storage_name='working_facade_class_name'), 'LifecycleDefinitionParamName': _YidlSimpleNamespace(name='LifecycleDefinitionParamName', storage_name='lifecycle_definition_param_name'), 'AnnotationsParamName': _YidlSimpleNamespace(name='AnnotationsParamName', storage_name='annotations_param_name'), 'TxKeysParamName': _YidlSimpleNamespace(name='TxKeysParamName', storage_name='tx_keys_param_name'), 'LifecycleFieldNames': _YidlSimpleNamespace(name='LifecycleFieldNames', storage_name='lifecycle_field_names'), 'FieldId': _YidlSimpleNamespace(name='FieldId', storage_name='field_id'), 'FieldOwner': _YidlSimpleNamespace(name='FieldOwner', storage_name='field_owner'), 'FieldName': _YidlSimpleNamespace(name='FieldName', storage_name='field_name'), 'FieldOrder': _YidlSimpleNamespace(name='FieldOrder', storage_name='field_order'), 'FieldKind': _YidlSimpleNamespace(name='FieldKind', storage_name='field_kind'), 'BindingShape': _YidlSimpleNamespace(name='BindingShape', storage_name='binding_shape'), 'Annotation': _YidlSimpleNamespace(name='Annotation', storage_name='annotation'), 'Init': _YidlSimpleNamespace(name='Init', storage_name='init'), 'HasDefault': _YidlSimpleNamespace(name='HasDefault', storage_name='has_default'), 'DefaultValue': _YidlSimpleNamespace(name='DefaultValue', storage_name='default_value'), 'DefaultValueParamName': _YidlSimpleNamespace(name='DefaultValueParamName', storage_name='default_value_param_name'), 'HasDefaultFactory': _YidlSimpleNamespace(name='HasDefaultFactory', storage_name='has_default_factory'), 'DefaultFactory': _YidlSimpleNamespace(name='DefaultFactory', storage_name='default_factory'), 'DefaultFactoryParamName': _YidlSimpleNamespace(name='DefaultFactoryParamName', storage_name='default_factory_param_name'), 'DefaultFactoryParamNames': _YidlSimpleNamespace(name='DefaultFactoryParamNames', storage_name='default_factory_param_names'), 'HasWorkingDefaultFactory': _YidlSimpleNamespace(name='HasWorkingDefaultFactory', storage_name='has_working_default_factory'), 'WorkingDefaultFactory': _YidlSimpleNamespace(name='WorkingDefaultFactory', storage_name='working_default_factory'), 'WorkingDefaultFactoryParamName': _YidlSimpleNamespace(name='WorkingDefaultFactoryParamName', storage_name='working_default_factory_param_name'), 'WorkingDefaultFactoryParamNames': _YidlSimpleNamespace(name='WorkingDefaultFactoryParamNames', storage_name='working_default_factory_param_names'), 'TxKeyKey': _YidlSimpleNamespace(name='TxKeyKey', storage_name='tx_key_key'), 'ValueSlotName': _YidlSimpleNamespace(name='ValueSlotName', storage_name='value_slot_name'), 'CurrentSlotName': _YidlSimpleNamespace(name='CurrentSlotName', storage_name='current_slot_name'), 'WorkingSlotName': _YidlSimpleNamespace(name='WorkingSlotName', storage_name='working_slot_name'), 'StagedSlotName': _YidlSimpleNamespace(name='StagedSlotName', storage_name='staged_slot_name'), 'HasFreeze': _YidlSimpleNamespace(name='HasFreeze', storage_name='has_freeze'), 'Freeze': _YidlSimpleNamespace(name='Freeze', storage_name='freeze'), 'FreezeParamName': _YidlSimpleNamespace(name='FreezeParamName', storage_name='freeze_param_name'), 'HasThaw': _YidlSimpleNamespace(name='HasThaw', storage_name='has_thaw'), 'Thaw': _YidlSimpleNamespace(name='Thaw', storage_name='thaw'), 'ThawParamName': _YidlSimpleNamespace(name='ThawParamName', storage_name='thaw_param_name'), 'HasOptionalNone': _YidlSimpleNamespace(name='HasOptionalNone', storage_name='has_optional_none'), 'MethodId': _YidlSimpleNamespace(name='MethodId', storage_name='method_id'), 'MethodOwner': _YidlSimpleNamespace(name='MethodOwner', storage_name='method_owner'), 'MethodName': _YidlSimpleNamespace(name='MethodName', storage_name='method_name'), 'MethodKind': _YidlSimpleNamespace(name='MethodKind', storage_name='method_kind'), 'DeclarationOrder': _YidlSimpleNamespace(name='DeclarationOrder', storage_name='declaration_order'), 'TxIndex': _YidlSimpleNamespace(name='TxIndex', storage_name='tx_index'), 'FacadeId': _YidlSimpleNamespace(name='FacadeId', storage_name='facade_id'), 'FacadeOwner': _YidlSimpleNamespace(name='FacadeOwner', storage_name='facade_owner'), 'FacadeKind': _YidlSimpleNamespace(name='FacadeKind', storage_name='facade_kind'), 'FacadeMode': _YidlSimpleNamespace(name='FacadeMode', storage_name='facade_mode'), 'FacadeClassName': _YidlSimpleNamespace(name='FacadeClassName', storage_name='facade_class_name'), 'FacadeOrder': _YidlSimpleNamespace(name='FacadeOrder', storage_name='facade_order'), 'OwnerFacadeId': _YidlSimpleNamespace(name='OwnerFacadeId', storage_name='owner_facade_id'), 'TargetFacadeId': _YidlSimpleNamespace(name='TargetFacadeId', storage_name='target_facade_id'), 'ExposureOrder': _YidlSimpleNamespace(name='ExposureOrder', storage_name='exposure_order'), 'InitParameterId': _YidlSimpleNamespace(name='InitParameterId', storage_name='init_parameter_id'), 'InitParameterOwner': _YidlSimpleNamespace(name='InitParameterOwner', storage_name='init_parameter_owner'), 'InitParameterName': _YidlSimpleNamespace(name='InitParameterName', storage_name='init_parameter_name'), 'InitParameterOrder': _YidlSimpleNamespace(name='InitParameterOrder', storage_name='init_parameter_order'), 'InitParameterKind': _YidlSimpleNamespace(name='InitParameterKind', storage_name='init_parameter_kind'), 'InitAssignmentId': _YidlSimpleNamespace(name='InitAssignmentId', storage_name='init_assignment_id'), 'InitAssignmentOwner': _YidlSimpleNamespace(name='InitAssignmentOwner', storage_name='init_assignment_owner'), 'InitAssignmentFieldId': _YidlSimpleNamespace(name='InitAssignmentFieldId', storage_name='init_assignment_field_id'), 'InitAssignmentFieldName': _YidlSimpleNamespace(name='InitAssignmentFieldName', storage_name='init_assignment_field_name'), 'InitAssignmentOrder': _YidlSimpleNamespace(name='InitAssignmentOrder', storage_name='init_assignment_order'), 'InitAssignmentKind': _YidlSimpleNamespace(name='InitAssignmentKind', storage_name='init_assignment_kind'), 'ClassVarAssignmentId': _YidlSimpleNamespace(name='ClassVarAssignmentId', storage_name='class_var_assignment_id'), 'ClassVarAssignmentOwner': _YidlSimpleNamespace(name='ClassVarAssignmentOwner', storage_name='class_var_assignment_owner'), 'ClassVarAssignmentName': _YidlSimpleNamespace(name='ClassVarAssignmentName', storage_name='class_var_assignment_name'), 'ClassVarAssignmentOrder': _YidlSimpleNamespace(name='ClassVarAssignmentOrder', storage_name='class_var_assignment_order'), 'TxKeyOrder': _YidlSimpleNamespace(name='TxKeyOrder', storage_name='tx_key_order'), 'TxOwner': _YidlSimpleNamespace(name='TxOwner', storage_name='tx_owner'), 'CommitOrderKeyFunctionName': _YidlSimpleNamespace(name='CommitOrderKeyFunctionName', storage_name='commit_order_key_function_name'), 'RequiresValidationFunctionName': _YidlSimpleNamespace(name='RequiresValidationFunctionName', storage_name='requires_validation_function_name'), 'ValidateCommitFunctionName': _YidlSimpleNamespace(name='ValidateCommitFunctionName', storage_name='validate_commit_function_name'), 'BeforeCommitFunctionName': _YidlSimpleNamespace(name='BeforeCommitFunctionName', storage_name='before_commit_function_name'), 'AfterCommitFunctionName': _YidlSimpleNamespace(name='AfterCommitFunctionName', storage_name='after_commit_function_name'), 'AfterRollbackFunctionName': _YidlSimpleNamespace(name='AfterRollbackFunctionName', storage_name='after_rollback_function_name'), 'PrepareCommitFieldsFunctionName': _YidlSimpleNamespace(name='PrepareCommitFieldsFunctionName', storage_name='prepare_commit_fields_function_name'), 'ApplyPreparedCommitFieldsFunctionName': _YidlSimpleNamespace(name='ApplyPreparedCommitFieldsFunctionName', storage_name='apply_prepared_commit_fields_function_name'), 'RollbackFieldsFunctionName': _YidlSimpleNamespace(name='RollbackFieldsFunctionName', storage_name='rollback_fields_function_name'), 'DependencyOwner': _YidlSimpleNamespace(name='DependencyOwner', storage_name='dependency_owner'), 'ConsumerFieldId': _YidlSimpleNamespace(name='ConsumerFieldId', storage_name='consumer_field_id'), 'ConsumerFieldName': _YidlSimpleNamespace(name='ConsumerFieldName', storage_name='consumer_field_name'), 'ConsumerFieldKind': _YidlSimpleNamespace(name='ConsumerFieldKind', storage_name='consumer_field_kind'), 'ConsumerFieldOrder': _YidlSimpleNamespace(name='ConsumerFieldOrder', storage_name='consumer_field_order'), 'ProviderName': _YidlSimpleNamespace(name='ProviderName', storage_name='provider_name'), 'ProviderFieldId': _YidlSimpleNamespace(name='ProviderFieldId', storage_name='provider_field_id'), 'ProviderFieldKind': _YidlSimpleNamespace(name='ProviderFieldKind', storage_name='provider_field_kind'), 'ProviderInit': _YidlSimpleNamespace(name='ProviderInit', storage_name='provider_init'), 'ProviderHasDefault': _YidlSimpleNamespace(name='ProviderHasDefault', storage_name='provider_has_default'), 'ProviderHasDefaultFactory': _YidlSimpleNamespace(name='ProviderHasDefaultFactory', storage_name='provider_has_default_factory'), 'ParamName': _YidlSimpleNamespace(name='ParamName', storage_name='param_name'), 'ParamOrder': _YidlSimpleNamespace(name='ParamOrder', storage_name='param_order'), 'ConsumerEvalOrder': _YidlSimpleNamespace(name='ConsumerEvalOrder', storage_name='consumer_eval_order'), 'EvalStepId': _YidlSimpleNamespace(name='EvalStepId', storage_name='eval_step_id'), 'EvalOwner': _YidlSimpleNamespace(name='EvalOwner', storage_name='eval_owner'), 'EvalFieldId': _YidlSimpleNamespace(name='EvalFieldId', storage_name='eval_field_id'), 'EvalFieldName': _YidlSimpleNamespace(name='EvalFieldName', storage_name='eval_field_name'), 'EvalFieldKind': _YidlSimpleNamespace(name='EvalFieldKind', storage_name='eval_field_kind'), 'EvalBindingShape': _YidlSimpleNamespace(name='EvalBindingShape', storage_name='eval_binding_shape'), 'EvalInit': _YidlSimpleNamespace(name='EvalInit', storage_name='eval_init'), 'EvalStateSlotName': _YidlSimpleNamespace(name='EvalStateSlotName', storage_name='eval_state_slot_name'), 'EvalDefaultFactoryParamName': _YidlSimpleNamespace(name='EvalDefaultFactoryParamName', storage_name='eval_default_factory_param_name'), 'EvalOrder': _YidlSimpleNamespace(name='EvalOrder', storage_name='eval_order'), 'EvalStatementOrder': _YidlSimpleNamespace(name='EvalStatementOrder', storage_name='eval_statement_order'), 'DiagnosticId': _YidlSimpleNamespace(name='DiagnosticId', storage_name='diagnostic_id'), 'DiagnosticOwner': _YidlSimpleNamespace(name='DiagnosticOwner', storage_name='diagnostic_owner'), 'DiagnosticFieldId': _YidlSimpleNamespace(name='DiagnosticFieldId', storage_name='diagnostic_field_id'), 'DiagnosticMessage': _YidlSimpleNamespace(name='DiagnosticMessage', storage_name='diagnostic_message'), 'RetainedSlotName': _YidlSimpleNamespace(name='RetainedSlotName', storage_name='retained_slot_name'), 'RetainOrder': _YidlSimpleNamespace(name='RetainOrder', storage_name='retain_order'), 'WorkingFactoryArgId': _YidlSimpleNamespace(name='WorkingFactoryArgId', storage_name='working_factory_arg_id'), 'WorkingFactoryArgOwner': _YidlSimpleNamespace(name='WorkingFactoryArgOwner', storage_name='working_factory_arg_owner'), 'WorkingFactoryConsumerFieldId': _YidlSimpleNamespace(name='WorkingFactoryConsumerFieldId', storage_name='working_factory_consumer_field_id'), 'WorkingFactoryConsumerFieldOrder': _YidlSimpleNamespace(name='WorkingFactoryConsumerFieldOrder', storage_name='working_factory_consumer_field_order'), 'WorkingFactoryArgKind': _YidlSimpleNamespace(name='WorkingFactoryArgKind', storage_name='working_factory_arg_kind')}
ASSEMBLY_RESOURCES = {'ModuleRoot': from_astichi_code("""\
from __future__ import annotations

import weakref

from yidl.runtime.lifecycle import _HAS_DEFAULT_FACTORY
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION
from yidl.runtime.transaction_yidl import TransactionManager


VOID = object()


def build_lifecycle_class(decorated_cls, builder_params__astichi_param_hole__):
    astichi_hole(function_body)
    astichi_hole(return_statement)""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=213), 'BuilderParam': astichi_template(from_astichi_code("""\
def astichi_params(*, value_name__astichi_arg__):
    pass""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=231)), 'TransactionManagerParam': astichi_template(from_astichi_code("""\
def astichi_params(*, transaction_manager=None):
    pass""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=236)), 'StateSlotEntry': astichi_template(from_astichi_code('astichi_bind_external(slot_name)', file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=241)), 'InitParamRequired': astichi_template(from_astichi_code("""\
def astichi_params(param_name__astichi_arg__: astichi_bind_external(annotation)):
    pass""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=245)), 'InitParamDefault': astichi_template(from_astichi_code("""\
def astichi_params(
    param_name__astichi_arg__: astichi_bind_external(annotation)
    = default_value_name__astichi_arg__
):
    pass""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=250)), 'PlainStateAssignment': astichi_template(from_astichi_code("""\
astichi_pass(state, outer_bind=True).astichi_ref(external=state_slot)._ = astichi_pass(
    init_value_name__astichi_arg__,
    outer_bind=True,
)""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=258)), 'InitVarLocalDefaultAssignment': astichi_template(from_astichi_code("""\
init_value_name__astichi_arg__ = astichi_pass(
    default_value_name__astichi_arg__,
    outer_bind=True,
)""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=265)), 'PlainProperty': astichi_template(from_astichi_code("""\
@property
def property_getter_name__astichi_arg__(self):
    return self._y_state.astichi_ref(external=state_slot)

@property_setter_target_name__astichi_arg__.setter
def property_setter_name__astichi_arg__(self, value):
    self._y_state.astichi_ref(external=state_slot)._ = value""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=272)), 'ClassVarDefaultAssignment': astichi_template(from_astichi_code("""\
classvar_name__astichi_arg__ = astichi_pass(
    classvar_value_name__astichi_arg__,
    outer_bind=True,
)""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=282)), 'CommitOrderKeyBranch': astichi_template(from_astichi_code("""\
def astichi_elif():
    astichi_import(tx_index)
    astichi_import(self)

    if tx_index == astichi_bind_external(tx_index_value):
        return self._y_get_default_facade().astichi_ref(external=method_name)()""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=289)), 'RequiresValidationBranch': astichi_template(from_astichi_code("""\
def astichi_elif():
    astichi_import(tx_index)

    if tx_index == astichi_bind_external(tx_index_value):
        return True""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=298)), 'ValidateCommitBranch': astichi_template(from_astichi_code("""\
def astichi_elif():
    astichi_import(tx_index)
    astichi_import(self)

    if tx_index == astichi_bind_external(tx_index_value):
        result = self._y_get_default_facade().astichi_ref(external=method_name)()
        if result is False:
            return False""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=306)), 'TransactionHookCall': astichi_template(from_astichi_code("""\
def astichi_elif():
    astichi_import(tx_index)
    astichi_import(self)

    if tx_index == astichi_bind_external(tx_index_value):
        self._y_get_default_facade().astichi_ref(external=method_name)()""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=317)), 'CommitOrderKeyFallbackBranch': astichi_template(from_astichi_code("""\
def astichi_elif():
    if True:
        return ()""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=326)), 'RequiresValidationFallbackBranch': astichi_template(from_astichi_code("""\
def astichi_elif():
    if True:
        return False""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=332)), 'ValidateCommitFallbackBranch': astichi_template(from_astichi_code("""\
def astichi_elif():
    if True:
        return True""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=338)), 'PassFallbackBranch': astichi_template(from_astichi_code("""\
def astichi_elif():
    if True:
        pass""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=344)), 'ClassBundle': astichi_template(from_astichi_code("""\
class state_class_decl_name__astichi_arg__:
    __slots__ = (
        "_y_transaction_manager",
        "_y_default_ref",
        "_y_current_ref",
        "_y_working_ref",
        *astichi_hole(state_slots),
        "_y_working_tx_ids",
    )
    __yidl_tx_index_to_key__ = astichi_pass(
        tx_keys_for_index_name__astichi_arg__,
        outer_bind=True,
    )
    __yidl_tx_key_to_index__ = {
        key: index for index, key in enumerate(
            astichi_pass(tx_keys_for_map_name__astichi_arg__, outer_bind=True)
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
        ref = self._y_current_ref
        facade = None if ref is None else ref()
        if facade is None:
            facade = object.__new__(current_facade_class_ref__astichi_arg__)
            object.__setattr__(facade, "_y_state", self)
            self._y_current_ref = weakref.ref(facade)
            default_ref = self._y_default_ref
            default = None if default_ref is None else default_ref()
            if default is not None:
                object.__setattr__(default, "_y_current_facade", facade)
        return facade

    def _y_get_working_facade(self):
        ref = self._y_working_ref
        facade = None if ref is None else ref()
        if facade is None:
            facade = object.__new__(working_facade_class_ref__astichi_arg__)
            object.__setattr__(facade, "_y_state", self)
            self._y_working_ref = weakref.ref(facade)
            default_ref = self._y_default_ref
            default = None if default_ref is None else default_ref()
            if default is not None:
                object.__setattr__(default, "_y_working_facade", facade)
        return facade

    def _y_require_active_transaction(self, tx_index):
        tx_key = self.__yidl_tx_index_to_key__[tx_index]
        transaction = self._y_transaction_manager.active_transaction_for(tx_key)
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
            tx_key = self.__yidl_tx_index_to_key__[tx_index]
            self._y_working_tx_ids[tx_index] = (
                self._y_transaction_manager.enlist(self, tx_key)
            )
        return transaction

    def commit_order_key_for(self, tx_key=DEFAULT_TRANSACTION):
        tx_index = self.__yidl_tx_key_to_index__[tx_key]
        if False:
            pass
        elif astichi_elif(commit_order_key_body):
            pass

    def requires_validation_for(self, tx_key=DEFAULT_TRANSACTION):
        tx_index = self.__yidl_tx_key_to_index__[tx_key]
        if False:
            pass
        elif astichi_elif(requires_validation_body):
            pass

    def validate_commit_for(self, tx_key=DEFAULT_TRANSACTION):
        tx_index = self.__yidl_tx_key_to_index__[tx_key]
        if False:
            pass
        elif astichi_elif(validate_commit_body):
            pass

    def _prepare_commit_tx_by_key(self, tx_key=DEFAULT_TRANSACTION, tx_token=None):
        tx_index = self.__yidl_tx_key_to_index__[tx_key]
        if self._y_working_tx_ids[tx_index] != tx_token:
            raise RuntimeError("stale yidl transaction token")
        if False:
            pass
        elif astichi_elif(before_commit_body):
            pass
        if False:
            pass
        elif astichi_elif(prepare_commit_transaction_dispatch_body):
            pass
        return self._y_get_default_facade()

    def _apply_prepared_commit_tx_by_key(self, tx_key=DEFAULT_TRANSACTION, tx_token=None):
        tx_index = self.__yidl_tx_key_to_index__[tx_key]
        if self._y_working_tx_ids[tx_index] != tx_token:
            raise RuntimeError("stale yidl transaction token")
        if False:
            pass
        elif astichi_elif(commit_transaction_dispatch_body):
            pass
        with astichi_hole(commit_transaction_body) as astichi_fallback:
            pass
        self._y_working_tx_ids[tx_index] = None
        return self._y_get_default_facade()

    def _after_commit_tx_by_key(self, tx_key=DEFAULT_TRANSACTION, tx_token=None):
        del tx_token
        tx_index = self.__yidl_tx_key_to_index__[tx_key]
        if False:
            pass
        elif astichi_elif(after_commit_body):
            pass
        return self._y_get_default_facade()

    def _rollback_tx_by_key(self, tx_key=DEFAULT_TRANSACTION, tx_token=None):
        tx_index = self.__yidl_tx_key_to_index__[tx_key]
        del tx_token
        if False:
            pass
        elif astichi_elif(rollback_transaction_dispatch_body):
            pass
        with astichi_hole(rollback_transaction_body) as astichi_fallback:
            pass
        self._y_working_tx_ids[tx_index] = None
        return self._y_get_default_facade()

    def _after_rollback_tx_by_key(self, tx_key=DEFAULT_TRANSACTION, tx_token=None):
        del tx_token
        tx_index = self.__yidl_tx_key_to_index__[tx_key]
        if False:
            pass
        elif astichi_elif(after_rollback_body):
            pass
        return self._y_get_default_facade()

    with astichi_hole(commit_transaction_helpers) as astichi_fallback:
        pass
    with astichi_hole(rollback_transaction_helpers) as astichi_fallback:
        pass


class facade_base_decl_name__astichi_arg__(
    astichi_pass(decorated_cls, outer_bind=True)
):
    __slots__ = (
        ("_y_state",)
        if hasattr(astichi_pass(decorated_cls, outer_bind=True), "__weakref__")
        else ("_y_state", "__weakref__")
    )
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

    def begin(self, *tx_keys):
        return self._y_state._y_transaction_manager.begin(*tx_keys)

    def validate(self, *tx_keys):
        return self._y_state._y_transaction_manager.validate(*tx_keys)

    def commit_only(self, *tx_keys):
        return self._y_state._y_transaction_manager.commit_only(*tx_keys)

    def commit(self, *tx_keys):
        return self._y_state._y_transaction_manager.commit(*tx_keys)

    def rollback(self, *tx_keys):
        return self._y_state._y_transaction_manager.rollback(*tx_keys)

    with astichi_hole(facade_base_body) as astichi_fallback:
        pass
    with astichi_hole(facade_properties) as astichi_fallback:
        pass


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
    __yidl_tx_index_to_key__ = astichi_pass(
        tx_keys_for_class_index_name__astichi_arg__,
        outer_bind=True,
    )
    __yidl_tx_key_to_index__ = {
        key: index for index, key in enumerate(
            astichi_pass(
                tx_keys_for_class_map_name__astichi_arg__,
                outer_bind=True,
            )
        )
    }

    with astichi_hole(default_facade_properties) as astichi_fallback:
        pass

    def __init__(self, init_params__astichi_param_hole__):
        state = object.__new__(state_class_ref__astichi_arg__)
        object.__setattr__(self, "_y_state", state)
        object.__setattr__(self, "_y_current_facade", None)
        object.__setattr__(self, "_y_working_facade", None)
        state._y_transaction_manager = transaction_manager or TransactionManager(
            tx_keys=tuple(
                group for group in astichi_pass(
                    tx_keys_for_manager_name__astichi_arg__,
                    outer_bind=True,
                )
                if group != DEFAULT_TRANSACTION
            )
        )
        state._y_default_ref = weakref.ref(self)
        state._y_current_ref = None
        state._y_working_ref = None
        with astichi_hole(state_init_body) as astichi_fallback:
            pass
        state._y_working_tx_ids = [
            None
            for _group in astichi_pass(
                tx_keys_for_slots_name__astichi_arg__,
                outer_bind=True,
            )
        ]


class current_facade_class_decl_name__astichi_arg__(
    facade_base_current_base_name__astichi_arg__
):
    __slots__ = ()
    with astichi_hole(current_facade_properties) as astichi_fallback:
        pass


class working_facade_class_decl_name__astichi_arg__(
    facade_base_working_base_name__astichi_arg__
):
    __slots__ = ()
    with astichi_hole(working_facade_properties) as astichi_fallback:
        pass""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=350, keep_names=('DEFAULT_TRANSACTION', 'TransactionManager', 'VOID', 'weakref', '_HAS_DEFAULT_FACTORY'))), 'ReturnClass': astichi_template(from_astichi_code("""\
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
return return_class_result_ref__astichi_arg__""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=675)), 'BuildTransactionFactsBody': from_astichi_code("""\
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
        TxKeysCollection,
        TxKey(
            tx_owner=lifecycle_class.class_id,
            tx_key_key=DEFAULT_TRANSACTION,
            tx_index=0,
            tx_key_order=0,
            commit_order_key_function_name="_commit_order_key_tx_0",
            requires_validation_function_name="_requires_validation_tx_0",
            validate_commit_function_name="_validate_commit_tx_0",
            before_commit_function_name="_before_commit_tx_0",
            after_commit_function_name="_after_commit_tx_0",
            after_rollback_function_name="_after_rollback_tx_0",
            prepare_commit_fields_function_name="_prepare_commit_tx_0_fields",
            apply_prepared_commit_fields_function_name="_apply_prepared_commit_tx_0_fields",
            rollback_fields_function_name="_rollback_tx_0_fields",
        ),
        policy=RejectDuplicate,
    )

    for field in fields:
        if field.field_owner != lifecycle_class.class_id:
            continue
        if field.field_kind not in {"managed", "owned", "transient"}:
            continue

        tx_key = field.tx_key_key
        if tx_key is None:
            tx_key = DEFAULT_TRANSACTION
        if tx_key not in seen:
            seen[tx_key] = len(seen)
            ctx.write(
                TxKeysCollection,
                TxKey(
                    tx_owner=lifecycle_class.class_id,
                    tx_key_key=tx_key,
                    tx_index=seen[tx_key],
                    tx_key_order=field.field_order,
                    commit_order_key_function_name=(
                        f"_commit_order_key_tx_{seen[tx_key]}"
                    ),
                    requires_validation_function_name=(
                        f"_requires_validation_tx_{seen[tx_key]}"
                    ),
                    validate_commit_function_name=(
                        f"_validate_commit_tx_{seen[tx_key]}"
                    ),
                    before_commit_function_name=(
                        f"_before_commit_tx_{seen[tx_key]}"
                    ),
                    after_commit_function_name=(
                        f"_after_commit_tx_{seen[tx_key]}"
                    ),
                    after_rollback_function_name=(
                        f"_after_rollback_tx_{seen[tx_key]}"
                    ),
                    prepare_commit_fields_function_name=(
                        f"_prepare_commit_tx_{seen[tx_key]}_fields"
                    ),
                    apply_prepared_commit_fields_function_name=(
                        f"_apply_prepared_commit_tx_{seen[tx_key]}_fields"
                    ),
                    rollback_fields_function_name=(
                        f"_rollback_tx_{seen[tx_key]}_fields"
                    ),
                ),
                policy=RejectDuplicate,
            )

        tx_index = seen[tx_key]
        ctx.write(
            TransactionalFieldsCollection,
            TransactionalField(
                field_id=field.field_id,
                field_owner=field.field_owner,
                field_name=field.field_name,
                field_order=field.field_order,
                tx_key_key=tx_key,
            ),
            policy=RejectDuplicate,
        )
        if field.field_kind != "managed":
            continue
        ctx.write(
            IndexedTransactionalFieldsCollection,
            IndexedTransactionalField(
                field_id=field.field_id,
                field_owner=field.field_owner,
                field_name=field.field_name,
                field_order=field.field_order,
                tx_key_key=tx_key,
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
        )""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=77, keep_names=('ctx', 'ClassesCollection', 'FieldsCollection', 'TxKeysCollection', 'TransactionalFieldsCollection', 'IndexedTransactionalFieldsCollection', 'TxKey', 'TransactionalField', 'IndexedTransactionalField', 'RejectDuplicate')), 'ManagedCurrentStateAssignment': astichi_template(from_astichi_code("""\
astichi_pass(state, outer_bind=True).astichi_ref(external=current_slot)._ = astichi_pass(
    init_value_name__astichi_arg__,
    outer_bind=True,
)""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=211)), 'ManagedWorkingStateAssignment': astichi_template(from_astichi_code('astichi_pass(state, outer_bind=True).astichi_ref(external=working_slot)._ = VOID', file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=218, keep_names=('VOID',))), 'ManagedStagedStateAssignment': astichi_template(from_astichi_code('astichi_pass(state, outer_bind=True).astichi_ref(external=staged_slot)._ = VOID', file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=224, keep_names=('VOID',))), 'ManagedDefaultProperty': astichi_template(from_astichi_code("""\
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
    state.astichi_ref(external=working_slot)._ = value""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=230, keep_names=('VOID',))), 'ManagedCurrentProperty': astichi_template(from_astichi_code("""\
@property
def property_getter_name__astichi_arg__(self):
    return self._y_state.astichi_ref(external=current_slot)

@property_setter_target_name__astichi_arg__.setter
def property_setter_name__astichi_arg__(self, value):
    del value
    raise AttributeError(
        "current facade is read-only for transactional field "
        + astichi_bind_external(field_name)
    )""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=247)), 'ManagedWorkingProperty': astichi_template(from_astichi_code("""\
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
    state.astichi_ref(external=working_slot)._ = value""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=261, keep_names=('VOID',))), 'ManagedThawWorkingProperty': astichi_template(from_astichi_code("""\
@property
def property_getter_name__astichi_arg__(self):
    state = self._y_state
    if state.astichi_ref(external=working_slot) is not VOID:
        return state.astichi_ref(external=working_slot)
    tx_key = state.__yidl_tx_index_to_key__[
        astichi_bind_external(working_tx_index)
    ]
    if state._y_transaction_manager.active_transaction_for(tx_key) is None:
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
    state.astichi_ref(external=working_slot)._ = value""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=278, keep_names=('VOID',))), 'ManagedOptionalThawWorkingProperty': astichi_template(from_astichi_code("""\
@property
def property_getter_name__astichi_arg__(self):
    state = self._y_state
    if state.astichi_ref(external=working_slot) is not VOID:
        return state.astichi_ref(external=working_slot)
    tx_key = state.__yidl_tx_index_to_key__[
        astichi_bind_external(working_tx_index)
    ]
    if state._y_transaction_manager.active_transaction_for(tx_key) is None:
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
    state.astichi_ref(external=working_slot)._ = value""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=305, keep_names=('VOID',))), 'ManagedPlainPrepareBranch': astichi_template(from_astichi_code("""\
if astichi_pass(self, outer_bind=True).astichi_ref(external=working_slot) is not VOID:
    astichi_pass(self, outer_bind=True).astichi_ref(external=staged_slot)._ = (
        astichi_pass(self, outer_bind=True).astichi_ref(external=working_slot)
    )""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=335, keep_names=('VOID',))), 'ManagedFreezePrepareBranch': astichi_template(from_astichi_code("""\
if astichi_pass(self, outer_bind=True).astichi_ref(external=working_slot) is not VOID:
    astichi_pass(self, outer_bind=True).astichi_ref(external=staged_slot)._ = (
        freeze_func_name__astichi_arg__(
            astichi_pass(self, outer_bind=True).astichi_ref(external=working_slot)
        )
    )""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=344, keep_names=('VOID',))), 'ManagedOptionalFreezePrepareBranch': astichi_template(from_astichi_code("""\
if astichi_pass(self, outer_bind=True).astichi_ref(external=working_slot) is not VOID:
    astichi_pass(self, outer_bind=True).astichi_ref(external=staged_slot)._ = (
        None
        if astichi_pass(self, outer_bind=True).astichi_ref(external=working_slot) is None
        else freeze_func_name__astichi_arg__(
            astichi_pass(self, outer_bind=True).astichi_ref(external=working_slot)
        )
    )""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=355, keep_names=('VOID',))), 'ManagedApplyPreparedCommitBranch': astichi_template(from_astichi_code("""\
if astichi_pass(self, outer_bind=True).astichi_ref(external=staged_slot) is not VOID:
    astichi_pass(self, outer_bind=True).astichi_ref(external=current_slot)._ = (
        astichi_pass(self, outer_bind=True).astichi_ref(external=staged_slot)
    )
    astichi_pass(self, outer_bind=True).astichi_ref(external=staged_slot)._ = VOID
    astichi_pass(self, outer_bind=True).astichi_ref(external=working_slot)._ = VOID""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=368, keep_names=('VOID',))), 'ManagedRollbackBranch': astichi_template(from_astichi_code("""\
astichi_pass(self, outer_bind=True).astichi_ref(external=staged_slot)._ = VOID
astichi_pass(self, outer_bind=True).astichi_ref(external=working_slot)._ = VOID""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=379, keep_names=('VOID',))), 'CommitOrderKeyFunction': astichi_template(from_astichi_code("""\
def commit_order_key_function_name__astichi_arg__(self):
    with astichi_hole(commit_order_key_tx_body) as astichi_fallback:
        pass
    return ()""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=386)), 'RequiresValidationFunction': astichi_template(from_astichi_code("""\
def requires_validation_function_name__astichi_arg__(self):
    with astichi_hole(requires_validation_tx_body) as astichi_fallback:
        pass
    return False""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=393)), 'ValidateCommitFunction': astichi_template(from_astichi_code("""\
def validate_commit_function_name__astichi_arg__(self):
    with astichi_hole(validate_commit_tx_body) as astichi_fallback:
        pass
    return True""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=400)), 'BeforeCommitFunction': astichi_template(from_astichi_code("""\
def before_commit_function_name__astichi_arg__(self):
    with astichi_hole(before_commit_tx_body) as astichi_fallback:
        pass""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=407)), 'AfterCommitFunction': astichi_template(from_astichi_code("""\
def after_commit_function_name__astichi_arg__(self):
    with astichi_hole(after_commit_tx_body) as astichi_fallback:
        pass""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=413)), 'AfterRollbackFunction': astichi_template(from_astichi_code("""\
def after_rollback_function_name__astichi_arg__(self):
    with astichi_hole(after_rollback_tx_body) as astichi_fallback:
        pass""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=419)), 'CommitOrderKeyHelperCall': astichi_template(from_astichi_code("""\
return astichi_pass(
    self,
    outer_bind=True,
)._y_get_default_facade().astichi_ref(external=method_name)()""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=425)), 'RequiresValidationHelperCall': astichi_template(from_astichi_code('return True', file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=432)), 'ValidateCommitHelperCall': astichi_template(from_astichi_code("""\
result = astichi_pass(
    self,
    outer_bind=True,
)._y_get_default_facade().astichi_ref(external=method_name)()
if not result:
    return result""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=436)), 'TransactionHookHelperCall': astichi_template(from_astichi_code("""\
astichi_pass(
    self,
    outer_bind=True,
)._y_get_default_facade().astichi_ref(external=method_name)()""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=445)), 'CommitOrderKeyDispatchCall': astichi_template(from_astichi_code("""\
def astichi_elif():
    astichi_import(tx_index)
    astichi_import(self)

    if tx_index == astichi_bind_external(tx_index_value):
        return self.astichi_ref(external=commit_order_key_function_name)()""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=452)), 'RequiresValidationDispatchCall': astichi_template(from_astichi_code("""\
def astichi_elif():
    astichi_import(tx_index)
    astichi_import(self)

    if tx_index == astichi_bind_external(tx_index_value):
        return self.astichi_ref(external=requires_validation_function_name)()""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=461)), 'ValidateCommitDispatchCall': astichi_template(from_astichi_code("""\
def astichi_elif():
    astichi_import(tx_index)
    astichi_import(self)

    if tx_index == astichi_bind_external(tx_index_value):
        return self.astichi_ref(external=validate_commit_function_name)()""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=470)), 'BeforeCommitDispatchCall': astichi_template(from_astichi_code("""\
def astichi_elif():
    astichi_import(tx_index)
    astichi_import(self)

    if tx_index == astichi_bind_external(tx_index_value):
        self.astichi_ref(external=before_commit_function_name)()""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=479)), 'AfterCommitDispatchCall': astichi_template(from_astichi_code("""\
def astichi_elif():
    astichi_import(tx_index)
    astichi_import(self)

    if tx_index == astichi_bind_external(tx_index_value):
        self.astichi_ref(external=after_commit_function_name)()""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=488)), 'AfterRollbackDispatchCall': astichi_template(from_astichi_code("""\
def astichi_elif():
    astichi_import(tx_index)
    astichi_import(self)

    if tx_index == astichi_bind_external(tx_index_value):
        self.astichi_ref(external=after_rollback_function_name)()""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=497)), 'PrepareCommitFieldsFunction': astichi_template(from_astichi_code("""\
def prepare_commit_fields_function_name__astichi_arg__(self):
    with astichi_hole(prepare_commit_fields_body) as astichi_fallback:
        pass""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=506)), 'ApplyPreparedCommitFieldsFunction': astichi_template(from_astichi_code("""\
def apply_prepared_commit_fields_function_name__astichi_arg__(self):
    with astichi_hole(apply_prepared_commit_fields_body) as astichi_fallback:
        pass""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=512)), 'RollbackFieldsFunction': astichi_template(from_astichi_code("""\
def rollback_fields_function_name__astichi_arg__(self):
    with astichi_hole(rollback_fields_body) as astichi_fallback:
        pass""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=518)), 'ApplyPreparedCommitDispatchBranch': astichi_template(from_astichi_code("""\
def astichi_elif():
    astichi_import(tx_index)
    astichi_import(self)

    if tx_index == astichi_bind_external(tx_index_value):
        self.astichi_ref(external=apply_prepared_commit_fields_function_name)()""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=524)), 'PrepareCommitDispatchBranch': astichi_template(from_astichi_code("""\
def astichi_elif():
    astichi_import(tx_index)
    astichi_import(self)

    if tx_index == astichi_bind_external(tx_index_value):
        self.astichi_ref(external=prepare_commit_fields_function_name)()""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=533)), 'RollbackDispatchBranch': astichi_template(from_astichi_code("""\
def astichi_elif():
    astichi_import(tx_index)
    astichi_import(self)

    if tx_index == astichi_bind_external(tx_index_value):
        self.astichi_ref(external=rollback_fields_function_name)()""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl', line_number=542)), 'BuildDefaultFactoryFactsBody': from_astichi_code("""\
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
            if (
                consumer.field_kind == "static"
                and provider.field_kind == "initvar"
            ):
                add_diagnostic(
                    consumer,
                    f"static_initvar.{param_name}",
                    (
                        f"{lifecycle_class.class_name}."
                        f"{consumer.field_name}: static default_factory "
                        f"cannot reference initvar {param_name!r} "
                        "until retained initvar support is enabled"
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
                consumer_field_kind=consumer.field_kind,
                consumer_field_order=consumer.field_order,
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

    for field in factory_fields:
        if field.default_factory_param_names:
            continue
        ctx.write(
            DefaultFactoryDependenciesCollection,
            DefaultFactoryDependency(
                dependency_owner=lifecycle_class.class_id,
                consumer_field_id=field.field_id,
                consumer_field_name=field.field_name,
                consumer_field_kind=field.field_kind,
                consumer_field_order=field.field_order,
                provider_name="",
                provider_field_id="",
                provider_field_kind="",
                provider_init=True,
                provider_has_default=False,
                provider_has_default_factory=False,
                param_name="",
                param_order=-1,
                consumer_eval_order=eval_order_by_id[field.field_id],
            ),
            policy=RejectDuplicate,
        )

    for eval_order, field_id in enumerate(ordered_field_ids):
        field = by_id[field_id]
        state_slot = ""
        if field.value_slot_name:
            state_slot = field.value_slot_name
        elif field.field_kind == "managed":
            state_slot = field.current_slot_name
        elif field.field_kind == "owned":
            state_slot = field.current_slot_name
        elif field.field_kind == "transient":
            state_slot = field.current_slot_name
        ctx.write(
            DefaultFactoryEvaluationStepsCollection,
            DefaultFactoryEvaluationStep(
                eval_step_id=field.field_id,
                eval_owner=lifecycle_class.class_id,
                eval_field_id=field.field_id,
                eval_field_name=field.field_name,
                eval_field_kind=field.field_kind,
                eval_binding_shape=field.binding_shape,
                eval_init=field.init,
                eval_state_slot_name=state_slot,
                eval_default_factory_param_name=(
                    field.default_factory_param_name
                ),
                eval_order=eval_order,
                eval_statement_order=100000 + eval_order,
            ),
            policy=RejectDuplicate,
        )""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_default_factories.yidl', line_number=91, keep_names=('ctx', 'ClassesCollection', 'FieldsCollection', 'DefaultFactoryDependenciesCollection', 'DefaultFactoryEvaluationStepsCollection', 'DefaultFactoryDiagnosticsCollection', 'DefaultFactoryDependency', 'DefaultFactoryEvaluationStep', 'DefaultFactoryDiagnostic', 'RejectDuplicate', 'ReplaceExisting')), 'RaiseDefaultFactoryDiagnosticsBody': from_astichi_code("""\
for diagnostic in ctx.records(DefaultFactoryDiagnosticsCollection):
    raise AssemblyDiagnosticError(diagnostic.diagnostic_message)""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_default_factories.yidl', line_number=322, keep_names=('ctx', 'DefaultFactoryDiagnosticsCollection', 'AssemblyDiagnosticError')), 'InitParamDefaultFactory': astichi_template(from_astichi_code("""\
def astichi_params(
    param_name__astichi_arg__: astichi_bind_external(annotation)
    = _HAS_DEFAULT_FACTORY
):
    pass""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_default_factories.yidl', line_number=338, keep_names=('_HAS_DEFAULT_FACTORY',))), 'StoredDefaultFactoryEvalInit': astichi_template(from_astichi_code("""\
if astichi_pass(field_name__astichi_arg__, outer_bind=True) is _HAS_DEFAULT_FACTORY:
    astichi_pass(field_name__astichi_arg__, outer_bind=True)._ = (
        default_factory_name__astichi_arg__(
            **astichi_hole(default_factory_args)
        )
    )
astichi_pass(state, outer_bind=True).astichi_ref(external=state_slot)._ = astichi_pass(
    field_name__astichi_arg__,
    outer_bind=True,
)""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_default_factories.yidl', line_number=348, keep_names=('_HAS_DEFAULT_FACTORY',))), 'StoredDefaultFactoryEvalNoInit': astichi_template(from_astichi_code("""\
field_name__astichi_arg__ = default_factory_name__astichi_arg__(
    **astichi_hole(default_factory_args)
)
astichi_pass(state, outer_bind=True).astichi_ref(external=state_slot)._ = astichi_pass(
    field_name__astichi_arg__,
    outer_bind=True,
)""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_default_factories.yidl', line_number=363)), 'InitVarDefaultFactoryEvalInit': astichi_template(from_astichi_code("""\
if astichi_pass(field_name__astichi_arg__, outer_bind=True) is _HAS_DEFAULT_FACTORY:
    astichi_pass(field_name__astichi_arg__, outer_bind=True)._ = (
        default_factory_name__astichi_arg__(
            **astichi_hole(default_factory_args)
        )
    )""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_default_factories.yidl', line_number=373, keep_names=('_HAS_DEFAULT_FACTORY',))), 'InitVarDefaultFactoryEvalNoInit': astichi_template(from_astichi_code("""\
field_name__astichi_arg__ = default_factory_name__astichi_arg__(
    **astichi_hole(default_factory_args)
)""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_default_factories.yidl', line_number=384)), 'DefaultFactoryStoredArg': astichi_template(from_astichi_code("""\
astichi_funcargs(
    param_name__astichi_arg__=astichi_pass(
        self,
        outer_bind=True,
    ).astichi_ref(external=provider_name)
)""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_default_factories.yidl', line_number=390)), 'DefaultFactoryLocalArg': astichi_template(from_astichi_code("""\
astichi_funcargs(
    param_name__astichi_arg__=astichi_pass(
        provider_name__astichi_arg__,
        outer_bind=True,
    )
)""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_default_factories.yidl', line_number=399)), 'DefaultFactoryEmptyArg': astichi_template(from_astichi_code('astichi_funcargs()', file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_default_factories.yidl', line_number=408)), 'BuildTransientFactsBody': from_astichi_code("""\
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION

fields = list(ctx.records(FieldsCollection))
by_owner_name = {
    (field.field_owner, field.field_name): field
    for field in fields
}
tx_keys = {
    (tx_key.tx_owner, tx_key.tx_key_key): tx_key.tx_index
    for tx_key in ctx.records(TxKeysCollection)
}
for field in fields:
    if field.field_kind != "transient":
        continue
    tx_key = field.tx_key_key
    if tx_key is None:
        tx_key = DEFAULT_TRANSACTION
    tx_index = tx_keys[(field.field_owner, tx_key)]
    ctx.write(
        IndexedTransientFieldsCollection,
        IndexedTransientField(
            field_id=field.field_id,
            field_owner=field.field_owner,
            field_name=field.field_name,
            field_order=field.field_order,
            tx_key_key=tx_key,
            tx_index=tx_index,
            current_slot_name=field.current_slot_name,
            working_slot_name=field.working_slot_name,
            has_working_default_factory=field.has_working_default_factory,
            working_default_factory_param_name=(
                field.working_default_factory_param_name
            ),
        ),
        policy=RejectDuplicate,
    )
    if (
        field.has_working_default_factory
        and not field.working_default_factory_param_names
    ):
        ctx.write(
            TransientWorkingFactoryArgsCollection,
            TransientWorkingFactoryArg(
                working_factory_arg_id=f"{field.field_id}.__empty__",
                working_factory_arg_owner=field.field_owner,
                working_factory_consumer_field_id=field.field_id,
                working_factory_consumer_field_order=field.field_order,
                param_name="",
                param_order=-1,
                provider_name="",
                working_factory_arg_kind="empty",
                retained_slot_name="",
            ),
            policy=RejectDuplicate,
        )
    for param_order, param_name in enumerate(
        field.working_default_factory_param_names
    ):
        arg_kind = ""
        provider_name = param_name
        retained_slot_name = ""
        if param_name in {"self", "current", "working"}:
            arg_kind = param_name
        else:
            provider = by_owner_name.get((field.field_owner, param_name))
            if provider is None:
                raise AssemblyDiagnosticError(
                    f"{field.field_name}: working_default_factory "
                    f"references unknown name {param_name!r}"
                )
            if provider.field_kind != "initvar":
                raise AssemblyDiagnosticError(
                    f"{field.field_name}: working_default_factory "
                    f"cannot retain non-initvar provider {param_name!r}"
                )
            if (
                not provider.init
                and not provider.has_default
                and not provider.has_default_factory
            ):
                raise AssemblyDiagnosticError(
                    f"{field.field_name}: working_default_factory "
                    f"cannot retain initvar {param_name!r} without "
                    "a default or default_factory"
                )
            arg_kind = "retained_initvar"
            retained_slot_name = f"_y_{param_name}_initvar"
            ctx.write(
                RetainedInitVarsCollection,
                RetainedInitVar(
                    field_id=provider.field_id,
                    field_owner=provider.field_owner,
                    field_name=provider.field_name,
                    field_order=provider.field_order,
                    retained_slot_name=retained_slot_name,
                    retain_order=200000 + provider.field_order,
                ),
                policy=ReplaceExisting,
            )
        ctx.write(
            TransientWorkingFactoryArgsCollection,
            TransientWorkingFactoryArg(
                working_factory_arg_id=f"{field.field_id}.{param_name}",
                working_factory_arg_owner=field.field_owner,
                working_factory_consumer_field_id=field.field_id,
                working_factory_consumer_field_order=field.field_order,
                param_name=param_name,
                param_order=param_order,
                provider_name=provider_name,
                working_factory_arg_kind=arg_kind,
                retained_slot_name=retained_slot_name,
            ),
            policy=RejectDuplicate,
        )""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_transient.yidl', line_number=65, keep_names=('ctx', 'FieldsCollection', 'TxKeysCollection', 'IndexedTransientFieldsCollection', 'IndexedTransientField', 'RetainedInitVarsCollection', 'RetainedInitVar', 'TransientWorkingFactoryArgsCollection', 'TransientWorkingFactoryArg', 'RejectDuplicate', 'ReplaceExisting', 'AssemblyDiagnosticError')), 'TransientCurrentProperty': astichi_template(from_astichi_code("""\
@property
def property_getter_name__astichi_arg__(self):
    return self._y_state.astichi_ref(external=current_slot)""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_transient.yidl', line_number=193)), 'TransientWorkingStateAssignment': astichi_template(from_astichi_code('astichi_pass(state, outer_bind=True).astichi_ref(external=working_slot)._ = VOID', file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_transient.yidl', line_number=199, keep_names=('VOID',))), 'TransientFacadeProperty': astichi_template(from_astichi_code("""\
@property
def property_getter_name__astichi_arg__(self):
    state = self._y_state
    if state.astichi_ref(external=working_slot) is not VOID:
        return state.astichi_ref(external=working_slot)
    tx_key = state.__yidl_tx_index_to_key__[astichi_bind_external(tx_index)]
    if state._y_transaction_manager.active_transaction_for(tx_key) is None:
        return state.astichi_ref(external=current_slot)
    state._y_ensure_working_transaction(astichi_bind_external(tx_index))
    state.astichi_ref(external=working_slot)._ = (
        state.astichi_ref(external=current_slot)
    )
    return state.astichi_ref(external=working_slot)

@property_setter_target_name__astichi_arg__.setter
def property_setter_name__astichi_arg__(self, value):
    state = self._y_state
    state._y_ensure_working_transaction(astichi_bind_external(tx_index))
    state.astichi_ref(external=working_slot)._ = value""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_transient.yidl', line_number=205, keep_names=('VOID',))), 'TransientWorkingDefaultFactoryProperty': astichi_template(from_astichi_code("""\
@property
def property_getter_name__astichi_arg__(self):
    state = self._y_state
    if state.astichi_ref(external=working_slot) is not VOID:
        return state.astichi_ref(external=working_slot)
    tx_key = state.__yidl_tx_index_to_key__[astichi_bind_external(tx_index)]
    if state._y_transaction_manager.active_transaction_for(tx_key) is None:
        return state.astichi_ref(external=current_slot)
    state._y_ensure_working_transaction(astichi_bind_external(tx_index))
    state.astichi_ref(external=working_slot)._ = (
        working_default_factory_name__astichi_arg__(
            **astichi_hole(working_default_factory_args)
        )
    )
    return state.astichi_ref(external=working_slot)

@property_setter_target_name__astichi_arg__.setter
def property_setter_name__astichi_arg__(self, value):
    state = self._y_state
    state._y_ensure_working_transaction(astichi_bind_external(tx_index))
    state.astichi_ref(external=working_slot)._ = value""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_transient.yidl', line_number=229, keep_names=('VOID',))), 'TransientClearWorkingBranch': astichi_template(from_astichi_code('astichi_pass(self, outer_bind=True).astichi_ref(external=working_slot)._ = VOID', file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_transient.yidl', line_number=255, keep_names=('VOID',))), 'RetainedInitVarAssignment': astichi_template(from_astichi_code("""\
astichi_pass(state, outer_bind=True).astichi_ref(external=retained_slot)._ = astichi_pass(
    init_value_name__astichi_arg__,
    outer_bind=True,
)""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_transient.yidl', line_number=261)), 'TransientWorkingFactorySelfArg': astichi_template(from_astichi_code("""\
astichi_funcargs(
    param_name__astichi_arg__=astichi_pass(
        state,
        outer_bind=True,
    )._y_get_default_facade()
)""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_transient.yidl', line_number=268)), 'TransientWorkingFactoryCurrentArg': astichi_template(from_astichi_code("""\
astichi_funcargs(
    param_name__astichi_arg__=astichi_pass(
        state,
        outer_bind=True,
    )._y_get_current_facade()
)""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_transient.yidl', line_number=277)), 'TransientWorkingFactoryWorkingArg': astichi_template(from_astichi_code("""\
astichi_funcargs(
    param_name__astichi_arg__=astichi_pass(
        state,
        outer_bind=True,
    )._y_get_working_facade()
)""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_transient.yidl', line_number=286)), 'TransientWorkingFactoryRetainedInitVarArg': astichi_template(from_astichi_code("""\
astichi_funcargs(
    param_name__astichi_arg__=astichi_pass(
        state,
        outer_bind=True,
    ).astichi_ref(external=retained_slot)
)""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_transient.yidl', line_number=295)), 'TransientWorkingFactoryEmptyArg': astichi_template(from_astichi_code('astichi_funcargs()', file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_transient.yidl', line_number=304)), 'BuildOwnedFactsBody': from_astichi_code("""\
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION

tx_keys = {
    (tx_key.tx_owner, tx_key.tx_key_key): tx_key.tx_index
    for tx_key in ctx.records(TxKeysCollection)
}
for field in ctx.records(FieldsCollection):
    if field.field_kind != "owned":
        continue
    tx_key = field.tx_key_key
    if tx_key is None:
        tx_key = DEFAULT_TRANSACTION
    ctx.write(
        IndexedOwnedFieldsCollection,
        IndexedOwnedField(
            field_id=field.field_id,
            field_owner=field.field_owner,
            field_name=field.field_name,
            field_order=field.field_order,
            binding_shape=field.binding_shape,
            tx_key_key=tx_key,
            tx_index=tx_keys[(field.field_owner, tx_key)],
            current_slot_name=field.current_slot_name,
            working_slot_name=field.working_slot_name,
            staged_slot_name=field.staged_slot_name,
        ),
        policy=RejectDuplicate,
    )""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl', line_number=44, keep_names=('ctx', 'FieldsCollection', 'TxKeysCollection', 'IndexedOwnedFieldsCollection', 'IndexedOwnedField', 'RejectDuplicate')), 'BindingSupportHelper': from_astichi_code("""\
astichi_pyimport(module=collections.abc, names=(Mapping,))
astichi_pyimport(module=yidl.runtime.bindings, names=(BindingBase, BindingDict,))

def _y_validate_binding_value(field_name, value):
    if value is not None and not isinstance(value, BindingBase):
        raise TypeError(
            "binding field " + repr(field_name)
            + " expects BindingBase or None"
        )
    return value

def _y_validate_binding_map_value(field_name, value):

    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise TypeError(
            "binding map field " + repr(field_name)
            + " expects a mapping or None"
        )
    result = value if isinstance(value, BindingDict) else BindingDict(value)
    for key, item in result.items():
        if not isinstance(item, BindingBase):
            raise TypeError(
                "binding map field " + repr(field_name)
                + " expects BindingBase values; key "
                + repr(key)
                + " has "
                + type(item).__name__
            )
    return result""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl', line_number=84), 'OwnedScalarStateAssignment': astichi_template(from_astichi_code("""\
value = astichi_pass(_y_validate_binding_value, outer_bind=True)(
    astichi_bind_external(field_name),
    astichi_pass(init_value_name__astichi_arg__, outer_bind=True),
)
astichi_pass(state, outer_bind=True).astichi_ref(external=state_slot)._ = value""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl', line_number=118)), 'OwnedMapStateAssignment': astichi_template(from_astichi_code("""\
value = astichi_pass(_y_validate_binding_map_value, outer_bind=True)(
    astichi_bind_external(field_name),
    astichi_pass(init_value_name__astichi_arg__, outer_bind=True),
)
astichi_pass(state, outer_bind=True).astichi_ref(external=state_slot)._ = value""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl', line_number=126)), 'OwnedEmptyStateAssignment': astichi_template(from_astichi_code('astichi_pass(state, outer_bind=True).astichi_ref(external=state_slot)._ = VOID', file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl', line_number=134, keep_names=('VOID',))), 'OwnedDefaultProperty': astichi_template(from_astichi_code("""\
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
    state.astichi_ref(external=working_slot)._ = (
        astichi_pass(_y_validate_binding_value, outer_bind=True)(
            astichi_bind_external(field_name),
            value,
        )
    )""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl', line_number=140, keep_names=('VOID',))), 'OwnedMapDefaultProperty': astichi_template(from_astichi_code("""\
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
    state.astichi_ref(external=working_slot)._ = (
        astichi_pass(_y_validate_binding_map_value, outer_bind=True)(
            astichi_bind_external(field_name),
            value,
        )
    )""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl', line_number=162, keep_names=('VOID',))), 'OwnedCurrentProperty': astichi_template(from_astichi_code("""\
@property
def property_getter_name__astichi_arg__(self):
    return self._y_state.astichi_ref(external=current_slot)

@property_setter_target_name__astichi_arg__.setter
def property_setter_name__astichi_arg__(self, value):
    del value
    raise AttributeError(
        "current facade is read-only for owned field "
        + astichi_bind_external(field_name)
    )""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl', line_number=184)), 'OwnedWorkingProperty': astichi_template(from_astichi_code("""\
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
    state.astichi_ref(external=working_slot)._ = (
        astichi_pass(_y_validate_binding_value, outer_bind=True)(
            astichi_bind_external(field_name),
            value,
        )
    )""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl', line_number=198, keep_names=('VOID',))), 'OwnedMapWorkingProperty': astichi_template(from_astichi_code("""\
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
    state.astichi_ref(external=working_slot)._ = (
        astichi_pass(_y_validate_binding_map_value, outer_bind=True)(
            astichi_bind_external(field_name),
            value,
        )
    )""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl', line_number=220, keep_names=('VOID',))), 'OwnedPrepareCommitBranch': astichi_template(from_astichi_code("""\
if astichi_pass(self, outer_bind=True).astichi_ref(external=working_slot) is not VOID:
    value = astichi_pass(self, outer_bind=True).astichi_ref(external=working_slot)
    if value is not None:
        value.accepted()
    astichi_pass(self, outer_bind=True).astichi_ref(external=staged_slot)._ = value""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl', line_number=242, keep_names=('VOID',))), 'OwnedMapPrepareCommitBranch': astichi_template(from_astichi_code("""\
if astichi_pass(self, outer_bind=True).astichi_ref(external=working_slot) is not VOID:
    value = astichi_pass(self, outer_bind=True).astichi_ref(external=working_slot)
    if value is not None:
        for item in value.values():
            item.accepted()
    astichi_pass(self, outer_bind=True).astichi_ref(external=staged_slot)._ = value""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl', line_number=252, keep_names=('VOID',))), 'OwnedScalarDefaultFactoryEvalInit': astichi_template(from_astichi_code("""\
if astichi_pass(field_name__astichi_arg__, outer_bind=True) is _HAS_DEFAULT_FACTORY:
    astichi_pass(field_name__astichi_arg__, outer_bind=True)._ = (
        default_factory_name__astichi_arg__(
            **astichi_hole(default_factory_args)
        )
    )
value = astichi_pass(_y_validate_binding_value, outer_bind=True)(
    astichi_bind_external(field_name_value),
    astichi_pass(field_name__astichi_arg__, outer_bind=True),
)
astichi_pass(state, outer_bind=True).astichi_ref(external=state_slot)._ = value""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl', line_number=263, keep_names=('_HAS_DEFAULT_FACTORY',))), 'OwnedScalarDefaultFactoryEvalNoInit': astichi_template(from_astichi_code("""\
field_name__astichi_arg__ = default_factory_name__astichi_arg__(
    **astichi_hole(default_factory_args)
)
value = astichi_pass(_y_validate_binding_value, outer_bind=True)(
    astichi_bind_external(field_name_value),
    astichi_pass(field_name__astichi_arg__, outer_bind=True),
)
astichi_pass(state, outer_bind=True).astichi_ref(external=state_slot)._ = value""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl', line_number=279)), 'OwnedMapDefaultFactoryEvalInit': astichi_template(from_astichi_code("""\
if astichi_pass(field_name__astichi_arg__, outer_bind=True) is _HAS_DEFAULT_FACTORY:
    astichi_pass(field_name__astichi_arg__, outer_bind=True)._ = (
        default_factory_name__astichi_arg__(
            **astichi_hole(default_factory_args)
        )
    )
value = astichi_pass(_y_validate_binding_map_value, outer_bind=True)(
    astichi_bind_external(field_name_value),
    astichi_pass(field_name__astichi_arg__, outer_bind=True),
)
astichi_pass(state, outer_bind=True).astichi_ref(external=state_slot)._ = value""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl', line_number=290, keep_names=('_HAS_DEFAULT_FACTORY',))), 'OwnedMapDefaultFactoryEvalNoInit': astichi_template(from_astichi_code("""\
field_name__astichi_arg__ = default_factory_name__astichi_arg__(
    **astichi_hole(default_factory_args)
)
value = astichi_pass(_y_validate_binding_map_value, outer_bind=True)(
    astichi_bind_external(field_name_value),
    astichi_pass(field_name__astichi_arg__, outer_bind=True),
)
astichi_pass(state, outer_bind=True).astichi_ref(external=state_slot)._ = value""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl', line_number=306)), 'OwnedApplyPreparedCommitBranch': astichi_template(from_astichi_code("""\
if astichi_pass(self, outer_bind=True).astichi_ref(external=staged_slot) is not VOID:
    astichi_pass(self, outer_bind=True).astichi_ref(external=current_slot)._ = (
        astichi_pass(self, outer_bind=True).astichi_ref(external=staged_slot)
    )
    astichi_pass(self, outer_bind=True).astichi_ref(external=staged_slot)._ = VOID
    astichi_pass(self, outer_bind=True).astichi_ref(external=working_slot)._ = VOID""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl', line_number=317, keep_names=('VOID',))), 'OwnedRollbackBranch': astichi_template(from_astichi_code("""\
astichi_pass(self, outer_bind=True).astichi_ref(external=staged_slot)._ = VOID
astichi_pass(self, outer_bind=True).astichi_ref(external=working_slot)._ = VOID""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl', line_number=328, keep_names=('VOID',))), 'BindingStateAssignment': astichi_template(from_astichi_code("""\
value = astichi_pass(_y_validate_binding_value, outer_bind=True)(
    astichi_bind_external(field_name),
    astichi_pass(init_value_name__astichi_arg__, outer_bind=True),
)
astichi_pass(state, outer_bind=True).astichi_ref(external=state_slot)._ = value""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl', line_number=335)), 'BindingMapStateAssignment': astichi_template(from_astichi_code("""\
value = astichi_pass(_y_validate_binding_map_value, outer_bind=True)(
    astichi_bind_external(field_name),
    astichi_pass(init_value_name__astichi_arg__, outer_bind=True),
)
astichi_pass(state, outer_bind=True).astichi_ref(external=state_slot)._ = value""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl', line_number=343)), 'BindingProperty': astichi_template(from_astichi_code("""\
@property
def property_getter_name__astichi_arg__(self):
    return self._y_state.astichi_ref(external=state_slot)

@property_setter_target_name__astichi_arg__.setter
def property_setter_name__astichi_arg__(self, value):
    self._y_state.astichi_ref(external=state_slot)._ = (
        astichi_pass(_y_validate_binding_value, outer_bind=True)(
            astichi_bind_external(field_name),
            value,
        )
    )""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl', line_number=351)), 'BindingMapProperty': astichi_template(from_astichi_code("""\
@property
def property_getter_name__astichi_arg__(self):
    return self._y_state.astichi_ref(external=state_slot)

@property_setter_target_name__astichi_arg__.setter
def property_setter_name__astichi_arg__(self, value):
    self._y_state.astichi_ref(external=state_slot)._ = (
        astichi_pass(_y_validate_binding_map_value, outer_bind=True)(
            astichi_bind_external(field_name),
            value,
        )
    )""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl', line_number=366)), 'BindingDefaultFactoryEvalInit': astichi_template(from_astichi_code("""\
if astichi_pass(field_name__astichi_arg__, outer_bind=True) is _HAS_DEFAULT_FACTORY:
    astichi_pass(field_name__astichi_arg__, outer_bind=True)._ = (
        default_factory_name__astichi_arg__(
            **astichi_hole(default_factory_args)
        )
    )
astichi_pass(self, outer_bind=True).astichi_ref(external=property_name)._ = astichi_pass(
    field_name__astichi_arg__,
    outer_bind=True,
)""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl', line_number=381, keep_names=('_HAS_DEFAULT_FACTORY',))), 'BindingDefaultFactoryEvalNoInit': astichi_template(from_astichi_code("""\
field_name__astichi_arg__ = default_factory_name__astichi_arg__(
    **astichi_hole(default_factory_args)
)
astichi_pass(self, outer_bind=True).astichi_ref(external=property_name)._ = astichi_pass(
    field_name__astichi_arg__,
    outer_bind=True,
)""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl', line_number=396)), 'ConstReadOnlyProperty': astichi_template(from_astichi_code("""\
@property
def property_getter_name__astichi_arg__(self):
    return self._y_state.astichi_ref(external=state_slot)

@property_setter_target_name__astichi_arg__.setter
def property_setter_name__astichi_arg__(self, value):
    del value
    raise AttributeError(
        f"const field {astichi_bind_external(field_name)!r} is read-only"
    )""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_const_static.yidl', line_number=21)), 'StaticInitAssignment': astichi_template(from_astichi_code("""\
if astichi_pass(init_value_name__astichi_arg__, outer_bind=True) is _HAS_DEFAULT_FACTORY:
    astichi_pass(state, outer_bind=True).astichi_ref(external=state_slot)._ = VOID
else:
    astichi_pass(state, outer_bind=True).astichi_ref(external=state_slot)._ = astichi_pass(
        init_value_name__astichi_arg__,
        outer_bind=True,
    )""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_const_static.yidl', line_number=34, keep_names=('_HAS_DEFAULT_FACTORY', 'VOID'))), 'StaticVoidAssignment': astichi_template(from_astichi_code('astichi_pass(state, outer_bind=True).astichi_ref(external=state_slot)._ = VOID', file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_const_static.yidl', line_number=46, keep_names=('VOID',))), 'StaticUnsetProperty': astichi_template(from_astichi_code("""\
@property
def property_getter_name__astichi_arg__(self):
    value = self._y_state.astichi_ref(external=state_slot)
    if value is VOID:
        raise AttributeError(
            f"static field {astichi_bind_external(field_name)!r} is not initialized"
        )
    return value

@property_setter_target_name__astichi_arg__.setter
def property_setter_name__astichi_arg__(self, value):
    state = self._y_state
    if state.astichi_ref(external=state_slot) is VOID:
        state.astichi_ref(external=state_slot)._ = value
        return
    raise AttributeError(
        f"static field {astichi_bind_external(field_name)!r} is already initialized"
    )""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_const_static.yidl', line_number=52, keep_names=('VOID',))), 'StaticDefaultProperty': astichi_template(from_astichi_code("""\
@property
def property_getter_name__astichi_arg__(self):
    state = self._y_state
    value = state.astichi_ref(external=state_slot)
    if value is VOID:
        value = astichi_pass(default_value_name__astichi_arg__, outer_bind=True)
        state.astichi_ref(external=state_slot)._ = value
    return value

@property_setter_target_name__astichi_arg__.setter
def property_setter_name__astichi_arg__(self, value):
    state = self._y_state
    if state.astichi_ref(external=state_slot) is VOID:
        state.astichi_ref(external=state_slot)._ = value
        return
    raise AttributeError(
        f"static field {astichi_bind_external(field_name)!r} is already initialized"
    )""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_const_static.yidl', line_number=75, keep_names=('VOID',))), 'StaticDefaultFactoryProperty': astichi_template(from_astichi_code("""\
@property
def property_getter_name__astichi_arg__(self):
    state = self._y_state
    value = state.astichi_ref(external=state_slot)
    if value is VOID:
        value = default_factory_name__astichi_arg__(
            **astichi_hole(static_default_factory_args)
        )
        state.astichi_ref(external=state_slot)._ = value
    return value

@property_setter_target_name__astichi_arg__.setter
def property_setter_name__astichi_arg__(self, value):
    state = self._y_state
    if state.astichi_ref(external=state_slot) is VOID:
        state.astichi_ref(external=state_slot)._ = value
        return
    raise AttributeError(
        f"static field {astichi_bind_external(field_name)!r} is already initialized"
    )""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_const_static.yidl', line_number=98, keep_names=('VOID',))), 'StaticDefaultFactoryEvalPlaceholder': astichi_template(from_astichi_code("""\
if False:
    default_factory_name__astichi_arg__(
        **astichi_hole(default_factory_args)
    )""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_const_static.yidl', line_number=123)), 'StaticDefaultFactoryStoredArg': astichi_template(from_astichi_code("""\
astichi_funcargs(
    param_name__astichi_arg__=astichi_pass(
        self,
        outer_bind=True,
    ).astichi_ref(external=provider_name)
)""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_const_static.yidl', line_number=130)), 'StaticDefaultFactoryEmptyArg': astichi_template(from_astichi_code('astichi_funcargs()', file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_const_static.yidl', line_number=139))}
ASSEMBLY_CONTRIBUTIONS = {'LifecycleDefinitionBuilderParam': ContributionSpec(name='LifecycleDefinitionBuilderParam', source_name='BuilderParam', source_kind='resource', build_name='LifecycleDefinitionBuilderParam', index=ValueRef('ClassOrder'), order=ValueRef('ClassOrder'), target=TargetSpec(name='builder_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='Root', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='value_name', value=ValueRef('LifecycleDefinitionParamName')),)), 'AnnotationsBuilderParam': ContributionSpec(name='AnnotationsBuilderParam', source_name='BuilderParam', source_kind='resource', build_name='AnnotationsBuilderParam', index=ValueRef('ClassOrder'), order=ValueRef('ClassOrder'), target=TargetSpec(name='builder_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='Root', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='value_name', value=ValueRef('AnnotationsParamName')),)), 'TxKeysBuilderParam': ContributionSpec(name='TxKeysBuilderParam', source_name='BuilderParam', source_kind='resource', build_name='TxKeysBuilderParam', index=ValueRef('ClassOrder'), order=ValueRef('ClassOrder'), target=TargetSpec(name='builder_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='Root', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='value_name', value=ValueRef('TxKeysParamName')),)), 'FieldDefaultBuilderParam': ContributionSpec(name='FieldDefaultBuilderParam', source_name='BuilderParam', source_kind='resource', build_name='FieldDefaultBuilderParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='builder_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='Root', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='value_name', value=ValueRef('DefaultValueParamName')),)), 'CommitOrderKeyFallback': ContributionSpec(name='CommitOrderKeyFallback', source_name='CommitOrderKeyFallbackBranch', source_kind='resource', build_name='CommitOrderKeyFallback', index=LiteralValueRef(1000000), order=LiteralValueRef(1000000), target=TargetSpec(name='commit_order_key_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=()), 'RequiresValidationFallback': ContributionSpec(name='RequiresValidationFallback', source_name='RequiresValidationFallbackBranch', source_kind='resource', build_name='RequiresValidationFallback', index=LiteralValueRef(1000000), order=LiteralValueRef(1000000), target=TargetSpec(name='requires_validation_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=()), 'ValidateCommitFallback': ContributionSpec(name='ValidateCommitFallback', source_name='ValidateCommitFallbackBranch', source_kind='resource', build_name='ValidateCommitFallback', index=LiteralValueRef(1000000), order=LiteralValueRef(1000000), target=TargetSpec(name='validate_commit_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=()), 'BeforeCommitFallback': ContributionSpec(name='BeforeCommitFallback', source_name='PassFallbackBranch', source_kind='resource', build_name='BeforeCommitFallback', index=LiteralValueRef(1000000), order=LiteralValueRef(1000000), target=TargetSpec(name='before_commit_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=()), 'PrepareCommitDispatchFallback': ContributionSpec(name='PrepareCommitDispatchFallback', source_name='PassFallbackBranch', source_kind='resource', build_name='PrepareCommitDispatchFallback', index=LiteralValueRef(1000000), order=LiteralValueRef(1000000), target=TargetSpec(name='prepare_commit_transaction_dispatch_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=()), 'CommitDispatchFallback': ContributionSpec(name='CommitDispatchFallback', source_name='PassFallbackBranch', source_kind='resource', build_name='CommitDispatchFallback', index=LiteralValueRef(1000000), order=LiteralValueRef(1000000), target=TargetSpec(name='commit_transaction_dispatch_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=()), 'AfterCommitFallback': ContributionSpec(name='AfterCommitFallback', source_name='PassFallbackBranch', source_kind='resource', build_name='AfterCommitFallback', index=LiteralValueRef(1000000), order=LiteralValueRef(1000000), target=TargetSpec(name='after_commit_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=()), 'RollbackDispatchFallback': ContributionSpec(name='RollbackDispatchFallback', source_name='PassFallbackBranch', source_kind='resource', build_name='RollbackDispatchFallback', index=LiteralValueRef(1000000), order=LiteralValueRef(1000000), target=TargetSpec(name='rollback_transaction_dispatch_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=()), 'AfterRollbackFallback': ContributionSpec(name='AfterRollbackFallback', source_name='PassFallbackBranch', source_kind='resource', build_name='AfterRollbackFallback', index=LiteralValueRef(1000000), order=LiteralValueRef(1000000), target=TargetSpec(name='after_rollback_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=()), 'ReturnClassContribution': ContributionSpec(name='ReturnClassContribution', source_name='ReturnClass', source_kind='resource', build_name='ReturnClass', index=ValueRef('ClassOrder'), order=ValueRef('ClassOrder'), target=TargetSpec(name='return_statement', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='Root', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='return_class_name_ref', value=ValueRef('ClassName')), BindingSpec(kind='ident', name='return_class_qualname_ref', value=ValueRef('ClassName')), BindingSpec(kind='ident', name='return_class_module_ref', value=ValueRef('ClassName')), BindingSpec(kind='ident', name='return_class_result_ref', value=ValueRef('ClassName')))), 'TransactionManagerInitParam': ContributionSpec(name='TransactionManagerInitParam', source_name='TransactionManagerParam', source_kind='resource', build_name='TransactionManagerInitParam', index=ValueRef('ClassOrder'), order=LiteralValueRef(0), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=()), 'PlainStateSlot': ContributionSpec(name='PlainStateSlot', source_name='StateSlotEntry', source_kind='resource', build_name='PlainStateSlot', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_slots', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='slot_name', value=ValueRef('ValueSlotName')),)), 'PlainInitParamRequired': ContributionSpec(name='PlainInitParamRequired', source_name='InitParamRequired', source_kind='resource', build_name='PlainInitParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')))), 'PlainInitParamDefault': ContributionSpec(name='PlainInitParamDefault', source_name='InitParamDefault', source_kind='resource', build_name='PlainInitParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')), BindingSpec(kind='ident', name='default_value_name', value=ValueRef('DefaultValueParamName')))), 'InitVarParamRequired': ContributionSpec(name='InitVarParamRequired', source_name='InitParamRequired', source_kind='resource', build_name='InitVarParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')))), 'InitVarParamDefault': ContributionSpec(name='InitVarParamDefault', source_name='InitParamDefault', source_kind='resource', build_name='InitVarParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')), BindingSpec(kind='ident', name='default_value_name', value=ValueRef('DefaultValueParamName')))), 'InitVarLocalDefault': ContributionSpec(name='InitVarLocalDefault', source_name='InitVarLocalDefaultAssignment', source_kind='resource', build_name='InitVarLocalDefault', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='init_value_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='default_value_name', value=ValueRef('DefaultValueParamName')))), 'PlainInitAssignment': ContributionSpec(name='PlainInitAssignment', source_name='PlainStateAssignment', source_kind='resource', build_name='PlainInitAssignment', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='init_value_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('ValueSlotName')))), 'PlainDefaultAssignment': ContributionSpec(name='PlainDefaultAssignment', source_name='PlainStateAssignment', source_kind='resource', build_name='PlainDefaultAssignment', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='init_value_name', value=ValueRef('DefaultValueParamName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('ValueSlotName')))), 'PlainFieldProperty': ContributionSpec(name='PlainFieldProperty', source_name='PlainProperty', source_kind='resource', build_name='PlainFieldProperty', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='property_getter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_target_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('ValueSlotName')))), 'ClassVarDefault': ContributionSpec(name='ClassVarDefault', source_name='ClassVarDefaultAssignment', source_kind='resource', build_name='ClassVarDefault', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='facade_base_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='classvar_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='classvar_value_name', value=ValueRef('DefaultValueParamName')))), 'CommitOrderKeyBranchContribution': ContributionSpec(name='CommitOrderKeyBranchContribution', source_name='CommitOrderKeyBranch', source_kind='resource', build_name='CommitOrderKeyBranch', index=ValueRef('DeclarationOrder'), order=ValueRef('DeclarationOrder'), target=TargetSpec(name='commit_order_key_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='method_name', value=ValueRef('MethodName')), BindingSpec(kind='external', name='tx_index_value', value=ValueRef('TxIndex')))), 'RequiresValidationBranchContribution': ContributionSpec(name='RequiresValidationBranchContribution', source_name='RequiresValidationBranch', source_kind='resource', build_name='RequiresValidationBranch', index=ValueRef('DeclarationOrder'), order=ValueRef('DeclarationOrder'), target=TargetSpec(name='requires_validation_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='tx_index_value', value=ValueRef('TxIndex')),)), 'ValidateCommitBranchContribution': ContributionSpec(name='ValidateCommitBranchContribution', source_name='ValidateCommitBranch', source_kind='resource', build_name='ValidateCommitBranch', index=ValueRef('DeclarationOrder'), order=ValueRef('DeclarationOrder'), target=TargetSpec(name='validate_commit_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='method_name', value=ValueRef('MethodName')), BindingSpec(kind='external', name='tx_index_value', value=ValueRef('TxIndex')))), 'BeforeCommitHookContribution': ContributionSpec(name='BeforeCommitHookContribution', source_name='TransactionHookCall', source_kind='resource', build_name='BeforeCommitHook', index=ValueRef('DeclarationOrder'), order=ValueRef('DeclarationOrder'), target=TargetSpec(name='before_commit_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='method_name', value=ValueRef('MethodName')), BindingSpec(kind='external', name='tx_index_value', value=ValueRef('TxIndex')))), 'AfterCommitHookContribution': ContributionSpec(name='AfterCommitHookContribution', source_name='TransactionHookCall', source_kind='resource', build_name='AfterCommitHook', index=ValueRef('DeclarationOrder'), order=ValueRef('DeclarationOrder'), target=TargetSpec(name='after_commit_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='method_name', value=ValueRef('MethodName')), BindingSpec(kind='external', name='tx_index_value', value=ValueRef('TxIndex')))), 'AfterRollbackHookContribution': ContributionSpec(name='AfterRollbackHookContribution', source_name='TransactionHookCall', source_kind='resource', build_name='AfterRollbackHook', index=ValueRef('DeclarationOrder'), order=ValueRef('DeclarationOrder'), target=TargetSpec(name='after_rollback_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='method_name', value=ValueRef('MethodName')), BindingSpec(kind='external', name='tx_index_value', value=ValueRef('TxIndex')))), 'CoreClassDefinition': ContributionSpec(name='CoreClassDefinition', source_name='CoreClassProduction', source_kind='production', build_name='ClassDef', index=ValueRef('ClassOrder'), order=ValueRef('ClassOrder'), target=TargetSpec(name='function_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='Root', indexes=()),))),)), bindings=()), 'ManagedCurrentStateSlot': ContributionSpec(name='ManagedCurrentStateSlot', source_name='StateSlotEntry', source_kind='resource', build_name='ManagedCurrentStateSlot', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_slots', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='slot_name', value=ValueRef('CurrentSlotName')),)), 'ManagedWorkingStateSlot': ContributionSpec(name='ManagedWorkingStateSlot', source_name='StateSlotEntry', source_kind='resource', build_name='ManagedWorkingStateSlot', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_slots', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='slot_name', value=ValueRef('WorkingSlotName')),)), 'ManagedStagedStateSlot': ContributionSpec(name='ManagedStagedStateSlot', source_name='StateSlotEntry', source_kind='resource', build_name='ManagedStagedStateSlot', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_slots', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='slot_name', value=ValueRef('StagedSlotName')),)), 'ManagedFreezeBuilderParam': ContributionSpec(name='ManagedFreezeBuilderParam', source_name='BuilderParam', source_kind='resource', build_name='ManagedFreezeBuilderParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='builder_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='Root', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='value_name', value=ValueRef('FreezeParamName')),)), 'ManagedThawBuilderParam': ContributionSpec(name='ManagedThawBuilderParam', source_name='BuilderParam', source_kind='resource', build_name='ManagedThawBuilderParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='builder_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='Root', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='value_name', value=ValueRef('ThawParamName')),)), 'ManagedInitParamDefault': ContributionSpec(name='ManagedInitParamDefault', source_name='InitParamDefault', source_kind='resource', build_name='ManagedInitParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')), BindingSpec(kind='ident', name='default_value_name', value=ValueRef('DefaultValueParamName')))), 'ManagedInitParamRequired': ContributionSpec(name='ManagedInitParamRequired', source_name='InitParamRequired', source_kind='resource', build_name='ManagedInitParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')))), 'ManagedCurrentInitAssignment': ContributionSpec(name='ManagedCurrentInitAssignment', source_name='ManagedCurrentStateAssignment', source_kind='resource', build_name='ManagedCurrentInitAssignment', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='init_value_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='current_slot', value=ValueRef('CurrentSlotName')))), 'ManagedCurrentDefaultAssignment': ContributionSpec(name='ManagedCurrentDefaultAssignment', source_name='ManagedCurrentStateAssignment', source_kind='resource', build_name='ManagedCurrentDefaultAssignment', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='init_value_name', value=ValueRef('DefaultValueParamName')), BindingSpec(kind='external', name='current_slot', value=ValueRef('CurrentSlotName')))), 'ManagedWorkingInitAssignment': ContributionSpec(name='ManagedWorkingInitAssignment', source_name='ManagedWorkingStateAssignment', source_kind='resource', build_name='ManagedWorkingInitAssignment', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='working_slot', value=ValueRef('WorkingSlotName')),)), 'ManagedStagedInitAssignment': ContributionSpec(name='ManagedStagedInitAssignment', source_name='ManagedStagedStateAssignment', source_kind='resource', build_name='ManagedStagedInitAssignment', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='staged_slot', value=ValueRef('StagedSlotName')),)), 'ManagedDefaultFacadeProperty': ContributionSpec(name='ManagedDefaultFacadeProperty', source_name='ManagedDefaultProperty', source_kind='resource', build_name='ManagedDefaultFacadeProperty', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='default_facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='property_getter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_target_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='current_slot', value=ValueRef('CurrentSlotName')), BindingSpec(kind='external', name='working_slot', value=ValueRef('WorkingSlotName')), BindingSpec(kind='external', name='tx_index', value=ValueRef('TxIndex')))), 'ManagedCurrentFacadeProperty': ContributionSpec(name='ManagedCurrentFacadeProperty', source_name='ManagedCurrentProperty', source_kind='resource', build_name='ManagedCurrentFacadeProperty', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='current_facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='property_getter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_target_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='current_slot', value=ValueRef('CurrentSlotName')), BindingSpec(kind='external', name='field_name', value=ValueRef('FieldName')))), 'ManagedWorkingFacadeProperty': ContributionSpec(name='ManagedWorkingFacadeProperty', source_name='ManagedWorkingProperty', source_kind='resource', build_name='ManagedWorkingFacadeProperty', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='working_facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='property_getter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_target_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='current_slot', value=ValueRef('CurrentSlotName')), BindingSpec(kind='external', name='working_slot', value=ValueRef('WorkingSlotName')), BindingSpec(kind='external', name='tx_index', value=ValueRef('TxIndex')))), 'ManagedThawWorkingFacadeProperty': ContributionSpec(name='ManagedThawWorkingFacadeProperty', source_name='ManagedThawWorkingProperty', source_kind='resource', build_name='ManagedWorkingFacadeProperty', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='working_facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='property_getter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_target_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='current_slot', value=ValueRef('CurrentSlotName')), BindingSpec(kind='external', name='working_slot', value=ValueRef('WorkingSlotName')), BindingSpec(kind='external', name='working_tx_index', value=ValueRef('TxIndex')), BindingSpec(kind='ident', name='thaw_func_name', value=ValueRef('ThawParamName')))), 'ManagedOptionalThawWorkingFacadeProperty': ContributionSpec(name='ManagedOptionalThawWorkingFacadeProperty', source_name='ManagedOptionalThawWorkingProperty', source_kind='resource', build_name='ManagedWorkingFacadeProperty', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='working_facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='property_getter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_target_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='current_slot', value=ValueRef('CurrentSlotName')), BindingSpec(kind='external', name='working_slot', value=ValueRef('WorkingSlotName')), BindingSpec(kind='external', name='working_tx_index', value=ValueRef('TxIndex')), BindingSpec(kind='ident', name='thaw_func_name', value=ValueRef('ThawParamName')))), 'ManagedPlainPrepareCommit': ContributionSpec(name='ManagedPlainPrepareCommit', source_name='ManagedPlainPrepareBranch', source_kind='resource', build_name='ManagedPrepareCommit', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='prepare_commit_fields_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='PrepareCommitFields', indexes=(ValueRef('TxIndex'),))))),)), bindings=(BindingSpec(kind='external', name='working_slot', value=ValueRef('WorkingSlotName')), BindingSpec(kind='external', name='staged_slot', value=ValueRef('StagedSlotName')))), 'ManagedFreezePrepareCommit': ContributionSpec(name='ManagedFreezePrepareCommit', source_name='ManagedFreezePrepareBranch', source_kind='resource', build_name='ManagedPrepareCommit', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='prepare_commit_fields_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='PrepareCommitFields', indexes=(ValueRef('TxIndex'),))))),)), bindings=(BindingSpec(kind='external', name='working_slot', value=ValueRef('WorkingSlotName')), BindingSpec(kind='external', name='staged_slot', value=ValueRef('StagedSlotName')), BindingSpec(kind='ident', name='freeze_func_name', value=ValueRef('FreezeParamName')))), 'ManagedOptionalFreezePrepareCommit': ContributionSpec(name='ManagedOptionalFreezePrepareCommit', source_name='ManagedOptionalFreezePrepareBranch', source_kind='resource', build_name='ManagedPrepareCommit', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='prepare_commit_fields_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='PrepareCommitFields', indexes=(ValueRef('TxIndex'),))))),)), bindings=(BindingSpec(kind='external', name='working_slot', value=ValueRef('WorkingSlotName')), BindingSpec(kind='external', name='staged_slot', value=ValueRef('StagedSlotName')), BindingSpec(kind='ident', name='freeze_func_name', value=ValueRef('FreezeParamName')))), 'ManagedApplyPreparedCommit': ContributionSpec(name='ManagedApplyPreparedCommit', source_name='ManagedApplyPreparedCommitBranch', source_kind='resource', build_name='ManagedApplyPreparedCommit', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='apply_prepared_commit_fields_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='ApplyPreparedCommitFields', indexes=(ValueRef('TxIndex'),))))),)), bindings=(BindingSpec(kind='external', name='current_slot', value=ValueRef('CurrentSlotName')), BindingSpec(kind='external', name='working_slot', value=ValueRef('WorkingSlotName')), BindingSpec(kind='external', name='staged_slot', value=ValueRef('StagedSlotName')))), 'ManagedRollback': ContributionSpec(name='ManagedRollback', source_name='ManagedRollbackBranch', source_kind='resource', build_name='ManagedRollback', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='rollback_fields_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='RollbackFields', indexes=(ValueRef('TxIndex'),))))),)), bindings=(BindingSpec(kind='external', name='working_slot', value=ValueRef('WorkingSlotName')), BindingSpec(kind='external', name='staged_slot', value=ValueRef('StagedSlotName')))), 'CommitOrderKeyHelper': ContributionSpec(name='CommitOrderKeyHelper', source_name='CommitOrderKeyFunction', source_kind='resource', build_name='CommitOrderKeyFunction', index=ValueRef('TxIndex'), order=ValueRef('TxIndex'), target=TargetSpec(name='commit_transaction_helpers', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='commit_order_key_function_name', value=ValueRef('CommitOrderKeyFunctionName')),)), 'RequiresValidationHelper': ContributionSpec(name='RequiresValidationHelper', source_name='RequiresValidationFunction', source_kind='resource', build_name='RequiresValidationFunction', index=ValueRef('TxIndex'), order=ValueRef('TxIndex'), target=TargetSpec(name='commit_transaction_helpers', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='requires_validation_function_name', value=ValueRef('RequiresValidationFunctionName')),)), 'ValidateCommitHelper': ContributionSpec(name='ValidateCommitHelper', source_name='ValidateCommitFunction', source_kind='resource', build_name='ValidateCommitFunction', index=ValueRef('TxIndex'), order=ValueRef('TxIndex'), target=TargetSpec(name='commit_transaction_helpers', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='validate_commit_function_name', value=ValueRef('ValidateCommitFunctionName')),)), 'BeforeCommitHelper': ContributionSpec(name='BeforeCommitHelper', source_name='BeforeCommitFunction', source_kind='resource', build_name='BeforeCommitFunction', index=ValueRef('TxIndex'), order=ValueRef('TxIndex'), target=TargetSpec(name='commit_transaction_helpers', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='before_commit_function_name', value=ValueRef('BeforeCommitFunctionName')),)), 'AfterCommitHelper': ContributionSpec(name='AfterCommitHelper', source_name='AfterCommitFunction', source_kind='resource', build_name='AfterCommitFunction', index=ValueRef('TxIndex'), order=ValueRef('TxIndex'), target=TargetSpec(name='commit_transaction_helpers', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='after_commit_function_name', value=ValueRef('AfterCommitFunctionName')),)), 'AfterRollbackHelper': ContributionSpec(name='AfterRollbackHelper', source_name='AfterRollbackFunction', source_kind='resource', build_name='AfterRollbackFunction', index=ValueRef('TxIndex'), order=ValueRef('TxIndex'), target=TargetSpec(name='rollback_transaction_helpers', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='after_rollback_function_name', value=ValueRef('AfterRollbackFunctionName')),)), 'CommitOrderKeyDispatch': ContributionSpec(name='CommitOrderKeyDispatch', source_name='CommitOrderKeyDispatchCall', source_kind='resource', build_name='CommitOrderKeyDispatch', index=ValueRef('TxIndex'), order=ValueRef('TxIndex'), target=TargetSpec(name='commit_order_key_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='commit_order_key_function_name', value=ValueRef('CommitOrderKeyFunctionName')), BindingSpec(kind='external', name='tx_index_value', value=ValueRef('TxIndex')))), 'RequiresValidationDispatch': ContributionSpec(name='RequiresValidationDispatch', source_name='RequiresValidationDispatchCall', source_kind='resource', build_name='RequiresValidationDispatch', index=ValueRef('TxIndex'), order=ValueRef('TxIndex'), target=TargetSpec(name='requires_validation_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='requires_validation_function_name', value=ValueRef('RequiresValidationFunctionName')), BindingSpec(kind='external', name='tx_index_value', value=ValueRef('TxIndex')))), 'ValidateCommitDispatch': ContributionSpec(name='ValidateCommitDispatch', source_name='ValidateCommitDispatchCall', source_kind='resource', build_name='ValidateCommitDispatch', index=ValueRef('TxIndex'), order=ValueRef('TxIndex'), target=TargetSpec(name='validate_commit_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='validate_commit_function_name', value=ValueRef('ValidateCommitFunctionName')), BindingSpec(kind='external', name='tx_index_value', value=ValueRef('TxIndex')))), 'BeforeCommitDispatch': ContributionSpec(name='BeforeCommitDispatch', source_name='BeforeCommitDispatchCall', source_kind='resource', build_name='BeforeCommitDispatch', index=ValueRef('TxIndex'), order=ValueRef('TxIndex'), target=TargetSpec(name='before_commit_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='before_commit_function_name', value=ValueRef('BeforeCommitFunctionName')), BindingSpec(kind='external', name='tx_index_value', value=ValueRef('TxIndex')))), 'AfterCommitDispatch': ContributionSpec(name='AfterCommitDispatch', source_name='AfterCommitDispatchCall', source_kind='resource', build_name='AfterCommitDispatch', index=ValueRef('TxIndex'), order=ValueRef('TxIndex'), target=TargetSpec(name='after_commit_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='after_commit_function_name', value=ValueRef('AfterCommitFunctionName')), BindingSpec(kind='external', name='tx_index_value', value=ValueRef('TxIndex')))), 'AfterRollbackDispatch': ContributionSpec(name='AfterRollbackDispatch', source_name='AfterRollbackDispatchCall', source_kind='resource', build_name='AfterRollbackDispatch', index=ValueRef('TxIndex'), order=ValueRef('TxIndex'), target=TargetSpec(name='after_rollback_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='after_rollback_function_name', value=ValueRef('AfterRollbackFunctionName')), BindingSpec(kind='external', name='tx_index_value', value=ValueRef('TxIndex')))), 'CommitOrderKeyHelperMethodCall': ContributionSpec(name='CommitOrderKeyHelperMethodCall', source_name='CommitOrderKeyHelperCall', source_kind='resource', build_name='CommitOrderKeyHelperMethodCall', index=ValueRef('DeclarationOrder'), order=ValueRef('DeclarationOrder'), target=TargetSpec(name='commit_order_key_tx_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='CommitOrderKeyFunction', indexes=(ValueRef('TxIndex'),))))),)), bindings=(BindingSpec(kind='external', name='method_name', value=ValueRef('MethodName')),)), 'RequiresValidationHelperMethodCall': ContributionSpec(name='RequiresValidationHelperMethodCall', source_name='RequiresValidationHelperCall', source_kind='resource', build_name='RequiresValidationHelperMethodCall', index=ValueRef('DeclarationOrder'), order=ValueRef('DeclarationOrder'), target=TargetSpec(name='requires_validation_tx_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='RequiresValidationFunction', indexes=(ValueRef('TxIndex'),))))),)), bindings=()), 'ValidateCommitHelperMethodCall': ContributionSpec(name='ValidateCommitHelperMethodCall', source_name='ValidateCommitHelperCall', source_kind='resource', build_name='ValidateCommitHelperMethodCall', index=ValueRef('DeclarationOrder'), order=ValueRef('DeclarationOrder'), target=TargetSpec(name='validate_commit_tx_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='ValidateCommitFunction', indexes=(ValueRef('TxIndex'),))))),)), bindings=(BindingSpec(kind='external', name='method_name', value=ValueRef('MethodName')),)), 'BeforeCommitHelperMethodCall': ContributionSpec(name='BeforeCommitHelperMethodCall', source_name='TransactionHookHelperCall', source_kind='resource', build_name='BeforeCommitHelperMethodCall', index=ValueRef('DeclarationOrder'), order=ValueRef('DeclarationOrder'), target=TargetSpec(name='before_commit_tx_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='BeforeCommitFunction', indexes=(ValueRef('TxIndex'),))))),)), bindings=(BindingSpec(kind='external', name='method_name', value=ValueRef('MethodName')),)), 'AfterCommitHelperMethodCall': ContributionSpec(name='AfterCommitHelperMethodCall', source_name='TransactionHookHelperCall', source_kind='resource', build_name='AfterCommitHelperMethodCall', index=ValueRef('DeclarationOrder'), order=ValueRef('DeclarationOrder'), target=TargetSpec(name='after_commit_tx_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='AfterCommitFunction', indexes=(ValueRef('TxIndex'),))))),)), bindings=(BindingSpec(kind='external', name='method_name', value=ValueRef('MethodName')),)), 'AfterRollbackHelperMethodCall': ContributionSpec(name='AfterRollbackHelperMethodCall', source_name='TransactionHookHelperCall', source_kind='resource', build_name='AfterRollbackHelperMethodCall', index=ValueRef('DeclarationOrder'), order=ValueRef('DeclarationOrder'), target=TargetSpec(name='after_rollback_tx_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='AfterRollbackFunction', indexes=(ValueRef('TxIndex'),))))),)), bindings=(BindingSpec(kind='external', name='method_name', value=ValueRef('MethodName')),)), 'PrepareCommitFields': ContributionSpec(name='PrepareCommitFields', source_name='PrepareCommitFieldsFunction', source_kind='resource', build_name='PrepareCommitFields', index=ValueRef('TxIndex'), order=ValueRef('TxIndex'), target=TargetSpec(name='commit_transaction_helpers', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='prepare_commit_fields_function_name', value=ValueRef('PrepareCommitFieldsFunctionName')),)), 'ApplyPreparedCommitFields': ContributionSpec(name='ApplyPreparedCommitFields', source_name='ApplyPreparedCommitFieldsFunction', source_kind='resource', build_name='ApplyPreparedCommitFields', index=ValueRef('TxIndex'), order=ValueRef('TxIndex'), target=TargetSpec(name='commit_transaction_helpers', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='apply_prepared_commit_fields_function_name', value=ValueRef('ApplyPreparedCommitFieldsFunctionName')),)), 'RollbackFields': ContributionSpec(name='RollbackFields', source_name='RollbackFieldsFunction', source_kind='resource', build_name='RollbackFields', index=ValueRef('TxIndex'), order=ValueRef('TxIndex'), target=TargetSpec(name='rollback_transaction_helpers', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='rollback_fields_function_name', value=ValueRef('RollbackFieldsFunctionName')),)), 'PrepareCommitDispatch': ContributionSpec(name='PrepareCommitDispatch', source_name='PrepareCommitDispatchBranch', source_kind='resource', build_name='PrepareCommitDispatch', index=ValueRef('TxIndex'), order=ValueRef('TxIndex'), target=TargetSpec(name='prepare_commit_transaction_dispatch_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='prepare_commit_fields_function_name', value=ValueRef('PrepareCommitFieldsFunctionName')), BindingSpec(kind='external', name='tx_index_value', value=ValueRef('TxIndex')))), 'ApplyPreparedCommitDispatch': ContributionSpec(name='ApplyPreparedCommitDispatch', source_name='ApplyPreparedCommitDispatchBranch', source_kind='resource', build_name='ApplyPreparedCommitDispatch', index=ValueRef('TxIndex'), order=ValueRef('TxIndex'), target=TargetSpec(name='commit_transaction_dispatch_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='apply_prepared_commit_fields_function_name', value=ValueRef('ApplyPreparedCommitFieldsFunctionName')), BindingSpec(kind='external', name='tx_index_value', value=ValueRef('TxIndex')))), 'RollbackDispatch': ContributionSpec(name='RollbackDispatch', source_name='RollbackDispatchBranch', source_kind='resource', build_name='RollbackDispatch', index=ValueRef('TxIndex'), order=ValueRef('TxIndex'), target=TargetSpec(name='rollback_transaction_dispatch_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='rollback_fields_function_name', value=ValueRef('RollbackFieldsFunctionName')), BindingSpec(kind='external', name='tx_index_value', value=ValueRef('TxIndex')))), 'FieldDefaultFactoryBuilderParam': ContributionSpec(name='FieldDefaultFactoryBuilderParam', source_name='BuilderParam', source_kind='resource', build_name='FieldDefaultFactoryBuilderParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='builder_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='Root', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='value_name', value=ValueRef('DefaultFactoryParamName')),)), 'PlainInitParamDefaultFactory': ContributionSpec(name='PlainInitParamDefaultFactory', source_name='InitParamDefaultFactory', source_kind='resource', build_name='PlainInitParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')))), 'InitVarParamDefaultFactory': ContributionSpec(name='InitVarParamDefaultFactory', source_name='InitParamDefaultFactory', source_kind='resource', build_name='InitVarParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')))), 'ManagedInitParamDefaultFactory': ContributionSpec(name='ManagedInitParamDefaultFactory', source_name='InitParamDefaultFactory', source_kind='resource', build_name='ManagedInitParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')))), 'StoredDefaultFactoryEvalInitContribution': ContributionSpec(name='StoredDefaultFactoryEvalInitContribution', source_name='StoredDefaultFactoryEvalInit', source_kind='resource', build_name='DefaultFactoryEval', index=ValueRef('EvalOrder'), order=ValueRef('EvalStatementOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='field_name', value=ValueRef('EvalFieldName')), BindingSpec(kind='ident', name='default_factory_name', value=ValueRef('EvalDefaultFactoryParamName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('EvalStateSlotName')))), 'StoredDefaultFactoryEvalNoInitContribution': ContributionSpec(name='StoredDefaultFactoryEvalNoInitContribution', source_name='StoredDefaultFactoryEvalNoInit', source_kind='resource', build_name='DefaultFactoryEval', index=ValueRef('EvalOrder'), order=ValueRef('EvalStatementOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='field_name', value=ValueRef('EvalFieldName')), BindingSpec(kind='ident', name='default_factory_name', value=ValueRef('EvalDefaultFactoryParamName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('EvalStateSlotName')))), 'InitVarDefaultFactoryEvalInitContribution': ContributionSpec(name='InitVarDefaultFactoryEvalInitContribution', source_name='InitVarDefaultFactoryEvalInit', source_kind='resource', build_name='DefaultFactoryEval', index=ValueRef('EvalOrder'), order=ValueRef('EvalStatementOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='field_name', value=ValueRef('EvalFieldName')), BindingSpec(kind='ident', name='default_factory_name', value=ValueRef('EvalDefaultFactoryParamName')))), 'InitVarDefaultFactoryEvalNoInitContribution': ContributionSpec(name='InitVarDefaultFactoryEvalNoInitContribution', source_name='InitVarDefaultFactoryEvalNoInit', source_kind='resource', build_name='DefaultFactoryEval', index=ValueRef('EvalOrder'), order=ValueRef('EvalStatementOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='field_name', value=ValueRef('EvalFieldName')), BindingSpec(kind='ident', name='default_factory_name', value=ValueRef('EvalDefaultFactoryParamName')))), 'DefaultFactoryStoredArgContribution': ContributionSpec(name='DefaultFactoryStoredArgContribution', source_name='DefaultFactoryStoredArg', source_kind='resource', build_name='DefaultFactoryArg', index=TupleValueRef((ValueRef('ConsumerEvalOrder'), ValueRef('ParamOrder'))), order=ValueRef('ParamOrder'), target=TargetSpec(name='default_factory_args', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='DefaultFactoryEval', indexes=(ValueRef('ConsumerEvalOrder'),))))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('ParamName')), BindingSpec(kind='external', name='provider_name', value=ValueRef('ProviderName')))), 'DefaultFactoryLocalArgContribution': ContributionSpec(name='DefaultFactoryLocalArgContribution', source_name='DefaultFactoryLocalArg', source_kind='resource', build_name='DefaultFactoryArg', index=TupleValueRef((ValueRef('ConsumerEvalOrder'), ValueRef('ParamOrder'))), order=ValueRef('ParamOrder'), target=TargetSpec(name='default_factory_args', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='DefaultFactoryEval', indexes=(ValueRef('ConsumerEvalOrder'),))))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('ParamName')), BindingSpec(kind='ident', name='provider_name', value=ValueRef('ProviderName')))), 'DefaultFactoryEmptyArgContribution': ContributionSpec(name='DefaultFactoryEmptyArgContribution', source_name='DefaultFactoryEmptyArg', source_kind='resource', build_name='DefaultFactoryArg', index=TupleValueRef((ValueRef('ConsumerEvalOrder'), ValueRef('ParamOrder'))), order=ValueRef('ParamOrder'), target=TargetSpec(name='default_factory_args', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='DefaultFactoryEval', indexes=(ValueRef('ConsumerEvalOrder'),))))),)), bindings=()), 'TransientCurrentStateSlot': ContributionSpec(name='TransientCurrentStateSlot', source_name='StateSlotEntry', source_kind='resource', build_name='TransientCurrentStateSlot', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_slots', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='slot_name', value=ValueRef('CurrentSlotName')),)), 'TransientWorkingStateSlot': ContributionSpec(name='TransientWorkingStateSlot', source_name='StateSlotEntry', source_kind='resource', build_name='TransientWorkingStateSlot', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_slots', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='slot_name', value=ValueRef('WorkingSlotName')),)), 'RetainedInitVarStateSlot': ContributionSpec(name='RetainedInitVarStateSlot', source_name='StateSlotEntry', source_kind='resource', build_name='RetainedInitVarStateSlot', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_slots', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='slot_name', value=ValueRef('RetainedSlotName')),)), 'TransientWorkingDefaultFactoryBuilderParam': ContributionSpec(name='TransientWorkingDefaultFactoryBuilderParam', source_name='BuilderParam', source_kind='resource', build_name='TransientWorkingDefaultFactoryBuilderParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='builder_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='Root', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='value_name', value=ValueRef('WorkingDefaultFactoryParamName')),)), 'TransientInitParamRequired': ContributionSpec(name='TransientInitParamRequired', source_name='InitParamRequired', source_kind='resource', build_name='TransientInitParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')))), 'TransientInitParamDefault': ContributionSpec(name='TransientInitParamDefault', source_name='InitParamDefault', source_kind='resource', build_name='TransientInitParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')), BindingSpec(kind='ident', name='default_value_name', value=ValueRef('DefaultValueParamName')))), 'TransientInitParamDefaultFactory': ContributionSpec(name='TransientInitParamDefaultFactory', source_name='InitParamDefaultFactory', source_kind='resource', build_name='TransientInitParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')))), 'TransientCurrentInitAssignment': ContributionSpec(name='TransientCurrentInitAssignment', source_name='PlainStateAssignment', source_kind='resource', build_name='TransientCurrentInitAssignment', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='init_value_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('CurrentSlotName')))), 'TransientCurrentDefaultAssignment': ContributionSpec(name='TransientCurrentDefaultAssignment', source_name='PlainStateAssignment', source_kind='resource', build_name='TransientCurrentDefaultAssignment', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='init_value_name', value=ValueRef('DefaultValueParamName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('CurrentSlotName')))), 'TransientWorkingInitAssignment': ContributionSpec(name='TransientWorkingInitAssignment', source_name='TransientWorkingStateAssignment', source_kind='resource', build_name='TransientWorkingInitAssignment', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='working_slot', value=ValueRef('WorkingSlotName')),)), 'RetainedInitVarStateAssignment': ContributionSpec(name='RetainedInitVarStateAssignment', source_name='RetainedInitVarAssignment', source_kind='resource', build_name='RetainedInitVarStateAssignment', index=ValueRef('FieldOrder'), order=ValueRef('RetainOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='init_value_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='retained_slot', value=ValueRef('RetainedSlotName')))), 'TransientCurrentPropertyContribution': ContributionSpec(name='TransientCurrentPropertyContribution', source_name='TransientCurrentProperty', source_kind='resource', build_name='TransientCurrentProperty', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='current_facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='property_getter_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='current_slot', value=ValueRef('CurrentSlotName')))), 'TransientDefaultFacadeProperty': ContributionSpec(name='TransientDefaultFacadeProperty', source_name='TransientFacadeProperty', source_kind='resource', build_name='TransientDefaultFacadeProperty', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='default_facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='property_getter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_target_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='current_slot', value=ValueRef('CurrentSlotName')), BindingSpec(kind='external', name='working_slot', value=ValueRef('WorkingSlotName')), BindingSpec(kind='external', name='tx_index', value=ValueRef('TxIndex')))), 'TransientDefaultWorkingDefaultFactoryProperty': ContributionSpec(name='TransientDefaultWorkingDefaultFactoryProperty', source_name='TransientWorkingDefaultFactoryProperty', source_kind='resource', build_name='TransientDefaultFacadeProperty', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='default_facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='property_getter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_target_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='working_default_factory_name', value=ValueRef('WorkingDefaultFactoryParamName')), BindingSpec(kind='external', name='current_slot', value=ValueRef('CurrentSlotName')), BindingSpec(kind='external', name='working_slot', value=ValueRef('WorkingSlotName')), BindingSpec(kind='external', name='tx_index', value=ValueRef('TxIndex')))), 'TransientWorkingFacadeProperty': ContributionSpec(name='TransientWorkingFacadeProperty', source_name='TransientFacadeProperty', source_kind='resource', build_name='TransientWorkingFacadeProperty', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='working_facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='property_getter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_target_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='current_slot', value=ValueRef('CurrentSlotName')), BindingSpec(kind='external', name='working_slot', value=ValueRef('WorkingSlotName')), BindingSpec(kind='external', name='tx_index', value=ValueRef('TxIndex')))), 'TransientWorkingWorkingDefaultFactoryProperty': ContributionSpec(name='TransientWorkingWorkingDefaultFactoryProperty', source_name='TransientWorkingDefaultFactoryProperty', source_kind='resource', build_name='TransientWorkingFacadeProperty', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='working_facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='property_getter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_target_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='working_default_factory_name', value=ValueRef('WorkingDefaultFactoryParamName')), BindingSpec(kind='external', name='current_slot', value=ValueRef('CurrentSlotName')), BindingSpec(kind='external', name='working_slot', value=ValueRef('WorkingSlotName')), BindingSpec(kind='external', name='tx_index', value=ValueRef('TxIndex')))), 'TransientDefaultWorkingFactorySelfArg': ContributionSpec(name='TransientDefaultWorkingFactorySelfArg', source_name='TransientWorkingFactorySelfArg', source_kind='resource', build_name='TransientDefaultWorkingFactoryArg', index=TupleValueRef((ValueRef('WorkingFactoryConsumerFieldOrder'), ValueRef('ParamOrder'))), order=ValueRef('ParamOrder'), target=TargetSpec(name='working_default_factory_args', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='TransientDefaultFacadeProperty', indexes=(ValueRef('WorkingFactoryConsumerFieldOrder'),))))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('ParamName')),)), 'TransientDefaultWorkingFactoryCurrentArg': ContributionSpec(name='TransientDefaultWorkingFactoryCurrentArg', source_name='TransientWorkingFactoryCurrentArg', source_kind='resource', build_name='TransientDefaultWorkingFactoryArg', index=TupleValueRef((ValueRef('WorkingFactoryConsumerFieldOrder'), ValueRef('ParamOrder'))), order=ValueRef('ParamOrder'), target=TargetSpec(name='working_default_factory_args', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='TransientDefaultFacadeProperty', indexes=(ValueRef('WorkingFactoryConsumerFieldOrder'),))))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('ParamName')),)), 'TransientDefaultWorkingFactoryWorkingArg': ContributionSpec(name='TransientDefaultWorkingFactoryWorkingArg', source_name='TransientWorkingFactoryWorkingArg', source_kind='resource', build_name='TransientDefaultWorkingFactoryArg', index=TupleValueRef((ValueRef('WorkingFactoryConsumerFieldOrder'), ValueRef('ParamOrder'))), order=ValueRef('ParamOrder'), target=TargetSpec(name='working_default_factory_args', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='TransientDefaultFacadeProperty', indexes=(ValueRef('WorkingFactoryConsumerFieldOrder'),))))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('ParamName')),)), 'TransientDefaultWorkingFactoryRetainedInitVarArg': ContributionSpec(name='TransientDefaultWorkingFactoryRetainedInitVarArg', source_name='TransientWorkingFactoryRetainedInitVarArg', source_kind='resource', build_name='TransientDefaultWorkingFactoryArg', index=TupleValueRef((ValueRef('WorkingFactoryConsumerFieldOrder'), ValueRef('ParamOrder'))), order=ValueRef('ParamOrder'), target=TargetSpec(name='working_default_factory_args', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='TransientDefaultFacadeProperty', indexes=(ValueRef('WorkingFactoryConsumerFieldOrder'),))))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('ParamName')), BindingSpec(kind='external', name='retained_slot', value=ValueRef('RetainedSlotName')))), 'TransientDefaultWorkingFactoryEmptyArg': ContributionSpec(name='TransientDefaultWorkingFactoryEmptyArg', source_name='TransientWorkingFactoryEmptyArg', source_kind='resource', build_name='TransientDefaultWorkingFactoryArg', index=TupleValueRef((ValueRef('WorkingFactoryConsumerFieldOrder'), ValueRef('ParamOrder'))), order=ValueRef('ParamOrder'), target=TargetSpec(name='working_default_factory_args', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='TransientDefaultFacadeProperty', indexes=(ValueRef('WorkingFactoryConsumerFieldOrder'),))))),)), bindings=()), 'TransientWorkingWorkingFactorySelfArg': ContributionSpec(name='TransientWorkingWorkingFactorySelfArg', source_name='TransientWorkingFactorySelfArg', source_kind='resource', build_name='TransientWorkingWorkingFactoryArg', index=TupleValueRef((ValueRef('WorkingFactoryConsumerFieldOrder'), ValueRef('ParamOrder'))), order=ValueRef('ParamOrder'), target=TargetSpec(name='working_default_factory_args', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='TransientWorkingFacadeProperty', indexes=(ValueRef('WorkingFactoryConsumerFieldOrder'),))))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('ParamName')),)), 'TransientWorkingWorkingFactoryCurrentArg': ContributionSpec(name='TransientWorkingWorkingFactoryCurrentArg', source_name='TransientWorkingFactoryCurrentArg', source_kind='resource', build_name='TransientWorkingWorkingFactoryArg', index=TupleValueRef((ValueRef('WorkingFactoryConsumerFieldOrder'), ValueRef('ParamOrder'))), order=ValueRef('ParamOrder'), target=TargetSpec(name='working_default_factory_args', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='TransientWorkingFacadeProperty', indexes=(ValueRef('WorkingFactoryConsumerFieldOrder'),))))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('ParamName')),)), 'TransientWorkingWorkingFactoryWorkingArg': ContributionSpec(name='TransientWorkingWorkingFactoryWorkingArg', source_name='TransientWorkingFactoryWorkingArg', source_kind='resource', build_name='TransientWorkingWorkingFactoryArg', index=TupleValueRef((ValueRef('WorkingFactoryConsumerFieldOrder'), ValueRef('ParamOrder'))), order=ValueRef('ParamOrder'), target=TargetSpec(name='working_default_factory_args', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='TransientWorkingFacadeProperty', indexes=(ValueRef('WorkingFactoryConsumerFieldOrder'),))))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('ParamName')),)), 'TransientWorkingWorkingFactoryRetainedInitVarArg': ContributionSpec(name='TransientWorkingWorkingFactoryRetainedInitVarArg', source_name='TransientWorkingFactoryRetainedInitVarArg', source_kind='resource', build_name='TransientWorkingWorkingFactoryArg', index=TupleValueRef((ValueRef('WorkingFactoryConsumerFieldOrder'), ValueRef('ParamOrder'))), order=ValueRef('ParamOrder'), target=TargetSpec(name='working_default_factory_args', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='TransientWorkingFacadeProperty', indexes=(ValueRef('WorkingFactoryConsumerFieldOrder'),))))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('ParamName')), BindingSpec(kind='external', name='retained_slot', value=ValueRef('RetainedSlotName')))), 'TransientWorkingWorkingFactoryEmptyArg': ContributionSpec(name='TransientWorkingWorkingFactoryEmptyArg', source_name='TransientWorkingFactoryEmptyArg', source_kind='resource', build_name='TransientWorkingWorkingFactoryArg', index=TupleValueRef((ValueRef('WorkingFactoryConsumerFieldOrder'), ValueRef('ParamOrder'))), order=ValueRef('ParamOrder'), target=TargetSpec(name='working_default_factory_args', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='TransientWorkingFacadeProperty', indexes=(ValueRef('WorkingFactoryConsumerFieldOrder'),))))),)), bindings=()), 'TransientApplyPreparedCommit': ContributionSpec(name='TransientApplyPreparedCommit', source_name='TransientClearWorkingBranch', source_kind='resource', build_name='TransientApplyPreparedCommit', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='apply_prepared_commit_fields_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='ApplyPreparedCommitFields', indexes=(ValueRef('TxIndex'),))))),)), bindings=(BindingSpec(kind='external', name='working_slot', value=ValueRef('WorkingSlotName')),)), 'TransientRollback': ContributionSpec(name='TransientRollback', source_name='TransientClearWorkingBranch', source_kind='resource', build_name='TransientRollback', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='rollback_fields_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='RollbackFields', indexes=(ValueRef('TxIndex'),))))),)), bindings=(BindingSpec(kind='external', name='working_slot', value=ValueRef('WorkingSlotName')),)), 'BindingSupportHelperContribution': ContributionSpec(name='BindingSupportHelperContribution', source_name='BindingSupportHelper', source_kind='resource', build_name='BindingSupportHelper', index=ValueRef('ClassOrder'), order=LiteralValueRef(-1000), target=TargetSpec(name='function_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='Root', indexes=()),))),)), bindings=()), 'BindingStateSlot': ContributionSpec(name='BindingStateSlot', source_name='StateSlotEntry', source_kind='resource', build_name='BindingStateSlot', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_slots', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='slot_name', value=ValueRef('ValueSlotName')),)), 'OwnedCurrentStateSlot': ContributionSpec(name='OwnedCurrentStateSlot', source_name='StateSlotEntry', source_kind='resource', build_name='OwnedCurrentStateSlot', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_slots', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='slot_name', value=ValueRef('CurrentSlotName')),)), 'OwnedWorkingStateSlot': ContributionSpec(name='OwnedWorkingStateSlot', source_name='StateSlotEntry', source_kind='resource', build_name='OwnedWorkingStateSlot', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_slots', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='slot_name', value=ValueRef('WorkingSlotName')),)), 'OwnedStagedStateSlot': ContributionSpec(name='OwnedStagedStateSlot', source_name='StateSlotEntry', source_kind='resource', build_name='OwnedStagedStateSlot', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_slots', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='slot_name', value=ValueRef('StagedSlotName')),)), 'BindingInitParamRequired': ContributionSpec(name='BindingInitParamRequired', source_name='InitParamRequired', source_kind='resource', build_name='BindingInitParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')))), 'BindingInitParamDefault': ContributionSpec(name='BindingInitParamDefault', source_name='InitParamDefault', source_kind='resource', build_name='BindingInitParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')), BindingSpec(kind='ident', name='default_value_name', value=ValueRef('DefaultValueParamName')))), 'BindingInitParamDefaultFactory': ContributionSpec(name='BindingInitParamDefaultFactory', source_name='InitParamDefaultFactory', source_kind='resource', build_name='BindingInitParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')))), 'OwnedInitParamRequired': ContributionSpec(name='OwnedInitParamRequired', source_name='InitParamRequired', source_kind='resource', build_name='OwnedInitParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')))), 'OwnedInitParamDefault': ContributionSpec(name='OwnedInitParamDefault', source_name='InitParamDefault', source_kind='resource', build_name='OwnedInitParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')), BindingSpec(kind='ident', name='default_value_name', value=ValueRef('DefaultValueParamName')))), 'OwnedInitParamDefaultFactory': ContributionSpec(name='OwnedInitParamDefaultFactory', source_name='InitParamDefaultFactory', source_kind='resource', build_name='OwnedInitParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')))), 'BindingInitAssignment': ContributionSpec(name='BindingInitAssignment', source_name='BindingStateAssignment', source_kind='resource', build_name='BindingInitAssignment', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='init_value_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='field_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('ValueSlotName')))), 'BindingDefaultAssignment': ContributionSpec(name='BindingDefaultAssignment', source_name='BindingStateAssignment', source_kind='resource', build_name='BindingInitAssignment', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='init_value_name', value=ValueRef('DefaultValueParamName')), BindingSpec(kind='external', name='field_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('ValueSlotName')))), 'BindingMapInitAssignment': ContributionSpec(name='BindingMapInitAssignment', source_name='BindingMapStateAssignment', source_kind='resource', build_name='BindingInitAssignment', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='init_value_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='field_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('ValueSlotName')))), 'BindingMapDefaultAssignment': ContributionSpec(name='BindingMapDefaultAssignment', source_name='BindingMapStateAssignment', source_kind='resource', build_name='BindingInitAssignment', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='init_value_name', value=ValueRef('DefaultValueParamName')), BindingSpec(kind='external', name='field_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('ValueSlotName')))), 'BindingFieldProperty': ContributionSpec(name='BindingFieldProperty', source_name='BindingProperty', source_kind='resource', build_name='BindingFieldProperty', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='property_getter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_target_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='field_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('ValueSlotName')))), 'BindingMapFieldProperty': ContributionSpec(name='BindingMapFieldProperty', source_name='BindingMapProperty', source_kind='resource', build_name='BindingFieldProperty', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='property_getter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_target_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='field_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('ValueSlotName')))), 'OwnedCurrentInitAssignment': ContributionSpec(name='OwnedCurrentInitAssignment', source_name='OwnedScalarStateAssignment', source_kind='resource', build_name='OwnedCurrentInitAssignment', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='init_value_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='field_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('CurrentSlotName')))), 'OwnedCurrentDefaultAssignment': ContributionSpec(name='OwnedCurrentDefaultAssignment', source_name='OwnedScalarStateAssignment', source_kind='resource', build_name='OwnedCurrentInitAssignment', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='init_value_name', value=ValueRef('DefaultValueParamName')), BindingSpec(kind='external', name='field_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('CurrentSlotName')))), 'OwnedMapCurrentInitAssignment': ContributionSpec(name='OwnedMapCurrentInitAssignment', source_name='OwnedMapStateAssignment', source_kind='resource', build_name='OwnedCurrentInitAssignment', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='init_value_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='field_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('CurrentSlotName')))), 'OwnedMapCurrentDefaultAssignment': ContributionSpec(name='OwnedMapCurrentDefaultAssignment', source_name='OwnedMapStateAssignment', source_kind='resource', build_name='OwnedCurrentInitAssignment', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='init_value_name', value=ValueRef('DefaultValueParamName')), BindingSpec(kind='external', name='field_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('CurrentSlotName')))), 'OwnedWorkingInitAssignment': ContributionSpec(name='OwnedWorkingInitAssignment', source_name='OwnedEmptyStateAssignment', source_kind='resource', build_name='OwnedWorkingInitAssignment', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='state_slot', value=ValueRef('WorkingSlotName')),)), 'OwnedStagedInitAssignment': ContributionSpec(name='OwnedStagedInitAssignment', source_name='OwnedEmptyStateAssignment', source_kind='resource', build_name='OwnedStagedInitAssignment', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='state_slot', value=ValueRef('StagedSlotName')),)), 'OwnedDefaultFacadeProperty': ContributionSpec(name='OwnedDefaultFacadeProperty', source_name='OwnedDefaultProperty', source_kind='resource', build_name='OwnedDefaultFacadeProperty', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='default_facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='property_getter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_target_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='current_slot', value=ValueRef('CurrentSlotName')), BindingSpec(kind='external', name='working_slot', value=ValueRef('WorkingSlotName')), BindingSpec(kind='external', name='field_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='tx_index', value=ValueRef('TxIndex')))), 'OwnedMapDefaultFacadeProperty': ContributionSpec(name='OwnedMapDefaultFacadeProperty', source_name='OwnedMapDefaultProperty', source_kind='resource', build_name='OwnedDefaultFacadeProperty', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='default_facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='property_getter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_target_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='current_slot', value=ValueRef('CurrentSlotName')), BindingSpec(kind='external', name='working_slot', value=ValueRef('WorkingSlotName')), BindingSpec(kind='external', name='field_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='tx_index', value=ValueRef('TxIndex')))), 'OwnedCurrentFacadeProperty': ContributionSpec(name='OwnedCurrentFacadeProperty', source_name='OwnedCurrentProperty', source_kind='resource', build_name='OwnedCurrentFacadeProperty', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='current_facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='property_getter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_target_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='current_slot', value=ValueRef('CurrentSlotName')), BindingSpec(kind='external', name='field_name', value=ValueRef('FieldName')))), 'OwnedWorkingFacadeProperty': ContributionSpec(name='OwnedWorkingFacadeProperty', source_name='OwnedWorkingProperty', source_kind='resource', build_name='OwnedWorkingFacadeProperty', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='working_facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='property_getter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_target_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='current_slot', value=ValueRef('CurrentSlotName')), BindingSpec(kind='external', name='working_slot', value=ValueRef('WorkingSlotName')), BindingSpec(kind='external', name='field_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='tx_index', value=ValueRef('TxIndex')))), 'OwnedMapWorkingFacadeProperty': ContributionSpec(name='OwnedMapWorkingFacadeProperty', source_name='OwnedMapWorkingProperty', source_kind='resource', build_name='OwnedWorkingFacadeProperty', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='working_facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='property_getter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_target_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='current_slot', value=ValueRef('CurrentSlotName')), BindingSpec(kind='external', name='working_slot', value=ValueRef('WorkingSlotName')), BindingSpec(kind='external', name='field_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='tx_index', value=ValueRef('TxIndex')))), 'OwnedPrepareCommit': ContributionSpec(name='OwnedPrepareCommit', source_name='OwnedPrepareCommitBranch', source_kind='resource', build_name='OwnedPrepareCommit', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='prepare_commit_fields_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='PrepareCommitFields', indexes=(ValueRef('TxIndex'),))))),)), bindings=(BindingSpec(kind='external', name='working_slot', value=ValueRef('WorkingSlotName')), BindingSpec(kind='external', name='staged_slot', value=ValueRef('StagedSlotName')))), 'OwnedMapPrepareCommit': ContributionSpec(name='OwnedMapPrepareCommit', source_name='OwnedMapPrepareCommitBranch', source_kind='resource', build_name='OwnedPrepareCommit', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='prepare_commit_fields_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='PrepareCommitFields', indexes=(ValueRef('TxIndex'),))))),)), bindings=(BindingSpec(kind='external', name='working_slot', value=ValueRef('WorkingSlotName')), BindingSpec(kind='external', name='staged_slot', value=ValueRef('StagedSlotName')))), 'OwnedApplyPreparedCommit': ContributionSpec(name='OwnedApplyPreparedCommit', source_name='OwnedApplyPreparedCommitBranch', source_kind='resource', build_name='OwnedApplyPreparedCommit', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='apply_prepared_commit_fields_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='ApplyPreparedCommitFields', indexes=(ValueRef('TxIndex'),))))),)), bindings=(BindingSpec(kind='external', name='current_slot', value=ValueRef('CurrentSlotName')), BindingSpec(kind='external', name='working_slot', value=ValueRef('WorkingSlotName')), BindingSpec(kind='external', name='staged_slot', value=ValueRef('StagedSlotName')))), 'OwnedRollback': ContributionSpec(name='OwnedRollback', source_name='OwnedRollbackBranch', source_kind='resource', build_name='OwnedRollback', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='rollback_fields_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='RollbackFields', indexes=(ValueRef('TxIndex'),))))),)), bindings=(BindingSpec(kind='external', name='working_slot', value=ValueRef('WorkingSlotName')), BindingSpec(kind='external', name='staged_slot', value=ValueRef('StagedSlotName')))), 'OwnedScalarDefaultFactoryEvalInitContribution': ContributionSpec(name='OwnedScalarDefaultFactoryEvalInitContribution', source_name='OwnedScalarDefaultFactoryEvalInit', source_kind='resource', build_name='DefaultFactoryEval', index=ValueRef('EvalOrder'), order=ValueRef('EvalStatementOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='field_name', value=ValueRef('EvalFieldName')), BindingSpec(kind='ident', name='default_factory_name', value=ValueRef('EvalDefaultFactoryParamName')), BindingSpec(kind='external', name='field_name_value', value=ValueRef('EvalFieldName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('EvalStateSlotName')))), 'OwnedScalarDefaultFactoryEvalNoInitContribution': ContributionSpec(name='OwnedScalarDefaultFactoryEvalNoInitContribution', source_name='OwnedScalarDefaultFactoryEvalNoInit', source_kind='resource', build_name='DefaultFactoryEval', index=ValueRef('EvalOrder'), order=ValueRef('EvalStatementOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='field_name', value=ValueRef('EvalFieldName')), BindingSpec(kind='ident', name='default_factory_name', value=ValueRef('EvalDefaultFactoryParamName')), BindingSpec(kind='external', name='field_name_value', value=ValueRef('EvalFieldName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('EvalStateSlotName')))), 'OwnedMapDefaultFactoryEvalInitContribution': ContributionSpec(name='OwnedMapDefaultFactoryEvalInitContribution', source_name='OwnedMapDefaultFactoryEvalInit', source_kind='resource', build_name='DefaultFactoryEval', index=ValueRef('EvalOrder'), order=ValueRef('EvalStatementOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='field_name', value=ValueRef('EvalFieldName')), BindingSpec(kind='ident', name='default_factory_name', value=ValueRef('EvalDefaultFactoryParamName')), BindingSpec(kind='external', name='field_name_value', value=ValueRef('EvalFieldName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('EvalStateSlotName')))), 'OwnedMapDefaultFactoryEvalNoInitContribution': ContributionSpec(name='OwnedMapDefaultFactoryEvalNoInitContribution', source_name='OwnedMapDefaultFactoryEvalNoInit', source_kind='resource', build_name='DefaultFactoryEval', index=ValueRef('EvalOrder'), order=ValueRef('EvalStatementOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='field_name', value=ValueRef('EvalFieldName')), BindingSpec(kind='ident', name='default_factory_name', value=ValueRef('EvalDefaultFactoryParamName')), BindingSpec(kind='external', name='field_name_value', value=ValueRef('EvalFieldName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('EvalStateSlotName')))), 'BindingDefaultFactoryEvalInitContribution': ContributionSpec(name='BindingDefaultFactoryEvalInitContribution', source_name='BindingDefaultFactoryEvalInit', source_kind='resource', build_name='DefaultFactoryEval', index=ValueRef('EvalOrder'), order=ValueRef('EvalStatementOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='field_name', value=ValueRef('EvalFieldName')), BindingSpec(kind='ident', name='default_factory_name', value=ValueRef('EvalDefaultFactoryParamName')), BindingSpec(kind='external', name='property_name', value=ValueRef('EvalFieldName')))), 'BindingDefaultFactoryEvalNoInitContribution': ContributionSpec(name='BindingDefaultFactoryEvalNoInitContribution', source_name='BindingDefaultFactoryEvalNoInit', source_kind='resource', build_name='DefaultFactoryEval', index=ValueRef('EvalOrder'), order=ValueRef('EvalStatementOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='field_name', value=ValueRef('EvalFieldName')), BindingSpec(kind='ident', name='default_factory_name', value=ValueRef('EvalDefaultFactoryParamName')), BindingSpec(kind='external', name='property_name', value=ValueRef('EvalFieldName')))), 'ConstStateSlot': ContributionSpec(name='ConstStateSlot', source_name='StateSlotEntry', source_kind='resource', build_name='ConstStateSlot', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_slots', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='slot_name', value=ValueRef('ValueSlotName')),)), 'StaticStateSlot': ContributionSpec(name='StaticStateSlot', source_name='StateSlotEntry', source_kind='resource', build_name='StaticStateSlot', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_slots', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='slot_name', value=ValueRef('ValueSlotName')),)), 'ConstInitParamRequired': ContributionSpec(name='ConstInitParamRequired', source_name='InitParamRequired', source_kind='resource', build_name='ConstInitParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')))), 'ConstInitParamDefault': ContributionSpec(name='ConstInitParamDefault', source_name='InitParamDefault', source_kind='resource', build_name='ConstInitParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')), BindingSpec(kind='ident', name='default_value_name', value=ValueRef('DefaultValueParamName')))), 'ConstInitParamDefaultFactory': ContributionSpec(name='ConstInitParamDefaultFactory', source_name='InitParamDefaultFactory', source_kind='resource', build_name='ConstInitParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')))), 'StaticInitParamOptional': ContributionSpec(name='StaticInitParamOptional', source_name='InitParamDefaultFactory', source_kind='resource', build_name='StaticInitParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')))), 'ConstInitAssignment': ContributionSpec(name='ConstInitAssignment', source_name='PlainStateAssignment', source_kind='resource', build_name='ConstInitAssignment', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='init_value_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('ValueSlotName')))), 'ConstDefaultAssignment': ContributionSpec(name='ConstDefaultAssignment', source_name='PlainStateAssignment', source_kind='resource', build_name='ConstDefaultAssignment', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='init_value_name', value=ValueRef('DefaultValueParamName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('ValueSlotName')))), 'StaticInitValueAssignment': ContributionSpec(name='StaticInitValueAssignment', source_name='StaticInitAssignment', source_kind='resource', build_name='StaticInitValueAssignment', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='init_value_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('ValueSlotName')))), 'StaticDefaultVoidAssignment': ContributionSpec(name='StaticDefaultVoidAssignment', source_name='StaticVoidAssignment', source_kind='resource', build_name='StaticDefaultVoidAssignment', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='state_slot', value=ValueRef('ValueSlotName')),)), 'ConstFieldProperty': ContributionSpec(name='ConstFieldProperty', source_name='ConstReadOnlyProperty', source_kind='resource', build_name='ConstFieldProperty', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='property_getter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_target_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('ValueSlotName')), BindingSpec(kind='external', name='field_name', value=ValueRef('FieldName')))), 'StaticUnsetFieldProperty': ContributionSpec(name='StaticUnsetFieldProperty', source_name='StaticUnsetProperty', source_kind='resource', build_name='StaticFieldProperty', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='property_getter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_target_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('ValueSlotName')), BindingSpec(kind='external', name='field_name', value=ValueRef('FieldName')))), 'StaticDefaultFieldProperty': ContributionSpec(name='StaticDefaultFieldProperty', source_name='StaticDefaultProperty', source_kind='resource', build_name='StaticFieldProperty', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='property_getter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_target_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='default_value_name', value=ValueRef('DefaultValueParamName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('ValueSlotName')), BindingSpec(kind='external', name='field_name', value=ValueRef('FieldName')))), 'StaticDefaultFactoryFieldProperty': ContributionSpec(name='StaticDefaultFactoryFieldProperty', source_name='StaticDefaultFactoryProperty', source_kind='resource', build_name='StaticFieldProperty', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='property_getter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_target_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='default_factory_name', value=ValueRef('DefaultFactoryParamName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('ValueSlotName')), BindingSpec(kind='external', name='field_name', value=ValueRef('FieldName')))), 'StaticDefaultFactoryEvalPlaceholderContribution': ContributionSpec(name='StaticDefaultFactoryEvalPlaceholderContribution', source_name='StaticDefaultFactoryEvalPlaceholder', source_kind='resource', build_name='DefaultFactoryEval', index=ValueRef('EvalOrder'), order=ValueRef('EvalStatementOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='default_factory_name', value=ValueRef('EvalDefaultFactoryParamName')),)), 'StaticDefaultFactoryStoredArgContribution': ContributionSpec(name='StaticDefaultFactoryStoredArgContribution', source_name='StaticDefaultFactoryStoredArg', source_kind='resource', build_name='StaticDefaultFactoryArg', index=TupleValueRef((ValueRef('ConsumerFieldOrder'), ValueRef('ParamOrder'))), order=ValueRef('ParamOrder'), target=TargetSpec(name='static_default_factory_args', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='StaticFieldProperty', indexes=(ValueRef('ConsumerFieldOrder'),))))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('ParamName')), BindingSpec(kind='external', name='provider_name', value=ValueRef('ProviderName')))), 'StaticDefaultFactoryEmptyArgContribution': ContributionSpec(name='StaticDefaultFactoryEmptyArgContribution', source_name='StaticDefaultFactoryEmptyArg', source_kind='resource', build_name='StaticDefaultFactoryArg', index=TupleValueRef((ValueRef('ConsumerFieldOrder'), ValueRef('ParamOrder'))), order=ValueRef('ParamOrder'), target=TargetSpec(name='static_default_factory_args', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()), PathSegmentSpec(kind='name', name='StaticFieldProperty', indexes=(ValueRef('ConsumerFieldOrder'),))))),)), bindings=())}
ASSEMBLY_MATCHERS = {'BuilderParamContributions': ContributionMatcherSpec(name='BuilderParamContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='LifecycleDefinitionBuilderParam', rules=()), 'AnnotationsBuilderParamContributions': ContributionMatcherSpec(name='AnnotationsBuilderParamContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='AnnotationsBuilderParam', rules=()), 'TxKeysBuilderParamContributions': ContributionMatcherSpec(name='TxKeysBuilderParamContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='TxKeysBuilderParam', rules=()), 'ReturnClassContributions': ContributionMatcherSpec(name='ReturnClassContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='ReturnClassContribution', rules=()), 'TransactionManagerInitParamContributions': ContributionMatcherSpec(name='TransactionManagerInitParamContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='TransactionManagerInitParam', rules=()), 'CommitOrderKeyFallbackContributions': ContributionMatcherSpec(name='CommitOrderKeyFallbackContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='CommitOrderKeyFallback', rules=()), 'RequiresValidationFallbackContributions': ContributionMatcherSpec(name='RequiresValidationFallbackContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='RequiresValidationFallback', rules=()), 'ValidateCommitFallbackContributions': ContributionMatcherSpec(name='ValidateCommitFallbackContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='ValidateCommitFallback', rules=()), 'BeforeCommitFallbackContributions': ContributionMatcherSpec(name='BeforeCommitFallbackContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='BeforeCommitFallback', rules=()), 'PrepareCommitDispatchFallbackContributions': ContributionMatcherSpec(name='PrepareCommitDispatchFallbackContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='PrepareCommitDispatchFallback', rules=()), 'CommitDispatchFallbackContributions': ContributionMatcherSpec(name='CommitDispatchFallbackContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='CommitDispatchFallback', rules=()), 'AfterCommitFallbackContributions': ContributionMatcherSpec(name='AfterCommitFallbackContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='AfterCommitFallback', rules=()), 'RollbackDispatchFallbackContributions': ContributionMatcherSpec(name='RollbackDispatchFallbackContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='RollbackDispatchFallback', rules=()), 'AfterRollbackFallbackContributions': ContributionMatcherSpec(name='AfterRollbackFallbackContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='AfterRollbackFallback', rules=()), 'PlainStateSlotContributions': ContributionMatcherSpec(name='PlainStateSlotContributions', inputs=(AssemblyInputSpec(name='field', collection_name='PlainFields', collection=None),), default_contribution_name='PlainStateSlot', rules=()), 'InitVarLocalDefaultContributions': ContributionMatcherSpec(name='InitVarLocalDefaultContributions', inputs=(AssemblyInputSpec(name='field', collection_name='InitVarFields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='default_value', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(False)), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='InitVarLocalDefault', weight=1.0),)), 'PlainInitAssignmentContributions': ContributionMatcherSpec(name='PlainInitAssignmentContributions', inputs=(AssemblyInputSpec(name='field', collection_name='PlainFields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='init_field', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='PlainInitAssignment', weight=1.0), ContributionRuleSpec(name='default_value', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(False)), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='PlainDefaultAssignment', weight=1.0))), 'PlainPropertyContributions': ContributionMatcherSpec(name='PlainPropertyContributions', inputs=(AssemblyInputSpec(name='field', collection_name='PlainFields', collection=None),), default_contribution_name='PlainFieldProperty', rules=()), 'ClassVarDefaultContributions': ContributionMatcherSpec(name='ClassVarDefaultContributions', inputs=(AssemblyInputSpec(name='field', collection_name='ClassVarFields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='has_default', condition=EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(True)), contribution_name='ClassVarDefault', weight=1.0),)), 'CommitOrderKeyContributions': ContributionMatcherSpec(name='CommitOrderKeyContributions', inputs=(AssemblyInputSpec(name='method', collection_name='CommitOrderKeyProviders', collection=None),), default_contribution_name='CommitOrderKeyBranchContribution', rules=(ContributionRuleSpec(name='helper', condition=EqConditionSpec(left=ValueRef('MethodKind'), right=LiteralValueRef('commit_order_key')), contribution_name='CommitOrderKeyHelperMethodCall', weight=1.0),)), 'RequiresValidationContributions': ContributionMatcherSpec(name='RequiresValidationContributions', inputs=(AssemblyInputSpec(name='method', collection_name='CommitValidators', collection=None),), default_contribution_name='RequiresValidationBranchContribution', rules=(ContributionRuleSpec(name='helper', condition=EqConditionSpec(left=ValueRef('MethodKind'), right=LiteralValueRef('validate_commit')), contribution_name='RequiresValidationHelperMethodCall', weight=1.0),)), 'ValidateCommitContributions': ContributionMatcherSpec(name='ValidateCommitContributions', inputs=(AssemblyInputSpec(name='method', collection_name='CommitValidators', collection=None),), default_contribution_name='ValidateCommitBranchContribution', rules=(ContributionRuleSpec(name='helper', condition=EqConditionSpec(left=ValueRef('MethodKind'), right=LiteralValueRef('validate_commit')), contribution_name='ValidateCommitHelperMethodCall', weight=1.0),)), 'BeforeCommitHookContributions': ContributionMatcherSpec(name='BeforeCommitHookContributions', inputs=(AssemblyInputSpec(name='method', collection_name='BeforeCommitHooks', collection=None),), default_contribution_name='BeforeCommitHookContribution', rules=(ContributionRuleSpec(name='helper', condition=EqConditionSpec(left=ValueRef('MethodKind'), right=LiteralValueRef('before_commit')), contribution_name='BeforeCommitHelperMethodCall', weight=1.0),)), 'AfterCommitHookContributions': ContributionMatcherSpec(name='AfterCommitHookContributions', inputs=(AssemblyInputSpec(name='method', collection_name='AfterCommitHooks', collection=None),), default_contribution_name='AfterCommitHookContribution', rules=(ContributionRuleSpec(name='helper', condition=EqConditionSpec(left=ValueRef('MethodKind'), right=LiteralValueRef('after_commit')), contribution_name='AfterCommitHelperMethodCall', weight=1.0),)), 'AfterRollbackHookContributions': ContributionMatcherSpec(name='AfterRollbackHookContributions', inputs=(AssemblyInputSpec(name='method', collection_name='AfterRollbackHooks', collection=None),), default_contribution_name='AfterRollbackHookContribution', rules=(ContributionRuleSpec(name='helper', condition=EqConditionSpec(left=ValueRef('MethodKind'), right=LiteralValueRef('after_rollback')), contribution_name='AfterRollbackHelperMethodCall', weight=1.0),)), 'FieldDefaultBuilderParamContributions': ContributionMatcherSpec(name='FieldDefaultBuilderParamContributions', inputs=(AssemblyInputSpec(name='field', collection_name='Fields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='has_default', condition=EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(True)), contribution_name='FieldDefaultBuilderParam', weight=1.0), ContributionRuleSpec(name='has_default_factory', condition=EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(True)), contribution_name='FieldDefaultFactoryBuilderParam', weight=1.0))), 'CoreClassDefinitionContributions': ContributionMatcherSpec(name='CoreClassDefinitionContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='CoreClassDefinition', rules=()), 'PlainInitParamContributions': ContributionMatcherSpec(name='PlainInitParamContributions', inputs=(AssemblyInputSpec(name='field', collection_name='PlainFields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='required', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(False)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='PlainInitParamRequired', weight=1.0), ContributionRuleSpec(name='default_value', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='PlainInitParamDefault', weight=1.0), ContributionRuleSpec(name='default_factory', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(True)))), contribution_name='PlainInitParamDefaultFactory', weight=1.0))), 'InitVarParamContributions': ContributionMatcherSpec(name='InitVarParamContributions', inputs=(AssemblyInputSpec(name='field', collection_name='InitVarFields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='required', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(False)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='InitVarParamRequired', weight=1.0), ContributionRuleSpec(name='default_value', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='InitVarParamDefault', weight=1.0), ContributionRuleSpec(name='default_factory', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(True)))), contribution_name='InitVarParamDefaultFactory', weight=1.0))), 'ManagedCurrentStateSlotContributions': ContributionMatcherSpec(name='ManagedCurrentStateSlotContributions', inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), default_contribution_name='ManagedCurrentStateSlot', rules=()), 'ManagedWorkingStateSlotContributions': ContributionMatcherSpec(name='ManagedWorkingStateSlotContributions', inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), default_contribution_name='ManagedWorkingStateSlot', rules=()), 'ManagedStagedStateSlotContributions': ContributionMatcherSpec(name='ManagedStagedStateSlotContributions', inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), default_contribution_name='ManagedStagedStateSlot', rules=()), 'ManagedFreezeBuilderParamContributions': ContributionMatcherSpec(name='ManagedFreezeBuilderParamContributions', inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='has_freeze', condition=EqConditionSpec(left=ValueRef('HasFreeze'), right=LiteralValueRef(True)), contribution_name='ManagedFreezeBuilderParam', weight=1.0),)), 'ManagedThawBuilderParamContributions': ContributionMatcherSpec(name='ManagedThawBuilderParamContributions', inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='has_thaw', condition=EqConditionSpec(left=ValueRef('HasThaw'), right=LiteralValueRef(True)), contribution_name='ManagedThawBuilderParam', weight=1.0),)), 'ManagedCurrentInitAssignmentContributions': ContributionMatcherSpec(name='ManagedCurrentInitAssignmentContributions', inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='init_field', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='ManagedCurrentInitAssignment', weight=1.0), ContributionRuleSpec(name='default_value', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(False)), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='ManagedCurrentDefaultAssignment', weight=1.0))), 'ManagedWorkingInitAssignmentContributions': ContributionMatcherSpec(name='ManagedWorkingInitAssignmentContributions', inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), default_contribution_name='ManagedWorkingInitAssignment', rules=()), 'ManagedStagedInitAssignmentContributions': ContributionMatcherSpec(name='ManagedStagedInitAssignmentContributions', inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), default_contribution_name='ManagedStagedInitAssignment', rules=()), 'ManagedDefaultFacadePropertyContributions': ContributionMatcherSpec(name='ManagedDefaultFacadePropertyContributions', inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransactionalFields', collection=None),), default_contribution_name='ManagedDefaultFacadeProperty', rules=()), 'ManagedCurrentFacadePropertyContributions': ContributionMatcherSpec(name='ManagedCurrentFacadePropertyContributions', inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransactionalFields', collection=None),), default_contribution_name='ManagedCurrentFacadeProperty', rules=()), 'ManagedWorkingFacadePropertyContributions': ContributionMatcherSpec(name='ManagedWorkingFacadePropertyContributions', inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransactionalFields', collection=None),), default_contribution_name='ManagedWorkingFacadeProperty', rules=(ContributionRuleSpec(name='with_optional_thaw', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('HasThaw'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasOptionalNone'), right=LiteralValueRef(True)))), contribution_name='ManagedOptionalThawWorkingFacadeProperty', weight=1.0), ContributionRuleSpec(name='with_thaw', condition=EqConditionSpec(left=ValueRef('HasThaw'), right=LiteralValueRef(True)), contribution_name='ManagedThawWorkingFacadeProperty', weight=1.0))), 'ManagedPrepareCommitContributions': ContributionMatcherSpec(name='ManagedPrepareCommitContributions', inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransactionalFields', collection=None),), default_contribution_name='ManagedPlainPrepareCommit', rules=(ContributionRuleSpec(name='with_optional_freeze', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('HasFreeze'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasOptionalNone'), right=LiteralValueRef(True)))), contribution_name='ManagedOptionalFreezePrepareCommit', weight=1.0), ContributionRuleSpec(name='with_freeze', condition=EqConditionSpec(left=ValueRef('HasFreeze'), right=LiteralValueRef(True)), contribution_name='ManagedFreezePrepareCommit', weight=1.0))), 'ManagedApplyPreparedCommitContributions': ContributionMatcherSpec(name='ManagedApplyPreparedCommitContributions', inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransactionalFields', collection=None),), default_contribution_name='ManagedApplyPreparedCommit', rules=()), 'ManagedRollbackContributions': ContributionMatcherSpec(name='ManagedRollbackContributions', inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransactionalFields', collection=None),), default_contribution_name='ManagedRollback', rules=()), 'CommitOrderKeyHelperContributions': ContributionMatcherSpec(name='CommitOrderKeyHelperContributions', inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), default_contribution_name='CommitOrderKeyHelper', rules=()), 'RequiresValidationHelperContributions': ContributionMatcherSpec(name='RequiresValidationHelperContributions', inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), default_contribution_name='RequiresValidationHelper', rules=()), 'ValidateCommitHelperContributions': ContributionMatcherSpec(name='ValidateCommitHelperContributions', inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), default_contribution_name='ValidateCommitHelper', rules=()), 'BeforeCommitHelperContributions': ContributionMatcherSpec(name='BeforeCommitHelperContributions', inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), default_contribution_name='BeforeCommitHelper', rules=()), 'AfterCommitHelperContributions': ContributionMatcherSpec(name='AfterCommitHelperContributions', inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), default_contribution_name='AfterCommitHelper', rules=()), 'AfterRollbackHelperContributions': ContributionMatcherSpec(name='AfterRollbackHelperContributions', inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), default_contribution_name='AfterRollbackHelper', rules=()), 'CommitOrderKeyDispatchContributions': ContributionMatcherSpec(name='CommitOrderKeyDispatchContributions', inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), default_contribution_name='CommitOrderKeyDispatch', rules=()), 'RequiresValidationDispatchContributions': ContributionMatcherSpec(name='RequiresValidationDispatchContributions', inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), default_contribution_name='RequiresValidationDispatch', rules=()), 'ValidateCommitDispatchContributions': ContributionMatcherSpec(name='ValidateCommitDispatchContributions', inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), default_contribution_name='ValidateCommitDispatch', rules=()), 'BeforeCommitDispatchContributions': ContributionMatcherSpec(name='BeforeCommitDispatchContributions', inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), default_contribution_name='BeforeCommitDispatch', rules=()), 'AfterCommitDispatchContributions': ContributionMatcherSpec(name='AfterCommitDispatchContributions', inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), default_contribution_name='AfterCommitDispatch', rules=()), 'AfterRollbackDispatchContributions': ContributionMatcherSpec(name='AfterRollbackDispatchContributions', inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), default_contribution_name='AfterRollbackDispatch', rules=()), 'ApplyPreparedCommitFieldsContributions': ContributionMatcherSpec(name='ApplyPreparedCommitFieldsContributions', inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), default_contribution_name='ApplyPreparedCommitFields', rules=()), 'PrepareCommitFieldsContributions': ContributionMatcherSpec(name='PrepareCommitFieldsContributions', inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), default_contribution_name='PrepareCommitFields', rules=()), 'RollbackFieldsContributions': ContributionMatcherSpec(name='RollbackFieldsContributions', inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), default_contribution_name='RollbackFields', rules=()), 'PrepareCommitDispatchContributions': ContributionMatcherSpec(name='PrepareCommitDispatchContributions', inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), default_contribution_name='PrepareCommitDispatch', rules=()), 'ApplyPreparedCommitDispatchContributions': ContributionMatcherSpec(name='ApplyPreparedCommitDispatchContributions', inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), default_contribution_name='ApplyPreparedCommitDispatch', rules=()), 'RollbackDispatchContributions': ContributionMatcherSpec(name='RollbackDispatchContributions', inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), default_contribution_name='RollbackDispatch', rules=()), 'ManagedInitParamContributions': ContributionMatcherSpec(name='ManagedInitParamContributions', inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='required', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(False)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='ManagedInitParamRequired', weight=1.0), ContributionRuleSpec(name='default_value', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='ManagedInitParamDefault', weight=1.0), ContributionRuleSpec(name='default_factory', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(True)))), contribution_name='ManagedInitParamDefaultFactory', weight=1.0))), 'DefaultFactoryEvalContributions': ContributionMatcherSpec(name='DefaultFactoryEvalContributions', inputs=(AssemblyInputSpec(name='step', collection_name='DefaultFactoryEvaluationSteps', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='field_init', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('EvalFieldKind'), right=LiteralValueRef('field')), EqConditionSpec(left=ValueRef('EvalInit'), right=LiteralValueRef(True)))), contribution_name='StoredDefaultFactoryEvalInitContribution', weight=1.0), ContributionRuleSpec(name='field_no_init', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('EvalFieldKind'), right=LiteralValueRef('field')), EqConditionSpec(left=ValueRef('EvalInit'), right=LiteralValueRef(False)))), contribution_name='StoredDefaultFactoryEvalNoInitContribution', weight=1.0), ContributionRuleSpec(name='managed_init', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('EvalFieldKind'), right=LiteralValueRef('managed')), EqConditionSpec(left=ValueRef('EvalInit'), right=LiteralValueRef(True)))), contribution_name='StoredDefaultFactoryEvalInitContribution', weight=1.0), ContributionRuleSpec(name='managed_no_init', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('EvalFieldKind'), right=LiteralValueRef('managed')), EqConditionSpec(left=ValueRef('EvalInit'), right=LiteralValueRef(False)))), contribution_name='StoredDefaultFactoryEvalNoInitContribution', weight=1.0), ContributionRuleSpec(name='initvar_init', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('EvalFieldKind'), right=LiteralValueRef('initvar')), EqConditionSpec(left=ValueRef('EvalInit'), right=LiteralValueRef(True)))), contribution_name='InitVarDefaultFactoryEvalInitContribution', weight=1.0), ContributionRuleSpec(name='initvar_no_init', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('EvalFieldKind'), right=LiteralValueRef('initvar')), EqConditionSpec(left=ValueRef('EvalInit'), right=LiteralValueRef(False)))), contribution_name='InitVarDefaultFactoryEvalNoInitContribution', weight=1.0), ContributionRuleSpec(name='transient_init', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('EvalFieldKind'), right=LiteralValueRef('transient')), EqConditionSpec(left=ValueRef('EvalInit'), right=LiteralValueRef(True)))), contribution_name='StoredDefaultFactoryEvalInitContribution', weight=1.0), ContributionRuleSpec(name='transient_no_init', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('EvalFieldKind'), right=LiteralValueRef('transient')), EqConditionSpec(left=ValueRef('EvalInit'), right=LiteralValueRef(False)))), contribution_name='StoredDefaultFactoryEvalNoInitContribution', weight=1.0), ContributionRuleSpec(name='binding_init', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('EvalFieldKind'), right=LiteralValueRef('binding')), EqConditionSpec(left=ValueRef('EvalInit'), right=LiteralValueRef(True)))), contribution_name='BindingDefaultFactoryEvalInitContribution', weight=1.0), ContributionRuleSpec(name='binding_no_init', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('EvalFieldKind'), right=LiteralValueRef('binding')), EqConditionSpec(left=ValueRef('EvalInit'), right=LiteralValueRef(False)))), contribution_name='BindingDefaultFactoryEvalNoInitContribution', weight=1.0), ContributionRuleSpec(name='owned_scalar_init', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('EvalFieldKind'), right=LiteralValueRef('owned')), EqConditionSpec(left=ValueRef('EvalBindingShape'), right=LiteralValueRef('scalar')), EqConditionSpec(left=ValueRef('EvalInit'), right=LiteralValueRef(True)))), contribution_name='OwnedScalarDefaultFactoryEvalInitContribution', weight=1.0), ContributionRuleSpec(name='owned_scalar_no_init', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('EvalFieldKind'), right=LiteralValueRef('owned')), EqConditionSpec(left=ValueRef('EvalBindingShape'), right=LiteralValueRef('scalar')), EqConditionSpec(left=ValueRef('EvalInit'), right=LiteralValueRef(False)))), contribution_name='OwnedScalarDefaultFactoryEvalNoInitContribution', weight=1.0), ContributionRuleSpec(name='owned_map_init', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('EvalFieldKind'), right=LiteralValueRef('owned')), EqConditionSpec(left=ValueRef('EvalBindingShape'), right=LiteralValueRef('map')), EqConditionSpec(left=ValueRef('EvalInit'), right=LiteralValueRef(True)))), contribution_name='OwnedMapDefaultFactoryEvalInitContribution', weight=1.0), ContributionRuleSpec(name='owned_map_no_init', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('EvalFieldKind'), right=LiteralValueRef('owned')), EqConditionSpec(left=ValueRef('EvalBindingShape'), right=LiteralValueRef('map')), EqConditionSpec(left=ValueRef('EvalInit'), right=LiteralValueRef(False)))), contribution_name='OwnedMapDefaultFactoryEvalNoInitContribution', weight=1.0), ContributionRuleSpec(name='const_init', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('EvalFieldKind'), right=LiteralValueRef('const')), EqConditionSpec(left=ValueRef('EvalInit'), right=LiteralValueRef(True)))), contribution_name='StoredDefaultFactoryEvalInitContribution', weight=1.0), ContributionRuleSpec(name='const_no_init', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('EvalFieldKind'), right=LiteralValueRef('const')), EqConditionSpec(left=ValueRef('EvalInit'), right=LiteralValueRef(False)))), contribution_name='StoredDefaultFactoryEvalNoInitContribution', weight=1.0), ContributionRuleSpec(name='static_lazy', condition=EqConditionSpec(left=ValueRef('EvalFieldKind'), right=LiteralValueRef('static')), contribution_name='StaticDefaultFactoryEvalPlaceholderContribution', weight=1.0))), 'DefaultFactoryArgContributions': ContributionMatcherSpec(name='DefaultFactoryArgContributions', inputs=(AssemblyInputSpec(name='dep', collection_name='DefaultFactoryDependencies', collection=None),), default_contribution_name='DefaultFactoryStoredArgContribution', rules=(ContributionRuleSpec(name='empty_provider', condition=EqConditionSpec(left=ValueRef('ParamName'), right=LiteralValueRef('')), contribution_name='DefaultFactoryEmptyArgContribution', weight=1.0), ContributionRuleSpec(name='local_provider', condition=EqConditionSpec(left=ValueRef('ProviderFieldKind'), right=LiteralValueRef('initvar')), contribution_name='DefaultFactoryLocalArgContribution', weight=1.0))), 'TransientCurrentStateSlotContributions': ContributionMatcherSpec(name='TransientCurrentStateSlotContributions', inputs=(AssemblyInputSpec(name='field', collection_name='TransientFields', collection=None),), default_contribution_name='TransientCurrentStateSlot', rules=()), 'TransientWorkingStateSlotContributions': ContributionMatcherSpec(name='TransientWorkingStateSlotContributions', inputs=(AssemblyInputSpec(name='field', collection_name='TransientFields', collection=None),), default_contribution_name='TransientWorkingStateSlot', rules=()), 'RetainedInitVarStateSlotContributions': ContributionMatcherSpec(name='RetainedInitVarStateSlotContributions', inputs=(AssemblyInputSpec(name='initvar', collection_name='RetainedInitVars', collection=None),), default_contribution_name='RetainedInitVarStateSlot', rules=()), 'TransientWorkingDefaultBuilderParamContributions': ContributionMatcherSpec(name='TransientWorkingDefaultBuilderParamContributions', inputs=(AssemblyInputSpec(name='field', collection_name='Fields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='has_working_default_factory', condition=EqConditionSpec(left=ValueRef('HasWorkingDefaultFactory'), right=LiteralValueRef(True)), contribution_name='TransientWorkingDefaultFactoryBuilderParam', weight=1.0),)), 'TransientInitParamContributions': ContributionMatcherSpec(name='TransientInitParamContributions', inputs=(AssemblyInputSpec(name='field', collection_name='TransientFields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='required', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(False)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='TransientInitParamRequired', weight=1.0), ContributionRuleSpec(name='default_value', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='TransientInitParamDefault', weight=1.0), ContributionRuleSpec(name='default_factory', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(True)))), contribution_name='TransientInitParamDefaultFactory', weight=1.0))), 'TransientCurrentInitAssignmentContributions': ContributionMatcherSpec(name='TransientCurrentInitAssignmentContributions', inputs=(AssemblyInputSpec(name='field', collection_name='TransientFields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='init_value', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='TransientCurrentInitAssignment', weight=1.0), ContributionRuleSpec(name='default_value', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(False)), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='TransientCurrentDefaultAssignment', weight=1.0))), 'TransientWorkingInitAssignmentContributions': ContributionMatcherSpec(name='TransientWorkingInitAssignmentContributions', inputs=(AssemblyInputSpec(name='field', collection_name='TransientFields', collection=None),), default_contribution_name='TransientWorkingInitAssignment', rules=()), 'RetainedInitVarStateAssignmentContributions': ContributionMatcherSpec(name='RetainedInitVarStateAssignmentContributions', inputs=(AssemblyInputSpec(name='initvar', collection_name='RetainedInitVars', collection=None),), default_contribution_name='RetainedInitVarStateAssignment', rules=()), 'TransientCurrentPropertyContributions': ContributionMatcherSpec(name='TransientCurrentPropertyContributions', inputs=(AssemblyInputSpec(name='field', collection_name='TransientFields', collection=None),), default_contribution_name='TransientCurrentPropertyContribution', rules=()), 'TransientDefaultFacadePropertyContributions': ContributionMatcherSpec(name='TransientDefaultFacadePropertyContributions', inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransientFields', collection=None),), default_contribution_name='TransientDefaultFacadeProperty', rules=(ContributionRuleSpec(name='working_default_factory', condition=EqConditionSpec(left=ValueRef('HasWorkingDefaultFactory'), right=LiteralValueRef(True)), contribution_name='TransientDefaultWorkingDefaultFactoryProperty', weight=1.0),)), 'TransientWorkingFacadePropertyContributions': ContributionMatcherSpec(name='TransientWorkingFacadePropertyContributions', inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransientFields', collection=None),), default_contribution_name='TransientWorkingFacadeProperty', rules=(ContributionRuleSpec(name='working_default_factory', condition=EqConditionSpec(left=ValueRef('HasWorkingDefaultFactory'), right=LiteralValueRef(True)), contribution_name='TransientWorkingWorkingDefaultFactoryProperty', weight=1.0),)), 'TransientApplyPreparedCommitContributions': ContributionMatcherSpec(name='TransientApplyPreparedCommitContributions', inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransientFields', collection=None),), default_contribution_name='TransientApplyPreparedCommit', rules=()), 'TransientRollbackContributions': ContributionMatcherSpec(name='TransientRollbackContributions', inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransientFields', collection=None),), default_contribution_name='TransientRollback', rules=()), 'TransientDefaultWorkingFactoryArgContributions': ContributionMatcherSpec(name='TransientDefaultWorkingFactoryArgContributions', inputs=(AssemblyInputSpec(name='arg', collection_name='TransientWorkingFactoryArgs', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='empty', condition=EqConditionSpec(left=ValueRef('WorkingFactoryArgKind'), right=LiteralValueRef('empty')), contribution_name='TransientDefaultWorkingFactoryEmptyArg', weight=1.0), ContributionRuleSpec(name='self_arg', condition=EqConditionSpec(left=ValueRef('WorkingFactoryArgKind'), right=LiteralValueRef('self')), contribution_name='TransientDefaultWorkingFactorySelfArg', weight=1.0), ContributionRuleSpec(name='current_arg', condition=EqConditionSpec(left=ValueRef('WorkingFactoryArgKind'), right=LiteralValueRef('current')), contribution_name='TransientDefaultWorkingFactoryCurrentArg', weight=1.0), ContributionRuleSpec(name='working_arg', condition=EqConditionSpec(left=ValueRef('WorkingFactoryArgKind'), right=LiteralValueRef('working')), contribution_name='TransientDefaultWorkingFactoryWorkingArg', weight=1.0), ContributionRuleSpec(name='retained_initvar', condition=EqConditionSpec(left=ValueRef('WorkingFactoryArgKind'), right=LiteralValueRef('retained_initvar')), contribution_name='TransientDefaultWorkingFactoryRetainedInitVarArg', weight=1.0))), 'TransientWorkingWorkingFactoryArgContributions': ContributionMatcherSpec(name='TransientWorkingWorkingFactoryArgContributions', inputs=(AssemblyInputSpec(name='arg', collection_name='TransientWorkingFactoryArgs', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='empty', condition=EqConditionSpec(left=ValueRef('WorkingFactoryArgKind'), right=LiteralValueRef('empty')), contribution_name='TransientWorkingWorkingFactoryEmptyArg', weight=1.0), ContributionRuleSpec(name='self_arg', condition=EqConditionSpec(left=ValueRef('WorkingFactoryArgKind'), right=LiteralValueRef('self')), contribution_name='TransientWorkingWorkingFactorySelfArg', weight=1.0), ContributionRuleSpec(name='current_arg', condition=EqConditionSpec(left=ValueRef('WorkingFactoryArgKind'), right=LiteralValueRef('current')), contribution_name='TransientWorkingWorkingFactoryCurrentArg', weight=1.0), ContributionRuleSpec(name='working_arg', condition=EqConditionSpec(left=ValueRef('WorkingFactoryArgKind'), right=LiteralValueRef('working')), contribution_name='TransientWorkingWorkingFactoryWorkingArg', weight=1.0), ContributionRuleSpec(name='retained_initvar', condition=EqConditionSpec(left=ValueRef('WorkingFactoryArgKind'), right=LiteralValueRef('retained_initvar')), contribution_name='TransientWorkingWorkingFactoryRetainedInitVarArg', weight=1.0))), 'BindingSupportHelperContributions': ContributionMatcherSpec(name='BindingSupportHelperContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='BindingSupportHelperContribution', rules=()), 'BindingStateSlotContributions': ContributionMatcherSpec(name='BindingStateSlotContributions', inputs=(AssemblyInputSpec(name='field', collection_name='BindingFields', collection=None),), default_contribution_name='BindingStateSlot', rules=()), 'OwnedCurrentStateSlotContributions': ContributionMatcherSpec(name='OwnedCurrentStateSlotContributions', inputs=(AssemblyInputSpec(name='field', collection_name='OwnedFields', collection=None),), default_contribution_name='OwnedCurrentStateSlot', rules=()), 'OwnedWorkingStateSlotContributions': ContributionMatcherSpec(name='OwnedWorkingStateSlotContributions', inputs=(AssemblyInputSpec(name='field', collection_name='OwnedFields', collection=None),), default_contribution_name='OwnedWorkingStateSlot', rules=()), 'OwnedStagedStateSlotContributions': ContributionMatcherSpec(name='OwnedStagedStateSlotContributions', inputs=(AssemblyInputSpec(name='field', collection_name='OwnedFields', collection=None),), default_contribution_name='OwnedStagedStateSlot', rules=()), 'BindingInitParamContributions': ContributionMatcherSpec(name='BindingInitParamContributions', inputs=(AssemblyInputSpec(name='field', collection_name='BindingFields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='required', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(False)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='BindingInitParamRequired', weight=1.0), ContributionRuleSpec(name='default_value', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='BindingInitParamDefault', weight=1.0), ContributionRuleSpec(name='default_factory', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(True)))), contribution_name='BindingInitParamDefaultFactory', weight=1.0))), 'OwnedInitParamContributions': ContributionMatcherSpec(name='OwnedInitParamContributions', inputs=(AssemblyInputSpec(name='field', collection_name='OwnedFields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='required', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(False)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='OwnedInitParamRequired', weight=1.0), ContributionRuleSpec(name='default_value', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='OwnedInitParamDefault', weight=1.0), ContributionRuleSpec(name='default_factory', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(True)))), contribution_name='OwnedInitParamDefaultFactory', weight=1.0))), 'BindingInitAssignmentContributions': ContributionMatcherSpec(name='BindingInitAssignmentContributions', inputs=(AssemblyInputSpec(name='field', collection_name='BindingFields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='init_field', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('BindingShape'), right=LiteralValueRef('scalar')), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='BindingInitAssignment', weight=1.0), ContributionRuleSpec(name='default_value', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(False)), EqConditionSpec(left=ValueRef('BindingShape'), right=LiteralValueRef('scalar')), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='BindingDefaultAssignment', weight=1.0), ContributionRuleSpec(name='map_init_field', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('BindingShape'), right=LiteralValueRef('map')), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='BindingMapInitAssignment', weight=1.0), ContributionRuleSpec(name='map_default_value', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(False)), EqConditionSpec(left=ValueRef('BindingShape'), right=LiteralValueRef('map')), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='BindingMapDefaultAssignment', weight=1.0))), 'BindingPropertyContributions': ContributionMatcherSpec(name='BindingPropertyContributions', inputs=(AssemblyInputSpec(name='field', collection_name='BindingFields', collection=None),), default_contribution_name='BindingFieldProperty', rules=(ContributionRuleSpec(name='map_field', condition=EqConditionSpec(left=ValueRef('BindingShape'), right=LiteralValueRef('map')), contribution_name='BindingMapFieldProperty', weight=1.0),)), 'OwnedCurrentInitAssignmentContributions': ContributionMatcherSpec(name='OwnedCurrentInitAssignmentContributions', inputs=(AssemblyInputSpec(name='field', collection_name='OwnedFields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='init_field', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('BindingShape'), right=LiteralValueRef('scalar')), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='OwnedCurrentInitAssignment', weight=1.0), ContributionRuleSpec(name='default_value', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(False)), EqConditionSpec(left=ValueRef('BindingShape'), right=LiteralValueRef('scalar')), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='OwnedCurrentDefaultAssignment', weight=1.0), ContributionRuleSpec(name='map_init_field', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('BindingShape'), right=LiteralValueRef('map')), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='OwnedMapCurrentInitAssignment', weight=1.0), ContributionRuleSpec(name='map_default_value', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(False)), EqConditionSpec(left=ValueRef('BindingShape'), right=LiteralValueRef('map')), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='OwnedMapCurrentDefaultAssignment', weight=1.0))), 'OwnedWorkingInitAssignmentContributions': ContributionMatcherSpec(name='OwnedWorkingInitAssignmentContributions', inputs=(AssemblyInputSpec(name='field', collection_name='OwnedFields', collection=None),), default_contribution_name='OwnedWorkingInitAssignment', rules=()), 'OwnedStagedInitAssignmentContributions': ContributionMatcherSpec(name='OwnedStagedInitAssignmentContributions', inputs=(AssemblyInputSpec(name='field', collection_name='OwnedFields', collection=None),), default_contribution_name='OwnedStagedInitAssignment', rules=()), 'OwnedDefaultFacadePropertyContributions': ContributionMatcherSpec(name='OwnedDefaultFacadePropertyContributions', inputs=(AssemblyInputSpec(name='field', collection_name='IndexedOwnedFields', collection=None),), default_contribution_name='OwnedDefaultFacadeProperty', rules=(ContributionRuleSpec(name='map_field', condition=EqConditionSpec(left=ValueRef('BindingShape'), right=LiteralValueRef('map')), contribution_name='OwnedMapDefaultFacadeProperty', weight=1.0),)), 'OwnedCurrentFacadePropertyContributions': ContributionMatcherSpec(name='OwnedCurrentFacadePropertyContributions', inputs=(AssemblyInputSpec(name='field', collection_name='IndexedOwnedFields', collection=None),), default_contribution_name='OwnedCurrentFacadeProperty', rules=()), 'OwnedWorkingFacadePropertyContributions': ContributionMatcherSpec(name='OwnedWorkingFacadePropertyContributions', inputs=(AssemblyInputSpec(name='field', collection_name='IndexedOwnedFields', collection=None),), default_contribution_name='OwnedWorkingFacadeProperty', rules=(ContributionRuleSpec(name='map_field', condition=EqConditionSpec(left=ValueRef('BindingShape'), right=LiteralValueRef('map')), contribution_name='OwnedMapWorkingFacadeProperty', weight=1.0),)), 'OwnedPrepareCommitContributions': ContributionMatcherSpec(name='OwnedPrepareCommitContributions', inputs=(AssemblyInputSpec(name='field', collection_name='IndexedOwnedFields', collection=None),), default_contribution_name='OwnedPrepareCommit', rules=(ContributionRuleSpec(name='map_field', condition=EqConditionSpec(left=ValueRef('BindingShape'), right=LiteralValueRef('map')), contribution_name='OwnedMapPrepareCommit', weight=1.0),)), 'OwnedApplyPreparedCommitContributions': ContributionMatcherSpec(name='OwnedApplyPreparedCommitContributions', inputs=(AssemblyInputSpec(name='field', collection_name='IndexedOwnedFields', collection=None),), default_contribution_name='OwnedApplyPreparedCommit', rules=()), 'OwnedRollbackContributions': ContributionMatcherSpec(name='OwnedRollbackContributions', inputs=(AssemblyInputSpec(name='field', collection_name='IndexedOwnedFields', collection=None),), default_contribution_name='OwnedRollback', rules=()), 'ConstStateSlotContributions': ContributionMatcherSpec(name='ConstStateSlotContributions', inputs=(AssemblyInputSpec(name='field', collection_name='ConstFields', collection=None),), default_contribution_name='ConstStateSlot', rules=()), 'StaticStateSlotContributions': ContributionMatcherSpec(name='StaticStateSlotContributions', inputs=(AssemblyInputSpec(name='field', collection_name='StaticFields', collection=None),), default_contribution_name='StaticStateSlot', rules=()), 'ConstInitParamContributions': ContributionMatcherSpec(name='ConstInitParamContributions', inputs=(AssemblyInputSpec(name='field', collection_name='ConstFields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='required', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(False)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='ConstInitParamRequired', weight=1.0), ContributionRuleSpec(name='default_value', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='ConstInitParamDefault', weight=1.0), ContributionRuleSpec(name='default_factory', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(True)))), contribution_name='ConstInitParamDefaultFactory', weight=1.0))), 'StaticInitParamContributions': ContributionMatcherSpec(name='StaticInitParamContributions', inputs=(AssemblyInputSpec(name='field', collection_name='StaticFields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='init_field', condition=EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), contribution_name='StaticInitParamOptional', weight=1.0),)), 'ConstInitAssignmentContributions': ContributionMatcherSpec(name='ConstInitAssignmentContributions', inputs=(AssemblyInputSpec(name='field', collection_name='ConstFields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='init_field', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='ConstInitAssignment', weight=1.0), ContributionRuleSpec(name='default_value', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(False)), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='ConstDefaultAssignment', weight=1.0))), 'StaticInitAssignmentContributions': ContributionMatcherSpec(name='StaticInitAssignmentContributions', inputs=(AssemblyInputSpec(name='field', collection_name='StaticFields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='init_field', condition=EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), contribution_name='StaticInitValueAssignment', weight=1.0), ContributionRuleSpec(name='no_init', condition=EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(False)), contribution_name='StaticDefaultVoidAssignment', weight=1.0))), 'ConstPropertyContributions': ContributionMatcherSpec(name='ConstPropertyContributions', inputs=(AssemblyInputSpec(name='field', collection_name='ConstFields', collection=None),), default_contribution_name='ConstFieldProperty', rules=()), 'StaticPropertyContributions': ContributionMatcherSpec(name='StaticPropertyContributions', inputs=(AssemblyInputSpec(name='field', collection_name='StaticFields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='unset', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(False)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='StaticUnsetFieldProperty', weight=1.0), ContributionRuleSpec(name='default_value', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='StaticDefaultFieldProperty', weight=1.0), ContributionRuleSpec(name='default_factory', condition=EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(True)), contribution_name='StaticDefaultFactoryFieldProperty', weight=1.0))), 'StaticDefaultFactoryArgContributions': ContributionMatcherSpec(name='StaticDefaultFactoryArgContributions', inputs=(AssemblyInputSpec(name='dep', collection_name='DefaultFactoryDependencies', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='static_empty', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('ConsumerFieldKind'), right=LiteralValueRef('static')), EqConditionSpec(left=ValueRef('ParamName'), right=LiteralValueRef('')))), contribution_name='StaticDefaultFactoryEmptyArgContribution', weight=1.0), ContributionRuleSpec(name='static_field', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('ConsumerFieldKind'), right=LiteralValueRef('static')), EqConditionSpec(left=ValueRef('ProviderFieldKind'), right=LiteralValueRef('field')))), contribution_name='StaticDefaultFactoryStoredArgContribution', weight=1.0), ContributionRuleSpec(name='static_const', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('ConsumerFieldKind'), right=LiteralValueRef('static')), EqConditionSpec(left=ValueRef('ProviderFieldKind'), right=LiteralValueRef('const')))), contribution_name='StaticDefaultFactoryStoredArgContribution', weight=1.0), ContributionRuleSpec(name='static_static', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('ConsumerFieldKind'), right=LiteralValueRef('static')), EqConditionSpec(left=ValueRef('ProviderFieldKind'), right=LiteralValueRef('static')))), contribution_name='StaticDefaultFactoryStoredArgContribution', weight=1.0), ContributionRuleSpec(name='static_classvar', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('ConsumerFieldKind'), right=LiteralValueRef('static')), EqConditionSpec(left=ValueRef('ProviderFieldKind'), right=LiteralValueRef('classvar')))), contribution_name='StaticDefaultFactoryStoredArgContribution', weight=1.0), ContributionRuleSpec(name='static_managed', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('ConsumerFieldKind'), right=LiteralValueRef('static')), EqConditionSpec(left=ValueRef('ProviderFieldKind'), right=LiteralValueRef('managed')))), contribution_name='StaticDefaultFactoryStoredArgContribution', weight=1.0), ContributionRuleSpec(name='static_binding', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('ConsumerFieldKind'), right=LiteralValueRef('static')), EqConditionSpec(left=ValueRef('ProviderFieldKind'), right=LiteralValueRef('binding')))), contribution_name='StaticDefaultFactoryStoredArgContribution', weight=1.0), ContributionRuleSpec(name='static_owned', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('ConsumerFieldKind'), right=LiteralValueRef('static')), EqConditionSpec(left=ValueRef('ProviderFieldKind'), right=LiteralValueRef('owned')))), contribution_name='StaticDefaultFactoryStoredArgContribution', weight=1.0), ContributionRuleSpec(name='static_transient', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('ConsumerFieldKind'), right=LiteralValueRef('static')), EqConditionSpec(left=ValueRef('ProviderFieldKind'), right=LiteralValueRef('transient')))), contribution_name='StaticDefaultFactoryStoredArgContribution', weight=1.0)))}
ASSEMBLY_EDGES = {'CoreModuleProduction.lifecycle_definition_params': AssemblyEdgeSpec(name='CoreModuleProduction.lifecycle_definition_params', context_inputs=(), from_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), condition=None, matcher_name='BuilderParamContributions'), 'CoreModuleProduction.annotations_params': AssemblyEdgeSpec(name='CoreModuleProduction.annotations_params', context_inputs=(), from_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), condition=None, matcher_name='AnnotationsBuilderParamContributions'), 'CoreModuleProduction.tx_keys_params': AssemblyEdgeSpec(name='CoreModuleProduction.tx_keys_params', context_inputs=(), from_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), condition=None, matcher_name='TxKeysBuilderParamContributions'), 'CoreModuleProduction.field_default_params': AssemblyEdgeSpec(name='CoreModuleProduction.field_default_params', context_inputs=(), from_inputs=(AssemblyInputSpec(name='field', collection_name='Fields', collection=None),), condition=None, matcher_name='FieldDefaultBuilderParamContributions'), 'CoreModuleProduction.classes': AssemblyEdgeSpec(name='CoreModuleProduction.classes', context_inputs=(), from_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), condition=None, matcher_name='CoreClassDefinitionContributions'), 'CoreModuleProduction.return_class': AssemblyEdgeSpec(name='CoreModuleProduction.return_class', context_inputs=(), from_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), condition=None, matcher_name='ReturnClassContributions'), 'CoreClassProduction.state_slots': AssemblyEdgeSpec(name='CoreClassProduction.state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='PlainFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='PlainStateSlotContributions'), 'CoreClassProduction.transaction_manager_param': AssemblyEdgeSpec(name='CoreClassProduction.transaction_manager_param', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='TransactionManagerInitParamContributions'), 'CoreClassProduction.commit_order_key_fallback': AssemblyEdgeSpec(name='CoreClassProduction.commit_order_key_fallback', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='CommitOrderKeyFallbackContributions'), 'CoreClassProduction.requires_validation_fallback': AssemblyEdgeSpec(name='CoreClassProduction.requires_validation_fallback', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='RequiresValidationFallbackContributions'), 'CoreClassProduction.validate_commit_fallback': AssemblyEdgeSpec(name='CoreClassProduction.validate_commit_fallback', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='ValidateCommitFallbackContributions'), 'CoreClassProduction.before_commit_fallback': AssemblyEdgeSpec(name='CoreClassProduction.before_commit_fallback', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='BeforeCommitFallbackContributions'), 'CoreClassProduction.prepare_commit_dispatch_fallback': AssemblyEdgeSpec(name='CoreClassProduction.prepare_commit_dispatch_fallback', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='PrepareCommitDispatchFallbackContributions'), 'CoreClassProduction.commit_dispatch_fallback': AssemblyEdgeSpec(name='CoreClassProduction.commit_dispatch_fallback', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='CommitDispatchFallbackContributions'), 'CoreClassProduction.after_commit_fallback': AssemblyEdgeSpec(name='CoreClassProduction.after_commit_fallback', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='AfterCommitFallbackContributions'), 'CoreClassProduction.rollback_dispatch_fallback': AssemblyEdgeSpec(name='CoreClassProduction.rollback_dispatch_fallback', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='RollbackDispatchFallbackContributions'), 'CoreClassProduction.after_rollback_fallback': AssemblyEdgeSpec(name='CoreClassProduction.after_rollback_fallback', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='AfterRollbackFallbackContributions'), 'CoreClassProduction.classvars': AssemblyEdgeSpec(name='CoreClassProduction.classvars', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ClassVarFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ClassVarDefaultContributions'), 'CoreClassProduction.commit_order_keys': AssemblyEdgeSpec(name='CoreClassProduction.commit_order_keys', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='method', collection_name='CommitOrderKeyProviders', collection=None),), condition=EqConditionSpec(left=ValueRef('MethodOwner'), right=ValueRef('ClassId')), matcher_name='CommitOrderKeyContributions'), 'CoreClassProduction.validation_flags': AssemblyEdgeSpec(name='CoreClassProduction.validation_flags', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='method', collection_name='CommitValidators', collection=None),), condition=EqConditionSpec(left=ValueRef('MethodOwner'), right=ValueRef('ClassId')), matcher_name='RequiresValidationContributions'), 'CoreClassProduction.validators': AssemblyEdgeSpec(name='CoreClassProduction.validators', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='method', collection_name='CommitValidators', collection=None),), condition=EqConditionSpec(left=ValueRef('MethodOwner'), right=ValueRef('ClassId')), matcher_name='ValidateCommitContributions'), 'CoreClassProduction.before_commit_hooks': AssemblyEdgeSpec(name='CoreClassProduction.before_commit_hooks', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='method', collection_name='BeforeCommitHooks', collection=None),), condition=EqConditionSpec(left=ValueRef('MethodOwner'), right=ValueRef('ClassId')), matcher_name='BeforeCommitHookContributions'), 'CoreClassProduction.after_commit_hooks': AssemblyEdgeSpec(name='CoreClassProduction.after_commit_hooks', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='method', collection_name='AfterCommitHooks', collection=None),), condition=EqConditionSpec(left=ValueRef('MethodOwner'), right=ValueRef('ClassId')), matcher_name='AfterCommitHookContributions'), 'CoreClassProduction.after_rollback_hooks': AssemblyEdgeSpec(name='CoreClassProduction.after_rollback_hooks', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='method', collection_name='AfterRollbackHooks', collection=None),), condition=EqConditionSpec(left=ValueRef('MethodOwner'), right=ValueRef('ClassId')), matcher_name='AfterRollbackHookContributions'), 'CoreClassProduction.plain_init_params': AssemblyEdgeSpec(name='CoreClassProduction.plain_init_params', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='PlainFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='PlainInitParamContributions'), 'CoreClassProduction.initvar_params': AssemblyEdgeSpec(name='CoreClassProduction.initvar_params', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='InitVarFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='InitVarParamContributions'), 'CoreClassProduction.initvar_local_defaults': AssemblyEdgeSpec(name='CoreClassProduction.initvar_local_defaults', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='InitVarFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='InitVarLocalDefaultContributions'), 'CoreClassProduction.plain_init_assignments': AssemblyEdgeSpec(name='CoreClassProduction.plain_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='PlainFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='PlainInitAssignmentContributions'), 'CoreClassProduction.plain_properties': AssemblyEdgeSpec(name='CoreClassProduction.plain_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='PlainFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='PlainPropertyContributions'), 'CoreModuleProduction.managed_freeze_params': AssemblyEdgeSpec(name='CoreModuleProduction.managed_freeze_params', context_inputs=(), from_inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), condition=None, matcher_name='ManagedFreezeBuilderParamContributions'), 'CoreModuleProduction.managed_thaw_params': AssemblyEdgeSpec(name='CoreModuleProduction.managed_thaw_params', context_inputs=(), from_inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), condition=None, matcher_name='ManagedThawBuilderParamContributions'), 'CoreClassProduction.managed_current_state_slots': AssemblyEdgeSpec(name='CoreClassProduction.managed_current_state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedCurrentStateSlotContributions'), 'CoreClassProduction.managed_working_state_slots': AssemblyEdgeSpec(name='CoreClassProduction.managed_working_state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedWorkingStateSlotContributions'), 'CoreClassProduction.managed_staged_state_slots': AssemblyEdgeSpec(name='CoreClassProduction.managed_staged_state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedStagedStateSlotContributions'), 'CoreClassProduction.commit_order_key_helpers': AssemblyEdgeSpec(name='CoreClassProduction.commit_order_key_helpers', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='CommitOrderKeyHelperContributions'), 'CoreClassProduction.requires_validation_helpers': AssemblyEdgeSpec(name='CoreClassProduction.requires_validation_helpers', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='RequiresValidationHelperContributions'), 'CoreClassProduction.validate_commit_helpers': AssemblyEdgeSpec(name='CoreClassProduction.validate_commit_helpers', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='ValidateCommitHelperContributions'), 'CoreClassProduction.before_commit_helpers': AssemblyEdgeSpec(name='CoreClassProduction.before_commit_helpers', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='BeforeCommitHelperContributions'), 'CoreClassProduction.after_commit_helpers': AssemblyEdgeSpec(name='CoreClassProduction.after_commit_helpers', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='AfterCommitHelperContributions'), 'CoreClassProduction.after_rollback_helpers': AssemblyEdgeSpec(name='CoreClassProduction.after_rollback_helpers', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='AfterRollbackHelperContributions'), 'CoreClassProduction.commit_order_key_dispatch': AssemblyEdgeSpec(name='CoreClassProduction.commit_order_key_dispatch', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='CommitOrderKeyDispatchContributions'), 'CoreClassProduction.requires_validation_dispatch': AssemblyEdgeSpec(name='CoreClassProduction.requires_validation_dispatch', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='RequiresValidationDispatchContributions'), 'CoreClassProduction.validate_commit_dispatch': AssemblyEdgeSpec(name='CoreClassProduction.validate_commit_dispatch', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='ValidateCommitDispatchContributions'), 'CoreClassProduction.before_commit_dispatch': AssemblyEdgeSpec(name='CoreClassProduction.before_commit_dispatch', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='BeforeCommitDispatchContributions'), 'CoreClassProduction.after_commit_dispatch': AssemblyEdgeSpec(name='CoreClassProduction.after_commit_dispatch', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='AfterCommitDispatchContributions'), 'CoreClassProduction.after_rollback_dispatch': AssemblyEdgeSpec(name='CoreClassProduction.after_rollback_dispatch', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='AfterRollbackDispatchContributions'), 'CoreClassProduction.managed_init_params': AssemblyEdgeSpec(name='CoreClassProduction.managed_init_params', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedInitParamContributions'), 'CoreClassProduction.managed_current_init_assignments': AssemblyEdgeSpec(name='CoreClassProduction.managed_current_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedCurrentInitAssignmentContributions'), 'CoreClassProduction.managed_working_init_assignments': AssemblyEdgeSpec(name='CoreClassProduction.managed_working_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedWorkingInitAssignmentContributions'), 'CoreClassProduction.managed_staged_init_assignments': AssemblyEdgeSpec(name='CoreClassProduction.managed_staged_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedStagedInitAssignmentContributions'), 'CoreClassProduction.managed_default_properties': AssemblyEdgeSpec(name='CoreClassProduction.managed_default_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransactionalFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedDefaultFacadePropertyContributions'), 'CoreClassProduction.managed_current_properties': AssemblyEdgeSpec(name='CoreClassProduction.managed_current_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransactionalFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedCurrentFacadePropertyContributions'), 'CoreClassProduction.managed_working_properties': AssemblyEdgeSpec(name='CoreClassProduction.managed_working_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransactionalFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedWorkingFacadePropertyContributions'), 'CoreClassProduction.apply_prepared_commit_helpers': AssemblyEdgeSpec(name='CoreClassProduction.apply_prepared_commit_helpers', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='ApplyPreparedCommitFieldsContributions'), 'CoreClassProduction.prepare_commit_helpers': AssemblyEdgeSpec(name='CoreClassProduction.prepare_commit_helpers', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='PrepareCommitFieldsContributions'), 'CoreClassProduction.rollback_helpers': AssemblyEdgeSpec(name='CoreClassProduction.rollback_helpers', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='RollbackFieldsContributions'), 'CoreClassProduction.prepare_commit_dispatch': AssemblyEdgeSpec(name='CoreClassProduction.prepare_commit_dispatch', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='PrepareCommitDispatchContributions'), 'CoreClassProduction.apply_prepared_commit_dispatch': AssemblyEdgeSpec(name='CoreClassProduction.apply_prepared_commit_dispatch', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='ApplyPreparedCommitDispatchContributions'), 'CoreClassProduction.rollback_dispatch': AssemblyEdgeSpec(name='CoreClassProduction.rollback_dispatch', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='RollbackDispatchContributions'), 'CoreClassProduction.managed_prepare_commit': AssemblyEdgeSpec(name='CoreClassProduction.managed_prepare_commit', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransactionalFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedPrepareCommitContributions'), 'CoreClassProduction.managed_apply_prepared_commit': AssemblyEdgeSpec(name='CoreClassProduction.managed_apply_prepared_commit', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransactionalFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedApplyPreparedCommitContributions'), 'CoreClassProduction.managed_rollback': AssemblyEdgeSpec(name='CoreClassProduction.managed_rollback', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransactionalFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedRollbackContributions'), 'CoreClassProduction.default_factory_evals': AssemblyEdgeSpec(name='CoreClassProduction.default_factory_evals', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='step', collection_name='DefaultFactoryEvaluationSteps', collection=None),), condition=EqConditionSpec(left=ValueRef('EvalOwner'), right=ValueRef('ClassId')), matcher_name='DefaultFactoryEvalContributions'), 'CoreClassProduction.default_factory_args': AssemblyEdgeSpec(name='CoreClassProduction.default_factory_args', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='dep', collection_name='DefaultFactoryDependencies', collection=None),), condition=EqConditionSpec(left=ValueRef('DependencyOwner'), right=ValueRef('ClassId')), matcher_name='DefaultFactoryArgContributions'), 'CoreModuleProduction.transient_working_default_params': AssemblyEdgeSpec(name='CoreModuleProduction.transient_working_default_params', context_inputs=(), from_inputs=(AssemblyInputSpec(name='field', collection_name='Fields', collection=None),), condition=None, matcher_name='TransientWorkingDefaultBuilderParamContributions'), 'CoreClassProduction.transient_current_state_slots': AssemblyEdgeSpec(name='CoreClassProduction.transient_current_state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='TransientFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='TransientCurrentStateSlotContributions'), 'CoreClassProduction.transient_working_state_slots': AssemblyEdgeSpec(name='CoreClassProduction.transient_working_state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='TransientFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='TransientWorkingStateSlotContributions'), 'CoreClassProduction.retained_initvar_state_slots': AssemblyEdgeSpec(name='CoreClassProduction.retained_initvar_state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='initvar', collection_name='RetainedInitVars', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='RetainedInitVarStateSlotContributions'), 'CoreClassProduction.transient_init_params': AssemblyEdgeSpec(name='CoreClassProduction.transient_init_params', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='TransientFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='TransientInitParamContributions'), 'CoreClassProduction.transient_current_init_assignments': AssemblyEdgeSpec(name='CoreClassProduction.transient_current_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='TransientFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='TransientCurrentInitAssignmentContributions'), 'CoreClassProduction.transient_working_init_assignments': AssemblyEdgeSpec(name='CoreClassProduction.transient_working_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='TransientFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='TransientWorkingInitAssignmentContributions'), 'CoreClassProduction.retained_initvar_state_assignments': AssemblyEdgeSpec(name='CoreClassProduction.retained_initvar_state_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='initvar', collection_name='RetainedInitVars', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='RetainedInitVarStateAssignmentContributions'), 'CoreClassProduction.transient_default_properties': AssemblyEdgeSpec(name='CoreClassProduction.transient_default_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransientFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='TransientDefaultFacadePropertyContributions'), 'CoreClassProduction.transient_current_properties': AssemblyEdgeSpec(name='CoreClassProduction.transient_current_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='TransientFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='TransientCurrentPropertyContributions'), 'CoreClassProduction.transient_working_properties': AssemblyEdgeSpec(name='CoreClassProduction.transient_working_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransientFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='TransientWorkingFacadePropertyContributions'), 'CoreClassProduction.transient_default_working_factory_args': AssemblyEdgeSpec(name='CoreClassProduction.transient_default_working_factory_args', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='arg', collection_name='TransientWorkingFactoryArgs', collection=None),), condition=EqConditionSpec(left=ValueRef('WorkingFactoryArgOwner'), right=ValueRef('ClassId')), matcher_name='TransientDefaultWorkingFactoryArgContributions'), 'CoreClassProduction.transient_working_working_factory_args': AssemblyEdgeSpec(name='CoreClassProduction.transient_working_working_factory_args', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='arg', collection_name='TransientWorkingFactoryArgs', collection=None),), condition=EqConditionSpec(left=ValueRef('WorkingFactoryArgOwner'), right=ValueRef('ClassId')), matcher_name='TransientWorkingWorkingFactoryArgContributions'), 'CoreClassProduction.transient_apply_prepared_commit': AssemblyEdgeSpec(name='CoreClassProduction.transient_apply_prepared_commit', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransientFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='TransientApplyPreparedCommitContributions'), 'CoreClassProduction.transient_rollback': AssemblyEdgeSpec(name='CoreClassProduction.transient_rollback', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransientFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='TransientRollbackContributions'), 'CoreModuleProduction.binding_support_helpers': AssemblyEdgeSpec(name='CoreModuleProduction.binding_support_helpers', context_inputs=(), from_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), condition=None, matcher_name='BindingSupportHelperContributions'), 'CoreClassProduction.binding_state_slots': AssemblyEdgeSpec(name='CoreClassProduction.binding_state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='BindingFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='BindingStateSlotContributions'), 'CoreClassProduction.owned_current_state_slots': AssemblyEdgeSpec(name='CoreClassProduction.owned_current_state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='OwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedCurrentStateSlotContributions'), 'CoreClassProduction.owned_working_state_slots': AssemblyEdgeSpec(name='CoreClassProduction.owned_working_state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='OwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedWorkingStateSlotContributions'), 'CoreClassProduction.owned_staged_state_slots': AssemblyEdgeSpec(name='CoreClassProduction.owned_staged_state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='OwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedStagedStateSlotContributions'), 'CoreClassProduction.binding_init_params': AssemblyEdgeSpec(name='CoreClassProduction.binding_init_params', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='BindingFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='BindingInitParamContributions'), 'CoreClassProduction.owned_init_params': AssemblyEdgeSpec(name='CoreClassProduction.owned_init_params', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='OwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedInitParamContributions'), 'CoreClassProduction.binding_init_assignments': AssemblyEdgeSpec(name='CoreClassProduction.binding_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='BindingFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='BindingInitAssignmentContributions'), 'CoreClassProduction.owned_current_init_assignments': AssemblyEdgeSpec(name='CoreClassProduction.owned_current_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='OwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedCurrentInitAssignmentContributions'), 'CoreClassProduction.owned_working_init_assignments': AssemblyEdgeSpec(name='CoreClassProduction.owned_working_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='OwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedWorkingInitAssignmentContributions'), 'CoreClassProduction.owned_staged_init_assignments': AssemblyEdgeSpec(name='CoreClassProduction.owned_staged_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='OwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedStagedInitAssignmentContributions'), 'CoreClassProduction.binding_properties': AssemblyEdgeSpec(name='CoreClassProduction.binding_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='BindingFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='BindingPropertyContributions'), 'CoreClassProduction.owned_default_properties': AssemblyEdgeSpec(name='CoreClassProduction.owned_default_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedOwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedDefaultFacadePropertyContributions'), 'CoreClassProduction.owned_current_properties': AssemblyEdgeSpec(name='CoreClassProduction.owned_current_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedOwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedCurrentFacadePropertyContributions'), 'CoreClassProduction.owned_working_properties': AssemblyEdgeSpec(name='CoreClassProduction.owned_working_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedOwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedWorkingFacadePropertyContributions'), 'CoreClassProduction.owned_apply_prepared_commit': AssemblyEdgeSpec(name='CoreClassProduction.owned_apply_prepared_commit', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedOwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedApplyPreparedCommitContributions'), 'CoreClassProduction.owned_rollback': AssemblyEdgeSpec(name='CoreClassProduction.owned_rollback', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedOwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedRollbackContributions'), 'CoreClassProduction.owned_prepare_commit': AssemblyEdgeSpec(name='CoreClassProduction.owned_prepare_commit', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedOwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedPrepareCommitContributions'), 'CoreClassProduction.const_state_slots': AssemblyEdgeSpec(name='CoreClassProduction.const_state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ConstFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ConstStateSlotContributions'), 'CoreClassProduction.static_state_slots': AssemblyEdgeSpec(name='CoreClassProduction.static_state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='StaticFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='StaticStateSlotContributions'), 'CoreClassProduction.const_init_params': AssemblyEdgeSpec(name='CoreClassProduction.const_init_params', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ConstFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ConstInitParamContributions'), 'CoreClassProduction.static_init_params': AssemblyEdgeSpec(name='CoreClassProduction.static_init_params', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='StaticFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='StaticInitParamContributions'), 'CoreClassProduction.const_init_assignments': AssemblyEdgeSpec(name='CoreClassProduction.const_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ConstFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ConstInitAssignmentContributions'), 'CoreClassProduction.static_init_assignments': AssemblyEdgeSpec(name='CoreClassProduction.static_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='StaticFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='StaticInitAssignmentContributions'), 'CoreClassProduction.const_properties': AssemblyEdgeSpec(name='CoreClassProduction.const_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ConstFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ConstPropertyContributions'), 'CoreClassProduction.static_properties': AssemblyEdgeSpec(name='CoreClassProduction.static_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='StaticFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='StaticPropertyContributions'), 'CoreClassProduction.static_default_factory_args': AssemblyEdgeSpec(name='CoreClassProduction.static_default_factory_args', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='dep', collection_name='DefaultFactoryDependencies', collection=None),), condition=EqConditionSpec(left=ValueRef('DependencyOwner'), right=ValueRef('ClassId')), matcher_name='StaticDefaultFactoryArgContributions')}
ASSEMBLY_PRODUCTIONS = {'CoreModuleProduction': ComposableProductionSpec(name='CoreModuleProduction', inputs=(), root=RootSpec(build_name='Root', resource_name='ModuleRoot', bindings=()), applies=(InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreModuleProduction.lifecycle_definition_params', context_inputs=(), from_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), condition=None, matcher_name='BuilderParamContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreModuleProduction.annotations_params', context_inputs=(), from_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), condition=None, matcher_name='AnnotationsBuilderParamContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreModuleProduction.tx_keys_params', context_inputs=(), from_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), condition=None, matcher_name='TxKeysBuilderParamContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreModuleProduction.field_default_params', context_inputs=(), from_inputs=(AssemblyInputSpec(name='field', collection_name='Fields', collection=None),), condition=None, matcher_name='FieldDefaultBuilderParamContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreModuleProduction.transient_working_default_params', context_inputs=(), from_inputs=(AssemblyInputSpec(name='field', collection_name='Fields', collection=None),), condition=None, matcher_name='TransientWorkingDefaultBuilderParamContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreModuleProduction.binding_support_helpers', context_inputs=(), from_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), condition=None, matcher_name='BindingSupportHelperContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreModuleProduction.managed_freeze_params', context_inputs=(), from_inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), condition=None, matcher_name='ManagedFreezeBuilderParamContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreModuleProduction.managed_thaw_params', context_inputs=(), from_inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), condition=None, matcher_name='ManagedThawBuilderParamContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreModuleProduction.classes', context_inputs=(), from_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), condition=None, matcher_name='CoreClassDefinitionContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreModuleProduction.return_class', context_inputs=(), from_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), condition=None, matcher_name='ReturnClassContributions')))), 'CoreClassProduction': ComposableProductionSpec(name='CoreClassProduction', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), root=RootSpec(build_name='ClassDef', resource_name='ClassBundle', bindings=(BindingSpec(kind='ident', name='state_class_decl_name', value=ValueRef('StateClassName')), BindingSpec(kind='ident', name='state_class_ref', value=ValueRef('StateClassName')), BindingSpec(kind='ident', name='default_facade_class_decl_name', value=ValueRef('ClassName')), BindingSpec(kind='ident', name='default_facade_class_ref', value=ValueRef('ClassName')), BindingSpec(kind='ident', name='facade_base_decl_name', value=ValueRef('FacadeBaseClassName')), BindingSpec(kind='ident', name='facade_base_default_base_name', value=ValueRef('FacadeBaseClassName')), BindingSpec(kind='ident', name='facade_base_current_base_name', value=ValueRef('FacadeBaseClassName')), BindingSpec(kind='ident', name='facade_base_working_base_name', value=ValueRef('FacadeBaseClassName')), BindingSpec(kind='ident', name='current_facade_class_decl_name', value=ValueRef('CurrentFacadeClassName')), BindingSpec(kind='ident', name='current_facade_class_ref', value=ValueRef('CurrentFacadeClassName')), BindingSpec(kind='ident', name='working_facade_class_decl_name', value=ValueRef('WorkingFacadeClassName')), BindingSpec(kind='ident', name='working_facade_class_ref', value=ValueRef('WorkingFacadeClassName')), BindingSpec(kind='ident', name='tx_keys_for_index_name', value=ValueRef('TxKeysParamName')), BindingSpec(kind='ident', name='tx_keys_for_map_name', value=ValueRef('TxKeysParamName')), BindingSpec(kind='ident', name='tx_keys_for_class_index_name', value=ValueRef('TxKeysParamName')), BindingSpec(kind='ident', name='tx_keys_for_class_map_name', value=ValueRef('TxKeysParamName')), BindingSpec(kind='ident', name='tx_keys_for_manager_name', value=ValueRef('TxKeysParamName')), BindingSpec(kind='ident', name='tx_keys_for_slots_name', value=ValueRef('TxKeysParamName')), BindingSpec(kind='ident', name='lifecycle_definition_name', value=ValueRef('LifecycleDefinitionParamName')), BindingSpec(kind='ident', name='annotations_name', value=ValueRef('AnnotationsParamName')), BindingSpec(kind='external', name='lifecycle_field_names', value=ValueRef('LifecycleFieldNames')))), applies=(InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='PlainFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='PlainStateSlotContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.const_state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ConstFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ConstStateSlotContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.static_state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='StaticFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='StaticStateSlotContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.binding_state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='BindingFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='BindingStateSlotContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.owned_current_state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='OwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedCurrentStateSlotContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.owned_working_state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='OwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedWorkingStateSlotContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.owned_staged_state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='OwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedStagedStateSlotContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.managed_current_state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedCurrentStateSlotContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.transient_current_state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='TransientFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='TransientCurrentStateSlotContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.managed_working_state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedWorkingStateSlotContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.transient_working_state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='TransientFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='TransientWorkingStateSlotContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.retained_initvar_state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='initvar', collection_name='RetainedInitVars', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='RetainedInitVarStateSlotContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.managed_staged_state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedStagedStateSlotContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.transaction_manager_param', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='TransactionManagerInitParamContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.commit_order_key_fallback', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='CommitOrderKeyFallbackContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.requires_validation_fallback', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='RequiresValidationFallbackContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.validate_commit_fallback', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='ValidateCommitFallbackContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.before_commit_fallback', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='BeforeCommitFallbackContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.prepare_commit_dispatch_fallback', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='PrepareCommitDispatchFallbackContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.commit_dispatch_fallback', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='CommitDispatchFallbackContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.after_commit_fallback', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='AfterCommitFallbackContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.rollback_dispatch_fallback', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='RollbackDispatchFallbackContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.after_rollback_fallback', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='AfterRollbackFallbackContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.commit_order_key_helpers', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='CommitOrderKeyHelperContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.requires_validation_helpers', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='RequiresValidationHelperContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.validate_commit_helpers', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='ValidateCommitHelperContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.before_commit_helpers', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='BeforeCommitHelperContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.after_commit_helpers', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='AfterCommitHelperContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.after_rollback_helpers', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='AfterRollbackHelperContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.commit_order_key_dispatch', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='CommitOrderKeyDispatchContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.requires_validation_dispatch', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='RequiresValidationDispatchContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.validate_commit_dispatch', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='ValidateCommitDispatchContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.before_commit_dispatch', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='BeforeCommitDispatchContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.after_commit_dispatch', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='AfterCommitDispatchContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.after_rollback_dispatch', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='AfterRollbackDispatchContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.classvars', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ClassVarFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ClassVarDefaultContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.commit_order_keys', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='method', collection_name='CommitOrderKeyProviders', collection=None),), condition=EqConditionSpec(left=ValueRef('MethodOwner'), right=ValueRef('ClassId')), matcher_name='CommitOrderKeyContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.validation_flags', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='method', collection_name='CommitValidators', collection=None),), condition=EqConditionSpec(left=ValueRef('MethodOwner'), right=ValueRef('ClassId')), matcher_name='RequiresValidationContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.validators', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='method', collection_name='CommitValidators', collection=None),), condition=EqConditionSpec(left=ValueRef('MethodOwner'), right=ValueRef('ClassId')), matcher_name='ValidateCommitContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.before_commit_hooks', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='method', collection_name='BeforeCommitHooks', collection=None),), condition=EqConditionSpec(left=ValueRef('MethodOwner'), right=ValueRef('ClassId')), matcher_name='BeforeCommitHookContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.after_commit_hooks', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='method', collection_name='AfterCommitHooks', collection=None),), condition=EqConditionSpec(left=ValueRef('MethodOwner'), right=ValueRef('ClassId')), matcher_name='AfterCommitHookContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.after_rollback_hooks', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='method', collection_name='AfterRollbackHooks', collection=None),), condition=EqConditionSpec(left=ValueRef('MethodOwner'), right=ValueRef('ClassId')), matcher_name='AfterRollbackHookContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.plain_init_params', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='PlainFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='PlainInitParamContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.const_init_params', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ConstFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ConstInitParamContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.static_init_params', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='StaticFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='StaticInitParamContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.binding_init_params', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='BindingFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='BindingInitParamContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.owned_init_params', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='OwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedInitParamContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.initvar_params', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='InitVarFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='InitVarParamContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.managed_init_params', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedInitParamContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.transient_init_params', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='TransientFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='TransientInitParamContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.initvar_local_defaults', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='InitVarFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='InitVarLocalDefaultContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.plain_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='PlainFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='PlainInitAssignmentContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.const_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ConstFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ConstInitAssignmentContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.static_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='StaticFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='StaticInitAssignmentContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.binding_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='BindingFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='BindingInitAssignmentContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.owned_current_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='OwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedCurrentInitAssignmentContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.managed_current_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedCurrentInitAssignmentContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.transient_current_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='TransientFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='TransientCurrentInitAssignmentContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.managed_working_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedWorkingInitAssignmentContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.transient_working_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='TransientFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='TransientWorkingInitAssignmentContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.owned_working_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='OwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedWorkingInitAssignmentContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.retained_initvar_state_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='initvar', collection_name='RetainedInitVars', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='RetainedInitVarStateAssignmentContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.owned_staged_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='OwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedStagedInitAssignmentContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.managed_staged_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ManagedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedStagedInitAssignmentContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.default_factory_evals', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='step', collection_name='DefaultFactoryEvaluationSteps', collection=None),), condition=EqConditionSpec(left=ValueRef('EvalOwner'), right=ValueRef('ClassId')), matcher_name='DefaultFactoryEvalContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.default_factory_args', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='dep', collection_name='DefaultFactoryDependencies', collection=None),), condition=EqConditionSpec(left=ValueRef('DependencyOwner'), right=ValueRef('ClassId')), matcher_name='DefaultFactoryArgContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.plain_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='PlainFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='PlainPropertyContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.const_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ConstFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ConstPropertyContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.static_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='StaticFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='StaticPropertyContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.static_default_factory_args', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='dep', collection_name='DefaultFactoryDependencies', collection=None),), condition=EqConditionSpec(left=ValueRef('DependencyOwner'), right=ValueRef('ClassId')), matcher_name='StaticDefaultFactoryArgContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.binding_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='BindingFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='BindingPropertyContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.owned_default_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedOwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedDefaultFacadePropertyContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.managed_default_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransactionalFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedDefaultFacadePropertyContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.transient_default_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransientFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='TransientDefaultFacadePropertyContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.managed_current_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransactionalFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedCurrentFacadePropertyContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.transient_current_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='TransientFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='TransientCurrentPropertyContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.owned_current_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedOwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedCurrentFacadePropertyContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.managed_working_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransactionalFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedWorkingFacadePropertyContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.owned_working_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedOwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedWorkingFacadePropertyContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.transient_working_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransientFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='TransientWorkingFacadePropertyContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.transient_default_working_factory_args', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='arg', collection_name='TransientWorkingFactoryArgs', collection=None),), condition=EqConditionSpec(left=ValueRef('WorkingFactoryArgOwner'), right=ValueRef('ClassId')), matcher_name='TransientDefaultWorkingFactoryArgContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.transient_working_working_factory_args', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='arg', collection_name='TransientWorkingFactoryArgs', collection=None),), condition=EqConditionSpec(left=ValueRef('WorkingFactoryArgOwner'), right=ValueRef('ClassId')), matcher_name='TransientWorkingWorkingFactoryArgContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.apply_prepared_commit_helpers', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='ApplyPreparedCommitFieldsContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.prepare_commit_helpers', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='PrepareCommitFieldsContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.rollback_helpers', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='RollbackFieldsContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.prepare_commit_dispatch', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='PrepareCommitDispatchContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.apply_prepared_commit_dispatch', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='ApplyPreparedCommitDispatchContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.rollback_dispatch', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='tx_key', collection_name='TxKeys', collection=None),), condition=EqConditionSpec(left=ValueRef('TxOwner'), right=ValueRef('ClassId')), matcher_name='RollbackDispatchContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.managed_prepare_commit', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransactionalFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedPrepareCommitContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.managed_apply_prepared_commit', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransactionalFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedApplyPreparedCommitContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.owned_apply_prepared_commit', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedOwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedApplyPreparedCommitContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.transient_apply_prepared_commit', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransientFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='TransientApplyPreparedCommitContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.managed_rollback', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransactionalFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ManagedRollbackContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.owned_rollback', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedOwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedRollbackContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.transient_rollback', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedTransientFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='TransientRollbackContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.owned_prepare_commit', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='IndexedOwnedFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='OwnedPrepareCommitContributions'))))}
ASSEMBLY_ASSEMBLIES = {'LifecycleCoreModule': AssemblySpec(name='LifecycleCoreModule', production_name='CoreModuleProduction'), 'LifecycleModule': AssemblySpec(name='LifecycleModule', production_name='CoreModuleProduction')}

ASSEMBLY_CONCEPT = _YidlSimpleNamespace(
    properties=ASSEMBLY_PROPERTIES,
    resources=ASSEMBLY_RESOURCES,
    contributions=ASSEMBLY_CONTRIBUTIONS,
    contribution_matchers=ASSEMBLY_MATCHERS,
    assembly_edges=ASSEMBLY_EDGES,
    composable_productions=ASSEMBLY_PRODUCTIONS,
    assemblies=ASSEMBLY_ASSEMBLIES,
)

_YIDL_BASE_BUILD_CONTAINER = globals().get('build_container')

def build_container(builder):
    if _YIDL_BASE_BUILD_CONTAINER is not None:
        return _YIDL_BASE_BUILD_CONTAINER(builder)
    return builder.freeze()

def build_assembly(entrypoint, container, *, unroll='auto'):
    return run_assembly(ASSEMBLY_CONCEPT, entrypoint, container, unroll=unroll)

def build_LifecycleCoreModule(container, *, unroll='auto'):
    return build_assembly('LifecycleCoreModule', container, unroll=unroll)

def build_LifecycleModule(container, *, unroll='auto'):
    return build_assembly('LifecycleModule', container, unroll=unroll)
