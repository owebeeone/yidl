# Resources and insertion surfaces

A snippet's Python shape must fit the receiving surface. A statement, scalar
expression, parameter payload and call-argument payload are different carriers.

| Receiving surface | Authored carrier | Qualification/empty case |
| --- | --- | --- |
| Statement body `astichi_hole(body)` | Statements such as direct stores | Tutorial zero/one/many stores; explicit `pass` fills an empty suite |
| Parameter suffix `params__astichi_param_hole__` | `def astichi_params(...): pass` | Tutorial zero/one/two required parameters |
| Keyword-only parameters | `def astichi_params(*, name): pass` | Existing dataclass canonical fixtures; consumer orders the partition |
| Call argument hole | `astichi_funcargs(...)` payload | Lifecycle canonical argument assembly; not a generic scalar-expression carrier |
| Tuple elements | Compatible scalar expression resources | Existing dataclass fixtures; bare reference statement is not qualified |
| Scalar expression | Expression-compatible resource | Qualify exact carrier/backend; nested expression chain remains unresolved |

The first two rows are freshly exercised by the tutorial against installed
Astichi 1.1.3. Other rows have different evidence boundaries in
[compatibility](../reference/compatibility.md); do not generalize from them.

## Four empty cases

**No match** supplies no contribution. **Empty source** is explicitly suppressed
by assembly. **Empty parameter payload** deliberately supplies a zero-parameter
shape. **`pass`** supplies a real statement. A Python suite containing an existing
`pass` can still have a mandatory Astichi hole awaiting fulfillment.

The tutorial always wires `EmptyParameters`, `EmptyStatements` and `ClassPass`.
They close mandatory holes for zero fields and disabled initialization. Its
`NoInit` resource suppresses method generation; it does not itself fill the
class's `methods` hole. This distinction is observable in the zero/disabled
canonical outputs.

`code` and `template` become generated-value wrappers. Template options can carry
edge expressions for identifier mapping, external binding and preserved names;
see [generated values](../reference/generated-values.md).
