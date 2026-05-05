from __future__ import annotations

from support.golden_case import run_case
from yidl.capsule.build_mapper import CapsuleClassBuildPlan
from yidl.capsule.build_mapper import ChildPortPlan
from yidl.capsule.build_mapper import RuntimePortRef
from yidl.capsule.build_mapper import TemplateEdgePlan
from yidl.capsule.build_mapper import build_class_source
from yidl.capsule.definition import capsule
from yidl.capsule.definition import concept
from yidl.generation.data_def_sys import AddIfAbsent
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import from_astichi_code
from yidl.generation.data_def_sys import match
from yidl.generation.data_def_sys import read


INIT_METHOD = from_astichi_code(
    "def __init__(self__astichi_keep__, params__astichi_param_hole__):\n"
    "    astichi_hole(body)\n"
)
REQUIRED_PARAM = from_astichi_code(
    "def astichi_params(*, field_name__astichi_arg__):\n"
    "    pass\n"
)
DEFAULTED_PARAM = from_astichi_code(
    "def astichi_params(\n"
    "    *,\n"
    "    field_name__astichi_arg__=astichi_bind_external(default_value),\n"
    "):\n"
    "    pass\n"
)
ASSIGNMENT = from_astichi_code(
    "astichi_import(self)\n"
    "self.astichi_ref(external=target_path)._ = astichi_pass(\n"
    "    source_name,\n"
    "    outer_bind=True,\n"
    ")\n"
)

TEMPLATE_VALUE_NAMES = (
    (INIT_METHOD, "INIT_METHOD"),
    (ASSIGNMENT, "ASSIGNMENT"),
)
TEMPLATE_GLOBALS = {
    "INIT_METHOD": INIT_METHOD,
    "ASSIGNMENT": ASSIGNMENT,
}


def define_class_and_fields(dds: DataDefinitionSystem) -> None:
    name = dds.ensure_property("Name", str, default=REQUIRED, storage_name="name")
    init = dds.ensure_property("Init", bool, default=True, storage_name="init")
    defaulted = dds.ensure_property(
        "Defaulted",
        bool,
        default=False,
        storage_name="defaulted",
    )
    default_value = dds.ensure_property(
        "DefaultValue",
        object,
        default=None,
        storage_name="default_value",
    )
    order = dds.ensure_property("Order", int, default=0, storage_name="order")
    target_port = dds.ensure_property(
        "TargetPort",
        object,
        default=REQUIRED,
        storage_name="target_port",
    )
    template = dds.ensure_property(
        "Template",
        object,
        default=REQUIRED,
        storage_name="template",
    )
    source_name = dds.ensure_property(
        "SourceName",
        str,
        default=REQUIRED,
        storage_name="source_name",
    )
    target_name = dds.ensure_property(
        "TargetName",
        str,
        default=REQUIRED,
        storage_name="target_name",
    )
    runtime_value = dds.ensure_property(
        "RuntimeValue",
        object,
        default=REQUIRED,
        storage_name="runtime_value",
    )
    class_value = dds.ensure_record(
        "ClassValue",
        name,
        target_port,
        order,
        runtime_value,
    )
    field = dds.ensure_record("FieldInput", name, init, defaulted, default_value, order)
    component = dds.ensure_record("Component", name, target_port, order, template)
    param = dds.ensure_record(
        "InitParam",
        name,
        target_port,
        order,
        template,
        defaulted,
        default_value,
    )
    assignment = dds.ensure_record(
        "InitAssignment",
        name,
        target_port,
        order,
        template,
        source_name,
        target_name,
    )
    dds.ensure_collection(
        "ClassValues",
        class_value,
        cardinality=dds.many,
        identity=name,
    )
    fields = dds.ensure_collection("Fields", field, cardinality=dds.many, identity=name)
    dds.ensure_collection("Components", component, cardinality=dds.many, identity=name)
    dds.ensure_collection("InitParams", param, cardinality=dds.many, identity=name)
    dds.ensure_collection(
        "InitAssignments",
        assignment,
        cardinality=dds.many,
        identity=name,
    )
    dds.ensure_computed_collection("InitFields", source=fields, when=(init.eq(True),))
    dds.ensure_port("Class.name", cardinality=dds.single)
    dds.ensure_port("Class.body", cardinality=dds.many)
    dds.ensure_port("Init.params", cardinality=dds.many)
    dds.ensure_port("Init.body", cardinality=dds.many)
    dds.ensure_port_index(target=target_port, order=order)


def define_init_productions(dds: DataDefinitionSystem) -> None:
    name = dds.ensure_property("Name", str, default=REQUIRED, storage_name="name")
    order = dds.ensure_property("Order", int, default=0, storage_name="order")
    defaulted = dds.ensure_property(
        "Defaulted",
        bool,
        default=False,
        storage_name="defaulted",
    )
    default_value = dds.ensure_property(
        "DefaultValue",
        object,
        default=None,
        storage_name="default_value",
    )
    target_port = dds.ensure_property(
        "TargetPort",
        object,
        default=REQUIRED,
        storage_name="target_port",
    )
    template = dds.ensure_property(
        "Template",
        object,
        default=REQUIRED,
        storage_name="template",
    )
    source_name = dds.ensure_property(
        "SourceName",
        str,
        default=REQUIRED,
        storage_name="source_name",
    )
    target_name = dds.ensure_property(
        "TargetName",
        str,
        default=REQUIRED,
        storage_name="target_name",
    )
    runtime_value = dds.ensure_property(
        "RuntimeValue",
        object,
        default=REQUIRED,
        storage_name="runtime_value",
    )
    init_fields = dds.ensure_computed_collection(
        "InitFields",
        source=dds.ensure_collection(
            "Fields",
            dds.ensure_record(
                "FieldInput",
                name,
                dds.ensure_property("Init", bool, default=True, storage_name="init"),
                defaulted,
                default_value,
                order,
            ),
            cardinality=dds.many,
            identity=name,
        ),
        when=(
            dds.ensure_property("Init", bool, default=True, storage_name="init").eq(
                True
            ),
        ),
    )
    class_values = dds.ensure_collection(
        "ClassValues",
        dds.ensure_record("ClassValue", name, target_port, order, runtime_value),
        cardinality=dds.many,
        identity=name,
    )
    components = dds.ensure_collection(
        "Components",
        dds.ensure_record("Component", name, target_port, order, template),
        cardinality=dds.many,
        identity=name,
    )
    params = dds.ensure_collection(
        "InitParams",
        dds.ensure_record(
            "InitParam",
            name,
            target_port,
            order,
            template,
            defaulted,
            default_value,
        ),
        cardinality=dds.many,
        identity=name,
    )
    assignments = dds.ensure_collection(
        "InitAssignments",
        dds.ensure_record(
            "InitAssignment",
            name,
            target_port,
            order,
            template,
            source_name,
            target_name,
        ),
        cardinality=dds.many,
        identity=name,
    )
    class_name = dds.ensure_port("Class.name", cardinality=dds.single)
    class_body = dds.ensure_port("Class.body", cardinality=dds.many)
    init_params = dds.ensure_port("Init.params", cardinality=dds.many)
    init_body = dds.ensure_port("Init.body", cardinality=dds.many)
    param_template = dds.ensure_matcher("InitParamTemplate")
    field_input = param_template.ensure_input("field", init_fields)
    param_template.default(REQUIRED_PARAM)
    param_template.rule(
        when=(field_input.prop(defaulted).eq(True),),
        resource=DEFAULTED_PARAM,
        name="defaulted-param",
    )
    dds.ensure_production_group(
        "Class",
        dds.production(
            "InitMethod",
            source=class_values,
            target=components,
            values={
                name: "__init__",
                target_port: class_body.of("runtime"),
                order: 0,
                template: INIT_METHOD,
            },
            policy=AddIfAbsent,
        ),
        dds.production(
            "InitParam",
            source=param_template.results(),
            target=params,
            values={
                name: match.record("field").prop(name),
                target_port: init_params.of(("runtime", "__init__")),
                order: match.record("field").prop(order),
                template: match.resource(),
                defaulted: match.value(0),
                default_value: match.record("field").prop(default_value),
            },
            policy=AddIfAbsent,
        ),
        dds.production(
            "InitAssignment",
            source=init_fields,
            target=assignments,
            values={
                name: read(name),
                target_port: init_body.of(("runtime", "__init__")),
                order: read(order),
                template: ASSIGNMENT,
                source_name: read(name),
                target_name: read(name),
            },
            policy=AddIfAbsent,
        ),
    )


def _definition():
    return capsule(
        "BuildMapperInit",
        concept("class-and-fields", define_class_and_fields),
        concept("init-productions", define_init_productions),
    )


def _runtime():
    return _definition().load_runtime(
        value_names=TEMPLATE_VALUE_NAMES,
        runtime_globals=TEMPLATE_GLOBALS,
    )


def _container():
    runtime = _runtime()
    namespace = runtime.namespace
    builder = runtime.new_builder()
    builder.add(
        namespace["ClassValuesCollection"],
        namespace["ClassValue"](
            name="Example",
            target_port=namespace["ClassNamePort"].of("runtime"),
            order=0,
            runtime_value="Example",
        ),
    )
    field = namespace["FieldInput"]
    fields = namespace["FieldsCollection"]
    builder.add(fields, field(name="count", init=True, defaulted=False, order=0))
    builder.add(
        fields,
        field(name="label", init=True, defaulted=True, default_value="cold", order=1),
    )
    builder.add(
        fields,
        field(name="retries", init=True, defaulted=True, default_value=3, order=2),
    )
    return runtime.build_container(builder), namespace


def render_case() -> str:
    container, namespace = _container()
    return build_class_source(
        container,
        namespace,
        CapsuleClassBuildPlan(
            class_name=RuntimePortRef("ClassNamePort", "runtime"),
            class_body=RuntimePortRef("ClassBodyPort", "runtime"),
            child_ports=(
                ChildPortPlan(
                    parent_name="__init__",
                    port_name="InitParamsPort",
                    target_hole="params",
                    edge=TemplateEdgePlan(
                        "InitParam",
                        arg_names=lambda record: {"field_name": record.name},
                        bind=lambda record: (
                            {"default_value": record.default_value}
                            if record.defaulted
                            else {}
                        ),
                    ),
                ),
                ChildPortPlan(
                    parent_name="__init__",
                    port_name="InitBodyPort",
                    target_hole="body",
                    edge=TemplateEdgePlan(
                        "InitBody",
                        arg_names=lambda record: {"source_name": record.source_name},
                        bind=lambda record: {"target_path": record.target_name},
                        keep_names=lambda record: ("self",),
                    ),
                ),
            ),
        ),
    )


def validate_case(source: str) -> None:
    namespace = {}
    exec(source, namespace)
    example = namespace["Example"]

    assert tuple(example(count=None).__dict__.items()) == (
        ("count", None),
        ("label", "cold"),
        ("retries", 3),
    )
    overridden = example(count=5, label="hot", retries=8)
    assert overridden.count == 5
    assert overridden.label == "hot"
    assert overridden.retries == 8
    assert "class Example:" in source
    assert "def __init__(self, *, count, label='cold', retries=3):" in source
    assert "self.count = count" in source


if __name__ == "__main__":
    raise SystemExit(run_case("capsule_build_mapper.py", render_case, validate_case))
