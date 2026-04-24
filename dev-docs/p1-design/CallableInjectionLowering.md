# Callable Injection Lowering

Current P1 callable-wrapper and injection design.

## 1. Purpose

1. Validate callable signatures at generation time.
2. Collect the values each callable needs.
3. Emit direct calls where possible.
4. Keep generic runner tables only when dynamic behavior is unavoidable.

## 2. Callable Kinds

| Callable kind | Allowed generated names |
|---|---|
| `default_factory` | `self`, `current`, `working`, initvar names |
| transient `working_default_factory` | `self`, `current`, `working`, initvar names |
| `on_before_commit` | `self`, `current`, `working`, `tx_group`, initvar names |
| `on_after_commit` | `self`, `previous`, `current`, `tx_group`, initvar names |
| `on_after_rollback` | `self`, `current`, `tx_group`, initvar names |
| `commit_validator` | `self`, initvar names |
| `commit_order_key` default factory | `self`, `current`, `working`, initvar names |

## 3. Signature Rules

1. Callable parameters must be named.
2. Positional-only parameters are rejected.
3. `*args` and `**kwargs` are rejected.
4. Unknown parameter names are rejected.
5. Type annotations are advisory for P1 wiring.

## 4. Initvar Rules

1. Every declared initvar must be consumed by at least one factory, hook, or
   validator by parameter name.
2. Constructor-phase initvars are always available during construction.
3. Retained initvar storage is materialized only when a post-init callable
   names that initvar.
4. Unused initvars fail decoration/generation.

## 5. FieldSpec Callable Properties

| Property | P1 handling |
|---|---|
| `default_factory` | Wrapper/lowerer with injection |
| `working_default_factory` | Transient-only wrapper/lowerer |
| `freeze` | Value conversion before publish |
| `thaw` | Value conversion before first working mutation |
| `state_factory` | Sidecar construction; direct unless it becomes injectable |
| `state_copy` | Sidecar copy; direct unless it becomes injectable |
| Hooks | Per-group generated call lists where possible |
| Validators | Per-group generated gate |

## 6. Cycle Detection

1. The state/store object owns a factory-resolution stack.
2. The stack keys by callable kind and field name.
3. Re-entry into a running `(kind, field)` raises a cycle error.
4. P1 covers `default_factory` and transient `working_default_factory`.
5. If `state_factory` or `state_copy` become lazy/injectable, they must opt
   into the same cycle policy deliberately.

## 7. Output Strategy

1. Prefer direct generated calls when all parameters are statically known.
2. Use small wrappers only when they materially simplify emitted code.
3. Avoid generic runner maps in generated hot paths.
4. Preserve enough metadata for diagnostics and parity tests.
