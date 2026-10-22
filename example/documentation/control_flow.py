"""Compose ordered statements inside interacting Python compound constructs."""

from __future__ import annotations

import ast

from yidl.concept_parser import compile_yidl_files
from yidl.generation.data_def_sys import emit_concept_runtime_source

SOURCE = """
concept ControlFlow {
    property Label: str
    property Order: int
    record Action { Label Order }
    collection Actions: Action identity Label many
    resource Root = code $[
        from contextlib import nullcontext

        def identity(function):
            return function

        @identity
        def run(items, fail=False):
            events = []
            try:
                with nullcontext():
                    for item in items:
                        if item > 1:
                            astichi_hole(actions)
                        elif item == 1:
                            events.append("one")
                        else:
                            events.append("other")
                    else:
                        events.append("loop-else")
                    if fail:
                        raise ValueError("requested")
            except ValueError:
                events.append("caught")
            finally:
                events.append("finally")
            return events, [item * item for item in items]
    ]$ { keep run }
    resource ActionCode = template $[
        astichi_pass(events, outer_bind=True).append((astichi_pass(item, outer_bind=True), astichi_bind_external(label)))
    ]$
    resource Empty = template `pass`
    contribution ActionContribution = ActionCode {
        as Action
        index Order
        order Order
        target actions { build /Root }
        external label = Label
    }
    contribution EmptyContribution = Empty {
        as Empty
        target actions { build /Root }
    }
    matcher Selected(action: Actions) -> contribution {
        default -> ActionContribution
    }
    matcher EmptySelection() -> contribution {
        default -> EmptyContribution
    }
    production RootProduction -> composable {
        root Root = Root
        apply empty using EmptySelection
        apply actions from action: Actions using Selected
    }
    assembly Module = RootProduction
}
"""


def run() -> str:
    concept = compile_yidl_files({"control.yidl": SOURCE}, "control.yidl").concepts[
        "ControlFlow"
    ]
    runtime = emit_concept_runtime_source(
        concept.plan.build_data_definition(),
        resources=concept.resources,
        assembly_plan=concept,
    )
    schema: dict[str, object] = {}
    exec(runtime, schema)
    sources = []
    for labels in ((), ("first",), ("first", "second")):
        builder = schema["new_builder"]()
        for order, label in reversed(tuple(enumerate(labels))):
            builder.add(
                schema["ActionsCollection"], schema["Action"](label=label, order=order)
            )
        tree = schema["build_Module"](builder.freeze()).to_executable_ast()
        namespace: dict[str, object] = {}
        exec(compile(tree, "control_model.py", "exec"), namespace)
        events, squares = namespace["run"]([2, 1, 0])
        assert events == [(2, label) for label in labels] + [
            "one",
            "other",
            "loop-else",
            "finally",
        ]
        assert squares == [4, 1, 0]
        events, squares = namespace["run"]([3], fail=True)
        assert events == [(3, label) for label in labels] + [
            "loop-else",
            "caught",
            "finally",
        ]
        assert squares == [9]
        assert namespace["run"]([]) == (["loop-else", "finally"], [])
        sources.append(ast.unparse(tree) + "\n")
    return sources[-1]


if __name__ == "__main__":
    print(run(), end="")
