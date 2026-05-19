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

    class Widget:
        __module__ = "generated_dataclasses"
        __dataclass_params__ = {"frozen": True}
        __dataclass_fields__ = {
            "count": _field_info(
                name="count",
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
            "level": _field_info(
                name="level",
                type="int",
                default=_yidl_defaults["Widget.level"],
                default_factory=_MISSING,
                init=True,
                repr=True,
                compare=True,
                hash=None,
                kw_only=False,
                metadata=None,
                kind="field",
            ),
            "tags": _field_info(
                name="tags",
                type="list[str]",
                default=_MISSING,
                default_factory=_yidl_default_factories["Widget.tags"],
                init=True,
                repr=True,
                compare=False,
                hash=None,
                kw_only=False,
                metadata=None,
                kind="field",
            ),
            "scale": _field_info(
                name="scale",
                type="int",
                default=_yidl_defaults["Widget.scale"],
                default_factory=_MISSING,
                init=True,
                repr=True,
                compare=False,
                hash=None,
                kw_only=False,
                metadata=None,
                kind="initvar",
            ),
            "hidden": _field_info(
                name="hidden",
                type="str",
                default=_yidl_defaults["Widget.hidden"],
                default_factory=_MISSING,
                init=False,
                repr=False,
                compare=False,
                hash=None,
                kw_only=False,
                metadata=None,
                kind="field",
            ),
            "kind": _field_info(
                name="kind",
                type="str",
                default=_yidl_defaults["Widget.kind"],
                default_factory=_MISSING,
                init=False,
                repr=False,
                compare=False,
                hash=None,
                kw_only=False,
                metadata=None,
                kind="classvar",
            ),
        }
        __annotations__ = {
            "count": "int",
            "level": "int",
            "tags": "list[str]",
            "scale": "int",
            "hidden": "str",
            "kind": "str",
        }
        pass
        pass
        level = _yidl_defaults["Widget.level"]
        pass
        pass
        hidden = _yidl_defaults["Widget.hidden"]
        kind = _yidl_defaults["Widget.kind"]
        __match_args__ = ("count", "level", "tags", "scale")

        def __init__(
            self,
            count: "int",
            level: "int" = _yidl_defaults["Widget.level"],
            tags: "list[str]" = _HAS_DEFAULT_FACTORY,
            scale: "int" = _yidl_defaults["Widget.scale"],
        ):
            pass
            pass
            if tags is _HAS_DEFAULT_FACTORY:
                tags = _yidl_default_factories["Widget.tags"]()
            pass
            pass
            pass
            object.__setattr__(self, "count", count)
            object.__setattr__(self, "level", level)
            object.__setattr__(self, "tags", tags)
            pass

        def __repr__(self):
            return (
                "Widget"
                + "("
                + ", ".join(
                    (
                        "count" + "=" + repr(getattr(self, "count")),
                        "level" + "=" + repr(getattr(self, "level")),
                        "tags" + "=" + repr(getattr(self, "tags")),
                    )
                )
                + ")"
            )

        def __eq__(self, other):
            if other.__class__ is self.__class__:
                return (getattr(self, "count"), getattr(self, "level")) == (
                    getattr(other, "count"),
                    getattr(other, "level"),
                )
            return NotImplemented

        pass
        pass
        pass
        pass

        def __hash__(self):
            return hash((getattr(self, "count"), getattr(self, "level")))

        def __setattr__(self, name, value):
            raise FrozenInstanceError(f"cannot assign to field {name!r}")

        def __delattr__(self, name):
            raise FrozenInstanceError(f"cannot delete field {name!r}")

    return {"Widget": Widget}
