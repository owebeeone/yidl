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
        __module__ = "generated_dataclasses"
        __dataclass_params__ = None
        __dataclass_fields__ = {
            "v1": _field_info(
                name="v1",
                type="int",
                default=_MISSING,
                default_factory=_MISSING,
                init=True,
                repr=True,
                compare=True,
                hash=None,
                kw_only=False,
                metadata=None,
                kind="field",
            ),
            "v3": _field_info(
                name="v3",
                type="int",
                default=_MISSING,
                default_factory=_yidl_default_factories["Example.v3"],
                init=True,
                repr=True,
                compare=True,
                hash=None,
                kw_only=False,
                metadata=None,
                kind="field",
            ),
            "v2": _field_info(
                name="v2",
                type="int",
                default=_MISSING,
                default_factory=_yidl_default_factories["Example.v2"],
                init=True,
                repr=True,
                compare=True,
                hash=None,
                kw_only=False,
                metadata=None,
                kind="field",
            ),
        }
        __annotations__ = {"v1": "int", "v3": "int", "v2": "int"}
        pass
        pass
        pass
        pass
        __match_args__ = ("v1", "v3", "v2")

        def __init__(
            self,
            v1: "int",
            v3: "int" = _HAS_DEFAULT_FACTORY,
            v2: "int" = _HAS_DEFAULT_FACTORY,
        ):
            if v2 is _HAS_DEFAULT_FACTORY:
                _yidl_factory_args = {}
                for _yidl_factory_param in ("v1",):
                    _yidl_factory_args[_yidl_factory_param] = locals()[
                        _yidl_factory_param
                    ]
                v2 = _yidl_default_factories["Example.v2"](**_yidl_factory_args)
            if v3 is _HAS_DEFAULT_FACTORY:
                _yidl_factory_args__astichi_scoped_1 = {}
                for _yidl_factory_param__astichi_scoped_2 in ("v2", "v1"):
                    _yidl_factory_args__astichi_scoped_1[
                        _yidl_factory_param__astichi_scoped_2
                    ] = locals()[_yidl_factory_param__astichi_scoped_2]
                v3 = _yidl_default_factories["Example.v3"](
                    **_yidl_factory_args__astichi_scoped_1
                )
            setattr(self, "v1", v1)
            setattr(self, "v3", v3)
            setattr(self, "v2", v2)
            pass

        def __repr__(self):
            return (
                "Example"
                + "("
                + ", ".join(
                    (
                        "v1" + "=" + repr(getattr(self, "v1")),
                        "v3" + "=" + repr(getattr(self, "v3")),
                        "v2" + "=" + repr(getattr(self, "v2")),
                    )
                )
                + ")"
            )

        def __eq__(self, other):
            if other.__class__ is self.__class__:
                return (
                    getattr(self, "v1"),
                    getattr(self, "v3"),
                    getattr(self, "v2"),
                ) == (getattr(other, "v1"), getattr(other, "v3"), getattr(other, "v2"))
            return NotImplemented

        pass
        pass
        pass
        pass
        __hash__ = None
        pass
        pass

    return {"Example": Example}
