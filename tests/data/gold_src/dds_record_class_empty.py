from __future__ import annotations

from support.golden_case import run_case
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import _emit_record_class_source


def render_case() -> str:
    dds = DataDefinitionSystem()
    record_spec = dds.record("Empty")

    return _emit_record_class_source(record_spec)


if __name__ == "__main__":
    raise SystemExit(run_case("dds_record_class_empty.py", render_case))
