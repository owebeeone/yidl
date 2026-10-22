# YIDL

YIDL is a declarative Python generator compiler. Define a fact schema, reusable
Astichi resources, matching rules and ordered assembly; populate facts and build
plain Python classes. Lifecycle, Dataclass and Undoable are separate consumers.

**0.1.0 development candidate.** Release planning is accepted; packaging and
publication readiness are separate. Current metadata omits Astichi, so install
it explicitly. The existing `yidl-compile` command targets the legacy transducer
frontend; use the Python concept API for current braced `.yidl` files.

- [Installation and qualified environment](docs/start/install.md)
- [Generate a two-field slotted class](docs/start/first-generator.md)
- [Matching/property/parameter flow](docs/guides/matching-and-data-flow.md)
- [Language reference](docs/reference/language.md)
- [Versions and limitations](docs/reference/compatibility.md)
- [Run and inspect examples](docs/examples/index.md)
- [Build the navigable HTML documentation](docs/contributing/documentation.md)

The canonical developer contracts are `dev-docs/YidlDesignSummary.md` and
`dev-docs/YidlCodingRules.md`. Public documentation explains the current generic
route; older lifecycle design and internal validation material are preserved and
excluded from public site output. No site deployment is enabled by this change.
