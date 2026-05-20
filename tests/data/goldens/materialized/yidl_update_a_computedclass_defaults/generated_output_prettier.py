from __future__ import annotations

_HAS_DEFAULT_FACTORY = object()


class FrozenInstanceError(AttributeError):
    pass


def build_generated_dataclasses(
    *,
    _Example_dataclass_params,
    _Example_dataclass_fields,
    _Example_annotations,
    _Example_match_args,
    _Example_v3_default_factory,
    _Example_v4_default,
    _Example_v2_default_factory,
):

    class Example:
        __module__ = "generated_dataclasses"
        __dataclass_params__ = _Example_dataclass_params
        __dataclass_fields__ = _Example_dataclass_fields
        __annotations__ = _Example_annotations
        pass
        pass
        pass
        v4 = _Example_v4_default
        pass
        __match_args__ = _Example_match_args

        def __init__(
            self,
            v1: "int",
            v3: "int" = _HAS_DEFAULT_FACTORY,
            v2: "int" = _HAS_DEFAULT_FACTORY,
        ):
            if v2 is _HAS_DEFAULT_FACTORY:
                v2 = _Example_v2_default_factory(v1=v1)
            if v3 is _HAS_DEFAULT_FACTORY:
                v3 = _Example_v3_default_factory(v2=v2, v1=v1, v4=_Example_v4_default)
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
