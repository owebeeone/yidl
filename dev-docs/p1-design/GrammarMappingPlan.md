# Grammar Mapping Plan

Current P1 grammar-to-model mapping.

## 1. Boundary

1. YIDL grammar expresses lifecycle semantics.
2. YIDL grammar does not expose flattened slot names or `_y_*` internals.
3. Field helper syntax maps to transducer artifacts that generate field
   descriptors and helper factories.
4. Callable syntax maps to callable-wrapper/lowerer inputs.
5. Transaction group syntax maps to immutable class tx metadata.
6. Behavior snippets lower through Astichi only after YIDL has assigned
   semantic meaning.
7. A compiled YIDL file is a generated Python library: it contains functions
   and decorators that generate the target class.

## 2. Parser Shape

1. Lexer is indentation-aware.
2. Lexer recognizes `%% ... %%` Python fences.
3. Parser is pure Python recursive descent.
4. Output AST has typed categories:
   1. Transducer nodes.
   2. Behavior nodes.
   3. Code nodes.
   4. Marker nodes.

## 3. Mapping Targets

| Grammar surface | Lowering target |
|---|---|
| Field helper declaration | Field descriptor / FieldSpec |
| Transducer declaration | Helper factory / class-generation function |
| Transaction group | `tx_key_to_index` / `tx_index_to_group` metadata |
| Callable body/reference | Callable injection lowerer input |
| Behavior snippet | Astichi `Composable` fragment |
| Virtual state reference | `StateRef` |
| Cleanup/destruction policy | Field operation metadata |

## 4. Known P1 Gaps

1. Virtual value homes required by each transducer.
2. Field-local scratch / previous-commit retention policy.
3. Destruction / cleanup policy declaration.
4. Rollback error aggregation syntax.
5. Optimized per-kind surface placement.
6. Single/list/map resource transducer selection for `binding` and `owned`
   while preserving that `binding` is non-transactional and `owned` is
   transaction-aware.
7. Cross-group visibility rules.
8. Annotation-driven behavior, if any; P1 uses explicit helper kwargs.

## 5. Bootstrap Containers

1. `_yidl.py` containers are development-only.
2. Canonical wrapper is `yidl.embed(source, yidl.global_args, globals())`.
3. Bootstrap is not a PRE_IMPL gate; it lands when source-in-Python probes need
   it.
4. Bootstrap must preserve source and source-line metadata for diagnostics.

## 6. Rules

1. Do not add grammar that bypasses the semantic model.
2. Do not introduce compiler internals into user syntax.
3. Unsupported features fail explicitly and locally.
4. Grammar work follows layout, refs, callables, and operation matrices.
