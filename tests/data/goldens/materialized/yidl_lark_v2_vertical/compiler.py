from itertools import product
from yidl.generation.data_def_sys import AddIfAbsent, DDSContainerBuilder, MatcherResult, NOT_PROVIDED, REQUIRED, RejectDuplicate, ReplaceExisting, RuntimeCollection, RuntimeComputedCollection, RuntimeContainerSpec, RuntimePort, RuntimePortIndex, RuntimeProperty, RuntimeRecord, RuntimeUnion, astichi_template, from_astichi_code
_NameProperty = RuntimeProperty('Name', str, default=REQUIRED, storage_name='name')
_KindProperty = RuntimeProperty('Kind', str, default='plain', storage_name='kind')
_TemplateProperty = RuntimeProperty('Template', object, default=REQUIRED, storage_name='template')
_PlainFieldSpec = RuntimeRecord('PlainField', (_NameProperty, _KindProperty))
_ManagedFieldSpec = RuntimeRecord('ManagedField', (_NameProperty, _KindProperty))
_ComponentSpec = RuntimeRecord('Component', (_NameProperty, _TemplateProperty))
_FieldSpecsUnion = RuntimeUnion('FieldSpecs', (_PlainFieldSpec, _ManagedFieldSpec))
_ComponentSpecsUnion = RuntimeUnion('ComponentSpecs', (_ComponentSpec,))

class PlainField:
    __slots__ = ('name', 'kind')
    __dds_record_spec__ = _PlainFieldSpec
    name: str
    kind: str

    def __init__(self, *, name: str, kind: str='plain'):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        if not isinstance(kind, str):
            raise TypeError('Kind must be str, got ' + type(kind).__name__)
        object.__setattr__(self, 'kind', kind)

    def __setattr__(self, name, value):
        if name in ('name', 'kind'):
            raise AttributeError('PlainField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('kind=' + repr(self.kind))
        return 'PlainField' + '(' + ', '.join(pieces) + ')'
_PlainFieldSpec.bind_record_class(PlainField)

class ManagedField:
    __slots__ = ('name', 'kind')
    __dds_record_spec__ = _ManagedFieldSpec
    name: str
    kind: str

    def __init__(self, *, name: str, kind: str='plain'):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        if not isinstance(kind, str):
            raise TypeError('Kind must be str, got ' + type(kind).__name__)
        object.__setattr__(self, 'kind', kind)

    def __setattr__(self, name, value):
        if name in ('name', 'kind'):
            raise AttributeError('ManagedField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('kind=' + repr(self.kind))
        return 'ManagedField' + '(' + ', '.join(pieces) + ')'
_ManagedFieldSpec.bind_record_class(ManagedField)

class Component:
    __slots__ = ('name', 'template')
    __dds_record_spec__ = _ComponentSpec
    name: str
    template: object

    def __init__(self, *, name: str, template: object):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'template', template)

    def __setattr__(self, name, value):
        if name in ('name', 'template'):
            raise AttributeError('Component records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('template=' + repr(self.template))
        return 'Component' + '(' + ', '.join(pieces) + ')'
_ComponentSpec.bind_record_class(Component)
FieldsCollection = RuntimeCollection('Fields', _FieldSpecsUnion, allows_multiple=True, identity=_NameProperty)
ComponentsCollection = RuntimeCollection('Components', _ComponentSpec, allows_multiple=True, identity=_NameProperty)
_RUNTIME_SPEC = RuntimeContainerSpec(collections=(FieldsCollection, ComponentsCollection), computed_collections=(), ports=(), port_index=None)

class FieldTemplateMatcher:

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
            return self._finish(cache_key, (astichi_template(from_astichi_code('astichi_bind_external(field_name)\n{"getter": field_name}', file_name='lark_v2_vertical.yidl', line_number=35, keep_names=('field_name',)), bind=from_astichi_code('{"field_name": record.name}', file_name='lark_v2_vertical.yidl', line_number=25, offset=34, keep_names=('record',)), keep_names=from_astichi_code('("field_name",)', file_name='lark_v2_vertical.yidl', line_number=28, offset=39)), 'managed', 1.0), records, values)
        return self._finish(cache_key, (astichi_template(from_astichi_code('{"getter": "plain"}', file_name='lark_v2_vertical.yidl', line_number=31)), None, 0.0), records, values)

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

def run_field_template_components(builder):
    snapshot = builder._snapshot()
    for source in snapshot.matchers.FieldTemplate.sequence():
        record = Component(name=source.records[0].name, template=source.resource)
        builder.write(ComponentsCollection, record, policy=AddIfAbsent)

def run_operations(builder):
    run_field_template_components(builder)
    return builder

def build_container(builder):
    run_operations(builder)
    return builder.freeze()

class _GeneratedMatcherNamespace:

    def __init__(self, container):
        self.FieldTemplate = _ContainerFieldTemplateMatcher(container)

class _ContainerFieldTemplateMatcher:

    def __init__(self, container):
        self._container = container
        self._runtime = FieldTemplateMatcher()

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
