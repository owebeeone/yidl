import ast

class YIDLTransformer(ast.NodeTransformer):
    """
    Transforms DSL Python AST snippets into execution context ASTs.
    Used during code generation of _lc_commit, _lc_rollback, etc.
    """
    def __init__(self, field_name: str, aliases: dict):
        self.field_name = field_name
        self.aliases = aliases

    def _build_attr(self, path: str, ctx_type) -> ast.Attribute:
        parts = path.split('.')
        node = ast.Name(id=parts[0], ctx=ast.Load())
        for part in parts[1:]:
            node = ast.Attribute(value=node, attr=part, ctx=ast.Load())
        return ast.Attribute(value=node, attr=self.field_name, ctx=ctx_type())

    def visit_Expr(self, node: ast.Expr) -> ast.AST:
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute):
            caller, method = node.value.func.value, node.value.func.attr
            if isinstance(caller, ast.Name) and caller.id in self.aliases and method == 'write':
                target = self._build_attr(self.aliases[caller.id], ast.Store)
                new_node = ast.Assign(targets=[target], value=node.value.args[0])
                return ast.copy_location(new_node, node)
        self.generic_visit(node)
        return node

    def visit_Call(self, node: ast.Call) -> ast.AST:
        if isinstance(node.func, ast.Attribute):
            caller, method = node.func.value, node.func.attr
            if isinstance(caller, ast.Name) and caller.id in self.aliases:
                if method == 'read':
                    return ast.copy_location(self._build_attr(self.aliases[caller.id], ast.Load), node)
                elif method == 'has':
                    read_node = self._build_attr(self.aliases[caller.id], ast.Load)
                    missing_node = ast.Name(id='MISSING', ctx=ast.Load())
                    new_node = ast.Compare(left=read_node, ops=[ast.IsNot()], comparators=[missing_node])
                    return ast.copy_location(new_node, node)
        self.generic_visit(node)
        return node
