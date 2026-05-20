from __future__ import annotations
_MISSING = object()
_HAS_DEFAULT_FACTORY = object()

class FrozenInstanceError(AttributeError):
    pass

def _field_info(**kw):
    return kw

def build_generated_dataclasses(*, defaults=None, default_factories=None):
    _yidl_defaults = {} if defaults is None else defaults
    _yidl_default_factories = {} if default_factories is None else default_factories

    class Example:
        __module__ = 'generated_dataclasses'
        __dataclass_params__ = None
        __dataclass_fields__ = {'v1': _field_info(name='v1', type='int', default=_MISSING, default_factory=_MISSING, init=True, repr=True, compare=True, hash=None, kw_only=False, metadata=None, kind='field'), 'v3': _field_info(name='v3', type='int', default=_MISSING, default_factory=_yidl_default_factories['Example.v3'], init=True, repr=True, compare=True, hash=None, kw_only=False, metadata=None, kind='field'), 'v4': _field_info(name='v4', type='int', default=_yidl_defaults['Example.v4'], default_factory=_MISSING, init=False, repr=False, compare=False, hash=None, kw_only=False, metadata=None, kind='field'), 'v2': _field_info(name='v2', type='int', default=_MISSING, default_factory=_yidl_default_factories['Example.v2'], init=True, repr=True, compare=True, hash=None, kw_only=False, metadata=None, kind='field')}
        __annotations__ = {'v1': 'int', 'v3': 'int', 'v4': 'int', 'v2': 'int'}
        pass
        pass
        pass
        v4 = _yidl_defaults['Example.v4']
        pass
        __match_args__ = ('v1', 'v3', 'v2')

        def __init__(self, v1: 'int', v3: 'int'=_HAS_DEFAULT_FACTORY, v2: 'int'=_HAS_DEFAULT_FACTORY):
            if v2 is _HAS_DEFAULT_FACTORY:
                v2 = _yidl_default_factories['Example.v2'](v1=v1)
            if v3 is _HAS_DEFAULT_FACTORY:
                v3 = _yidl_default_factories['Example.v3'](v2=v2, v1=v1, v4=_yidl_defaults['Example.v4'])
            setattr(self, 'v1', v1)
            setattr(self, 'v3', v3)
            setattr(self, 'v2', v2)
            pass

        def __repr__(self):
            return 'Example' + '(' + ', '.join(('v1' + '=' + repr(getattr(self, 'v1')), 'v3' + '=' + repr(getattr(self, 'v3')), 'v2' + '=' + repr(getattr(self, 'v2')))) + ')'

        def __eq__(self, other):
            if other.__class__ is self.__class__:
                return (getattr(self, 'v1'), getattr(self, 'v3'), getattr(self, 'v2')) == (getattr(other, 'v1'), getattr(other, 'v3'), getattr(other, 'v2'))
            return NotImplemented
        pass
        pass
        pass
        pass
        __hash__ = None
        pass
        pass
    return {'Example': Example}
