"""Hand-crafted generator for ``_yidl.py``-shape snippets via astichi.

This file is the first concrete step toward a real ``_yidl.py`` generator:
per-field, per-lifecycle-point snippets written as astichi composables that
can be spliced into a parent class shell to produce the full generated
facade+state module.

The end-to-end target is ``MultiTxMultiCounter`` (see
``lifeycle_examples.py``): the generator should consume the ``FieldSpec``
list for that class and emit the full generated module. This file carves
out one coordinate of that matrix at a time — currently
``ManagedComposables.commit`` — and demos it end-to-end via astichi.

Shape assumptions (MVP, aligned with the generated-strategy-A backend):

- Each field has two slots on the state object: ``<name>_current`` and
  ``<name>_working``. Uninitialised slots hold the module-private
  ``_VOID`` sentinel (identity compared).
- Commit promotes ``<name>_working`` into ``<name>_current`` when it is
  not ``_VOID``, then resets ``<name>_working`` to ``_VOID``.
- Contributions are spliced into a parent ``_commit_transaction`` body
  via an ``astichi_hole(commit_body)`` marker. The parent binds ``s``
  (``s = self._state``) before the hole; contributions read it as a free
  ``Load`` and the hygiene pass threads it through.

Start here for the ``managed`` + ``commit`` shape. Extend file-local
classes as each new (kind, lifecycle-point) coordinate is fleshed out.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Hashable
from dataclasses import dataclass
from typing import Any

import astichi
from astichi.model import BasicComposable


# ---------------------------------------------------------------------------
# FieldSpec: minimal subset of ``pyrolyze.lifecycle.FieldSpec`` — just what
# the generator needs to emit snippets for the MVP. Extend as additional
# lifecycle points come online (``compare``, ``freeze``/``thaw``, etc.).
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FieldSpec:
    name: str
    kind: str
    tx_key: Hashable = "default"
    default: Any = None
    default_factory: Any = None


# ---------------------------------------------------------------------------
# Composables ABC: per-kind bundle of astichi snippets, one method per
# lifecycle splice point. Each method takes a ``FieldSpec`` and returns a
# ``BasicComposable`` that can be added into the outer build tree.
#
# Only the coordinates we have locked in get a concrete implementation
# here; every other method raises ``NotImplementedError`` so a caller
# accidentally asking for an unfinished snippet fails loudly.
# ---------------------------------------------------------------------------


class Composables(ABC):
    """Per-kind snippet bundle for the generator."""

    @abstractmethod
    def init(self, spec: FieldSpec) -> BasicComposable:
        """State-object slot initialisation in the state ``__init__``."""

    @abstractmethod
    def get(self, spec: FieldSpec) -> BasicComposable:
        """Facade ``@property`` getter body."""

    @abstractmethod
    def set(self, spec: FieldSpec) -> BasicComposable:
        """Facade ``@<prop>.setter`` body."""

    @abstractmethod
    def commit(self, spec: FieldSpec) -> BasicComposable:
        """Inline contribution spliced into ``_commit_transaction`` body."""

    @abstractmethod
    def rollback(self, spec: FieldSpec) -> BasicComposable:
        """Inline contribution spliced into ``_rollback_transaction`` body."""


class ManagedComposables(Composables):
    """Snippets for the ``managed`` kind (overlay-stored, default-backed).

    Only ``commit`` is implemented for now. Other methods raise so the
    generator's scope remains honest.
    """

    def init(self, spec: FieldSpec) -> BasicComposable:
        raise NotImplementedError("ManagedComposables.init not yet implemented")

    def get(self, spec: FieldSpec) -> BasicComposable:
        raise NotImplementedError("ManagedComposables.get not yet implemented")

    def set(self, spec: FieldSpec) -> BasicComposable:
        raise NotImplementedError("ManagedComposables.set not yet implemented")

    def commit(self, spec: FieldSpec) -> BasicComposable:
        """Emit::

            if s.<name>_working is not _VOID:
                s.<name>_current = s.<name>_working
                s.<name>_working = _VOID

        ``s`` and ``_VOID`` are free ``Load``s — they resolve to the parent
        method's local ``s = self._state`` and to the generated module's
        ``_VOID`` sentinel respectively after hygiene.
        """
        current_path = f"s.{spec.name}_current"
        working_path = f"s.{spec.name}_working"
        return astichi.compile(
            f"if astichi_ref({working_path!r}) is not _VOID:\n"
            f"    astichi_ref({current_path!r}).astichi_v = astichi_ref({working_path!r})\n"
            f"    astichi_ref({working_path!r}).astichi_v = _VOID\n"
        )

    def rollback(self, spec: FieldSpec) -> BasicComposable:
        raise NotImplementedError("ManagedComposables.rollback not yet implemented")


# ---------------------------------------------------------------------------
# Dispatch table: map ``FieldSpec.kind`` tags to their ``Composables``
# implementation. Callers look up by tag rather than by class to keep the
# call sites stable as the set of kinds grows.
# ---------------------------------------------------------------------------


COMPOSABLES_BY_KIND: dict[str, Composables] = {
    "managed": ManagedComposables(),
}


def snippet_for(
    spec: FieldSpec,
    method: str,
) -> BasicComposable:
    """Return the snippet for ``(spec.kind, method)`` bound to ``spec``."""
    composables = COMPOSABLES_BY_KIND[spec.kind]
    return getattr(composables, method)(spec)


# ---------------------------------------------------------------------------
# Demo / smoke: compose a full ``_commit_transaction`` body from N managed
# field specs and print the emitted source. Running this module is the
# fastest way to eyeball whether the snippet shape is what we want.
# ---------------------------------------------------------------------------


_PARENT_COMMIT_SRC = (
    "class _Generated:\n"
    "    def _commit_transaction(self, tx_id):\n"
    "        s = self._state\n"
    "        if s.working_tx_id != tx_id:\n"
    "            return self\n"
    "        astichi_hole(commit_body)\n"
    "        s.working_tx_id = None\n"
    "        return self\n"
)


def compose_commit_demo(specs: list[FieldSpec]) -> str:
    """Compose ``_commit_transaction`` with one ``commit`` contribution per
    spec and return the emitted source as a string."""
    builder = astichi.build()
    builder.add.Root(astichi.compile(_PARENT_COMMIT_SRC))
    for idx, spec in enumerate(specs):
        name = f"C{idx}"
        contribution = snippet_for(spec, "commit")
        builder.add.__getattr__(name)(contribution)
        builder.Root.commit_body.add.__getattr__(name)(order=idx)
    return builder.build(unroll=True).materialize().emit(provenance=False)


if __name__ == "__main__":
    demo_specs = [
        FieldSpec(name="key1_total", kind="managed", tx_key="key1"),
        FieldSpec(name="items", kind="managed", tx_key="key1"),
        FieldSpec(name="first_pass", kind="managed", tx_key="key1"),
    ]
    print("# Generated _commit_transaction shape for 3 managed fields:")
    print()
    print(compose_commit_demo(demo_specs))
