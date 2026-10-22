# YIDL

YIDL helps you write Python code generators. You describe the information a
generator needs, reusable pieces of Python code, and rules for choosing and
combining those pieces. Your Python program supplies the particular inputs and
runs generation to obtain classes or functions, which applications then use as
ordinary Python.

For example, field-name inputs `x` and `y` can produce a plain slotted Point class
whose constructor stores its arguments directly. Those generation inputs are
separate from the instance values supplied later by `Point(3, 4)`.

**New to YIDL?** Follow this sequence before studying the complete example:

1. [How YIDL works](docs/concepts/model.md): what you author, the generator
   library versus generated application code, and YIDL's relationship to Astichi.
2. [Generation stages](docs/concepts/generation-pipeline.md): preparation,
   generation and application execution.
3. [Installation](docs/start/install.md), then
   [generate a two-field slotted class](docs/start/first-generator.md).

Already familiar with Python generation? Use the
[direct run route](docs/start/first-generator.md#run-and-inspect) after installation.

**0.1.0 development candidate; CPython 3.12+.** The recorded example environment
is qualified separately from that minimum. Current metadata omits Astichi, so
install it explicitly. The existing `yidl-compile` command targets the legacy
transducer frontend; use the Python concept API taught here for current braced
`.yidl` files. Packaging and publication readiness remain separate gates.

- [Matching/property/parameter flow](docs/guides/matching-and-data-flow.md)
- [Language reference](docs/reference/language.md)
- [Versions and limitations](docs/reference/compatibility.md)
- [Run and inspect examples](docs/examples/index.md)
- [Build the navigable HTML documentation](docs/contributing/documentation.md)

The canonical developer contracts are `dev-docs/YidlDesignSummary.md` and
`dev-docs/YidlCodingRules.md`. Older lifecycle design and internal validation
material are preserved and excluded from public site output.
