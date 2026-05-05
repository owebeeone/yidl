_NO_WORKING_VALUE = object()

class ExampleState:
    __slots__ = ('_count_current', '_count_working', '_label_value')

    def __init__(self, *, count, label):
        self._count_current = count
        self._count_working = _NO_WORKING_VALUE
        self._label_value = label

class Example:
    __slots__ = ('_state',)

    def __init__(self, *, count, label):
        self._state = ExampleState(count=count, label=label)

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
    def label(self):
        return self._state._label_value
