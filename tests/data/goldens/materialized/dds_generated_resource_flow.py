from itertools import product
from yidl.generation.data_def_sys import AddIfAbsent, DDSContainerBuilder, MatcherResult, NOT_PROVIDED, REQUIRED, RejectDuplicate, ReplaceExisting, RuntimeCollection, RuntimeComputedCollection, RuntimeContainerSpec, RuntimePort, RuntimePortIndex, RuntimeProperty, RuntimeRecord, RuntimeUnion, from_astichi_code, from_import
_NameProperty = RuntimeProperty('Name', str, default=REQUIRED, storage_name='name')
_KindProperty = RuntimeProperty('Kind', str, default='plain', storage_name='kind')
_TemplateProperty = RuntimeProperty('Template', object, default=REQUIRED, storage_name='template')
_FieldSpec = RuntimeRecord('Field', (_NameProperty, _KindProperty))
_TemplateComponentSpec = RuntimeRecord('TemplateComponent', (_NameProperty, _TemplateProperty))

class Field:
    __slots__ = ('name', 'kind')
    __dds_record_spec__ = _FieldSpec
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
            raise AttributeError('Field records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('kind=' + repr(self.kind))
        return 'Field' + '(' + ', '.join(pieces) + ')'
_FieldSpec.bind_record_class(Field)

class TemplateComponent:
    __slots__ = ('name', 'template')
    __dds_record_spec__ = _TemplateComponentSpec
    name: str
    template: object

    def __init__(self, *, name: str, template: object):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'template', template)

    def __setattr__(self, name, value):
        if name in ('name', 'template'):
            raise AttributeError('TemplateComponent records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('template=' + repr(self.template))
        return 'TemplateComponent' + '(' + ', '.join(pieces) + ')'
_TemplateComponentSpec.bind_record_class(TemplateComponent)
FieldsCollection = RuntimeCollection('Fields', _FieldSpec, allows_multiple=True, identity=_NameProperty)
TemplateComponentsCollection = RuntimeCollection('TemplateComponents', _TemplateComponentSpec, allows_multiple=True, identity=_NameProperty)
_RUNTIME_SPEC = RuntimeContainerSpec(collections=(FieldsCollection, TemplateComponentsCollection), computed_collections=(), ports=(), port_index=None)

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
        if values[0:1] == ('imported',):
            return self._finish(cache_key, (from_import('math', 'sqrt'), 'imported-template', 1.0), records, values)
        return self._finish(cache_key, (from_astichi_code('astichi_comment("plain property template")\n{"template": "plain"}'), None, 0.0), records, values)

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

def run_property_template_provides_component(builder):
    snapshot = builder._snapshot()
    for source in snapshot.matchers.PropertyTemplate.sequence():
        record = TemplateComponent(name=source.records[0].name, template=source.resource)
        builder.write(TemplateComponentsCollection, record, policy=AddIfAbsent)

def run_operations(builder):
    run_property_template_provides_component(builder)
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
