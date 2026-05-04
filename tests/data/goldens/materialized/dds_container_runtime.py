from yidl.generation.data_def_sys import AddIfAbsent, DDSContainerBuilder, NOT_PROVIDED, REQUIRED
from yidl.generation.data_def_sys import RejectDuplicate, ReplaceExisting
from yidl.generation.data_def_sys import RuntimeCollection, RuntimeComputedCollection, RuntimeContainerSpec
from yidl.generation.data_def_sys import RuntimePort, RuntimePortIndex
from yidl.generation.data_def_sys import RuntimeProperty, RuntimeRecord, RuntimeUnion
_NameProperty = RuntimeProperty('Name', str, default=REQUIRED, storage_name='name')
_InitProperty = RuntimeProperty('Init', bool, default=True, storage_name='init')
_KindProperty = RuntimeProperty('Kind', str, default=REQUIRED, storage_name='kind')

_PlainFieldSpec = RuntimeRecord('PlainField', (_NameProperty, _InitProperty))
_ManagedFieldSpec = RuntimeRecord('ManagedField', (_NameProperty, _InitProperty, _KindProperty))
_ClassInputSpec = RuntimeRecord('ClassInput', (_NameProperty,))

_FieldSpecsUnion = RuntimeUnion('FieldSpecs', (_PlainFieldSpec, _ManagedFieldSpec))

class PlainField:
    __slots__ = ('name', 'init')
    __dds_record_spec__ = _PlainFieldSpec
    name: str
    init: bool

    def __init__(self, *, name: str, init: bool=True):
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

    def __setattr__(self, name, value):
        if name in ('name', 'init'):
            raise AttributeError('PlainField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('init=' + repr(self.init))
        return 'PlainField' + '(' + ', '.join(pieces) + ')'
_PlainFieldSpec.bind_record_class(PlainField)

class ManagedField:
    __slots__ = ('name', 'init', 'kind')
    __dds_record_spec__ = _ManagedFieldSpec
    name: str
    init: bool
    kind: str

    def __init__(self, *, name: str, init: bool=True, kind: str):
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
        if not isinstance(kind, str):
            raise TypeError(
                'Kind must be str, got '
                + type(kind).__name__
            )
        object.__setattr__(self, 'kind', kind)

    def __setattr__(self, name, value):
        if name in ('name', 'init', 'kind'):
            raise AttributeError('ManagedField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('init=' + repr(self.init))
        pieces.append('kind=' + repr(self.kind))
        return 'ManagedField' + '(' + ', '.join(pieces) + ')'
_ManagedFieldSpec.bind_record_class(ManagedField)

class ClassInput:
    __slots__ = ('name',)
    __dds_record_spec__ = _ClassInputSpec
    name: str

    def __init__(self, *, name: str):
        if not isinstance(name, str):
            raise TypeError(
                'Name must be str, got '
                + type(name).__name__
            )
        object.__setattr__(self, 'name', name)

    def __setattr__(self, name, value):
        if name in ('name',):
            raise AttributeError('ClassInput records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        return 'ClassInput' + '(' + ', '.join(pieces) + ')'
_ClassInputSpec.bind_record_class(ClassInput)

FieldsCollection = RuntimeCollection('Fields', _FieldSpecsUnion, allows_multiple=True, identity=_NameProperty)
ClassInputCollection = RuntimeCollection('ClassInput', _ClassInputSpec, allows_multiple=False, identity=_NameProperty)

InitFieldsCollection = RuntimeComputedCollection('InitFields', source=FieldsCollection, when=(_InitProperty.eq(True),))
ManagedInitFieldsCollection = RuntimeComputedCollection('ManagedInitFields', source=InitFieldsCollection, when=(_KindProperty.eq('managed'),))

_RUNTIME_SPEC = RuntimeContainerSpec(collections=(FieldsCollection, ClassInputCollection), computed_collections=(InitFieldsCollection, ManagedInitFieldsCollection), ports=(), port_index=None)

from itertools import product
from yidl.generation.data_def_sys import MatcherResult, NOT_PROVIDED, from_astichi_code

class InitGetterMatcher:

    def __init__(self):
        self._cache = {}

    def resolve(self, field_record):
        records = (field_record,)
        values = (getattr(field_record, 'name', NOT_PROVIDED),)
        try:
            cached = self._cache.get(values, NOT_PROVIDED)
        except TypeError:
            cached = NOT_PROVIDED
            cache_key = None
        else:
            cache_key = values
        if cached is not NOT_PROVIDED:
            return self._finish(None, cached, records, values)
        if values[0:1] == ('count',):
            return self._finish(cache_key, (from_astichi_code("{'resource': 'count'}"), 'count', 1.0), records, values)
        return self._finish(cache_key, None, records, values)

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

class _GeneratedMatcherNamespace:
    def __init__(self, container):
        self.InitGetter = _ContainerInitGetterMatcher(container)

class _ContainerInitGetterMatcher:
    def __init__(self, container):
        self._container = container
        self._runtime = InitGetterMatcher()

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
