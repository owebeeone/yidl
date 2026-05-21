# Lifecycle Constructor Performance Fixtures

This directory contains the checked-in generated source used by the gated
lifecycle constructor throughput comparison. The fixture keeps the timed loop
focused on object construction and excludes one-time YIDL assembly and source
generation cost.

Regenerate the lifecycle fixture after changes to
`tests/data/yidl/yidl_transactional_lifecycle/lifecycle_base.yidl` or the
lifecycle source generator:

```sh
PYTHONPATH=../astichi/src uv run python tests/data/perf/generate_lifecycle_constructor_perf_fixture.py
```

Run the lifecycle-vs-dataclass constructor comparison:

```sh
PYTHONPATH=../astichi/src uv run --with pytest python tests/data/perf/run_lifecycle_constructor_perf_comparison.py
```

The comparison creates generated lifecycle classes and equivalent
`dataclasses.make_dataclass(..., slots=True)` classes for field group sizes
10, 50, and 100. Each size has the same number of plain fields, managed count
fields, and derived managed fields. The derived dataclass fields are initialized
in `__post_init__`; the lifecycle fields use generated parameterized
`default_factory` lowering.

The test is skipped during normal regression runs unless `YIDL_PERF_TESTS=1`
is set.
