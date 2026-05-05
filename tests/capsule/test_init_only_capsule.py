from __future__ import annotations

import ast
import inspect

import pytest

from yidl.capsule.init_only_capsule import (
    compile_init_only_capsule,
    field_spec,
    InitOnlyFieldSpec,
    ResolvedInitField,
    render_init_only_class,
)


def test_field_spec_records_init_and_default_options() -> None:
    spec = field_spec(init=False, default="cold")

    assert isinstance(spec, InitOnlyFieldSpec)
    assert spec.init is False
    assert spec.default == "cold"


def test_render_init_only_class_builds_plain_python_init() -> None:
    source = render_init_only_class(
        "Counter",
        (
            ResolvedInitField(
                field_name="count",
                field_anno=int,
                init=True,
                default=0,
            ),
            ResolvedInitField(
                field_name="label",
                field_anno=str,
                init=False,
                default="cold",
            ),
            ResolvedInitField(
                field_name="required",
                field_anno=int,
                init=True,
            ),
        ),
    )

    assert ast.unparse(ast.parse(source)) == (
        "class Counter:\n\n"
        "    def __init__(self, *, count: int=0, required: int):\n"
        "        self.count = count\n"
        "        self.label = 'cold'\n"
        "        self.required = required"
    )


def test_render_init_only_class_rejects_hidden_field_without_default() -> None:
    with pytest.raises(ValueError, match="missing initial value for field 'label'"):
        render_init_only_class(
            "Counter",
            (
                ResolvedInitField(
                    field_name="label",
                    field_anno=str,
                    init=False,
                ),
            ),
        )


def test_compile_init_only_capsule_builds_decorator_from_field_spec_definitions() -> None:
    init_only = compile_init_only_capsule()

    @init_only
    class Example:
        count: int = field_spec(init=True, default=1)
        label: str = field_spec(init=False, default="cold")

    assert Example.__name__ == "Example"
    assert Example.__yidl_class_definition__.class_name == "Example"
    assert Example.__yidl_class_definition__.wrapped_class is Example.__wrapped__
    assert [field.field_name for field in Example.__yidl_class_definition__.fields] == [
        "count",
        "label",
    ]
    assert "def make_wrapper_class(class_definition):" in Example.__yidl_factory_source__
    assert "_y_wrapped_class =" in Example.__yidl_factory_source__
    assert "_y_count_anno =" in Example.__yidl_factory_source__
    assert "_y_count_default =" in Example.__yidl_factory_source__
    assert "_y_label_default =" in Example.__yidl_factory_source__
    assert "class Example(_y_wrapped_class):" in Example.__yidl_factory_source__
    assert "self.label = _y_label_default" in Example.__yidl_factory_source__

    defaulted = Example()
    overridden = Example(count=3)

    assert defaulted.count == 1
    assert defaulted.label == "cold"
    assert overridden.count == 3
    assert overridden.label == "cold"
    assert tuple(inspect.signature(Example).parameters) == ("count",)


def test_compile_init_only_capsule_rejects_hidden_field_without_default_at_decoration_time() -> None:
    init_only = compile_init_only_capsule()

    with pytest.raises(ValueError, match="missing initial value for field 'label'"):

        @init_only
        class Example:
            label: str = field_spec(init=False)
            pass
