# YIDL Undo Redo Concept

Status: proposed documentation example.

A small YIDL consumer could generate a Lifecycle-like data class whose
committed state is a sequence of immutable frames. A transaction edits a
working value; commit appends a frame, and undo or redo selects an existing
frame. This applies to ordinary application data, independently of any UI.

The example would demonstrate YIDL and Astichi generating another state model.
Its initial scope is one root model, one history manager, and one active edit.

## State and frames

The manager owns a sequence of frames, a cursor selecting the active frame,
and a temporary working state during an edit. Each frame contains all declared
field values for the root model. One shared cursor keeps those fields aligned.
Construction establishes the initial frame.

The generated model is a stable handle. Its current view reads the selected
frame; its working view exposes editable values inside an active transaction.
The ordinary view reads working state during an edit and current state
otherwise. Field replacement requires an active edit.

For collection fields, thaw produces an editable representation and freeze
produces a stable committed value. A list of immutable values can become a
tuple. Nested mutable contents also need conversion or copying: a tuple alone
does not make its elements immutable. Retained working references must not be
able to alter an installed frame.

## History operations

- **Begin:** create working state from the selected frame.
- **Commit:** freeze the complete candidate state, discard the redo tail, append
  the candidate frame, and advance the cursor. Complete freezing before
  changing history so a conversion failure preserves the previous frames.
- **Rollback:** discard working state and preserve the frames and cursor.
- **Undo:** move the cursor to the preceding frame.
- **Redo:** move the cursor to the following frame.

Successful edit-scope exit commits; exceptional exit rolls back. The first
example rejects nested edits and history navigation during an active edit.
Undo and redo return whether the cursor moved; reaching a history boundary
leaves state unchanged. Every successful commit records a frame, including
an unchanged value; suppressing redundant frames can be added later.

Appending, deleting, or replacing collection items simply produces another
collection value. Previous frames already contain the earlier contents, so
individual edits need no custom reversal functions. References explicitly
obtained from an older immutable frame remain historical values; navigation
does not mutate them.

## Illustrative API

All history names below are proposed, not existing YIDL or Lifecycle APIs.

```python
@undoable
class Model:
    items: tuple[str, ...] = versioned(
        default=(), thaw=list, freeze=tuple
    )


history = UndoRedoManager()
model = Model(history=history)

with history.begin():
    model.working.items.append("first")
    model.working.items.append("second")

assert model.items == ("first", "second")
assert history.undo()
assert model.items == ()
assert history.redo()
assert model.items == ("first", "second")
```

The constructor attaches the root model to its manager. The example's two
appends become one committed frame. `can_undo()` and `can_redo()` expose
navigation availability without changing state.

## Minimal implementation and verification

Generate the declared-field storage, views, write guards, and freeze/thaw
paths from YIDL resources composed through Astichi. Keep frame storage and
cursor navigation in a small manager. History publication must install a
complete frozen root as one edit boundary.

A canonical generated-source example should verify the initial frame, grouped
edits, commit, abort, cursor boundaries, and editing after undo. It should also
prove that writes outside an edit fail and later working mutations cannot
change saved frames, including retained nested values.

Ordinary lists or tuples are sufficient for the first example. Snapshot cost
depends on the chosen freeze operation; structural sharing can reduce copying
when values support it. [Pyrsistent](https://github.com/tobgu/pyrsistent)
provides immutable collections and editable evolvers as an optional foundation.
[ObjectState](https://objectstate.readthedocs.io/en/stable/undo_redo.html)
provides a separate example of grouped snapshot history.

Later extensions could add bounded retention, disk storage for serializable
frames, and node revisions for efficient comparisons. They are independent of
the basic frame-and-cursor mechanism.
