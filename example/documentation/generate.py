"""Generate Point(x, y) using installed YIDL and Astichi packages.

With no scenario flag, generate the two-field Point class. Choose at most one
scenario flag. Output paths are relative to the current working directory.
"""

from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
import inspect
import json
from pathlib import Path
import sys
from typing import Mapping

from astichi.lower_engine.native import select_effective_lower_engine
from yidl.concept_parser import compile_yidl_files
from yidl.generation.data_def_sys import emit_concept_runtime_source


@dataclass(frozen=True)
class Output:
    runtime: str
    model: str
    observations: Mapping[str, object]


def generate(
    *, extended: bool = False, empty: bool = False, disabled: bool = False
) -> Output:
    authority = Path(__file__).with_name("classes.yidl")
    module = compile_yidl_files({"classes.yidl": authority.read_text()}, "classes.yidl")
    concept = module.concepts["Classes"]
    runtime = emit_concept_runtime_source(
        concept.plan.build_data_definition(),
        resources=concept.resources,
        assembly_plan=concept,
    )
    schema: dict[str, object] = {}
    exec(compile(runtime, "generated_runtime.py", "exec"), schema)
    builder = schema["new_builder"]()
    classes = [("point", "Point", 10, () if empty else ("x", "y"))]
    if extended:
        classes.append(("size", "Size", 20, ("x",)))
    for identity, name, order, slots in classes:
        builder.add(
            schema["ClassesCollection"],
            schema["ClassRow"](
                class_id=identity,
                class_name=name,
                class_order=order,
                slot_names=slots,
                enable_init=not disabled,
            ),
        )
    # Reversed insertion order proves that FieldOrder owns parameter order.
    rows = (
        []
        if empty
        else [
            ("point.y", "point", "y", 20, True),
            ("point.x", "point", "x", 10, True),
            ("point.hidden", "point", "hidden", 30, False),
        ]
    )
    if extended:
        rows.extend(
            [("size.x", "size", "x", 10, True), ("orphan.z", "absent", "z", 99, True)]
        )
    for identity, owner, name, order, selected in rows:
        builder.add(
            schema["FieldsCollection"],
            schema["FieldRow"](
                field_id=identity,
                owner=owner,
                field_name=name,
                field_order=order,
                selected=selected,
            ),
        )
    facts = builder.freeze()
    composable = schema["build_Module"](facts)
    tree = composable.to_executable_ast()
    model = ast.unparse(tree) + "\n"
    namespace: dict[str, object] = {"__name__": "documentation_model"}
    exec(compile(tree, "generated_model.py", "exec"), namespace)
    point = namespace["Point"]
    if disabled:
        assert "__init__" not in point.__dict__
        result = {"init": "omitted"}
    elif empty:
        instance = point()
        assert point.__slots__ == ()
        assert not hasattr(instance, "__dict__")
        result = {"slots": []}
    else:
        instance = point(3, 4)
        assert (instance.x, instance.y) == (3, 4)
        assert not hasattr(instance, "__dict__")
        assert "hidden" not in model and "orphan" not in model
        assert list(inspect.signature(point).parameters) == ["x", "y"]
        assert "self.x = x" in model and "self.y = y" in model
        result = {"Point": [instance.x, instance.y], "parameters": ["x", "y"]}
    if extended:
        size = namespace["Size"](8)
        assert size.x == 8
        assert list(inspect.signature(namespace["Size"]).parameters) == ["x"]
        result["Size"] = size.x
    return Output(runtime, model, result)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("build/documentation"),
        help="Directory for runtime.py and model.py; relative to the current working directory",
    )
    parser.add_argument(
        "--extended",
        action="store_true",
        help="Generate Point(x, y) and Size(x)",
    )
    parser.add_argument(
        "--empty",
        action="store_true",
        help="Generate Point with no fields and a zero-parameter constructor",
    )
    parser.add_argument(
        "--disabled",
        action="store_true",
        help="Generate Point with slots but omit its __init__ method",
    )
    args = parser.parse_args()
    output = generate(extended=args.extended, empty=args.empty, disabled=args.disabled)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "runtime.py").write_text(output.runtime)
    (args.out / "model.py").write_text(output.model)
    print(
        json.dumps(
            {
                "python": sys.version.split()[0],
                "engine": select_effective_lower_engine().snapshot(),
                "observations": output.observations,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
