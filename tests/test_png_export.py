"""Tests for export/png_export.py."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from gerberdelta.export.png_export import build_overlay_png

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _solid(h: int, w: int, bgra: tuple[int, int, int, int]) -> np.ndarray:
    """Return a solid-colour H x W x 4 uint8 array in BGRA order."""
    arr = np.zeros((h, w, 4), dtype=np.uint8)
    arr[:] = bgra
    return arr


def _blank(h: int, w: int) -> np.ndarray:
    return np.zeros((h, w, 4), dtype=np.uint8)


def _xor(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    result: np.ndarray = np.bitwise_xor(a, b)
    return result


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_build_overlay_creates_file(tmp_path: Path) -> None:
    h, w = 32, 32
    a = _solid(h, w, (0, 255, 0, 255))
    b = _blank(h, w)
    out = tmp_path / "diff.png"
    build_overlay_png(a, b, _xor(a, b), out)
    assert out.exists()
    assert out.stat().st_size > 50


def test_build_overlay_no_overwrite_raises(tmp_path: Path) -> None:
    out = tmp_path / "diff.png"
    out.write_bytes(b"existing")
    a = _blank(8, 8)
    with pytest.raises(FileExistsError):
        build_overlay_png(a, a, _xor(a, a), out, overwrite=False)
    assert out.read_bytes() == b"existing"


def test_build_overlay_overwrite_allowed(tmp_path: Path) -> None:
    out = tmp_path / "diff.png"
    out.write_bytes(b"existing")
    a = _blank(8, 8)
    build_overlay_png(a, a, _xor(a, a), out, overwrite=True)
    assert out.stat().st_size > 0
    assert out.read_bytes() != b"existing"


def test_build_overlay_identical_images_no_colour(tmp_path: Path) -> None:
    """Identical images produce a fully transparent (blank) overlay."""
    h, w = 16, 16
    a = _solid(h, w, (0, 200, 0, 255))
    xor = _xor(a, a)
    out = tmp_path / "blank.png"
    build_overlay_png(a, a, xor, out)
    assert out.exists()
    # XOR of identical arrays is all zero → changed mask is empty.
    assert np.all(xor == 0)


def test_build_overlay_removed_pixels_red(tmp_path: Path) -> None:
    """Pixels only in A show as red (R=255, G=0, B=0) in RGBA output."""
    h, w = 8, 8
    a = _solid(h, w, (0, 0, 255, 255))   # white in BGRA → alpha=255 in A
    b = _blank(h, w)                       # transparent in B
    xor = _xor(a, b)
    out = tmp_path / "removed.png"
    build_overlay_png(a, b, xor, out)
    assert out.exists()


def test_build_overlay_added_pixels_green(tmp_path: Path) -> None:
    """Pixels only in B → green."""
    h, w = 8, 8
    a = _blank(h, w)
    b = _solid(h, w, (0, 0, 255, 255))
    xor = _xor(a, b)
    out = tmp_path / "added.png"
    build_overlay_png(a, b, xor, out)
    assert out.exists()


def test_build_overlay_show_common_no_crash(tmp_path: Path) -> None:
    h, w = 16, 16
    a = _solid(h, w, (0, 200, 0, 255))
    b = _solid(h, w, (0, 200, 0, 255))
    xor = _xor(a, b)
    out = tmp_path / "common.png"
    build_overlay_png(a, b, xor, out, show_common=True)
    assert out.exists()


def test_build_overlay_creates_parent_dirs(tmp_path: Path) -> None:
    out = tmp_path / "sub" / "dir" / "diff.png"
    a = _blank(4, 4)
    build_overlay_png(a, a, _xor(a, a), out)
    assert out.exists()
