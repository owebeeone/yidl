from __future__ import annotations

import ast
import inspect

import pytest

from yidl.capsule import CapsuleSpecInstance
from yidl.capsule.init_only_capsule import (
    InitOnlyCapsule,
    build_init_only_capsule,
    compile_init_only_capsule,
    field_spec,
    render_init_only_class,
)


def test_init_only_capsule_extends_base_capsule_with_field_spec_and_init_method() -> None:
    built = build_init_only_capsule()

    assert built == InitOnlyCapsule
    assert [facade.name for facade in built.facades] == ["Main"]
    assert [prop.name for prop in built.properties] == [
        "Init",
        "Default",
        "FieldName",
        "FieldAnno",
    ]
    assert [prop.property_name for prop in built.properties] == [
        "init",
        "default",
        "field_name",
        "field_anno",
    ]
    assert [spec.name for spec in built.specs] == ["base_spec", "field_spec"]
    assert built.specs[1].property_names == (
        "FieldName",
        "FieldAnno",
        "Init",
        "Default",
    )
    assert [(method.facade_name, method.name) for method in built.methods] == [
        ("Main", "__init__")
    ]
    assert [surface.name for surface in built.methods[0].surfaces] == ["params", "body"]


def test_render_init_only_class_builds_plain_python_init() -> None:
    source = render_init_only_class(
        "Counter",
        (
            CapsuleSpecInstance.from_values(
                "field_spec",
                field_name="count",
                field_anno=int,
                init=True,
                default=0,
            ),
            CapsuleSpecInstance.from_values(
                "field_spec",
                field_name="label",
                field_anno=str,
                init=False,
                default="cold",
            ),
            CapsuleSpecInstance.from_values(
                "field_spec",
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
                CapsuleSpecInstance.from_values(
                    "field_spec",
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
