from __future__ import annotations

import pytest

from gerberdiff.parse.macro_parser import (
    BinaryNode,
    EvaluatedCircle,
    EvaluatedLineVector,
    EvaluatedOutline,
    EvaluatedPolygon,
    LiteralNode,
    UnaryNegNode,
    VariableNode,
    evaluate_macro_expression,
    evaluate_macro_primitives,
    parse_macro_body,
)

# ---------------------------------------------------------------------------
# Expression evaluation
# ---------------------------------------------------------------------------


def test_literal_expression() -> None:
    assert evaluate_macro_expression(LiteralNode(value=3.14), {}) == pytest.approx(3.14)


def test_variable_expression() -> None:
    assert evaluate_macro_expression(VariableNode(index=1), {1: 2.5}) == pytest.approx(2.5)


def test_variable_missing_returns_zero() -> None:
    assert evaluate_macro_expression(VariableNode(index=99), {}) == pytest.approx(0.0)


def test_unary_neg() -> None:
    node = UnaryNegNode(operand=LiteralNode(value=5.0))
    assert evaluate_macro_expression(node, {}) == pytest.approx(-5.0)


def test_binary_add() -> None:
    node = BinaryNode(op="+", left=LiteralNode(value=1.0), right=LiteralNode(value=2.0))
    assert evaluate_macro_expression(node, {}) == pytest.approx(3.0)


def test_binary_subtract() -> None:
    node = BinaryNode(op="-", left=LiteralNode(value=5.0), right=LiteralNode(value=3.0))
    assert evaluate_macro_expression(node, {}) == pytest.approx(2.0)


def test_binary_multiply() -> None:
    node = BinaryNode(op="x", left=LiteralNode(value=3.0), right=LiteralNode(value=4.0))
    assert evaluate_macro_expression(node, {}) == pytest.approx(12.0)


def test_binary_divide() -> None:
    node = BinaryNode(op="/", left=LiteralNode(value=9.0), right=LiteralNode(value=3.0))
    assert evaluate_macro_expression(node, {}) == pytest.approx(3.0)


def test_binary_divide_by_zero() -> None:
    node = BinaryNode(op="/", left=LiteralNode(value=1.0), right=LiteralNode(value=0.0))
    assert evaluate_macro_expression(node, {}) == pytest.approx(0.0)


def test_nested_expression() -> None:
    # ($1 + 2) x 3 = (0.5 + 2) x 3 = 7.5
    inner = BinaryNode(op="+", left=VariableNode(index=1), right=LiteralNode(value=2.0))
    node = BinaryNode(op="x", left=inner, right=LiteralNode(value=3.0))
    assert evaluate_macro_expression(node, {1: 0.5}) == pytest.approx(7.5)


# ---------------------------------------------------------------------------
# parse_macro_body + evaluate_macro_primitives
# ---------------------------------------------------------------------------


def test_parse_circle_primitive() -> None:
    macro = parse_macro_body("TEST", "1,1,$1,0,0,0")
    assert len(macro.body) == 1
    prims = evaluate_macro_primitives(macro, [0.5])
    assert len(prims) == 1
    p = prims[0]
    assert isinstance(p, EvaluatedCircle)
    assert p.code == 1
    assert p.diameter == pytest.approx(0.5)
    assert p.exposure == pytest.approx(1.0)


def test_assignment_updates_variable() -> None:
    # $2 = $1 x 2, then circle with diameter=$2
    macro = parse_macro_body("TEST", "$2=$1x2*1,1,$2,0,0,0")
    prims = evaluate_macro_primitives(macro, [0.3])
    assert len(prims) == 1
    p = prims[0]
    assert isinstance(p, EvaluatedCircle)
    assert p.diameter == pytest.approx(0.6)


def test_parse_line_vector_primitive() -> None:
    macro = parse_macro_body("TEST", "20,1,0.1,0,0,1,0,0")
    prims = evaluate_macro_primitives(macro, [])
    assert len(prims) == 1
    p = prims[0]
    assert isinstance(p, EvaluatedLineVector)
    assert p.code == 20
    assert p.width == pytest.approx(0.1)
    assert p.end_x == pytest.approx(1.0)


def test_parse_polygon_primitive() -> None:
    macro = parse_macro_body("TEST", "5,1,6,0,0,0.5,0")
    prims = evaluate_macro_primitives(macro, [])
    p = prims[0]
    assert isinstance(p, EvaluatedPolygon)
    assert p.num_vertices == 6
    assert p.diameter == pytest.approx(0.5)


def test_parse_outline_primitive() -> None:
    # code 4: exposure, n_vertices, x0,y0, x1,y1, x2,y2, rotation
    macro = parse_macro_body("TEST", "4,1,3,0,0,1,0,0.5,1,0")
    prims = evaluate_macro_primitives(macro, [])
    p = prims[0]
    assert isinstance(p, EvaluatedOutline)
    assert p.exposure == pytest.approx(1.0)
    assert len(p.vertices) == 6  # 3 pairs


def test_comment_lines_skipped() -> None:
    # "0 this is a comment" should be skipped
    macro = parse_macro_body("TEST", "0 a comment*1,1,0.2,0,0,0")
    prims = evaluate_macro_primitives(macro, [])
    assert len(prims) == 1


def test_multiple_primitives() -> None:
    macro = parse_macro_body("TEST", "1,1,0.1,0,0,0*1,1,0.2,0,0,0")
    prims = evaluate_macro_primitives(macro, [])
    assert len(prims) == 2


def test_macrodef_name() -> None:
    macro = parse_macro_body("MYMACRO", "1,1,0.1,0,0,0")
    assert macro.name == "MYMACRO"


def test_expression_with_parentheses() -> None:
    # Primitive 1 with diameter = ($1 + $2) x 2
    macro = parse_macro_body("TEST", "1,1,($1+$2)x2,0,0,0")
    prims = evaluate_macro_primitives(macro, [0.1, 0.15])
    p = prims[0]
    assert isinstance(p, EvaluatedCircle)
    assert p.diameter == pytest.approx(0.5)  # (0.1+0.15)*2 = 0.5
