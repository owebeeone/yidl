# Astichi × YIDL use cases

This document explains why an AST stitching/composition engine (`astichi`) is
useful for YIDL, what the boundary should be, and which concrete YIDL behaviors
should be modeled through it first.

The purpose is not to commit to an implementation immediately. The purpose is
to decide whether the idea is real enough to justify a separate project/module
boundary and to identify the first practical wins.

## 1. Why Astichi exists

YIDL needs to generate code for overlapping semantics:

- current vs working state
- commit/rollback logic
- freeze/thaw behavior
- binding/owned resource ordering
- local-store/native-homed fast paths
- init/default/default_factory ordering

If these are modeled as ordinary runtime helper calls, YIDL pays costs in:

- runtime call overhead
- generic state passing
- difficulty eliding dead branches
- difficulty specializing for simple cases
- difficulty fusing adjacent semantics into one optimized method body

`astichi` is the proposed answer:

- semantics are described as composable code fragments or AST fragments
- the stitcher composes them into one final method body
- the result is emitted code with the semantics blended together rather than
  chained through runtime helper calls

This is the “superpower”:

- semantic composition without runtime indirection
- optimization through composition, inlining, and elision

## 2. Why separate it from YIDL

The case for a separate project/module is strong:

- it isolates AST-version fragility in one place
- it gives one place to fix Python `ast` compatibility issues
- it keeps YIDL from growing its own embedded AST utility ecosystem
- it enforces a real architectural boundary between:
  - YIDL-specific semantics
  - generic AST stitching/composition mechanics
- it allows YIDL to keep the semantic model while `astichi` owns the AST
  mechanics

This is especially valuable if Python `ast` changes in a future release. A fix
to `astichi` can be shipped independently of broader YIDL changes.

## 3. Boundary: what belongs in Astichi vs YIDL

### 3.1 Astichi owns

`astichi` should own:

- fragment composition mechanics
- AST node rewriting helpers
- splice/stitch APIs
- dead-code elision during stitching
- temporary-name management
- sequencing/merge infrastructure for fragments
- Python-version compatibility shims around `ast`
- optional direct-emission helpers where AST composition would otherwise become
  repetitive boilerplate

`astichi` should not know lifecycle semantics by name.

It should not know:

- what a `managed` field is
- what `binding` means
- what “PublishedStore” means
- what a transaction group means

It should only know how to compose semantic fragments that YIDL provides.

### 3.2 YIDL owns

YIDL should own:

- semantic meaning of fields/helpers
- field/store/view/runtime model
- precedence and ordering semantics
- choice of which fragments are supplied for each helper
- harvested/spec metadata
- final generated class/factory structure

YIDL tells `astichi`:

- what semantic fragments exist
- how they should be sequenced or merged
- which paths are dead in a given generated context

`astichi` returns:

- stitched AST or emitted code fragments

## 4. Core composition model

The key design idea is:

- semantics are not values passed through helper calls
- semantics are code fragments that are stitched into the final caller body

This means the caller is not generic; the caller is synthesized from the
composed semantics.

Examples:

- a setter does not call `freeze_then_write_then_cleanup(value)`
- instead, the final setter body is assembled from:
  - value acquisition/normalization fragment
  - old-value capture fragment
  - write-target fragment
  - binding/resource staging fragment
  - cleanup fragment

The stitched result can omit unused steps and inline the ones that matter.

## 5. Stitching contract

The key implementation rule is that fragments do not communicate only through
ordinary function parameters and return values. They communicate through
declared semantic input modes and output/effect modes.

This is how generic logic can “bleed back” into the final generated caller in a
way that removes abstraction overhead rather than adding more of it.

### 5.1 Input modes

Fragments should be able to declare inputs such as:

- use this literal or compile-time constant
- read this local binding
- read this attribute from `self`
- use this already-built AST expression
- call this supplier expression exactly once and bind the result
- optionally request old-value capture or destination lookup semantics

The important point is that an input is not always “pass variable `x`”. An
input may instead mean “read from this place”, “bind this once”, or “splice in
this expression if the final method actually needs it”.

### 5.2 Output and effect modes

Fragments should be able to produce outputs such as:

- yield an expression upward for the enclosing fragment to consume
- assign to a declared destination
- append statements to the current method body
- emit a call as an effect, without forcing a helper boundary
- emit control flow such as `if`, early return, or raise
- request that a temporary binding be preserved for later fragments

This means the fragment interface is effect-oriented, not just value-oriented.

### 5.3 Binding model

Bindings are central because they let YIDL compute something once and then let
multiple stitched behaviors reuse it without paying runtime abstraction costs.

Examples:

- capture `old_value` once and reuse it for compare, cleanup, and hooks
- compute destination/store access once and reuse it for writeback and commit
- normalize an incoming value once and feed multiple later fragments

The stitcher should therefore treat “introduce local binding” as a first-class
operation rather than an incidental AST detail.

### 5.4 Name hygiene and single-evaluation rule

Once fragments are stitched together, variable names stop being local design
details. They become part of the composition surface.

That means `astichi` must enforce both:

- unique local-name generation across all stitched fragments
- single-evaluation lowering for expressions that may otherwise be duplicated

Examples:

- if four nested fragments all want an `input` binding, they cannot all emit
  `input` as-is
- if a supplied value comes from a call-like expression and three later
  fragments use it, the final body should usually bind it once and reuse that
  binding
- even attribute/reference reads such as `self.current.foo` may need lowering
  into a local when the access is non-trivial or used multiple times

This is not only a correctness rule. It is also a performance rule.

The stitcher should therefore model:

- caller-provided names
- fragment-requested symbolic names
- collision-free lowered local names
- explicit “evaluate once, bind, and reuse” decisions

Without this, stitching either becomes semantically unsafe or quietly
reintroduces abstraction and repeated-evaluation costs.

### 5.5 Final method boundary

The final emitted boundary is a real method or function with a specific
purpose, for example:

- field getter
- field setter
- commit-one-field
- commit-all-fields
- freeze
- thaw
- rollback fragment

That final boundary should accept only the fundamental parameters that the
caller truly owns. Everything else should be stitched into the body.

This is the point of the model: keep the public/emitted boundary small while
allowing the internal semantics to expand or collapse during generation.

### 5.6 Ambient reference rule

Generated class methods should be assumed to run with access to:

- `self`
- explicit method parameters
- locals introduced by stitching

Anything else should cross the boundary explicitly.

That keeps the generated code inspectable and prevents hidden ambient lookups
from becoming an accidental dependency channel.

### 5.7 Dead-path elision invariant

If a semantic path is not used, it should not appear in the emitted AST.

That includes:

- helper calls that become unnecessary
- old-value capture when nothing consumes it
- freeze/thaw logic when the field does not require it
- cleanup code for helpers not present on that field
- commit/rollback branches that cannot fire for the emitted class

This should be treated as a core invariant, not an optimization afterthought.

### 5.8 Function-size risk

There is some risk that stitched methods become large.

That is acceptable in the first design pass because the main purpose of
`astichi` is to eliminate abstraction overhead. If method size later becomes a
measured problem, it can be addressed with secondary controls such as:

- hoisting repeated expressions into locals
- splitting cold or error paths
- extracting non-hot helpers only where benchmarks justify it

The first-order goal remains: emit the smallest amount of code that directly
implements the needed semantics, with no generic helper layer in the hot path.

## 6. First YIDL use cases for Astichi

These are the most compelling first use cases.

### 6.1 Plain local-store / native-homed setters and getters

This is the simple fast path and a critical benchmark target.

Goal:

- generate code for local-store/native-homed fields that is as close as
  possible to plain handwritten attribute access

Why it matters:

- many properties are likely to be simple/local-like
- if YIDL is slow here, it will feel expensive everywhere
- if YIDL is near-native here, it becomes viable as the default for many
  classes

Astichi benefit:

- lets YIDL emit direct fast-path getter/setter bodies
- elides store/view indirection entirely where the semantics allow it
- avoids paying for generic runtime machinery on trivial fields

### 6.2 Managed setter composition

Managed setters involve more than “assign new value.”

Potential components:

- capture or load destination path
- capture old value if needed
- thaw or promote working state if needed
- compare / dirty-detection logic
- write to the correct store
- optionally schedule commit-time work

Astichi benefit:

- the final setter can be synthesized specifically for the field shape
- dead steps can be removed
- compare/dirty logic can be fused directly into the setter

### 6.3 Freeze/thaw

Freeze/thaw is a strong example of semantics bleeding into the caller.

Without stitching:

- setter/getter/commit code calls helper functions and passes values around

With stitching:

- freeze/thaw logic is inserted directly into the generated access or commit
  body where needed
- if the field does not use freeze/thaw, those fragments vanish completely

Astichi benefit:

- no runtime penalty for features not in use
- no generic helper chain for features that are in use

### 6.4 Binding / owned update paths

Binding/owned semantics are exactly the kind of multi-step behavior that become
expensive and messy as generic helper calls.

Potential components:

- load old value
- stage incoming value
- update store state
- perform evict-last cleanup

A useful stitched setter signature conceptually looks like:

- semantic setter fragments receive destination semantics and old-value semantics
- not just a raw parameter value

This supports a model like:

- `set(dest, old, new)` as semantic inputs
- with `dest` and `old` represented as AST-producing semantics rather than plain
  runtime values

Astichi benefit:

- write/update/cleanup become one synthesized body
- evict-last ordering is preserved without helper-call nesting
- direct fast paths can be swapped in later if a shortcut exists

### 6.5 Commit / rollback synthesis

Commit/rollback is not one feature; it is a composition surface.

Potential components:

- field commit writeback
- compare/dirty logic
- validator hooks
- before/after hooks
- resource cleanup
- group-local routing

Astichi benefit:

- commit/rollback bodies can be assembled deterministically from fragments
- ordering becomes explicit and inspectable
- group-specific or helper-specific fragments can be included only when needed

### 6.6 Init/default/default_factory ordering

Initialization is another strong composition use case.

Potential components:

- store allocation assumptions
- hidden-store access
- declaration-order sequencing
- dependency-sensitive default/default_factory logic

Astichi benefit:

- initialization logic can be generated from ordered semantic fragments rather
  than one giant handwritten template

## 7. Why this matters for performance

The clearest performance argument is:

- if YIDL can get close to native performance for the plain/local-store case
- and if it remains correct and faster than lifecycle-style generic machinery on
  more complex transactional cases
- then YIDL becomes not merely an internal convenience, but a compelling
  technology choice

That would make YIDL attractive because:

- simple fields remain cheap
- complex fields do not collapse into generic slow paths
- transactional complexity becomes specialized rather than paid at runtime for
  every access

This is the threshold where YIDL stops being “interesting compiler work” and
starts becoming “worth using for real complex transactional systems.”

## 8. Concrete study targets for Astichi

The first practical targets should be:

1. local-store/native-homed getter and setter
2. managed single-field setter
3. managed commit path for a simple field
4. freeze/thaw insertion into getter/setter/commit
5. binding/owned evict-last setter path

These should be studied before trying to generalize everything.

## 9. Success criteria for adopting Astichi

The idea is compelling enough to proceed if the study shows:

- YIDL semantic fragments can be expressed cleanly enough for stitching
- stitched methods are clearer or faster than equivalent helper-call-based
  generation
- simple/local-store cases can get near plain-property performance
- complex cases gain correctness and/or performance without exploding code
  complexity
- the boundary between YIDL semantics and AST mechanics remains clean

## 10. Main risk

The main risk is overbuilding a generic AST framework before the fragment model
is proven.

That is why the first implementation should stay focused on a handful of strong
YIDL use cases:

- local_store/native-homed fast path
- managed setter
- freeze/thaw insertion
- binding/owned evict-last update

If those do not benefit materially, the concept is weaker than it appears.

If they do, `astichi` is justified.
