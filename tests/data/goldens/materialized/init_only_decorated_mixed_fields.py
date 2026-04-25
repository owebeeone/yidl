def make_wrapper_class(class_definition):
    _y_class_definition = class_definition
    _y_wrapped_class = _y_class_definition.wrapped_class
    _y_required_anno = _y_class_definition.fields_by_name['required'].field_anno
    _y_token_anno = _y_class_definition.fields_by_name['token'].field_anno
    _y_token_default = _y_class_definition.fields_by_name['token'].default
    _y_label_default = _y_class_definition.fields_by_name['label'].default

    class Session(_y_wrapped_class):
        __yidl_class_definition__ = _y_class_definition

        def __init__(self, *, required: _y_required_anno, token: _y_token_anno=_y_token_default):
            self.required = required
            self.token = token
            self.label = _y_label_default
    return Session
