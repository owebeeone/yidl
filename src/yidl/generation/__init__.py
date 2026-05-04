"""Generation-system interfaces for YIDL."""

from yidl.generation.data_def_sys import AddIfAbsent
from yidl.generation.data_def_sys import ComputedValue
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import DDSContainer
from yidl.generation.data_def_sys import DDSContainerBuilder
from yidl.generation.data_def_sys import MatcherGeneratedValue
from yidl.generation.data_def_sys import MatcherSpec
from yidl.generation.data_def_sys import NOT_PROVIDED
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import RejectDuplicate
from yidl.generation.data_def_sys import ReplaceExisting
from yidl.generation.data_def_sys import emit_container_runtime_source
from yidl.generation.data_def_sys import emit_matcher_runtime_source
from yidl.generation.data_def_sys import from_astichi_code
from yidl.generation.data_def_sys import from_literal

__all__ = [
    "AddIfAbsent",
    "ComputedValue",
    "DataDefinitionSystem",
    "DDSContainer",
    "DDSContainerBuilder",
    "MatcherGeneratedValue",
    "MatcherSpec",
    "NOT_PROVIDED",
    "REQUIRED",
    "RejectDuplicate",
    "ReplaceExisting",
    "emit_container_runtime_source",
    "emit_matcher_runtime_source",
    "from_astichi_code",
    "from_literal",
]
