class Example:
    __slots__ = ('count', 'label', 'cache', 'retries')

    def __init__(self, *, count, label='cold', retries=3):
        self.count = count
        self.label = label
        self.retries = retries
