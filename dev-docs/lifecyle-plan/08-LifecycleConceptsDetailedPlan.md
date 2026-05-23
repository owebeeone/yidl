# Lifecycle Concepts Detailed Plan

## Goal

Define how lifecycle generation should be assembled from DDS concepts without
adding lifecycle behavior to DDS core.

This plan covers:

- field helper concepts
- state and facade concepts
- operation contribution records
- runtime method ports
- helper/decorator library generation
- concept extension/merge strategy

## Key Principle

DDS provides generic data and production machinery. Lifecycle behavior lives in
recorded concepts that define:

- data records
- computed views
- matchers
- generated resources
- productions
- ports
- operation contribution records

There should not be a `LifecycleDDS` engine.

## Concept Composition API

Recorded concepts should be composed by extension:

```python
LifecycleCore = build_lifecycle_core_concept()
ManagedFields = build_managed_field_concept()
ConstFields = build_const_field_concept()
Transactions = build_transaction_concept()
LifecycleClass = build_lifecycle_class_concept()

LifecycleP1 = CapsuleConceptBuilder("LifecycleP1")
LifecycleP1.extends(LifecycleCore)
LifecycleP1.extends(ManagedFields)
LifecycleP1.extends(ConstFields)
LifecycleP1.extends(Transactions)
LifecycleP1.extends(LifecycleClass)

LifecycleP1Concept = LifecycleP1.build()
```

Use `extends`, not `mixin`, `requires`, or inheritance terminology. The semantic
meaning is: replay the referenced concept's declarations into this concept,
then add more declarations.

## Field Helper Concepts

Each helper concept contributes facts and resources. It should not emit a whole
class by itself.

### Managed Field Concept

```python
builder = CapsuleConceptBuilder("ManagedFieldConcept")
Core = builder.extends(LifecycleCoreConcept)

FieldSpecs = Core.unions.FieldSpecs
Name = Core.props.Name
Kind = Core.props.Kind
TxKey = Core.props.TxKey
Default = Core.props.Default
DefaultFactory = Core.props.DefaultFactory

ManagedField = FieldSpecs.variant(
    "ManagedField",
    TxKey,
    Default,
    DefaultFactory,
    Core.props.InitialWorking,
    Core.props.Freeze,
    Core.props.Thaw,
)

builder.resources.ManagedGetterTemplate(
    from_astichi_template(
        """
        astichi_comment("property template: managed getter")

        @property
        def field_name__astichi_arg__(self):
            return self.astichi_ref(external=working_path)
        """
    )
)
```

### Const Field Concept

```python
builder = CapsuleConceptBuilder("ConstFieldConcept")
Core = builder.extends(LifecycleCoreConcept)

ConstField = Core.unions.FieldSpecs.variant(
    "ConstField",
    Core.props.Default,
    Core.props.DefaultFactory,
)

PropertyTemplate = Core.matchers.PropertyTemplate
field = PropertyTemplate.input.field(Core.collections.MergedFields)

PropertyTemplate.rule.const_readonly(
    when=(field.prop(Core.props.Kind).eq(CONST_KIND),),
    resource=from_astichi_template(
        """
        astichi_comment("property template: const getter")

        @property
        def field_name__astichi_arg__(self):
            return self.astichi_ref(external=published_path)
        """
    ),
)
```

## State And Facade Concepts

State owns storage. Facades expose behavior.

### Data Records

```python
ClassRole = dds.property("ClassRole", object, REQUIRED, storage_name="class_role")
ClassName = dds.property("ClassName", str, REQUIRED, storage_name="class_name")
StorageRoot = dds.property("StorageRoot", object, REQUIRED, storage_name="storage_root")

GeneratedClass = dds.record(
    "GeneratedClass",
    ClassRole,
    ClassName,
    StorageRoot,
)

GeneratedClasses = dds.collection("GeneratedClasses", GeneratedClass, identity=ClassRole)
```

Roles are semantic objects:

```python
STATE_CLASS = ClassRoleValue("state")
MAIN_FACADE = ClassRoleValue("main_facade")
CURRENT_FACADE = ClassRoleValue("current_facade")
WORKING_FACADE = ClassRoleValue("working_facade")
```

Do not use raw strings as role values in APIs.

### Ports

```python
ModuleBody = dds.port("Module.body", cardinality=dds.many)
ClassBody = dds.port("Class.body", cardinality=dds.many)
ClassSlots = dds.port("Class.__slots__.items", cardinality=dds.many)
InitParams = dds.port("Class.__init__.params", cardinality=dds.many)
InitBody = dds.port("Class.__init__.body", cardinality=dds.many)
PropertyBody = dds.port("Property.body", cardinality=dds.many)
OperationBody = dds.port("Operation.body", cardinality=dds.many)
```

Lifecycle concepts produce records targeted to these ports. The final renderer
is generic: it reads children at ports and inserts resources into Astichi holes.

## Operation Contribution Records

Runtime behavior is represented as data.

```python
OperationKind = dds.property("OperationKind", object, REQUIRED, storage_name="operation_kind")
Phase = dds.property("Phase", object, REQUIRED, storage_name="phase")
Target = dds.property("Target", object, REQUIRED, storage_name="target")
Order = dds.property("Order", int, REQUIRED, storage_name="order")
Template = dds.property("Template", object, REQUIRED, storage_name="template")
Bindings = dds.property("Bindings", object, (), storage_name="bindings")

OperationContribution = dds.record(
    "OperationContribution",
    OperationKind,
    Phase,
    Target,
    Order,
    Template,
    Bindings,
)

OperationContributions = dds.collection(
    "OperationContributions",
    OperationContribution,
    identity=(OperationKind, Phase, Target, Order),
)
```

Example phases:

```python
INIT_PHASE = PhaseValue("init")
GET_PHASE = PhaseValue("get")
SET_PHASE = PhaseValue("set")
VALIDATE_PHASE = PhaseValue("validate")
COMMIT_PHASE = PhaseValue("commit")
ROLLBACK_PHASE = PhaseValue("rollback")
CLOSE_PHASE = PhaseValue("close")
```

Again, these are lifecycle semantic objects, not DDS core enums.

Any semantic object used in a tuple identity, such as `OperationKind` or
`Phase`, must be source-emittable in V1. Use generated resources, imported
constants, or literal source-renderable values; do not place arbitrary Python
objects in generated identity fields.

## Matchers For Operation Templates

```python
GetTemplate = dds.matcher("GetTemplate")
field = GetTemplate.input.field(IndexedFields)
facade = GetTemplate.input.facade(GeneratedClasses)

GetTemplate.rule.managed_main_facade(
    when=(
        field.prop(Kind).eq(MANAGED_KIND),
        facade.prop(ClassRole).eq(MAIN_FACADE),
    ),
    resource=from_astichi_template(
        """
        astichi_comment("property template: managed main facade getter")

        @property
        def field_name__astichi_arg__(self):
            return self.astichi_ref(external=current_path)
        """
    ),
)

GetTemplate.rule.managed_working_facade(
    when=(
        field.prop(Kind).eq(MANAGED_KIND),
        facade.prop(ClassRole).eq(WORKING_FACADE),
    ),
    resource=from_astichi_template(
        """
        astichi_comment("property template: managed working facade getter")

        @property
        def field_name__astichi_arg__(self):
            return self.astichi_ref(external=working_path)
        """
    ),
)
```

## Production To Operation Contributions

```python
dds.production(
    "GetTemplateToOperationContribution",
    source=GetTemplate.results(),
    target=OperationContributions,
    identity=tuple_value(
        literal(GET_OPERATION),
        literal(GET_PHASE),
        match.record("field").prop(Name),
        match.record("field").prop(SourceOrder),
    ),
    values={
        OperationKind: literal(GET_OPERATION),
        Phase: literal(GET_PHASE),
        Target: match.record("field").prop(Name),
        Order: match.record("field").prop(SourceOrder),
        Template: match.resource(),
        Bindings: call("get-bindings", make_get_bindings),
    },
    policy=ReplaceExisting,
)
```

If `tuple_value(...)` does not exist, identity can derive from target collection
tuple identity and values.

## Helper And Decorator Library Concept

Do not start here. Build this after the generated lifecycle staircase works.

When implemented, the library concept uses module-level ports:

```python
ModuleImports = dds.port("Module.imports", cardinality=dds.many)
ModuleBody = dds.port("Module.body", cardinality=dds.many)
HelperFunctions = dds.port("Module.helpers", cardinality=dds.many)
Decorators = dds.port("Module.decorators", cardinality=dds.many)
```

Helper functions should be generated with Astichi parameter holes:

```python
from_astichi_template(
    """
    def managed(
        name,
        default=REQUIRED,
        tx_key=DEFAULT_TRANSACTION,
        *field_params__astichi_param_hole__,
    ):
        astichi_hole(body)
    """
)
```

If the parameter-hole surface cannot express a helper signature cleanly, fix
Astichi rather than hand-writing helper strings.

## Expected Use Case

For a class with managed field `count` and const field `label`, lifecycle
concepts produce:

```text
GeneratedClasses:
  State: ExampleState
  MainFacade: Example

StateSlot contributions:
  _count_current
  _count_working
  _label_value

InitParam contributions:
  count
  label

Operation contributions:
  count getter
  count setter
  count commit
  count rollback
  label getter
```

The renderer then assembles these into one generated module.

## Expected Generated Source Golden

Expected excerpt for
`tests/data/goldens/materialized/dds_lifecycle_concepts.py`:

```python
class ExampleState:
    __slots__ = (
        "_count_current",
        "_count_working",
        "_label_value",
    )

    def __init__(self, *, count, label):
        self._count_current = count
        self._count_working = _NO_WORKING_VALUE
        self._label_value = label


class Example:
    __slots__ = ("_state",)

    def __init__(self, *, count, label):
        self._state = ExampleState(count=count, label=label)

    @property
    def count(self):
        state = self._state
        if state._count_working is not _NO_WORKING_VALUE:
            return state._count_working
        return state._count_current

    @count.setter
    def count(self, value):
        self._state._count_working = value

    @property
    def label(self):
        return self._state._label_value
```

The golden must prove:

- state owns storage
- facade owns behavior
- generated operations are assembled from contribution records
- parameter names are stable API names
- no lifecycle-specific DDS runtime appears in the final class

## Diagnostics

Concept replay diagnostics:

- incompatible concept extension
- duplicate port declaration with incompatible cardinality
- matcher rule collision
- production group insertion conflict
- missing required resource

Lifecycle model diagnostics:

- no state class selected
- facade references missing state class
- operation contribution has no target method/port
- template binding missing a required value

## Implementation Notes

The lifecycle concepts should be written after the generic features are usable.
Do not add lifecycle concepts that bypass:

- matcher resource selection
- production records
- port-targeted contributions
- generated resource values

If a concept has to manually loop over fields and append strings, stop and
either improve DDS/Astichi or add a properly modeled production/resource.

## Test Plan

Bespoke:

- `test_concept_extension_reuses_existing_property`
- `test_concept_extension_rejects_incompatible_port`
- `test_operation_contribution_identity_is_stable`
- `test_operation_contribution_missing_template_rejects`

Goldens:

- `tests/data/gold_src/dds_lifecycle_concepts.py`
- `tests/data/goldens/materialized/dds_lifecycle_concepts.py`

The golden should build state/facade classes from contribution records, not from
a handwritten class generator.
