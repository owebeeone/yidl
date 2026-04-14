"""
Target shape for lifecycle codegen (see docs/YIDLDesign.md §5).

Two-phase picture:
  1) YIDL compiler → FieldSpec / helper functions (schema; what the harvester reads).
  2) Generated @managed_context (or equivalent) → builds a spec dict and exec()s a
     factory like this so UserBaseClass, thaw/freeze, and factories are captured as
     closures on the emitted Proxy / view classes (LOAD_DEREF), not stored on instances.

This module is hand-maintained as a reference skeleton until the string builder emits it.
"""

def build_bar_class(bar_spec):
    # =========================================================================
    # LOCAL VARIABLE EXTRACTION (For debuggability and closure capture)
    # =========================================================================
    MISSING = bar_spec['MISSING']
    UserBaseClass = bar_spec['UserBaseClass']
    __thaw_b = bar_spec['thaw_b']
    __freeze_b = bar_spec['freeze_b']
    __c_factory = bar_spec['c_factory']
    __d_factory = bar_spec['d_factory']

    # =========================================================================
    # 1. PHYSICAL DATA STORES (No Logic, Just Slotted Memory)
    # =========================================================================
    class _Bar_PublishedStore:
        __slots__ = ('a', 'b', 'c')
        def __init__(self):
            self.a = MISSING
            self.b = MISSING
            self.c = MISSING

    class _Bar_WorkingStore:
        __slots__ = ('a', 'b', 'c')
        def __init__(self):
            self.a = MISSING
            self.b = MISSING
            self.c = MISSING

    # =========================================================================
    # 2. LOGICAL SURFACES (Facades)
    # =========================================================================
    class _Bar_CurrentView(UserBaseClass):
        __slots__ = ('_published', 'current', '_main_instance')

        def __init__(self, published_store):
            self._published = published_store
            self.current = self  # Deterministic routing
            self._main_instance = None # Wired up in Main

        # Field 'a' (Managed)
        @property
        def a(self): return self._published.a

        # Field 'b' (Managed)
        @property
        def b(self): return self._published.b

        # Field 'c' (Binding)
        @property
        def c(self): return self._published.c

        # Field 'd' (Local Store - Homed on Instance)
        # The Current view delegates local store reads back to the main instance
        @property
        def d(self): return self._main_instance.d


    class _Bar_WorkingView(UserBaseClass):
        __slots__ = ('_published', '_working', '_txm', 'working', 'current')

        def __init__(self, published_store, working_store, txm):
            self._published = published_store
            self._working = working_store
            self._txm = txm

            self.working = self  # Deterministic routing
            self.current = None  # Wired up in Main

        # --- Field 'a' (Managed) ---
        @property
        def a(self):
            return self._working.a if self._working.a is not MISSING else self._published.a

        @a.setter
        def a(self, value):
            self._working.a = value
            self._txm.mark_dirty(self, "DEFAULT_TRANSACTION")

        # --- Field 'b' (Managed with Copy-on-Read / Thaw) ---
        @property
        def b(self):
            if self._working.b is MISSING:
                # CLOSURE CAPTURE: __thaw_b is resolved from the function scope!
                self._working.b = __thaw_b(self._published.b)
            return self._working.b

        @b.setter
        def b(self, value):
            self._working.b = value
            self._txm.mark_dirty(self, "DEFAULT_TRANSACTION")

        # --- Field 'c' (Binding with overwrite safety) ---
        @property
        def c(self):
            return self._working.c if self._working.c is not MISSING else self._published.c

        @c.setter
        def c(self, value):
            # 1. Stage new value
            if value is not None:
                value.inc_ref()

            old_val = self._working.c

            # 2. Update structures so the tree is completely consistent
            self._working.c = value
            self._txm.mark_dirty(self, "DEFAULT_TRANSACTION")

            # 3. Evict old value LAST to safely isolate any side-effects
            if old_val is not MISSING and old_val is not None:
                old_val.dec_ref()


    # =========================================================================
    # 3. THE MAIN PROXY CLASS (Instantiated by the user)
    # =========================================================================
    class Bar(UserBaseClass):
        # 'd' is homed directly on the proxy instance for raw python speed
        __slots__ = ('_published', '_working', 'current', 'working', '_txm', 'd')

        def __init__(self, a=MISSING, b=MISSING, txm=None):
            # 1. Initialize Stores
            self._published = _Bar_PublishedStore()
            self._working = _Bar_WorkingStore()
            self._txm = txm

            # 2. Initialize Views
            self.current = _Bar_CurrentView(self._published)
            self.working = _Bar_WorkingView(self._published, self._working, self._txm)

            # Cross-wire specific fallbacks
            self.current._main_instance = self
            self.working.current = self.current

            # 3. Sequential Field Initialization (Init Surface)
            if a is not MISSING:
                self._published.a = a

            if b is not MISSING:
                self._published.b = b

            # CLOSURE CAPTURE: __c_factory is resolved from the function scope
            if __c_factory is not None:
                val = __c_factory(self)
                self._published.c = val
                if val is not None: val.inc_ref()

            # CLOSURE CAPTURE: __d_factory is resolved from the function scope
            if __d_factory is not None:
                self.d = __d_factory(self) # Homed directly on self!

        # --- Proxy Routing Properties ---
        @property
        def a(self):
            return self.working.a if self._txm.is_active("DEFAULT_TRANSACTION") else self.current.a

        @a.setter
        def a(self, value):
            if not self._txm.is_active("DEFAULT_TRANSACTION"): raise RuntimeError()
            self.working.a = value

        # ... (Same routing for b and c) ...

        # --- Transaction Hooks (Compiled directly into the class) ---
        def _lc_commit(self, group):
            if group == "DEFAULT_TRANSACTION":
                # Unrolled Managed Commit (a)
                if self._working.a is not MISSING:
                    self._published.a = self._working.a
                    self._working.a = MISSING

                # Unrolled Managed Commit with Freeze (b)
                if self._working.b is not MISSING:
                    # CLOSURE CAPTURE: __freeze_b is resolved from the function scope!
                    self._published.b = __freeze_b(self._working.b)
                    self._working.b = MISSING

                # Unrolled Binding Commit (c)
                if self._working.c is not MISSING:
                    new_binding = self._working.c
                    old_binding = self._published.c

                    # 1. Promote new value
                    if new_binding is not None: new_binding.accepted()

                    # 2. Update structures so the tree is completely consistent
                    self._published.c = new_binding
                    self._working.c = MISSING

                    # 3. Evict old value LAST to safely isolate any side-effects
                    if old_binding is not None: old_binding._close()

    return Bar
