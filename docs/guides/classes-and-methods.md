# Assemble classes and methods

Start with the desired Python shape: class shell, slots declaration, methods,
then method parameters and statements. Expose a named surface for each part
that varies. Keep field policy in input facts and matcher rules.

The [first generator](../start/first-generator.md) uses a `ClassShell` resource
and a nested `InitProduction`. Its class root binds the class-name identifier
and the already-normalized slot tuple. Field rows supply direct stores through
transparent attribute targets. There is no descriptor dispatch in those stores.

To add a property getter/setter, use an authored method/property resource,
select it by field policy, bind its public field name and storage path, and insert
it into the class body. Keep the public spelling deliberately; let unrelated
locals be hygienically renamed. [Consumer examples](../examples/consumers.md)
show specialized accessors selected from actual consumer facts.

## Conditional omission

The tutorial's `EnableInit` selects `InitContribution`; the fallback selects an
empty-source resource. Empty source suppresses that contribution. The always
present `ClassPass` fills the mandatory class method hole so disabled-init output
still materializes. `--empty` instead keeps an actual zero-parameter constructor.
These outcomes differ: omitted init inherits Python's default construction;
empty init is a generated function.

## Compound Python constructs

YIDL embeds Astichi Python resources rather than defining separate syntax for
`if`, `try`, `with`, decorators or comprehensions. An insertion must remain within
a legal Python construct boundary. Put statement holes inside braced YIDL
resources containing normal indented Python; use explicit `pass` contributions
when a selected suite is empty. Interacting exception/loop/decorator constructs
need their own SDK/version qualification. The first class does not establish all
Python syntax as supported. See the [bridge](../reference/astichi-bridge.md) for
known positions and limitations, and [compatibility](../reference/compatibility.md)
for unqualified compound cases.

## Execute interacting compound constructs

`example/documentation/control_flow.py` qualifies a statement-hole insertion
inside `if` nested in `for`/`else`, `with`, `try`/`except`/`finally`, with a
decorated function and comprehension in the same resource. Zero/one/two ordered
actions, empty input and a raised exception have explicit behavior assertions.
This is a CPython 3.12.12 / Astichi 1.1.3 Python-backend recipe; other Python
construct positions and version-specific syntax require separate checks.

{{source:example/documentation/control_flow.py|python}}

{{source:tests/data/goldens/materialized/documentation_classes/control_flow_model.py|python}}
