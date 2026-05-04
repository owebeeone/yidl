from yidl.generation.data_def_sys import AddIfAbsent, DDSContainerBuilder, NOT_PROVIDED, REQUIRED
from yidl.generation.data_def_sys import RejectDuplicate, ReplaceExisting
from yidl.generation.data_def_sys import RuntimeCollection, RuntimeComputedCollection, RuntimeContainerSpec
from yidl.generation.data_def_sys import RuntimePort, RuntimePortIndex
from yidl.generation.data_def_sys import RuntimeProperty, RuntimeRecord, RuntimeUnion
_NameProperty = RuntimeProperty('Name', str, default=REQUIRED, storage_name='name')
_KindProperty = RuntimeProperty('Kind', str, default='plain', storage_name='kind')
_TargetPortProperty = RuntimeProperty('TargetPort', object, default=REQUIRED, storage_name='target_port')
_OrderProperty = RuntimeProperty('Order', int, default=0, storage_name='order')
_TemplateProperty = RuntimeProperty('Template', object, default=REQUIRED, storage_name='template')

_FieldSpec = RuntimeRecord('Field', (_NameProperty, _KindProperty, _OrderProperty))
_GetterSpec = RuntimeRecord('Getter', (_NameProperty, _TargetPortProperty, _OrderProperty, _TemplateProperty))

class Field:
    __slots__ = ('name', 'kind', 'order')
    __dds_record_spec__ = _FieldSpec
    name: str
    kind: str
    order: int

    def __init__(self, *, name: str, kind: str='plain', order: int=0):
        if not isinstance(name, str):
            raise TypeError(
                'Name must be str, got '
                + type(name).__name__
            )
        object.__setattr__(self, 'name', name)
        if not isinstance(kind, str):
            raise TypeError(
                'Kind must be str, got '
                + type(kind).__name__
            )
        object.__setattr__(self, 'kind', kind)
        if not isinstance(order, int):
            raise TypeError(
                'Order must be int, got '
                + type(order).__name__
            )
        object.__setattr__(self, 'order', order)

    def __setattr__(self, name, value):
        if name in ('name', 'kind', 'order'):
            raise AttributeError('Field records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('kind=' + repr(self.kind))
        pieces.append('order=' + repr(self.order))
        return 'Field' + '(' + ', '.join(pieces) + ')'
_FieldSpec.bind_record_class(Field)

class Getter:
    __slots__ = ('name', 'target_port', 'order', 'template')
    __dds_record_spec__ = _GetterSpec
    name: str
    target_port: object
    order: int
    template: object

    def __init__(self, *, name: str, target_port: object, order: int=0, template: object):
        if not isinstance(name, str):
            raise TypeError(
                'Name must be str, got '
                + type(name).__name__
            )
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'target_port', target_port)
        if not isinstance(order, int):
            raise TypeError(
                'Order must be int, got '
                + type(order).__name__
            )
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

FieldsCollection = RuntimeCollection('Fields', _FieldSpec, allows_multiple=True, identity=_NameProperty)
GettersCollection = RuntimeCollection('Getters', _GetterSpec, allows_multiple=True, identity=_NameProperty)

GetterFieldsCollection = RuntimeComputedCollection('GetterFields', source=FieldsCollection, when=())

ClassBodyPort = RuntimePort('Class.body', allows_multiple=True)

_RUNTIME_SPEC = RuntimeContainerSpec(collections=(FieldsCollection, GettersCollection), computed_collections=(GetterFieldsCollection,), ports=(ClassBodyPort,), port_index=RuntimePortIndex(target=_TargetPortProperty, order=_OrderProperty))

from itertools import product
from yidl.generation.data_def_sys import MatcherResult, NOT_PROVIDED, from_astichi_code

class PropertyGetterTemplateMatcher:

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

def run_field_provides_property_getter(builder):
    snapshot = builder._snapshot()
    for source in snapshot.matchers.PropertyGetterTemplate.sequence():
        record = Getter(name=source.records[0].name, target_port=ClassBodyPort.of('runtime'), order=source.records[0].order, template=source.resource)
        builder.write(GettersCollection, record, policy=AddIfAbsent)

def run_operations(builder):
    run_field_provides_property_getter(builder)
    return builder

def build_container(builder):
    run_operations(builder)
    return builder.freeze()

class _GeneratedMatcherNamespace:
    def __init__(self, container):
        self.PropertyGetterTemplate = _ContainerPropertyGetterTemplateMatcher(container)

class _ContainerPropertyGetterTemplateMatcher:
    def __init__(self, container):
        self._container = container
        self._runtime = PropertyGetterTemplateMatcher()

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
