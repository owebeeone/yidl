from dataclasses import dataclass, field
from typing import List, Optional, Dict
from yidl.lexer import Token

@dataclass
class StoreNode:
    name: str
    properties: Dict[str, str]

@dataclass
class SurfaceNode:
    name: str
    properties: Dict[str, str]

@dataclass
class InputNode:
    name: str
    type_expr: str
    default_expr: Optional[str]

@dataclass
class CompileAssertNode:
    expression: str

@dataclass
class CodeNode:
    code: str
    line_num: int

@dataclass
class InlineActionNode:
    action_type: str
    expression: str

@dataclass
class BlockActionNode:
    action_type: str
    code_block: CodeNode

@dataclass
class BehaviorNode:
    names: List[str]
    properties: Dict[str, str] = field(default_factory=dict)
    actions: List[InlineActionNode | BlockActionNode] = field(default_factory=list)
    code: Optional[CodeNode] = None

@dataclass
class TransducerNode:
    name: str
    options: Dict[str, str]
    inputs: List[InputNode] = field(default_factory=list)
    compile_asserts: List[CompileAssertNode] = field(default_factory=list)
    behaviors: List[BehaviorNode] = field(default_factory=list)

@dataclass
class AST:
    stores: List[StoreNode] = field(default_factory=list)
    surfaces: List[SurfaceNode] = field(default_factory=list)
    transducers: List[TransducerNode] = field(default_factory=list)

class YIDLParser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Optional[Token]:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self) -> Token:
        token = self.peek()
        self.pos += 1
        return token

    def parse(self) -> AST:
        ast = AST()
        try:
            while self.peek():
                token = self.consume()
                if token.type != "STATEMENT": continue

                if token.value.startswith("store "):
                    ast.stores.append(self._parse_entity(token, StoreNode))
                elif token.value.startswith("surface "):
                    ast.surfaces.append(self._parse_entity(token, SurfaceNode))
                elif token.value.startswith("transducer "):
                    ast.transducers.append(self._parse_transducer(token))
        except Exception as e:
            failed_token = self.tokens[self.pos - 1] if self.pos > 0 else None
            line_info = f" at line {failed_token.line_num}" if failed_token else ""
            code_snippet = failed_token.value.strip() if failed_token else ""
            raise RuntimeError(f"Parsing Error{line_info} [{code_snippet}]: {str(e)}") from e
        return ast

    def _parse_dict(self, s: str) -> Dict[str, str]:
        res = {}
        if not s.strip(): return res
        for part in s.split(","):
            part = part.strip()
            if not part: continue

            if "=" in part:
                k, v = part.split("=", 1)
                res[k.strip()] = v.strip().strip('"')
            else:
                res[part] = "True"
        return res

    def _parse_entity(self, token: Token, node_cls):
        left, _, right = token.value.partition(":")
        name = left.split()[1].strip()
        return node_cls(name, self._parse_dict(right))

    def _parse_transducer(self, token: Token) -> TransducerNode:
        left, _, right = token.value.partition(":")
        name = left.split()[1].strip()
        node = TransducerNode(name, self._parse_dict(right))

        while self.peek() and self.peek().indent > token.indent:
            child = self.consume()
            if child.type != "STATEMENT": continue

            if child.value == "inputs:":
                self._parse_inputs(node, child.indent)
            elif child.value == "compile_assert:":
                self._parse_asserts(node, child.indent)
            elif child.value.startswith("behavior "):
                node.behaviors.append(self._parse_behavior(child))
        return node

    def _parse_inputs(self, node: TransducerNode, parent_indent: int):
        while self.peek() and self.peek().indent > parent_indent:
            token = self.consume()
            left, _, right = token.value.partition(":")
            name = left.strip()
            type_expr = right.strip()
            default = None
            if "=" in type_expr:
                type_expr, default = [x.strip() for x in type_expr.split("=", 1)]
            node.inputs.append(InputNode(name, type_expr, default))

    def _parse_asserts(self, node: TransducerNode, parent_indent: int):
        while self.peek() and self.peek().indent > parent_indent:
            node.compile_asserts.append(CompileAssertNode(self.consume().value))

    def _parse_behavior(self, token: Token) -> BehaviorNode:
        names_str = token.value.split(" ", 1)[1].replace(":", "")
        names = [n.strip() for n in names_str.split(",")]
        node = BehaviorNode(names)

        raw_code_lines = []

        while self.peek() and self.peek().indent > token.indent:
            child = self.peek()

            if child.type == "CODE_SNIPPET":
                child = self.consume()
                raw_code_lines.append(child.value)
                continue

            if "=" in child.value and "(" not in child.value and ":" not in child.value and not child.value.startswith("if ") and not child.value.startswith("assert "):
                self.consume()
                k, v = [x.strip() for x in child.value.split("=", 1)]
                node.properties[k] = v
                continue

            if child.value.startswith("map_insert:"):
                self.consume()
                expr = child.value.split(":", 1)[1].strip()
                node.actions.append(InlineActionNode("map_insert", expr))
                continue

            if child.value.startswith("get:") or child.value.startswith("set"):
                self.consume()
                left, _, right = child.value.partition(":")
                action_type = left.strip()
                right = right.strip()

                if right:
                    node.actions.append(InlineActionNode(action_type, right))
                else:
                    if self.peek() and self.peek().type == "CODE_SNIPPET":
                        code_tok = self.consume()
                        node.actions.append(BlockActionNode(action_type, CodeNode(code_tok.value, code_tok.line_num)))
                    else:
                        action_lines = []
                        start_line = self.peek().line_num if self.peek() else child.line_num
                        while self.peek() and self.peek().indent > child.indent:
                            descendant = self.consume()
                            rel_indent = " " * max(0, descendant.indent - child.indent - 4)
                            action_lines.append(rel_indent + descendant.value)

                        code_str = "\n".join(action_lines).strip()
                        node.actions.append(BlockActionNode(action_type, CodeNode(code_str, start_line)))
                continue

            child = self.consume()
            rel_indent = " " * max(0, child.indent - token.indent - 4)
            raw_code_lines.append(rel_indent + child.value)

        if raw_code_lines:
            code_str = "\n".join(raw_code_lines).strip()
            node.code = CodeNode(code_str, token.line_num)

        return node
