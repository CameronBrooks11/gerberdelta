# gerberdiff

[![CI](https://github.com/CameronBrooks11/gerberdiff/actions/workflows/ci.yml/badge.svg)](https://github.com/CameronBrooks11/gerberdiff/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/gerberdiff)](https://pypi.org/project/gerberdiff/)
[![Python](https://img.shields.io/pypi/pyversions/gerberdiff)](https://pypi.org/project/gerberdiff/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)

Visual raster diff tool for Gerber/Excellon PCB design files.

## Install

```sh
pip install gerberdiff
```

Requires Python >= 3.11.

## Quick start

```sh
# Compare two board revisions
gerberdiff diff before/ after/

# Write a JSON report and overlay PNGs
gerberdiff diff before/ after/ --out-json report.json --out-png diffs/

# Exit 1 if any changes detected (useful in CI)
gerberdiff diff before/ after/ --fail-on-diff
```

```python
import gerberdiff
from pathlib import Path

result = gerberdiff.compute_full_diff(Path("before/"), Path("after/"))
print(f"has_changes={result.has_changes}")
```

## Docs

| Topic              | File                                         |
| ------------------ | -------------------------------------------- |
| CLI reference      | [docs/cli.md](docs/cli.md)                   |
| Python API         | [docs/api.md](docs/api.md)                   |
| JSON report schema | [docs/schema.md](docs/schema.md)             |
| Architecture       | [docs/architecture.md](docs/architecture.md) |

## Known limitations

- **Excellon rout mode:** only drill hits are rendered; routing paths produce a
  `Warning` diagnostic but no geometry.
- **Deprecated RS-274X commands (`%MI%`, `%OF%`, `%SF%`, `%AS%`):** ignored with an
  `Info` diagnostic.
- **Rectangle/obround aperture strokes:** rendered using `max(width, height)` as an
  approximation (see [docs/geometry-diff.md](docs/geometry-diff.md)).

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md).
