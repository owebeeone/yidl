from __future__ import annotations

_MISSING = object()
_HAS_DEFAULT_FACTORY = object()


class FrozenInstanceError(AttributeError):
    pass


def _field_info(**kw):
    return kw


class Widget:
    __module__ = "generated_dataclasses"
    __dataclass_params__ = {"frozen": True}
    __dataclass_fields__ = {
        "count": _field_info(
            name="count",
            type="int",
            default=None,
            default_factory=None,
            init=True,
            repr=True,
            compare=True,
            hash=None,
            kw_only=False,
            metadata=None,
            kind="field",
        ),
        "label": _field_info(
            name="label",
            type="str",
            default=None,
            default_factory=None,
            init=True,
            repr=True,
            compare=True,
            hash=None,
            kw_only=False,
            metadata=None,
            kind="field",
        ),
    }
    __annotations__ = {"count": "int", "label": "str"}
    pass
    pass
    pass
    __match_args__ = ("count", "label")

    def __init__(self, count: "int", label: "str"):
        pass
        pass
        object.__setattr__(self, "count", count)
        object.__setattr__(self, "label", label)
        pass

    def __repr__(self):
        return (
            "Widget"
            + "("
            + ", ".join(
                (
                    "count" + "=" + repr(getattr(self, "count")),
                    "label" + "=" + repr(getattr(self, "label")),
                )
            )
            + ")"
        )

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return (getattr(self, "count"), getattr(self, "label")) == (
                getattr(other, "count"),
                getattr(other, "label"),
            )
        return NotImplemented

    pass
    pass
    pass
    pass

    def __hash__(self):
        return hash((getattr(self, "count"), getattr(self, "label")))

    def __setattr__(self, name, value):
        raise FrozenInstanceError(f"cannot assign to field {name!r}")

    def __delattr__(self, name):
        raise FrozenInstanceError(f"cannot delete field {name!r}")
