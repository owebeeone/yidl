from __future__ import annotations

from yidl.runtime.lifecycle_markers import FieldDecl
from yidl.runtime.lifecycle_markers import LifecycleDefinitionError
from yidl.runtime.lifecycle_markers import LifecycleMarker
from yidl.runtime.lifecycle_markers import MISSING
from yidl.runtime.lifecycle_markers import classvar
from yidl.runtime.lifecycle_markers import field
from yidl.runtime.lifecycle_markers import initvar
from yidl.runtime.lifecycle_markers import managed
from yidl.runtime.lifecycle_markers import normalize_marker


def lifecycle(cls: type[object]) -> type[object]:
    """Phase B lifecycle decorator placeholder."""

    return cls


__all__ = [
    "FieldDecl",
    "LifecycleDefinitionError",
    "LifecycleMarker",
    "MISSING",
    "classvar",
    "field",
    "initvar",
    "lifecycle",
    "managed",
    "normalize_marker",
]

