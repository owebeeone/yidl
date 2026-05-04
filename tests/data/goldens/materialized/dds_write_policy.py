from yidl.generation.data_def_sys import AddIfAbsent, DDSContainerBuilder, NOT_PROVIDED, REQUIRED
from yidl.generation.data_def_sys import RejectDuplicate, ReplaceExisting
from yidl.generation.data_def_sys import RuntimeCollection, RuntimeComputedCollection, RuntimeContainerSpec
from yidl.generation.data_def_sys import RuntimeProperty, RuntimeRecord, RuntimeUnion
_NameProperty = RuntimeProperty('Name', str, default=REQUIRED, storage_name='name')
_ValueProperty = RuntimeProperty('Value', int, default=REQUIRED, storage_name='value')

_ItemSpec = RuntimeRecord('Item', (_NameProperty, _ValueProperty))

class Item:
    __slots__ = ('name', 'value')
    __dds_record_spec__ = _ItemSpec
    name: str
    value: int

    def __init__(self, *, name: str, value: int):
        if not isinstance(name, str):
            raise TypeError(
                'Name must be str, got '
                + type(name).__name__
            )
        object.__setattr__(self, 'name', name)
        if not isinstance(value, int):
            raise TypeError(
                'Value must be int, got '
                + type(value).__name__
            )
        object.__setattr__(self, 'value', value)

    def __setattr__(self, name, value):
        if name in ('name', 'value'):
            raise AttributeError('Item records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('value=' + repr(self.value))
        return 'Item' + '(' + ', '.join(pieces) + ')'
_ItemSpec.bind_record_class(Item)

ItemsCollection = RuntimeCollection('Items', _ItemSpec, allows_multiple=True, identity=_NameProperty)

_RUNTIME_SPEC = RuntimeContainerSpec(collections=(ItemsCollection,), computed_collections=())

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
