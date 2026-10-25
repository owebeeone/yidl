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

1. [How YIDL works](https://owebeeone.github.io/yidl/concepts/model/): what you author, the generator
   library versus generated application code, and YIDL's relationship to Astichi.
2. [Generation stages](https://owebeeone.github.io/yidl/concepts/generation-pipeline/): preparation,
   generation and application execution.
3. [Installation](https://owebeeone.github.io/yidl/start/install/), then
   [generate a two-field slotted class](https://owebeeone.github.io/yidl/start/first-generator/).

Already familiar with Python generation? Use the
[direct run route](https://owebeeone.github.io/yidl/start/first-generator/#run-and-inspect) after installation.

**Alpha release; CPython 3.12+.** The recorded example environment
is qualified separately from that minimum. Astichi 1.1.3 is declared as a
runtime dependency and is installed automatically. The existing `yidl-compile`
command targets the legacy
transducer frontend; use the Python concept API taught here for current braced
`.yidl` files. Packaging and publication readiness remain separate gates.

- [Matching/property/parameter flow](https://owebeeone.github.io/yidl/guides/matching-and-data-flow/)
- [Language reference](https://owebeeone.github.io/yidl/reference/language/)
- [Versions and limitations](https://owebeeone.github.io/yidl/reference/compatibility/)
- [Run and inspect examples](https://owebeeone.github.io/yidl/examples/)
- [Build the navigable HTML documentation](https://owebeeone.github.io/yidl/contributing/documentation/)

The canonical developer contracts are `dev-docs/YidlDesignSummary.md` and
`dev-docs/YidlCodingRules.md`. Older lifecycle design and internal validation
material are preserved and excluded from public site output.
