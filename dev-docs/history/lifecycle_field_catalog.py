"""
Catalog of pyrolyze.lifecycle field helper functions and keyword parameters.

Source of truth in code: ``pyrolyze/src/pyrolyze/lifecycle.py`` (``@define_kind``,
``helper_params`` chains, ``_PARAM_PRESETS``).

This module is static text so it stays importable without loading ``pyrolyze``
(which may require a newer Python than the host used for yidl tests).

Regenerate / verify when lifecycle adds kinds or parameters.
"""

from __future__ import annotations

from typing import Final

# Parameters referenced by LCKind.helper_params (see _PARAM_PRESETS for types/defaults).
COMMON_PARAM_NOTES: Final[str] = (
    "Factory/hook injectable names (when allowed): self, current, working; "
    "plus initvar names after initvar support lands. "
    "Hooks also: tx_group, previous (after_commit only). "
    "See lifecycle._SUPPORTED_FACTORY_PARAMS and _BEFORE_COMMIT_PARAMS / etc."
)

# Terminal helper name -> exposed keyword-only parameters (fixed params omitted).
FIELD_HELPERS: Final[dict[str, tuple[str, ...]]] = {
    "managed": (
        "compare",
        "tx_group",
        "default",
        "default_factory",
        "initial_working",
        "freeze",
        "thaw",
        "state_factory",
        "state_copy",
    ),
    "const": ("compare", "default", "default_factory"),
    "static": ("compare", "default", "default_factory"),
    "binding": ("tx_group", "default", "default_factory"),
    "owned": ("tx_group", "default", "default_factory"),
    "transient": (
        "compare",
        "default",
        "default_factory",
        "working_default_factory",
        "tx_group",
    ),
    "local_store": ("compare", "default", "default_factory"),
    "derived": ("compare", "default", "default_factory"),
    "initvar": ("init", "default", "default_factory"),
    "classvar": ("default", "default_factory"),
    # compare fixed to "value" at helper level; not a caller keyword.
    "commit_order_key": ("tx_group", "default", "default_factory"),
    # compare fixed "identity", init fixed False; not caller keywords.
    "commit_validator": ("tx_group", "default"),
    "on_before_commit": ("tx_group", "default"),
    "on_after_commit": ("tx_group", "default"),
    "on_after_rollback": ("tx_group", "default"),
}

# Order: implement / gain parity tests from top to bottom, prioritizing the
# managed/context spine before dependent or more specialized features.
IMPLEMENTATION_ORDER: Final[tuple[str, ...]] = (
    "infra_default_tx",
    "managed_single_group",
    "managed_advanced",
    "const",
    "static",
    "local_store",
    "derived",
    "multi_group_tx",
    "transient",
    "binding",
    "owned",
    "initvar_injection",
    "commit_order_key",
    "commit_validator",
    "on_before_commit",
    "on_after_commit",
    "on_after_rollback",
    "classvar",
    "lifecycle_field_escape",
)


def describe_feature(slug: str) -> str:
    """Human-readable one-liner for IMPL_PROGRESS rows."""
    return {
        "infra_default_tx": "Runtime: DEFAULT_TRANSACTION enlist, transaction commit/rollback path used by generated code",
        "managed_single_group": "managed: overlay, current/working/proxy, commit/rollback, freeze/thaw hooks",
        "managed_advanced": "managed: compare=identity, state_factory, state_copy",
        "multi_group_tx": "TransactionManager: multiple named groups, begin(group, ...), isolated dirty/validate/commit",
        "initvar_injection": "initvar + inject initvar names into default_factory / validators / hooks",
        "lifecycle_field_escape": "lifecycle_field low-level escape hatch / custom kinds (if in scope)",
    }.get(slug, slug.replace("_", " "))


def print_catalog() -> None:
    for name, params in sorted(FIELD_HELPERS.items()):
        print(f"{name}({', '.join(params)})")


if __name__ == "__main__":
    print_catalog()
