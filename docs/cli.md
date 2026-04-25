# CLI reference

## `parse` -- inspect a single file

```sh
gerberdelta parse board.gbr
gerberdelta parse board.gbr --dump-ir    # JSON summary to stdout
gerberdelta parse board.gbr --verbose    # include info-level diagnostics
```

## `render` -- rasterise a single file to PNG

```sh
gerberdelta render board.gbr --out-png board.png
gerberdelta render board.gbr --out-png board.png --width 4096 --height 4096
gerberdelta render board.gbr --out-png board.png --overwrite
```

## `diff` -- compare two layer directories

```sh
gerberdelta diff before/ after/
gerberdelta diff before/ after/ --fail-on-diff          # exit 1 if changes found
gerberdelta diff before/ after/ --out-json report.json
gerberdelta diff before/ after/ --out-png diff_pngs/
gerberdelta diff before/ after/ --layer F.Cu --verbose
gerberdelta diff before/ after/ --align-offset 0.5,0    # shift board B by 0.5 in
```

### Options

| Option                  | Default | Description                               |
| ----------------------- | ------- | ----------------------------------------- |
| `--width` / `--height`  | 2048    | Canvas size in pixels                     |
| `--min-pixels`          | 4       | Minimum pixel count for a reported region |
| `--merge-tolerance`     | 0.05    | Region merge padding in inches            |
| `--layer NAME`          | (all)   | Restrict to named layer (repeatable)      |
| `--out-json PATH`       | (none)  | Write JSON diff report                    |
| `--out-png DIR`         | (none)  | Write per-layer overlay PNGs              |
| `--overwrite`           | false   | Allow overwriting existing output files   |
| `--png-show-common`     | false   | Shade unchanged geometry grey in PNGs     |
| `--align-offset X,Y`    | 0,0     | Translate board B before diffing (inches) |
| `--fail-on-diff`        | false   | Exit 1 if any changes detected            |
| `--quiet` / `--verbose` | (none)  | Suppress or expand terminal output        |

### Overlay PNG colour scheme

| Colour | Meaning                                            |
| ------ | -------------------------------------------------- |
| Red    | Geometry present in **before** only (removed)      |
| Green  | Geometry present in **after** only (added)         |
| Yellow | Geometry changed (both non-zero, different value)  |
| Grey   | Unchanged geometry (only with `--png-show-common`) |
