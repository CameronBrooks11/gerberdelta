# Contributing

Thank you for your interest in contributing to **gerberdelta**!

## Development setup

Requires Python ≥ 3.11 and [uv](https://docs.astral.sh/uv/).

```sh
git clone https://github.com/CameronBrooks11/gerberdelta.git
cd gerberdelta
uv sync --dev
```

## Running the test suite

```sh
uv run pytest tests/ -q
```

With coverage:

```sh
uv run pytest tests/ --cov=gerberdelta --cov-report=term-missing
```

## Lint and type checking

```sh
uv run ruff check gerberdelta/ tests/
uv run ruff format gerberdelta/ tests/
uv run mypy gerberdelta/ tests/
```

All three must pass with no errors before a PR will be merged.  CI enforces this on every push.

## Commit messages

- Single sentence, imperative mood, no trailing period
- No phase or ticket prefix required (e.g. `Add viewport clamping for negative-Y boards`)

## Pull request checklist

- [ ] Tests added or updated for every changed behaviour
- [ ] `uv run ruff check` and `uv run mypy` pass locally
- [ ] `CHANGELOG.md` `[Unreleased]` section updated

## Versioning

This project follows [Semantic Versioning](https://semver.org/).  
The version is set in **both** `pyproject.toml` and `gerberdelta/__init__.py`; keep them in sync.

## License

By contributing you agree that your contributions will be licensed under the
[AGPL-3.0-only](LICENSE) licence.
