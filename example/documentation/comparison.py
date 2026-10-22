"""A bounded three-operand short-circuit recipe; not a general dataclass algorithm."""

from __future__ import annotations

import ast
from dataclasses import dataclass

from yidl.concept_parser import compile_yidl_files
from yidl.generation.data_def_sys import emit_concept_runtime_source

SOURCE = """
concept Comparison {
    property Name: str
    property Order: int
    property Last: bool
    record Operand { Name Order Last }
    collection Operands: Operand identity Name many
    resource Root = code $[
        def compare(left, right):
            astichi_hole(steps)
            return True
    ]$ { keep compare }
    resource Step = template $[
        result = astichi_pass(left, outer_bind=True).astichi_ref(external=path) == astichi_pass(right, outer_bind=True).astichi_ref(external=path)
        if not result:
            return result
    ]$
    resource Final = template $[
        return astichi_pass(left, outer_bind=True).astichi_ref(external=path) == astichi_pass(right, outer_bind=True).astichi_ref(external=path)
    ]$
    resource Empty = template `pass`
    contribution Next = Step {
        as Operand index Order order Order target steps { build /Root }
        external path = Name
    }
    contribution LastOperand = Final {
        as Operand index Order order Order target steps { build /Root }
        external path = Name
    }
    contribution EmptyOperand = Empty {
        as Empty target steps { build /Root }
    }
    matcher EmptySelection() -> contribution { default -> EmptyOperand }
    matcher Select(operand: Operands) -> contribution {
        default -> Next
        rule final when Last == True -> LastOperand
    }
    production RootProduction -> composable {
        root Root = Root
        apply empty using EmptySelection
        apply steps from operand: Operands using Select
    }
    assembly Module = RootProduction
}
"""


@dataclass
class Raw:
    truth: bool
    conversions: list[bool]

    def __bool__(self) -> bool:
        self.conversions.append(self.truth)
        return self.truth


@dataclass(frozen=True, eq=False)
class Value:
    name: str
    result: Raw
    events: list[str]

    def __eq__(self, other: object) -> object:
        self.events.append(self.name)
        return self.result


@dataclass
class Pair:
    first: object
    middle: object
    last: object


def run() -> str:
    concept = compile_yidl_files(
        {"comparison.yidl": SOURCE}, "comparison.yidl"
    ).concepts["Comparison"]
    runtime = emit_concept_runtime_source(
        concept.plan.build_data_definition(),
        resources=concept.resources,
        assembly_plan=concept,
    )
    schema: dict[str, object] = {}
    exec(runtime, schema)
    builder = schema["new_builder"]()
    for name, order, last in (
        ("last", 30, True),
        ("first", 10, False),
        ("middle", 20, False),
    ):
        builder.add(
            schema["OperandsCollection"],
            schema["Operand"](name=name, order=order, last=last),
        )
    tree = schema["build_Module"](builder.freeze()).to_executable_ast()
    namespace: dict[str, object] = {}
    exec(compile(tree, "comparison_model.py", "exec"), namespace)
    compare = namespace["compare"]
    events: list[str] = []
    yes, no, final = Raw(True, []), Raw(False, []), Raw(False, [])
    left = Pair(
        Value("first", no, events),
        Value("middle", yes, events),
        Value("last", final, events),
    )
    right = Pair(object(), object(), object())
    assert compare(left, right) is no
    assert events == ["first"] and no.conversions == [False]
    events.clear()
    left.first = Value("first", yes, events)
    assert compare(left, right) is final
    assert events == ["first", "middle", "last"]
    assert yes.conversions == [True, True] and final.conversions == []
    events.clear()
    # There is no implicit identity shortcut for shared/nonreflexive values.
    assert compare(left, left) is final
    assert events == ["first", "middle", "last"]
    empty_tree = schema["build_Module"](
        schema["new_builder"]().freeze()
    ).to_executable_ast()
    empty_namespace: dict[str, object] = {}
    exec(compile(empty_tree, "empty_comparison.py", "exec"), empty_namespace)
    assert empty_namespace["compare"](left, right) is True
    return ast.unparse(tree) + "\n"


if __name__ == "__main__":
    print(run(), end="")
