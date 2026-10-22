# Python APIs and the existing CLI

## Current concept compiler

The executable tutorial uses these entrypoints:

```python
from yidl.concept_parser import compile_yidl_files, parse_yidl_source
from yidl.generation.data_def_sys import emit_concept_runtime_source

module = compile_yidl_files(source_map, entry_name)
concept = module.concepts[concept_name]
runtime_source = emit_concept_runtime_source(
    concept.plan.build_data_definition(),
    resources=concept.resources,
    assembly_plan=concept,
)
```

`source_map` maps logical names to text; `entry_name` is one of its keys.
`parse_yidl_source(path, source)` parses one source to a Lark tree; compilation
also resolves imports and symbols. The compiled module exposes named concepts;
choose the one you intend to emit.

Execute trusted runtime source into a fresh namespace. It exposes concrete record
classes, `<Name>Collection` descriptors, `new_builder()` and assembly entrypoints.
Use generated storage keywords for records. `build_<Assembly>(container)` returns
a composable; `to_executable_ast()` returns final Python AST; compiling/executing
that AST creates user classes. `emit_commented()` is an inspection surface.
`emit_container_runtime_source(dds)` emits a DDS library when there is no concept
assembly plan. Recorded concept plans also offer runtime emission/loading for
Python-authored definitions.

This API route is demonstrated end-to-end, rather than a new CLI invented for
the documentation. Internal `ASSEMBLY_*` metadata and path helpers are useful for
diagnostics but not a blanket long-term stability promise.

## Legacy command

```sh
yidl-compile --help
```

The installed command describes a lifecycle transducer meta-compiler and accepts
`spec_file` and `--out`/`-o`. It lexes/parses the older transducer syntax and emits
helper/API definitions. It is **not the braced concept compiler** and should not
be used to compile `classes.yidl`. The command's existence does not imply
`yidl-compile build`, `--write`, `--trace`, or concept-specific flags.

Top-level old parser exports and the designed `yidl.embed(...)` bootstrap must
not be mistaken for the current tutorial API. `yidl.embed` is not implemented as
a usable current entrypoint. No API removal or replacement was performed by this
documentation task.
