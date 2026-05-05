_NO_WORKING_VALUE = object()

class ExampleState:
    __slots__ = ('_owner_retained',)

    def __init__(self, *, owner):
        self._owner_retained = owner

class Example:
    __slots__ = ('_state',)

    def __init__(self, *, seed, owner):
        self._state = ExampleState(owner=owner)
