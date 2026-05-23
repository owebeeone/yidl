# YIDL Transducer Composition Model Requirements

This document is intentionally narrow.

The problem is not “how does YIDL implement owned lists?” or “how many
transducer kinds exist?” Those are downstream questions.

The core problem is:

- I have a chunk of Python code
- I turn it into an AST
- I use specially written marker calls to declare semantics at specific points
- I want to inject AST from another snippet or generate a more optimal AST
- I may need to introduce locals, loops, sequencing, try/except, accumulation,
  recovery, and reporting but also definitly unrolling as all the lists are static.

The hard part is not parsing code. The hard part is composing code-bearing ASTs
without collapsing semantics or forcing everything into crude copy/paste.

Stores themselves should still be understood as zero-behavior data objects. The
composition problem exists because semantics live in transducers and generated
control flow, not because stores are supposed to carry semantic behavior.

## 1. Core Problem

We want to use Python code snippets as semantic source material.

The intended workflow is something like:

1. write a Python-shaped snippet
2. parse it into AST
3. detect marker calls that declare composition semantics
4. replace or transform those marked regions
5. emit a final optimized AST/function/class body

The desired transforms include:

- inject AST from another snippet
- replace generic logic with specialized logic
- introduce generated local variables
- create loops or unroll loops
- expand simple operations into transaction sequencing
- add try/except/cleanup/reporting structure

This should be read consistently with the multi-facade schema:

- `current` / `working` are facade concepts
- store names are separate generated/declared names
- transducers give facade operations their meaning by mapping them onto store
  roles and control state

## 2. Why Plain AST Substitution Fails

Blind subtree replacement is not enough.

It fails because:

- names collide
- expressions may be duplicated when they should be evaluated once
- replacing an expression may require adding statements before it
- replacing a statement may require changing the enclosing block
- replacing a simple action may require building loop or transaction structure
- loops are not semantically independent copy/paste units
- cleanup/recovery often needs to happen outside the local rewrite point

So the problem is not “can we swap one AST node for another?”

The problem is:

- what composition model lets us reshape surrounding code correctly

## 3. Minimal Required Operations

Any viable composition model must support at least these operations.

### 3.1 Marker discovery

We need a way to mark semantic splice points in Python snippets.

Likely forms:

- marker call in expression position
- marker call in statement position
- marker call that declares a semantic region or expansion site

### 3.2 Expression replacement

We need to replace one expression with:

- another expression
- prelude statements plus a final expression
- a generated binding followed by an expression use

### 3.3 Statement-list replacement

We need to replace one local action with:

- multiple statements
- conditional structure
- loop structure
- try/except/finally structure

### 3.4 Hygienic local introduction

We need to introduce locals without colliding with user code or other generated
bindings.

That means:

- unique name generation
- explicit binding requests
- ability to move expensive/nontrivial expressions into generated locals

### 3.5 Single-evaluation lowering

If a source expression is used more than once, the model must be able to say:

- evaluate this once
- bind it
- reuse the binding

This is both a correctness and performance requirement.

### 3.6 Structural expansion

We need transforms such as:

- singular operation -> loop
- loop -> unrolled sequence
- simple write -> transaction sequence
- direct action -> guarded action with cleanup/recovery/reporting

This is where local replacement stops being enough.

## 4. Three Concrete Examples

These examples are intentionally non-trivial but still small.

They are not meant to define the final API. They are meant to show the kinds of
transform that the composition model must be able to express.

### 4.1 Example A: single-evaluation expression lifting

Source-shaped snippet:

```python
return compare(load_value(self), marker_old_value("total"))
```

Suppose the composition model decides that:

- `load_value(self)` must be evaluated once
- the old value must be loaded from a generated location
- the final comparison should use generated locals

The resulting shape may need to become:

```python
__y_value = load_value(self)
__y_old = self.__y_state.__y_total_old
return compare(__y_value, __y_old)
```

Here `__y_...` names are generated/internal names only. They are not intended
to appear in source-level YIDL snippets.

Transducer-side pseudocode:

```python
# current YIDL parser-shaped sketch
transducer CompareWithOldValue: fieldhelper=managed
    inputs:
        name: @id
        tx_key: @str
    behavior Working:
        source = WorkingStore
        fallback = PublishedStore
        old_value = HiddenStore
        %%
            value = load_value(self)
            old = old_value.read()
            return compare(value, old)
```

Here the important point is that the example names the roles explicitly:

- `source` / `fallback` store roles
- `old_value` control/scratch role
- `tx_key` as a declared semantic input

These examples should be read as post-normalization semantic inputs, not as a
claim that source-level omission/defaulting is already represented correctly in
the current syntax.

This is not a plain expression replacement.

It requires:

- lifting an expression into prelude statements
- hygienic local introduction
- single-evaluation lowering

### 4.2 Example B: singular operation to loop expansion

Source-shaped snippet:

```python
marker_release(item)
```

Suppose the transducer decides this is actually a container case, so the
singular release operation must expand into iteration over owned values.

The resulting shape may need to become:

```python
for __y_item in items:
    __y_item.dec_ref()
```

Transducer-side pseudocode:

```python
# current YIDL parser-shaped sketch
transducer ReleaseOwnedList: fieldhelper=owned
    inputs:
        name: @id
        tx_key: @str
    behavior Rollback:
        staged = WorkingStore
        errors = HiddenStore
        scope = current_tx_field(name, tx_key)
        %%
            if not scope.has():
                return

            staged_items = staged_value(name, tx_key, consume=True)
            rollback_each_owned(
                staged_items,
                on_error=collect(errors),
            )
            raise_collected(errors, f"{name} rollback failed")
```

This is closer to the real problem because it names:

- field identity: `name`
- transaction identity: `tx_key`
- field-local staged participation: `scope.has()`
- staged-value role: `staged`
- rollback failure collation and grouped rethrow

It also avoids hard-coding low-level loop and accumulation structure too early.
That structure is exactly the kind of thing `astichi` should still be free to
choose during composition/lowering.

This is not just “replace one call with another call”.

It requires:

- replacing a singular semantic action with a loop
- introducing per-iteration locals
- choosing what outer names are captured by the loop

### 4.3 Example C: guarded transaction-style sequencing

Source-shaped snippet:

```python
marker_commit(field_name, new_value)
```

Suppose the composition model decides commit needs:

- previous-value capture
- staged install
- deferred cleanup
- best-effort error accumulation

The resulting shape may need to become:

```python
__y_previous = committed_store.total
try:
    committed_store.total = new_value
    cleanup_queue.append(__y_previous)
except Exception as exc:
    errors.append(exc)
```

Transducer-side pseudocode:

```python
# current YIDL parser-shaped sketch
transducer GuardedCommit: fieldhelper=owned
    inputs:
        name: @id
        tx_key: @str
    behavior Commit:
        target = PublishedStore
        source = WorkingStore
        scratch = HiddenStore
        scope = current_tx_field(name, tx_key)
        %%
            if not scope.has():
                return

            previous = committed_value(name)
            next_value = staged_value(name, tx_key, consume=True)
            guarded_commit(
                target=write_committed(name, next_value),
                preserve_previous=stash(scratch, previous),
                on_error=collect(scratch),
            )
            raise_collected(scratch, f"{name} commit failed")
```

Again, the point is not the literal store names. The point is that a realistic
composition example must surface:

- committed target role
- staged source role
- scratch/deferred-cleanup role
- field-local transaction participation
- grouped error handling

It should not pre-commit to a specific `try/except` layout, local-variable
layout, or cleanup queue structure unless that exact structure is the thing
being studied.

The exact generated code may differ, but the point is the same:

- one marker at one local point may need to inject a larger guarded sequence
- the rewrite is control-flow aware, not just expression aware

These examples also do not imply that initialization tracking is already
settled. That mechanism remains `TBD`; the examples are about composition
shape, not a final initialization design.

These examples are intentionally written in the current YIDL parser shape, not
as a claim that the existing language is already sufficient. The point is to
show the kind of transducer expression surface we need to reason about using
the syntax the repo actually parses today.

## 5. The Loop Problem

Loops are the clearest example of why the model cannot be simple AST paste.

Canonical Python-shaped marker example:

```python
sum = 0
for x in astichi_for(field_values):
    sum += x
```

If a loop body is transformed:

- each iteration is not independent
- per-iteration temps and outer temps have different lifetimes
- accumulation may need to happen outside the loop
- recovery may need to happen after the loop or around the loop
- cleanup may need both per-item and post-pass phases

So “turn this singular thing into a loop of things” is not a syntactic toy. It
requires a model of:

- iteration scope
- outer scope
- accumulation scope
- error/reporting scope

Likewise, “unwind this loop” is not simple text duplication if the body itself
contains markers, bindings, or sequencing logic.

There is also one explicit unresolved input-shape question here:

- how do we feed external compile-time values into the composition system so a
  loop can be unrolled from a plain list or other constant input rather than
  only from semantic field sets

That matters for at least:

- const-unroll
- const insertion
- evaluation of alternate unrolling strategies during design work

## 6. Transaction / Recovery Expansion

Transaction logic is another forcing case.

A simple source action may need to become:

- stage
- commit
- partial rollback
- best-effort cleanup
- error accumulation
- reporting

That often means transforming a local action into something shaped like:

- prelude bindings
- guarded sequence
- try/except/finally
- multiple cleanup phases
- local accumulation variables
- final error/report emission

This is much larger than expression substitution.

## 7. The Real Question

The question is not:

- “can we interpret Python?”

The real question is:

- what is the smallest composition model that lets marker-bearing Python
  snippets be transformed into correct larger AST structures

This may mean we need to interpret a restricted semantic sublanguage embedded in
Python-shaped snippets rather than attempting to interpret arbitrary Python.

## 8. Candidate Directions

These are the broad model options.

### 8.1 Direct AST substitution

Parse snippets and replace marked nodes directly.

Strength:

- simple mental model

Weakness:

- breaks down quickly once transforms need nonlocal restructuring

### 8.2 Restricted semantic interpretation

Parse snippets, detect special marker calls, and treat those markers as a
restricted semantic language.

Strength:

- still uses Python-shaped source
- more disciplined than raw replacement

Weakness:

- requires a real composition model for the marked regions

### 8.3 IR-backed composition

Parse snippets into AST, extract marked regions into a structured intermediate
model, then lower that model back into final AST.

Strength:

- handles loops, transaction expansion, and nonlocal restructuring more cleanly

Weakness:

- adds another layer of design

The likely practical answer is some hybrid of 8.2 and 8.3.

## 9. Immediate Requirements

Before any larger transducer taxonomy is settled, the composition system needs
to prove it can represent:

- marker sites
- expression-to-block lifting
- hygienic local insertion
- single-evaluation lowering
- singular-to-loop expansion
- loop-to-unrolled-sequence expansion
- try/except/finally wrapping
- accumulation/recovery/reporting injection

If it cannot do those things, then it cannot support the larger YIDL semantic
space in a principled way.

## 10. What This Document Is For

This document is meant to keep the next design pass focused.

The next useful step is not a giant transducer catalog.

It is to answer:

1. What should marker calls mean?
2. What is the unit of replacement: expression, statement, block, or enclosing
   region?
3. How do we represent loop-aware and transaction-aware rewrites without blind
   AST paste?
4. What is the smallest viable composition model that handles these cases?
5. How do external compile-time inputs such as plain lists enter the model for
   const-unroll and const insertion?

That is the real requirement surface we need to understand first.
