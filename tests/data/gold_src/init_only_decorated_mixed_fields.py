from __future__ import annotations

from support.golden_case import run_case
from yidl.capsule.init_only_capsule import compile_init_only_capsule, field_spec


def render_case() -> str:
    init_only = compile_init_only_capsule()

    @init_only
    class Session:
        required: int = field_spec(init=True)
        token: str = field_spec(init=True, default="seed")
        label: str = field_spec(init=False, default="cold")

    return Session.__yidl_factory_source__


if __name__ == "__main__":
    raise SystemExit(run_case("init_only_decorated_mixed_fields.py", render_case))
