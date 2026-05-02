from itertools import product
from yidl.generation.data_def_sys import MatcherResult, NOT_PROVIDED

class RangeMatcher:

    def __init__(self):
        self._cache = {}

    def resolve(self, record_record):
        records = (record_record,)
        values = (getattr(record_record, 'p0', NOT_PROVIDED), getattr(record_record, 'p1', NOT_PROVIDED), getattr(record_record, 'p2', NOT_PROVIDED), getattr(record_record, 'p3', NOT_PROVIDED), getattr(record_record, 'p4', NOT_PROVIDED), getattr(record_record, 'p5', NOT_PROVIDED), getattr(record_record, 'p6', NOT_PROVIDED), getattr(record_record, 'p7', NOT_PROVIDED), getattr(record_record, 'p8', NOT_PROVIDED), getattr(record_record, 'p9', NOT_PROVIDED))
        try:
            cached = self._cache.get(values, NOT_PROVIDED)
        except TypeError:
            cached = NOT_PROVIDED
            cache_key = None
        else:
            cache_key = values
        if cached is not NOT_PROVIDED:
            return self._finish(None, cached, records, values)
        if values[0:10] == (0, 1, 2, 3, 4, 5, 6, 7, 8, 9):
            return self._finish(cache_key, (FullRange, 'full', 10.0), records, values)
        if values[0:2] + values[4:6] + values[8:10] == (0, 1, 4, 5, 8, 9):
            return self._finish(cache_key, (SegmentRange, 'segments', 6.0), records, values)
        if values[1:2] + values[3:4] + values[5:6] + values[7:8] + values[9:10] == (1, 3, 5, 7, 9):
            return self._finish(cache_key, (OddRange, 'odd', 5.0), records, values)
        return self._finish(cache_key, (DefaultRange, None, 0.0), records, values)

    def _finish(self, cache_key, selection, records, values):
        if cache_key is not None:
            self._cache[cache_key] = selection
        if selection is None:
            return None
        resource, rule, score = selection
        return MatcherResult(resource=resource, rule=rule, score=score, records=records, values=values)

    def sequence(self, *record_sequences):
        if len(record_sequences) != 1:
            raise ValueError('wrong number of record sequences')
        for records in product(*record_sequences):
            result = self.resolve(*records)
            if result is not None:
                yield result
