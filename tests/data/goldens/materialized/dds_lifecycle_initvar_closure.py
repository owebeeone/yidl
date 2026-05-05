from itertools import product
from yidl.generation.data_def_sys import AddIfAbsent, DDSContainerBuilder, DDSOperationContext, MatcherResult, NOT_PROVIDED, REQUIRED, RejectDuplicate, ReplaceExisting, RuntimeCollection, RuntimeComputedCollection, RuntimeContainerSpec, RuntimePort, RuntimePortIndex, RuntimeProperty, RuntimeRecord, RuntimeUnion, astichi_template, from_astichi_code
from yidl.generation.lifecycle_facts import analyze_callable
_NameProperty = RuntimeProperty('Name', str, default=REQUIRED, storage_name='name')
_KindProperty = RuntimeProperty('Kind', str, default=REQUIRED, storage_name='kind')
_AnnotationPathProperty = RuntimeProperty('AnnotationPath', str, default='', storage_name='annotation_path')
_DefaultedProperty = RuntimeProperty('Defaulted', bool, default=False, storage_name='defaulted')
_DefaultValueProperty = RuntimeProperty('DefaultValue', object, default=None, storage_name='default_value')
_OrderProperty = RuntimeProperty('Order', int, default=0, storage_name='order')
_TxGroupProperty = RuntimeProperty('TxGroup', str, default='', storage_name='tx_group')
_TxIndexProperty = RuntimeProperty('TxIndex', int, default=REQUIRED, storage_name='tx_index')
_ClassRoleProperty = RuntimeProperty('ClassRole', str, default=REQUIRED, storage_name='class_role')
_ClassNameProperty = RuntimeProperty('ClassName', str, default=REQUIRED, storage_name='class_name')
_StateClassNameProperty = RuntimeProperty('StateClassName', str, default='', storage_name='state_class_name')
_TargetPortProperty = RuntimeProperty('TargetPort', object, default=REQUIRED, storage_name='target_port')
_TemplateProperty = RuntimeProperty('Template', object, default=REQUIRED, storage_name='template')
_RuntimeValueProperty = RuntimeProperty('RuntimeValue', object, default=REQUIRED, storage_name='runtime_value')
_SlotNameProperty = RuntimeProperty('SlotName', str, default='', storage_name='slot_name')
_SourceNameProperty = RuntimeProperty('SourceName', str, default='', storage_name='source_name')
_TargetNameProperty = RuntimeProperty('TargetName', str, default='', storage_name='target_name')
_FieldNameProperty = RuntimeProperty('FieldName', str, default='', storage_name='field_name')
_CurrentSlotProperty = RuntimeProperty('CurrentSlot', str, default='', storage_name='current_slot')
_WorkingSlotProperty = RuntimeProperty('WorkingSlot', str, default='', storage_name='working_slot')
_PublishedSlotProperty = RuntimeProperty('PublishedSlot', str, default='', storage_name='published_slot')
_PhaseProperty = RuntimeProperty('Phase', str, default='', storage_name='phase')
_OperationKindProperty = RuntimeProperty('OperationKind', str, default='', storage_name='operation_kind')
_CallablePathProperty = RuntimeProperty('CallablePath', str, default=REQUIRED, storage_name='callable_path')
_ReleasePathProperty = RuntimeProperty('ReleasePath', str, default='', storage_name='release_path')
_ResourcePolicyProperty = RuntimeProperty('ResourcePolicy', str, default='', storage_name='resource_policy')
_SourceLabelProperty = RuntimeProperty('SourceLabel', str, default='', storage_name='source_label')
_CallableObjectProperty = RuntimeProperty('CallableObject', object, default=REQUIRED, storage_name='callable_object')
_CallableRoleProperty = RuntimeProperty('CallableRole', str, default=REQUIRED, storage_name='callable_role')
_AllowedInjectionsProperty = RuntimeProperty('AllowedInjections', tuple, default=(), storage_name='allowed_injections')
_AcceptsVarArgsProperty = RuntimeProperty('AcceptsVarArgs', bool, default=False, storage_name='accepts_var_args')
_AcceptsVarKwargsProperty = RuntimeProperty('AcceptsVarKwargs', bool, default=False, storage_name='accepts_var_kwargs')
_CallableNameProperty = RuntimeProperty('CallableName', str, default=REQUIRED, storage_name='callable_name')
_ParamNameProperty = RuntimeProperty('ParamName', str, default=REQUIRED, storage_name='param_name')
_ParamKindProperty = RuntimeProperty('ParamKind', str, default=REQUIRED, storage_name='param_kind')
_ParamOrderProperty = RuntimeProperty('ParamOrder', int, default=0, storage_name='param_order')
_InjectionKindProperty = RuntimeProperty('InjectionKind', str, default=REQUIRED, storage_name='injection_kind')
_RequiredProperty = RuntimeProperty('Required', bool, default=True, storage_name='required')
_ConsumerProperty = RuntimeProperty('Consumer', str, default=REQUIRED, storage_name='consumer')
_InitVarNameProperty = RuntimeProperty('InitVarName', str, default=REQUIRED, storage_name='initvar_name')
_ManagedFieldSpec = RuntimeRecord('ManagedField', (_NameProperty, _KindProperty, _AnnotationPathProperty, _DefaultedProperty, _DefaultValueProperty, _OrderProperty, _TxGroupProperty))
_ConstFieldSpec = RuntimeRecord('ConstField', (_NameProperty, _KindProperty, _AnnotationPathProperty, _DefaultedProperty, _DefaultValueProperty, _OrderProperty, _TxGroupProperty))
_TxGroupRecordSpec = RuntimeRecord('TxGroupRecord', (_TxGroupProperty, _TxIndexProperty))
_ClassInputSpec = RuntimeRecord('ClassInput', (_ClassNameProperty, _StateClassNameProperty))
_ClassNameContributionSpec = RuntimeRecord('ClassNameContribution', (_ClassRoleProperty, _TargetPortProperty, _OrderProperty, _RuntimeValueProperty))
_ClassComponentSpec = RuntimeRecord('ClassComponent', (_ClassRoleProperty, _NameProperty, _TargetPortProperty, _OrderProperty, _TemplateProperty, _FieldNameProperty, _CurrentSlotProperty, _WorkingSlotProperty, _PublishedSlotProperty, _SourceNameProperty, _TargetNameProperty, _StateClassNameProperty))
_ModuleComponentSpec = RuntimeRecord('ModuleComponent', (_NameProperty, _TargetPortProperty, _OrderProperty, _TemplateProperty))
_SlotItemSpec = RuntimeRecord('SlotItem', (_ClassRoleProperty, _NameProperty, _TargetPortProperty, _OrderProperty, _TemplateProperty, _SlotNameProperty))
_InitParamSpec = RuntimeRecord('InitParam', (_ClassRoleProperty, _NameProperty, _TargetPortProperty, _OrderProperty, _TemplateProperty, _AnnotationPathProperty, _DefaultedProperty, _DefaultValueProperty))
_StateCtorArgSpec = RuntimeRecord('StateCtorArg', (_ClassRoleProperty, _NameProperty, _TargetPortProperty, _OrderProperty, _TemplateProperty))
_OperationContributionSpec = RuntimeRecord('OperationContribution', (_ClassRoleProperty, _NameProperty, _PhaseProperty, _OperationKindProperty, _TargetPortProperty, _OrderProperty, _TemplateProperty, _FieldNameProperty, _CurrentSlotProperty, _WorkingSlotProperty, _PublishedSlotProperty))
_MethodStatementSpec = RuntimeRecord('MethodStatement', (_ClassRoleProperty, _NameProperty, _TargetPortProperty, _OrderProperty, _TemplateProperty, _CurrentSlotProperty, _WorkingSlotProperty))
_CallableDeclarationSpec = RuntimeRecord('CallableDeclaration', (_NameProperty, _SourceLabelProperty, _CallableObjectProperty, _CallableRoleProperty, _AllowedInjectionsProperty))
_CallableSpecSpec = RuntimeRecord('CallableSpec', (_NameProperty, _SourceLabelProperty, _CallableRoleProperty, _AcceptsVarArgsProperty, _AcceptsVarKwargsProperty))
_CallableParamSpec = RuntimeRecord('CallableParam', (_CallableNameProperty, _ParamNameProperty, _ParamKindProperty, _ParamOrderProperty))
_CallableInjectionSpec = RuntimeRecord('CallableInjection', (_CallableNameProperty, _ParamNameProperty, _InjectionKindProperty, _RequiredProperty))
_CommitValidatorSpec = RuntimeRecord('CommitValidator', (_NameProperty, _SourceLabelProperty, _CallableObjectProperty, _CallableRoleProperty, _TxGroupProperty, _OrderProperty, _AllowedInjectionsProperty, _CallablePathProperty))
_CommitOrderKeySpec = RuntimeRecord('CommitOrderKey', (_NameProperty, _SourceLabelProperty, _CallableObjectProperty, _CallableRoleProperty, _TxGroupProperty, _OrderProperty, _AllowedInjectionsProperty, _CallablePathProperty))
_HookDeclarationSpec = RuntimeRecord('HookDeclaration', (_NameProperty, _SourceLabelProperty, _CallableObjectProperty, _CallableRoleProperty, _TxGroupProperty, _PhaseProperty, _OrderProperty, _AllowedInjectionsProperty, _CallablePathProperty))
_HookMethodStatementSpec = RuntimeRecord('HookMethodStatement', (_ClassRoleProperty, _NameProperty, _TargetPortProperty, _OrderProperty, _TemplateProperty, _CallablePathProperty))
_ResourceCleanupStatementSpec = RuntimeRecord('ResourceCleanupStatement', (_ClassRoleProperty, _NameProperty, _TargetPortProperty, _OrderProperty, _TemplateProperty, _ReleasePathProperty, _PublishedSlotProperty))
_OwnedFieldSpec = RuntimeRecord('OwnedField', (_NameProperty, _KindProperty, _AnnotationPathProperty, _DefaultedProperty, _DefaultValueProperty, _OrderProperty, _TxGroupProperty, _ReleasePathProperty, _ResourcePolicyProperty))
_BindingFieldSpec = RuntimeRecord('BindingField', (_NameProperty, _KindProperty, _AnnotationPathProperty, _DefaultedProperty, _DefaultValueProperty, _OrderProperty, _TxGroupProperty, _ReleasePathProperty, _ResourcePolicyProperty))
_InitvarEdgeSpec = RuntimeRecord('InitvarEdge', (_ConsumerProperty, _InitVarNameProperty, _SourceLabelProperty))
_LateInitvarConsumerSpec = RuntimeRecord('LateInitvarConsumer', (_ConsumerProperty, _SourceLabelProperty))
_RetainedInitVarSpec = RuntimeRecord('RetainedInitVar', (_NameProperty, _SourceLabelProperty))
_ConstructorOnlyInitVarSpec = RuntimeRecord('ConstructorOnlyInitVar', (_NameProperty, _SourceLabelProperty))
_InitVarFieldSpec = RuntimeRecord('InitVarField', (_NameProperty, _KindProperty, _AnnotationPathProperty, _DefaultedProperty, _DefaultValueProperty, _OrderProperty, _TxGroupProperty, _SourceLabelProperty))
_FieldSpecsUnion = RuntimeUnion('FieldSpecs', (_ManagedFieldSpec, _ConstFieldSpec, _OwnedFieldSpec, _BindingFieldSpec, _InitVarFieldSpec))

class ManagedField:
    __slots__ = ('name', 'kind', 'annotation_path', 'defaulted', 'default_value', 'order', 'tx_group')
    __dds_record_spec__ = _ManagedFieldSpec
    name: str
    kind: str
    annotation_path: str
    defaulted: bool
    default_value: object
    order: int
    tx_group: str

    def __init__(self, *, name: str, kind: str, annotation_path: str='', defaulted: bool=False, default_value: object=None, order: int=0, tx_group: str=''):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        if not isinstance(kind, str):
            raise TypeError('Kind must be str, got ' + type(kind).__name__)
        object.__setattr__(self, 'kind', kind)
        if not isinstance(annotation_path, str):
            raise TypeError('AnnotationPath must be str, got ' + type(annotation_path).__name__)
        object.__setattr__(self, 'annotation_path', annotation_path)
        if not isinstance(defaulted, bool):
            raise TypeError('Defaulted must be bool, got ' + type(defaulted).__name__)
        object.__setattr__(self, 'defaulted', defaulted)
        object.__setattr__(self, 'default_value', default_value)
        if not isinstance(order, int):
            raise TypeError('Order must be int, got ' + type(order).__name__)
        object.__setattr__(self, 'order', order)
        if not isinstance(tx_group, str):
            raise TypeError('TxGroup must be str, got ' + type(tx_group).__name__)
        object.__setattr__(self, 'tx_group', tx_group)

    def __setattr__(self, name, value):
        if name in ('name', 'kind', 'annotation_path', 'defaulted', 'default_value', 'order', 'tx_group'):
            raise AttributeError('ManagedField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('kind=' + repr(self.kind))
        pieces.append('annotation_path=' + repr(self.annotation_path))
        pieces.append('defaulted=' + repr(self.defaulted))
        pieces.append('default_value=' + repr(self.default_value))
        pieces.append('order=' + repr(self.order))
        pieces.append('tx_group=' + repr(self.tx_group))
        return 'ManagedField' + '(' + ', '.join(pieces) + ')'
_ManagedFieldSpec.bind_record_class(ManagedField)

class ConstField:
    __slots__ = ('name', 'kind', 'annotation_path', 'defaulted', 'default_value', 'order', 'tx_group')
    __dds_record_spec__ = _ConstFieldSpec
    name: str
    kind: str
    annotation_path: str
    defaulted: bool
    default_value: object
    order: int
    tx_group: str

    def __init__(self, *, name: str, kind: str, annotation_path: str='', defaulted: bool=False, default_value: object=None, order: int=0, tx_group: str=''):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        if not isinstance(kind, str):
            raise TypeError('Kind must be str, got ' + type(kind).__name__)
        object.__setattr__(self, 'kind', kind)
        if not isinstance(annotation_path, str):
            raise TypeError('AnnotationPath must be str, got ' + type(annotation_path).__name__)
        object.__setattr__(self, 'annotation_path', annotation_path)
        if not isinstance(defaulted, bool):
            raise TypeError('Defaulted must be bool, got ' + type(defaulted).__name__)
        object.__setattr__(self, 'defaulted', defaulted)
        object.__setattr__(self, 'default_value', default_value)
        if not isinstance(order, int):
            raise TypeError('Order must be int, got ' + type(order).__name__)
        object.__setattr__(self, 'order', order)
        if not isinstance(tx_group, str):
            raise TypeError('TxGroup must be str, got ' + type(tx_group).__name__)
        object.__setattr__(self, 'tx_group', tx_group)

    def __setattr__(self, name, value):
        if name in ('name', 'kind', 'annotation_path', 'defaulted', 'default_value', 'order', 'tx_group'):
            raise AttributeError('ConstField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('kind=' + repr(self.kind))
        pieces.append('annotation_path=' + repr(self.annotation_path))
        pieces.append('defaulted=' + repr(self.defaulted))
        pieces.append('default_value=' + repr(self.default_value))
        pieces.append('order=' + repr(self.order))
        pieces.append('tx_group=' + repr(self.tx_group))
        return 'ConstField' + '(' + ', '.join(pieces) + ')'
_ConstFieldSpec.bind_record_class(ConstField)

class TxGroupRecord:
    __slots__ = ('tx_group', 'tx_index')
    __dds_record_spec__ = _TxGroupRecordSpec
    tx_group: str
    tx_index: int

    def __init__(self, *, tx_group: str='', tx_index: int):
        if not isinstance(tx_group, str):
            raise TypeError('TxGroup must be str, got ' + type(tx_group).__name__)
        object.__setattr__(self, 'tx_group', tx_group)
        if not isinstance(tx_index, int):
            raise TypeError('TxIndex must be int, got ' + type(tx_index).__name__)
        object.__setattr__(self, 'tx_index', tx_index)

    def __setattr__(self, name, value):
        if name in ('tx_group', 'tx_index'):
            raise AttributeError('TxGroupRecord records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('tx_group=' + repr(self.tx_group))
        pieces.append('tx_index=' + repr(self.tx_index))
        return 'TxGroupRecord' + '(' + ', '.join(pieces) + ')'
_TxGroupRecordSpec.bind_record_class(TxGroupRecord)

class ClassInput:
    __slots__ = ('class_name', 'state_class_name')
    __dds_record_spec__ = _ClassInputSpec
    class_name: str
    state_class_name: str

    def __init__(self, *, class_name: str, state_class_name: str=''):
        if not isinstance(class_name, str):
            raise TypeError('ClassName must be str, got ' + type(class_name).__name__)
        object.__setattr__(self, 'class_name', class_name)
        if not isinstance(state_class_name, str):
            raise TypeError('StateClassName must be str, got ' + type(state_class_name).__name__)
        object.__setattr__(self, 'state_class_name', state_class_name)

    def __setattr__(self, name, value):
        if name in ('class_name', 'state_class_name'):
            raise AttributeError('ClassInput records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('class_name=' + repr(self.class_name))
        pieces.append('state_class_name=' + repr(self.state_class_name))
        return 'ClassInput' + '(' + ', '.join(pieces) + ')'
_ClassInputSpec.bind_record_class(ClassInput)

class ClassNameContribution:
    __slots__ = ('class_role', 'target_port', 'order', 'runtime_value')
    __dds_record_spec__ = _ClassNameContributionSpec
    class_role: str
    target_port: object
    order: int
    runtime_value: object

    def __init__(self, *, class_role: str, target_port: object, order: int=0, runtime_value: object):
        if not isinstance(class_role, str):
            raise TypeError('ClassRole must be str, got ' + type(class_role).__name__)
        object.__setattr__(self, 'class_role', class_role)
        object.__setattr__(self, 'target_port', target_port)
        if not isinstance(order, int):
            raise TypeError('Order must be int, got ' + type(order).__name__)
        object.__setattr__(self, 'order', order)
        object.__setattr__(self, 'runtime_value', runtime_value)

    def __setattr__(self, name, value):
        if name in ('class_role', 'target_port', 'order', 'runtime_value'):
            raise AttributeError('ClassNameContribution records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('class_role=' + repr(self.class_role))
        pieces.append('target_port=' + repr(self.target_port))
        pieces.append('order=' + repr(self.order))
        pieces.append('runtime_value=' + repr(self.runtime_value))
        return 'ClassNameContribution' + '(' + ', '.join(pieces) + ')'
_ClassNameContributionSpec.bind_record_class(ClassNameContribution)

class ClassComponent:
    __slots__ = ('class_role', 'name', 'target_port', 'order', 'template', 'field_name', 'current_slot', 'working_slot', 'published_slot', 'source_name', 'target_name', 'state_class_name')
    __dds_record_spec__ = _ClassComponentSpec
    class_role: str
    name: str
    target_port: object
    order: int
    template: object
    field_name: str
    current_slot: str
    working_slot: str
    published_slot: str
    source_name: str
    target_name: str
    state_class_name: str

    def __init__(self, *, class_role: str, name: str, target_port: object, order: int=0, template: object, field_name: str='', current_slot: str='', working_slot: str='', published_slot: str='', source_name: str='', target_name: str='', state_class_name: str=''):
        if not isinstance(class_role, str):
            raise TypeError('ClassRole must be str, got ' + type(class_role).__name__)
        object.__setattr__(self, 'class_role', class_role)
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'target_port', target_port)
        if not isinstance(order, int):
            raise TypeError('Order must be int, got ' + type(order).__name__)
        object.__setattr__(self, 'order', order)
        object.__setattr__(self, 'template', template)
        if not isinstance(field_name, str):
            raise TypeError('FieldName must be str, got ' + type(field_name).__name__)
        object.__setattr__(self, 'field_name', field_name)
        if not isinstance(current_slot, str):
            raise TypeError('CurrentSlot must be str, got ' + type(current_slot).__name__)
        object.__setattr__(self, 'current_slot', current_slot)
        if not isinstance(working_slot, str):
            raise TypeError('WorkingSlot must be str, got ' + type(working_slot).__name__)
        object.__setattr__(self, 'working_slot', working_slot)
        if not isinstance(published_slot, str):
            raise TypeError('PublishedSlot must be str, got ' + type(published_slot).__name__)
        object.__setattr__(self, 'published_slot', published_slot)
        if not isinstance(source_name, str):
            raise TypeError('SourceName must be str, got ' + type(source_name).__name__)
        object.__setattr__(self, 'source_name', source_name)
        if not isinstance(target_name, str):
            raise TypeError('TargetName must be str, got ' + type(target_name).__name__)
        object.__setattr__(self, 'target_name', target_name)
        if not isinstance(state_class_name, str):
            raise TypeError('StateClassName must be str, got ' + type(state_class_name).__name__)
        object.__setattr__(self, 'state_class_name', state_class_name)

    def __setattr__(self, name, value):
        if name in ('class_role', 'name', 'target_port', 'order', 'template', 'field_name', 'current_slot', 'working_slot', 'published_slot', 'source_name', 'target_name', 'state_class_name'):
            raise AttributeError('ClassComponent records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('class_role=' + repr(self.class_role))
        pieces.append('name=' + repr(self.name))
        pieces.append('target_port=' + repr(self.target_port))
        pieces.append('order=' + repr(self.order))
        pieces.append('template=' + repr(self.template))
        pieces.append('field_name=' + repr(self.field_name))
        pieces.append('current_slot=' + repr(self.current_slot))
        pieces.append('working_slot=' + repr(self.working_slot))
        pieces.append('published_slot=' + repr(self.published_slot))
        pieces.append('source_name=' + repr(self.source_name))
        pieces.append('target_name=' + repr(self.target_name))
        pieces.append('state_class_name=' + repr(self.state_class_name))
        return 'ClassComponent' + '(' + ', '.join(pieces) + ')'
_ClassComponentSpec.bind_record_class(ClassComponent)

class ModuleComponent:
    __slots__ = ('name', 'target_port', 'order', 'template')
    __dds_record_spec__ = _ModuleComponentSpec
    name: str
    target_port: object
    order: int
    template: object

    def __init__(self, *, name: str, target_port: object, order: int=0, template: object):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'target_port', target_port)
        if not isinstance(order, int):
            raise TypeError('Order must be int, got ' + type(order).__name__)
        object.__setattr__(self, 'order', order)
        object.__setattr__(self, 'template', template)

    def __setattr__(self, name, value):
        if name in ('name', 'target_port', 'order', 'template'):
            raise AttributeError('ModuleComponent records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('target_port=' + repr(self.target_port))
        pieces.append('order=' + repr(self.order))
        pieces.append('template=' + repr(self.template))
        return 'ModuleComponent' + '(' + ', '.join(pieces) + ')'
_ModuleComponentSpec.bind_record_class(ModuleComponent)

class SlotItem:
    __slots__ = ('class_role', 'name', 'target_port', 'order', 'template', 'slot_name')
    __dds_record_spec__ = _SlotItemSpec
    class_role: str
    name: str
    target_port: object
    order: int
    template: object
    slot_name: str

    def __init__(self, *, class_role: str, name: str, target_port: object, order: int=0, template: object, slot_name: str=''):
        if not isinstance(class_role, str):
            raise TypeError('ClassRole must be str, got ' + type(class_role).__name__)
        object.__setattr__(self, 'class_role', class_role)
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'target_port', target_port)
        if not isinstance(order, int):
            raise TypeError('Order must be int, got ' + type(order).__name__)
        object.__setattr__(self, 'order', order)
        object.__setattr__(self, 'template', template)
        if not isinstance(slot_name, str):
            raise TypeError('SlotName must be str, got ' + type(slot_name).__name__)
        object.__setattr__(self, 'slot_name', slot_name)

    def __setattr__(self, name, value):
        if name in ('class_role', 'name', 'target_port', 'order', 'template', 'slot_name'):
            raise AttributeError('SlotItem records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('class_role=' + repr(self.class_role))
        pieces.append('name=' + repr(self.name))
        pieces.append('target_port=' + repr(self.target_port))
        pieces.append('order=' + repr(self.order))
        pieces.append('template=' + repr(self.template))
        pieces.append('slot_name=' + repr(self.slot_name))
        return 'SlotItem' + '(' + ', '.join(pieces) + ')'
_SlotItemSpec.bind_record_class(SlotItem)

class InitParam:
    __slots__ = ('class_role', 'name', 'target_port', 'order', 'template', 'annotation_path', 'defaulted', 'default_value')
    __dds_record_spec__ = _InitParamSpec
    class_role: str
    name: str
    target_port: object
    order: int
    template: object
    annotation_path: str
    defaulted: bool
    default_value: object

    def __init__(self, *, class_role: str, name: str, target_port: object, order: int=0, template: object, annotation_path: str='', defaulted: bool=False, default_value: object=None):
        if not isinstance(class_role, str):
            raise TypeError('ClassRole must be str, got ' + type(class_role).__name__)
        object.__setattr__(self, 'class_role', class_role)
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'target_port', target_port)
        if not isinstance(order, int):
            raise TypeError('Order must be int, got ' + type(order).__name__)
        object.__setattr__(self, 'order', order)
        object.__setattr__(self, 'template', template)
        if not isinstance(annotation_path, str):
            raise TypeError('AnnotationPath must be str, got ' + type(annotation_path).__name__)
        object.__setattr__(self, 'annotation_path', annotation_path)
        if not isinstance(defaulted, bool):
            raise TypeError('Defaulted must be bool, got ' + type(defaulted).__name__)
        object.__setattr__(self, 'defaulted', defaulted)
        object.__setattr__(self, 'default_value', default_value)

    def __setattr__(self, name, value):
        if name in ('class_role', 'name', 'target_port', 'order', 'template', 'annotation_path', 'defaulted', 'default_value'):
            raise AttributeError('InitParam records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('class_role=' + repr(self.class_role))
        pieces.append('name=' + repr(self.name))
        pieces.append('target_port=' + repr(self.target_port))
        pieces.append('order=' + repr(self.order))
        pieces.append('template=' + repr(self.template))
        pieces.append('annotation_path=' + repr(self.annotation_path))
        pieces.append('defaulted=' + repr(self.defaulted))
        pieces.append('default_value=' + repr(self.default_value))
        return 'InitParam' + '(' + ', '.join(pieces) + ')'
_InitParamSpec.bind_record_class(InitParam)

class StateCtorArg:
    __slots__ = ('class_role', 'name', 'target_port', 'order', 'template')
    __dds_record_spec__ = _StateCtorArgSpec
    class_role: str
    name: str
    target_port: object
    order: int
    template: object

    def __init__(self, *, class_role: str, name: str, target_port: object, order: int=0, template: object):
        if not isinstance(class_role, str):
            raise TypeError('ClassRole must be str, got ' + type(class_role).__name__)
        object.__setattr__(self, 'class_role', class_role)
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'target_port', target_port)
        if not isinstance(order, int):
            raise TypeError('Order must be int, got ' + type(order).__name__)
        object.__setattr__(self, 'order', order)
        object.__setattr__(self, 'template', template)

    def __setattr__(self, name, value):
        if name in ('class_role', 'name', 'target_port', 'order', 'template'):
            raise AttributeError('StateCtorArg records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('class_role=' + repr(self.class_role))
        pieces.append('name=' + repr(self.name))
        pieces.append('target_port=' + repr(self.target_port))
        pieces.append('order=' + repr(self.order))
        pieces.append('template=' + repr(self.template))
        return 'StateCtorArg' + '(' + ', '.join(pieces) + ')'
_StateCtorArgSpec.bind_record_class(StateCtorArg)

class OperationContribution:
    __slots__ = ('class_role', 'name', 'phase', 'operation_kind', 'target_port', 'order', 'template', 'field_name', 'current_slot', 'working_slot', 'published_slot')
    __dds_record_spec__ = _OperationContributionSpec
    class_role: str
    name: str
    phase: str
    operation_kind: str
    target_port: object
    order: int
    template: object
    field_name: str
    current_slot: str
    working_slot: str
    published_slot: str

    def __init__(self, *, class_role: str, name: str, phase: str='', operation_kind: str='', target_port: object, order: int=0, template: object, field_name: str='', current_slot: str='', working_slot: str='', published_slot: str=''):
        if not isinstance(class_role, str):
            raise TypeError('ClassRole must be str, got ' + type(class_role).__name__)
        object.__setattr__(self, 'class_role', class_role)
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        if not isinstance(phase, str):
            raise TypeError('Phase must be str, got ' + type(phase).__name__)
        object.__setattr__(self, 'phase', phase)
        if not isinstance(operation_kind, str):
            raise TypeError('OperationKind must be str, got ' + type(operation_kind).__name__)
        object.__setattr__(self, 'operation_kind', operation_kind)
        object.__setattr__(self, 'target_port', target_port)
        if not isinstance(order, int):
            raise TypeError('Order must be int, got ' + type(order).__name__)
        object.__setattr__(self, 'order', order)
        object.__setattr__(self, 'template', template)
        if not isinstance(field_name, str):
            raise TypeError('FieldName must be str, got ' + type(field_name).__name__)
        object.__setattr__(self, 'field_name', field_name)
        if not isinstance(current_slot, str):
            raise TypeError('CurrentSlot must be str, got ' + type(current_slot).__name__)
        object.__setattr__(self, 'current_slot', current_slot)
        if not isinstance(working_slot, str):
            raise TypeError('WorkingSlot must be str, got ' + type(working_slot).__name__)
        object.__setattr__(self, 'working_slot', working_slot)
        if not isinstance(published_slot, str):
            raise TypeError('PublishedSlot must be str, got ' + type(published_slot).__name__)
        object.__setattr__(self, 'published_slot', published_slot)

    def __setattr__(self, name, value):
        if name in ('class_role', 'name', 'phase', 'operation_kind', 'target_port', 'order', 'template', 'field_name', 'current_slot', 'working_slot', 'published_slot'):
            raise AttributeError('OperationContribution records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('class_role=' + repr(self.class_role))
        pieces.append('name=' + repr(self.name))
        pieces.append('phase=' + repr(self.phase))
        pieces.append('operation_kind=' + repr(self.operation_kind))
        pieces.append('target_port=' + repr(self.target_port))
        pieces.append('order=' + repr(self.order))
        pieces.append('template=' + repr(self.template))
        pieces.append('field_name=' + repr(self.field_name))
        pieces.append('current_slot=' + repr(self.current_slot))
        pieces.append('working_slot=' + repr(self.working_slot))
        pieces.append('published_slot=' + repr(self.published_slot))
        return 'OperationContribution' + '(' + ', '.join(pieces) + ')'
_OperationContributionSpec.bind_record_class(OperationContribution)

class MethodStatement:
    __slots__ = ('class_role', 'name', 'target_port', 'order', 'template', 'current_slot', 'working_slot')
    __dds_record_spec__ = _MethodStatementSpec
    class_role: str
    name: str
    target_port: object
    order: int
    template: object
    current_slot: str
    working_slot: str

    def __init__(self, *, class_role: str, name: str, target_port: object, order: int=0, template: object, current_slot: str='', working_slot: str=''):
        if not isinstance(class_role, str):
            raise TypeError('ClassRole must be str, got ' + type(class_role).__name__)
        object.__setattr__(self, 'class_role', class_role)
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'target_port', target_port)
        if not isinstance(order, int):
            raise TypeError('Order must be int, got ' + type(order).__name__)
        object.__setattr__(self, 'order', order)
        object.__setattr__(self, 'template', template)
        if not isinstance(current_slot, str):
            raise TypeError('CurrentSlot must be str, got ' + type(current_slot).__name__)
        object.__setattr__(self, 'current_slot', current_slot)
        if not isinstance(working_slot, str):
            raise TypeError('WorkingSlot must be str, got ' + type(working_slot).__name__)
        object.__setattr__(self, 'working_slot', working_slot)

    def __setattr__(self, name, value):
        if name in ('class_role', 'name', 'target_port', 'order', 'template', 'current_slot', 'working_slot'):
            raise AttributeError('MethodStatement records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('class_role=' + repr(self.class_role))
        pieces.append('name=' + repr(self.name))
        pieces.append('target_port=' + repr(self.target_port))
        pieces.append('order=' + repr(self.order))
        pieces.append('template=' + repr(self.template))
        pieces.append('current_slot=' + repr(self.current_slot))
        pieces.append('working_slot=' + repr(self.working_slot))
        return 'MethodStatement' + '(' + ', '.join(pieces) + ')'
_MethodStatementSpec.bind_record_class(MethodStatement)

class CallableDeclaration:
    __slots__ = ('name', 'source_label', 'callable_object', 'callable_role', 'allowed_injections')
    __dds_record_spec__ = _CallableDeclarationSpec
    name: str
    source_label: str
    callable_object: object
    callable_role: str
    allowed_injections: tuple

    def __init__(self, *, name: str, source_label: str='', callable_object: object, callable_role: str, allowed_injections: tuple=()):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        if not isinstance(source_label, str):
            raise TypeError('SourceLabel must be str, got ' + type(source_label).__name__)
        object.__setattr__(self, 'source_label', source_label)
        object.__setattr__(self, 'callable_object', callable_object)
        if not isinstance(callable_role, str):
            raise TypeError('CallableRole must be str, got ' + type(callable_role).__name__)
        object.__setattr__(self, 'callable_role', callable_role)
        if not isinstance(allowed_injections, tuple):
            raise TypeError('AllowedInjections must be tuple, got ' + type(allowed_injections).__name__)
        object.__setattr__(self, 'allowed_injections', allowed_injections)

    def __setattr__(self, name, value):
        if name in ('name', 'source_label', 'callable_object', 'callable_role', 'allowed_injections'):
            raise AttributeError('CallableDeclaration records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('source_label=' + repr(self.source_label))
        pieces.append('callable_object=' + repr(self.callable_object))
        pieces.append('callable_role=' + repr(self.callable_role))
        pieces.append('allowed_injections=' + repr(self.allowed_injections))
        return 'CallableDeclaration' + '(' + ', '.join(pieces) + ')'
_CallableDeclarationSpec.bind_record_class(CallableDeclaration)

class CallableSpec:
    __slots__ = ('name', 'source_label', 'callable_role', 'accepts_var_args', 'accepts_var_kwargs')
    __dds_record_spec__ = _CallableSpecSpec
    name: str
    source_label: str
    callable_role: str
    accepts_var_args: bool
    accepts_var_kwargs: bool

    def __init__(self, *, name: str, source_label: str='', callable_role: str, accepts_var_args: bool=False, accepts_var_kwargs: bool=False):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        if not isinstance(source_label, str):
            raise TypeError('SourceLabel must be str, got ' + type(source_label).__name__)
        object.__setattr__(self, 'source_label', source_label)
        if not isinstance(callable_role, str):
            raise TypeError('CallableRole must be str, got ' + type(callable_role).__name__)
        object.__setattr__(self, 'callable_role', callable_role)
        if not isinstance(accepts_var_args, bool):
            raise TypeError('AcceptsVarArgs must be bool, got ' + type(accepts_var_args).__name__)
        object.__setattr__(self, 'accepts_var_args', accepts_var_args)
        if not isinstance(accepts_var_kwargs, bool):
            raise TypeError('AcceptsVarKwargs must be bool, got ' + type(accepts_var_kwargs).__name__)
        object.__setattr__(self, 'accepts_var_kwargs', accepts_var_kwargs)

    def __setattr__(self, name, value):
        if name in ('name', 'source_label', 'callable_role', 'accepts_var_args', 'accepts_var_kwargs'):
            raise AttributeError('CallableSpec records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('source_label=' + repr(self.source_label))
        pieces.append('callable_role=' + repr(self.callable_role))
        pieces.append('accepts_var_args=' + repr(self.accepts_var_args))
        pieces.append('accepts_var_kwargs=' + repr(self.accepts_var_kwargs))
        return 'CallableSpec' + '(' + ', '.join(pieces) + ')'
_CallableSpecSpec.bind_record_class(CallableSpec)

class CallableParam:
    __slots__ = ('callable_name', 'param_name', 'param_kind', 'param_order')
    __dds_record_spec__ = _CallableParamSpec
    callable_name: str
    param_name: str
    param_kind: str
    param_order: int

    def __init__(self, *, callable_name: str, param_name: str, param_kind: str, param_order: int=0):
        if not isinstance(callable_name, str):
            raise TypeError('CallableName must be str, got ' + type(callable_name).__name__)
        object.__setattr__(self, 'callable_name', callable_name)
        if not isinstance(param_name, str):
            raise TypeError('ParamName must be str, got ' + type(param_name).__name__)
        object.__setattr__(self, 'param_name', param_name)
        if not isinstance(param_kind, str):
            raise TypeError('ParamKind must be str, got ' + type(param_kind).__name__)
        object.__setattr__(self, 'param_kind', param_kind)
        if not isinstance(param_order, int):
            raise TypeError('ParamOrder must be int, got ' + type(param_order).__name__)
        object.__setattr__(self, 'param_order', param_order)

    def __setattr__(self, name, value):
        if name in ('callable_name', 'param_name', 'param_kind', 'param_order'):
            raise AttributeError('CallableParam records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('callable_name=' + repr(self.callable_name))
        pieces.append('param_name=' + repr(self.param_name))
        pieces.append('param_kind=' + repr(self.param_kind))
        pieces.append('param_order=' + repr(self.param_order))
        return 'CallableParam' + '(' + ', '.join(pieces) + ')'
_CallableParamSpec.bind_record_class(CallableParam)

class CallableInjection:
    __slots__ = ('callable_name', 'param_name', 'injection_kind', 'required')
    __dds_record_spec__ = _CallableInjectionSpec
    callable_name: str
    param_name: str
    injection_kind: str
    required: bool

    def __init__(self, *, callable_name: str, param_name: str, injection_kind: str, required: bool=True):
        if not isinstance(callable_name, str):
            raise TypeError('CallableName must be str, got ' + type(callable_name).__name__)
        object.__setattr__(self, 'callable_name', callable_name)
        if not isinstance(param_name, str):
            raise TypeError('ParamName must be str, got ' + type(param_name).__name__)
        object.__setattr__(self, 'param_name', param_name)
        if not isinstance(injection_kind, str):
            raise TypeError('InjectionKind must be str, got ' + type(injection_kind).__name__)
        object.__setattr__(self, 'injection_kind', injection_kind)
        if not isinstance(required, bool):
            raise TypeError('Required must be bool, got ' + type(required).__name__)
        object.__setattr__(self, 'required', required)

    def __setattr__(self, name, value):
        if name in ('callable_name', 'param_name', 'injection_kind', 'required'):
            raise AttributeError('CallableInjection records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('callable_name=' + repr(self.callable_name))
        pieces.append('param_name=' + repr(self.param_name))
        pieces.append('injection_kind=' + repr(self.injection_kind))
        pieces.append('required=' + repr(self.required))
        return 'CallableInjection' + '(' + ', '.join(pieces) + ')'
_CallableInjectionSpec.bind_record_class(CallableInjection)

class CommitValidator:
    __slots__ = ('name', 'source_label', 'callable_object', 'callable_role', 'tx_group', 'order', 'allowed_injections', 'callable_path')
    __dds_record_spec__ = _CommitValidatorSpec
    name: str
    source_label: str
    callable_object: object
    callable_role: str
    tx_group: str
    order: int
    allowed_injections: tuple
    callable_path: str

    def __init__(self, *, name: str, source_label: str='', callable_object: object, callable_role: str, tx_group: str='', order: int=0, allowed_injections: tuple=(), callable_path: str):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        if not isinstance(source_label, str):
            raise TypeError('SourceLabel must be str, got ' + type(source_label).__name__)
        object.__setattr__(self, 'source_label', source_label)
        object.__setattr__(self, 'callable_object', callable_object)
        if not isinstance(callable_role, str):
            raise TypeError('CallableRole must be str, got ' + type(callable_role).__name__)
        object.__setattr__(self, 'callable_role', callable_role)
        if not isinstance(tx_group, str):
            raise TypeError('TxGroup must be str, got ' + type(tx_group).__name__)
        object.__setattr__(self, 'tx_group', tx_group)
        if not isinstance(order, int):
            raise TypeError('Order must be int, got ' + type(order).__name__)
        object.__setattr__(self, 'order', order)
        if not isinstance(allowed_injections, tuple):
            raise TypeError('AllowedInjections must be tuple, got ' + type(allowed_injections).__name__)
        object.__setattr__(self, 'allowed_injections', allowed_injections)
        if not isinstance(callable_path, str):
            raise TypeError('CallablePath must be str, got ' + type(callable_path).__name__)
        object.__setattr__(self, 'callable_path', callable_path)

    def __setattr__(self, name, value):
        if name in ('name', 'source_label', 'callable_object', 'callable_role', 'tx_group', 'order', 'allowed_injections', 'callable_path'):
            raise AttributeError('CommitValidator records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('source_label=' + repr(self.source_label))
        pieces.append('callable_object=' + repr(self.callable_object))
        pieces.append('callable_role=' + repr(self.callable_role))
        pieces.append('tx_group=' + repr(self.tx_group))
        pieces.append('order=' + repr(self.order))
        pieces.append('allowed_injections=' + repr(self.allowed_injections))
        pieces.append('callable_path=' + repr(self.callable_path))
        return 'CommitValidator' + '(' + ', '.join(pieces) + ')'
_CommitValidatorSpec.bind_record_class(CommitValidator)

class CommitOrderKey:
    __slots__ = ('name', 'source_label', 'callable_object', 'callable_role', 'tx_group', 'order', 'allowed_injections', 'callable_path')
    __dds_record_spec__ = _CommitOrderKeySpec
    name: str
    source_label: str
    callable_object: object
    callable_role: str
    tx_group: str
    order: int
    allowed_injections: tuple
    callable_path: str

    def __init__(self, *, name: str, source_label: str='', callable_object: object, callable_role: str, tx_group: str='', order: int=0, allowed_injections: tuple=(), callable_path: str):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        if not isinstance(source_label, str):
            raise TypeError('SourceLabel must be str, got ' + type(source_label).__name__)
        object.__setattr__(self, 'source_label', source_label)
        object.__setattr__(self, 'callable_object', callable_object)
        if not isinstance(callable_role, str):
            raise TypeError('CallableRole must be str, got ' + type(callable_role).__name__)
        object.__setattr__(self, 'callable_role', callable_role)
        if not isinstance(tx_group, str):
            raise TypeError('TxGroup must be str, got ' + type(tx_group).__name__)
        object.__setattr__(self, 'tx_group', tx_group)
        if not isinstance(order, int):
            raise TypeError('Order must be int, got ' + type(order).__name__)
        object.__setattr__(self, 'order', order)
        if not isinstance(allowed_injections, tuple):
            raise TypeError('AllowedInjections must be tuple, got ' + type(allowed_injections).__name__)
        object.__setattr__(self, 'allowed_injections', allowed_injections)
        if not isinstance(callable_path, str):
            raise TypeError('CallablePath must be str, got ' + type(callable_path).__name__)
        object.__setattr__(self, 'callable_path', callable_path)

    def __setattr__(self, name, value):
        if name in ('name', 'source_label', 'callable_object', 'callable_role', 'tx_group', 'order', 'allowed_injections', 'callable_path'):
            raise AttributeError('CommitOrderKey records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('source_label=' + repr(self.source_label))
        pieces.append('callable_object=' + repr(self.callable_object))
        pieces.append('callable_role=' + repr(self.callable_role))
        pieces.append('tx_group=' + repr(self.tx_group))
        pieces.append('order=' + repr(self.order))
        pieces.append('allowed_injections=' + repr(self.allowed_injections))
        pieces.append('callable_path=' + repr(self.callable_path))
        return 'CommitOrderKey' + '(' + ', '.join(pieces) + ')'
_CommitOrderKeySpec.bind_record_class(CommitOrderKey)

class HookDeclaration:
    __slots__ = ('name', 'source_label', 'callable_object', 'callable_role', 'tx_group', 'phase', 'order', 'allowed_injections', 'callable_path')
    __dds_record_spec__ = _HookDeclarationSpec
    name: str
    source_label: str
    callable_object: object
    callable_role: str
    tx_group: str
    phase: str
    order: int
    allowed_injections: tuple
    callable_path: str

    def __init__(self, *, name: str, source_label: str='', callable_object: object, callable_role: str, tx_group: str='', phase: str='', order: int=0, allowed_injections: tuple=(), callable_path: str):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        if not isinstance(source_label, str):
            raise TypeError('SourceLabel must be str, got ' + type(source_label).__name__)
        object.__setattr__(self, 'source_label', source_label)
        object.__setattr__(self, 'callable_object', callable_object)
        if not isinstance(callable_role, str):
            raise TypeError('CallableRole must be str, got ' + type(callable_role).__name__)
        object.__setattr__(self, 'callable_role', callable_role)
        if not isinstance(tx_group, str):
            raise TypeError('TxGroup must be str, got ' + type(tx_group).__name__)
        object.__setattr__(self, 'tx_group', tx_group)
        if not isinstance(phase, str):
            raise TypeError('Phase must be str, got ' + type(phase).__name__)
        object.__setattr__(self, 'phase', phase)
        if not isinstance(order, int):
            raise TypeError('Order must be int, got ' + type(order).__name__)
        object.__setattr__(self, 'order', order)
        if not isinstance(allowed_injections, tuple):
            raise TypeError('AllowedInjections must be tuple, got ' + type(allowed_injections).__name__)
        object.__setattr__(self, 'allowed_injections', allowed_injections)
        if not isinstance(callable_path, str):
            raise TypeError('CallablePath must be str, got ' + type(callable_path).__name__)
        object.__setattr__(self, 'callable_path', callable_path)

    def __setattr__(self, name, value):
        if name in ('name', 'source_label', 'callable_object', 'callable_role', 'tx_group', 'phase', 'order', 'allowed_injections', 'callable_path'):
            raise AttributeError('HookDeclaration records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('source_label=' + repr(self.source_label))
        pieces.append('callable_object=' + repr(self.callable_object))
        pieces.append('callable_role=' + repr(self.callable_role))
        pieces.append('tx_group=' + repr(self.tx_group))
        pieces.append('phase=' + repr(self.phase))
        pieces.append('order=' + repr(self.order))
        pieces.append('allowed_injections=' + repr(self.allowed_injections))
        pieces.append('callable_path=' + repr(self.callable_path))
        return 'HookDeclaration' + '(' + ', '.join(pieces) + ')'
_HookDeclarationSpec.bind_record_class(HookDeclaration)

class HookMethodStatement:
    __slots__ = ('class_role', 'name', 'target_port', 'order', 'template', 'callable_path')
    __dds_record_spec__ = _HookMethodStatementSpec
    class_role: str
    name: str
    target_port: object
    order: int
    template: object
    callable_path: str

    def __init__(self, *, class_role: str, name: str, target_port: object, order: int=0, template: object, callable_path: str):
        if not isinstance(class_role, str):
            raise TypeError('ClassRole must be str, got ' + type(class_role).__name__)
        object.__setattr__(self, 'class_role', class_role)
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'target_port', target_port)
        if not isinstance(order, int):
            raise TypeError('Order must be int, got ' + type(order).__name__)
        object.__setattr__(self, 'order', order)
        object.__setattr__(self, 'template', template)
        if not isinstance(callable_path, str):
            raise TypeError('CallablePath must be str, got ' + type(callable_path).__name__)
        object.__setattr__(self, 'callable_path', callable_path)

    def __setattr__(self, name, value):
        if name in ('class_role', 'name', 'target_port', 'order', 'template', 'callable_path'):
            raise AttributeError('HookMethodStatement records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('class_role=' + repr(self.class_role))
        pieces.append('name=' + repr(self.name))
        pieces.append('target_port=' + repr(self.target_port))
        pieces.append('order=' + repr(self.order))
        pieces.append('template=' + repr(self.template))
        pieces.append('callable_path=' + repr(self.callable_path))
        return 'HookMethodStatement' + '(' + ', '.join(pieces) + ')'
_HookMethodStatementSpec.bind_record_class(HookMethodStatement)

class ResourceCleanupStatement:
    __slots__ = ('class_role', 'name', 'target_port', 'order', 'template', 'release_path', 'published_slot')
    __dds_record_spec__ = _ResourceCleanupStatementSpec
    class_role: str
    name: str
    target_port: object
    order: int
    template: object
    release_path: str
    published_slot: str

    def __init__(self, *, class_role: str, name: str, target_port: object, order: int=0, template: object, release_path: str='', published_slot: str=''):
        if not isinstance(class_role, str):
            raise TypeError('ClassRole must be str, got ' + type(class_role).__name__)
        object.__setattr__(self, 'class_role', class_role)
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'target_port', target_port)
        if not isinstance(order, int):
            raise TypeError('Order must be int, got ' + type(order).__name__)
        object.__setattr__(self, 'order', order)
        object.__setattr__(self, 'template', template)
        if not isinstance(release_path, str):
            raise TypeError('ReleasePath must be str, got ' + type(release_path).__name__)
        object.__setattr__(self, 'release_path', release_path)
        if not isinstance(published_slot, str):
            raise TypeError('PublishedSlot must be str, got ' + type(published_slot).__name__)
        object.__setattr__(self, 'published_slot', published_slot)

    def __setattr__(self, name, value):
        if name in ('class_role', 'name', 'target_port', 'order', 'template', 'release_path', 'published_slot'):
            raise AttributeError('ResourceCleanupStatement records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('class_role=' + repr(self.class_role))
        pieces.append('name=' + repr(self.name))
        pieces.append('target_port=' + repr(self.target_port))
        pieces.append('order=' + repr(self.order))
        pieces.append('template=' + repr(self.template))
        pieces.append('release_path=' + repr(self.release_path))
        pieces.append('published_slot=' + repr(self.published_slot))
        return 'ResourceCleanupStatement' + '(' + ', '.join(pieces) + ')'
_ResourceCleanupStatementSpec.bind_record_class(ResourceCleanupStatement)

class OwnedField:
    __slots__ = ('name', 'kind', 'annotation_path', 'defaulted', 'default_value', 'order', 'tx_group', 'release_path', 'resource_policy')
    __dds_record_spec__ = _OwnedFieldSpec
    name: str
    kind: str
    annotation_path: str
    defaulted: bool
    default_value: object
    order: int
    tx_group: str
    release_path: str
    resource_policy: str

    def __init__(self, *, name: str, kind: str, annotation_path: str='', defaulted: bool=False, default_value: object=None, order: int=0, tx_group: str='', release_path: str='', resource_policy: str=''):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        if not isinstance(kind, str):
            raise TypeError('Kind must be str, got ' + type(kind).__name__)
        object.__setattr__(self, 'kind', kind)
        if not isinstance(annotation_path, str):
            raise TypeError('AnnotationPath must be str, got ' + type(annotation_path).__name__)
        object.__setattr__(self, 'annotation_path', annotation_path)
        if not isinstance(defaulted, bool):
            raise TypeError('Defaulted must be bool, got ' + type(defaulted).__name__)
        object.__setattr__(self, 'defaulted', defaulted)
        object.__setattr__(self, 'default_value', default_value)
        if not isinstance(order, int):
            raise TypeError('Order must be int, got ' + type(order).__name__)
        object.__setattr__(self, 'order', order)
        if not isinstance(tx_group, str):
            raise TypeError('TxGroup must be str, got ' + type(tx_group).__name__)
        object.__setattr__(self, 'tx_group', tx_group)
        if not isinstance(release_path, str):
            raise TypeError('ReleasePath must be str, got ' + type(release_path).__name__)
        object.__setattr__(self, 'release_path', release_path)
        if not isinstance(resource_policy, str):
            raise TypeError('ResourcePolicy must be str, got ' + type(resource_policy).__name__)
        object.__setattr__(self, 'resource_policy', resource_policy)

    def __setattr__(self, name, value):
        if name in ('name', 'kind', 'annotation_path', 'defaulted', 'default_value', 'order', 'tx_group', 'release_path', 'resource_policy'):
            raise AttributeError('OwnedField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('kind=' + repr(self.kind))
        pieces.append('annotation_path=' + repr(self.annotation_path))
        pieces.append('defaulted=' + repr(self.defaulted))
        pieces.append('default_value=' + repr(self.default_value))
        pieces.append('order=' + repr(self.order))
        pieces.append('tx_group=' + repr(self.tx_group))
        pieces.append('release_path=' + repr(self.release_path))
        pieces.append('resource_policy=' + repr(self.resource_policy))
        return 'OwnedField' + '(' + ', '.join(pieces) + ')'
_OwnedFieldSpec.bind_record_class(OwnedField)

class BindingField:
    __slots__ = ('name', 'kind', 'annotation_path', 'defaulted', 'default_value', 'order', 'tx_group', 'release_path', 'resource_policy')
    __dds_record_spec__ = _BindingFieldSpec
    name: str
    kind: str
    annotation_path: str
    defaulted: bool
    default_value: object
    order: int
    tx_group: str
    release_path: str
    resource_policy: str

    def __init__(self, *, name: str, kind: str, annotation_path: str='', defaulted: bool=False, default_value: object=None, order: int=0, tx_group: str='', release_path: str='', resource_policy: str=''):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        if not isinstance(kind, str):
            raise TypeError('Kind must be str, got ' + type(kind).__name__)
        object.__setattr__(self, 'kind', kind)
        if not isinstance(annotation_path, str):
            raise TypeError('AnnotationPath must be str, got ' + type(annotation_path).__name__)
        object.__setattr__(self, 'annotation_path', annotation_path)
        if not isinstance(defaulted, bool):
            raise TypeError('Defaulted must be bool, got ' + type(defaulted).__name__)
        object.__setattr__(self, 'defaulted', defaulted)
        object.__setattr__(self, 'default_value', default_value)
        if not isinstance(order, int):
            raise TypeError('Order must be int, got ' + type(order).__name__)
        object.__setattr__(self, 'order', order)
        if not isinstance(tx_group, str):
            raise TypeError('TxGroup must be str, got ' + type(tx_group).__name__)
        object.__setattr__(self, 'tx_group', tx_group)
        if not isinstance(release_path, str):
            raise TypeError('ReleasePath must be str, got ' + type(release_path).__name__)
        object.__setattr__(self, 'release_path', release_path)
        if not isinstance(resource_policy, str):
            raise TypeError('ResourcePolicy must be str, got ' + type(resource_policy).__name__)
        object.__setattr__(self, 'resource_policy', resource_policy)

    def __setattr__(self, name, value):
        if name in ('name', 'kind', 'annotation_path', 'defaulted', 'default_value', 'order', 'tx_group', 'release_path', 'resource_policy'):
            raise AttributeError('BindingField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('kind=' + repr(self.kind))
        pieces.append('annotation_path=' + repr(self.annotation_path))
        pieces.append('defaulted=' + repr(self.defaulted))
        pieces.append('default_value=' + repr(self.default_value))
        pieces.append('order=' + repr(self.order))
        pieces.append('tx_group=' + repr(self.tx_group))
        pieces.append('release_path=' + repr(self.release_path))
        pieces.append('resource_policy=' + repr(self.resource_policy))
        return 'BindingField' + '(' + ', '.join(pieces) + ')'
_BindingFieldSpec.bind_record_class(BindingField)

class InitvarEdge:
    __slots__ = ('consumer', 'initvar_name', 'source_label')
    __dds_record_spec__ = _InitvarEdgeSpec
    consumer: str
    initvar_name: str
    source_label: str

    def __init__(self, *, consumer: str, initvar_name: str, source_label: str=''):
        if not isinstance(consumer, str):
            raise TypeError('Consumer must be str, got ' + type(consumer).__name__)
        object.__setattr__(self, 'consumer', consumer)
        if not isinstance(initvar_name, str):
            raise TypeError('InitVarName must be str, got ' + type(initvar_name).__name__)
        object.__setattr__(self, 'initvar_name', initvar_name)
        if not isinstance(source_label, str):
            raise TypeError('SourceLabel must be str, got ' + type(source_label).__name__)
        object.__setattr__(self, 'source_label', source_label)

    def __setattr__(self, name, value):
        if name in ('consumer', 'initvar_name', 'source_label'):
            raise AttributeError('InitvarEdge records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('consumer=' + repr(self.consumer))
        pieces.append('initvar_name=' + repr(self.initvar_name))
        pieces.append('source_label=' + repr(self.source_label))
        return 'InitvarEdge' + '(' + ', '.join(pieces) + ')'
_InitvarEdgeSpec.bind_record_class(InitvarEdge)

class LateInitvarConsumer:
    __slots__ = ('consumer', 'source_label')
    __dds_record_spec__ = _LateInitvarConsumerSpec
    consumer: str
    source_label: str

    def __init__(self, *, consumer: str, source_label: str=''):
        if not isinstance(consumer, str):
            raise TypeError('Consumer must be str, got ' + type(consumer).__name__)
        object.__setattr__(self, 'consumer', consumer)
        if not isinstance(source_label, str):
            raise TypeError('SourceLabel must be str, got ' + type(source_label).__name__)
        object.__setattr__(self, 'source_label', source_label)

    def __setattr__(self, name, value):
        if name in ('consumer', 'source_label'):
            raise AttributeError('LateInitvarConsumer records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('consumer=' + repr(self.consumer))
        pieces.append('source_label=' + repr(self.source_label))
        return 'LateInitvarConsumer' + '(' + ', '.join(pieces) + ')'
_LateInitvarConsumerSpec.bind_record_class(LateInitvarConsumer)

class RetainedInitVar:
    __slots__ = ('name', 'source_label')
    __dds_record_spec__ = _RetainedInitVarSpec
    name: str
    source_label: str

    def __init__(self, *, name: str, source_label: str=''):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        if not isinstance(source_label, str):
            raise TypeError('SourceLabel must be str, got ' + type(source_label).__name__)
        object.__setattr__(self, 'source_label', source_label)

    def __setattr__(self, name, value):
        if name in ('name', 'source_label'):
            raise AttributeError('RetainedInitVar records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('source_label=' + repr(self.source_label))
        return 'RetainedInitVar' + '(' + ', '.join(pieces) + ')'
_RetainedInitVarSpec.bind_record_class(RetainedInitVar)

class ConstructorOnlyInitVar:
    __slots__ = ('name', 'source_label')
    __dds_record_spec__ = _ConstructorOnlyInitVarSpec
    name: str
    source_label: str

    def __init__(self, *, name: str, source_label: str=''):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        if not isinstance(source_label, str):
            raise TypeError('SourceLabel must be str, got ' + type(source_label).__name__)
        object.__setattr__(self, 'source_label', source_label)

    def __setattr__(self, name, value):
        if name in ('name', 'source_label'):
            raise AttributeError('ConstructorOnlyInitVar records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('source_label=' + repr(self.source_label))
        return 'ConstructorOnlyInitVar' + '(' + ', '.join(pieces) + ')'
_ConstructorOnlyInitVarSpec.bind_record_class(ConstructorOnlyInitVar)

class InitVarField:
    __slots__ = ('name', 'kind', 'annotation_path', 'defaulted', 'default_value', 'order', 'tx_group', 'source_label')
    __dds_record_spec__ = _InitVarFieldSpec
    name: str
    kind: str
    annotation_path: str
    defaulted: bool
    default_value: object
    order: int
    tx_group: str
    source_label: str

    def __init__(self, *, name: str, kind: str, annotation_path: str='', defaulted: bool=False, default_value: object=None, order: int=0, tx_group: str='', source_label: str=''):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        if not isinstance(kind, str):
            raise TypeError('Kind must be str, got ' + type(kind).__name__)
        object.__setattr__(self, 'kind', kind)
        if not isinstance(annotation_path, str):
            raise TypeError('AnnotationPath must be str, got ' + type(annotation_path).__name__)
        object.__setattr__(self, 'annotation_path', annotation_path)
        if not isinstance(defaulted, bool):
            raise TypeError('Defaulted must be bool, got ' + type(defaulted).__name__)
        object.__setattr__(self, 'defaulted', defaulted)
        object.__setattr__(self, 'default_value', default_value)
        if not isinstance(order, int):
            raise TypeError('Order must be int, got ' + type(order).__name__)
        object.__setattr__(self, 'order', order)
        if not isinstance(tx_group, str):
            raise TypeError('TxGroup must be str, got ' + type(tx_group).__name__)
        object.__setattr__(self, 'tx_group', tx_group)
        if not isinstance(source_label, str):
            raise TypeError('SourceLabel must be str, got ' + type(source_label).__name__)
        object.__setattr__(self, 'source_label', source_label)

    def __setattr__(self, name, value):
        if name in ('name', 'kind', 'annotation_path', 'defaulted', 'default_value', 'order', 'tx_group', 'source_label'):
            raise AttributeError('InitVarField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('kind=' + repr(self.kind))
        pieces.append('annotation_path=' + repr(self.annotation_path))
        pieces.append('defaulted=' + repr(self.defaulted))
        pieces.append('default_value=' + repr(self.default_value))
        pieces.append('order=' + repr(self.order))
        pieces.append('tx_group=' + repr(self.tx_group))
        pieces.append('source_label=' + repr(self.source_label))
        return 'InitVarField' + '(' + ', '.join(pieces) + ')'
_InitVarFieldSpec.bind_record_class(InitVarField)
FieldsCollection = RuntimeCollection('Fields', _FieldSpecsUnion, allows_multiple=True, identity=_NameProperty)
TxGroupsCollection = RuntimeCollection('TxGroups', _TxGroupRecordSpec, allows_multiple=True, identity=_TxGroupProperty)
ClassInputsCollection = RuntimeCollection('ClassInputs', _ClassInputSpec, allows_multiple=False, identity=_ClassNameProperty)
ClassNamesCollection = RuntimeCollection('ClassNames', _ClassNameContributionSpec, allows_multiple=True, identity=_ClassRoleProperty)
ClassComponentsCollection = RuntimeCollection('ClassComponents', _ClassComponentSpec, allows_multiple=True, identity=(_ClassRoleProperty, _NameProperty))
ModuleComponentsCollection = RuntimeCollection('ModuleComponents', _ModuleComponentSpec, allows_multiple=True, identity=_NameProperty)
SlotItemsCollection = RuntimeCollection('SlotItems', _SlotItemSpec, allows_multiple=True, identity=(_ClassRoleProperty, _SlotNameProperty))
InitParamsCollection = RuntimeCollection('InitParams', _InitParamSpec, allows_multiple=True, identity=(_ClassRoleProperty, _NameProperty))
StateCtorArgsCollection = RuntimeCollection('StateCtorArgs', _StateCtorArgSpec, allows_multiple=True, identity=(_ClassRoleProperty, _NameProperty))
OperationContributionsCollection = RuntimeCollection('OperationContributions', _OperationContributionSpec, allows_multiple=True, identity=(_ClassRoleProperty, _NameProperty, _PhaseProperty))
MethodStatementsCollection = RuntimeCollection('MethodStatements', _MethodStatementSpec, allows_multiple=True, identity=(_ClassRoleProperty, _NameProperty))
CallableDeclarationsCollection = RuntimeCollection('CallableDeclarations', _CallableDeclarationSpec, allows_multiple=True, identity=_NameProperty)
CallableSpecsCollection = RuntimeCollection('CallableSpecs', _CallableSpecSpec, allows_multiple=True, identity=_NameProperty)
CallableParamsCollection = RuntimeCollection('CallableParams', _CallableParamSpec, allows_multiple=True, identity=(_CallableNameProperty, _ParamNameProperty))
CallableInjectionsCollection = RuntimeCollection('CallableInjections', _CallableInjectionSpec, allows_multiple=True, identity=(_CallableNameProperty, _ParamNameProperty))
CommitValidatorsCollection = RuntimeCollection('CommitValidators', _CommitValidatorSpec, allows_multiple=True, identity=_TxGroupProperty)
CommitOrderKeysCollection = RuntimeCollection('CommitOrderKeys', _CommitOrderKeySpec, allows_multiple=True, identity=_TxGroupProperty)
HookDeclarationsCollection = RuntimeCollection('HookDeclarations', _HookDeclarationSpec, allows_multiple=True, identity=(_PhaseProperty, _TxGroupProperty, _NameProperty))
HookMethodStatementsCollection = RuntimeCollection('HookMethodStatements', _HookMethodStatementSpec, allows_multiple=True, identity=(_ClassRoleProperty, _NameProperty))
ResourceCleanupStatementsCollection = RuntimeCollection('ResourceCleanupStatements', _ResourceCleanupStatementSpec, allows_multiple=True, identity=(_ClassRoleProperty, _NameProperty))
InitvarEdgesCollection = RuntimeCollection('InitvarEdges', _InitvarEdgeSpec, allows_multiple=True, identity=(_ConsumerProperty, _InitVarNameProperty))
LateInitvarConsumersCollection = RuntimeCollection('LateInitvarConsumers', _LateInitvarConsumerSpec, allows_multiple=True, identity=_ConsumerProperty)
RetainedInitVarsCollection = RuntimeCollection('RetainedInitVars', _RetainedInitVarSpec, allows_multiple=True, identity=_NameProperty)
ConstructorOnlyInitVarsCollection = RuntimeCollection('ConstructorOnlyInitVars', _ConstructorOnlyInitVarSpec, allows_multiple=True, identity=_NameProperty)
ModuleBodyPort = RuntimePort('Module.body', allows_multiple=True)
ClassNamePort = RuntimePort('Class.name', allows_multiple=False)
ClassBodyPort = RuntimePort('Class.body', allows_multiple=True)
SlotsItemsPort = RuntimePort('Slots.items', allows_multiple=True)
InitParamsPort = RuntimePort('Init.params', allows_multiple=True)
InitBodyPort = RuntimePort('Init.body', allows_multiple=True)
StateCtorArgsPort = RuntimePort('StateCtor.args', allows_multiple=True)
MethodBodyPort = RuntimePort('Method.body', allows_multiple=True)
_RUNTIME_SPEC = RuntimeContainerSpec(collections=(FieldsCollection, TxGroupsCollection, ClassInputsCollection, ClassNamesCollection, ClassComponentsCollection, ModuleComponentsCollection, SlotItemsCollection, InitParamsCollection, StateCtorArgsCollection, OperationContributionsCollection, MethodStatementsCollection, CallableDeclarationsCollection, CallableSpecsCollection, CallableParamsCollection, CallableInjectionsCollection, CommitValidatorsCollection, CommitOrderKeysCollection, HookDeclarationsCollection, HookMethodStatementsCollection, ResourceCleanupStatementsCollection, InitvarEdgesCollection, LateInitvarConsumersCollection, RetainedInitVarsCollection, ConstructorOnlyInitVarsCollection), computed_collections=(), ports=(ModuleBodyPort, ClassNamePort, ClassBodyPort, SlotsItemsPort, InitParamsPort, InitBodyPort, StateCtorArgsPort, MethodBodyPort), port_index=RuntimePortIndex(target=_TargetPortProperty, order=_OrderProperty))

class PropertyTemplateMatcher:

    def __init__(self):
        self._cache = {}

    def resolve(self, field_record):
        records = (field_record,)
        values = (getattr(field_record, 'kind', NOT_PROVIDED),)
        try:
            cached = self._cache.get(values, NOT_PROVIDED)
        except TypeError:
            cached = NOT_PROVIDED
            cache_key = None
        else:
            cache_key = values
        if cached is not NOT_PROVIDED:
            return self._finish(None, cached, records, values)
        if values[0:1] == ('managed',):
            return self._finish(cache_key, (astichi_template(from_astichi_code('astichi_comment("property template: managed value")\n\n@property\ndef field_name__astichi_arg__(self):\n    state = self._state\n    if state.astichi_ref(external=working_slot) is not _NO_WORKING_VALUE:\n        return state.astichi_ref(external=working_slot)\n    return state.astichi_ref(external=current_slot)\n\n@field_name__astichi_arg__.setter\ndef field_name__astichi_arg__(self, value):\n    self._state.astichi_ref(external=working_slot)._ = value', keep_names=('_NO_WORKING_VALUE',)), arg_names=from_astichi_code('{"field_name": astichi_pass(record, outer_bind=True).field_name}'), bind=from_astichi_code('{\n    "current_slot": (\n        astichi_pass(record, outer_bind=True).current_slot\n    ),\n    "working_slot": (\n        astichi_pass(record, outer_bind=True).working_slot\n    ),\n}')), 'managed-property', 1.0), records, values)
        return self._finish(cache_key, (astichi_template(from_astichi_code('astichi_comment("property template: const value")\n\n@property\ndef field_name__astichi_arg__(self):\n    return self._state.astichi_ref(external=published_slot)'), arg_names=from_astichi_code('{"field_name": astichi_pass(record, outer_bind=True).field_name}'), bind=from_astichi_code('{\n    "published_slot": (\n        astichi_pass(record, outer_bind=True).published_slot\n    )\n}')), None, 0.0), records, values)

    def _finish(self, cache_key, selection, records, values):
        if cache_key is not None:
            self._cache[cache_key] = selection
        if selection is None:
            return None
        resource, rule, score = selection
        return MatcherResult(resource=resource, rule=rule, score=score, records=records, values=values)

    def sequence(self, *record_sequences):
        if len(record_sequences) != 1:
            raise ValueError('wrong number of record sequences')
        for records in product(*record_sequences):
            result = self.resolve(*records)
            if result is not None:
                yield result

def run_operation_contribution_component(builder):
    for source in builder.records(OperationContributionsCollection):
        record = ClassComponent(class_role=source.class_role, name=source.name, target_port=source.target_port, order=source.order, template=source.template, field_name=source.field_name, current_slot=source.current_slot, working_slot=source.working_slot, published_slot=source.published_slot)
        builder.write(ClassComponentsCollection, record, policy=AddIfAbsent)

def run_property_contribution(builder):
    snapshot = builder._snapshot()
    for source in snapshot.matchers.PropertyTemplate.sequence():
        record = OperationContribution(class_role='main_facade', name=source.records[0].name, phase='property', operation_kind='get', target_port=ClassBodyPort.of('main_facade'), order=property_order_for(source), template=source.resource, field_name=source.records[0].name, current_slot=current_slot_for_result(source), working_slot=working_slot_for_result(source), published_slot=published_slot_for_result(source))
        builder.write(OperationContributionsCollection, record, policy=AddIfAbsent)

def run_build_tx_groups(builder):
    ctx = DDSOperationContext(builder, 'BuildTxGroups', ordered_inputs={})
    seen = set()
    next_index = 0
    for field in sorted(ctx.records(FieldsCollection), key=lambda record: (record.order, ctx.write_order(record))):
        if field.kind != 'managed':
            continue
        if field.tx_group in seen:
            continue
        seen.add(field.tx_group)
        ctx.write(TxGroupsCollection, TxGroupRecord(tx_group=field.tx_group, tx_index=next_index), policy=AddIfAbsent)
        next_index += 1

def run_build_lifecycle_scaffold(builder):
    ctx = DDSOperationContext(builder, 'BuildLifecycleScaffold', ordered_inputs={})
    module_sentinel_template = from_astichi_code('_NO_WORKING_VALUE = object()')
    slots_template = from_astichi_code('__slots__ = (*astichi_hole(items),)', keep_names=('__slots__',))
    init_template = from_astichi_code('def __init__(self, params__astichi_param_hole__):\n    astichi_hole(body)', keep_names=('self',))
    init_param_template = from_astichi_code('def astichi_params(*, field_name__astichi_arg__):\n    pass')
    defaulted_param_template = from_astichi_code('def astichi_params(\n    *,\n    field_name__astichi_arg__=astichi_bind_external(default_value),\n):\n    pass')
    annotated_param_template = from_astichi_code('def astichi_params(\n    *,\n    field_name__astichi_arg__: astichi_ref(external=annotation_path),\n):\n    pass')
    annotated_defaulted_param_template = from_astichi_code('def astichi_params(\n    *,\n    field_name__astichi_arg__: astichi_ref(external=annotation_path)\n    = astichi_bind_external(default_value),\n):\n    pass')
    slot_item_template = from_astichi_code('astichi_bind_external(slot_name)\nslot_name')
    current_assign_template = from_astichi_code('astichi_import(self)\nself.astichi_ref(external=target_path)._ = astichi_pass(source_name, outer_bind=True)')
    working_assign_template = from_astichi_code('astichi_import(self)\nself.astichi_ref(external=target_path)._ = _NO_WORKING_VALUE', keep_names=('_NO_WORKING_VALUE',))
    state_ctor_template = from_astichi_code('self._state = state_class__astichi_arg__(astichi_hole(state_ctor_args))', keep_names=('self',))
    state_ctor_arg_template = from_astichi_code('astichi_funcargs(field_name__astichi_arg__=field_name__astichi_arg__)')
    class_inputs = tuple(ctx.records(ClassInputsCollection))
    if len(class_inputs) != 1:
        raise ValueError('expected exactly one lifecycle class input')
    class_input = class_inputs[0]
    fields = sorted(ctx.records(FieldsCollection), key=lambda record: (record.order, ctx.write_order(record)))
    state_role = 'state'
    facade_role = 'main_facade'
    ctx.write(ModuleComponentsCollection, ModuleComponent(name='_NO_WORKING_VALUE', target_port=ModuleBodyPort.of('runtime'), order=-100, template=module_sentinel_template), policy=AddIfAbsent)
    ctx.write(ClassNamesCollection, ClassNameContribution(class_role=state_role, target_port=ClassNamePort.of(state_role), order=0, runtime_value=class_input.state_class_name), policy=AddIfAbsent)
    ctx.write(ClassNamesCollection, ClassNameContribution(class_role=facade_role, target_port=ClassNamePort.of(facade_role), order=10, runtime_value=class_input.class_name), policy=AddIfAbsent)
    for role in (state_role, facade_role):
        ctx.write(ClassComponentsCollection, ClassComponent(class_role=role, name='__slots__', target_port=ClassBodyPort.of(role), order=-10, template=slots_template), policy=AddIfAbsent)
        ctx.write(ClassComponentsCollection, ClassComponent(class_role=role, name='__init__', target_port=ClassBodyPort.of(role), order=0, template=init_template), policy=AddIfAbsent)
    ctx.write(SlotItemsCollection, SlotItem(class_role=facade_role, name='_state', target_port=SlotsItemsPort.of((facade_role, '__slots__')), order=0, template=slot_item_template, slot_name='_state'), policy=AddIfAbsent)
    ctx.write(ClassComponentsCollection, ClassComponent(class_role=facade_role, name='state_ctor', target_port=InitBodyPort.of((facade_role, '__init__')), order=0, template=state_ctor_template, state_class_name=class_input.state_class_name), policy=AddIfAbsent)
    for field in fields:
        if field.annotation_path and field.defaulted:
            param_template = annotated_defaulted_param_template
        elif field.annotation_path:
            param_template = annotated_param_template
        elif field.defaulted:
            param_template = defaulted_param_template
        else:
            param_template = init_param_template
        ctx.write(InitParamsCollection, InitParam(class_role=state_role, name=field.name, target_port=InitParamsPort.of((state_role, '__init__')), order=field.order, template=param_template, annotation_path=field.annotation_path, defaulted=field.defaulted, default_value=field.default_value), policy=AddIfAbsent)
        ctx.write(InitParamsCollection, InitParam(class_role=facade_role, name=field.name, target_port=InitParamsPort.of((facade_role, '__init__')), order=field.order, template=param_template, annotation_path=field.annotation_path, defaulted=field.defaulted, default_value=field.default_value), policy=AddIfAbsent)
        ctx.write(StateCtorArgsCollection, StateCtorArg(class_role=facade_role, name=field.name, target_port=StateCtorArgsPort.of((facade_role, 'state_ctor')), order=field.order, template=state_ctor_arg_template), policy=AddIfAbsent)
        if field.kind == 'managed':
            current_slot = f'_{field.name}_current'
            working_slot = f'_{field.name}_working'
            slot_specs = ((current_slot, field.order * 2), (working_slot, field.order * 2 + 1))
            assignments = ((f'{field.name}_current', current_slot, field.name, current_assign_template, field.order * 2), (f'{field.name}_working', working_slot, '', working_assign_template, field.order * 2 + 1))
        else:
            published_slot = f'_{field.name}_value'
            slot_specs = ((published_slot, field.order * 2),)
            assignments = ((f'{field.name}_value', published_slot, field.name, current_assign_template, field.order * 2),)
        for slot_name, slot_order in slot_specs:
            ctx.write(SlotItemsCollection, SlotItem(class_role=state_role, name=slot_name, target_port=SlotsItemsPort.of((state_role, '__slots__')), order=slot_order, template=slot_item_template, slot_name=slot_name), policy=AddIfAbsent)
        for assign_name, target, source, assign_template, assign_order in assignments:
            ctx.write(ClassComponentsCollection, ClassComponent(class_role=state_role, name=assign_name, target_port=InitBodyPort.of((state_role, '__init__')), order=assign_order, template=assign_template, source_name=source, target_name=target), policy=AddIfAbsent)

def run_build_transaction_methods(builder):
    ctx = DDSOperationContext(builder, 'BuildTransactionMethods', ordered_inputs={})
    commit_template = from_astichi_code('def commit(self):\n    state = self._state\n    astichi_hole(body)', keep_names=('self',))
    rollback_template = from_astichi_code('def rollback(self):\n    state = self._state\n    astichi_hole(body)', keep_names=('self',))
    commit_statement_template = from_astichi_code('if astichi_pass(state, outer_bind=True).astichi_ref(external=working_slot) is not _NO_WORKING_VALUE:\n    astichi_pass(state, outer_bind=True).astichi_ref(external=current_slot)._ = astichi_pass(state, outer_bind=True).astichi_ref(external=working_slot)\n    astichi_pass(state, outer_bind=True).astichi_ref(external=working_slot)._ = _NO_WORKING_VALUE', keep_names=('_NO_WORKING_VALUE',))
    rollback_statement_template = from_astichi_code('astichi_pass(state, outer_bind=True).astichi_ref(external=working_slot)._ = _NO_WORKING_VALUE', keep_names=('_NO_WORKING_VALUE',))
    managed_fields = [field for field in sorted(ctx.records(FieldsCollection), key=lambda record: (record.order, ctx.write_order(record))) if field.kind == 'managed']
    if not managed_fields:
        return
    facade_role = 'main_facade'
    ctx.write(ClassComponentsCollection, ClassComponent(class_role=facade_role, name='commit', target_port=ClassBodyPort.of(facade_role), order=1000, template=commit_template), policy=AddIfAbsent)
    ctx.write(ClassComponentsCollection, ClassComponent(class_role=facade_role, name='rollback', target_port=ClassBodyPort.of(facade_role), order=1010, template=rollback_template), policy=AddIfAbsent)
    for field in managed_fields:
        current_slot = f'_{field.name}_current'
        working_slot = f'_{field.name}_working'
        ctx.write(MethodStatementsCollection, MethodStatement(class_role=facade_role, name=f'commit_{field.name}', target_port=MethodBodyPort.of((facade_role, 'commit')), order=field.order, template=commit_statement_template, current_slot=current_slot, working_slot=working_slot), policy=AddIfAbsent)
        ctx.write(MethodStatementsCollection, MethodStatement(class_role=facade_role, name=f'rollback_{field.name}', target_port=MethodBodyPort.of((facade_role, 'rollback')), order=field.order, template=rollback_statement_template, current_slot=current_slot, working_slot=working_slot), policy=AddIfAbsent)

def run_build_special_callable_declarations(builder):
    ctx = DDSOperationContext(builder, 'BuildSpecialCallableDeclarations', ordered_inputs={})
    for declaration in (*ctx.records(CommitValidatorsCollection), *ctx.records(CommitOrderKeysCollection), *ctx.records(HookDeclarationsCollection)):
        ctx.write(CallableDeclarationsCollection, CallableDeclaration(name=declaration.name, source_label=declaration.source_label, callable_object=declaration.callable_object, callable_role=declaration.callable_role, allowed_injections=declaration.allowed_injections), policy=RejectDuplicate)

def run_produce_callable_facts(builder):
    ctx = DDSOperationContext(builder, 'ProduceCallableFacts', ordered_inputs={})
    for declaration in ctx.records(CallableDeclarationsCollection):
        result = analyze_callable(name=declaration.name, source_label=declaration.source_label, role=declaration.callable_role, callable_obj=declaration.callable_object, allowed_injections=declaration.allowed_injections)
        ctx.write(CallableSpecsCollection, CallableSpec(**result.spec), policy=ReplaceExisting)
        for param in result.params:
            ctx.write(CallableParamsCollection, CallableParam(**param), policy=RejectDuplicate)
        for injection in result.injections:
            ctx.write(CallableInjectionsCollection, CallableInjection(**injection), policy=RejectDuplicate)

def run_build_hook_method_statements(builder):
    ctx = DDSOperationContext(builder, 'BuildHookMethodStatements', ordered_inputs={})
    call_template = from_astichi_code('astichi_ref(external=callable_path)(current=self)', keep_names=('self',))
    for validator in ctx.records(CommitValidatorsCollection):
        ctx.write(HookMethodStatementsCollection, HookMethodStatement(class_role='main_facade', name=f'validate_{validator.tx_group}', target_port=MethodBodyPort.of(('main_facade', 'commit')), order=-500 + validator.order, template=call_template, callable_path=validator.callable_path), policy=AddIfAbsent)
    for hook in ctx.records(HookDeclarationsCollection):
        if hook.callable_role == 'before_commit':
            method_name = 'commit'
            offset = -1000
        elif hook.callable_role == 'after_commit':
            method_name = 'commit'
            offset = 500
        elif hook.callable_role == 'after_rollback':
            method_name = 'rollback'
            offset = 500
        else:
            continue
        ctx.write(HookMethodStatementsCollection, HookMethodStatement(class_role='main_facade', name=f'{hook.callable_role}_{hook.name}', target_port=MethodBodyPort.of(('main_facade', method_name)), order=offset + hook.order, template=call_template, callable_path=hook.callable_path), policy=AddIfAbsent)

def run_build_resource_cleanup_methods(builder):
    ctx = DDSOperationContext(builder, 'BuildResourceCleanupMethods', ordered_inputs={})
    close_template = from_astichi_code('def close(self):\n    state = self._state\n    astichi_hole(body)', keep_names=('self',))
    cleanup_template = from_astichi_code('value = astichi_pass(state, outer_bind=True).astichi_ref(external=published_slot)\nif value is not None:\n    astichi_ref(external=release_path)(value)')
    resource_fields = [field for field in ctx.records(FieldsCollection) if field.kind in ('owned', 'binding')]
    for field in resource_fields:
        if field.resource_policy not in ('owned_scalar', 'binding_scalar'):
            raise TypeError(f'unsupported resource policy {field.resource_policy!r} for field {field.name!r}')
    cleanup_fields = [field for field in resource_fields if field.release_path]
    if not cleanup_fields:
        return
    ctx.write(ClassComponentsCollection, ClassComponent(class_role='main_facade', name='close', target_port=ClassBodyPort.of('main_facade'), order=1020, template=close_template), policy=AddIfAbsent)
    for field in cleanup_fields:
        ctx.write(ResourceCleanupStatementsCollection, ResourceCleanupStatement(class_role='main_facade', name=f'close_{field.name}', target_port=MethodBodyPort.of(('main_facade', 'close')), order=field.order, template=cleanup_template, release_path=field.release_path, published_slot=f'_{field.name}_value'), policy=AddIfAbsent)

def run_build_initvar_edges(builder):
    ctx = DDSOperationContext(builder, 'BuildInitvarEdges', ordered_inputs={})
    initvars_by_name = {field.name: field for field in ctx.records(FieldsCollection) if field.kind == 'initvar'}
    specs_by_name = {spec.name: spec for spec in ctx.records(CallableSpecsCollection)}
    used_initvars = set()
    late_roles = {'commit_validator', 'commit_order_key', 'before_commit', 'after_commit', 'after_rollback'}
    for injection in ctx.records(CallableInjectionsCollection):
        if injection.injection_kind != 'initvar':
            continue
        spec = specs_by_name.get(injection.callable_name)
        initvar = initvars_by_name.get(injection.param_name)
        if initvar is None:
            raise TypeError(f'unknown lifecycle initvar {injection.param_name!r} requested by callable {injection.callable_name!r}')
        used_initvars.add(injection.param_name)
        source_label = spec.source_label if spec is not None else injection.callable_name
        ctx.write(InitvarEdgesCollection, InitvarEdge(consumer=injection.callable_name, initvar_name=injection.param_name, source_label=source_label), policy=AddIfAbsent)
        if spec is not None and spec.callable_role in late_roles:
            ctx.write(LateInitvarConsumersCollection, LateInitvarConsumer(consumer=injection.callable_name, source_label=source_label), policy=AddIfAbsent)
    unused = [field for field in sorted(initvars_by_name.values(), key=lambda record: (record.order, ctx.write_order(record))) if field.name not in used_initvars]
    if unused:
        names = ', '.join((repr(field.name) for field in unused))
        raise TypeError('unused lifecycle initvar declarations: ' + names)

def run_build_retained_init_vars(builder):
    ctx = DDSOperationContext(builder, 'BuildRetainedInitVars', ordered_inputs={})
    roots = [record.consumer for record in ctx.records(LateInitvarConsumersCollection)]
    edges_by_consumer = {}
    for edge in ctx.records(InitvarEdgesCollection):
        edges_by_consumer.setdefault(edge.consumer, []).append(edge)
    seen_consumers = set()
    seen_initvars = set()
    queue = list(roots)
    while queue:
        consumer = queue.pop(0)
        if consumer in seen_consumers:
            continue
        seen_consumers.add(consumer)
        for edge in edges_by_consumer.get(consumer, ()):
            initvar_name = edge.initvar_name
            if initvar_name in seen_initvars:
                continue
            seen_initvars.add(initvar_name)
            ctx.write(RetainedInitVarsCollection, RetainedInitVar(name=initvar_name, source_label=edge.source_label), policy=AddIfAbsent)
            queue.append(initvar_name)

def run_build_constructor_only_init_vars(builder):
    ctx = DDSOperationContext(builder, 'BuildConstructorOnlyInitVars', ordered_inputs={})
    retained_names = {record.name for record in ctx.records(RetainedInitVarsCollection)}
    for field in sorted(ctx.records(FieldsCollection), key=lambda record: (record.order, ctx.write_order(record))):
        if field.kind != 'initvar':
            continue
        if field.name in retained_names:
            continue
        ctx.write(ConstructorOnlyInitVarsCollection, ConstructorOnlyInitVar(name=field.name, source_label=getattr(field, 'source_label', '')), policy=AddIfAbsent)

def run_operations(builder):
    run_build_tx_groups(builder)
    run_build_lifecycle_scaffold(builder)
    run_operation_contribution_component(builder)
    run_property_contribution(builder)
    run_build_transaction_methods(builder)
    run_build_special_callable_declarations(builder)
    run_produce_callable_facts(builder)
    run_build_hook_method_statements(builder)
    run_build_resource_cleanup_methods(builder)
    run_build_initvar_edges(builder)
    run_build_retained_init_vars(builder)
    run_build_constructor_only_init_vars(builder)
    return builder

def build_container(builder):
    run_operations(builder)
    return builder.freeze()

class _GeneratedMatcherNamespace:

    def __init__(self, container):
        self.PropertyTemplate = _ContainerPropertyTemplateMatcher(container)

class _ContainerPropertyTemplateMatcher:

    def __init__(self, container):
        self._container = container
        self._runtime = PropertyTemplateMatcher()

    def resolve(self, *records):
        return self._runtime.resolve(*records)

    def sequence(self):
        yield from self._runtime.sequence(self._container.Fields.sequence())

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
