from yidl.generation.data_def_sys import AddIfAbsent, DDSContainerBuilder, NOT_PROVIDED, REQUIRED
from yidl.generation.data_def_sys import RejectDuplicate, ReplaceExisting
from yidl.generation.data_def_sys import RuntimeCollection, RuntimeComputedCollection, RuntimeContainerSpec
from yidl.generation.data_def_sys import RuntimePort, RuntimePortIndex
from yidl.generation.data_def_sys import RuntimeProperty, RuntimeRecord, RuntimeUnion
_NameProperty = RuntimeProperty('Name', str, default=REQUIRED, storage_name='name')
_TargetPortProperty = RuntimeProperty('TargetPort', object, default=REQUIRED, storage_name='target_port')
_OrderProperty = RuntimeProperty('Order', int, default=0, storage_name='order')

_ComponentSpec = RuntimeRecord('Component', (_NameProperty, _TargetPortProperty, _OrderProperty))

class Component:
    __slots__ = ('name', 'target_port', 'order')
    __dds_record_spec__ = _ComponentSpec
    name: str
    target_port: object
    order: int

    def __init__(self, *, name: str, target_port: object, order: int=0):
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

ComponentsCollection = RuntimeCollection('Components', _ComponentSpec, allows_multiple=True, identity=_NameProperty)

ClassBodyPort = RuntimePort('Class.body', allows_multiple=True)
ClassNamePort = RuntimePort('Class.name', allows_multiple=False)

_RUNTIME_SPEC = RuntimeContainerSpec(collections=(ComponentsCollection,), computed_collections=(), ports=(ClassBodyPort, ClassNamePort), port_index=RuntimePortIndex(target=_TargetPortProperty, order=_OrderProperty))

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
