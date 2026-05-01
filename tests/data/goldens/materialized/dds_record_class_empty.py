from yidl.generation.data_def_sys import dds_record_spec

class Empty:
    __slots__ = ()
    __dds_record_spec__ = dds_record_spec('Empty')

    def __init__(self):
        pass

    def __repr__(self):
        return 'Empty' + '()'
