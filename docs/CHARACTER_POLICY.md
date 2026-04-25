# Character usage policy

All source files in this repository must be pure ASCII (codepoints U+0000--U+007F).
This covers Python source, tests, TOML, YAML, Markdown, and any other text file
tracked by git.

## Rationale

Non-ASCII characters in source code and documentation cause silent encoding
failures across editors, terminals, diff tools, and CI environments that default
to a non-UTF-8 locale. They are invisible in many fonts, indistinguishable from
lookalike ASCII, and meaningless to grep. The maintenance cost is zero benefit.

## Banned characters and their replacements

| Character         | Codepoint | Replacement |
| ----------------- | --------- | ----------- |
| em dash           | U+2014    | `--`        |
| en dash           | U+2013    | `-`         |
| ellipsis          | U+2026    | `...`       |
| right arrow       | U+2192    | `->`        |
| left arrow        | U+2190    | `<-`        |
| multiplication    | U+00D7    | `x`         |
| minus sign        | U+2212    | `-`         |
| greater-or-equal  | U+2265    | `>=`        |
| less-or-equal     | U+2264    | `<=`        |
| almost-equal      | U+2248    | `~=`        |
| plus-minus        | U+00B1    | `+/-`       |
| degree            | U+00B0    | `deg`       |
| superscript 2     | U+00B2    | `^2`        |
| e-acute           | U+00E9    | `e`         |
| box-drawing chars | U+2500+   | `-`, `|`, `+` |

## Enforcement

Run the scanner before committing:

```sh
python scripts/scan_unicode.py        # report only
python scripts/scan_unicode.py --fix  # apply known substitutions
```

The scanner operates on all files returned by `git ls-files`, skipping binary
extensions (`.gbr`, `.drl`, `.png`, `.lock`, etc.) and untracked paths.

Substitutions that cannot be auto-fixed (codepoint not in the table) are reported
as `MANUAL` items and cause the script to exit with code 1. Resolve them by hand
before committing.
