from __future__ import annotations

import ast
from collections.abc import Callable, Sequence
from pathlib import Path
import sys


Validation = Callable[[str], None]


def write_source(path: str | Path, source: str) -> None:
    if not source.endswith("\n"):
        source += "\n"
    if str(path) == "-":
        sys.stdout.write(source)
        return
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(source, encoding="utf-8")


def run_case(
    case_name: str,
    render_case: Callable[[], str],
    validate: Validation | None = None,
    argv: Sequence[str] | None = None,
) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        raise SystemExit(
            f"usage: {case_name} <materialized-output.py>"
        )

    materialized_source = render_case()
    if validate is not None:
        validate(materialized_source)

    write_source(args[0], materialized_source)
    return 0


def extract_wrapped_class_source(factory_source: str) -> str:
    module = ast.parse(factory_source)
    if not module.body or not isinstance(module.body[0], ast.FunctionDef):
        raise TypeError("expected make_wrapper_class function source")
    factory = module.body[0]
    class_def = next(
        (statement for statement in factory.body if isinstance(statement, ast.ClassDef)),
        None,
    )
    if class_def is None:
        raise ValueError("factory source does not contain a generated class")
    class_module = ast.Module(body=[class_def], type_ignores=[])
    ast.fix_missing_locations(class_module)
    return ast.unparse(class_module)
