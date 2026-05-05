from yidl.generation.data_def_sys import AddIfAbsent, DDSContainerBuilder, NOT_PROVIDED, REQUIRED, RejectDuplicate, ReplaceExisting, RuntimeCollection, RuntimeComputedCollection, RuntimeContainerSpec, RuntimePort, RuntimePortIndex, RuntimeProperty, RuntimeRecord, RuntimeUnion
_NameProperty = RuntimeProperty('Name', str, default=REQUIRED, storage_name='name')
_LayerProperty = RuntimeProperty('Layer', int, default=0, storage_name='layer')
_OrderProperty = RuntimeProperty('Order', int, default=0, storage_name='order')
_SourceItemSpec = RuntimeRecord('SourceItem', (_NameProperty, _LayerProperty, _OrderProperty))
_OrderedItemSpec = RuntimeRecord('OrderedItem', (_NameProperty, _LayerProperty, _OrderProperty))

class SourceItem:
    __slots__ = ('name', 'layer', 'order')
    __dds_record_spec__ = _SourceItemSpec
    name: str
    layer: int
    order: int

    def __init__(self, *, name: str, layer: int=0, order: int=0):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        if not isinstance(layer, int):
            raise TypeError('Layer must be int, got ' + type(layer).__name__)
        object.__setattr__(self, 'layer', layer)
        if not isinstance(order, int):
            raise TypeError('Order must be int, got ' + type(order).__name__)
        object.__setattr__(self, 'order', order)

    def __setattr__(self, name, value):
        if name in ('name', 'layer', 'order'):
            raise AttributeError('SourceItem records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('layer=' + repr(self.layer))
        pieces.append('order=' + repr(self.order))
        return 'SourceItem' + '(' + ', '.join(pieces) + ')'
_SourceItemSpec.bind_record_class(SourceItem)

class OrderedItem:
    __slots__ = ('name', 'layer', 'order')
    __dds_record_spec__ = _OrderedItemSpec
    name: str
    layer: int
    order: int

    def __init__(self, *, name: str, layer: int=0, order: int=0):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        if not isinstance(layer, int):
            raise TypeError('Layer must be int, got ' + type(layer).__name__)
        object.__setattr__(self, 'layer', layer)
        if not isinstance(order, int):
            raise TypeError('Order must be int, got ' + type(order).__name__)
        object.__setattr__(self, 'order', order)

    def __setattr__(self, name, value):
        if name in ('name', 'layer', 'order'):
            raise AttributeError('OrderedItem records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('layer=' + repr(self.layer))
        pieces.append('order=' + repr(self.order))
        return 'OrderedItem' + '(' + ', '.join(pieces) + ')'
_OrderedItemSpec.bind_record_class(OrderedItem)
SourceItemsCollection = RuntimeCollection('SourceItems', _SourceItemSpec, allows_multiple=True, identity=_NameProperty)
OrderedItemsCollection = RuntimeCollection('OrderedItems', _OrderedItemSpec, allows_multiple=True, identity=_NameProperty)
_RUNTIME_SPEC = RuntimeContainerSpec(collections=(SourceItemsCollection, OrderedItemsCollection), computed_collections=(), ports=(), port_index=None)

def run_source_provides_ordered_item(builder):
    for source in builder.ordered_records(SourceItemsCollection, _LayerProperty, _OrderProperty):
        record = OrderedItem(name=source.name, layer=source.layer, order=source.order)
        builder.write(OrderedItemsCollection, record, policy=AddIfAbsent)

def run_operations(builder):
    run_source_provides_ordered_item(builder)
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
