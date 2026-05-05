from yidl.generation.data_def_sys import AddIfAbsent, DDSContainerBuilder, NOT_PROVIDED, REQUIRED, RejectDuplicate, ReplaceExisting, RuntimeCollection, RuntimeComputedCollection, RuntimeContainerSpec, RuntimePort, RuntimePortIndex, RuntimeProperty, RuntimeRecord, RuntimeUnion
_NameProperty = RuntimeProperty('Name', str, default=REQUIRED, storage_name='name')
_InitProperty = RuntimeProperty('Init', bool, default=True, storage_name='init')
_OrderProperty = RuntimeProperty('Order', int, default=0, storage_name='order')
_TargetPortProperty = RuntimeProperty('TargetPort', object, default=REQUIRED, storage_name='target_port')
_FieldSpec = RuntimeRecord('Field', (_NameProperty, _InitProperty, _OrderProperty))
_ComponentSpec = RuntimeRecord('Component', (_NameProperty, _TargetPortProperty, _OrderProperty))

class Field:
    __slots__ = ('name', 'init', 'order')
    __dds_record_spec__ = _FieldSpec
    name: str
    init: bool
    order: int

    def __init__(self, *, name: str, init: bool=True, order: int=0):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        if not isinstance(init, bool):
            raise TypeError('Init must be bool, got ' + type(init).__name__)
        object.__setattr__(self, 'init', init)
        if not isinstance(order, int):
            raise TypeError('Order must be int, got ' + type(order).__name__)
        object.__setattr__(self, 'order', order)

    def __setattr__(self, name, value):
        if name in ('name', 'init', 'order'):
            raise AttributeError('Field records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('init=' + repr(self.init))
        pieces.append('order=' + repr(self.order))
        return 'Field' + '(' + ', '.join(pieces) + ')'
_FieldSpec.bind_record_class(Field)

class Component:
    __slots__ = ('name', 'target_port', 'order')
    __dds_record_spec__ = _ComponentSpec
    name: str
    target_port: object
    order: int

    def __init__(self, *, name: str, target_port: object, order: int=0):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'target_port', target_port)
        if not isinstance(order, int):
            raise TypeError('Order must be int, got ' + type(order).__name__)
        object.__setattr__(self, 'order', order)

    def __setattr__(self, name, value):
        if name in ('name', 'target_port', 'order'):
            raise AttributeError('Component records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('target_port=' + repr(self.target_port))
        pieces.append('order=' + repr(self.order))
        return 'Component' + '(' + ', '.join(pieces) + ')'
_ComponentSpec.bind_record_class(Component)
FieldsCollection = RuntimeCollection('Fields', _FieldSpec, allows_multiple=True, identity=_NameProperty)
ComponentsCollection = RuntimeCollection('Components', _ComponentSpec, allows_multiple=True, identity=_NameProperty)
InitFieldsCollection = RuntimeComputedCollection('InitFields', source=FieldsCollection, when=(_InitProperty.eq(True),))
ClassBodyPort = RuntimePort('Class.body', allows_multiple=True)
_RUNTIME_SPEC = RuntimeContainerSpec(collections=(FieldsCollection, ComponentsCollection), computed_collections=(InitFieldsCollection,), ports=(ClassBodyPort,), port_index=RuntimePortIndex(target=_TargetPortProperty, order=_OrderProperty))

def run_init_field_provides_component(builder):
    for source in builder.records(InitFieldsCollection):
        record = Component(name=source.name, target_port=ClassBodyPort.of('runtime'), order=field_order(source))
        builder.write(ComponentsCollection, record, policy=AddIfAbsent)

def run_operations(builder):
    run_init_field_provides_component(builder)
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
