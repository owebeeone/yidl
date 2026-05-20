from __future__ import annotations
_HAS_DEFAULT_FACTORY = object()

class FrozenInstanceError(AttributeError):
    pass

def build_generated_dataclasses(*, _Widget_dataclass_params, _Widget_dataclass_fields, _Widget_annotations, _Widget_match_args, _Widget_level_default, _Widget_tags_default_factory, _Widget_scale_default, _Widget_hidden_default, _Widget_kind_default):

    class Widget:
        __module__ = 'generated_dataclasses'
        __dataclass_params__ = _Widget_dataclass_params
        __dataclass_fields__ = _Widget_dataclass_fields
        __annotations__ = _Widget_annotations
        pass
        pass
        level = _Widget_level_default
        pass
        pass
        hidden = _Widget_hidden_default
        kind = _Widget_kind_default
        __match_args__ = _Widget_match_args

        def __init__(self, count: 'int', level: 'int'=_Widget_level_default, tags: 'list[str]'=_HAS_DEFAULT_FACTORY, scale: 'int'=_Widget_scale_default):
            pass
            pass
            if tags is _HAS_DEFAULT_FACTORY:
                tags = _Widget_tags_default_factory()
            pass
            pass
            pass
            object.__setattr__(self, 'count', count)
            object.__setattr__(self, 'level', level)
            object.__setattr__(self, 'tags', tags)
            pass

        def __repr__(self):
            return 'Widget' + '(' + ', '.join(('count' + '=' + repr(getattr(self, 'count')), 'level' + '=' + repr(getattr(self, 'level')), 'tags' + '=' + repr(getattr(self, 'tags')))) + ')'

        def __eq__(self, other):
            if other.__class__ is self.__class__:
                return (getattr(self, 'count'), getattr(self, 'level')) == (getattr(other, 'count'), getattr(other, 'level'))
            return NotImplemented
        pass
        pass
        pass
        pass

        def __hash__(self):
            return hash((getattr(self, 'count'), getattr(self, 'level')))

        def __setattr__(self, name, value):
            raise FrozenInstanceError(f'cannot assign to field {name!r}')

        def __delattr__(self, name):
            raise FrozenInstanceError(f'cannot delete field {name!r}')
    return {'Widget': Widget}
