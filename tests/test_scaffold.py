"""Smoke tests for package import and CLI wiring."""

from __future__ import annotations


def test_version_string_is_defined() -> None:
    import gerberdiff

    assert hasattr(gerberdiff, "__version__")
    assert isinstance(gerberdiff.__version__, str)
    # Check semver shape -- don't hardcode the exact version
    parts = gerberdiff.__version__.split(".")
    assert len(parts) == 3, "version must be MAJOR.MINOR.PATCH"


def test_cli_group_importable() -> None:
    from gerberdiff.cli import cli

    assert callable(cli)
