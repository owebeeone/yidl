from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from types import SimpleNamespace

import black

from support.golden_case import run_multi_source_case
from yidl.concept_parser import compile_yidl_files
from yidl.generation.data_def_sys import emit_concept_runtime_source
from yidl.runtime.lifecycle import _build_lifecycle_container
from yidl.runtime.lifecycle import _strip_redundant_pass_statements
from yidl.runtime.lifecycle import classvar
from yidl.runtime.lifecycle import const
from yidl.runtime.lifecycle import harvest_lifecycle_definition
from yidl.runtime.lifecycle import initvar
from yidl.runtime.lifecycle import lifecycle
from yidl.runtime.lifecycle import managed

YIDL_FIXTURE_DIR = Path("tests/data/yidl/yidl_transactional_lifecycle")
YIDL_PATHS = (
    YIDL_FIXTURE_DIR / "lifecycle_core.yidl",
    YIDL_FIXTURE_DIR / "lifecycle_managed.yidl",
    YIDL_FIXTURE_DIR / "lifecycle_default_factories.yidl",
    YIDL_FIXTURE_DIR / "lifecycle_transient.yidl",
    YIDL_FIXTURE_DIR / "lifecycle_owned.yidl",
    YIDL_FIXTURE_DIR / "lifecycle_const_static.yidl",
    YIDL_FIXTURE_DIR / "lifecycle_local_store.yidl",
    YIDL_FIXTURE_DIR / "lifecycle_base.yidl",
)
ENTRY_PATH = YIDL_FIXTURE_DIR / "lifecycle_base.yidl"


def render_case() -> Mapping[str, str]:
    decorator_source = _decorator_source()
    output_source = _generate_lifecycle_source(
        decorator_source,
        harvest_lifecycle_definition(_fixture_class()),
    )
    inherited_output_source = _generate_lifecycle_source(
        decorator_source,
        harvest_lifecycle_definition(_derived_fixture_class()),
    )
    return {
        "decorator.py": decorator_source,
        "decorator_prettier.py": _prettier_source(decorator_source),
        "generated_output.py": output_source,
        "generated_output_prettier.py": _prettier_source(output_source),
        "generated_inherited_output.py": inherited_output_source,
        "generated_inherited_output_prettier.py": _prettier_source(
            inherited_output_source,
        ),
    }


def validate_case(sources: Mapping[str, str]) -> None:
    decorator_namespace: dict[str, object] = {}
    exec(sources["decorator.py"], decorator_namespace)
    assert "LifecycleClass" in decorator_namespace
    assert "build_LifecycleModule" in decorator_namespace

    output_namespace: dict[str, object] = {}
    exec(sources["generated_output.py"], output_namespace)
    output_prettier_namespace: dict[str, object] = {}
    exec(sources["generated_output_prettier.py"], output_prettier_namespace)
    inherited_output_namespace: dict[str, object] = {}
    exec(sources["generated_inherited_output.py"], inherited_output_namespace)
    inherited_output_prettier_namespace: dict[str, object] = {}
    exec(
        sources["generated_inherited_output_prettier.py"],
        inherited_output_prettier_namespace,
    )

    _assert_generated_class(output_namespace)
    _assert_generated_class(output_prettier_namespace)
    _assert_inherited_generated_class(inherited_output_namespace)
    _assert_inherited_generated_class(inherited_output_prettier_namespace)
    _assert_decorator_frontend()
    _assert_source_shape(sources)


def _decorator_source() -> str:
    concept = compile_yidl_files(
        {path.as_posix(): path.read_text(encoding="utf-8") for path in YIDL_PATHS},
        ENTRY_PATH.as_posix(),
    ).concepts["LifecycleBase"]
    return emit_concept_runtime_source(
        concept.plan.build_data_definition(),
        resources=concept.resources,
        assembly_plan=concept,
    )


def _generate_lifecycle_source(
    decorator_source: str,
    harvested: object,
) -> str:
    namespace: dict[str, object] = {}
    exec(decorator_source, namespace)
    generated = SimpleNamespace(**namespace)
    source = namespace["build_LifecycleModule"](
        _build_lifecycle_container(generated, harvested),
    ).emit_commented()
    return _strip_redundant_pass_statements(source)


def _fixture_class() -> type[object]:
    class Example:
        SCALE: int = classvar(default=10)
        v1: int
        owner: str = const(default="owner")
        owner_tag: str = const(
            default_factory=lambda self: self.owner + "-tag",
            allow_self_factory=True,
        )
        seed: int = initvar(init=False, default=4)
        class_name_size: int = initvar(
            init=False,
            default_factory=lambda cls: len(cls.__name__),
        )
        self_tag_size: int = initvar(
            init=False,
            default_factory=lambda self: len(self.owner),
            allow_self_factory=True,
        )
        temp: int = initvar(
            init=False,
            default_factory=lambda seed, v1: seed + v1,
        )
        v2: int = managed(default_factory=lambda v1: v1 + 2)
        v3: int = managed(default_factory=lambda v2, v1: v1 + v2 + 2)
        v4: int = managed(init=False, default_factory=lambda v3: v3 * 2)
        v5: int = managed(
            init=False,
            default_factory=lambda class_name_size, self_tag_size, SCALE, v4: (
                class_name_size + self_tag_size + SCALE + v4
            ),
        )

    return Example


def _base_fixture_class() -> type[object]:
    class Base:
        v1: int = managed(default=2)

    return Base


def _derived_fixture_class() -> type[object]:
    Base = lifecycle(_base_fixture_class())

    class Derived(Base):
        v2: int = managed(default_factory=lambda v1: v1 + 5)

    return Derived


def _assert_generated_class(namespace: Mapping[str, object]) -> None:
    example_cls = _fixture_class()
    harvested = harvest_lifecycle_definition(example_cls)
    generated = namespace["build_lifecycle_class"](
        example_cls,
        **dict(harvested.build_kwargs),
    )
    _assert_example_class(generated)


def _assert_example_class(generated: type[object]) -> None:
    item = generated(v1=1)
    assert generated.SCALE == 10
    assert item.v1 == 1
    assert item.owner == "owner"
    assert item.owner_tag == "owner-tag"
    assert item.v2 == 3
    assert item.v3 == 6
    assert item.v4 == 12
    assert item.v5 == 34
    assert not hasattr(item._y_state, "_y_seed_value")
    assert not hasattr(item._y_state, "_y_class_name_size_value")
    assert not hasattr(item._y_state, "_y_self_tag_size_value")
    assert not hasattr(item._y_state, "_y_temp_value")

    explicit = generated(v1=1, v2=20, v3=30)
    assert explicit.v2 == 20
    assert explicit.v3 == 30
    assert explicit.v4 == 60
    assert explicit.v5 == 82


def _assert_inherited_generated_class(namespace: Mapping[str, object]) -> None:
    derived_cls = _derived_fixture_class()
    harvested = harvest_lifecycle_definition(derived_cls)
    generated = namespace["build_lifecycle_class"](
        derived_cls,
        **dict(harvested.build_kwargs),
    )
    _assert_inherited_class(generated)


def _assert_inherited_class(generated: type[object]) -> None:
    item = generated()
    assert item.v1 == 2
    assert item.v2 == 7

    explicit = generated(v1=10)
    assert explicit.v1 == 10
    assert explicit.v2 == 15


def _assert_decorator_frontend() -> None:
    generated = lifecycle(_fixture_class())
    _assert_example_class(generated)

    inherited = lifecycle(_derived_fixture_class())
    _assert_inherited_class(inherited)


def _assert_source_shape(sources: Mapping[str, str]) -> None:
    combined = "\n".join(sources.values())
    assert "locals()" not in combined
    assert "default_factories=" not in combined
    assert "default_factories[" not in combined

    source = sources["generated_output.py"]
    assert "_Example_owner_tag_default_factory(self=self)" in source
    assert "_Example_v2_default_factory(v1=self.v1)" in source
    assert "_Example_v3_default_factory(v2=self.v2, v1=self.v1)" in source
    assert "_Example_v4_default_factory(v3=self.v3)" in source
    assert "_Example_class_name_size_default_factory(cls=decorated_cls)" in source
    assert "_Example_self_tag_size_default_factory(self=self)" in source
    assert (
        "_Example_v5_default_factory("
        "class_name_size=class_name_size, self_tag_size=self_tag_size, "
        "SCALE=self.SCALE, v4=self.v4)"
    ) in source

    inherited_source = sources["generated_inherited_output.py"]
    assert "_Derived_v2_default_factory(v1=self.v1)" in inherited_source


def _prettier_source(source: str) -> str:
    return black.format_str(source, mode=black.FileMode())


if __name__ == "__main__":
    raise SystemExit(
        run_multi_source_case(
            "yidl_transactional_phase_c_default_factories.py",
            render_case,
            validate_case,
        )
    )
