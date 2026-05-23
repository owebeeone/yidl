from yidl.generation.data_def_sys import AddIfAbsent, AssemblyDiagnosticError, DDSContainerBuilder, DDSOperationContext, NOT_PROVIDED, REQUIRED, RejectDuplicate, ReplaceExisting, RuntimeCollection, RuntimeComputedCollection, RuntimeContainerSpec, RuntimePort, RuntimePortIndex, RuntimeProperty, RuntimeRecord, RuntimeUnion
_NameProperty = RuntimeProperty('Name', str, default=REQUIRED, storage_name='name')
_SourceOrderProperty = RuntimeProperty('SourceOrder', int, default=0, storage_name='source_order')
_TxKeyProperty = RuntimeProperty('TxKey', str, default=REQUIRED, storage_name='tx_key')
_TxIndexProperty = RuntimeProperty('TxIndex', int, default=REQUIRED, storage_name='tx_index')
_TransactionalFieldSpec = RuntimeRecord('TransactionalField', (_NameProperty, _TxKeyProperty, _SourceOrderProperty))
_TxKeyRecordSpec = RuntimeRecord('TxKeyRecord', (_TxKeyProperty, _TxIndexProperty))

class TransactionalField:
    __slots__ = ('name', 'tx_key', 'source_order')
    __dds_record_spec__ = _TransactionalFieldSpec
    name: str
    tx_key: str
    source_order: int

    def __init__(self, *, name: str, tx_key: str, source_order: int=0):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        if not isinstance(tx_key, str):
            raise TypeError('TxKey must be str, got ' + type(tx_key).__name__)
        object.__setattr__(self, 'tx_key', tx_key)
        if not isinstance(source_order, int):
            raise TypeError('SourceOrder must be int, got ' + type(source_order).__name__)
        object.__setattr__(self, 'source_order', source_order)

    def __setattr__(self, name, value):
        if name in ('name', 'tx_key', 'source_order'):
            raise AttributeError('TransactionalField records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('tx_key=' + repr(self.tx_key))
        pieces.append('source_order=' + repr(self.source_order))
        return 'TransactionalField' + '(' + ', '.join(pieces) + ')'
_TransactionalFieldSpec.bind_record_class(TransactionalField)

class TxKeyRecord:
    __slots__ = ('tx_key', 'tx_index')
    __dds_record_spec__ = _TxKeyRecordSpec
    tx_key: str
    tx_index: int

    def __init__(self, *, tx_key: str, tx_index: int):
        if not isinstance(tx_key, str):
            raise TypeError('TxKey must be str, got ' + type(tx_key).__name__)
        object.__setattr__(self, 'tx_key', tx_key)
        if not isinstance(tx_index, int):
            raise TypeError('TxIndex must be int, got ' + type(tx_index).__name__)
        object.__setattr__(self, 'tx_index', tx_index)

    def __setattr__(self, name, value):
        if name in ('tx_key', 'tx_index'):
            raise AttributeError('TxKeyRecord records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('tx_key=' + repr(self.tx_key))
        pieces.append('tx_index=' + repr(self.tx_index))
        return 'TxKeyRecord' + '(' + ', '.join(pieces) + ')'
_TxKeyRecordSpec.bind_record_class(TxKeyRecord)
TransactionalFieldsCollection = RuntimeCollection('TransactionalFields', _TransactionalFieldSpec, allows_multiple=True, identity=_NameProperty)
TxKeysCollection = RuntimeCollection('TxKeys', _TxKeyRecordSpec, allows_multiple=True, identity=_TxKeyProperty)
_RUNTIME_SPEC = RuntimeContainerSpec(collections=(TransactionalFieldsCollection, TxKeysCollection), computed_collections=(), ports=(), port_index=None)

def run_build_tx_keys(builder):
    ctx = DDSOperationContext(builder, 'BuildTxKeys', ordered_inputs={TransactionalFieldsCollection: (_SourceOrderProperty,)})
    seen = set()
    next_index = 0
    for field in ctx.records(TransactionalFieldsCollection):
        tx_key = field.tx_key
        if tx_key in seen:
            continue
        seen.add(tx_key)
        ctx.write(TxKeysCollection, TxKeyRecord(tx_key=tx_key, tx_index=next_index), policy=AddIfAbsent)
        next_index += 1

def run_operations(builder):
    run_build_tx_keys(builder)
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
