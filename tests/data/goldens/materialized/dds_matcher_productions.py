from yidl.generation.data_def_sys import AddIfAbsent, DDSContainerBuilder, NOT_PROVIDED, REQUIRED
from yidl.generation.data_def_sys import RejectDuplicate, ReplaceExisting
from yidl.generation.data_def_sys import RuntimeCollection, RuntimeComputedCollection, RuntimeContainerSpec
from yidl.generation.data_def_sys import RuntimePort, RuntimePortIndex
from yidl.generation.data_def_sys import RuntimeProperty, RuntimeRecord, RuntimeUnion
_NameProperty = RuntimeProperty('Name', str, default=REQUIRED, storage_name='name')
_InitProperty = RuntimeProperty('Init', bool, default=True, storage_name='init')
_DefaultedProperty = RuntimeProperty('Defaulted', bool, default=False, storage_name='defaulted')
_OrderProperty = RuntimeProperty('Order', int, default=0, storage_name='order')
_TargetPortProperty = RuntimeProperty('TargetPort', object, default=REQUIRED, storage_name='target_port')
_TemplateProperty = RuntimeProperty('Template', object, default=REQUIRED, storage_name='template')

_FieldSpec = RuntimeRecord('Field', (_NameProperty, _InitProperty, _DefaultedProperty, _OrderProperty))
_ParamComponentSpec = RuntimeRecord('ParamComponent', (_NameProperty, _TargetPortProperty, _OrderProperty, _TemplateProperty, _DefaultedProperty))

class Field:
    __slots__ = ('name', 'init', 'defaulted', 'order')
    __dds_record_spec__ = _FieldSpec
    name: str
    init: bool
    defaulted: bool
    order: int

    def __init__(self, *, name: str, init: bool=True, defaulted: bool=False, order: int=0):
        if not isinstance(name, str):
            raise TypeError(
                'Name must be str, got '
                + type(name).__name__
            )
        object.__setattr__(self, 'name', name)
        if not isinstance(init, bool):
            raise TypeError(
                'Init must be bool, got '
                + type(init).__name__
            )
        object.__setattr__(self, 'init', init)
        if not isinstance(defaulted, bool):
            raise TypeError(
                'Defaulted must be bool, got '
                + type(defaulted).__name__
            )
        object.__setattr__(self, 'defaulted', defaulted)
        if not isinstance(order, int):
            raise TypeError(
                'Order must be int, got '
                + type(order).__name__
            )
        object.__setattr__(self, 'order', order)

    def __setattr__(self, name, value):
        if name in ('name', 'init', 'defaulted', 'order'):
            raise AttributeError('Field records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('init=' + repr(self.init))
        pieces.append('defaulted=' + repr(self.defaulted))
        pieces.append('order=' + repr(self.order))
        return 'Field' + '(' + ', '.join(pieces) + ')'
_FieldSpec.bind_record_class(Field)

class ParamComponent:
    __slots__ = ('name', 'target_port', 'order', 'template', 'defaulted')
    __dds_record_spec__ = _ParamComponentSpec
    name: str
    target_port: object
    order: int
    template: object
    defaulted: bool

    def __init__(self, *, name: str, target_port: object, order: int=0, template: object, defaulted: bool=False):
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
        if not isinstance(defaulted, bool):
            raise TypeError(
                'Defaulted must be bool, got '
                + type(defaulted).__name__
            )
        object.__setattr__(self, 'defaulted', defaulted)

    def __setattr__(self, name, value):
        if name in ('name', 'target_port', 'order', 'template', 'defaulted'):
            raise AttributeError('ParamComponent records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('target_port=' + repr(self.target_port))
        pieces.append('order=' + repr(self.order))
        pieces.append('template=' + repr(self.template))
        pieces.append('defaulted=' + repr(self.defaulted))
        return 'ParamComponent' + '(' + ', '.join(pieces) + ')'
_ParamComponentSpec.bind_record_class(ParamComponent)

FieldsCollection = RuntimeCollection('Fields', _FieldSpec, allows_multiple=True, identity=_NameProperty)
ParamsCollection = RuntimeCollection('Params', _ParamComponentSpec, allows_multiple=True, identity=_NameProperty)

InitFieldsCollection = RuntimeComputedCollection('InitFields', source=FieldsCollection, when=(_InitProperty.eq(True),))

InitParamsPort = RuntimePort('Init.params', allows_multiple=True)

_RUNTIME_SPEC = RuntimeContainerSpec(collections=(FieldsCollection, ParamsCollection), computed_collections=(InitFieldsCollection,), ports=(InitParamsPort,), port_index=RuntimePortIndex(target=_TargetPortProperty, order=_OrderProperty))

from itertools import product
from yidl.generation.data_def_sys import MatcherResult, NOT_PROVIDED, from_astichi_code

class InitParamTemplateMatcher:

    def __init__(self):
        self._cache = {}

    def resolve(self, field_record):
        records = (field_record,)
        values = (getattr(field_record, 'defaulted', NOT_PROVIDED),)
        try:
            cached = self._cache.get(values, NOT_PROVIDED)
        except TypeError:
            cached = NOT_PROVIDED
            cache_key = None
        else:
            cache_key = values
        if cached is not NOT_PROVIDED:
            return self._finish(None, cached, records, values)
        if values[0:1] == (True,):
            return self._finish(cache_key, (from_astichi_code("{'param': 'defaulted'}"), 'defaulted-param', 1.0), records, values)
        return self._finish(cache_key, (from_astichi_code("{'param': 'required'}"), None, 0.0), records, values)

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

def run_init_param_template_provides_param(builder):
    snapshot = builder._snapshot()
    for source in snapshot.matchers.InitParamTemplate.sequence():
        record = ParamComponent(name=source.records[0].name, target_port=InitParamsPort.of(('Example', '__init__')), order=source.records[0].order, template=source.resource, defaulted=source.values[0])
        builder.write(ParamsCollection, record, policy=AddIfAbsent)

def run_operations(builder):
    run_init_param_template_provides_param(builder)
    return builder

def build_container(builder):
    run_operations(builder)
    return builder.freeze()

class _GeneratedMatcherNamespace:
    def __init__(self, container):
        self.InitParamTemplate = _ContainerInitParamTemplateMatcher(container)

class _ContainerInitParamTemplateMatcher:
    def __init__(self, container):
        self._container = container
        self._runtime = InitParamTemplateMatcher()

    def resolve(self, *records):
        return self._runtime.resolve(*records)

    def sequence(self):
        yield from self._runtime.sequence(self._container.InitFields.sequence())

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
