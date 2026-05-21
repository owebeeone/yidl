from yidl.generation.data_def_sys import AddIfAbsent, AssemblyDiagnosticError, DDSContainerBuilder, DDSOperationContext, NOT_PROVIDED, REQUIRED, RejectDuplicate, ReplaceExisting, RuntimeCollection, RuntimeComputedCollection, RuntimeContainerSpec, RuntimePort, RuntimePortIndex, RuntimeProperty, RuntimeRecord, RuntimeUnion
_NameProperty = RuntimeProperty('Name', str, default=REQUIRED, storage_name='name')
_SourceLabelProperty = RuntimeProperty('SourceLabel', str, default='', storage_name='source_label')
_SeverityProperty = RuntimeProperty('Severity', str, default=REQUIRED, storage_name='severity')
_CategoryProperty = RuntimeProperty('Category', str, default=REQUIRED, storage_name='category')
_MessageProperty = RuntimeProperty('Message', str, default=REQUIRED, storage_name='message')
_FieldNameProperty = RuntimeProperty('FieldName', str, default='', storage_name='field_name')
_ConceptNameProperty = RuntimeProperty('ConceptName', str, default='', storage_name='concept_name')
_FieldSpec = RuntimeRecord('Field', (_NameProperty, _SourceLabelProperty))
_DiagnosticSpec = RuntimeRecord('Diagnostic', (_SeverityProperty, _CategoryProperty, _MessageProperty, _SourceLabelProperty, _FieldNameProperty, _ConceptNameProperty))

class Field:
    __slots__ = ('name', 'source_label')
    __dds_record_spec__ = _FieldSpec
    name: str
    source_label: str

    def __init__(self, *, name: str, source_label: str=''):
        if not isinstance(name, str):
            raise TypeError('Name must be str, got ' + type(name).__name__)
        object.__setattr__(self, 'name', name)
        if not isinstance(source_label, str):
            raise TypeError('SourceLabel must be str, got ' + type(source_label).__name__)
        object.__setattr__(self, 'source_label', source_label)

    def __setattr__(self, name, value):
        if name in ('name', 'source_label'):
            raise AttributeError('Field records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('name=' + repr(self.name))
        pieces.append('source_label=' + repr(self.source_label))
        return 'Field' + '(' + ', '.join(pieces) + ')'
_FieldSpec.bind_record_class(Field)

class Diagnostic:
    __slots__ = ('severity', 'category', 'message', 'source_label', 'field_name', 'concept_name')
    __dds_record_spec__ = _DiagnosticSpec
    severity: str
    category: str
    message: str
    source_label: str
    field_name: str
    concept_name: str

    def __init__(self, *, severity: str, category: str, message: str, source_label: str='', field_name: str='', concept_name: str=''):
        if not isinstance(severity, str):
            raise TypeError('Severity must be str, got ' + type(severity).__name__)
        object.__setattr__(self, 'severity', severity)
        if not isinstance(category, str):
            raise TypeError('Category must be str, got ' + type(category).__name__)
        object.__setattr__(self, 'category', category)
        if not isinstance(message, str):
            raise TypeError('Message must be str, got ' + type(message).__name__)
        object.__setattr__(self, 'message', message)
        if not isinstance(source_label, str):
            raise TypeError('SourceLabel must be str, got ' + type(source_label).__name__)
        object.__setattr__(self, 'source_label', source_label)
        if not isinstance(field_name, str):
            raise TypeError('FieldName must be str, got ' + type(field_name).__name__)
        object.__setattr__(self, 'field_name', field_name)
        if not isinstance(concept_name, str):
            raise TypeError('ConceptName must be str, got ' + type(concept_name).__name__)
        object.__setattr__(self, 'concept_name', concept_name)

    def __setattr__(self, name, value):
        if name in ('severity', 'category', 'message', 'source_label', 'field_name', 'concept_name'):
            raise AttributeError('Diagnostic records are immutable')
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append('severity=' + repr(self.severity))
        pieces.append('category=' + repr(self.category))
        pieces.append('message=' + repr(self.message))
        pieces.append('source_label=' + repr(self.source_label))
        pieces.append('field_name=' + repr(self.field_name))
        pieces.append('concept_name=' + repr(self.concept_name))
        return 'Diagnostic' + '(' + ', '.join(pieces) + ')'
_DiagnosticSpec.bind_record_class(Diagnostic)
FieldsCollection = RuntimeCollection('Fields', _FieldSpec, allows_multiple=True, identity=None)
DiagnosticsCollection = RuntimeCollection('Diagnostics', _DiagnosticSpec, allows_multiple=True, identity=None)
_RUNTIME_SPEC = RuntimeContainerSpec(collections=(FieldsCollection, DiagnosticsCollection), computed_collections=(), ports=(), port_index=None)

def run_validate_duplicate_fields(builder):
    ctx = DDSOperationContext(builder, 'ValidateDuplicateFields', ordered_inputs={})
    seen = set()
    for field in ctx.records(FieldsCollection):
        if field.name not in seen:
            seen.add(field.name)
            continue
        ctx.write(DiagnosticsCollection, Diagnostic(severity='error', category='design_conflict', message=f'duplicate field {field.name!r}', source_label=field.source_label, field_name=field.name, concept_name='FieldValidation'), policy=RejectDuplicate)

def run_raise_diagnostics(builder):
    ctx = DDSOperationContext(builder, 'RaiseDiagnostics', ordered_inputs={})
    errors = [diagnostic for diagnostic in ctx.records(DiagnosticsCollection) if diagnostic.severity == 'error']
    if errors:
        raise TypeError('\n'.join((diagnostic.message for diagnostic in errors)))

def run_operations(builder):
    run_validate_duplicate_fields(builder)
    run_raise_diagnostics(builder)
    return builder

def build_container(builder):
    run_operations(builder)
    return builder.freeze()

class _GeneratedMatcherNamespace:

    def __init__(self, container):
        pass

class _GeneratedContainerBuilder:

    def __init__(self):
        self._builder = DDSContainerBuilder(_RUNTIME_SPEC)

    def add(self, *args, **kwargs):
        self._builder.add(*args, **kwargs)
        return self

    def write(self, *args, **kwargs):
        self._builder.write(*args, **kwargs)
        return self

    def children_at(self, port_address):
        return self._builder.children_at(port_address)

    def _snapshot(self):
        container = self._builder._snapshot()
        container.matchers = _GeneratedMatcherNamespace(container)
        return container

    def record(self, *args, **kwargs):
        return self._builder.record(*args, **kwargs)

    def freeze(self):
        container = self._builder.freeze()
        container.matchers = _GeneratedMatcherNamespace(container)
        return container

    def __getattr__(self, name):
        return getattr(self._builder, name)

def new_builder():
    return _GeneratedContainerBuilder()
