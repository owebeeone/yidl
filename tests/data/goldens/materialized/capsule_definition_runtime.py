from itertools import product
from yidl.generation.data_def_sys import AddIfAbsent, DDSContainerBuilder, MatcherResult, NOT_PROVIDED, REQUIRED, RejectDuplicate, ReplaceExisting, RuntimeCollection, RuntimeComputedCollection, RuntimeContainerSpec, RuntimePort, RuntimePortIndex, RuntimeProperty, RuntimeRecord, RuntimeUnion, from_astichi_code
_NameProperty = RuntimeProperty('Name', str, default=REQUIRED, storage_name='name')
_InitProperty = RuntimeProperty('Init', bool, default=True, storage_name='init')
_KindProperty = RuntimeProperty('Kind', str, default='plain', storage_name='kind')
_OrderProperty = RuntimeProperty('Order', int, default=0, storage_name='order')
_TargetPortProperty = RuntimeProperty('TargetPort', object, default=REQUIRED, storage_name='target_port')
_TemplateProperty = RuntimeProperty('Template', object, default=REQUIRED, storage_name='template')
_FieldInputSpec = RuntimeRecord('FieldInput', (_NameProperty, _InitProperty, _KindProperty, _OrderProperty))
_InitComponentSpec = RuntimeRecord('InitComponent', (_NameProperty, _TargetPortProperty, _OrderProperty, _TemplateProperty))
_GetterSpec = RuntimeRecord('Getter', (_NameProperty, _TargetPortProperty, _OrderProperty, _TemplateProperty))

class FieldInput:
    __slots__ = ('name', 'init', 'kind', 'order')
    __dds_record_spec__ = _FieldInputSpec
    name: str
    init: bool
    kind: str
    order: int

    def __init__(self, *, name: str, init: bool=True, kind: str='plain', order: int=0):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        if not isinstance(init, bool):
            raise TypeError('Init must be bool, got ' + type(init).__name__)
        object.__setattr__(self, 'init', init)
        if not isinstance(kind, str):
            raise TypeError('Kind must be str, got ' + type(kind).__name__)
        object.__setattr__(self, 'kind', kind)
        if not isinstance(order, int):
            raise TypeError('Order must be int, got ' + type(order).__name__)
        object.__setattr__(self, 'order', order)

    def __setattr__(self, name, value):
        if name in ('name', 'init', 'kind', 'order'):
            raise AttributeError('FieldInput records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('init=' + repr(self.init))
        pieces.append('kind=' + repr(self.kind))
        pieces.append('order=' + repr(self.order))
        return 'FieldInput' + '(' + ', '.join(pieces) + ')'
_FieldInputSpec.bind_record_class(FieldInput)

class InitComponent:
    __slots__ = ('name', 'target_port', 'order', 'template')
    __dds_record_spec__ = _InitComponentSpec
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
            raise AttributeError('InitComponent records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('target_port=' + repr(self.target_port))
        pieces.append('order=' + repr(self.order))
        pieces.append('template=' + repr(self.template))
        return 'InitComponent' + '(' + ', '.join(pieces) + ')'
_InitComponentSpec.bind_record_class(InitComponent)

class Getter:
    __slots__ = ('name', 'target_port', 'order', 'template')
    __dds_record_spec__ = _GetterSpec
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
            raise AttributeError('Getter records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('target_port=' + repr(self.target_port))
        pieces.append('order=' + repr(self.order))
        pieces.append('template=' + repr(self.template))
        return 'Getter' + '(' + ', '.join(pieces) + ')'
_GetterSpec.bind_record_class(Getter)
FieldsCollection = RuntimeCollection('Fields', _FieldInputSpec, allows_multiple=True, identity=_NameProperty)
InitComponentsCollection = RuntimeCollection('InitComponents', _InitComponentSpec, allows_multiple=True, identity=_NameProperty)
GettersCollection = RuntimeCollection('Getters', _GetterSpec, allows_multiple=True, identity=_NameProperty)
InitFieldsCollection = RuntimeComputedCollection('InitFields', source=FieldsCollection, when=(_InitProperty.eq(True),))
GetterFieldsCollection = RuntimeComputedCollection('GetterFields', source=FieldsCollection, when=())
ClassBodyPort = RuntimePort('Class.body', allows_multiple=True)
_RUNTIME_SPEC = RuntimeContainerSpec(collections=(FieldsCollection, InitComponentsCollection, GettersCollection), computed_collections=(InitFieldsCollection, GetterFieldsCollection), ports=(ClassBodyPort,), port_index=RuntimePortIndex(target=_TargetPortProperty, order=_OrderProperty))

class GetterTemplateMatcher:

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
            return self._finish(cache_key, (from_astichi_code("{'getter': 'managed'}"), 'managed-getter', 1.0), records, values)
        return self._finish(cache_key, (from_astichi_code("{'getter': 'plain'}"), None, 0.0), records, values)

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

def run_init_field_provides_component(builder):
    for source in builder.records(InitFieldsCollection):
        record = InitComponent(name=source.name, target_port=ClassBodyPort.of('runtime'), order=source.order, template='init-field-component')
        builder.write(InitComponentsCollection, record, policy=AddIfAbsent)

def run_field_provides_getter(builder):
    snapshot = builder._snapshot()
    for source in snapshot.matchers.GetterTemplate.sequence():
        record = Getter(name=source.records[0].name, target_port=ClassBodyPort.of('runtime'), order=getter_order_for(source), template=source.resource)
        builder.write(GettersCollection, record, policy=AddIfAbsent)

def run_operations(builder):
    run_init_field_provides_component(builder)
    run_field_provides_getter(builder)
    return builder

def build_container(builder):
    run_operations(builder)
    return builder.freeze()

class _GeneratedMatcherNamespace:

    def __init__(self, container):
        self.GetterTemplate = _ContainerGetterTemplateMatcher(container)

class _ContainerGetterTemplateMatcher:

    def __init__(self, container):
        self._container = container
        self._runtime = GetterTemplateMatcher()

    def resolve(self, *records):
        return self._runtime.resolve(*records)

    def sequence(self):
        yield from self._runtime.sequence(self._container.GetterFields.sequence())

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
