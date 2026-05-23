from yidl.generation.data_def_sys import AddIfAbsent, AssemblyDiagnosticError, DDSContainerBuilder, DDSOperationContext, NOT_PROVIDED, REQUIRED, RejectDuplicate, ReplaceExisting, RuntimeCollection, RuntimeComputedCollection, RuntimeContainerSpec, RuntimePort, RuntimePortIndex, RuntimeProperty, RuntimeRecord, RuntimeUnion
from yidl.generation.lifecycle_facts import analyze_callable
_NameProperty = RuntimeProperty('Name', str, default=REQUIRED, storage_name='name')
_KindProperty = RuntimeProperty('Kind', str, default=REQUIRED, storage_name='kind')
_AnnotationPathProperty = RuntimeProperty('AnnotationPath', str, default='', storage_name='annotation_path')
_DefaultedProperty = RuntimeProperty('Defaulted', bool, default=False, storage_name='defaulted')
_DefaultValueProperty = RuntimeProperty('DefaultValue', object, default=None, storage_name='default_value')
_OrderProperty = RuntimeProperty('Order', int, default=0, storage_name='order')
_TxKeyProperty = RuntimeProperty('TxKey', str, default='', storage_name='tx_key')
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
_ManagedFieldSpec = RuntimeRecord('ManagedField', (_NameProperty, _KindProperty, _AnnotationPathProperty, _DefaultedProperty, _DefaultValueProperty, _OrderProperty, _TxKeyProperty))
_ConstFieldSpec = RuntimeRecord('ConstField', (_NameProperty, _KindProperty, _AnnotationPathProperty, _DefaultedProperty, _DefaultValueProperty, _OrderProperty, _TxKeyProperty))
_CallableDeclarationSpec = RuntimeRecord('CallableDeclaration', (_NameProperty, _SourceLabelProperty, _CallableObjectProperty, _CallableRoleProperty, _AllowedInjectionsProperty))
_CallableSpecSpec = RuntimeRecord('CallableSpec', (_NameProperty, _SourceLabelProperty, _CallableRoleProperty, _AcceptsVarArgsProperty, _AcceptsVarKwargsProperty))
_CallableParamSpec = RuntimeRecord('CallableParam', (_CallableNameProperty, _ParamNameProperty, _ParamKindProperty, _ParamOrderProperty))
_CallableInjectionSpec = RuntimeRecord('CallableInjection', (_CallableNameProperty, _ParamNameProperty, _InjectionKindProperty, _RequiredProperty))
_FieldSpecsUnion = RuntimeUnion('FieldSpecs', (_ManagedFieldSpec, _ConstFieldSpec))

class ManagedField:
    __slots__ = ('name', 'kind', 'annotation_path', 'defaulted', 'default_value', 'order', 'tx_key')
    __dds_record_spec__ = _ManagedFieldSpec
    name: str
    kind: str
    annotation_path: str
    defaulted: bool
    default_value: object
    order: int
    tx_key: str

    def __init__(self, *, name: str, kind: str, annotation_path: str='', defaulted: bool=False, default_value: object=None, order: int=0, tx_key: str=''):
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
        if not isinstance(tx_key, str):
            raise TypeError('TxKey must be str, got ' + type(tx_key).__name__)
        object.__setattr__(self, 'tx_key', tx_key)

    def __setattr__(self, name, value):
        if name in ('name', 'kind', 'annotation_path', 'defaulted', 'default_value', 'order', 'tx_key'):
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
        pieces.append('tx_key=' + repr(self.tx_key))
        return 'ManagedField' + '(' + ', '.join(pieces) + ')'
_ManagedFieldSpec.bind_record_class(ManagedField)

class ConstField:
    __slots__ = ('name', 'kind', 'annotation_path', 'defaulted', 'default_value', 'order', 'tx_key')
    __dds_record_spec__ = _ConstFieldSpec
    name: str
    kind: str
    annotation_path: str
    defaulted: bool
    default_value: object
    order: int
    tx_key: str

    def __init__(self, *, name: str, kind: str, annotation_path: str='', defaulted: bool=False, default_value: object=None, order: int=0, tx_key: str=''):
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
        if not isinstance(tx_key, str):
            raise TypeError('TxKey must be str, got ' + type(tx_key).__name__)
        object.__setattr__(self, 'tx_key', tx_key)

    def __setattr__(self, name, value):
        if name in ('name', 'kind', 'annotation_path', 'defaulted', 'default_value', 'order', 'tx_key'):
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
        pieces.append('tx_key=' + repr(self.tx_key))
        return 'ConstField' + '(' + ', '.join(pieces) + ')'
_ConstFieldSpec.bind_record_class(ConstField)

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
FieldsCollection = RuntimeCollection('Fields', _FieldSpecsUnion, allows_multiple=True, identity=_NameProperty)
CallableDeclarationsCollection = RuntimeCollection('CallableDeclarations', _CallableDeclarationSpec, allows_multiple=True, identity=_NameProperty)
CallableSpecsCollection = RuntimeCollection('CallableSpecs', _CallableSpecSpec, allows_multiple=True, identity=_NameProperty)
CallableParamsCollection = RuntimeCollection('CallableParams', _CallableParamSpec, allows_multiple=True, identity=(_CallableNameProperty, _ParamNameProperty))
CallableInjectionsCollection = RuntimeCollection('CallableInjections', _CallableInjectionSpec, allows_multiple=True, identity=(_CallableNameProperty, _ParamNameProperty))
_RUNTIME_SPEC = RuntimeContainerSpec(collections=(FieldsCollection, CallableDeclarationsCollection, CallableSpecsCollection, CallableParamsCollection, CallableInjectionsCollection), computed_collections=(), ports=(), port_index=None)

def run_produce_callable_facts(builder):
    ctx = DDSOperationContext(builder, 'ProduceCallableFacts', ordered_inputs={})
    for declaration in ctx.records(CallableDeclarationsCollection):
        result = analyze_callable(name=declaration.name, source_label=declaration.source_label, role=declaration.callable_role, callable_obj=declaration.callable_object, allowed_injections=declaration.allowed_injections)
        ctx.write(CallableSpecsCollection, CallableSpec(**result.spec), policy=ReplaceExisting)
        for param in result.params:
            ctx.write(CallableParamsCollection, CallableParam(**param), policy=RejectDuplicate)
        for injection in result.injections:
            ctx.write(CallableInjectionsCollection, CallableInjection(**injection), policy=RejectDuplicate)

def run_operations(builder):
    run_produce_callable_facts(builder)
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
