# YIDL Cleanup Reccomendations

This is a cleanup plan, not an implementation patch. It identifies source and
test material that appears to be a false start now that the working lifecycle
path lives in `../yidl-lifecycle` and the active generic compiler substrate is
the recorded concept / DDS / assembly stack in `src/yidl`.

Cleanup must preserve the current generated lifecycle base:

- `../yidl-lifecycle/src/yidl_lifecycle/yidl/*.yidl`
- `../yidl-lifecycle/src/yidl_lifecycle/_generated_lifecycle_base.py`

After any cleanup step, the generated base should compare unchanged and the
`../yidl-lifecycle` golden tests should continue to pass.

## 1. Keep As Canonical

These files are part of the current working system and should not be deleted as
part of false-start cleanup.

In `yidl`:

1. `src/yidl/concept_parser.py`
2. `src/yidl/concept_grammar.lark`
3. `src/yidl/capsule/recorded_builder.py`
4. `src/yidl/generation/assembly_plan.py`
5. `src/yidl/generation/assembly_runtime.py`
6. `src/yidl/generation/assembly_source.py`
7. `src/yidl/generation/container_runtime_source.py`
8. `src/yidl/generation/data_def_sys.py`
9. `src/yidl/generation/data_schema.py`
10. `src/yidl/generation/data_container.py`
11. `src/yidl/generation/data_production.py`
12. `src/yidl/generation/matcher.py`
13. `src/yidl/generation/matcher_values.py`
14. `src/yidl/sentinel_maker.py`
15. `src/yidl/testing/versioned_test_harness.py`, unless lifecycle gets an
    owned copy first.

In `../yidl-lifecycle`:

1. `src/yidl_lifecycle/lifecycle.py`
2. `src/yidl_lifecycle/lifecycle_harvester.py`
3. `src/yidl_lifecycle/lifecycle_markers.py`
4. `src/yidl_lifecycle/transaction_yidl.py`
5. `src/yidl_lifecycle/bindings.py`
6. `src/yidl_lifecycle/bindings_refcount.py`, until the explicit-refcount
   runtime is deliberately dropped.
7. `src/yidl_lifecycle/yidl/*.yidl`
8. `src/yidl_lifecycle/_generated_lifecycle_base.py`
9. `tests/test_yidl_goldens.py`
10. `tests/test_lifecycle_yidl_layering.py`
11. `tests/data/gold_src/*`
12. `tests/data/goldens/materialized/*`

## 2. Delete Or Retire From `yidl`

These files are the old indentation/transducer/API-generation prototype. They
are not used by the current lifecycle generation path.

Recommended deletion set:

1. `src/yidl/lexer.py`
2. `src/yidl/parser.py`
3. `src/yidl/cli.py`
4. `src/yidl/ast_tx.py`
5. `tests/test_lexer.py`
6. `tests/test_parser.py`
7. `tests/test_cli.py`
8. `tests/test_ast_tx.py`
9. `example/example.yidl`, if it only exists to exercise `yidl-compile`.

Required companion edits:

1. Remove the `yidl-compile = "yidl.cli:main"` script from `pyproject.toml`, or
   replace it with a new concept/lifecycle regeneration command.
2. Remove `Token`, `lex_yidl`, `AST`, and `YIDLParser` exports from
   `src/yidl/__init__.py`.
3. Remove docs that describe the old indentation parser as active. The current
   archived copy is under `dev-docs/history/`.
4. If any downstream consumer still imports these names, create a short
   deprecation branch first instead of deleting immediately.

Suggested verification:

1. `uv run --with pytest pytest tests/generation tests/capsule tests/test_yidl_goldens.py -q`
2. From `../yidl-lifecycle`: `uv run --with pytest pytest tests/test_yidl_goldens.py tests/test_lifecycle_yidl_layering.py -q`

## 3. Review Before Deleting `yidl` Capsule Prototypes

These files are probably superseded by recorded concepts and assembly, but they
may still document useful prototype behavior or remain imported by tests.

Candidate cleanup set:

1. `src/yidl/capsule/init_only_capsule.py`
2. `tests/capsule/test_init_only_capsule.py`
3. Old fluent capsule exports from `src/yidl/capsule/__init__.py`, if any
   remain after current imports are audited.

Do not delete these in the same commit as the old parser cleanup unless import
usage is checked first. The safer sequence is:

1. Confirm the lifecycle generation path does not import them.
2. Confirm active tests do not rely on them except their own prototype tests.
3. Delete the prototype and tests together.
4. Keep any reusable idea only if it is rewritten into recorded concept /
   assembly terminology.

## 4. Remove Or Collapse Obsolete Tests

These tests should be removed with the old parser/CLI files because they assert
behavior that is no longer the working system:

1. `tests/test_cli.py`
2. `tests/test_parser.py`
3. `tests/test_lexer.py`
4. `tests/test_ast_tx.py`

Tests that should stay:

1. Golden fixture tests in both `yidl` and `../yidl-lifecycle`, because they
   protect generated source shape.
2. `yidl` generation/container/matcher/assembly tests, because they protect the
   generic substrate used by lifecycle YIDL layers.
3. `../yidl-lifecycle/tests/test_lifecycle_decorator.py`, because it is the
   broad behavior regression suite for the generated decorator.
4. `../yidl-lifecycle/tests/test_lifecycle_harvester.py`, because it protects
   source-class harvesting and diagnostics.
5. `../yidl-lifecycle/tests/test_transaction_yidl.py`, because generated code
   targets that transaction runtime.
6. `../yidl-lifecycle/tests/test_bindings.py` and
   `../yidl-lifecycle/tests/test_bindings_refcount.py`, until the runtime
   binding policy is reduced to one implementation.

## 5. Lifecycle Source Cleanup Candidates

No lifecycle source files should be deleted now. The current package is small
and every source module has an active role:

1. `lifecycle.py` is the decorator frontend and generator bridge.
2. `lifecycle_harvester.py` owns class harvesting, inheritance facts, and
   collision diagnostics.
3. `lifecycle_markers.py` owns public marker factories and transaction method
   decorators.
4. `transaction_yidl.py` owns the runtime transaction manager targeted by
   generated classes.
5. `bindings.py` is the default binding runtime.
6. `bindings_refcount.py` is an alternate explicit-refcount runtime with tests.
7. `_generated_lifecycle_base.py` is generated from current YIDL layers and
   must remain committed until the project adopts a generated-at-build policy.

Possible future removals:

1. Delete `bindings_refcount.py` and `tests/test_bindings_refcount.py` only if
   the design drops explicit-refcount support.
2. Trim phase-named golden cases only after a smaller semantic golden matrix
   covers the same generated behavior. Do not remove broad generated-output
   coverage before then.
3. Rename phase-labeled tests/goldens later for readability, but do not do it
   in the same cleanup that verifies generated source is unchanged.

## 6. Dev-Docs Cleanup Completed

The active `dev-docs` directory should now contain only:

1. `YidlCodingRules.md`
2. `YidlDesignSummary.md`
3. `YidlDesignSummary-gaps2.md`
4. `YidlCleanupReccomendations.md`
5. `history/`

Everything else that used to be top-level dev-doc material belongs in
`dev-docs/history/` and should be treated as read-only background.

## 7. Recommended Cleanup Order

1. Use `yidl-lifecycle-regenerate-base` as the stable regeneration/no-diff
   command for
   `../yidl-lifecycle/src/yidl_lifecycle/_generated_lifecycle_base.py`.
2. Remove the old `yidl` parser/CLI/AST transformer files and their tests.
3. Update `src/yidl/__init__.py` and `pyproject.toml` to stop exporting the old
   prototype as public API.
4. Run `yidl` substrate tests and `../yidl-lifecycle` golden/layering tests.
5. Review and remove `init_only_capsule.py` only after the first cleanup lands
   and import usage is known.
6. Revisit lifecycle golden case names and phase labels as a separate
   readability cleanup.

## 8. No-Diff Guardrail

Before and after each cleanup step, compare the generated lifecycle base:

1. Run `yidl-lifecycle-regenerate-base` from `../yidl-lifecycle` to check the
   committed generated base against `src/yidl_lifecycle/yidl/*.yidl`.
2. Use `yidl-lifecycle-regenerate-base --write` only when intentionally
   refreshing
   `../yidl-lifecycle/src/yidl_lifecycle/_generated_lifecycle_base.py`.
3. If there is any diff, stop and classify it as either a generator behavior
   change or a stale committed generated file. Do not mix that change with
   false-start deletion.
