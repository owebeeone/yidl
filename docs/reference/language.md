# Current language reference

The current `.yidl` route is brace-blocked Lark concept syntax. The old
indentation/transducer parser and `%%` fences belong to a different frontend.
`yidl-compile` invokes that older frontend; use the [Python API](apis-and-cli.md)
for this language.

## Authoring rules

| Surface | Syntax/meaning |
| --- | --- |
| Module | `module example.generator` labels the source module |
| Imports | `import "base.yidl" as base`; `from "base.yidl" import concept Base` |
| Export | `export concept Classes` makes a concept available to importers |
| Concept | `concept Child extends base.Base { ... }` |
| Property | `property FieldName: str storage field_name`; optional `= value` default |
| Record | `record Field { FieldName FieldOrder }` — no commas between entries |
| Family | `family Fields { common Name, Order variant Plain {} }` |
| Collection | `collection Fields: Field identity FieldId many`; tuple identities supported |
| Computed view | `computed collection Selected: Field from Fields where Enabled == True` |
| Resource | `resource Store = template $[ ... ]$`; `code`, literal/import forms also exist |
| Matcher | Named input aliases; defaults and named `when` rules; resource/contribution/operation result kinds |
| Contribution | Resource/production, `as`, numeric `index`, `order`, target and bindings |
| Data production | `production P from Source to Target { set Name = source.Name }` |
| Composable production | `production P -> composable { root Root = Resource ... }` |
| Assembly | `assembly Module = P` exports a named callable build |
| Operation | Declared collection inputs/outputs and resource or matcher implementation |

Conditions are equality terms joined with `and`; this is not unrestricted Python
expression syntax. Resource bodies are Python/Astichi, but contribution binding
expressions have a smaller grammar (literal, visible semantic name or tuple).
An accepted parse is not proof that every syntactic combination has runtime
semantics for your chosen surface/backend.

## Delimiters and small failures

Resources accept quoted strings, inline backticks, fenced blocks and `$[ ... ]$`
or `$( ... )$` forms defined below. Use the tutorial's `$[` form for multiline
Python. YIDL record bodies use separate property entries: `record R { Name Order }`.
`record R { Name, Order }` raises a comma parser diagnostic. A comma in `common`
or an explicit tuple is a different grammar position.

A missing imported key fails resolution; a missing export fails symbol lookup;
duplicate inherited productions/defaults fail composition. An assembly name is
not inferred from a production's name.

## Exact grammar of this candidate

This block is extracted from the compiler grammar at site build time. It provides
all productions, including phase/operation/diagnostic syntax. Tested grammar
acceptance/rejection is covered by `tests/generation/test_yidl_lark_parser.py`,
`test_yidl_lark_update_a_diagnostics.py` and `test_yidl_operation_matchers.py`.

{{source:src/yidl/concept_grammar.lark|text}}
