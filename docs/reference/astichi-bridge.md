# YIDL's Astichi boundary

YIDL owns facts, rule selection, ordering and consumer policy. Astichi owns Python
fragment composition, scopes, hygiene, free-load resolution and AST lowering.
The current source/compiler is the authority for marker mechanics; see the
[Astichi repository](https://github.com/owebeeone/astichi) for its own documentation.

| Marker/surface | Position and purpose | This documentation's evidence |
| --- | --- | --- |
| `astichi_hole(name)` | Named insertion point | Tutorial module/class/method bodies |
| `params__astichi_param_hole__` | Function parameter surface | Zero/one/two tutorial parameters |
| `astichi_params(...)` | Parameter payload carrier | Tutorial and dataclass fixtures |
| `astichi_funcargs(...)` | Call-argument payload | Canonical Lifecycle call argument fixtures |
| `name__astichi_arg__` | Identifier demand | Tutorial class/parameter names |
| `astichi_ref(external=path)` | Expression path, Name/Attribute chain | Tutorial direct slot access |
| `._` / `.astichi_v` | Transparent target wrapper | Tutorial Store; other target contexts separately qualified |
| `astichi_pass(..., outer_bind=True)` | Cross-scope value reference | Constructor store reads |
| `astichi_import/export` | Scope boundary declarations | SDK-owned; not runtime Python imports/captures |
| `astichi_keep` / suffix keep | Deliberate spelling preservation | Distinct from providing a value |
| `astichi_pyimport` | Generated Python import | Generated DDS runtime assembly |
| `astichi_for` | Compile-time unrolling | SDK construct, no broad tutorial qualification |

A path is a validated dotted identifier chain, not arbitrary executable source.
Bare statement-form reference/pass markers are not value expressions in a valid
receiving surface. Ordinary attributes do not become demands by name suffix.

## Scope of construct claims

Normal Python `if`/`elif`/`else`, exceptions, loops/else, `with`, decorators and
comprehensions can appear as authored resource constructs only insofar as the
selected SDK supports their surfaces. An unchanged construct that compiles is not
evidence that arbitrary insertions inside it compose correctly. Insertion must
preserve legal target and lexical contexts and fill mandatory empty suites.
The executable `control_flow.py` recipe checks insertion into interacting if,
for/else, with and try/except/finally constructs, with decorator/comprehension
context. Its precise Python tuple is qualified; other combinations/minors remain
listed in compatibility.

The consumer's original nested scalar chain and reference-annotation arrangement
remain bounded investigations. Astichi source improvements, API changes or native
repairs are separate projects, not prerequisites silently added to this tutorial.
