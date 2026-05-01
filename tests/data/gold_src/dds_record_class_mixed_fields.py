from __future__ import annotations

from support.golden_case import run_case
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import _emit_record_class_source


def render_case() -> str:
    dds = DataDefinitionSystem()
    init = dds.property("Init", bool, default=True, storage_name="init")
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    payload = dds.property("Payload", object, default=None, storage_name="payload")
    record_spec = dds.record("FieldSpec", init, name, payload)

    return _emit_record_class_source(record_spec)


if __name__ == "__main__":
    raise SystemExit(run_case("dds_record_class_mixed_fields.py", render_case))
