from __future__ import annotations

from support.golden_case import run_case
from yidl.capsule.init_only_capsule import (
    class_definition_from_class,
    emit_init_only_factory_source,
    field_spec,
)


def render_case() -> str:
    class Example:
        count: int = field_spec(init=True, default=1)
        label: str = field_spec(init=False, default="cold")

    return emit_init_only_factory_source(class_definition_from_class(Example))


if __name__ == "__main__":
    raise SystemExit(run_case("init_only_decorator_source.py", render_case))
