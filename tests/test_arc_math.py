from __future__ import annotations

import math

from gerberdelta.parse.arc_math import compute_arc_multi_quadrant, compute_arc_single_quadrant


def test_multi_quadrant_quarter_circle_ccw() -> None:
    # Arc from (1,0) to (0,1) CCW; center (0,0): I=-1, J=0
    arc = compute_arc_multi_quadrant(1.0, 0.0, 0.0, 1.0, -1.0, 0.0, clockwise=False)
    assert arc is not None
    assert abs(arc.center_x) < 1e-9
    assert abs(arc.center_y) < 1e-9
    assert abs(arc.radius - 1.0) < 1e-9
    assert abs(arc.start_angle_deg - 0.0) < 1e-6
    assert abs(arc.end_angle_deg - 90.0) < 1e-6


def test_multi_quadrant_quarter_circle_cw() -> None:
    # Arc from (0,1) to (1,0) CW; center (0,0): I=0, J=-1
    arc = compute_arc_multi_quadrant(0.0, 1.0, 1.0, 0.0, 0.0, -1.0, clockwise=True)
    assert arc is not None
    assert abs(arc.radius - 1.0) < 1e-9
    # CW: end_angle < start_angle
    assert arc.end_angle_deg < arc.start_angle_deg


def test_multi_quadrant_full_circle_ccw() -> None:
    # start == end, non-zero I → full 360° arc
    arc = compute_arc_multi_quadrant(1.0, 0.0, 1.0, 0.0, -1.0, 0.0, clockwise=False)
    assert arc is not None
    assert abs(arc.end_angle_deg - arc.start_angle_deg - 360.0) < 1e-6


def test_multi_quadrant_full_circle_cw() -> None:
    arc = compute_arc_multi_quadrant(1.0, 0.0, 1.0, 0.0, -1.0, 0.0, clockwise=True)
    assert arc is not None
    assert abs(arc.start_angle_deg - arc.end_angle_deg - 360.0) < 1e-6


def test_multi_quadrant_degenerate_returns_none() -> None:
    # i=j=0 → radius 0 → degenerate
    arc = compute_arc_multi_quadrant(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, clockwise=False)
    assert arc is None


def test_multi_quadrant_radius_consistency() -> None:
    # Both start and end should be on the circle
    arc = compute_arc_multi_quadrant(2.0, 0.0, 0.0, 2.0, -2.0, 0.0, clockwise=False)
    assert arc is not None
    r_start = math.hypot(2.0 - arc.center_x, 0.0 - arc.center_y)
    r_end = math.hypot(0.0 - arc.center_x, 2.0 - arc.center_y)
    assert abs(r_start - arc.radius) < 1e-9
    assert abs(r_end - arc.radius) < 1e-9


def test_single_quadrant_quarter_circle() -> None:
    # Same geometry as multi-quadrant test: pick i=1,j=0 gives center (-1+1=0, 0+0=0) hmm
    # Arc from (1,0) to (0,1) CCW; abs_i=1, abs_j=0
    arc = compute_arc_single_quadrant(1.0, 0.0, 0.0, 1.0, 1.0, 0.0, clockwise=False)
    assert arc is not None
    assert abs(arc.radius - 1.0) < 1e-9
    # sweep should be ≤ 90°
    sweep = arc.end_angle_deg - arc.start_angle_deg
    assert 0.0 < sweep <= 90.5


def test_single_quadrant_degenerate_returns_none() -> None:
    arc = compute_arc_single_quadrant(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, clockwise=False)
    assert arc is None
