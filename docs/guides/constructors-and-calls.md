# Constructor parameters and specialized calls

Parameters are signature payloads. Statements are body payloads. Calls need an
argument payload. Give each surface its own resource instead of trying to insert
one snippet shape into all three.

```python
# Required identifier-bound parameter carrier
def astichi_params(name__astichi_arg__):
    pass
```

The executable tutorial contains the exact carrier. For keyword-only parameters use
`def astichi_params(*, name__astichi_arg__): pass`. A default can refer to an
identifier-bound capture instead of serializing a live Python object. The
consumer partitions required/defaulted and positional/keyword-only parameters;
YIDL does not infer Python signature legality from arbitrary field policies.

## Annotations and defaults

Distinguish literal strings (including explicit string annotations), live type
objects, and capture identifiers. A reference marker in an annotation is not
assumed to lower like a body expression. The qualified consumer route captures a
name and uses an identifier demand in the annotation/default position. Do not
advertise the ongoing Lifecycle live-type annotation fix as accepted support.

An opaque default or callback belongs in a fresh execution namespace or authored
factory closure. Bind its private identifier into the parameter resource. Keep
real objects out of literal external bindings. [Ownership](../concepts/binding-and-ownership.md)
explains the separate lifetimes.

## Calls and dependencies

The canonical Lifecycle callable/closure fixtures generate `MethodCallArgument`
records, select them by owner, and insert `astichi_funcargs(...)` payloads into
call holes. Provider analysis, available injection names, positional-only policy,
unknown/variadic handling and dependency-cycle diagnostics belong to that
consumer's analysis operation. DDS stores those facts; it does not discover
callable dependencies by itself.

Constructor parameter order and initialization dependency order may differ. A
consumer should normalize each order independently and reject unavailable
providers/cycles before building code. This site does not claim a universal
factory dependency resolver or a generic reachability query. See
[fact production](fact-production.md) and [real consumers](../examples/consumers.md).
