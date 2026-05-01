from yidl.generation.data_def_sys import REQUIRED, dds_property, dds_record_spec

class FieldSpec:
    __slots__ = ('init', 'name', 'payload')
    __dds_record_spec__ = dds_record_spec('FieldSpec', dds_property('Init', bool, default=True, storage_name='init'), dds_property('Name', str, default=REQUIRED, storage_name='name'), dds_property('Payload', object, default=None, storage_name='payload'))
    init: bool
    name: str
    payload: object

    def __init__(self, *, init: bool=True, name: str, payload: object=None):
        if not isinstance(init, bool):
            raise TypeError('Init must be bool, got ' + type(init).__name__)
        object.__setattr__(self, 'init', init)
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'payload', payload)

    def __setattr__(self, name, value):
        if name in ('init', 'name', 'payload'):
            raise AttributeError('FieldSpec records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('init=' + repr(self.init))
        pieces.append('name=' + repr(self.name))
        pieces.append('payload=' + repr(self.payload))
        return 'FieldSpec' + '(' + ', '.join(pieces) + ')'
