from itertools import product
from yidl.generation.data_def_sys import MatcherResult, NOT_PROVIDED, from_astichi_code

class GetterMatcher:

    def __init__(self):
        self._cache = {}

    def resolve(self, field_record):
        records = (field_record,)
        values = (getattr(field_record, 'init', NOT_PROVIDED), getattr(field_record, 'annotation', NOT_PROVIDED), is_managed_field(field_record))
        try:
            cached = self._cache.get(values, NOT_PROVIDED)
        except TypeError:
            cached = NOT_PROVIDED
            cache_key = None
        else:
            cache_key = values
        if cached is not NOT_PROVIDED:
            return self._finish(None, cached, records, values)
        if values[0:3] == (False, str, True):
            return self._finish(cache_key, (from_astichi_code("{'getter': 'managed'}"), 'managed-string-no-init', 3.0), records, values)
        if values[0:2] == (False, str):
            return self._finish(cache_key, (from_astichi_code("{'getter': 'plain'}"), 'plain-string-no-init', 2.0), records, values)
        return self._finish(cache_key, (from_astichi_code('astichi_pyimport(module="yidl.generation.data_def_sys", names=("REQUIRED",))\nREQUIRED\n'), None, 0.0), records, values)

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
