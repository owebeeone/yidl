from __future__ import annotations

import ast
from collections.abc import Callable, Sequence
from collections.abc import Mapping
from pathlib import Path
import shutil
import sys


Validation = Callable[[str], None]
MultiSourceValidation = Callable[[Mapping[str, str]], None]


def write_source(path: str | Path, source: str) -> None:
    if not source.endswith("\n"):
        source += "\n"
    if str(path) == "-":
        sys.stdout.write(source)
        return
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(source, encoding="utf-8")


def write_sources(path: str | Path, sources: Mapping[str, str]) -> None:
    if str(path) == "-":
        for name, source in sources.items():
            sys.stdout.write(f"# {name}\n")
            sys.stdout.write(source)
            if not source.endswith("\n"):
                sys.stdout.write("\n")
        return

    output_root = Path(path)
    if output_root.exists():
        if output_root.is_dir():
            shutil.rmtree(output_root)
        else:
            output_root.unlink()
    output_root.mkdir(parents=True, exist_ok=True)

    for name, source in sources.items():
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"invalid generated source path: {name!r}")
        write_source(output_root / relative, source)


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


def run_multi_source_case(
    case_name: str,
    render_case: Callable[[], Mapping[str, str]],
    validate: MultiSourceValidation | None = None,
    argv: Sequence[str] | None = None,
) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        raise SystemExit(
            f"usage: {case_name} <materialized-output-dir>"
        )

    materialized_sources = dict(render_case())
    if validate is not None:
        validate(materialized_sources)

    write_sources(args[0], materialized_sources)
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
