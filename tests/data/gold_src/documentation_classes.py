"""Canonical snapshots; behavior assertions live in the executable tutorial."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
import runpy

from support.golden_case import run_multi_source_case


def render_case() -> Mapping[str, str]:
    tutorial = runpy.run_path(str(Path("example/documentation/generate.py")))
    generate = tutorial["generate"]
    result: dict[str, str] = {}
    for name, options in (
        ("first", {}),
        ("extended", {"extended": True}),
        ("empty", {"empty": True}),
        ("disabled", {"disabled": True}),
    ):
        output = generate(**options)
        result[f"{name}_model.py"] = output.model
    captures = runpy.run_path("example/documentation/captures.py")
    result["captures_model.py"] = captures["run"]()
    for name in ("control_flow", "comparison"):
        recipe = runpy.run_path(f"example/documentation/{name}.py")
        result[f"{name}_model.py"] = recipe["run"]()
    return result


if __name__ == "__main__":
    raise SystemExit(run_multi_source_case("documentation_classes.py", render_case))
