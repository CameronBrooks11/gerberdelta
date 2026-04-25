from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, TypeAlias

# ---------------------------------------------------------------------------
# Expression node types
# ---------------------------------------------------------------------------
# These form a recursive union (ExprNode).  With `from __future__ import
# annotations` all field type annotations are strings, so forward references
# to ExprNode resolve correctly even though the alias is defined after the
# dataclasses.


@dataclass
class LiteralNode:
    value: float = 0.0


@dataclass
class VariableNode:
    index: int = 1  # $1, $2, ... -- 1-based


@dataclass
class UnaryNegNode:
    operand: ExprNode = field(default_factory=LiteralNode)


@dataclass
class BinaryNode:
    op: str = "+"  # "+", "-", "x", "/"
    left: ExprNode = field(default_factory=LiteralNode)
    right: ExprNode = field(default_factory=LiteralNode)


ExprNode: TypeAlias = LiteralNode | VariableNode | UnaryNegNode | BinaryNode


def _lit(v: float = 0.0) -> LiteralNode:
    return LiteralNode(value=v)


# ---------------------------------------------------------------------------
# Macro primitive templates  (ExprNode fields -- evaluated later)
# ---------------------------------------------------------------------------


@dataclass
class CirclePrimitive:
    code: ClassVar[int] = 1
    exposure: ExprNode = field(default_factory=lambda: _lit(1.0))
    diameter: ExprNode = field(default_factory=_lit)
    center_x: ExprNode = field(default_factory=_lit)
    center_y: ExprNode = field(default_factory=_lit)
    rotation: ExprNode = field(default_factory=_lit)


@dataclass
class LineVectorPrimitive:
    code: ClassVar[int] = 20
    exposure: ExprNode = field(default_factory=lambda: _lit(1.0))
    width: ExprNode = field(default_factory=_lit)
    start_x: ExprNode = field(default_factory=_lit)
    start_y: ExprNode = field(default_factory=_lit)
    end_x: ExprNode = field(default_factory=_lit)
    end_y: ExprNode = field(default_factory=_lit)
    rotation: ExprNode = field(default_factory=_lit)


@dataclass
class LineCenterPrimitive:
    code: ClassVar[int] = 21
    exposure: ExprNode = field(default_factory=lambda: _lit(1.0))
    width: ExprNode = field(default_factory=_lit)
    height: ExprNode = field(default_factory=_lit)
    center_x: ExprNode = field(default_factory=_lit)
    center_y: ExprNode = field(default_factory=_lit)
    rotation: ExprNode = field(default_factory=_lit)


@dataclass
class OutlinePrimitive:
    code: ClassVar[int] = 4
    exposure: ExprNode = field(default_factory=lambda: _lit(1.0))
    vertices: list[ExprNode] = field(default_factory=list)  # flat [x0,y0,x1,y1,...]
    rotation: ExprNode = field(default_factory=_lit)


@dataclass
class PolygonPrimitive:
    code: ClassVar[int] = 5
    exposure: ExprNode = field(default_factory=lambda: _lit(1.0))
    num_vertices: ExprNode = field(default_factory=lambda: _lit(4.0))
    center_x: ExprNode = field(default_factory=_lit)
    center_y: ExprNode = field(default_factory=_lit)
    diameter: ExprNode = field(default_factory=_lit)
    rotation: ExprNode = field(default_factory=_lit)


@dataclass
class MoirePrimitive:
    code: ClassVar[int] = 6
    center_x: ExprNode = field(default_factory=_lit)
    center_y: ExprNode = field(default_factory=_lit)
    outer_diameter: ExprNode = field(default_factory=_lit)
    ring_thickness: ExprNode = field(default_factory=_lit)
    ring_gap: ExprNode = field(default_factory=_lit)
    max_rings: ExprNode = field(default_factory=_lit)
    crosshair_thickness: ExprNode = field(default_factory=_lit)
    crosshair_length: ExprNode = field(default_factory=_lit)
    rotation: ExprNode = field(default_factory=_lit)


@dataclass
class ThermalPrimitive:
    code: ClassVar[int] = 7
    center_x: ExprNode = field(default_factory=_lit)
    center_y: ExprNode = field(default_factory=_lit)
    outer_diameter: ExprNode = field(default_factory=_lit)
    inner_diameter: ExprNode = field(default_factory=_lit)
    gap: ExprNode = field(default_factory=_lit)
    rotation: ExprNode = field(default_factory=_lit)


@dataclass
class AssignmentStatement:
    variable_index: int
    expression: ExprNode = field(default_factory=_lit)


MacroBodyItem: TypeAlias = (
    CirclePrimitive
    | LineVectorPrimitive
    | LineCenterPrimitive
    | OutlinePrimitive
    | PolygonPrimitive
    | MoirePrimitive
    | ThermalPrimitive
    | AssignmentStatement
)


@dataclass
class MacroDef:
    name: str
    body: list[MacroBodyItem] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Evaluated primitive types  (float fields -- produced after evaluation)
# ---------------------------------------------------------------------------


@dataclass
class EvaluatedCircle:
    code: ClassVar[int] = 1
    exposure: float = 0.0
    diameter: float = 0.0
    center_x: float = 0.0
    center_y: float = 0.0
    rotation: float = 0.0


@dataclass
class EvaluatedLineVector:
    code: ClassVar[int] = 20
    exposure: float = 0.0
    width: float = 0.0
    start_x: float = 0.0
    start_y: float = 0.0
    end_x: float = 0.0
    end_y: float = 0.0
    rotation: float = 0.0


@dataclass
class EvaluatedLineCenter:
    code: ClassVar[int] = 21
    exposure: float = 0.0
    width: float = 0.0
    height: float = 0.0
    center_x: float = 0.0
    center_y: float = 0.0
    rotation: float = 0.0


@dataclass
class EvaluatedOutline:
    code: ClassVar[int] = 4
    exposure: float = 0.0
    vertices: list[float] = field(default_factory=list)
    rotation: float = 0.0


@dataclass
class EvaluatedPolygon:
    code: ClassVar[int] = 5
    exposure: float = 0.0
    num_vertices: int = 4
    center_x: float = 0.0
    center_y: float = 0.0
    diameter: float = 0.0
    rotation: float = 0.0


@dataclass
class EvaluatedMoire:
    code: ClassVar[int] = 6
    center_x: float = 0.0
    center_y: float = 0.0
    outer_diameter: float = 0.0
    ring_thickness: float = 0.0
    ring_gap: float = 0.0
    max_rings: int = 0
    crosshair_thickness: float = 0.0
    crosshair_length: float = 0.0
    rotation: float = 0.0


@dataclass
class EvaluatedThermal:
    code: ClassVar[int] = 7
    center_x: float = 0.0
    center_y: float = 0.0
    outer_diameter: float = 0.0
    inner_diameter: float = 0.0
    gap: float = 0.0
    rotation: float = 0.0


EvaluatedPrimitive: TypeAlias = (
    EvaluatedCircle
    | EvaluatedLineVector
    | EvaluatedLineCenter
    | EvaluatedOutline
    | EvaluatedPolygon
    | EvaluatedMoire
    | EvaluatedThermal
)

# ---------------------------------------------------------------------------
# Expression parser (internal)
# ---------------------------------------------------------------------------
# Tokens: ("number", "3.14") | ("variable", "1") | ("op", "+") | ("lparen","(") | ("rparen",")")


def _tokenize_expr(s: str) -> list[tuple[str, str]]:
    tokens: list[tuple[str, str]] = []
    i = 0
    while i < len(s):
        c = s[i]
        if c in " \t\n\r":
            i += 1
        elif c.isdigit() or (c == "." and i + 1 < len(s) and s[i + 1].isdigit()):
            j = i
            while j < len(s) and (s[j].isdigit() or s[j] == "."):
                j += 1
            tokens.append(("number", s[i:j]))
            i = j
        elif c == "$":
            i += 1
            j = i
            while j < len(s) and s[j].isdigit():
                j += 1
            tokens.append(("variable", s[i:j]))
            i = j
        elif c in "+-/":
            tokens.append(("op", c))
            i += 1
        elif c in "xX":
            tokens.append(("op", "x"))
            i += 1
        elif c == "(":
            tokens.append(("lparen", "("))
            i += 1
        elif c == ")":
            tokens.append(("rparen", ")"))
            i += 1
        else:
            i += 1
    return tokens


class _ExprParser:
    """Recursive-descent parser for Gerber macro expressions.

    Precedence (low -> high): additive (+/-) -> multiplicative (x/) -> unary (-) -> primary
    """

    def __init__(self, tokens: list[tuple[str, str]]) -> None:
        self._tokens = tokens
        self._pos = 0

    def _peek(self) -> tuple[str, str] | None:
        return self._tokens[self._pos] if self._pos < len(self._tokens) else None

    def _consume(self) -> tuple[str, str]:
        tok = self._tokens[self._pos]
        self._pos += 1
        return tok

    def parse(self) -> ExprNode:
        return self._additive()

    def _additive(self) -> ExprNode:
        left: ExprNode = self._multiplicative()
        tok = self._peek()
        while tok is not None and tok[0] == "op" and tok[1] in ("+", "-"):
            op = self._consume()[1]
            right = self._multiplicative()
            left = BinaryNode(op=op, left=left, right=right)
            tok = self._peek()
        return left

    def _multiplicative(self) -> ExprNode:
        left: ExprNode = self._unary()
        tok = self._peek()
        while tok is not None and tok[0] == "op" and tok[1] in ("x", "/"):
            op = self._consume()[1]
            right = self._unary()
            left = BinaryNode(op=op, left=left, right=right)
            tok = self._peek()
        return left

    def _unary(self) -> ExprNode:
        tok = self._peek()
        if tok is not None and tok[0] == "op" and tok[1] == "-":
            self._consume()
            return UnaryNegNode(operand=self._unary())
        return self._primary()

    def _primary(self) -> ExprNode:
        tok = self._peek()
        if tok is None:
            return LiteralNode(value=0.0)
        if tok[0] == "number":
            self._consume()
            return LiteralNode(value=float(tok[1]))
        if tok[0] == "variable":
            self._consume()
            return VariableNode(index=int(tok[1]))
        if tok[0] == "lparen":
            self._consume()
            expr = self._additive()
            if (t := self._peek()) is not None and t[0] == "rparen":
                self._consume()
            return expr
        return LiteralNode(value=0.0)


def _parse_expr(s: str) -> ExprNode:
    return _ExprParser(_tokenize_expr(s)).parse()


def _parse_args(s: str) -> list[ExprNode]:
    """Split a comma-separated argument string (respecting parentheses) and parse each arg."""
    args: list[ExprNode] = []
    depth = 0
    buf = ""
    for c in s:
        if c == "(":
            depth += 1
            buf += c
        elif c == ")":
            depth -= 1
            buf += c
        elif c == "," and depth == 0:
            args.append(_parse_expr(buf.strip()))
            buf = ""
        else:
            buf += c
    if buf.strip():
        args.append(_parse_expr(buf.strip()))
    return args


def _get_arg(args: list[ExprNode], idx: int, default: float = 0.0) -> ExprNode:
    return args[idx] if idx < len(args) else _lit(default)


def _build_primitive(code: int, args: list[ExprNode]) -> MacroBodyItem | None:
    """Construct the appropriate primitive template from a code and argument list."""
    if code == 1:
        return CirclePrimitive(
            exposure=_get_arg(args, 0, 1.0),
            diameter=_get_arg(args, 1),
            center_x=_get_arg(args, 2),
            center_y=_get_arg(args, 3),
            rotation=_get_arg(args, 4),
        )
    if code in (2, 20):
        return LineVectorPrimitive(
            exposure=_get_arg(args, 0, 1.0),
            width=_get_arg(args, 1),
            start_x=_get_arg(args, 2),
            start_y=_get_arg(args, 3),
            end_x=_get_arg(args, 4),
            end_y=_get_arg(args, 5),
            rotation=_get_arg(args, 6),
        )
    if code in (21, 22):
        return LineCenterPrimitive(
            exposure=_get_arg(args, 0, 1.0),
            width=_get_arg(args, 1),
            height=_get_arg(args, 2),
            center_x=_get_arg(args, 3),
            center_y=_get_arg(args, 4),
            rotation=_get_arg(args, 5),
        )
    if code == 4:
        if len(args) < 2:
            return None
        # args[0]=exposure, args[1]=vertex_count (evaluated at parse time)
        # args[2..n-1]=vertex pairs, args[-1]=rotation
        exposure = args[0]
        vertices = args[2 : len(args) - 1]
        rotation = args[-1]
        return OutlinePrimitive(exposure=exposure, vertices=vertices, rotation=rotation)
    if code == 5:
        return PolygonPrimitive(
            exposure=_get_arg(args, 0, 1.0),
            num_vertices=_get_arg(args, 1, 4.0),
            center_x=_get_arg(args, 2),
            center_y=_get_arg(args, 3),
            diameter=_get_arg(args, 4),
            rotation=_get_arg(args, 5),
        )
    if code == 6:
        return MoirePrimitive(
            center_x=_get_arg(args, 0),
            center_y=_get_arg(args, 1),
            outer_diameter=_get_arg(args, 2),
            ring_thickness=_get_arg(args, 3),
            ring_gap=_get_arg(args, 4),
            max_rings=_get_arg(args, 5),
            crosshair_thickness=_get_arg(args, 6),
            crosshair_length=_get_arg(args, 7),
            rotation=_get_arg(args, 8),
        )
    if code == 7:
        return ThermalPrimitive(
            center_x=_get_arg(args, 0),
            center_y=_get_arg(args, 1),
            outer_diameter=_get_arg(args, 2),
            inner_diameter=_get_arg(args, 3),
            gap=_get_arg(args, 4),
            rotation=_get_arg(args, 5),
        )
    return None


# ---------------------------------------------------------------------------
# Public functions
# ---------------------------------------------------------------------------


def parse_macro_body(name: str, body: str) -> MacroDef:
    """Parse the body of an AM extended command block into a MacroDef.

    ``body`` is the raw content between the AMNAME* token and the closing %,
    with individual statements delimited by *.  Each statement is either:

    - An assignment:  ``$n=<expr>``
    - A primitive:    ``<code>,<param0>,<param1>,...``
    - A comment:      starts with ``0 `` or is the single character ``0``
    """
    items: list[MacroBodyItem] = []
    for stmt in (s.strip() for s in body.split("*")):
        if not stmt or stmt == "0" or stmt.startswith("0 "):
            continue  # skip comments
        if stmt.startswith("$"):
            eq = stmt.find("=")
            if eq > 0:
                var_idx = int(stmt[1:eq])
                expr = _parse_expr(stmt[eq + 1 :])
                items.append(AssignmentStatement(variable_index=var_idx, expression=expr))
            continue
        # Primitive statement: first argument is the primitive code (a literal integer)
        args = _parse_args(stmt)
        if not args:
            continue
        # Evaluate code with an empty var_map -- it must be a literal in practice
        code = round(evaluate_macro_expression(args[0], {}))
        prim = _build_primitive(code, args[1:])
        if prim is not None:
            items.append(prim)

    return MacroDef(name=name, body=items)


def evaluate_macro_expression(node: ExprNode, var_map: dict[int, float]) -> float:
    """Recursively evaluate a macro expression tree given a variable substitution map."""
    if isinstance(node, LiteralNode):
        return node.value
    if isinstance(node, VariableNode):
        return var_map.get(node.index, 0.0)
    if isinstance(node, UnaryNegNode):
        return -evaluate_macro_expression(node.operand, var_map)
    # BinaryNode
    lv = evaluate_macro_expression(node.left, var_map)
    rv = evaluate_macro_expression(node.right, var_map)
    if node.op == "+":
        return lv + rv
    if node.op == "-":
        return lv - rv
    if node.op == "x":
        return lv * rv
    if node.op == "/" and rv != 0.0:
        return lv / rv
    return 0.0


def _eval(node: ExprNode, vm: dict[int, float]) -> float:
    return evaluate_macro_expression(node, vm)


def evaluate_macro_primitives(
    macro_def: MacroDef,
    params: list[float],
) -> list[EvaluatedPrimitive]:
    """Evaluate all primitives in a macro definition with the given parameter list.

    ``params[0]`` maps to ``$1``, ``params[1]`` to ``$2``, etc.
    Assignment statements update the variable map in evaluation order.
    """
    var_map: dict[int, float] = {i + 1: v for i, v in enumerate(params)}
    result: list[EvaluatedPrimitive] = []

    for item in macro_def.body:
        if isinstance(item, AssignmentStatement):
            var_map[item.variable_index] = _eval(item.expression, var_map)
            continue

        ev: EvaluatedPrimitive | None = None

        if isinstance(item, CirclePrimitive):
            ev = EvaluatedCircle(
                exposure=_eval(item.exposure, var_map),
                diameter=_eval(item.diameter, var_map),
                center_x=_eval(item.center_x, var_map),
                center_y=_eval(item.center_y, var_map),
                rotation=_eval(item.rotation, var_map),
            )
        elif isinstance(item, LineVectorPrimitive):
            ev = EvaluatedLineVector(
                exposure=_eval(item.exposure, var_map),
                width=_eval(item.width, var_map),
                start_x=_eval(item.start_x, var_map),
                start_y=_eval(item.start_y, var_map),
                end_x=_eval(item.end_x, var_map),
                end_y=_eval(item.end_y, var_map),
                rotation=_eval(item.rotation, var_map),
            )
        elif isinstance(item, LineCenterPrimitive):
            ev = EvaluatedLineCenter(
                exposure=_eval(item.exposure, var_map),
                width=_eval(item.width, var_map),
                height=_eval(item.height, var_map),
                center_x=_eval(item.center_x, var_map),
                center_y=_eval(item.center_y, var_map),
                rotation=_eval(item.rotation, var_map),
            )
        elif isinstance(item, OutlinePrimitive):
            ev = EvaluatedOutline(
                exposure=_eval(item.exposure, var_map),
                vertices=[_eval(v, var_map) for v in item.vertices],
                rotation=_eval(item.rotation, var_map),
            )
        elif isinstance(item, PolygonPrimitive):
            ev = EvaluatedPolygon(
                exposure=_eval(item.exposure, var_map),
                num_vertices=round(_eval(item.num_vertices, var_map)),
                center_x=_eval(item.center_x, var_map),
                center_y=_eval(item.center_y, var_map),
                diameter=_eval(item.diameter, var_map),
                rotation=_eval(item.rotation, var_map),
            )
        elif isinstance(item, MoirePrimitive):
            ev = EvaluatedMoire(
                center_x=_eval(item.center_x, var_map),
                center_y=_eval(item.center_y, var_map),
                outer_diameter=_eval(item.outer_diameter, var_map),
                ring_thickness=_eval(item.ring_thickness, var_map),
                ring_gap=_eval(item.ring_gap, var_map),
                max_rings=round(_eval(item.max_rings, var_map)),
                crosshair_thickness=_eval(item.crosshair_thickness, var_map),
                crosshair_length=_eval(item.crosshair_length, var_map),
                rotation=_eval(item.rotation, var_map),
            )
        elif isinstance(item, ThermalPrimitive):
            ev = EvaluatedThermal(
                center_x=_eval(item.center_x, var_map),
                center_y=_eval(item.center_y, var_map),
                outer_diameter=_eval(item.outer_diameter, var_map),
                inner_diameter=_eval(item.inner_diameter, var_map),
                gap=_eval(item.gap, var_map),
                rotation=_eval(item.rotation, var_map),
            )

        if ev is not None:
            result.append(ev)

    return result
