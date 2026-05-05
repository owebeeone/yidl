class Example:

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value

    @property
    def owner(self):
        return self._owner_working

    @owner.setter
    def owner(self, value):
        self._owner_working = value

    @property
    def label(self):
        return self._label

    @property
    def session(self):
        return self._session_working
