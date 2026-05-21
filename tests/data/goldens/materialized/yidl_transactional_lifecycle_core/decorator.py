from yidl.generation.data_def_sys import AddIfAbsent, DDSContainerBuilder, NOT_PROVIDED, REQUIRED, RejectDuplicate, ReplaceExisting, RuntimeCollection, RuntimeComputedCollection, RuntimeContainerSpec, RuntimePort, RuntimePortIndex, RuntimeProperty, RuntimeRecord, RuntimeUnion
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
_TxGroupsParamNameProperty = RuntimeProperty('TxGroupsParamName', str, default='', storage_name='tx_groups_param_name')
_LifecycleFieldNamesProperty = RuntimeProperty('LifecycleFieldNames', object, default=(), storage_name='lifecycle_field_names')
_FieldIdProperty = RuntimeProperty('FieldId', str, default=REQUIRED, storage_name='field_id')
_FieldOwnerProperty = RuntimeProperty('FieldOwner', str, default=REQUIRED, storage_name='field_owner')
_FieldNameProperty = RuntimeProperty('FieldName', str, default=REQUIRED, storage_name='field_name')
_FieldOrderProperty = RuntimeProperty('FieldOrder', int, default=REQUIRED, storage_name='field_order')
_FieldKindProperty = RuntimeProperty('FieldKind', str, default='field', storage_name='field_kind')
_AnnotationProperty = RuntimeProperty('Annotation', object, default=object, storage_name='annotation')
_InitProperty = RuntimeProperty('Init', bool, default=True, storage_name='init')
_HasDefaultProperty = RuntimeProperty('HasDefault', bool, default=False, storage_name='has_default')
_DefaultValueProperty = RuntimeProperty('DefaultValue', object, default=None, storage_name='default_value')
_DefaultValueParamNameProperty = RuntimeProperty('DefaultValueParamName', str, default='', storage_name='default_value_param_name')
_HasDefaultFactoryProperty = RuntimeProperty('HasDefaultFactory', bool, default=False, storage_name='has_default_factory')
_DefaultFactoryProperty = RuntimeProperty('DefaultFactory', object, default=None, storage_name='default_factory')
_DefaultFactoryParamNameProperty = RuntimeProperty('DefaultFactoryParamName', str, default='', storage_name='default_factory_param_name')
_DefaultFactoryParamNamesProperty = RuntimeProperty('DefaultFactoryParamNames', object, default=(), storage_name='default_factory_param_names')
_TxGroupKeyProperty = RuntimeProperty('TxGroupKey', object, default=None, storage_name='tx_group_key')
_ValueSlotNameProperty = RuntimeProperty('ValueSlotName', str, default='', storage_name='value_slot_name')
_CurrentSlotNameProperty = RuntimeProperty('CurrentSlotName', str, default='', storage_name='current_slot_name')
_WorkingSlotNameProperty = RuntimeProperty('WorkingSlotName', str, default='', storage_name='working_slot_name')
_MethodIdProperty = RuntimeProperty('MethodId', str, default=REQUIRED, storage_name='method_id')
_MethodOwnerProperty = RuntimeProperty('MethodOwner', str, default=REQUIRED, storage_name='method_owner')
_MethodNameProperty = RuntimeProperty('MethodName', str, default=REQUIRED, storage_name='method_name')
_MethodKindProperty = RuntimeProperty('MethodKind', str, default=REQUIRED, storage_name='method_kind')
_DeclarationOrderProperty = RuntimeProperty('DeclarationOrder', int, default=0, storage_name='declaration_order')
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
_LifecycleClassSpec = RuntimeRecord('LifecycleClass', (_ClassIdProperty, _ClassNameProperty, _ClassOrderProperty, _ModuleNameProperty, _StateClassNameProperty, _FacadeBaseClassNameProperty, _CurrentFacadeClassNameProperty, _WorkingFacadeClassNameProperty, _LifecycleDefinitionParamNameProperty, _AnnotationsParamNameProperty, _TxGroupsParamNameProperty, _LifecycleFieldNamesProperty))
_TransactionMethodSpec = RuntimeRecord('TransactionMethod', (_MethodIdProperty, _MethodOwnerProperty, _MethodNameProperty, _MethodKindProperty, _TxGroupKeyProperty, _DeclarationOrderProperty))
_FacadeClassSpec = RuntimeRecord('FacadeClass', (_FacadeOwnerProperty, _FacadeIdProperty, _FacadeKindProperty, _FacadeModeProperty, _FacadeClassNameProperty, _FacadeOrderProperty))
_FacadeExposureSpec = RuntimeRecord('FacadeExposure', (_FacadeOwnerProperty, _OwnerFacadeIdProperty, _FieldNameProperty, _TargetFacadeIdProperty, _ExposureOrderProperty))
_InitParameterSpec = RuntimeRecord('InitParameter', (_InitParameterIdProperty, _InitParameterOwnerProperty, _InitParameterNameProperty, _InitParameterOrderProperty, _InitParameterKindProperty))
_InitAssignmentSpec = RuntimeRecord('InitAssignment', (_InitAssignmentIdProperty, _InitAssignmentOwnerProperty, _InitAssignmentFieldIdProperty, _InitAssignmentFieldNameProperty, _InitAssignmentOrderProperty, _InitAssignmentKindProperty))
_ClassVarAssignmentSpec = RuntimeRecord('ClassVarAssignment', (_ClassVarAssignmentIdProperty, _ClassVarAssignmentOwnerProperty, _ClassVarAssignmentNameProperty, _ClassVarAssignmentOrderProperty))
_PlainFieldSpec = RuntimeRecord('PlainField', (_FieldIdProperty, _FieldOwnerProperty, _FieldNameProperty, _FieldOrderProperty, _FieldKindProperty, _AnnotationProperty, _InitProperty, _HasDefaultProperty, _DefaultValueProperty, _DefaultValueParamNameProperty, _HasDefaultFactoryProperty, _DefaultFactoryProperty, _DefaultFactoryParamNameProperty, _DefaultFactoryParamNamesProperty, _TxGroupKeyProperty, _ValueSlotNameProperty, _CurrentSlotNameProperty, _WorkingSlotNameProperty))
_InitVarFieldSpec = RuntimeRecord('InitVarField', (_FieldIdProperty, _FieldOwnerProperty, _FieldNameProperty, _FieldOrderProperty, _FieldKindProperty, _AnnotationProperty, _InitProperty, _HasDefaultProperty, _DefaultValueProperty, _DefaultValueParamNameProperty, _HasDefaultFactoryProperty, _DefaultFactoryProperty, _DefaultFactoryParamNameProperty, _DefaultFactoryParamNamesProperty, _TxGroupKeyProperty, _ValueSlotNameProperty, _CurrentSlotNameProperty, _WorkingSlotNameProperty))
_ClassVarFieldSpec = RuntimeRecord('ClassVarField', (_FieldIdProperty, _FieldOwnerProperty, _FieldNameProperty, _FieldOrderProperty, _FieldKindProperty, _AnnotationProperty, _InitProperty, _HasDefaultProperty, _DefaultValueProperty, _DefaultValueParamNameProperty, _HasDefaultFactoryProperty, _DefaultFactoryProperty, _DefaultFactoryParamNameProperty, _DefaultFactoryParamNamesProperty, _TxGroupKeyProperty, _ValueSlotNameProperty, _CurrentSlotNameProperty, _WorkingSlotNameProperty))
_LifecycleFieldSpecUnion = RuntimeUnion('LifecycleFieldSpec', (_PlainFieldSpec, _InitVarFieldSpec, _ClassVarFieldSpec))

class LifecycleClass:
    __slots__ = ('class_id', 'class_name', 'class_order', 'module_name', 'state_class_name', 'facade_base_class_name', 'current_facade_class_name', 'working_facade_class_name', 'lifecycle_definition_param_name', 'annotations_param_name', 'tx_groups_param_name', 'lifecycle_field_names')
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

    def __init__(self, *, class_id: str, class_name: str, class_order: int=0, module_name: str='__main__', state_class_name: str, facade_base_class_name: str, current_facade_class_name: str, working_facade_class_name: str, lifecycle_definition_param_name: str='', annotations_param_name: str='', tx_groups_param_name: str='', lifecycle_field_names: object=()):
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
        if not isinstance(tx_groups_param_name, str):
            raise TypeError('TxGroupsParamName must be str, got ' + type(tx_groups_param_name).__name__)
        object.__setattr__(self, 'tx_groups_param_name', tx_groups_param_name)
        object.__setattr__(self, 'lifecycle_field_names', lifecycle_field_names)

    def __setattr__(self, name, value):
        if name in ('class_id', 'class_name', 'class_order', 'module_name', 'state_class_name', 'facade_base_class_name', 'current_facade_class_name', 'working_facade_class_name', 'lifecycle_definition_param_name', 'annotations_param_name', 'tx_groups_param_name', 'lifecycle_field_names'):
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
        pieces.append('tx_groups_param_name=' + repr(self.tx_groups_param_name))
        pieces.append('lifecycle_field_names=' + repr(self.lifecycle_field_names))
        return 'LifecycleClass' + '(' + ', '.join(pieces) + ')'
_LifecycleClassSpec.bind_record_class(LifecycleClass)

class TransactionMethod:
    __slots__ = ('method_id', 'method_owner', 'method_name', 'method_kind', 'tx_group_key', 'declaration_order')
    __dds_record_spec__ = _TransactionMethodSpec
    method_id: str
    method_owner: str
    method_name: str
    method_kind: str
    tx_group_key: object
    declaration_order: int

    def __init__(self, *, method_id: str, method_owner: str, method_name: str, method_kind: str, tx_group_key: object=None, declaration_order: int=0):
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
        object.__setattr__(self, 'tx_group_key', tx_group_key)
        if not isinstance(declaration_order, int):
            raise TypeError('DeclarationOrder must be int, got ' + type(declaration_order).__name__)
        object.__setattr__(self, 'declaration_order', declaration_order)

    def __setattr__(self, name, value):
        if name in ('method_id', 'method_owner', 'method_name', 'method_kind', 'tx_group_key', 'declaration_order'):
            raise AttributeError('TransactionMethod records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('method_id=' + repr(self.method_id))
        pieces.append('method_owner=' + repr(self.method_owner))
        pieces.append('method_name=' + repr(self.method_name))
        pieces.append('method_kind=' + repr(self.method_kind))
        pieces.append('tx_group_key=' + repr(self.tx_group_key))
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
    __slots__ = ('field_id', 'field_owner', 'field_name', 'field_order', 'field_kind', 'annotation', 'init', 'has_default', 'default_value', 'default_value_param_name', 'has_default_factory', 'default_factory', 'default_factory_param_name', 'default_factory_param_names', 'tx_group_key', 'value_slot_name', 'current_slot_name', 'working_slot_name')
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

    def __init__(self, *, field_id: str, field_owner: str, field_name: str, field_order: int, field_kind: str='field', annotation: object=object, init: bool=True, has_default: bool=False, default_value: object=None, default_value_param_name: str='', has_default_factory: bool=False, default_factory: object=None, default_factory_param_name: str='', default_factory_param_names: object=(), tx_group_key: object=None, value_slot_name: str='', current_slot_name: str='', working_slot_name: str=''):
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
        object.__setattr__(self, 'tx_group_key', tx_group_key)
        if not isinstance(value_slot_name, str):
            raise TypeError('ValueSlotName must be str, got ' + type(value_slot_name).__name__)
        object.__setattr__(self, 'value_slot_name', value_slot_name)
        if not isinstance(current_slot_name, str):
            raise TypeError('CurrentSlotName must be str, got ' + type(current_slot_name).__name__)
        object.__setattr__(self, 'current_slot_name', current_slot_name)
        if not isinstance(working_slot_name, str):
            raise TypeError('WorkingSlotName must be str, got ' + type(working_slot_name).__name__)
        object.__setattr__(self, 'working_slot_name', working_slot_name)

    def __setattr__(self, name, value):
        if name in ('field_id', 'field_owner', 'field_name', 'field_order', 'field_kind', 'annotation', 'init', 'has_default', 'default_value', 'default_value_param_name', 'has_default_factory', 'default_factory', 'default_factory_param_name', 'default_factory_param_names', 'tx_group_key', 'value_slot_name', 'current_slot_name', 'working_slot_name'):
            raise AttributeError('PlainField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('field_id=' + repr(self.field_id))
        pieces.append('field_owner=' + repr(self.field_owner))
        pieces.append('field_name=' + repr(self.field_name))
        pieces.append('field_order=' + repr(self.field_order))
        pieces.append('field_kind=' + repr(self.field_kind))
        pieces.append('annotation=' + repr(self.annotation))
        pieces.append('init=' + repr(self.init))
        pieces.append('has_default=' + repr(self.has_default))
        pieces.append('default_value=' + repr(self.default_value))
        pieces.append('default_value_param_name=' + repr(self.default_value_param_name))
        pieces.append('has_default_factory=' + repr(self.has_default_factory))
        pieces.append('default_factory=' + repr(self.default_factory))
        pieces.append('default_factory_param_name=' + repr(self.default_factory_param_name))
        pieces.append('default_factory_param_names=' + repr(self.default_factory_param_names))
        pieces.append('tx_group_key=' + repr(self.tx_group_key))
        pieces.append('value_slot_name=' + repr(self.value_slot_name))
        pieces.append('current_slot_name=' + repr(self.current_slot_name))
        pieces.append('working_slot_name=' + repr(self.working_slot_name))
        return 'PlainField' + '(' + ', '.join(pieces) + ')'
_PlainFieldSpec.bind_record_class(PlainField)

class InitVarField:
    __slots__ = ('field_id', 'field_owner', 'field_name', 'field_order', 'field_kind', 'annotation', 'init', 'has_default', 'default_value', 'default_value_param_name', 'has_default_factory', 'default_factory', 'default_factory_param_name', 'default_factory_param_names', 'tx_group_key', 'value_slot_name', 'current_slot_name', 'working_slot_name')
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

    def __init__(self, *, field_id: str, field_owner: str, field_name: str, field_order: int, field_kind: str='field', annotation: object=object, init: bool=True, has_default: bool=False, default_value: object=None, default_value_param_name: str='', has_default_factory: bool=False, default_factory: object=None, default_factory_param_name: str='', default_factory_param_names: object=(), tx_group_key: object=None, value_slot_name: str='', current_slot_name: str='', working_slot_name: str=''):
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
        object.__setattr__(self, 'tx_group_key', tx_group_key)
        if not isinstance(value_slot_name, str):
            raise TypeError('ValueSlotName must be str, got ' + type(value_slot_name).__name__)
        object.__setattr__(self, 'value_slot_name', value_slot_name)
        if not isinstance(current_slot_name, str):
            raise TypeError('CurrentSlotName must be str, got ' + type(current_slot_name).__name__)
        object.__setattr__(self, 'current_slot_name', current_slot_name)
        if not isinstance(working_slot_name, str):
            raise TypeError('WorkingSlotName must be str, got ' + type(working_slot_name).__name__)
        object.__setattr__(self, 'working_slot_name', working_slot_name)

    def __setattr__(self, name, value):
        if name in ('field_id', 'field_owner', 'field_name', 'field_order', 'field_kind', 'annotation', 'init', 'has_default', 'default_value', 'default_value_param_name', 'has_default_factory', 'default_factory', 'default_factory_param_name', 'default_factory_param_names', 'tx_group_key', 'value_slot_name', 'current_slot_name', 'working_slot_name'):
            raise AttributeError('InitVarField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('field_id=' + repr(self.field_id))
        pieces.append('field_owner=' + repr(self.field_owner))
        pieces.append('field_name=' + repr(self.field_name))
        pieces.append('field_order=' + repr(self.field_order))
        pieces.append('field_kind=' + repr(self.field_kind))
        pieces.append('annotation=' + repr(self.annotation))
        pieces.append('init=' + repr(self.init))
        pieces.append('has_default=' + repr(self.has_default))
        pieces.append('default_value=' + repr(self.default_value))
        pieces.append('default_value_param_name=' + repr(self.default_value_param_name))
        pieces.append('has_default_factory=' + repr(self.has_default_factory))
        pieces.append('default_factory=' + repr(self.default_factory))
        pieces.append('default_factory_param_name=' + repr(self.default_factory_param_name))
        pieces.append('default_factory_param_names=' + repr(self.default_factory_param_names))
        pieces.append('tx_group_key=' + repr(self.tx_group_key))
        pieces.append('value_slot_name=' + repr(self.value_slot_name))
        pieces.append('current_slot_name=' + repr(self.current_slot_name))
        pieces.append('working_slot_name=' + repr(self.working_slot_name))
        return 'InitVarField' + '(' + ', '.join(pieces) + ')'
_InitVarFieldSpec.bind_record_class(InitVarField)

class ClassVarField:
    __slots__ = ('field_id', 'field_owner', 'field_name', 'field_order', 'field_kind', 'annotation', 'init', 'has_default', 'default_value', 'default_value_param_name', 'has_default_factory', 'default_factory', 'default_factory_param_name', 'default_factory_param_names', 'tx_group_key', 'value_slot_name', 'current_slot_name', 'working_slot_name')
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

    def __init__(self, *, field_id: str, field_owner: str, field_name: str, field_order: int, field_kind: str='field', annotation: object=object, init: bool=True, has_default: bool=False, default_value: object=None, default_value_param_name: str='', has_default_factory: bool=False, default_factory: object=None, default_factory_param_name: str='', default_factory_param_names: object=(), tx_group_key: object=None, value_slot_name: str='', current_slot_name: str='', working_slot_name: str=''):
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
        object.__setattr__(self, 'tx_group_key', tx_group_key)
        if not isinstance(value_slot_name, str):
            raise TypeError('ValueSlotName must be str, got ' + type(value_slot_name).__name__)
        object.__setattr__(self, 'value_slot_name', value_slot_name)
        if not isinstance(current_slot_name, str):
            raise TypeError('CurrentSlotName must be str, got ' + type(current_slot_name).__name__)
        object.__setattr__(self, 'current_slot_name', current_slot_name)
        if not isinstance(working_slot_name, str):
            raise TypeError('WorkingSlotName must be str, got ' + type(working_slot_name).__name__)
        object.__setattr__(self, 'working_slot_name', working_slot_name)

    def __setattr__(self, name, value):
        if name in ('field_id', 'field_owner', 'field_name', 'field_order', 'field_kind', 'annotation', 'init', 'has_default', 'default_value', 'default_value_param_name', 'has_default_factory', 'default_factory', 'default_factory_param_name', 'default_factory_param_names', 'tx_group_key', 'value_slot_name', 'current_slot_name', 'working_slot_name'):
            raise AttributeError('ClassVarField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('field_id=' + repr(self.field_id))
        pieces.append('field_owner=' + repr(self.field_owner))
        pieces.append('field_name=' + repr(self.field_name))
        pieces.append('field_order=' + repr(self.field_order))
        pieces.append('field_kind=' + repr(self.field_kind))
        pieces.append('annotation=' + repr(self.annotation))
        pieces.append('init=' + repr(self.init))
        pieces.append('has_default=' + repr(self.has_default))
        pieces.append('default_value=' + repr(self.default_value))
        pieces.append('default_value_param_name=' + repr(self.default_value_param_name))
        pieces.append('has_default_factory=' + repr(self.has_default_factory))
        pieces.append('default_factory=' + repr(self.default_factory))
        pieces.append('default_factory_param_name=' + repr(self.default_factory_param_name))
        pieces.append('default_factory_param_names=' + repr(self.default_factory_param_names))
        pieces.append('tx_group_key=' + repr(self.tx_group_key))
        pieces.append('value_slot_name=' + repr(self.value_slot_name))
        pieces.append('current_slot_name=' + repr(self.current_slot_name))
        pieces.append('working_slot_name=' + repr(self.working_slot_name))
        return 'ClassVarField' + '(' + ', '.join(pieces) + ')'
_ClassVarFieldSpec.bind_record_class(ClassVarField)
ClassesCollection = RuntimeCollection('Classes', _LifecycleClassSpec, allows_multiple=True, identity=_ClassIdProperty)
FieldsCollection = RuntimeCollection('Fields', _LifecycleFieldSpecUnion, allows_multiple=True, identity=_FieldIdProperty)
TransactionMethodsCollection = RuntimeCollection('TransactionMethods', _TransactionMethodSpec, allows_multiple=True, identity=_MethodIdProperty)
FacadeClassesCollection = RuntimeCollection('FacadeClasses', _FacadeClassSpec, allows_multiple=True, identity=(_FacadeOwnerProperty, _FacadeIdProperty))
FacadeExposuresCollection = RuntimeCollection('FacadeExposures', _FacadeExposureSpec, allows_multiple=True, identity=(_FacadeOwnerProperty, _OwnerFacadeIdProperty, _FieldNameProperty))
InitParametersCollection = RuntimeCollection('InitParameters', _InitParameterSpec, allows_multiple=True, identity=_InitParameterIdProperty)
InitAssignmentsCollection = RuntimeCollection('InitAssignments', _InitAssignmentSpec, allows_multiple=True, identity=_InitAssignmentIdProperty)
ClassVarAssignmentsCollection = RuntimeCollection('ClassVarAssignments', _ClassVarAssignmentSpec, allows_multiple=True, identity=_ClassVarAssignmentIdProperty)
PlainFieldsCollection = RuntimeComputedCollection('PlainFields', source=FieldsCollection, when=(_FieldKindProperty.eq('field'),))
InitVarFieldsCollection = RuntimeComputedCollection('InitVarFields', source=FieldsCollection, when=(_FieldKindProperty.eq('initvar'),))
ClassVarFieldsCollection = RuntimeComputedCollection('ClassVarFields', source=FieldsCollection, when=(_FieldKindProperty.eq('classvar'),))
CommitOrderKeyProvidersCollection = RuntimeComputedCollection('CommitOrderKeyProviders', source=TransactionMethodsCollection, when=(_MethodKindProperty.eq('commit_order_key'),))
CommitValidatorsCollection = RuntimeComputedCollection('CommitValidators', source=TransactionMethodsCollection, when=(_MethodKindProperty.eq('validate_commit'),))
BeforeCommitHooksCollection = RuntimeComputedCollection('BeforeCommitHooks', source=TransactionMethodsCollection, when=(_MethodKindProperty.eq('before_commit'),))
AfterCommitHooksCollection = RuntimeComputedCollection('AfterCommitHooks', source=TransactionMethodsCollection, when=(_MethodKindProperty.eq('after_commit'),))
AfterRollbackHooksCollection = RuntimeComputedCollection('AfterRollbackHooks', source=TransactionMethodsCollection, when=(_MethodKindProperty.eq('after_rollback'),))
_RUNTIME_SPEC = RuntimeContainerSpec(collections=(ClassesCollection, FieldsCollection, TransactionMethodsCollection, FacadeClassesCollection, FacadeExposuresCollection, InitParametersCollection, InitAssignmentsCollection, ClassVarAssignmentsCollection), computed_collections=(PlainFieldsCollection, InitVarFieldsCollection, ClassVarFieldsCollection, CommitOrderKeyProvidersCollection, CommitValidatorsCollection, BeforeCommitHooksCollection, AfterCommitHooksCollection, AfterRollbackHooksCollection), ports=(), port_index=None)

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

ASSEMBLY_PROPERTIES = {'ClassId': _YidlSimpleNamespace(name='ClassId', storage_name='class_id'), 'ClassName': _YidlSimpleNamespace(name='ClassName', storage_name='class_name'), 'ClassOrder': _YidlSimpleNamespace(name='ClassOrder', storage_name='class_order'), 'ModuleName': _YidlSimpleNamespace(name='ModuleName', storage_name='module_name'), 'StateClassName': _YidlSimpleNamespace(name='StateClassName', storage_name='state_class_name'), 'FacadeBaseClassName': _YidlSimpleNamespace(name='FacadeBaseClassName', storage_name='facade_base_class_name'), 'CurrentFacadeClassName': _YidlSimpleNamespace(name='CurrentFacadeClassName', storage_name='current_facade_class_name'), 'WorkingFacadeClassName': _YidlSimpleNamespace(name='WorkingFacadeClassName', storage_name='working_facade_class_name'), 'LifecycleDefinitionParamName': _YidlSimpleNamespace(name='LifecycleDefinitionParamName', storage_name='lifecycle_definition_param_name'), 'AnnotationsParamName': _YidlSimpleNamespace(name='AnnotationsParamName', storage_name='annotations_param_name'), 'TxGroupsParamName': _YidlSimpleNamespace(name='TxGroupsParamName', storage_name='tx_groups_param_name'), 'LifecycleFieldNames': _YidlSimpleNamespace(name='LifecycleFieldNames', storage_name='lifecycle_field_names'), 'FieldId': _YidlSimpleNamespace(name='FieldId', storage_name='field_id'), 'FieldOwner': _YidlSimpleNamespace(name='FieldOwner', storage_name='field_owner'), 'FieldName': _YidlSimpleNamespace(name='FieldName', storage_name='field_name'), 'FieldOrder': _YidlSimpleNamespace(name='FieldOrder', storage_name='field_order'), 'FieldKind': _YidlSimpleNamespace(name='FieldKind', storage_name='field_kind'), 'Annotation': _YidlSimpleNamespace(name='Annotation', storage_name='annotation'), 'Init': _YidlSimpleNamespace(name='Init', storage_name='init'), 'HasDefault': _YidlSimpleNamespace(name='HasDefault', storage_name='has_default'), 'DefaultValue': _YidlSimpleNamespace(name='DefaultValue', storage_name='default_value'), 'DefaultValueParamName': _YidlSimpleNamespace(name='DefaultValueParamName', storage_name='default_value_param_name'), 'HasDefaultFactory': _YidlSimpleNamespace(name='HasDefaultFactory', storage_name='has_default_factory'), 'DefaultFactory': _YidlSimpleNamespace(name='DefaultFactory', storage_name='default_factory'), 'DefaultFactoryParamName': _YidlSimpleNamespace(name='DefaultFactoryParamName', storage_name='default_factory_param_name'), 'DefaultFactoryParamNames': _YidlSimpleNamespace(name='DefaultFactoryParamNames', storage_name='default_factory_param_names'), 'TxGroupKey': _YidlSimpleNamespace(name='TxGroupKey', storage_name='tx_group_key'), 'ValueSlotName': _YidlSimpleNamespace(name='ValueSlotName', storage_name='value_slot_name'), 'CurrentSlotName': _YidlSimpleNamespace(name='CurrentSlotName', storage_name='current_slot_name'), 'WorkingSlotName': _YidlSimpleNamespace(name='WorkingSlotName', storage_name='working_slot_name'), 'MethodId': _YidlSimpleNamespace(name='MethodId', storage_name='method_id'), 'MethodOwner': _YidlSimpleNamespace(name='MethodOwner', storage_name='method_owner'), 'MethodName': _YidlSimpleNamespace(name='MethodName', storage_name='method_name'), 'MethodKind': _YidlSimpleNamespace(name='MethodKind', storage_name='method_kind'), 'DeclarationOrder': _YidlSimpleNamespace(name='DeclarationOrder', storage_name='declaration_order'), 'FacadeId': _YidlSimpleNamespace(name='FacadeId', storage_name='facade_id'), 'FacadeOwner': _YidlSimpleNamespace(name='FacadeOwner', storage_name='facade_owner'), 'FacadeKind': _YidlSimpleNamespace(name='FacadeKind', storage_name='facade_kind'), 'FacadeMode': _YidlSimpleNamespace(name='FacadeMode', storage_name='facade_mode'), 'FacadeClassName': _YidlSimpleNamespace(name='FacadeClassName', storage_name='facade_class_name'), 'FacadeOrder': _YidlSimpleNamespace(name='FacadeOrder', storage_name='facade_order'), 'OwnerFacadeId': _YidlSimpleNamespace(name='OwnerFacadeId', storage_name='owner_facade_id'), 'TargetFacadeId': _YidlSimpleNamespace(name='TargetFacadeId', storage_name='target_facade_id'), 'ExposureOrder': _YidlSimpleNamespace(name='ExposureOrder', storage_name='exposure_order'), 'InitParameterId': _YidlSimpleNamespace(name='InitParameterId', storage_name='init_parameter_id'), 'InitParameterOwner': _YidlSimpleNamespace(name='InitParameterOwner', storage_name='init_parameter_owner'), 'InitParameterName': _YidlSimpleNamespace(name='InitParameterName', storage_name='init_parameter_name'), 'InitParameterOrder': _YidlSimpleNamespace(name='InitParameterOrder', storage_name='init_parameter_order'), 'InitParameterKind': _YidlSimpleNamespace(name='InitParameterKind', storage_name='init_parameter_kind'), 'InitAssignmentId': _YidlSimpleNamespace(name='InitAssignmentId', storage_name='init_assignment_id'), 'InitAssignmentOwner': _YidlSimpleNamespace(name='InitAssignmentOwner', storage_name='init_assignment_owner'), 'InitAssignmentFieldId': _YidlSimpleNamespace(name='InitAssignmentFieldId', storage_name='init_assignment_field_id'), 'InitAssignmentFieldName': _YidlSimpleNamespace(name='InitAssignmentFieldName', storage_name='init_assignment_field_name'), 'InitAssignmentOrder': _YidlSimpleNamespace(name='InitAssignmentOrder', storage_name='init_assignment_order'), 'InitAssignmentKind': _YidlSimpleNamespace(name='InitAssignmentKind', storage_name='init_assignment_kind'), 'ClassVarAssignmentId': _YidlSimpleNamespace(name='ClassVarAssignmentId', storage_name='class_var_assignment_id'), 'ClassVarAssignmentOwner': _YidlSimpleNamespace(name='ClassVarAssignmentOwner', storage_name='class_var_assignment_owner'), 'ClassVarAssignmentName': _YidlSimpleNamespace(name='ClassVarAssignmentName', storage_name='class_var_assignment_name'), 'ClassVarAssignmentOrder': _YidlSimpleNamespace(name='ClassVarAssignmentOrder', storage_name='class_var_assignment_order')}
ASSEMBLY_RESOURCES = {'ModuleRoot': from_astichi_code("""\
from __future__ import annotations

import weakref

from yidl.runtime.lifecycle import _HAS_DEFAULT_FACTORY
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION
from yidl.runtime.transaction_yidl import TransactionManager


VOID = object()


def build_lifecycle_class(decorated_cls, builder_params__astichi_param_hole__):
    astichi_hole(function_body)
    astichi_hole(return_statement)""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=192), 'BuilderParam': astichi_template(from_astichi_code("""\
def astichi_params(*, value_name__astichi_arg__):
    pass""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=210)), 'TransactionManagerParam': astichi_template(from_astichi_code("""\
def astichi_params(*, transaction_manager=None):
    pass""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=215)), 'StateSlotEntry': astichi_template(from_astichi_code('astichi_bind_external(slot_name)', file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=220)), 'InitParamRequired': astichi_template(from_astichi_code("""\
def astichi_params(param_name__astichi_arg__: astichi_bind_external(annotation)):
    pass""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=224)), 'InitParamDefault': astichi_template(from_astichi_code("""\
def astichi_params(
    param_name__astichi_arg__: astichi_bind_external(annotation)
    = default_value_name__astichi_arg__
):
    pass""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=229)), 'PlainStateAssignment': astichi_template(from_astichi_code("""\
astichi_pass(state, outer_bind=True).astichi_ref(external=state_slot)._ = astichi_pass(
    init_value_name__astichi_arg__,
    outer_bind=True,
)""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=237)), 'InitVarLocalDefaultAssignment': astichi_template(from_astichi_code("""\
init_value_name__astichi_arg__ = astichi_pass(
    default_value_name__astichi_arg__,
    outer_bind=True,
)""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=244)), 'PlainProperty': astichi_template(from_astichi_code("""\
@property
def property_getter_name__astichi_arg__(self):
    return self._y_state.astichi_ref(external=state_slot)

@property_setter_target_name__astichi_arg__.setter
def property_setter_name__astichi_arg__(self, value):
    self._y_state.astichi_ref(external=state_slot)._ = value""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=251)), 'ClassVarDefaultAssignment': astichi_template(from_astichi_code("""\
classvar_name__astichi_arg__ = astichi_pass(
    classvar_value_name__astichi_arg__,
    outer_bind=True,
)""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=261)), 'CommitOrderKeyBranch': astichi_template(from_astichi_code("""\
if astichi_pass(tx_group, outer_bind=True) == astichi_bind_external(tx_group_key):
    return astichi_pass(
        self,
        outer_bind=True,
    )._y_get_default_facade().astichi_ref(external=method_name)()""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=268)), 'RequiresValidationBranch': astichi_template(from_astichi_code("""\
if astichi_pass(tx_group, outer_bind=True) == astichi_bind_external(tx_group_key):
    return True""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=276)), 'ValidateCommitBranch': astichi_template(from_astichi_code("""\
if astichi_pass(tx_group, outer_bind=True) == astichi_bind_external(tx_group_key):
    result = astichi_pass(
        self,
        outer_bind=True,
    )._y_get_default_facade().astichi_ref(external=method_name)()
    if result is False:
        return False""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=281)), 'TransactionHookCall': astichi_template(from_astichi_code("""\
if astichi_pass(tx_group, outer_bind=True) == astichi_bind_external(tx_group_key):
    astichi_pass(
        self,
        outer_bind=True,
    )._y_get_default_facade().astichi_ref(external=method_name)()""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=291)), 'ClassBundle': astichi_template(from_astichi_code("""\
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
            self._y_default_ref = weakref.ref(facade)
        return facade

    def _y_get_current_facade(self):
        ref = self._y_current_ref
        facade = None if ref is None else ref()
        if facade is None:
            facade = object.__new__(current_facade_class_ref__astichi_arg__)
            object.__setattr__(facade, "_y_state", self)
            self._y_current_ref = weakref.ref(facade)
        return facade

    def _y_get_working_facade(self):
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
        astichi_hole(commit_order_key_body)
        return ()

    def requires_validation_for(self, tx_group=DEFAULT_TRANSACTION):
        astichi_hole(requires_validation_body)
        return False

    def validate_commit_for(self, tx_group=DEFAULT_TRANSACTION):
        astichi_hole(validate_commit_body)
        return True

    def _commit_transaction(self, tx_id, tx_group=DEFAULT_TRANSACTION):
        tx_index = self.__yidl_tx_group_to_index__[tx_group]
        if self._y_working_tx_ids[tx_index] != tx_id:
            return self._y_get_default_facade()
        astichi_hole(before_commit_body)
        astichi_hole(commit_transaction_body)
        self._y_working_tx_ids[tx_index] = None
        astichi_hole(after_commit_body)
        return self._y_get_default_facade()

    def _rollback_transaction(self, tx_id, tx_group=DEFAULT_TRANSACTION):
        tx_index = self.__yidl_tx_group_to_index__[tx_group]
        if self._y_working_tx_ids[tx_index] != tx_id:
            return self._y_get_default_facade()
        astichi_hole(rollback_transaction_body)
        self._y_working_tx_ids[tx_index] = None
        astichi_hole(after_rollback_body)
        return self._y_get_default_facade()


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
    __slots__ = ()
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
    astichi_hole(working_facade_properties)""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=299, keep_names=('DEFAULT_TRANSACTION', 'TransactionManager', 'VOID', 'weakref', '_HAS_DEFAULT_FACTORY'))), 'ReturnClass': astichi_template(from_astichi_code("""\
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
return return_class_result_ref__astichi_arg__""", file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=540)), 'PassStatement': astichi_template(from_astichi_code('pass', file_name='tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl', line_number=556))}
ASSEMBLY_CONTRIBUTIONS = {'LifecycleDefinitionBuilderParam': ContributionSpec(name='LifecycleDefinitionBuilderParam', source_name='BuilderParam', source_kind='resource', build_name='LifecycleDefinitionBuilderParam', index=ValueRef('ClassOrder'), order=ValueRef('ClassOrder'), target=TargetSpec(name='builder_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='Root', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='value_name', value=ValueRef('LifecycleDefinitionParamName')),)), 'AnnotationsBuilderParam': ContributionSpec(name='AnnotationsBuilderParam', source_name='BuilderParam', source_kind='resource', build_name='AnnotationsBuilderParam', index=ValueRef('ClassOrder'), order=ValueRef('ClassOrder'), target=TargetSpec(name='builder_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='Root', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='value_name', value=ValueRef('AnnotationsParamName')),)), 'TxGroupsBuilderParam': ContributionSpec(name='TxGroupsBuilderParam', source_name='BuilderParam', source_kind='resource', build_name='TxGroupsBuilderParam', index=ValueRef('ClassOrder'), order=ValueRef('ClassOrder'), target=TargetSpec(name='builder_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='Root', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='value_name', value=ValueRef('TxGroupsParamName')),)), 'FieldDefaultBuilderParam': ContributionSpec(name='FieldDefaultBuilderParam', source_name='BuilderParam', source_kind='resource', build_name='FieldDefaultBuilderParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='builder_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='Root', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='value_name', value=ValueRef('DefaultValueParamName')),)), 'FacadeBaseBodyPass': ContributionSpec(name='FacadeBaseBodyPass', source_name='PassStatement', source_kind='resource', build_name='FacadeBaseBodyPass', index=LiteralValueRef(0), order=LiteralValueRef(0), target=TargetSpec(name='facade_base_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=()), 'FacadePropertiesPass': ContributionSpec(name='FacadePropertiesPass', source_name='PassStatement', source_kind='resource', build_name='FacadePropertiesPass', index=LiteralValueRef(0), order=LiteralValueRef(0), target=TargetSpec(name='facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=()), 'DefaultFacadePropertiesPass': ContributionSpec(name='DefaultFacadePropertiesPass', source_name='PassStatement', source_kind='resource', build_name='DefaultFacadePropertiesPass', index=LiteralValueRef(0), order=LiteralValueRef(0), target=TargetSpec(name='default_facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=()), 'CurrentFacadePropertiesPass': ContributionSpec(name='CurrentFacadePropertiesPass', source_name='PassStatement', source_kind='resource', build_name='CurrentFacadePropertiesPass', index=LiteralValueRef(0), order=LiteralValueRef(0), target=TargetSpec(name='current_facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=()), 'WorkingFacadePropertiesPass': ContributionSpec(name='WorkingFacadePropertiesPass', source_name='PassStatement', source_kind='resource', build_name='WorkingFacadePropertiesPass', index=LiteralValueRef(0), order=LiteralValueRef(0), target=TargetSpec(name='working_facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=()), 'StateInitBodyPass': ContributionSpec(name='StateInitBodyPass', source_name='PassStatement', source_kind='resource', build_name='StateInitBodyPass', index=LiteralValueRef(0), order=LiteralValueRef(0), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=()), 'CommitTransactionBodyPass': ContributionSpec(name='CommitTransactionBodyPass', source_name='PassStatement', source_kind='resource', build_name='CommitTransactionBodyPass', index=LiteralValueRef(0), order=LiteralValueRef(0), target=TargetSpec(name='commit_transaction_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=()), 'RollbackTransactionBodyPass': ContributionSpec(name='RollbackTransactionBodyPass', source_name='PassStatement', source_kind='resource', build_name='RollbackTransactionBodyPass', index=LiteralValueRef(0), order=LiteralValueRef(0), target=TargetSpec(name='rollback_transaction_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=()), 'CommitOrderKeyBodyPass': ContributionSpec(name='CommitOrderKeyBodyPass', source_name='PassStatement', source_kind='resource', build_name='CommitOrderKeyBodyPass', index=LiteralValueRef(0), order=LiteralValueRef(0), target=TargetSpec(name='commit_order_key_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=()), 'RequiresValidationBodyPass': ContributionSpec(name='RequiresValidationBodyPass', source_name='PassStatement', source_kind='resource', build_name='RequiresValidationBodyPass', index=LiteralValueRef(0), order=LiteralValueRef(0), target=TargetSpec(name='requires_validation_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=()), 'ValidateCommitBodyPass': ContributionSpec(name='ValidateCommitBodyPass', source_name='PassStatement', source_kind='resource', build_name='ValidateCommitBodyPass', index=LiteralValueRef(0), order=LiteralValueRef(0), target=TargetSpec(name='validate_commit_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=()), 'BeforeCommitBodyPass': ContributionSpec(name='BeforeCommitBodyPass', source_name='PassStatement', source_kind='resource', build_name='BeforeCommitBodyPass', index=LiteralValueRef(0), order=LiteralValueRef(0), target=TargetSpec(name='before_commit_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=()), 'AfterCommitBodyPass': ContributionSpec(name='AfterCommitBodyPass', source_name='PassStatement', source_kind='resource', build_name='AfterCommitBodyPass', index=LiteralValueRef(0), order=LiteralValueRef(0), target=TargetSpec(name='after_commit_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=()), 'AfterRollbackBodyPass': ContributionSpec(name='AfterRollbackBodyPass', source_name='PassStatement', source_kind='resource', build_name='AfterRollbackBodyPass', index=LiteralValueRef(0), order=LiteralValueRef(0), target=TargetSpec(name='after_rollback_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=()), 'ReturnClassContribution': ContributionSpec(name='ReturnClassContribution', source_name='ReturnClass', source_kind='resource', build_name='ReturnClass', index=ValueRef('ClassOrder'), order=ValueRef('ClassOrder'), target=TargetSpec(name='return_statement', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='Root', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='return_class_name_ref', value=ValueRef('ClassName')), BindingSpec(kind='ident', name='return_class_qualname_ref', value=ValueRef('ClassName')), BindingSpec(kind='ident', name='return_class_module_ref', value=ValueRef('ClassName')), BindingSpec(kind='ident', name='return_class_result_ref', value=ValueRef('ClassName')))), 'TransactionManagerInitParam': ContributionSpec(name='TransactionManagerInitParam', source_name='TransactionManagerParam', source_kind='resource', build_name='TransactionManagerInitParam', index=ValueRef('ClassOrder'), order=LiteralValueRef(0), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=()), 'PlainStateSlot': ContributionSpec(name='PlainStateSlot', source_name='StateSlotEntry', source_kind='resource', build_name='PlainStateSlot', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_slots', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='slot_name', value=ValueRef('ValueSlotName')),)), 'PlainInitParamRequired': ContributionSpec(name='PlainInitParamRequired', source_name='InitParamRequired', source_kind='resource', build_name='PlainInitParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')))), 'PlainInitParamDefault': ContributionSpec(name='PlainInitParamDefault', source_name='InitParamDefault', source_kind='resource', build_name='PlainInitParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')), BindingSpec(kind='ident', name='default_value_name', value=ValueRef('DefaultValueParamName')))), 'InitVarParamRequired': ContributionSpec(name='InitVarParamRequired', source_name='InitParamRequired', source_kind='resource', build_name='InitVarParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')))), 'InitVarParamDefault': ContributionSpec(name='InitVarParamDefault', source_name='InitParamDefault', source_kind='resource', build_name='InitVarParam', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='init_params', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='param_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='annotation', value=ValueRef('Annotation')), BindingSpec(kind='ident', name='default_value_name', value=ValueRef('DefaultValueParamName')))), 'InitVarLocalDefault': ContributionSpec(name='InitVarLocalDefault', source_name='InitVarLocalDefaultAssignment', source_kind='resource', build_name='InitVarLocalDefault', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='init_value_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='default_value_name', value=ValueRef('DefaultValueParamName')))), 'PlainInitAssignment': ContributionSpec(name='PlainInitAssignment', source_name='PlainStateAssignment', source_kind='resource', build_name='PlainInitAssignment', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='init_value_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('ValueSlotName')))), 'PlainDefaultAssignment': ContributionSpec(name='PlainDefaultAssignment', source_name='PlainStateAssignment', source_kind='resource', build_name='PlainDefaultAssignment', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='state_init_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='init_value_name', value=ValueRef('DefaultValueParamName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('ValueSlotName')))), 'PlainFieldProperty': ContributionSpec(name='PlainFieldProperty', source_name='PlainProperty', source_kind='resource', build_name='PlainFieldProperty', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='facade_properties', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='property_getter_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_target_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='property_setter_name', value=ValueRef('FieldName')), BindingSpec(kind='external', name='state_slot', value=ValueRef('ValueSlotName')))), 'ClassVarDefault': ContributionSpec(name='ClassVarDefault', source_name='ClassVarDefaultAssignment', source_kind='resource', build_name='ClassVarDefault', index=ValueRef('FieldOrder'), order=ValueRef('FieldOrder'), target=TargetSpec(name='facade_base_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='ident', name='classvar_name', value=ValueRef('FieldName')), BindingSpec(kind='ident', name='classvar_value_name', value=ValueRef('DefaultValueParamName')))), 'CommitOrderKeyBranchContribution': ContributionSpec(name='CommitOrderKeyBranchContribution', source_name='CommitOrderKeyBranch', source_kind='resource', build_name='CommitOrderKeyBranch', index=ValueRef('DeclarationOrder'), order=ValueRef('DeclarationOrder'), target=TargetSpec(name='commit_order_key_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='method_name', value=ValueRef('MethodName')), BindingSpec(kind='external', name='tx_group_key', value=ValueRef('TxGroupKey')))), 'RequiresValidationBranchContribution': ContributionSpec(name='RequiresValidationBranchContribution', source_name='RequiresValidationBranch', source_kind='resource', build_name='RequiresValidationBranch', index=ValueRef('DeclarationOrder'), order=ValueRef('DeclarationOrder'), target=TargetSpec(name='requires_validation_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='tx_group_key', value=ValueRef('TxGroupKey')),)), 'ValidateCommitBranchContribution': ContributionSpec(name='ValidateCommitBranchContribution', source_name='ValidateCommitBranch', source_kind='resource', build_name='ValidateCommitBranch', index=ValueRef('DeclarationOrder'), order=ValueRef('DeclarationOrder'), target=TargetSpec(name='validate_commit_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='method_name', value=ValueRef('MethodName')), BindingSpec(kind='external', name='tx_group_key', value=ValueRef('TxGroupKey')))), 'BeforeCommitHookContribution': ContributionSpec(name='BeforeCommitHookContribution', source_name='TransactionHookCall', source_kind='resource', build_name='BeforeCommitHook', index=ValueRef('DeclarationOrder'), order=ValueRef('DeclarationOrder'), target=TargetSpec(name='before_commit_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='method_name', value=ValueRef('MethodName')), BindingSpec(kind='external', name='tx_group_key', value=ValueRef('TxGroupKey')))), 'AfterCommitHookContribution': ContributionSpec(name='AfterCommitHookContribution', source_name='TransactionHookCall', source_kind='resource', build_name='AfterCommitHook', index=ValueRef('DeclarationOrder'), order=ValueRef('DeclarationOrder'), target=TargetSpec(name='after_commit_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='method_name', value=ValueRef('MethodName')), BindingSpec(kind='external', name='tx_group_key', value=ValueRef('TxGroupKey')))), 'AfterRollbackHookContribution': ContributionSpec(name='AfterRollbackHookContribution', source_name='TransactionHookCall', source_kind='resource', build_name='AfterRollbackHook', index=ValueRef('DeclarationOrder'), order=ValueRef('DeclarationOrder'), target=TargetSpec(name='after_rollback_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='ClassDef', indexes=()),))),)), bindings=(BindingSpec(kind='external', name='method_name', value=ValueRef('MethodName')), BindingSpec(kind='external', name='tx_group_key', value=ValueRef('TxGroupKey')))), 'CoreClassDefinition': ContributionSpec(name='CoreClassDefinition', source_name='CoreClassProduction', source_kind='production', build_name='ClassDef', index=ValueRef('ClassOrder'), order=ValueRef('ClassOrder'), target=TargetSpec(name='function_body', paths=(TargetPathSpec(kind='build', path=PathSpec(segments=(PathSegmentSpec(kind='name', name='Root', indexes=()),))),)), bindings=())}
ASSEMBLY_MATCHERS = {'BuilderParamContributions': ContributionMatcherSpec(name='BuilderParamContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='LifecycleDefinitionBuilderParam', rules=()), 'AnnotationsBuilderParamContributions': ContributionMatcherSpec(name='AnnotationsBuilderParamContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='AnnotationsBuilderParam', rules=()), 'TxGroupsBuilderParamContributions': ContributionMatcherSpec(name='TxGroupsBuilderParamContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='TxGroupsBuilderParam', rules=()), 'ReturnClassContributions': ContributionMatcherSpec(name='ReturnClassContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='ReturnClassContribution', rules=()), 'TransactionManagerInitParamContributions': ContributionMatcherSpec(name='TransactionManagerInitParamContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='TransactionManagerInitParam', rules=()), 'FacadeBaseBodyPassContributions': ContributionMatcherSpec(name='FacadeBaseBodyPassContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='FacadeBaseBodyPass', rules=()), 'FacadePropertiesPassContributions': ContributionMatcherSpec(name='FacadePropertiesPassContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='FacadePropertiesPass', rules=()), 'DefaultFacadePropertiesPassContributions': ContributionMatcherSpec(name='DefaultFacadePropertiesPassContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='DefaultFacadePropertiesPass', rules=()), 'CurrentFacadePropertiesPassContributions': ContributionMatcherSpec(name='CurrentFacadePropertiesPassContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='CurrentFacadePropertiesPass', rules=()), 'WorkingFacadePropertiesPassContributions': ContributionMatcherSpec(name='WorkingFacadePropertiesPassContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='WorkingFacadePropertiesPass', rules=()), 'StateInitBodyPassContributions': ContributionMatcherSpec(name='StateInitBodyPassContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='StateInitBodyPass', rules=()), 'CommitTransactionBodyPassContributions': ContributionMatcherSpec(name='CommitTransactionBodyPassContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='CommitTransactionBodyPass', rules=()), 'RollbackTransactionBodyPassContributions': ContributionMatcherSpec(name='RollbackTransactionBodyPassContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='RollbackTransactionBodyPass', rules=()), 'CommitOrderKeyBodyPassContributions': ContributionMatcherSpec(name='CommitOrderKeyBodyPassContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='CommitOrderKeyBodyPass', rules=()), 'RequiresValidationBodyPassContributions': ContributionMatcherSpec(name='RequiresValidationBodyPassContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='RequiresValidationBodyPass', rules=()), 'ValidateCommitBodyPassContributions': ContributionMatcherSpec(name='ValidateCommitBodyPassContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='ValidateCommitBodyPass', rules=()), 'BeforeCommitBodyPassContributions': ContributionMatcherSpec(name='BeforeCommitBodyPassContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='BeforeCommitBodyPass', rules=()), 'AfterCommitBodyPassContributions': ContributionMatcherSpec(name='AfterCommitBodyPassContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='AfterCommitBodyPass', rules=()), 'AfterRollbackBodyPassContributions': ContributionMatcherSpec(name='AfterRollbackBodyPassContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='AfterRollbackBodyPass', rules=()), 'PlainStateSlotContributions': ContributionMatcherSpec(name='PlainStateSlotContributions', inputs=(AssemblyInputSpec(name='field', collection_name='PlainFields', collection=None),), default_contribution_name='PlainStateSlot', rules=()), 'InitVarLocalDefaultContributions': ContributionMatcherSpec(name='InitVarLocalDefaultContributions', inputs=(AssemblyInputSpec(name='field', collection_name='InitVarFields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='default_value', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(False)), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='InitVarLocalDefault', weight=1.0),)), 'PlainInitAssignmentContributions': ContributionMatcherSpec(name='PlainInitAssignmentContributions', inputs=(AssemblyInputSpec(name='field', collection_name='PlainFields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='init_field', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='PlainInitAssignment', weight=1.0), ContributionRuleSpec(name='default_value', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(False)), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='PlainDefaultAssignment', weight=1.0))), 'PlainPropertyContributions': ContributionMatcherSpec(name='PlainPropertyContributions', inputs=(AssemblyInputSpec(name='field', collection_name='PlainFields', collection=None),), default_contribution_name='PlainFieldProperty', rules=()), 'ClassVarDefaultContributions': ContributionMatcherSpec(name='ClassVarDefaultContributions', inputs=(AssemblyInputSpec(name='field', collection_name='ClassVarFields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='has_default', condition=EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(True)), contribution_name='ClassVarDefault', weight=1.0),)), 'CommitOrderKeyContributions': ContributionMatcherSpec(name='CommitOrderKeyContributions', inputs=(AssemblyInputSpec(name='method', collection_name='CommitOrderKeyProviders', collection=None),), default_contribution_name='CommitOrderKeyBranchContribution', rules=()), 'RequiresValidationContributions': ContributionMatcherSpec(name='RequiresValidationContributions', inputs=(AssemblyInputSpec(name='method', collection_name='CommitValidators', collection=None),), default_contribution_name='RequiresValidationBranchContribution', rules=()), 'ValidateCommitContributions': ContributionMatcherSpec(name='ValidateCommitContributions', inputs=(AssemblyInputSpec(name='method', collection_name='CommitValidators', collection=None),), default_contribution_name='ValidateCommitBranchContribution', rules=()), 'BeforeCommitHookContributions': ContributionMatcherSpec(name='BeforeCommitHookContributions', inputs=(AssemblyInputSpec(name='method', collection_name='BeforeCommitHooks', collection=None),), default_contribution_name='BeforeCommitHookContribution', rules=()), 'AfterCommitHookContributions': ContributionMatcherSpec(name='AfterCommitHookContributions', inputs=(AssemblyInputSpec(name='method', collection_name='AfterCommitHooks', collection=None),), default_contribution_name='AfterCommitHookContribution', rules=()), 'AfterRollbackHookContributions': ContributionMatcherSpec(name='AfterRollbackHookContributions', inputs=(AssemblyInputSpec(name='method', collection_name='AfterRollbackHooks', collection=None),), default_contribution_name='AfterRollbackHookContribution', rules=()), 'FieldDefaultBuilderParamContributions': ContributionMatcherSpec(name='FieldDefaultBuilderParamContributions', inputs=(AssemblyInputSpec(name='field', collection_name='Fields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='has_default', condition=EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(True)), contribution_name='FieldDefaultBuilderParam', weight=1.0),)), 'CoreClassDefinitionContributions': ContributionMatcherSpec(name='CoreClassDefinitionContributions', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), default_contribution_name='CoreClassDefinition', rules=()), 'PlainInitParamContributions': ContributionMatcherSpec(name='PlainInitParamContributions', inputs=(AssemblyInputSpec(name='field', collection_name='PlainFields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='required', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(False)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='PlainInitParamRequired', weight=1.0), ContributionRuleSpec(name='default_value', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='PlainInitParamDefault', weight=1.0))), 'InitVarParamContributions': ContributionMatcherSpec(name='InitVarParamContributions', inputs=(AssemblyInputSpec(name='field', collection_name='InitVarFields', collection=None),), default_contribution_name=None, rules=(ContributionRuleSpec(name='required', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(False)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='InitVarParamRequired', weight=1.0), ContributionRuleSpec(name='default_value', condition=AndConditionSpec(items=(EqConditionSpec(left=ValueRef('Init'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefault'), right=LiteralValueRef(True)), EqConditionSpec(left=ValueRef('HasDefaultFactory'), right=LiteralValueRef(False)))), contribution_name='InitVarParamDefault', weight=1.0)))}
ASSEMBLY_EDGES = {'CoreModuleProduction.lifecycle_definition_params': AssemblyEdgeSpec(name='CoreModuleProduction.lifecycle_definition_params', context_inputs=(), from_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), condition=None, matcher_name='BuilderParamContributions'), 'CoreModuleProduction.annotations_params': AssemblyEdgeSpec(name='CoreModuleProduction.annotations_params', context_inputs=(), from_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), condition=None, matcher_name='AnnotationsBuilderParamContributions'), 'CoreModuleProduction.tx_groups_params': AssemblyEdgeSpec(name='CoreModuleProduction.tx_groups_params', context_inputs=(), from_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), condition=None, matcher_name='TxGroupsBuilderParamContributions'), 'CoreModuleProduction.field_default_params': AssemblyEdgeSpec(name='CoreModuleProduction.field_default_params', context_inputs=(), from_inputs=(AssemblyInputSpec(name='field', collection_name='Fields', collection=None),), condition=None, matcher_name='FieldDefaultBuilderParamContributions'), 'CoreModuleProduction.classes': AssemblyEdgeSpec(name='CoreModuleProduction.classes', context_inputs=(), from_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), condition=None, matcher_name='CoreClassDefinitionContributions'), 'CoreModuleProduction.return_class': AssemblyEdgeSpec(name='CoreModuleProduction.return_class', context_inputs=(), from_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), condition=None, matcher_name='ReturnClassContributions'), 'CoreClassProduction.state_slots': AssemblyEdgeSpec(name='CoreClassProduction.state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='PlainFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='PlainStateSlotContributions'), 'CoreClassProduction.transaction_manager_param': AssemblyEdgeSpec(name='CoreClassProduction.transaction_manager_param', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='TransactionManagerInitParamContributions'), 'CoreClassProduction.facade_base_body_pass': AssemblyEdgeSpec(name='CoreClassProduction.facade_base_body_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='FacadeBaseBodyPassContributions'), 'CoreClassProduction.facade_properties_pass': AssemblyEdgeSpec(name='CoreClassProduction.facade_properties_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='FacadePropertiesPassContributions'), 'CoreClassProduction.default_facade_properties_pass': AssemblyEdgeSpec(name='CoreClassProduction.default_facade_properties_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='DefaultFacadePropertiesPassContributions'), 'CoreClassProduction.current_facade_properties_pass': AssemblyEdgeSpec(name='CoreClassProduction.current_facade_properties_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='CurrentFacadePropertiesPassContributions'), 'CoreClassProduction.working_facade_properties_pass': AssemblyEdgeSpec(name='CoreClassProduction.working_facade_properties_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='WorkingFacadePropertiesPassContributions'), 'CoreClassProduction.state_init_body_pass': AssemblyEdgeSpec(name='CoreClassProduction.state_init_body_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='StateInitBodyPassContributions'), 'CoreClassProduction.commit_transaction_body_pass': AssemblyEdgeSpec(name='CoreClassProduction.commit_transaction_body_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='CommitTransactionBodyPassContributions'), 'CoreClassProduction.rollback_transaction_body_pass': AssemblyEdgeSpec(name='CoreClassProduction.rollback_transaction_body_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='RollbackTransactionBodyPassContributions'), 'CoreClassProduction.commit_order_key_body_pass': AssemblyEdgeSpec(name='CoreClassProduction.commit_order_key_body_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='CommitOrderKeyBodyPassContributions'), 'CoreClassProduction.requires_validation_body_pass': AssemblyEdgeSpec(name='CoreClassProduction.requires_validation_body_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='RequiresValidationBodyPassContributions'), 'CoreClassProduction.validate_commit_body_pass': AssemblyEdgeSpec(name='CoreClassProduction.validate_commit_body_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='ValidateCommitBodyPassContributions'), 'CoreClassProduction.before_commit_body_pass': AssemblyEdgeSpec(name='CoreClassProduction.before_commit_body_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='BeforeCommitBodyPassContributions'), 'CoreClassProduction.after_commit_body_pass': AssemblyEdgeSpec(name='CoreClassProduction.after_commit_body_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='AfterCommitBodyPassContributions'), 'CoreClassProduction.after_rollback_body_pass': AssemblyEdgeSpec(name='CoreClassProduction.after_rollback_body_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='AfterRollbackBodyPassContributions'), 'CoreClassProduction.classvars': AssemblyEdgeSpec(name='CoreClassProduction.classvars', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ClassVarFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ClassVarDefaultContributions'), 'CoreClassProduction.commit_order_keys': AssemblyEdgeSpec(name='CoreClassProduction.commit_order_keys', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='method', collection_name='CommitOrderKeyProviders', collection=None),), condition=EqConditionSpec(left=ValueRef('MethodOwner'), right=ValueRef('ClassId')), matcher_name='CommitOrderKeyContributions'), 'CoreClassProduction.validation_flags': AssemblyEdgeSpec(name='CoreClassProduction.validation_flags', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='method', collection_name='CommitValidators', collection=None),), condition=EqConditionSpec(left=ValueRef('MethodOwner'), right=ValueRef('ClassId')), matcher_name='RequiresValidationContributions'), 'CoreClassProduction.validators': AssemblyEdgeSpec(name='CoreClassProduction.validators', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='method', collection_name='CommitValidators', collection=None),), condition=EqConditionSpec(left=ValueRef('MethodOwner'), right=ValueRef('ClassId')), matcher_name='ValidateCommitContributions'), 'CoreClassProduction.before_commit_hooks': AssemblyEdgeSpec(name='CoreClassProduction.before_commit_hooks', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='method', collection_name='BeforeCommitHooks', collection=None),), condition=EqConditionSpec(left=ValueRef('MethodOwner'), right=ValueRef('ClassId')), matcher_name='BeforeCommitHookContributions'), 'CoreClassProduction.after_commit_hooks': AssemblyEdgeSpec(name='CoreClassProduction.after_commit_hooks', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='method', collection_name='AfterCommitHooks', collection=None),), condition=EqConditionSpec(left=ValueRef('MethodOwner'), right=ValueRef('ClassId')), matcher_name='AfterCommitHookContributions'), 'CoreClassProduction.after_rollback_hooks': AssemblyEdgeSpec(name='CoreClassProduction.after_rollback_hooks', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='method', collection_name='AfterRollbackHooks', collection=None),), condition=EqConditionSpec(left=ValueRef('MethodOwner'), right=ValueRef('ClassId')), matcher_name='AfterRollbackHookContributions'), 'CoreClassProduction.plain_init_params': AssemblyEdgeSpec(name='CoreClassProduction.plain_init_params', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='PlainFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='PlainInitParamContributions'), 'CoreClassProduction.initvar_params': AssemblyEdgeSpec(name='CoreClassProduction.initvar_params', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='InitVarFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='InitVarParamContributions'), 'CoreClassProduction.initvar_local_defaults': AssemblyEdgeSpec(name='CoreClassProduction.initvar_local_defaults', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='InitVarFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='InitVarLocalDefaultContributions'), 'CoreClassProduction.plain_init_assignments': AssemblyEdgeSpec(name='CoreClassProduction.plain_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='PlainFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='PlainInitAssignmentContributions'), 'CoreClassProduction.plain_properties': AssemblyEdgeSpec(name='CoreClassProduction.plain_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='PlainFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='PlainPropertyContributions')}
ASSEMBLY_PRODUCTIONS = {'CoreModuleProduction': ComposableProductionSpec(name='CoreModuleProduction', inputs=(), root=RootSpec(build_name='Root', resource_name='ModuleRoot', bindings=()), applies=(InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreModuleProduction.lifecycle_definition_params', context_inputs=(), from_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), condition=None, matcher_name='BuilderParamContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreModuleProduction.annotations_params', context_inputs=(), from_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), condition=None, matcher_name='AnnotationsBuilderParamContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreModuleProduction.tx_groups_params', context_inputs=(), from_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), condition=None, matcher_name='TxGroupsBuilderParamContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreModuleProduction.field_default_params', context_inputs=(), from_inputs=(AssemblyInputSpec(name='field', collection_name='Fields', collection=None),), condition=None, matcher_name='FieldDefaultBuilderParamContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreModuleProduction.classes', context_inputs=(), from_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), condition=None, matcher_name='CoreClassDefinitionContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreModuleProduction.return_class', context_inputs=(), from_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), condition=None, matcher_name='ReturnClassContributions')))), 'CoreClassProduction': ComposableProductionSpec(name='CoreClassProduction', inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), root=RootSpec(build_name='ClassDef', resource_name='ClassBundle', bindings=(BindingSpec(kind='ident', name='state_class_decl_name', value=ValueRef('StateClassName')), BindingSpec(kind='ident', name='state_class_ref', value=ValueRef('StateClassName')), BindingSpec(kind='ident', name='default_facade_class_decl_name', value=ValueRef('ClassName')), BindingSpec(kind='ident', name='default_facade_class_ref', value=ValueRef('ClassName')), BindingSpec(kind='ident', name='facade_base_decl_name', value=ValueRef('FacadeBaseClassName')), BindingSpec(kind='ident', name='facade_base_default_base_name', value=ValueRef('FacadeBaseClassName')), BindingSpec(kind='ident', name='facade_base_current_base_name', value=ValueRef('FacadeBaseClassName')), BindingSpec(kind='ident', name='facade_base_working_base_name', value=ValueRef('FacadeBaseClassName')), BindingSpec(kind='ident', name='current_facade_class_decl_name', value=ValueRef('CurrentFacadeClassName')), BindingSpec(kind='ident', name='current_facade_class_ref', value=ValueRef('CurrentFacadeClassName')), BindingSpec(kind='ident', name='working_facade_class_decl_name', value=ValueRef('WorkingFacadeClassName')), BindingSpec(kind='ident', name='working_facade_class_ref', value=ValueRef('WorkingFacadeClassName')), BindingSpec(kind='ident', name='tx_groups_for_index_name', value=ValueRef('TxGroupsParamName')), BindingSpec(kind='ident', name='tx_groups_for_map_name', value=ValueRef('TxGroupsParamName')), BindingSpec(kind='ident', name='tx_groups_for_class_index_name', value=ValueRef('TxGroupsParamName')), BindingSpec(kind='ident', name='tx_groups_for_class_map_name', value=ValueRef('TxGroupsParamName')), BindingSpec(kind='ident', name='tx_groups_for_manager_name', value=ValueRef('TxGroupsParamName')), BindingSpec(kind='ident', name='tx_groups_for_slots_name', value=ValueRef('TxGroupsParamName')), BindingSpec(kind='ident', name='lifecycle_definition_name', value=ValueRef('LifecycleDefinitionParamName')), BindingSpec(kind='ident', name='annotations_name', value=ValueRef('AnnotationsParamName')), BindingSpec(kind='external', name='lifecycle_field_names', value=ValueRef('LifecycleFieldNames')))), applies=(InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.state_slots', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='PlainFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='PlainStateSlotContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.transaction_manager_param', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='TransactionManagerInitParamContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.facade_base_body_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='FacadeBaseBodyPassContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.facade_properties_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='FacadePropertiesPassContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.default_facade_properties_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='DefaultFacadePropertiesPassContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.current_facade_properties_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='CurrentFacadePropertiesPassContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.working_facade_properties_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='WorkingFacadePropertiesPassContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.state_init_body_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='StateInitBodyPassContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.commit_transaction_body_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='CommitTransactionBodyPassContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.rollback_transaction_body_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='RollbackTransactionBodyPassContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.commit_order_key_body_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='CommitOrderKeyBodyPassContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.requires_validation_body_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='RequiresValidationBodyPassContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.validate_commit_body_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='ValidateCommitBodyPassContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.before_commit_body_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='BeforeCommitBodyPassContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.after_commit_body_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='AfterCommitBodyPassContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.after_rollback_body_pass', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(), condition=None, matcher_name='AfterRollbackBodyPassContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.classvars', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='ClassVarFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='ClassVarDefaultContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.commit_order_keys', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='method', collection_name='CommitOrderKeyProviders', collection=None),), condition=EqConditionSpec(left=ValueRef('MethodOwner'), right=ValueRef('ClassId')), matcher_name='CommitOrderKeyContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.validation_flags', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='method', collection_name='CommitValidators', collection=None),), condition=EqConditionSpec(left=ValueRef('MethodOwner'), right=ValueRef('ClassId')), matcher_name='RequiresValidationContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.validators', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='method', collection_name='CommitValidators', collection=None),), condition=EqConditionSpec(left=ValueRef('MethodOwner'), right=ValueRef('ClassId')), matcher_name='ValidateCommitContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.before_commit_hooks', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='method', collection_name='BeforeCommitHooks', collection=None),), condition=EqConditionSpec(left=ValueRef('MethodOwner'), right=ValueRef('ClassId')), matcher_name='BeforeCommitHookContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.after_commit_hooks', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='method', collection_name='AfterCommitHooks', collection=None),), condition=EqConditionSpec(left=ValueRef('MethodOwner'), right=ValueRef('ClassId')), matcher_name='AfterCommitHookContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.after_rollback_hooks', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='method', collection_name='AfterRollbackHooks', collection=None),), condition=EqConditionSpec(left=ValueRef('MethodOwner'), right=ValueRef('ClassId')), matcher_name='AfterRollbackHookContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.plain_init_params', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='PlainFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='PlainInitParamContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.initvar_params', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='InitVarFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='InitVarParamContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.initvar_local_defaults', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='InitVarFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='InitVarLocalDefaultContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.plain_init_assignments', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='PlainFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='PlainInitAssignmentContributions')), InlineApplySpec(edge=AssemblyEdgeSpec(name='CoreClassProduction.plain_properties', context_inputs=(AssemblyInputSpec(name='lifecycle_class', collection_name='Classes', collection=None),), from_inputs=(AssemblyInputSpec(name='field', collection_name='PlainFields', collection=None),), condition=EqConditionSpec(left=ValueRef('FieldOwner'), right=ValueRef('ClassId')), matcher_name='PlainPropertyContributions'))))}
ASSEMBLY_ASSEMBLIES = {'LifecycleCoreModule': AssemblySpec(name='LifecycleCoreModule', production_name='CoreModuleProduction')}

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
