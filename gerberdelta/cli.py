from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import click

from gerberdelta import __version__
from gerberdelta.types import DiagnosticSeverity

_EXCELLON_SUFFIXES = frozenset({".drl", ".exc", ".xln", ".ncd"})
_MEMORY_WARN_PIXELS = 16_777_216  # 4096²


@click.group()
@click.version_option(__version__, prog_name="gerberdelta")
def cli() -> None:
    """Geometry-aware Gerber/Excellon diff tool."""


@cli.command("parse")
@click.argument("file", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--dump-ir", is_flag=True, help="Print ParsedImage summary as JSON to stdout.")
@click.option("-q", "--quiet", is_flag=True, help="Suppress all output except errors.")
@click.option("-v", "--verbose", is_flag=True, help="Print Info-level diagnostics.")
def parse_cmd(file: Path, dump_ir: bool, quiet: bool, verbose: bool) -> None:
    """Parse a Gerber or Excellon file and report diagnostics."""
    from gerberdelta.parse.excellon_parser import parse_excellon
    from gerberdelta.parse.gerber_state import parse_gerber

    try:
        content = file.read_text(errors="replace")
    except OSError as exc:
        click.echo(f"error: {exc}", err=True)
        sys.exit(1)

    if file.suffix.lower() in _EXCELLON_SUFFIXES:
        img = parse_excellon(content, source_path=file)
    else:
        img = parse_gerber(content, source_path=file)

    has_errors = False
    for diag in img.diagnostics:
        loc = f" (line {diag.line})" if diag.line else ""
        if diag.severity == DiagnosticSeverity.Error:
            has_errors = True
            click.echo(f"error: {diag.message}{loc}", err=True)
        elif diag.severity == DiagnosticSeverity.Warning and not quiet:
            click.echo(f"warning: {diag.message}{loc}", err=True)
        elif diag.severity == DiagnosticSeverity.Info and verbose:
            click.echo(f"info: {diag.message}", err=True)

    if not quiet and not dump_ir:
        click.echo(f"nets: {len(img.nets)}")
        click.echo(f"apertures: {len(img.apertures)}")
        if img.bounding_box.is_valid:
            bb = img.bounding_box
            click.echo(
                f"bbox: x=[{bb.min_x:.6f}, {bb.max_x:.6f}]"
                f" y=[{bb.min_y:.6f}, {bb.max_y:.6f}] inches"
            )
        else:
            click.echo("bbox: empty (no geometry)")

    if dump_ir:
        bb = img.bounding_box
        ir: dict[str, object] = {
            "source": str(file),
            "net_count": len(img.nets),
            "aperture_count": len(img.apertures),
            "layer_count": len(img.layers),
            "bounding_box": {
                "min_x": bb.min_x if bb.is_valid else None,
                "min_y": bb.min_y if bb.is_valid else None,
                "max_x": bb.max_x if bb.is_valid else None,
                "max_y": bb.max_y if bb.is_valid else None,
            },
            "diagnostics": [
                {"severity": d.severity.value, "message": d.message, "line": d.line}
                for d in img.diagnostics
            ],
        }
        click.echo(json.dumps(ir, indent=2))

    sys.exit(2 if has_errors else 0)


@cli.command("render")
@click.argument("file", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option(
    "--out-png",
    required=True,
    type=click.Path(dir_okay=False, path_type=Path),
    help="Output PNG path.",
)
@click.option("--width", default=2048, show_default=True, help="Canvas width in pixels.")
@click.option("--height", default=2048, show_default=True, help="Canvas height in pixels.")
@click.option("--overwrite", is_flag=True, help="Overwrite output file if it already exists.")
@click.option("-q", "--quiet", is_flag=True, help="Suppress all output except errors.")
@click.option("-v", "--verbose", is_flag=True, help="Print render timing and diagnostic detail.")
def render_cmd(
    file: Path,
    out_png: Path,
    width: int,
    height: int,
    overwrite: bool,
    quiet: bool,
    verbose: bool,
) -> None:
    """Render a Gerber or Excellon file to a PNG image."""
    from gerberdelta.parse.excellon_parser import parse_excellon
    from gerberdelta.parse.gerber_state import parse_gerber
    from gerberdelta.render.renderer import render_to_surface
    from gerberdelta.render.viewport import compute_viewport

    # Memory warning — non-blocking.
    total_pixels = width * height
    if total_pixels > _MEMORY_WARN_PIXELS:
        mb = (total_pixels * 4) / (1024 * 1024)
        click.echo(
            f"warning: canvas {width}x{height} = {total_pixels:,} pixels "
            f"(~{mb:.0f} MB); reduce --width/--height if memory is limited.",
            err=True,
        )

    if out_png.exists() and not overwrite:
        click.echo(
            f"error: output file already exists: {out_png}  (use --overwrite to replace)",
            err=True,
        )
        sys.exit(1)

    try:
        content = file.read_text(errors="replace")
    except OSError as exc:
        click.echo(f"error: {exc}", err=True)
        sys.exit(1)

    if file.suffix.lower() in _EXCELLON_SUFFIXES:
        img = parse_excellon(content, source_path=file)
    else:
        img = parse_gerber(content, source_path=file)

    has_errors = False
    for diag in img.diagnostics:
        loc = f" (line {diag.line})" if diag.line else ""
        if diag.severity == DiagnosticSeverity.Error:
            has_errors = True
            click.echo(f"error: {diag.message}{loc}", err=True)
        elif diag.severity == DiagnosticSeverity.Warning and not quiet:
            click.echo(f"warning: {diag.message}{loc}", err=True)
        elif diag.severity == DiagnosticSeverity.Info and verbose:
            click.echo(f"info: {diag.message}", err=True)

    if has_errors:
        sys.exit(2)

    vp = compute_viewport(img.bounding_box, width, height)

    t0 = time.perf_counter()
    surface = render_to_surface(img, vp)
    elapsed = time.perf_counter() - t0

    try:
        out_png.parent.mkdir(parents=True, exist_ok=True)
        surface.write_to_png(str(out_png))
    except OSError as exc:
        click.echo(f"error: {exc}", err=True)
        sys.exit(1)

    if not quiet:
        click.echo(f"rendered {width}x{height} → {out_png}")
    if verbose:
        click.echo(f"render time: {elapsed * 1000:.1f} ms")
        click.echo(f"nets: {len(img.nets)}  apertures: {len(img.apertures)}")


if __name__ == "__main__":
    cli()
