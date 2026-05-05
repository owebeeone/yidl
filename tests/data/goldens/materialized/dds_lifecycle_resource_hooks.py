_NO_WORKING_VALUE = object()

class ExampleState:
    __slots__ = ('_count_current', '_count_working', '_resource_value')

    def __init__(self, *, count: int=0, resource: object=None):
        self._count_current = count
        self._count_working = _NO_WORKING_VALUE
        self._resource_value = resource

class Example:
    __slots__ = ('_state',)

    def __init__(self, *, count: int=0, resource: object=None):
        self._state = ExampleState(count=count, resource=resource)

    @property
    def count(self):
        state = self._state
        if state._count_working is not _NO_WORKING_VALUE:
            return state._count_working
        return state._count_current

    @count.setter
    def count(self, value):
        self._state._count_working = value

    @property
    def resource(self):
        return self._state._resource_value

    def commit(self):
        state = self._state
        before_default(current=self)
        validate_default(current=self)
        if state._count_working is not _NO_WORKING_VALUE:
            state._count_current = state._count_working
            state._count_working = _NO_WORKING_VALUE
        after_default(current=self)

    def rollback(self):
        state = self._state
        state._count_working = _NO_WORKING_VALUE
        rollback_default(current=self)

    def close(self):
        state = self._state
        value = state._resource_value
        if value is not None:
            release_resource(value)
