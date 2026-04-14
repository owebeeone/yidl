"""Shared Python version matrix for PRE_IMPL study runners.

Validation and performance runners should import from this module rather than
duplicating version lists in multiple places.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class PythonVersionTarget:
    key: str
    version: str
    description: str


# PRE_IMPL study matrix.
#
# These versions are chosen so lifecycle-backed study work stays compatible with
# pyrolyze's supported floor while still giving comparison signal across a small
# forward-looking range.
VERSION_MATRIX: Final[tuple[PythonVersionTarget, ...]] = (
    PythonVersionTarget(
        key="lowest_supported",
        version="3.12",
        description="Lowest supported Python version for YIDL study runs",
    ),
    PythonVersionTarget(
        key="mainstream_current",
        version="3.13",
        description="Mainstream/current Python version for YIDL study runs",
    ),
    PythonVersionTarget(
        key="newer_stable",
        version="3.14",
        description="Newer stable Python version for YIDL study runs",
    ),
    PythonVersionTarget(
        key="newer_candidate",
        version="3.15",
        description="Newer Python version likely to matter for optimization decisions",
    ),
)
