# Bind names and assignment targets

The tutorial uses three distinct bindings for one direct store:

```python
astichi_pass(self, outer_bind=True).astichi_ref(external=slot)._ = astichi_pass(value__astichi_arg__, outer_bind=True)
```

`self` and the bound parameter are reads of the containing constructor scope.
`slot` is an external **path string** such as `x`, not a Python object value.
The trailing `._` makes the reference a transparent Store target. The output is
`self.x = x`; the marker calls do not run when the user constructs the object.

An ordinary authored name target plus identifier binding is enough for simple
local assignments. A naked value expression is not automatically a Store target.
Python rejects Load-context AST used on the left of assignment. Transparent
`._` / `.astichi_v` wrappers exist for supported assignment, augmented-assignment
and deletion surfaces; each carrier/context/backend needs qualification.

## Scope markers

| Marker | Role |
| --- | --- |
| `astichi_keep(name)` / suffix keep | Preserve identifier spelling through hygiene |
| `astichi_import(name)` | Declaration importing a parent-scope binding |
| `astichi_export(name)` | Publish a local binding for wiring |
| `astichi_pass(name, outer_bind=True)` | Value reference across a scope boundary |
| `name__astichi_arg__` | Identifier demand resolved during binding |
| `astichi_ref(external=path)` | Expression-only Name/Attribute path |

A keep does not install a capture object. A parameter demand does not rename an
attribute just because it has a similar spelling. An outer read does not acquire
target context without the correct carrier. Use dotted identifier paths for
nested attributes, not arbitrary source expressions in a path string.

When a binding survives as a marker, inspect its exact AST position and remaining
demands. If an external is “already queued,” check whether two live insertions
share a build identity. The tutorial's composite numeric field indices avoid
collisions across owners; collection `FieldId` alone did not set those indices.
