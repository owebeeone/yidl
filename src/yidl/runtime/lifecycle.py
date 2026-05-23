"""Compatibility shim for lifecycle runtime APIs.

The lifecycle implementation lives in ``yidl_lifecycle``. This module preserves
the historical ``yidl.runtime.lifecycle`` import path during extraction.
"""

from yidl_lifecycle.lifecycle import *  # noqa: F401,F403
from yidl_lifecycle.lifecycle import _build_lifecycle_container
from yidl_lifecycle.lifecycle import _generate_lifecycle_source
from yidl_lifecycle.lifecycle import _HAS_DEFAULT_FACTORY

