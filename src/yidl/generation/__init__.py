"""Generation-system interfaces for YIDL."""

from yidl.generation.data_def_sys import ComputedValue
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import DDSContainer
from yidl.generation.data_def_sys import DDSContainerBuilder
from yidl.generation.data_def_sys import MatcherSpec
from yidl.generation.data_def_sys import NOT_PROVIDED
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import emit_container_runtime_source
from yidl.generation.data_def_sys import emit_matcher_runtime_source

__all__ = [
    "ComputedValue",
    "DataDefinitionSystem",
    "DDSContainer",
    "DDSContainerBuilder",
    "MatcherSpec",
    "NOT_PROVIDED",
    "REQUIRED",
    "emit_container_runtime_source",
    "emit_matcher_runtime_source",
]
