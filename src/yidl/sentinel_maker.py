from __future__ import annotations

from collections.abc import Callable
import inspect
import pickle


try:
    from sentinellib import Sentinel as _Pep661Sentinel
except Exception:  # pragma: no cover - depends on Python version.
    _Pep661Sentinel = None


_RegistryKey = tuple[str, str]
_REGISTRY: dict[_RegistryKey, object] = {}


class _FallbackSentinel:
    """Small PEP-661-like sentinel that preserves identity through pickle."""

    __slots__ = ("_name", "_module_name")

    def __init__(self, name: str, module_name: str) -> None:
        object.__setattr__(self, "_name", name)
        object.__setattr__(self, "_module_name", module_name)

    @property
    def name(self) -> str:
        return self._name

    @property
    def module_name(self) -> str:
        return self._module_name

    def __repr__(self) -> str:
        return self._name

    def __setattr__(self, name: str, value: object) -> None:
        raise AttributeError(f"{type(self).__name__} is immutable")

    def __reduce__(self) -> tuple[Callable[[str, str], object], tuple[str, str]]:
        return (_restore_sentinel, (self._name, self._module_name))


class SentinelNamespace:
    """Attribute-based sentinel factory.

    ``sentinels.MISSING`` returns a process-unique sentinel named ``MISSING``.
    Repeated access returns the same object, and the fallback implementation
    round-trips through pickle with identity preserved.
    """

    __slots__ = ("_module_name",)

    def __init__(self, module_name: str | None = None) -> None:
        self._module_name = module_name or _caller_module_name()

    def __getattr__(self, name: str) -> object:
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        return make_sentinel(name, module_name=self._module_name)

    def __call__(self, name: str) -> object:
        return make_sentinel(name, module_name=self._module_name)


def make_sentinel(name: str, *, module_name: str | None = None) -> object:
    """Return a unique sentinel for ``module_name`` and ``name``.

    If Python exposes the PEP 661 sentinel implementation, use it when it
    preserves pickle identity. Otherwise use the local fallback.
    """

    _validate_name(name)
    resolved_module = module_name or _caller_module_name()
    key = (resolved_module, name)
    sentinel = _REGISTRY.get(key)
    if sentinel is not None:
        return sentinel

    sentinel = _make_pep661_sentinel(name, resolved_module)
    if sentinel is None:
        sentinel = _FallbackSentinel(name, resolved_module)
    _REGISTRY[key] = sentinel
    return sentinel


def _restore_sentinel(name: str, module_name: str) -> object:
    return make_sentinel(name, module_name=module_name)


def _make_pep661_sentinel(name: str, module_name: str) -> object | None:
    if _Pep661Sentinel is None:
        return None

    attempts = (
        lambda: _Pep661Sentinel(name, module_name=module_name),
        lambda: _Pep661Sentinel(name, module=module_name),
        lambda: _Pep661Sentinel(name),
    )
    for attempt in attempts:
        try:
            sentinel = attempt()
        except TypeError:
            continue
        except Exception:
            return None
        if _pickle_preserves_identity(sentinel):
            return sentinel
    return None


def _pickle_preserves_identity(value: object) -> bool:
    try:
        return pickle.loads(pickle.dumps(value)) is value
    except Exception:
        return False


def _caller_module_name() -> str:
    frame = inspect.currentframe()
    if frame is None:
        return __name__
    caller = frame.f_back.f_back if frame.f_back is not None else None
    if caller is None:
        return __name__
    return caller.f_globals.get("__name__", __name__)


def _validate_name(name: str) -> None:
    if not isinstance(name, str):
        raise TypeError("sentinel name must be a string")
    if not name:
        raise ValueError("sentinel name must not be empty")


sentinels = SentinelNamespace(__name__)
