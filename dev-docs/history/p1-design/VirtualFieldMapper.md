# Virtual Field Mapper

P1 design for writing helper logic against virtual stores while emitting flat
optimized generated Python.

## 1. Problem

1. YIDL semantics are easiest to reason about as virtual surfaces:
   `current.foo`, `working.foo`, `field_state.foo`, `tx_state[group]`.
2. Generated code should avoid generic dictionaries and indirect lookup on hot
   paths.
3. Astichi can stitch and lower Python AST, but YIDL owns the semantic meaning
   of state locations.

## 2. Design

1. YIDL declares virtual state surfaces through `StateRef` objects.
2. Helper fragments use semantic refs instead of physical names.
3. The virtual field mapper lowers each semantic ref to a `StateNaming` slot
   on the single state/store object.
4. Astichi performs AST-level substitution from semantic paths to direct names.
5. Tests can run against virtual accessors before lowering and against flat
   generated code after lowering.

## 3. Inputs

1. Field descriptor list.
2. Transaction group mapping.
3. Virtual store declarations.
4. `StateRef` objects for every helper operation.
5. Astichi snippets that contain semantic refs.

## 4. Outputs

1. Lowered AST/source with direct physical names.
2. Mapping table useful for diagnostics and generated-source review.
3. Rejection of unknown or ambiguous virtual refs.

## 5. Astichi Boundary

1. Astichi owns AST stitching, hygiene, and materialization.
2. YIDL owns the virtual-to-physical mapping.
3. YIDL supplies Astichi with paths and bind values.
4. Astichi must not know lifecycle helper semantics by name.

## 6. Testing

1. Validate every declared `StateRef` lowers to the expected physical slot.
2. Validate invalid refs fail before code emission.
3. Execute equivalent virtual and lowered snippets where practical.
4. Include nested/staged composition cases so multi-stage builds preserve full
   paths.
5. Keep generated code free of virtual store names unless deliberately emitted
   as debug/provenance.
