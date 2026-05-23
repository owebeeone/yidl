from yidl.generation.data_def_sys import AddIfAbsent, DDSContainerBuilder, NOT_PROVIDED, REQUIRED, RejectDuplicate, ReplaceExisting, RuntimeCollection, RuntimeComputedCollection, RuntimeContainerSpec, RuntimePort, RuntimePortIndex, RuntimeProperty, RuntimeRecord, RuntimeUnion
_NameProperty = RuntimeProperty('Name', str, default=REQUIRED, storage_name='name')
_TxKeyProperty = RuntimeProperty('TxKey', str, default=REQUIRED, storage_name='tx_key')
_PhaseProperty = RuntimeProperty('Phase', str, default=REQUIRED, storage_name='phase')
_TxIndexProperty = RuntimeProperty('TxIndex', int, default=REQUIRED, storage_name='tx_index')
_OrderProperty = RuntimeProperty('Order', int, default=0, storage_name='order')
_TxKeyRecordSpec = RuntimeRecord('TxKeyRecord', (_TxKeyProperty, _PhaseProperty, _TxIndexProperty))
_FieldSpec = RuntimeRecord('Field', (_NameProperty, _TxKeyProperty, _PhaseProperty, _OrderProperty))
_ContributionSpec = RuntimeRecord('Contribution', (_TxIndexProperty, _NameProperty, _OrderProperty))

class TxKeyRecord:
    __slots__ = ('tx_key', 'phase', 'tx_index')
    __dds_record_spec__ = _TxKeyRecordSpec
    tx_key: str
    phase: str
    tx_index: int

    def __init__(self, *, tx_key: str, phase: str, tx_index: int):
        if not isinstance(tx_key, str):
            raise TypeError('TxKey must be str, got ' + type(tx_key).__name__)
        object.__setattr__(self, 'tx_key', tx_key)
        if not isinstance(phase, str):
            raise TypeError('Phase must be str, got ' + type(phase).__name__)
        object.__setattr__(self, 'phase', phase)
        if not isinstance(tx_index, int):
            raise TypeError('TxIndex must be int, got ' + type(tx_index).__name__)
        object.__setattr__(self, 'tx_index', tx_index)

    def __setattr__(self, name, value):
        if name in ('tx_key', 'phase', 'tx_index'):
            raise AttributeError('TxKeyRecord records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('tx_key=' + repr(self.tx_key))
        pieces.append('phase=' + repr(self.phase))
        pieces.append('tx_index=' + repr(self.tx_index))
        return 'TxKeyRecord' + '(' + ', '.join(pieces) + ')'
_TxKeyRecordSpec.bind_record_class(TxKeyRecord)

class Field:
    __slots__ = ('name', 'tx_key', 'phase', 'order')
    __dds_record_spec__ = _FieldSpec
    name: str
    tx_key: str
    phase: str
    order: int

    def __init__(self, *, name: str, tx_key: str, phase: str, order: int=0):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        if not isinstance(tx_key, str):
            raise TypeError('TxKey must be str, got ' + type(tx_key).__name__)
        object.__setattr__(self, 'tx_key', tx_key)
        if not isinstance(phase, str):
            raise TypeError('Phase must be str, got ' + type(phase).__name__)
        object.__setattr__(self, 'phase', phase)
        if not isinstance(order, int):
            raise TypeError('Order must be int, got ' + type(order).__name__)
        object.__setattr__(self, 'order', order)

    def __setattr__(self, name, value):
        if name in ('name', 'tx_key', 'phase', 'order'):
            raise AttributeError('Field records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('tx_key=' + repr(self.tx_key))
        pieces.append('phase=' + repr(self.phase))
        pieces.append('order=' + repr(self.order))
        return 'Field' + '(' + ', '.join(pieces) + ')'
_FieldSpec.bind_record_class(Field)

class Contribution:
    __slots__ = ('tx_index', 'name', 'order')
    __dds_record_spec__ = _ContributionSpec
    tx_index: int
    name: str
    order: int

    def __init__(self, *, tx_index: int, name: str, order: int=0):
        if not isinstance(tx_index, int):
            raise TypeError('TxIndex must be int, got ' + type(tx_index).__name__)
        object.__setattr__(self, 'tx_index', tx_index)
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        if not isinstance(order, int):
            raise TypeError('Order must be int, got ' + type(order).__name__)
        object.__setattr__(self, 'order', order)

    def __setattr__(self, name, value):
        if name in ('tx_index', 'name', 'order'):
            raise AttributeError('Contribution records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('tx_index=' + repr(self.tx_index))
        pieces.append('name=' + repr(self.name))
        pieces.append('order=' + repr(self.order))
        return 'Contribution' + '(' + ', '.join(pieces) + ')'
_ContributionSpec.bind_record_class(Contribution)
TxKeysCollection = RuntimeCollection('TxKeys', _TxKeyRecordSpec, allows_multiple=True, identity=(_TxKeyProperty, _PhaseProperty))
FieldsCollection = RuntimeCollection('Fields', _FieldSpec, allows_multiple=True, identity=_NameProperty)
ContributionsCollection = RuntimeCollection('Contributions', _ContributionSpec, allows_multiple=True, identity=(_TxIndexProperty, _NameProperty))
_RUNTIME_SPEC = RuntimeContainerSpec(collections=(TxKeysCollection, FieldsCollection, ContributionsCollection), computed_collections=(), ports=(), port_index=None)

def run_field_provides_contribution(builder):
    for source in builder.records(FieldsCollection):
        lookup_0_key = (source.tx_key, source.phase)
        lookup_0_record = builder.by_identity(TxKeysCollection, lookup_0_key)
        if lookup_0_record is None:
            raise ValueError('no TxKeys record for identity ' + repr(lookup_0_key))
        lookup_0_value = lookup_0_record.tx_index
        record = Contribution(tx_index=lookup_0_value, name=source.name, order=source.order)
        builder.write(ContributionsCollection, record, policy=AddIfAbsent)

def run_operations(builder):
    run_field_provides_contribution(builder)
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
