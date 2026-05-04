from __future__ import annotations

from support.golden_case import run_case
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import from_literal


FullRange = from_literal({"range": "full"})
SegmentRange = from_literal({"range": "segments"})
OddRange = from_literal({"range": "odd"})
DefaultRange = from_literal({"range": "default"})


def _build_matcher():
    dds = DataDefinitionSystem()
    props = tuple(
        dds.property(f"P{index}", int, default=REQUIRED, storage_name=f"p{index}")
        for index in range(10)
    )
    record_spec = dds.record("RangeRecord", *props)
    records = dds.collection(
        "RangeRecords",
        record_spec,
        cardinality=dds.many,
        identity=props[0],
    )
    matcher = dds.matcher("Range")
    record = matcher.input("record", records)
    refs = tuple(record.prop(prop) for prop in props)
    matcher.default(DefaultRange)
    matcher.rule(
        name="full",
        when=tuple(ref.eq(index) for index, ref in enumerate(refs)),
        resource=FullRange,
    )
    matcher.rule(
        name="segments",
        when=(
            refs[0].eq(0),
            refs[1].eq(1),
            refs[4].eq(4),
            refs[5].eq(5),
            refs[8].eq(8),
            refs[9].eq(9),
        ),
        resource=SegmentRange,
    )
    matcher.rule(
        name="odd",
        when=tuple(refs[index].eq(index) for index in (1, 3, 5, 7, 9)),
        resource=OddRange,
    )
    return matcher, record_spec


def render_case() -> str:
    matcher, _ = _build_matcher()
    return matcher.emit_runtime_source(
        class_name="RangeMatcher",
    )


def validate_case(source: str) -> None:
    _, record_spec = _build_matcher()
    namespace = {}
    exec(source, namespace)
    runtime = namespace["RangeMatcher"]()

    full_record = record_spec.record(**{f"p{index}": index for index in range(10)})
    segment_values = {f"p{index}": index + 100 for index in range(10)}
    for index in (0, 1, 4, 5, 8, 9):
        segment_values[f"p{index}"] = index
    segment_record = record_spec.record(**segment_values)
    odd_values = {f"p{index}": index + 100 for index in range(10)}
    for index in (1, 3, 5, 7, 9):
        odd_values[f"p{index}"] = index
    odd_record = record_spec.record(**odd_values)
    default_record = record_spec.record(**{f"p{index}": index + 100 for index in range(10)})

    full_result = runtime.resolve(full_record)
    segment_result = runtime.resolve(segment_record)
    odd_result = runtime.resolve(odd_record)
    default_result = runtime.resolve(default_record)

    assert full_result.resource == FullRange
    assert full_result.rule == "full"
    assert full_result.score == 10.0
    assert segment_result.resource == SegmentRange
    assert segment_result.rule == "segments"
    assert segment_result.score == 6.0
    assert odd_result.resource == OddRange
    assert odd_result.rule == "odd"
    assert odd_result.score == 5.0
    assert default_result.resource == DefaultRange
    assert default_result.rule is None
    assert source.index("values[0:10]") < source.index("values[0:2] + values[4:6] + values[8:10]")
    assert "values[1:2] + values[3:4] + values[5:6] + values[7:8] + values[9:10]" in source
    assert "astichi_hole" not in source


if __name__ == "__main__":
    raise SystemExit(run_case("matcher_runtime_ranges.py", render_case, validate_case))
