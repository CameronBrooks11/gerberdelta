# Python API

All public symbols are importable from the root package.

## Parsing

```python
import gerberdiff

img = gerberdiff.parse_gerber(Path("board.gbr").read_text())
img = gerberdiff.parse_excellon(Path("board.drl").read_text())
```

Both return a `ParsedImage`. Diagnostics (warnings, errors) are in `img.diagnostics`.

## Rendering

```python
# Fit the board's bounding box into a pixel canvas
vp = gerberdiff.compute_viewport(img.bounding_box, width=1024, height=1024)

# Render to numpy array -- shape (H, W, 4) uint8 BGRA
arr = gerberdiff.render_to_numpy(img, vp)

# Render to a cairocffi ImageSurface (when Cairo drawing operations are needed)
surface = gerberdiff.render_to_surface(img, vp)
```

## Diffing

```python
# Single-layer diff (returns SingleLayerDiff)
before = gerberdiff.parse_gerber(Path("before/F.Cu.gbr").read_text())
after  = gerberdiff.parse_gerber(Path("after/F.Cu.gbr").read_text())
diff = gerberdiff.compute_diff(before, after, width=1024, height=1024)
print(f"{diff.changed_pixel_count} px changed, {len(diff.regions)} regions")

# Multi-layer directory diff (returns DiffResult)
result = gerberdiff.compute_full_diff(
    Path("before/"),
    Path("after/"),
    width=2048,
    height=2048,
    alignment_offset=None,   # optional (dx, dy) inches to shift the after image
    min_pixel_count=4,
    merge_tolerance=0.05,
)
print(f"has_changes={result.has_changes}")
for layer in result.layers:
    print(f"  {layer.name}: {layer.changed_pixel_count} px ({layer.status})")
```

`overlay_callback` on both `compute_diff` and `compute_full_diff` is an optional
`Callable[[np.ndarray, np.ndarray, np.ndarray], None]` invoked with
`(arr_before, arr_after, xor)` -- use it to write overlay PNGs without keeping all
three arrays in memory simultaneously.

## Public types

```python
from gerberdiff import (
    ParsedImage, BoundingBox, Viewport,
    DiffResult, LayerDiffResult, SingleLayerDiff, Region,
    LayerPair, LayerType, LayerStatus,
    Diagnostic, DiagnosticSeverity,
)
```

See `gerberdiff/types.py` for field-level documentation. Coordinate values are in
**inches** throughout. See [schema.md](schema.md) for the JSON report format.
