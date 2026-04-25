def make_wrapper_class(class_definition):
    _y_class_definition = class_definition
    _y_wrapped_class = _y_class_definition.wrapped_class
    _y_count_anno = _y_class_definition.fields_by_name['count'].field_anno
    _y_count_default = _y_class_definition.fields_by_name['count'].default
    _y_label_default = _y_class_definition.fields_by_name['label'].default

    class Example(_y_wrapped_class):
        __yidl_class_definition__ = _y_class_definition

        def __init__(self, *, count: _y_count_anno=_y_count_default):
            self.count = count
            self.label = _y_label_default
    return Example
