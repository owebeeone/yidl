"""Live captures stay in independent namespaces; they never become literal reprs."""

from __future__ import annotations

import ast
from dataclasses import dataclass
import json

from yidl.concept_parser import compile_yidl_files
from yidl.generation.data_def_sys import emit_concept_runtime_source, from_literal

SOURCE = """
concept Captures {
    resource Root = code $[
        class class_name__astichi_arg__:
            def value(self):
                return default_name__astichi_arg__
            def call(self):
                return callback_name__astichi_arg__()
    ]$ { keep value, call }
    production RootProduction -> composable {
        root Root = Root {
            ident class_name = "Box"
            ident default_name = "_default"
            ident callback_name = "_callback"
        }
    }
    assembly Module = RootProduction
}
"""


@dataclass(frozen=True)
class Opaque:
    label: str

    def __repr__(self) -> str:
        raise AssertionError("opaque capture must never be rendered")


def run() -> str:
    concept = compile_yidl_files({"captures.yidl": SOURCE}, "captures.yidl").concepts[
        "Captures"
    ]
    runtime = emit_concept_runtime_source(
        concept.plan.build_data_definition(),
        resources=concept.resources,
        assembly_plan=concept,
    )
    schema: dict[str, object] = {}
    exec(runtime, schema)
    tree = schema["build_Module"](schema["new_builder"]().freeze()).to_executable_ast()
    code = compile(tree, "capture_model.py", "exec")
    calls: list[str] = []
    first, second = Opaque("first"), Opaque("second")

    def callback_one() -> object:
        calls.append("one")
        return first

    def callback_two() -> object:
        calls.append("two")
        return second

    namespaces = [
        {"_default": first, "_callback": callback_one},
        {"_default": second, "_callback": callback_two},
    ]
    for namespace in namespaces:
        exec(code, namespace)
    assert calls == []
    assert namespaces[0]["Box"]().value() is first
    assert namespaces[1]["Box"]().value() is second
    assert namespaces[0]["Box"]().call() is first
    assert namespaces[1]["Box"]().call() is second
    assert calls == ["one", "two"]
    assert namespaces[0]["Box"] is not namespaces[1]["Box"]
    wrapper = from_literal(("one", 2))
    assert wrapper.to_generator() is wrapper.to_generator()
    try:
        from_literal(first)
    except TypeError as error:
        assert "unsupported matcher literal type" in str(error)
    else:
        raise AssertionError("opaque literal should reject")
    return ast.unparse(tree) + "\n"


if __name__ == "__main__":
    print(run(), end="")
    print(
        json.dumps(
            {
                "capture_isolation": True,
                "generation_calls": 0,
                "runtime_calls": ["one", "two"],
            },
            sort_keys=True,
        )
    )
