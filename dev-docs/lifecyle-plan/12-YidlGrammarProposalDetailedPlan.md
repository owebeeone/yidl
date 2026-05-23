# YIDL Grammar Proposal

## Goal

Define a textual `.yidl` grammar that can describe the full DDS/concept
capability and import YIDL files into other YIDL files.

The grammar should compile to recorded concept plans. It should not execute
Python during definition. Generated decorator/runtime code may later use emitted
Python helpers, generated resources, and Astichi composables.

## Design Principles

- A `.yidl` file declares symbols and concepts.
- Imported `.yidl` files compile to symbol tables and concept plans.
- Names refer to semantic objects, not string tags.
- Concepts compose with `extends`.
- Public DDS primitives stay small.
- Higher-level lifecycle conveniences lower to aggregate operations.
- Source snippets are Astichi resources, not ad hoc strings.
- The grammar is declarative; no arbitrary Python statements.

## File Shape

Example:

```text
module yidl.lifecycle.managed

import "./core.yidl" as core
from "./diagnostics.yidl" import concept Diagnostics

concept ManagedFields extends core.LifecycleCore, Diagnostics {
    property TxKey: object = DEFAULT_TRANSACTION storage tx_key
    property Default: object = REQUIRED storage default
    property DefaultFactory: object = None storage default_factory

    family FieldSpecs {
        common core.Name, core.Annotation, core.SourceOrder, core.SourceLabel
        variant ManagedField {
            core.Kind
            TxKey
            Default
            DefaultFactory
        }
    }

    collection MergedFields: FieldSpecs identity core.Name

    resource ManagedGetter = astichi_template """
        @property
        def field_name__astichi_arg__(self):
            state = self._state
            if state.astichi_ref(external=working_slot) is not _NO_WORKING_VALUE:
                return state.astichi_ref(external=working_slot)
            return state.astichi_ref(external=current_slot)
    """

    matcher PropertyTemplate(field: MergedFields) {
        default core.PlainGetter
        rule managed when field.core.Kind == core.MANAGED_KIND -> ManagedGetter
    }
}
```

## Import Semantics

### Module Declaration

```text
module yidl.lifecycle.core
```

The module name is a semantic name for diagnostics and generated source names.
It is not a Python import path unless explicitly mapped by the build system.

### File Import

```text
import "./core.yidl" as core
```

Rules:

- path is relative to the importing file
- imported file is parsed and compiled to a concept module
- symbols are accessed through the alias
- import cycles reject unless a later design adds explicit forward declarations

### Selective Import

```text
from "./diagnostics.yidl" import concept Diagnostics, property SourceLabel
```

Rules:

- imported symbols keep their original identity
- aliases are allowed:

```text
from "./core.yidl" import concept LifecycleCore as Core
```

### Re-Export

```text
export concept ManagedFields
export property TxKey
```

Only exported symbols are visible to importing files unless the build is in
private/test mode.

## Lexical Conventions

Identifiers:

```text
Identifier = /[A-Za-z_][A-Za-z0-9_]*/
QualifiedName = Identifier ("." Identifier)*
```

String literals use Python-compatible single, double, or triple quotes.
The Lark grammar should implement this as one `PythonString` token covering
single-line and triple-quoted strings; resource snippets use the same token.

Parser token aliases used below:

```text
identifier := Identifier
qualified_name := QualifiedName
string := PythonString
integer := /[0-9]+/
number := /[0-9]+(\.[0-9]+)?/

literal_expr
  := string
   | integer
   | number
   | "True"
   | "False"
   | "None"

literal_list
  := literal_expr ("," literal_expr)*

type_ref
  := qualified_name

resource_ref
  := qualified_name
```

Comments:

```text
# line comment
```

No significant indentation is required in the grammar; braces define blocks.

## Grammar Sketch

This is intentionally close to EBNF, not a parser implementation.

```text
file
  := module_decl? import_decl* top_level_decl*

module_decl
  := "module" qualified_name

import_decl
  := "import" string "as" identifier
   | "from" string "import" import_item ("," import_item)*

import_item
  := symbol_kind identifier ("as" identifier)?

symbol_kind
  := "concept" | "property" | "record" | "union" | "collection"
   | "port" | "resource" | "matcher" | "operation"

top_level_decl
  := export_decl
   | concept_decl
   | property_decl
   | resource_decl

export_decl
  := "export" symbol_kind identifier

concept_decl
  := "concept" identifier extends_clause? "{" concept_member* "}"

extends_clause
  := "extends" qualified_name ("," qualified_name)*

concept_member
  := use_decl
   | property_decl
   | record_decl
   | union_decl
   | family_decl
   | collection_decl
   | computed_collection_decl
   | port_decl
   | resource_decl
   | matcher_decl
   | production_decl
   | operation_decl
   | diagnostics_decl

use_decl
  := "use" qualified_name ("as" identifier)?
```

## Property Grammar

```text
property_decl
  := "property" identifier ":" type_expr default_clause? storage_clause?

default_clause
  := "=" value_expr

storage_clause
  := "storage" identifier

type_expr
  := qualified_name
   | "object" | "str" | "int" | "bool" | "float"
   | "literal" "[" literal_list "]"
```

Example:

```text
property Name: str storage name
property Init: bool = True storage init
property Default: object = REQUIRED storage default
```

Lowering:

```python
Name = dds.property("Name", str, REQUIRED, storage_name="name")
Init = dds.property("Init", bool, True, storage_name="init")
```

## Record, Union, And Family Grammar

### Record

```text
record_decl
  := "record" identifier "{" property_ref* "}"

property_ref
  := qualified_name
```

Records inherit storage names from the referenced properties. Record
declarations do not redeclare storage names.

Example:

```text
record TxKey {
    TxKeyName
    TxIndex
}
```

### Union

```text
union_decl
  := "union" identifier "{" variant_decl* "}"

variant_decl
  := "variant" identifier "{" property_ref* "}"
```

Example:

```text
union FieldSpecs {
    variant ManagedField {
        Name
        Annotation
        TxKey
    }
}
```

### Family

`family` is fluent-layer sugar over `union`.

```text
family_decl
  := "family" qualified_name "{" family_member* "}"

family_member
  := "common" property_ref ("," property_ref)*
   | variant_decl
```

Example:

```text
family FieldSpecs {
    common Name, Annotation, SourceOrder, SourceLabel
    variant ManagedField {
        Kind
        TxKey
        Default
    }
    variant InitVarField {
        Default
        DefaultFactory
    }
}
```

Lowering:

```python
FieldSpecs = dds.union("FieldSpecs")
ManagedField = FieldSpecs.variant(
    "ManagedField",
    Name,
    Annotation,
    SourceOrder,
    SourceLabel,
    Kind,
    TxKey,
    Default,
)
```

## Collection Grammar

```text
collection_decl
  := "collection" identifier ":" type_ref identity_clause? cardinality_clause?

identity_clause
  := "identity" identity_expr

identity_expr
  := property_ref
   | "(" property_ref ("," property_ref)+ ")"

cardinality_clause
  := "single" | "many"
```

Example:

```text
collection MergedFields: FieldSpecs identity Name
collection SpecialDeclarations: SpecialDeclaration identity (SpecialKind, TxKey)
```

## Computed Collection Grammar

```text
computed_collection_decl
  := "computed" "collection" identifier ":" type_ref
     "from" qualified_name
     "where" condition_expr
```

Example:

```text
computed collection TransactionalFields: FieldSpecs
from MergedFields
where HasTransaction == True
```

V1 conditions are Eq-only:

```text
condition_expr
  := operand "==" operand
   | condition_expr "and" condition_expr

operand
  := value_expr
```

No inequality, greater-than, less-than, or arbitrary predicates in V1.

## Port Grammar

```text
port_decl
  := "port" identifier string cardinality_clause
```

Example:

```text
port ClassBody "Class.body" many
port ClassName "Class.name" single
```

Lowering:

```python
ClassBody = dds.port("Class.body", cardinality=dds.many)
```

## Resource Grammar

```text
resource_decl
  := "resource" identifier "=" resource_expr

resource_expr
  := "literal" value_expr
   | "import" string "." identifier
   | "astichi_code" string
   | "astichi_template" string
```

Examples:

```text
resource RequiredParam = astichi_template """
    def astichi_params(*, field_name__astichi_arg__: astichi_ref(external=annotation_path)):
        pass
"""

resource ObjectSetattr = import "builtins".object
resource DefaultTx = literal DEFAULT_TRANSACTION
```

Resource strings are compile inputs. They are not parsed or compiled at YIDL
definition time unless the compiler is running validation. Generated decorator
paths use emitted resources.

## Matcher Grammar

```text
matcher_decl
  := "matcher" identifier "(" matcher_input_list? ")" "{"
       matcher_default?
       matcher_rule*
     "}"

matcher_input_list
  := matcher_input ("," matcher_input)*

matcher_input
  := identifier ":" qualified_name

matcher_default
  := "default" resource_ref

matcher_rule
  := "rule" identifier "when" condition_expr "->" resource_ref weight_clause?

weight_clause
  := "weight" number
```

Example:

```text
matcher PropertyTemplate(field: MergedFields) {
    default PlainProperty
    rule managed when field.Kind == MANAGED_KIND -> ManagedProperty
    rule const when field.Kind == CONST_KIND -> ConstProperty
}
```

Rules lower to current `MatcherSpec` with Eq-only conditions and descending
specificity.

## Production Grammar

Record-to-record productions stay declarative:

```text
production_decl
  := "production" identifier "from" source_expr "to" qualified_name "{"
       production_member*
     "}"

source_expr
  := qualified_name order_clause?
   | qualified_name "." "results" "(" ")" order_clause?

order_clause
  := "ordered" "(" property_ref ("," property_ref)* ")"

production_member
  := "identity" value_expr
   | "policy" qualified_name
   | "set" property_ref "=" value_expr
```

Example:

```text
production PropertyTemplateToClassBody
from PropertyTemplate.results()
to ClassComponents {
    identity match.record("field").Name
    policy ReplaceExisting
    set Name = match.record("field").Name
    set Target = ClassBody.of("Example")
    set Order = match.record("field").SourceOrder
    set Template = match.resource()
}
```

## Aggregate Operation Grammar

Aggregate operations cover layered merge, distinct index, fact production,
graph closure, and validation.

```text
operation_decl
  := "operation" identifier operation_io "using" resource_ref operation_options?

operation_io
  := "inputs" "(" qualified_name_list? ")"
     "outputs" "(" qualified_name_list? ")"

qualified_name_list
  := qualified_name ("," qualified_name)*

operation_options
  := "{" operation_option* "}"

operation_option
  := "ordered" "(" property_ref ("," property_ref)* ")"
   | "diagnostics" qualified_name
```

Example:

```text
operation BuildTxKeys
inputs (TransactionalFields)
outputs (TxKeys)
using BuildTxKeysOperation {
    ordered(SourceOrder)
}
```

Generated operation resource contract:

```python
def run(ctx):
    ...
```

`using` lowers to the Python `dds.operation(..., resource=...)` argument. The
YIDL compiler validates that declared input and output collections exist. The
operation body remains a generated resource.

V1 operations must declare at least one input or one output. A zero-input
operation is allowed for constant/module setup. A zero-output operation is
allowed only for validation/final-gate operations. A zero-input and zero-output
operation is invalid.

## Diagnostic Grammar

Diagnostics are fluent sugar, not DDS core:

```text
diagnostics_decl
  := "diagnostics" identifier "{"
       "collection" identifier
       "gate" identifier
     "}"
```

Example:

```text
diagnostics LifecycleDiagnostics {
    collection Diagnostics
    gate RaiseDiagnostics
}
```

This lowers to ordinary records, collections, and an aggregate operation.

## Value Expression Grammar

```text
value_expr
  := literal_expr
   | qualified_name
   | source_ref
   | match_ref
   | lookup_expr
   | port_address_expr
   | tuple_expr

source_ref
  := "source" "." property_ref

match_ref
  := "match" "." "resource" "(" ")"
   | "match" "." "record" "(" string ")" "." property_ref
   | "match" "." "value" "(" integer ")"

lookup_expr
  := "lookup" "(" qualified_name "," "key" "=" value_expr "," "value" "=" property_ref default_arg? ")"

default_arg
  := "," "default" "=" value_expr

port_address_expr
  := qualified_name "." "of" "(" value_expr ")"

tuple_expr
  := "(" value_expr ("," value_expr)+ ")"
```

## Full Example: Core + Managed Import

`core.yidl`:

```text
module yidl.lifecycle.core

export concept LifecycleCore

concept LifecycleCore {
    property Name: str storage name
    property Annotation: object storage annotation
    property SourceOrder: int storage source_order
    property Kind: object storage kind
    property DeclarationSpace: object storage declaration_space

    port ClassBody "Class.body" many
    port InitParams "Class.__init__.params" many

    family FieldSpecs {
        common Name, Annotation, SourceOrder, Kind, DeclarationSpace
    }
}
```

`managed.yidl`:

```text
module yidl.lifecycle.managed

import "./core.yidl" as core

export concept ManagedFields

concept ManagedFields extends core.LifecycleCore {
    property TxKey: object = DEFAULT_TRANSACTION storage tx_key
    property Default: object = REQUIRED storage default

    family core.FieldSpecs {
        variant ManagedField {
            TxKey
            Default
        }
    }

    collection MergedFields: core.FieldSpecs identity core.Name

    resource ManagedGetter = astichi_template """
        @property
        def field_name__astichi_arg__(self):
            return self._state.astichi_ref(external=current_slot)
    """

    matcher PropertyTemplate(field: MergedFields) {
        rule managed when field.core.Kind == MANAGED_KIND -> ManagedGetter
    }
}
```

## Ambiguities Resolved

### Can A File Extend A Family Imported From Another File?

Yes. This is how lifecycle helper concepts add variants to the common
`FieldSpecs` family.

```text
family core.FieldSpecs {
    variant ManagedField { ... }
}
```

The compiler records this as an extension contribution to the imported family
symbol. Replay rejects incompatible duplicate variants.

Property names inside an extended family resolve in the extending concept
first, then in the owning concept of the family being extended. If neither
scope defines the property, replay rejects the variant contribution.

### Are Imported Symbols Mutable?

No. Imports are immutable semantic symbols. A concept can extend a family or
matcher only through explicit extension syntax. It cannot redefine an imported
property.

### How Do Multi-Input Matchers Evaluate?

A matcher result source evaluates the cross product of its declared input
collections unless the production source explicitly supplies paired records.
This is deliberate: facade/field matchers need to evaluate each field against
each facade role. If a use case needs paired semantics, model the pair as an
ordinary source record and use a single matcher input over that paired
collection.

### Can A Concept Import Private Symbols?

No in normal mode. Tests may allow private imports with a compiler flag, but
committed `.yidl` files should import exported symbols only.

### Is This A Runtime Language?

No. `.yidl` compiles to concept plans and generated resources. It is a
definition language.

## Parser Output

The first implementation should use Lark for parsing `.yidl` files. Lark is a
definition-stage dependency only; generated decorator/runtime code must not
invoke it.

The parser should produce:

```python
YidlModule(
    module_name="yidl.lifecycle.managed",
    imports=(...),
    concepts=(...),
    exports=(...),
)
```

Compilation resolves imports and produces:

```python
CapsuleConceptPlan
```

or a module containing multiple named concept plans.

## Test Plan

Bespoke parser tests:

- parse module/import/export
- parse concept extends
- parse property/record/family/collection/port/resource/matcher/production/operation
- reject import cycles
- reject private imported symbol
- reject incompatible imported symbol extension

Goldens:

- `tests/data/gold_src/yidl_imported_concepts.py`
- generated source produced from `core.yidl` + `managed.yidl`
- final output proves imported concept symbols are reused, not duplicated
