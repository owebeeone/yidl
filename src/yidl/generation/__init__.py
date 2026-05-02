"""Generation-system interfaces for YIDL."""

from yidl.generation.data_def_sys import ComputedValue
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import MatcherSpec
from yidl.generation.data_def_sys import NOT_PROVIDED
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import emit_matcher_runtime_source

__all__ = [
    "ComputedValue",
    "DataDefinitionSystem",
    "MatcherSpec",
    "NOT_PROVIDED",
    "REQUIRED",
    "emit_matcher_runtime_source",
]
