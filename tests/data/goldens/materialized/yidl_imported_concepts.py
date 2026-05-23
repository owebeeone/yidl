from yidl.generation.data_def_sys import AddIfAbsent, DDSContainerBuilder, NOT_PROVIDED, REQUIRED, RejectDuplicate, ReplaceExisting, RuntimeCollection, RuntimeComputedCollection, RuntimeContainerSpec, RuntimePort, RuntimePortIndex, RuntimeProperty, RuntimeRecord, RuntimeUnion
_NameProperty = RuntimeProperty('Name', str, default=REQUIRED, storage_name='name')
_KindProperty = RuntimeProperty('Kind', object, default=REQUIRED, storage_name='kind')
_SourceOrderProperty = RuntimeProperty('SourceOrder', int, default=0, storage_name='source_order')
_TxKeyProperty = RuntimeProperty('TxKey', str, default='default', storage_name='tx_key')
_PlainFieldSpec = RuntimeRecord('PlainField', (_NameProperty, _KindProperty, _SourceOrderProperty))
_ManagedFieldSpec = RuntimeRecord('ManagedField', (_NameProperty, _KindProperty, _SourceOrderProperty, _TxKeyProperty))
_FieldSpecsUnion = RuntimeUnion('FieldSpecs', (_PlainFieldSpec, _ManagedFieldSpec))

class PlainField:
    __slots__ = ('name', 'kind', 'source_order')
    __dds_record_spec__ = _PlainFieldSpec
    name: str
    kind: object
    source_order: int

    def __init__(self, *, name: str, kind: object, source_order: int=0):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'kind', kind)
        if not isinstance(source_order, int):
            raise TypeError('SourceOrder must be int, got ' + type(source_order).__name__)
        object.__setattr__(self, 'source_order', source_order)

    def __setattr__(self, name, value):
        if name in ('name', 'kind', 'source_order'):
            raise AttributeError('PlainField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('kind=' + repr(self.kind))
        pieces.append('source_order=' + repr(self.source_order))
        return 'PlainField' + '(' + ', '.join(pieces) + ')'
_PlainFieldSpec.bind_record_class(PlainField)

class ManagedField:
    __slots__ = ('name', 'kind', 'source_order', 'tx_key')
    __dds_record_spec__ = _ManagedFieldSpec
    name: str
    kind: object
    source_order: int
    tx_key: str

    def __init__(self, *, name: str, kind: object, source_order: int=0, tx_key: str='default'):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'kind', kind)
        if not isinstance(source_order, int):
            raise TypeError('SourceOrder must be int, got ' + type(source_order).__name__)
        object.__setattr__(self, 'source_order', source_order)
        if not isinstance(tx_key, str):
            raise TypeError('TxKey must be str, got ' + type(tx_key).__name__)
        object.__setattr__(self, 'tx_key', tx_key)

    def __setattr__(self, name, value):
        if name in ('name', 'kind', 'source_order', 'tx_key'):
            raise AttributeError('ManagedField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('kind=' + repr(self.kind))
        pieces.append('source_order=' + repr(self.source_order))
        pieces.append('tx_key=' + repr(self.tx_key))
        return 'ManagedField' + '(' + ', '.join(pieces) + ')'
_ManagedFieldSpec.bind_record_class(ManagedField)
FieldsCollection = RuntimeCollection('Fields', _FieldSpecsUnion, allows_multiple=True, identity=_NameProperty)
_RUNTIME_SPEC = RuntimeContainerSpec(collections=(FieldsCollection,), computed_collections=(), ports=(), port_index=None)

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
