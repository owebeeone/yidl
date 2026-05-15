from yidl.generation.data_def_sys import (
    AddIfAbsent,
    DDSContainerBuilder,
    NOT_PROVIDED,
    REQUIRED,
    RejectDuplicate,
    ReplaceExisting,
    RuntimeCollection,
    RuntimeComputedCollection,
    RuntimeContainerSpec,
    RuntimePort,
    RuntimePortIndex,
    RuntimeProperty,
    RuntimeRecord,
    RuntimeUnion,
)

_ClassIdProperty = RuntimeProperty(
    "ClassId", str, default=REQUIRED, storage_name="class_id"
)
_ClassNameProperty = RuntimeProperty(
    "ClassName", str, default=REQUIRED, storage_name="class_name"
)
_ClassOrderProperty = RuntimeProperty(
    "ClassOrder", int, default=0, storage_name="class_order"
)
_ModuleNameProperty = RuntimeProperty(
    "ModuleName", str, default="__main__", storage_name="module_name"
)
_BasesProperty = RuntimeProperty("Bases", object, default=(), storage_name="bases")
_DecoratorInitProperty = RuntimeProperty(
    "DecoratorInit", bool, default=True, storage_name="decorator_init"
)
_DecoratorReprProperty = RuntimeProperty(
    "DecoratorRepr", bool, default=True, storage_name="decorator_repr"
)
_DecoratorEqProperty = RuntimeProperty(
    "DecoratorEq", bool, default=True, storage_name="decorator_eq"
)
_DecoratorOrderProperty = RuntimeProperty(
    "DecoratorOrder", bool, default=False, storage_name="decorator_order"
)
_DecoratorUnsafeHashProperty = RuntimeProperty(
    "DecoratorUnsafeHash", bool, default=False, storage_name="decorator_unsafe_hash"
)
_DecoratorFrozenProperty = RuntimeProperty(
    "DecoratorFrozen", bool, default=False, storage_name="decorator_frozen"
)
_DecoratorSlotsProperty = RuntimeProperty(
    "DecoratorSlots", bool, default=False, storage_name="decorator_slots"
)
_DecoratorWeakrefSlotProperty = RuntimeProperty(
    "DecoratorWeakrefSlot", bool, default=False, storage_name="decorator_weakref_slot"
)
_DecoratorMatchArgsProperty = RuntimeProperty(
    "DecoratorMatchArgs", bool, default=True, storage_name="decorator_match_args"
)
_DecoratorKwOnlyProperty = RuntimeProperty(
    "DecoratorKwOnly", bool, default=False, storage_name="decorator_kw_only"
)
_HasPostInitProperty = RuntimeProperty(
    "HasPostInit", bool, default=False, storage_name="has_post_init"
)
_HasKwOnlyInitFieldsProperty = RuntimeProperty(
    "HasKwOnlyInitFields", bool, default=False, storage_name="has_kw_only_init_fields"
)
_KwOnlyFenceOrderProperty = RuntimeProperty(
    "KwOnlyFenceOrder", int, default=0, storage_name="kw_only_fence_order"
)
_DataclassParamsProperty = RuntimeProperty(
    "DataclassParams", object, default=None, storage_name="dataclass_params"
)
_SlotNamesProperty = RuntimeProperty(
    "SlotNames", object, default=(), storage_name="slot_names"
)
_MatchArgsProperty = RuntimeProperty(
    "MatchArgs", object, default=(), storage_name="match_args"
)
_FieldIdProperty = RuntimeProperty(
    "FieldId", str, default=REQUIRED, storage_name="field_id"
)
_FieldOwnerProperty = RuntimeProperty(
    "FieldOwner", str, default=REQUIRED, storage_name="field_owner"
)
_FieldNameProperty = RuntimeProperty(
    "FieldName", str, default=REQUIRED, storage_name="field_name"
)
_FieldOrderProperty = RuntimeProperty(
    "FieldOrder", int, default=REQUIRED, storage_name="field_order"
)
_FieldKindProperty = RuntimeProperty(
    "FieldKind", str, default="field", storage_name="field_kind"
)
_AnnotationProperty = RuntimeProperty(
    "Annotation", object, default=object, storage_name="annotation"
)
_HasDefaultProperty = RuntimeProperty(
    "HasDefault", bool, default=False, storage_name="has_default"
)
_DefaultValueProperty = RuntimeProperty(
    "DefaultValue", object, default=None, storage_name="default_value"
)
_HasDefaultFactoryProperty = RuntimeProperty(
    "HasDefaultFactory", bool, default=False, storage_name="has_default_factory"
)
_DefaultFactoryProperty = RuntimeProperty(
    "DefaultFactory", object, default=None, storage_name="default_factory"
)
_InitProperty = RuntimeProperty("Init", bool, default=True, storage_name="init")
_ReprProperty = RuntimeProperty("Repr", bool, default=True, storage_name="repr")
_CompareProperty = RuntimeProperty(
    "Compare", bool, default=True, storage_name="compare"
)
_HashProperty = RuntimeProperty("Hash", object, default=None, storage_name="hash")
_KwOnlyProperty = RuntimeProperty("KwOnly", bool, default=False, storage_name="kw_only")
_MetadataProperty = RuntimeProperty(
    "Metadata", object, default=None, storage_name="metadata"
)
_DataclassFacadeSpec = RuntimeRecord(
    "DataclassFacade",
    (
        _ClassIdProperty,
        _ClassNameProperty,
        _ClassOrderProperty,
        _ModuleNameProperty,
        _BasesProperty,
        _DecoratorInitProperty,
        _DecoratorReprProperty,
        _DecoratorEqProperty,
        _DecoratorOrderProperty,
        _DecoratorUnsafeHashProperty,
        _DecoratorFrozenProperty,
        _DecoratorSlotsProperty,
        _DecoratorWeakrefSlotProperty,
        _DecoratorMatchArgsProperty,
        _DecoratorKwOnlyProperty,
        _HasPostInitProperty,
        _HasKwOnlyInitFieldsProperty,
        _KwOnlyFenceOrderProperty,
        _DataclassParamsProperty,
        _SlotNamesProperty,
        _MatchArgsProperty,
    ),
)
_DataclassFieldSpec = RuntimeRecord(
    "DataclassField",
    (
        _FieldIdProperty,
        _FieldOwnerProperty,
        _FieldNameProperty,
        _FieldOrderProperty,
        _FieldKindProperty,
        _AnnotationProperty,
        _HasDefaultProperty,
        _DefaultValueProperty,
        _HasDefaultFactoryProperty,
        _DefaultFactoryProperty,
        _InitProperty,
        _ReprProperty,
        _CompareProperty,
        _HashProperty,
        _KwOnlyProperty,
        _MetadataProperty,
    ),
)


class DataclassFacade:
    __slots__ = (
        "class_id",
        "class_name",
        "class_order",
        "module_name",
        "bases",
        "decorator_init",
        "decorator_repr",
        "decorator_eq",
        "decorator_order",
        "decorator_unsafe_hash",
        "decorator_frozen",
        "decorator_slots",
        "decorator_weakref_slot",
        "decorator_match_args",
        "decorator_kw_only",
        "has_post_init",
        "has_kw_only_init_fields",
        "kw_only_fence_order",
        "dataclass_params",
        "slot_names",
        "match_args",
    )
    __dds_record_spec__ = _DataclassFacadeSpec
    class_id: str
    class_name: str
    class_order: int
    module_name: str
    bases: object
    decorator_init: bool
    decorator_repr: bool
    decorator_eq: bool
    decorator_order: bool
    decorator_unsafe_hash: bool
    decorator_frozen: bool
    decorator_slots: bool
    decorator_weakref_slot: bool
    decorator_match_args: bool
    decorator_kw_only: bool
    has_post_init: bool
    has_kw_only_init_fields: bool
    kw_only_fence_order: int
    dataclass_params: object
    slot_names: object
    match_args: object

    def __init__(
        self,
        *,
        class_id: str,
        class_name: str,
        class_order: int = 0,
        module_name: str = "__main__",
        bases: object = (),
        decorator_init: bool = True,
        decorator_repr: bool = True,
        decorator_eq: bool = True,
        decorator_order: bool = False,
        decorator_unsafe_hash: bool = False,
        decorator_frozen: bool = False,
        decorator_slots: bool = False,
        decorator_weakref_slot: bool = False,
        decorator_match_args: bool = True,
        decorator_kw_only: bool = False,
        has_post_init: bool = False,
        has_kw_only_init_fields: bool = False,
        kw_only_fence_order: int = 0,
        dataclass_params: object = None,
        slot_names: object = (),
        match_args: object = ()
    ):
        if not isinstance(class_id, str):
            raise TypeError("ClassId must be str, got " + type(class_id).__name__)
        object.__setattr__(self, "class_id", class_id)
        if not isinstance(class_name, str):
            raise TypeError("ClassName must be str, got " + type(class_name).__name__)
        object.__setattr__(self, "class_name", class_name)
        if not isinstance(class_order, int):
            raise TypeError("ClassOrder must be int, got " + type(class_order).__name__)
        object.__setattr__(self, "class_order", class_order)
        if not isinstance(module_name, str):
            raise TypeError("ModuleName must be str, got " + type(module_name).__name__)
        object.__setattr__(self, "module_name", module_name)
        object.__setattr__(self, "bases", bases)
        if not isinstance(decorator_init, bool):
            raise TypeError(
                "DecoratorInit must be bool, got " + type(decorator_init).__name__
            )
        object.__setattr__(self, "decorator_init", decorator_init)
        if not isinstance(decorator_repr, bool):
            raise TypeError(
                "DecoratorRepr must be bool, got " + type(decorator_repr).__name__
            )
        object.__setattr__(self, "decorator_repr", decorator_repr)
        if not isinstance(decorator_eq, bool):
            raise TypeError(
                "DecoratorEq must be bool, got " + type(decorator_eq).__name__
            )
        object.__setattr__(self, "decorator_eq", decorator_eq)
        if not isinstance(decorator_order, bool):
            raise TypeError(
                "DecoratorOrder must be bool, got " + type(decorator_order).__name__
            )
        object.__setattr__(self, "decorator_order", decorator_order)
        if not isinstance(decorator_unsafe_hash, bool):
            raise TypeError(
                "DecoratorUnsafeHash must be bool, got "
                + type(decorator_unsafe_hash).__name__
            )
        object.__setattr__(self, "decorator_unsafe_hash", decorator_unsafe_hash)
        if not isinstance(decorator_frozen, bool):
            raise TypeError(
                "DecoratorFrozen must be bool, got " + type(decorator_frozen).__name__
            )
        object.__setattr__(self, "decorator_frozen", decorator_frozen)
        if not isinstance(decorator_slots, bool):
            raise TypeError(
                "DecoratorSlots must be bool, got " + type(decorator_slots).__name__
            )
        object.__setattr__(self, "decorator_slots", decorator_slots)
        if not isinstance(decorator_weakref_slot, bool):
            raise TypeError(
                "DecoratorWeakrefSlot must be bool, got "
                + type(decorator_weakref_slot).__name__
            )
        object.__setattr__(self, "decorator_weakref_slot", decorator_weakref_slot)
        if not isinstance(decorator_match_args, bool):
            raise TypeError(
                "DecoratorMatchArgs must be bool, got "
                + type(decorator_match_args).__name__
            )
        object.__setattr__(self, "decorator_match_args", decorator_match_args)
        if not isinstance(decorator_kw_only, bool):
            raise TypeError(
                "DecoratorKwOnly must be bool, got " + type(decorator_kw_only).__name__
            )
        object.__setattr__(self, "decorator_kw_only", decorator_kw_only)
        if not isinstance(has_post_init, bool):
            raise TypeError(
                "HasPostInit must be bool, got " + type(has_post_init).__name__
            )
        object.__setattr__(self, "has_post_init", has_post_init)
        if not isinstance(has_kw_only_init_fields, bool):
            raise TypeError(
                "HasKwOnlyInitFields must be bool, got "
                + type(has_kw_only_init_fields).__name__
            )
        object.__setattr__(self, "has_kw_only_init_fields", has_kw_only_init_fields)
        if not isinstance(kw_only_fence_order, int):
            raise TypeError(
                "KwOnlyFenceOrder must be int, got "
                + type(kw_only_fence_order).__name__
            )
        object.__setattr__(self, "kw_only_fence_order", kw_only_fence_order)
        object.__setattr__(self, "dataclass_params", dataclass_params)
        object.__setattr__(self, "slot_names", slot_names)
        object.__setattr__(self, "match_args", match_args)

    def __setattr__(self, name, value):
        if name in (
            "class_id",
            "class_name",
            "class_order",
            "module_name",
            "bases",
            "decorator_init",
            "decorator_repr",
            "decorator_eq",
            "decorator_order",
            "decorator_unsafe_hash",
            "decorator_frozen",
            "decorator_slots",
            "decorator_weakref_slot",
            "decorator_match_args",
            "decorator_kw_only",
            "has_post_init",
            "has_kw_only_init_fields",
            "kw_only_fence_order",
            "dataclass_params",
            "slot_names",
            "match_args",
        ):
            raise AttributeError("DataclassFacade records are immutable")
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append("class_id=" + repr(self.class_id))
        pieces.append("class_name=" + repr(self.class_name))
        pieces.append("class_order=" + repr(self.class_order))
        pieces.append("module_name=" + repr(self.module_name))
        pieces.append("bases=" + repr(self.bases))
        pieces.append("decorator_init=" + repr(self.decorator_init))
        pieces.append("decorator_repr=" + repr(self.decorator_repr))
        pieces.append("decorator_eq=" + repr(self.decorator_eq))
        pieces.append("decorator_order=" + repr(self.decorator_order))
        pieces.append("decorator_unsafe_hash=" + repr(self.decorator_unsafe_hash))
        pieces.append("decorator_frozen=" + repr(self.decorator_frozen))
        pieces.append("decorator_slots=" + repr(self.decorator_slots))
        pieces.append("decorator_weakref_slot=" + repr(self.decorator_weakref_slot))
        pieces.append("decorator_match_args=" + repr(self.decorator_match_args))
        pieces.append("decorator_kw_only=" + repr(self.decorator_kw_only))
        pieces.append("has_post_init=" + repr(self.has_post_init))
        pieces.append("has_kw_only_init_fields=" + repr(self.has_kw_only_init_fields))
        pieces.append("kw_only_fence_order=" + repr(self.kw_only_fence_order))
        pieces.append("dataclass_params=" + repr(self.dataclass_params))
        pieces.append("slot_names=" + repr(self.slot_names))
        pieces.append("match_args=" + repr(self.match_args))
        return "DataclassFacade" + "(" + ", ".join(pieces) + ")"


_DataclassFacadeSpec.bind_record_class(DataclassFacade)


class DataclassField:
    __slots__ = (
        "field_id",
        "field_owner",
        "field_name",
        "field_order",
        "field_kind",
        "annotation",
        "has_default",
        "default_value",
        "has_default_factory",
        "default_factory",
        "init",
        "repr",
        "compare",
        "hash",
        "kw_only",
        "metadata",
    )
    __dds_record_spec__ = _DataclassFieldSpec
    field_id: str
    field_owner: str
    field_name: str
    field_order: int
    field_kind: str
    annotation: object
    has_default: bool
    default_value: object
    has_default_factory: bool
    default_factory: object
    init: bool
    repr: bool
    compare: bool
    hash: object
    kw_only: bool
    metadata: object

    def __init__(
        self,
        *,
        field_id: str,
        field_owner: str,
        field_name: str,
        field_order: int,
        field_kind: str = "field",
        annotation: object = object,
        has_default: bool = False,
        default_value: object = None,
        has_default_factory: bool = False,
        default_factory: object = None,
        init: bool = True,
        repr: bool = True,
        compare: bool = True,
        hash: object = None,
        kw_only: bool = False,
        metadata: object = None
    ):
        if not isinstance(field_id, str):
            raise TypeError("FieldId must be str, got " + type(field_id).__name__)
        object.__setattr__(self, "field_id", field_id)
        if not isinstance(field_owner, str):
            raise TypeError("FieldOwner must be str, got " + type(field_owner).__name__)
        object.__setattr__(self, "field_owner", field_owner)
        if not isinstance(field_name, str):
            raise TypeError("FieldName must be str, got " + type(field_name).__name__)
        object.__setattr__(self, "field_name", field_name)
        if not isinstance(field_order, int):
            raise TypeError("FieldOrder must be int, got " + type(field_order).__name__)
        object.__setattr__(self, "field_order", field_order)
        if not isinstance(field_kind, str):
            raise TypeError("FieldKind must be str, got " + type(field_kind).__name__)
        object.__setattr__(self, "field_kind", field_kind)
        object.__setattr__(self, "annotation", annotation)
        if not isinstance(has_default, bool):
            raise TypeError(
                "HasDefault must be bool, got " + type(has_default).__name__
            )
        object.__setattr__(self, "has_default", has_default)
        object.__setattr__(self, "default_value", default_value)
        if not isinstance(has_default_factory, bool):
            raise TypeError(
                "HasDefaultFactory must be bool, got "
                + type(has_default_factory).__name__
            )
        object.__setattr__(self, "has_default_factory", has_default_factory)
        object.__setattr__(self, "default_factory", default_factory)
        if not isinstance(init, bool):
            raise TypeError("Init must be bool, got " + type(init).__name__)
        object.__setattr__(self, "init", init)
        if not isinstance(repr, bool):
            raise TypeError("Repr must be bool, got " + type(repr).__name__)
        object.__setattr__(self, "repr", repr)
        if not isinstance(compare, bool):
            raise TypeError("Compare must be bool, got " + type(compare).__name__)
        object.__setattr__(self, "compare", compare)
        object.__setattr__(self, "hash", hash)
        if not isinstance(kw_only, bool):
            raise TypeError("KwOnly must be bool, got " + type(kw_only).__name__)
        object.__setattr__(self, "kw_only", kw_only)
        object.__setattr__(self, "metadata", metadata)

    def __setattr__(self, name, value):
        if name in (
            "field_id",
            "field_owner",
            "field_name",
            "field_order",
            "field_kind",
            "annotation",
            "has_default",
            "default_value",
            "has_default_factory",
            "default_factory",
            "init",
            "repr",
            "compare",
            "hash",
            "kw_only",
            "metadata",
        ):
            raise AttributeError("DataclassField records are immutable")
        object.__setattr__(self, name, value)

    def __repr__(self):
        pieces = []
        pieces.append("field_id=" + repr(self.field_id))
        pieces.append("field_owner=" + repr(self.field_owner))
        pieces.append("field_name=" + repr(self.field_name))
        pieces.append("field_order=" + repr(self.field_order))
        pieces.append("field_kind=" + repr(self.field_kind))
        pieces.append("annotation=" + repr(self.annotation))
        pieces.append("has_default=" + repr(self.has_default))
        pieces.append("default_value=" + repr(self.default_value))
        pieces.append("has_default_factory=" + repr(self.has_default_factory))
        pieces.append("default_factory=" + repr(self.default_factory))
        pieces.append("init=" + repr(self.init))
        pieces.append("repr=" + repr(self.repr))
        pieces.append("compare=" + repr(self.compare))
        pieces.append("hash=" + repr(self.hash))
        pieces.append("kw_only=" + repr(self.kw_only))
        pieces.append("metadata=" + repr(self.metadata))
        return "DataclassField" + "(" + ", ".join(pieces) + ")"


_DataclassFieldSpec.bind_record_class(DataclassField)
FacadesCollection = RuntimeCollection(
    "Facades", _DataclassFacadeSpec, allows_multiple=True, identity=_ClassIdProperty
)
FieldsCollection = RuntimeCollection(
    "Fields", _DataclassFieldSpec, allows_multiple=True, identity=_FieldIdProperty
)
_RUNTIME_SPEC = RuntimeContainerSpec(
    collections=(FacadesCollection, FieldsCollection),
    computed_collections=(),
    ports=(),
    port_index=None,
)


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


from types import SimpleNamespace as _YidlSimpleNamespace
from yidl.generation.assembly_plan import (
    AndConditionSpec,
    AssemblyEdgeSpec,
    AssemblyInputSpec,
    AssemblySpec,
    BindingSpec,
    ComposableProductionSpec,
    ContributionMatcherSpec,
    ContributionRuleSpec,
    ContributionSpec,
    EdgeApplySpec,
    EqConditionSpec,
    InlineApplySpec,
    LiteralValueRef,
    PathSegmentSpec,
    PathSpec,
    RootSpec,
    TargetPathSpec,
    TargetSpec,
    TupleValueRef,
    ValueRef,
)
from yidl.generation.assembly_runtime import run_assembly
from yidl.generation.matcher_values import (
    astichi_template,
    from_astichi_code,
    from_import,
)

ASSEMBLY_PROPERTIES = {
    "ClassId": _YidlSimpleNamespace(name="ClassId", storage_name="class_id"),
    "ClassName": _YidlSimpleNamespace(name="ClassName", storage_name="class_name"),
    "ClassOrder": _YidlSimpleNamespace(name="ClassOrder", storage_name="class_order"),
    "ModuleName": _YidlSimpleNamespace(name="ModuleName", storage_name="module_name"),
    "Bases": _YidlSimpleNamespace(name="Bases", storage_name="bases"),
    "DecoratorInit": _YidlSimpleNamespace(
        name="DecoratorInit", storage_name="decorator_init"
    ),
    "DecoratorRepr": _YidlSimpleNamespace(
        name="DecoratorRepr", storage_name="decorator_repr"
    ),
    "DecoratorEq": _YidlSimpleNamespace(
        name="DecoratorEq", storage_name="decorator_eq"
    ),
    "DecoratorOrder": _YidlSimpleNamespace(
        name="DecoratorOrder", storage_name="decorator_order"
    ),
    "DecoratorUnsafeHash": _YidlSimpleNamespace(
        name="DecoratorUnsafeHash", storage_name="decorator_unsafe_hash"
    ),
    "DecoratorFrozen": _YidlSimpleNamespace(
        name="DecoratorFrozen", storage_name="decorator_frozen"
    ),
    "DecoratorSlots": _YidlSimpleNamespace(
        name="DecoratorSlots", storage_name="decorator_slots"
    ),
    "DecoratorWeakrefSlot": _YidlSimpleNamespace(
        name="DecoratorWeakrefSlot", storage_name="decorator_weakref_slot"
    ),
    "DecoratorMatchArgs": _YidlSimpleNamespace(
        name="DecoratorMatchArgs", storage_name="decorator_match_args"
    ),
    "DecoratorKwOnly": _YidlSimpleNamespace(
        name="DecoratorKwOnly", storage_name="decorator_kw_only"
    ),
    "HasPostInit": _YidlSimpleNamespace(
        name="HasPostInit", storage_name="has_post_init"
    ),
    "HasKwOnlyInitFields": _YidlSimpleNamespace(
        name="HasKwOnlyInitFields", storage_name="has_kw_only_init_fields"
    ),
    "KwOnlyFenceOrder": _YidlSimpleNamespace(
        name="KwOnlyFenceOrder", storage_name="kw_only_fence_order"
    ),
    "DataclassParams": _YidlSimpleNamespace(
        name="DataclassParams", storage_name="dataclass_params"
    ),
    "SlotNames": _YidlSimpleNamespace(name="SlotNames", storage_name="slot_names"),
    "MatchArgs": _YidlSimpleNamespace(name="MatchArgs", storage_name="match_args"),
    "FieldId": _YidlSimpleNamespace(name="FieldId", storage_name="field_id"),
    "FieldOwner": _YidlSimpleNamespace(name="FieldOwner", storage_name="field_owner"),
    "FieldName": _YidlSimpleNamespace(name="FieldName", storage_name="field_name"),
    "FieldOrder": _YidlSimpleNamespace(name="FieldOrder", storage_name="field_order"),
    "FieldKind": _YidlSimpleNamespace(name="FieldKind", storage_name="field_kind"),
    "Annotation": _YidlSimpleNamespace(name="Annotation", storage_name="annotation"),
    "HasDefault": _YidlSimpleNamespace(name="HasDefault", storage_name="has_default"),
    "DefaultValue": _YidlSimpleNamespace(
        name="DefaultValue", storage_name="default_value"
    ),
    "HasDefaultFactory": _YidlSimpleNamespace(
        name="HasDefaultFactory", storage_name="has_default_factory"
    ),
    "DefaultFactory": _YidlSimpleNamespace(
        name="DefaultFactory", storage_name="default_factory"
    ),
    "Init": _YidlSimpleNamespace(name="Init", storage_name="init"),
    "Repr": _YidlSimpleNamespace(name="Repr", storage_name="repr"),
    "Compare": _YidlSimpleNamespace(name="Compare", storage_name="compare"),
    "Hash": _YidlSimpleNamespace(name="Hash", storage_name="hash"),
    "KwOnly": _YidlSimpleNamespace(name="KwOnly", storage_name="kw_only"),
    "Metadata": _YidlSimpleNamespace(name="Metadata", storage_name="metadata"),
}
ASSEMBLY_RESOURCES = {
    "ModuleRoot": from_astichi_code(
        "from __future__ import annotations\n\n_MISSING = object()\n_HAS_DEFAULT_FACTORY = object()\n\n\nclass FrozenInstanceError(AttributeError):\n    pass\n\n\ndef _field_info(**kw):\n    return kw\n\n\nastichi_hole(module_body)",
        file_name="tests/data/yidl/dataclasses_example.yidl",
        line_number=115,
    ),
    "ClassShell": astichi_template(
        from_astichi_code(
            "class class_name__astichi_arg__:\n    __module__ = astichi_bind_external(module_name)\n    __dataclass_params__ = astichi_bind_external(dataclass_params)\n    __dataclass_fields__ = {**astichi_hole(field_info_entries)}\n    __annotations__ = {**astichi_hole(annotation_entries)}\n\n    astichi_hole(slots_decl)\n    astichi_hole(field_defaults)\n    astichi_hole(match_args_decl)\n    astichi_hole(init_method)\n    astichi_hole(repr_method)\n    astichi_hole(eq_method)\n    astichi_hole(order_methods)\n    astichi_hole(hash_method)\n    astichi_hole(frozen_methods)",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=133,
        )
    ),
    "EmptyStatement": astichi_template(
        from_astichi_code(
            "pass",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=150,
            offset=40,
        )
    ),
    "SlotsDecl": astichi_template(
        from_astichi_code(
            "__slots__ = astichi_bind_external(slot_names)",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=171,
        )
    ),
    "MatchArgsDecl": astichi_template(
        from_astichi_code(
            "__match_args__ = astichi_bind_external(match_args)",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=175,
        )
    ),
    "AnnotationEntry": astichi_template(
        from_astichi_code(
            "{astichi_bind_external(field_name): astichi_bind_external(annotation)}",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=179,
        )
    ),
    "FieldInfoEntry": astichi_template(
        from_astichi_code(
            "{\n    astichi_bind_external(field_name): _field_info(\n        name=astichi_bind_external(field_name),\n        type=astichi_bind_external(annotation),\n        default=astichi_bind_external(default_value),\n        default_factory=astichi_bind_external(default_factory),\n        init=astichi_bind_external(init),\n        repr=astichi_bind_external(repr),\n        compare=astichi_bind_external(compare),\n        hash=astichi_bind_external(hash),\n        kw_only=astichi_bind_external(kw_only),\n        metadata=astichi_bind_external(metadata),\n        kind=astichi_bind_external(kind),\n    )\n}",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=183,
            keep_names=("_field_info",),
        )
    ),
    "DefaultValueAssignment": astichi_template(
        from_astichi_code(
            "field_name__astichi_arg__ = astichi_bind_external(default_value)",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=203,
        )
    ),
    "InitMethodTemplate": astichi_template(
        from_astichi_code(
            "def __init__(self, params__astichi_param_hole__):\n    astichi_hole(default_factory_guards)\n    astichi_hole(init_assignments)\n    astichi_hole(post_init_call)",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=321,
        )
    ),
    "RequiredParam": astichi_template(
        from_astichi_code(
            "def astichi_params(field_name__astichi_arg__: astichi_bind_external(annotation)):\n    pass",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=328,
        )
    ),
    "KwOnlyFence": astichi_template(
        from_astichi_code(
            "def astichi_params():\n    pass",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=333,
        )
    ),
    "DefaultParam": astichi_template(
        from_astichi_code(
            "def astichi_params(\n    field_name__astichi_arg__: astichi_bind_external(annotation) = astichi_bind_external(default_value)\n):\n    pass",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=338,
        )
    ),
    "DefaultFactoryParam": astichi_template(
        from_astichi_code(
            "def astichi_params(\n    field_name__astichi_arg__: astichi_bind_external(annotation) = _HAS_DEFAULT_FACTORY\n):\n    pass",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=345,
        )
    ),
    "PlainInitAssign": astichi_template(
        from_astichi_code(
            "setattr(\n    astichi_pass(self, outer_bind=True),\n    astichi_bind_external(field_name_text),\n    astichi_pass(field_name__astichi_arg__, outer_bind=True),\n)",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=352,
        )
    ),
    "FrozenInitAssign": astichi_template(
        from_astichi_code(
            "object.__setattr__(\n    astichi_pass(self, outer_bind=True),\n    astichi_bind_external(field_name_text),\n    astichi_pass(field_name__astichi_arg__, outer_bind=True),\n)",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=360,
        )
    ),
    "DefaultFactoryGuard": astichi_template(
        from_astichi_code(
            "if field_name__astichi_arg__ is _HAS_DEFAULT_FACTORY:\n    field_name__astichi_arg__ = astichi_bind_external(default_factory)()",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=368,
        )
    ),
    "PostInitCall": astichi_template(
        from_astichi_code(
            "self.__post_init__(astichi_hole(post_init_args))",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=373,
        )
    ),
    "PostInitArg": astichi_template(
        from_astichi_code(
            "astichi_funcargs(field_name__astichi_arg__)",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=377,
        )
    ),
    "ReprMethodTemplate": astichi_template(
        from_astichi_code(
            'def __repr__(self):\n    return astichi_bind_external(class_name) + "(" + ", ".join((*astichi_hole(repr_parts),)) + ")"',
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=597,
        )
    ),
    "ReprPart": astichi_template(
        from_astichi_code(
            'astichi_bind_external(field_name_text) + "=" + repr(getattr(self, astichi_bind_external(field_name_text)))',
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=602,
        )
    ),
    "EqMethodTemplate": astichi_template(
        from_astichi_code(
            "def __eq__(self, other):\n    if other.__class__ is self.__class__:\n        return (*astichi_hole(self_compare_values),) == (*astichi_hole(other_compare_values),)\n    return NotImplemented",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=606,
        )
    ),
    "SelfCompareValue": astichi_template(
        from_astichi_code(
            "getattr(self, astichi_bind_external(field_name_text))",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=613,
        )
    ),
    "OtherCompareValue": astichi_template(
        from_astichi_code(
            "getattr(other, astichi_bind_external(field_name_text))",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=617,
        )
    ),
    "LtMethodTemplate": astichi_template(
        from_astichi_code(
            "def __lt__(self, other):\n    if other.__class__ is self.__class__:\n        return (*astichi_hole(self_order_values),) < (*astichi_hole(other_order_values),)\n    return NotImplemented",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=621,
        )
    ),
    "LeMethodTemplate": astichi_template(
        from_astichi_code(
            "def __le__(self, other):\n    if other.__class__ is self.__class__:\n        return (*astichi_hole(self_order_values),) <= (*astichi_hole(other_order_values),)\n    return NotImplemented",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=628,
        )
    ),
    "GtMethodTemplate": astichi_template(
        from_astichi_code(
            "def __gt__(self, other):\n    if other.__class__ is self.__class__:\n        return (*astichi_hole(self_order_values),) > (*astichi_hole(other_order_values),)\n    return NotImplemented",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=635,
        )
    ),
    "GeMethodTemplate": astichi_template(
        from_astichi_code(
            "def __ge__(self, other):\n    if other.__class__ is self.__class__:\n        return (*astichi_hole(self_order_values),) >= (*astichi_hole(other_order_values),)\n    return NotImplemented",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=642,
        )
    ),
    "HashMethodTemplate": astichi_template(
        from_astichi_code(
            "def __hash__(self):\n    return hash((*astichi_hole(hash_values),))",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=649,
        )
    ),
    "HashNone": astichi_template(
        from_astichi_code(
            "__hash__ = None",
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=654,
        )
    ),
    "FrozenSetattr": astichi_template(
        from_astichi_code(
            'def __setattr__(self, name, value):\n    raise FrozenInstanceError(f"cannot assign to field {name!r}")',
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=1065,
        )
    ),
    "FrozenDelattr": astichi_template(
        from_astichi_code(
            'def __delattr__(self, name):\n    raise FrozenInstanceError(f"cannot delete field {name!r}")',
            file_name="tests/data/yidl/dataclasses_example.yidl",
            line_number=1070,
        )
    ),
}
ASSEMBLY_CONTRIBUTIONS = {
    "ClassDefinition": ContributionSpec(
        name="ClassDefinition",
        source_name="ClassProduction",
        source_kind="production",
        build_name="ClassDef",
        index=ValueRef("ClassOrder"),
        order=ValueRef("ClassOrder"),
        target=TargetSpec(
            name="module_body",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="Root", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "SlotsDeclContribution": ContributionSpec(
        name="SlotsDeclContribution",
        source_name="SlotsDecl",
        source_kind="resource",
        build_name="SlotsDeclContribution",
        index=None,
        order=None,
        target=TargetSpec(
            name="slots_decl",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="slot_names", value=ValueRef("SlotNames")
            ),
        ),
    ),
    "EmptySlotsDeclContribution": ContributionSpec(
        name="EmptySlotsDeclContribution",
        source_name="EmptyStatement",
        source_kind="resource",
        build_name="EmptySlotsDeclContribution",
        index=None,
        order=None,
        target=TargetSpec(
            name="slots_decl",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "MatchArgsContribution": ContributionSpec(
        name="MatchArgsContribution",
        source_name="MatchArgsDecl",
        source_kind="resource",
        build_name="MatchArgsContribution",
        index=None,
        order=None,
        target=TargetSpec(
            name="match_args_decl",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="match_args", value=ValueRef("MatchArgs")
            ),
        ),
    ),
    "EmptyMatchArgsContribution": ContributionSpec(
        name="EmptyMatchArgsContribution",
        source_name="EmptyStatement",
        source_kind="resource",
        build_name="EmptyMatchArgsContribution",
        index=None,
        order=None,
        target=TargetSpec(
            name="match_args_decl",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "AnnotationContribution": ContributionSpec(
        name="AnnotationContribution",
        source_name="AnnotationEntry",
        source_kind="resource",
        build_name="AnnotationEntry",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="annotation_entries",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="field_name", value=ValueRef("FieldName")
            ),
            BindingSpec(
                kind="external", name="annotation", value=ValueRef("Annotation")
            ),
        ),
    ),
    "FieldInfoContribution": ContributionSpec(
        name="FieldInfoContribution",
        source_name="FieldInfoEntry",
        source_kind="resource",
        build_name="FieldInfoEntry",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="field_info_entries",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="field_name", value=ValueRef("FieldName")
            ),
            BindingSpec(
                kind="external", name="annotation", value=ValueRef("Annotation")
            ),
            BindingSpec(
                kind="external", name="default_value", value=ValueRef("DefaultValue")
            ),
            BindingSpec(
                kind="external",
                name="default_factory",
                value=ValueRef("DefaultFactory"),
            ),
            BindingSpec(kind="external", name="init", value=ValueRef("Init")),
            BindingSpec(kind="external", name="repr", value=ValueRef("Repr")),
            BindingSpec(kind="external", name="compare", value=ValueRef("Compare")),
            BindingSpec(kind="external", name="hash", value=ValueRef("Hash")),
            BindingSpec(kind="external", name="kw_only", value=ValueRef("KwOnly")),
            BindingSpec(kind="external", name="metadata", value=ValueRef("Metadata")),
            BindingSpec(kind="external", name="kind", value=ValueRef("FieldKind")),
        ),
    ),
    "DefaultValueContribution": ContributionSpec(
        name="DefaultValueContribution",
        source_name="DefaultValueAssignment",
        source_kind="resource",
        build_name="FieldDefault",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="field_defaults",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(kind="ident", name="field_name", value=ValueRef("FieldName")),
            BindingSpec(
                kind="external", name="default_value", value=ValueRef("DefaultValue")
            ),
        ),
    ),
    "EmptyDefaultValueContribution": ContributionSpec(
        name="EmptyDefaultValueContribution",
        source_name="EmptyStatement",
        source_kind="resource",
        build_name="EmptyFieldDefault",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="field_defaults",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "InitMethodContribution": ContributionSpec(
        name="InitMethodContribution",
        source_name="InitMethodProduction",
        source_kind="production",
        build_name="InitMethod",
        index=None,
        order=None,
        target=TargetSpec(
            name="init_method",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "RequiredParamContribution": ContributionSpec(
        name="RequiredParamContribution",
        source_name="RequiredParam",
        source_kind="resource",
        build_name="InitParam",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="params",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="InitMethod", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(kind="ident", name="field_name", value=ValueRef("FieldName")),
            BindingSpec(
                kind="external", name="annotation", value=ValueRef("Annotation")
            ),
        ),
    ),
    "KwOnlyFenceContribution": ContributionSpec(
        name="KwOnlyFenceContribution",
        source_name="KwOnlyFence",
        source_kind="resource",
        build_name="InitParam",
        index=ValueRef("KwOnlyFenceOrder"),
        order=ValueRef("KwOnlyFenceOrder"),
        target=TargetSpec(
            name="params",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="InitMethod", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "DefaultParamContribution": ContributionSpec(
        name="DefaultParamContribution",
        source_name="DefaultParam",
        source_kind="resource",
        build_name="InitParam",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="params",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="InitMethod", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(kind="ident", name="field_name", value=ValueRef("FieldName")),
            BindingSpec(
                kind="external", name="annotation", value=ValueRef("Annotation")
            ),
            BindingSpec(
                kind="external", name="default_value", value=ValueRef("DefaultValue")
            ),
        ),
    ),
    "DefaultFactoryParamContribution": ContributionSpec(
        name="DefaultFactoryParamContribution",
        source_name="DefaultFactoryParam",
        source_kind="resource",
        build_name="InitParam",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="params",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="InitMethod", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(kind="ident", name="field_name", value=ValueRef("FieldName")),
            BindingSpec(
                kind="external", name="annotation", value=ValueRef("Annotation")
            ),
        ),
    ),
    "PlainInitAssignContribution": ContributionSpec(
        name="PlainInitAssignContribution",
        source_name="PlainInitAssign",
        source_kind="resource",
        build_name="InitAssign",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="init_assignments",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="InitMethod", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(kind="ident", name="field_name", value=ValueRef("FieldName")),
            BindingSpec(
                kind="external", name="field_name_text", value=ValueRef("FieldName")
            ),
        ),
    ),
    "FrozenInitAssignContribution": ContributionSpec(
        name="FrozenInitAssignContribution",
        source_name="FrozenInitAssign",
        source_kind="resource",
        build_name="InitAssign",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="init_assignments",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="InitMethod", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="field_name_text", value=ValueRef("FieldName")
            ),
            BindingSpec(kind="ident", name="field_name", value=ValueRef("FieldName")),
        ),
    ),
    "DefaultFactoryGuardContribution": ContributionSpec(
        name="DefaultFactoryGuardContribution",
        source_name="DefaultFactoryGuard",
        source_kind="resource",
        build_name="DefaultFactoryGuard",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="default_factory_guards",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="InitMethod", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(kind="ident", name="field_name", value=ValueRef("FieldName")),
            BindingSpec(
                kind="external",
                name="default_factory",
                value=ValueRef("DefaultFactory"),
            ),
        ),
    ),
    "EmptyDefaultFactoryGuardContribution": ContributionSpec(
        name="EmptyDefaultFactoryGuardContribution",
        source_name="EmptyStatement",
        source_kind="resource",
        build_name="EmptyDefaultFactoryGuard",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="default_factory_guards",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="InitMethod", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "PostInitCallContribution": ContributionSpec(
        name="PostInitCallContribution",
        source_name="PostInitCall",
        source_kind="resource",
        build_name="PostInitCall",
        index=None,
        order=None,
        target=TargetSpec(
            name="post_init_call",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="InitMethod", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "EmptyPostInitContribution": ContributionSpec(
        name="EmptyPostInitContribution",
        source_name="EmptyStatement",
        source_kind="resource",
        build_name="EmptyPostInitContribution",
        index=None,
        order=None,
        target=TargetSpec(
            name="post_init_call",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="InitMethod", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "PostInitArgContribution": ContributionSpec(
        name="PostInitArgContribution",
        source_name="PostInitArg",
        source_kind="resource",
        build_name="PostInitArg",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="post_init_args",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="InitMethod", indexes=()),
                            PathSegmentSpec(
                                kind="name", name="PostInitCall", indexes=()
                            ),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(kind="ident", name="field_name", value=ValueRef("FieldName")),
        ),
    ),
    "ReprMethodContribution": ContributionSpec(
        name="ReprMethodContribution",
        source_name="ReprMethodProduction",
        source_kind="production",
        build_name="ReprMethod",
        index=None,
        order=None,
        target=TargetSpec(
            name="repr_method",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "EmptyReprMethodContribution": ContributionSpec(
        name="EmptyReprMethodContribution",
        source_name="EmptyStatement",
        source_kind="resource",
        build_name="EmptyReprMethodContribution",
        index=None,
        order=None,
        target=TargetSpec(
            name="repr_method",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "ReprPartContribution": ContributionSpec(
        name="ReprPartContribution",
        source_name="ReprPart",
        source_kind="resource",
        build_name="ReprPart",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="repr_parts",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ReprMethod", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="field_name_text", value=ValueRef("FieldName")
            ),
        ),
    ),
    "EqMethodContribution": ContributionSpec(
        name="EqMethodContribution",
        source_name="EqMethodProduction",
        source_kind="production",
        build_name="EqMethod",
        index=None,
        order=None,
        target=TargetSpec(
            name="eq_method",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "EmptyEqMethodContribution": ContributionSpec(
        name="EmptyEqMethodContribution",
        source_name="EmptyStatement",
        source_kind="resource",
        build_name="EmptyEqMethodContribution",
        index=None,
        order=None,
        target=TargetSpec(
            name="eq_method",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "SelfCompareContribution": ContributionSpec(
        name="SelfCompareContribution",
        source_name="SelfCompareValue",
        source_kind="resource",
        build_name="SelfCompareValue",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="self_compare_values",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="EqMethod", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="field_name_text", value=ValueRef("FieldName")
            ),
        ),
    ),
    "OtherCompareContribution": ContributionSpec(
        name="OtherCompareContribution",
        source_name="OtherCompareValue",
        source_kind="resource",
        build_name="OtherCompareValue",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="other_compare_values",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="EqMethod", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="field_name_text", value=ValueRef("FieldName")
            ),
        ),
    ),
    "LtMethodContribution": ContributionSpec(
        name="LtMethodContribution",
        source_name="LtMethodProduction",
        source_kind="production",
        build_name="LtMethod",
        index=None,
        order=None,
        target=TargetSpec(
            name="order_methods",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "EmptyLtMethodContribution": ContributionSpec(
        name="EmptyLtMethodContribution",
        source_name="EmptyStatement",
        source_kind="resource",
        build_name="EmptyLtMethodContribution",
        index=None,
        order=None,
        target=TargetSpec(
            name="order_methods",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "LeMethodContribution": ContributionSpec(
        name="LeMethodContribution",
        source_name="LeMethodProduction",
        source_kind="production",
        build_name="LeMethod",
        index=None,
        order=None,
        target=TargetSpec(
            name="order_methods",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "EmptyLeMethodContribution": ContributionSpec(
        name="EmptyLeMethodContribution",
        source_name="EmptyStatement",
        source_kind="resource",
        build_name="EmptyLeMethodContribution",
        index=None,
        order=None,
        target=TargetSpec(
            name="order_methods",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "GtMethodContribution": ContributionSpec(
        name="GtMethodContribution",
        source_name="GtMethodProduction",
        source_kind="production",
        build_name="GtMethod",
        index=None,
        order=None,
        target=TargetSpec(
            name="order_methods",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "EmptyGtMethodContribution": ContributionSpec(
        name="EmptyGtMethodContribution",
        source_name="EmptyStatement",
        source_kind="resource",
        build_name="EmptyGtMethodContribution",
        index=None,
        order=None,
        target=TargetSpec(
            name="order_methods",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "GeMethodContribution": ContributionSpec(
        name="GeMethodContribution",
        source_name="GeMethodProduction",
        source_kind="production",
        build_name="GeMethod",
        index=None,
        order=None,
        target=TargetSpec(
            name="order_methods",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "EmptyGeMethodContribution": ContributionSpec(
        name="EmptyGeMethodContribution",
        source_name="EmptyStatement",
        source_kind="resource",
        build_name="EmptyGeMethodContribution",
        index=None,
        order=None,
        target=TargetSpec(
            name="order_methods",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "SelfLtOrderContribution": ContributionSpec(
        name="SelfLtOrderContribution",
        source_name="SelfCompareValue",
        source_kind="resource",
        build_name="SelfOrderValue",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="self_order_values",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="LtMethod", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="field_name_text", value=ValueRef("FieldName")
            ),
        ),
    ),
    "OtherLtOrderContribution": ContributionSpec(
        name="OtherLtOrderContribution",
        source_name="OtherCompareValue",
        source_kind="resource",
        build_name="OtherOrderValue",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="other_order_values",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="LtMethod", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="field_name_text", value=ValueRef("FieldName")
            ),
        ),
    ),
    "SelfLeOrderContribution": ContributionSpec(
        name="SelfLeOrderContribution",
        source_name="SelfCompareValue",
        source_kind="resource",
        build_name="SelfOrderValue",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="self_order_values",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="LeMethod", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="field_name_text", value=ValueRef("FieldName")
            ),
        ),
    ),
    "OtherLeOrderContribution": ContributionSpec(
        name="OtherLeOrderContribution",
        source_name="OtherCompareValue",
        source_kind="resource",
        build_name="OtherOrderValue",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="other_order_values",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="LeMethod", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="field_name_text", value=ValueRef("FieldName")
            ),
        ),
    ),
    "SelfGtOrderContribution": ContributionSpec(
        name="SelfGtOrderContribution",
        source_name="SelfCompareValue",
        source_kind="resource",
        build_name="SelfOrderValue",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="self_order_values",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="GtMethod", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="field_name_text", value=ValueRef("FieldName")
            ),
        ),
    ),
    "OtherGtOrderContribution": ContributionSpec(
        name="OtherGtOrderContribution",
        source_name="OtherCompareValue",
        source_kind="resource",
        build_name="OtherOrderValue",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="other_order_values",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="GtMethod", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="field_name_text", value=ValueRef("FieldName")
            ),
        ),
    ),
    "SelfGeOrderContribution": ContributionSpec(
        name="SelfGeOrderContribution",
        source_name="SelfCompareValue",
        source_kind="resource",
        build_name="SelfOrderValue",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="self_order_values",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="GeMethod", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="field_name_text", value=ValueRef("FieldName")
            ),
        ),
    ),
    "OtherGeOrderContribution": ContributionSpec(
        name="OtherGeOrderContribution",
        source_name="OtherCompareValue",
        source_kind="resource",
        build_name="OtherOrderValue",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="other_order_values",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="GeMethod", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="field_name_text", value=ValueRef("FieldName")
            ),
        ),
    ),
    "HashMethodContribution": ContributionSpec(
        name="HashMethodContribution",
        source_name="HashMethodProduction",
        source_kind="production",
        build_name="HashMethod",
        index=None,
        order=None,
        target=TargetSpec(
            name="hash_method",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "EmptyHashMethodContribution": ContributionSpec(
        name="EmptyHashMethodContribution",
        source_name="EmptyStatement",
        source_kind="resource",
        build_name="HashMethod",
        index=None,
        order=None,
        target=TargetSpec(
            name="hash_method",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "HashNoneContribution": ContributionSpec(
        name="HashNoneContribution",
        source_name="HashNone",
        source_kind="resource",
        build_name="HashMethod",
        index=None,
        order=None,
        target=TargetSpec(
            name="hash_method",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "HashValueContribution": ContributionSpec(
        name="HashValueContribution",
        source_name="SelfCompareValue",
        source_kind="resource",
        build_name="HashValue",
        index=ValueRef("FieldOrder"),
        order=ValueRef("FieldOrder"),
        target=TargetSpec(
            name="hash_values",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="HashMethod", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(
            BindingSpec(
                kind="external", name="field_name_text", value=ValueRef("FieldName")
            ),
        ),
    ),
    "FrozenSetattrContribution": ContributionSpec(
        name="FrozenSetattrContribution",
        source_name="FrozenSetattr",
        source_kind="resource",
        build_name="FrozenSetattrContribution",
        index=None,
        order=None,
        target=TargetSpec(
            name="frozen_methods",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "EmptyFrozenSetattrContribution": ContributionSpec(
        name="EmptyFrozenSetattrContribution",
        source_name="EmptyStatement",
        source_kind="resource",
        build_name="EmptyFrozenSetattrContribution",
        index=None,
        order=None,
        target=TargetSpec(
            name="frozen_methods",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "FrozenDelattrContribution": ContributionSpec(
        name="FrozenDelattrContribution",
        source_name="FrozenDelattr",
        source_kind="resource",
        build_name="FrozenDelattrContribution",
        index=None,
        order=None,
        target=TargetSpec(
            name="frozen_methods",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
    "EmptyFrozenDelattrContribution": ContributionSpec(
        name="EmptyFrozenDelattrContribution",
        source_name="EmptyStatement",
        source_kind="resource",
        build_name="EmptyFrozenDelattrContribution",
        index=None,
        order=None,
        target=TargetSpec(
            name="frozen_methods",
            paths=(
                TargetPathSpec(
                    kind="build",
                    path=PathSpec(
                        segments=(
                            PathSegmentSpec(kind="name", name="ClassDef", indexes=()),
                        )
                    ),
                ),
            ),
        ),
        bindings=(),
    ),
}
ASSEMBLY_MATCHERS = {
    "ClassDefinitionContribution": ContributionMatcherSpec(
        name="ClassDefinitionContribution",
        inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name="ClassDefinition",
        rules=(),
    ),
    "SlotsContribution": ContributionMatcherSpec(
        name="SlotsContribution",
        inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name="EmptySlotsDeclContribution",
        rules=(
            ContributionRuleSpec(
                name="slots",
                condition=EqConditionSpec(
                    left=ValueRef("DecoratorSlots"), right=LiteralValueRef(True)
                ),
                contribution_name="SlotsDeclContribution",
                weight=1.0,
            ),
        ),
    ),
    "MatchArgsContributions": ContributionMatcherSpec(
        name="MatchArgsContributions",
        inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name="EmptyMatchArgsContribution",
        rules=(
            ContributionRuleSpec(
                name="match_args",
                condition=EqConditionSpec(
                    left=ValueRef("DecoratorMatchArgs"), right=LiteralValueRef(True)
                ),
                contribution_name="MatchArgsContribution",
                weight=1.0,
            ),
        ),
    ),
    "AnnotationContributions": ContributionMatcherSpec(
        name="AnnotationContributions",
        inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name="AnnotationContribution",
        rules=(),
    ),
    "FieldInfoContributions": ContributionMatcherSpec(
        name="FieldInfoContributions",
        inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name="FieldInfoContribution",
        rules=(),
    ),
    "DefaultValueContributions": ContributionMatcherSpec(
        name="DefaultValueContributions",
        inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name="EmptyDefaultValueContribution",
        rules=(
            ContributionRuleSpec(
                name="defaulted",
                condition=EqConditionSpec(
                    left=ValueRef("HasDefault"), right=LiteralValueRef(True)
                ),
                contribution_name="DefaultValueContribution",
                weight=1.0,
            ),
        ),
    ),
    "InitMethodContributions": ContributionMatcherSpec(
        name="InitMethodContributions",
        inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="enabled",
                condition=EqConditionSpec(
                    left=ValueRef("DecoratorInit"), right=LiteralValueRef(True)
                ),
                contribution_name="InitMethodContribution",
                weight=1.0,
            ),
        ),
    ),
    "KwOnlyFenceContributions": ContributionMatcherSpec(
        name="KwOnlyFenceContributions",
        inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="enabled",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorInit"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasKwOnlyInitFields"),
                            right=LiteralValueRef(True),
                        ),
                    )
                ),
                contribution_name="KwOnlyFenceContribution",
                weight=1.0,
            ),
        ),
    ),
    "InitParamContribution": ContributionMatcherSpec(
        name="InitParamContribution",
        inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="required",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorInit"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("FieldKind"), right=LiteralValueRef("field")
                        ),
                        EqConditionSpec(
                            left=ValueRef("Init"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefault"), right=LiteralValueRef(False)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefaultFactory"),
                            right=LiteralValueRef(False),
                        ),
                    )
                ),
                contribution_name="RequiredParamContribution",
                weight=1.0,
            ),
            ContributionRuleSpec(
                name="default_value",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorInit"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("FieldKind"), right=LiteralValueRef("field")
                        ),
                        EqConditionSpec(
                            left=ValueRef("Init"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefault"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefaultFactory"),
                            right=LiteralValueRef(False),
                        ),
                    )
                ),
                contribution_name="DefaultParamContribution",
                weight=1.0,
            ),
            ContributionRuleSpec(
                name="default_factory",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorInit"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("FieldKind"), right=LiteralValueRef("field")
                        ),
                        EqConditionSpec(
                            left=ValueRef("Init"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefault"), right=LiteralValueRef(False)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefaultFactory"),
                            right=LiteralValueRef(True),
                        ),
                    )
                ),
                contribution_name="DefaultFactoryParamContribution",
                weight=1.0,
            ),
            ContributionRuleSpec(
                name="initvar_required",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorInit"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("FieldKind"), right=LiteralValueRef("initvar")
                        ),
                        EqConditionSpec(
                            left=ValueRef("Init"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefault"), right=LiteralValueRef(False)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefaultFactory"),
                            right=LiteralValueRef(False),
                        ),
                    )
                ),
                contribution_name="RequiredParamContribution",
                weight=1.0,
            ),
            ContributionRuleSpec(
                name="initvar_default",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorInit"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("FieldKind"), right=LiteralValueRef("initvar")
                        ),
                        EqConditionSpec(
                            left=ValueRef("Init"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefault"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefaultFactory"),
                            right=LiteralValueRef(False),
                        ),
                    )
                ),
                contribution_name="DefaultParamContribution",
                weight=1.0,
            ),
        ),
    ),
    "DefaultFactoryGuardContributions": ContributionMatcherSpec(
        name="DefaultFactoryGuardContributions",
        inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name="EmptyDefaultFactoryGuardContribution",
        rules=(
            ContributionRuleSpec(
                name="default_factory",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorInit"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("FieldKind"), right=LiteralValueRef("field")
                        ),
                        EqConditionSpec(
                            left=ValueRef("Init"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasDefaultFactory"),
                            right=LiteralValueRef(True),
                        ),
                    )
                ),
                contribution_name="DefaultFactoryGuardContribution",
                weight=1.0,
            ),
        ),
    ),
    "InitAssignContribution": ContributionMatcherSpec(
        name="InitAssignContribution",
        inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="mutable",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorInit"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("FieldKind"), right=LiteralValueRef("field")
                        ),
                        EqConditionSpec(
                            left=ValueRef("Init"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("DecoratorFrozen"),
                            right=LiteralValueRef(False),
                        ),
                    )
                ),
                contribution_name="PlainInitAssignContribution",
                weight=1.0,
            ),
            ContributionRuleSpec(
                name="frozen",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorInit"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("FieldKind"), right=LiteralValueRef("field")
                        ),
                        EqConditionSpec(
                            left=ValueRef("Init"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("DecoratorFrozen"),
                            right=LiteralValueRef(True),
                        ),
                    )
                ),
                contribution_name="FrozenInitAssignContribution",
                weight=1.0,
            ),
        ),
    ),
    "PostInitContribution": ContributionMatcherSpec(
        name="PostInitContribution",
        inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name="EmptyPostInitContribution",
        rules=(
            ContributionRuleSpec(
                name="post_init",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorInit"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasPostInit"), right=LiteralValueRef(True)
                        ),
                    )
                ),
                contribution_name="PostInitCallContribution",
                weight=1.0,
            ),
        ),
    ),
    "PostInitArgContributions": ContributionMatcherSpec(
        name="PostInitArgContributions",
        inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="initvar",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorInit"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("HasPostInit"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("FieldKind"), right=LiteralValueRef("initvar")
                        ),
                    )
                ),
                contribution_name="PostInitArgContribution",
                weight=1.0,
            ),
        ),
    ),
    "ReprMethodContributions": ContributionMatcherSpec(
        name="ReprMethodContributions",
        inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name="EmptyReprMethodContribution",
        rules=(
            ContributionRuleSpec(
                name="enabled",
                condition=EqConditionSpec(
                    left=ValueRef("DecoratorRepr"), right=LiteralValueRef(True)
                ),
                contribution_name="ReprMethodContribution",
                weight=1.0,
            ),
        ),
    ),
    "ReprPartContributions": ContributionMatcherSpec(
        name="ReprPartContributions",
        inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="repr_field",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorRepr"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("FieldKind"), right=LiteralValueRef("field")
                        ),
                        EqConditionSpec(
                            left=ValueRef("Repr"), right=LiteralValueRef(True)
                        ),
                    )
                ),
                contribution_name="ReprPartContribution",
                weight=1.0,
            ),
        ),
    ),
    "EqMethodContributions": ContributionMatcherSpec(
        name="EqMethodContributions",
        inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name="EmptyEqMethodContribution",
        rules=(
            ContributionRuleSpec(
                name="enabled",
                condition=EqConditionSpec(
                    left=ValueRef("DecoratorEq"), right=LiteralValueRef(True)
                ),
                contribution_name="EqMethodContribution",
                weight=1.0,
            ),
        ),
    ),
    "SelfCompareValueContributions": ContributionMatcherSpec(
        name="SelfCompareValueContributions",
        inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="self_value",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorEq"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("FieldKind"), right=LiteralValueRef("field")
                        ),
                        EqConditionSpec(
                            left=ValueRef("Compare"), right=LiteralValueRef(True)
                        ),
                    )
                ),
                contribution_name="SelfCompareContribution",
                weight=1.0,
            ),
        ),
    ),
    "OtherCompareValueContributions": ContributionMatcherSpec(
        name="OtherCompareValueContributions",
        inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="other_value",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorEq"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("FieldKind"), right=LiteralValueRef("field")
                        ),
                        EqConditionSpec(
                            left=ValueRef("Compare"), right=LiteralValueRef(True)
                        ),
                    )
                ),
                contribution_name="OtherCompareContribution",
                weight=1.0,
            ),
        ),
    ),
    "LtMethodContributions": ContributionMatcherSpec(
        name="LtMethodContributions",
        inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name="EmptyLtMethodContribution",
        rules=(
            ContributionRuleSpec(
                name="lt",
                condition=EqConditionSpec(
                    left=ValueRef("DecoratorOrder"), right=LiteralValueRef(True)
                ),
                contribution_name="LtMethodContribution",
                weight=1.0,
            ),
        ),
    ),
    "LeMethodContributions": ContributionMatcherSpec(
        name="LeMethodContributions",
        inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name="EmptyLeMethodContribution",
        rules=(
            ContributionRuleSpec(
                name="le",
                condition=EqConditionSpec(
                    left=ValueRef("DecoratorOrder"), right=LiteralValueRef(True)
                ),
                contribution_name="LeMethodContribution",
                weight=1.0,
            ),
        ),
    ),
    "GtMethodContributions": ContributionMatcherSpec(
        name="GtMethodContributions",
        inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name="EmptyGtMethodContribution",
        rules=(
            ContributionRuleSpec(
                name="gt",
                condition=EqConditionSpec(
                    left=ValueRef("DecoratorOrder"), right=LiteralValueRef(True)
                ),
                contribution_name="GtMethodContribution",
                weight=1.0,
            ),
        ),
    ),
    "GeMethodContributions": ContributionMatcherSpec(
        name="GeMethodContributions",
        inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name="EmptyGeMethodContribution",
        rules=(
            ContributionRuleSpec(
                name="ge",
                condition=EqConditionSpec(
                    left=ValueRef("DecoratorOrder"), right=LiteralValueRef(True)
                ),
                contribution_name="GeMethodContribution",
                weight=1.0,
            ),
        ),
    ),
    "SelfLtOrderValueContributions": ContributionMatcherSpec(
        name="SelfLtOrderValueContributions",
        inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="value",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorOrder"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("FieldKind"), right=LiteralValueRef("field")
                        ),
                        EqConditionSpec(
                            left=ValueRef("Compare"), right=LiteralValueRef(True)
                        ),
                    )
                ),
                contribution_name="SelfLtOrderContribution",
                weight=1.0,
            ),
        ),
    ),
    "OtherLtOrderValueContributions": ContributionMatcherSpec(
        name="OtherLtOrderValueContributions",
        inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="value",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorOrder"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("FieldKind"), right=LiteralValueRef("field")
                        ),
                        EqConditionSpec(
                            left=ValueRef("Compare"), right=LiteralValueRef(True)
                        ),
                    )
                ),
                contribution_name="OtherLtOrderContribution",
                weight=1.0,
            ),
        ),
    ),
    "SelfLeOrderValueContributions": ContributionMatcherSpec(
        name="SelfLeOrderValueContributions",
        inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="value",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorOrder"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("FieldKind"), right=LiteralValueRef("field")
                        ),
                        EqConditionSpec(
                            left=ValueRef("Compare"), right=LiteralValueRef(True)
                        ),
                    )
                ),
                contribution_name="SelfLeOrderContribution",
                weight=1.0,
            ),
        ),
    ),
    "OtherLeOrderValueContributions": ContributionMatcherSpec(
        name="OtherLeOrderValueContributions",
        inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="value",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorOrder"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("FieldKind"), right=LiteralValueRef("field")
                        ),
                        EqConditionSpec(
                            left=ValueRef("Compare"), right=LiteralValueRef(True)
                        ),
                    )
                ),
                contribution_name="OtherLeOrderContribution",
                weight=1.0,
            ),
        ),
    ),
    "SelfGtOrderValueContributions": ContributionMatcherSpec(
        name="SelfGtOrderValueContributions",
        inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="value",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorOrder"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("FieldKind"), right=LiteralValueRef("field")
                        ),
                        EqConditionSpec(
                            left=ValueRef("Compare"), right=LiteralValueRef(True)
                        ),
                    )
                ),
                contribution_name="SelfGtOrderContribution",
                weight=1.0,
            ),
        ),
    ),
    "OtherGtOrderValueContributions": ContributionMatcherSpec(
        name="OtherGtOrderValueContributions",
        inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="value",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorOrder"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("FieldKind"), right=LiteralValueRef("field")
                        ),
                        EqConditionSpec(
                            left=ValueRef("Compare"), right=LiteralValueRef(True)
                        ),
                    )
                ),
                contribution_name="OtherGtOrderContribution",
                weight=1.0,
            ),
        ),
    ),
    "SelfGeOrderValueContributions": ContributionMatcherSpec(
        name="SelfGeOrderValueContributions",
        inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="value",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorOrder"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("FieldKind"), right=LiteralValueRef("field")
                        ),
                        EqConditionSpec(
                            left=ValueRef("Compare"), right=LiteralValueRef(True)
                        ),
                    )
                ),
                contribution_name="SelfGeOrderContribution",
                weight=1.0,
            ),
        ),
    ),
    "OtherGeOrderValueContributions": ContributionMatcherSpec(
        name="OtherGeOrderValueContributions",
        inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="value",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorOrder"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("FieldKind"), right=LiteralValueRef("field")
                        ),
                        EqConditionSpec(
                            left=ValueRef("Compare"), right=LiteralValueRef(True)
                        ),
                    )
                ),
                contribution_name="OtherGeOrderContribution",
                weight=1.0,
            ),
        ),
    ),
    "HashMethodContributions": ContributionMatcherSpec(
        name="HashMethodContributions",
        inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name="EmptyHashMethodContribution",
        rules=(
            ContributionRuleSpec(
                name="unsafe",
                condition=EqConditionSpec(
                    left=ValueRef("DecoratorUnsafeHash"), right=LiteralValueRef(True)
                ),
                contribution_name="HashMethodContribution",
                weight=1.0,
            ),
            ContributionRuleSpec(
                name="frozen_eq",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorFrozen"),
                            right=LiteralValueRef(True),
                        ),
                        EqConditionSpec(
                            left=ValueRef("DecoratorEq"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("DecoratorUnsafeHash"),
                            right=LiteralValueRef(False),
                        ),
                    )
                ),
                contribution_name="HashMethodContribution",
                weight=1.0,
            ),
            ContributionRuleSpec(
                name="unhashable_eq",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorFrozen"),
                            right=LiteralValueRef(False),
                        ),
                        EqConditionSpec(
                            left=ValueRef("DecoratorEq"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("DecoratorUnsafeHash"),
                            right=LiteralValueRef(False),
                        ),
                    )
                ),
                contribution_name="HashNoneContribution",
                weight=1.0,
            ),
        ),
    ),
    "HashUnsafeValueContributions": ContributionMatcherSpec(
        name="HashUnsafeValueContributions",
        inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="explicit_hash",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorUnsafeHash"),
                            right=LiteralValueRef(True),
                        ),
                        EqConditionSpec(
                            left=ValueRef("FieldKind"), right=LiteralValueRef("field")
                        ),
                        EqConditionSpec(
                            left=ValueRef("Hash"), right=LiteralValueRef(True)
                        ),
                    )
                ),
                contribution_name="HashValueContribution",
                weight=1.0,
            ),
            ContributionRuleSpec(
                name="compare_hash",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorUnsafeHash"),
                            right=LiteralValueRef(True),
                        ),
                        EqConditionSpec(
                            left=ValueRef("FieldKind"), right=LiteralValueRef("field")
                        ),
                        EqConditionSpec(
                            left=ValueRef("Hash"), right=LiteralValueRef(None)
                        ),
                        EqConditionSpec(
                            left=ValueRef("Compare"), right=LiteralValueRef(True)
                        ),
                    )
                ),
                contribution_name="HashValueContribution",
                weight=1.0,
            ),
        ),
    ),
    "HashFrozenEqValueContributions": ContributionMatcherSpec(
        name="HashFrozenEqValueContributions",
        inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name=None,
        rules=(
            ContributionRuleSpec(
                name="explicit_hash",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorUnsafeHash"),
                            right=LiteralValueRef(False),
                        ),
                        EqConditionSpec(
                            left=ValueRef("DecoratorFrozen"),
                            right=LiteralValueRef(True),
                        ),
                        EqConditionSpec(
                            left=ValueRef("DecoratorEq"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("FieldKind"), right=LiteralValueRef("field")
                        ),
                        EqConditionSpec(
                            left=ValueRef("Hash"), right=LiteralValueRef(True)
                        ),
                    )
                ),
                contribution_name="HashValueContribution",
                weight=1.0,
            ),
            ContributionRuleSpec(
                name="compare_hash",
                condition=AndConditionSpec(
                    items=(
                        EqConditionSpec(
                            left=ValueRef("DecoratorUnsafeHash"),
                            right=LiteralValueRef(False),
                        ),
                        EqConditionSpec(
                            left=ValueRef("DecoratorFrozen"),
                            right=LiteralValueRef(True),
                        ),
                        EqConditionSpec(
                            left=ValueRef("DecoratorEq"), right=LiteralValueRef(True)
                        ),
                        EqConditionSpec(
                            left=ValueRef("FieldKind"), right=LiteralValueRef("field")
                        ),
                        EqConditionSpec(
                            left=ValueRef("Hash"), right=LiteralValueRef(None)
                        ),
                        EqConditionSpec(
                            left=ValueRef("Compare"), right=LiteralValueRef(True)
                        ),
                    )
                ),
                contribution_name="HashValueContribution",
                weight=1.0,
            ),
        ),
    ),
    "FrozenSetattrContributions": ContributionMatcherSpec(
        name="FrozenSetattrContributions",
        inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name="EmptyFrozenSetattrContribution",
        rules=(
            ContributionRuleSpec(
                name="setattr",
                condition=EqConditionSpec(
                    left=ValueRef("DecoratorFrozen"), right=LiteralValueRef(True)
                ),
                contribution_name="FrozenSetattrContribution",
                weight=1.0,
            ),
        ),
    ),
    "FrozenDelattrContributions": ContributionMatcherSpec(
        name="FrozenDelattrContributions",
        inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        default_contribution_name="EmptyFrozenDelattrContribution",
        rules=(
            ContributionRuleSpec(
                name="delattr",
                condition=EqConditionSpec(
                    left=ValueRef("DecoratorFrozen"), right=LiteralValueRef(True)
                ),
                contribution_name="FrozenDelattrContribution",
                weight=1.0,
            ),
        ),
    ),
}
ASSEMBLY_EDGES = {
    "ModuleProduction.classes": AssemblyEdgeSpec(
        name="ModuleProduction.classes",
        context_inputs=(),
        from_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        condition=None,
        matcher_name="ClassDefinitionContribution",
    ),
    "ClassProduction.slots": AssemblyEdgeSpec(
        name="ClassProduction.slots",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="SlotsContribution",
    ),
    "ClassProduction.match_args": AssemblyEdgeSpec(
        name="ClassProduction.match_args",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="MatchArgsContributions",
    ),
    "ClassProduction.annotations": AssemblyEdgeSpec(
        name="ClassProduction.annotations",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="AnnotationContributions",
    ),
    "ClassProduction.field_info": AssemblyEdgeSpec(
        name="ClassProduction.field_info",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="FieldInfoContributions",
    ),
    "ClassProduction.field_defaults": AssemblyEdgeSpec(
        name="ClassProduction.field_defaults",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="DefaultValueContributions",
    ),
    "ClassProduction.init_method": AssemblyEdgeSpec(
        name="ClassProduction.init_method",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="InitMethodContributions",
    ),
    "ClassProduction.repr_method": AssemblyEdgeSpec(
        name="ClassProduction.repr_method",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="ReprMethodContributions",
    ),
    "ClassProduction.eq_method": AssemblyEdgeSpec(
        name="ClassProduction.eq_method",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="EqMethodContributions",
    ),
    "ClassProduction.lt_method": AssemblyEdgeSpec(
        name="ClassProduction.lt_method",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="LtMethodContributions",
    ),
    "ClassProduction.le_method": AssemblyEdgeSpec(
        name="ClassProduction.le_method",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="LeMethodContributions",
    ),
    "ClassProduction.gt_method": AssemblyEdgeSpec(
        name="ClassProduction.gt_method",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="GtMethodContributions",
    ),
    "ClassProduction.ge_method": AssemblyEdgeSpec(
        name="ClassProduction.ge_method",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="GeMethodContributions",
    ),
    "ClassProduction.hash_method": AssemblyEdgeSpec(
        name="ClassProduction.hash_method",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="HashMethodContributions",
    ),
    "ClassProduction.frozen_setattr": AssemblyEdgeSpec(
        name="ClassProduction.frozen_setattr",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="FrozenSetattrContributions",
    ),
    "ClassProduction.frozen_delattr": AssemblyEdgeSpec(
        name="ClassProduction.frozen_delattr",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="FrozenDelattrContributions",
    ),
    "InitMethodProduction.kw_only_fence": AssemblyEdgeSpec(
        name="InitMethodProduction.kw_only_fence",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="KwOnlyFenceContributions",
    ),
    "InitMethodProduction.params": AssemblyEdgeSpec(
        name="InitMethodProduction.params",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="InitParamContribution",
    ),
    "InitMethodProduction.default_factory_guards": AssemblyEdgeSpec(
        name="InitMethodProduction.default_factory_guards",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="DefaultFactoryGuardContributions",
    ),
    "InitMethodProduction.assignments": AssemblyEdgeSpec(
        name="InitMethodProduction.assignments",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="InitAssignContribution",
    ),
    "InitMethodProduction.post_init_call": AssemblyEdgeSpec(
        name="InitMethodProduction.post_init_call",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(),
        condition=None,
        matcher_name="PostInitContribution",
    ),
    "InitMethodProduction.post_init_args": AssemblyEdgeSpec(
        name="InitMethodProduction.post_init_args",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="PostInitArgContributions",
    ),
    "ReprMethodProduction.parts": AssemblyEdgeSpec(
        name="ReprMethodProduction.parts",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="ReprPartContributions",
    ),
    "EqMethodProduction.self_values": AssemblyEdgeSpec(
        name="EqMethodProduction.self_values",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="SelfCompareValueContributions",
    ),
    "EqMethodProduction.other_values": AssemblyEdgeSpec(
        name="EqMethodProduction.other_values",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="OtherCompareValueContributions",
    ),
    "LtMethodProduction.self_values": AssemblyEdgeSpec(
        name="LtMethodProduction.self_values",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="SelfLtOrderValueContributions",
    ),
    "LtMethodProduction.other_values": AssemblyEdgeSpec(
        name="LtMethodProduction.other_values",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="OtherLtOrderValueContributions",
    ),
    "LeMethodProduction.self_values": AssemblyEdgeSpec(
        name="LeMethodProduction.self_values",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="SelfLeOrderValueContributions",
    ),
    "LeMethodProduction.other_values": AssemblyEdgeSpec(
        name="LeMethodProduction.other_values",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="OtherLeOrderValueContributions",
    ),
    "GtMethodProduction.self_values": AssemblyEdgeSpec(
        name="GtMethodProduction.self_values",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="SelfGtOrderValueContributions",
    ),
    "GtMethodProduction.other_values": AssemblyEdgeSpec(
        name="GtMethodProduction.other_values",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="OtherGtOrderValueContributions",
    ),
    "GeMethodProduction.self_values": AssemblyEdgeSpec(
        name="GeMethodProduction.self_values",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="SelfGeOrderValueContributions",
    ),
    "GeMethodProduction.other_values": AssemblyEdgeSpec(
        name="GeMethodProduction.other_values",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="OtherGeOrderValueContributions",
    ),
    "HashMethodProduction.unsafe_values": AssemblyEdgeSpec(
        name="HashMethodProduction.unsafe_values",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="HashUnsafeValueContributions",
    ),
    "HashMethodProduction.frozen_eq_values": AssemblyEdgeSpec(
        name="HashMethodProduction.frozen_eq_values",
        context_inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        from_inputs=(
            AssemblyInputSpec(name="field", collection_name="Fields", collection=None),
        ),
        condition=EqConditionSpec(
            left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
        ),
        matcher_name="HashFrozenEqValueContributions",
    ),
}
ASSEMBLY_PRODUCTIONS = {
    "ModuleProduction": ComposableProductionSpec(
        name="ModuleProduction",
        inputs=(),
        root=RootSpec(build_name="Root", resource_name="ModuleRoot", bindings=()),
        applies=(
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ModuleProduction.classes",
                    context_inputs=(),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    condition=None,
                    matcher_name="ClassDefinitionContribution",
                )
            ),
        ),
    ),
    "ClassProduction": ComposableProductionSpec(
        name="ClassProduction",
        inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        root=RootSpec(
            build_name="ClassDef",
            resource_name="ClassShell",
            bindings=(
                BindingSpec(
                    kind="ident", name="class_name", value=ValueRef("ClassName")
                ),
                BindingSpec(
                    kind="external", name="module_name", value=ValueRef("ModuleName")
                ),
                BindingSpec(
                    kind="external",
                    name="dataclass_params",
                    value=ValueRef("DataclassParams"),
                ),
            ),
        ),
        applies=(
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.slots",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="SlotsContribution",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.match_args",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="MatchArgsContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.annotations",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="Fields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="AnnotationContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.field_info",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="Fields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="FieldInfoContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.field_defaults",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="Fields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="DefaultValueContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.init_method",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="InitMethodContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.repr_method",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="ReprMethodContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.eq_method",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="EqMethodContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.lt_method",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="LtMethodContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.le_method",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="LeMethodContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.gt_method",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="GtMethodContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.ge_method",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="GeMethodContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.hash_method",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="HashMethodContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.frozen_setattr",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="FrozenSetattrContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ClassProduction.frozen_delattr",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="FrozenDelattrContributions",
                )
            ),
        ),
    ),
    "InitMethodProduction": ComposableProductionSpec(
        name="InitMethodProduction",
        inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        root=RootSpec(
            build_name="InitMethod", resource_name="InitMethodTemplate", bindings=()
        ),
        applies=(
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="InitMethodProduction.kw_only_fence",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="KwOnlyFenceContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="InitMethodProduction.params",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="Fields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="InitParamContribution",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="InitMethodProduction.default_factory_guards",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="Fields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="DefaultFactoryGuardContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="InitMethodProduction.assignments",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="Fields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="InitAssignContribution",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="InitMethodProduction.post_init_call",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(),
                    condition=None,
                    matcher_name="PostInitContribution",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="InitMethodProduction.post_init_args",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="Fields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="PostInitArgContributions",
                )
            ),
        ),
    ),
    "ReprMethodProduction": ComposableProductionSpec(
        name="ReprMethodProduction",
        inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        root=RootSpec(
            build_name="ReprMethod",
            resource_name="ReprMethodTemplate",
            bindings=(
                BindingSpec(
                    kind="external", name="class_name", value=ValueRef("ClassName")
                ),
            ),
        ),
        applies=(
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="ReprMethodProduction.parts",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="Fields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="ReprPartContributions",
                )
            ),
        ),
    ),
    "EqMethodProduction": ComposableProductionSpec(
        name="EqMethodProduction",
        inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        root=RootSpec(
            build_name="EqMethod", resource_name="EqMethodTemplate", bindings=()
        ),
        applies=(
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="EqMethodProduction.self_values",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="Fields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="SelfCompareValueContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="EqMethodProduction.other_values",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="Fields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="OtherCompareValueContributions",
                )
            ),
        ),
    ),
    "LtMethodProduction": ComposableProductionSpec(
        name="LtMethodProduction",
        inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        root=RootSpec(
            build_name="LtMethod", resource_name="LtMethodTemplate", bindings=()
        ),
        applies=(
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="LtMethodProduction.self_values",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="Fields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="SelfLtOrderValueContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="LtMethodProduction.other_values",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="Fields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="OtherLtOrderValueContributions",
                )
            ),
        ),
    ),
    "LeMethodProduction": ComposableProductionSpec(
        name="LeMethodProduction",
        inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        root=RootSpec(
            build_name="LeMethod", resource_name="LeMethodTemplate", bindings=()
        ),
        applies=(
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="LeMethodProduction.self_values",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="Fields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="SelfLeOrderValueContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="LeMethodProduction.other_values",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="Fields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="OtherLeOrderValueContributions",
                )
            ),
        ),
    ),
    "GtMethodProduction": ComposableProductionSpec(
        name="GtMethodProduction",
        inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        root=RootSpec(
            build_name="GtMethod", resource_name="GtMethodTemplate", bindings=()
        ),
        applies=(
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="GtMethodProduction.self_values",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="Fields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="SelfGtOrderValueContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="GtMethodProduction.other_values",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="Fields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="OtherGtOrderValueContributions",
                )
            ),
        ),
    ),
    "GeMethodProduction": ComposableProductionSpec(
        name="GeMethodProduction",
        inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        root=RootSpec(
            build_name="GeMethod", resource_name="GeMethodTemplate", bindings=()
        ),
        applies=(
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="GeMethodProduction.self_values",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="Fields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="SelfGeOrderValueContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="GeMethodProduction.other_values",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="Fields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="OtherGeOrderValueContributions",
                )
            ),
        ),
    ),
    "HashMethodProduction": ComposableProductionSpec(
        name="HashMethodProduction",
        inputs=(
            AssemblyInputSpec(
                name="facade", collection_name="Facades", collection=None
            ),
        ),
        root=RootSpec(
            build_name="HashMethod", resource_name="HashMethodTemplate", bindings=()
        ),
        applies=(
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="HashMethodProduction.unsafe_values",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="Fields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="HashUnsafeValueContributions",
                )
            ),
            InlineApplySpec(
                edge=AssemblyEdgeSpec(
                    name="HashMethodProduction.frozen_eq_values",
                    context_inputs=(
                        AssemblyInputSpec(
                            name="facade", collection_name="Facades", collection=None
                        ),
                    ),
                    from_inputs=(
                        AssemblyInputSpec(
                            name="field", collection_name="Fields", collection=None
                        ),
                    ),
                    condition=EqConditionSpec(
                        left=ValueRef("FieldOwner"), right=ValueRef("ClassId")
                    ),
                    matcher_name="HashFrozenEqValueContributions",
                )
            ),
        ),
    ),
}
ASSEMBLY_ASSEMBLIES = {
    "DataclassModule": AssemblySpec(
        name="DataclassModule", production_name="ModuleProduction"
    )
}

ASSEMBLY_CONCEPT = _YidlSimpleNamespace(
    properties=ASSEMBLY_PROPERTIES,
    resources=ASSEMBLY_RESOURCES,
    contributions=ASSEMBLY_CONTRIBUTIONS,
    contribution_matchers=ASSEMBLY_MATCHERS,
    assembly_edges=ASSEMBLY_EDGES,
    composable_productions=ASSEMBLY_PRODUCTIONS,
    assemblies=ASSEMBLY_ASSEMBLIES,
)

_YIDL_BASE_BUILD_CONTAINER = globals().get("build_container")


def build_container(builder):
    if _YIDL_BASE_BUILD_CONTAINER is not None:
        return _YIDL_BASE_BUILD_CONTAINER(builder)
    return builder.freeze()


def build_assembly(entrypoint, container, *, unroll="auto"):
    return run_assembly(ASSEMBLY_CONCEPT, entrypoint, container, unroll=unroll)


def build_DataclassModule(container, *, unroll="auto"):
    return build_assembly("DataclassModule", container, unroll=unroll)
