# Developer guide

How to set up a development environment, run the bridge locally, and use the project's tooling.
For branching, PR rules and code style, see [CONTRIBUTING.md](https://github.com/bio-tools/metadata-bridge/blob/dev/CONTRIBUTING.md).

## Set up

You need Python 3.12 or newer, `git`, and [Poetry](https://python-poetry.org/docs/#installation) (e.g. `pipx install poetry`).

```sh
git clone https://github.com/bio-tools/metadata-bridge.git
cd metadata-bridge
poetry install
poetry run pre-commit install --hook-type pre-commit --hook-type pre-push
cp .env.example .env  # then fill in your tokens
```

`poetry install` installs all dependency groups (runtime, dev and docs).
The pre-commit hooks run `fmt` before every commit and `lint` before every push.
See [Configuration](configuration.md) for what goes in `.env`;
run `bridge` from the project root so it finds the file.

## Run locally

```sh
poetry run bridge api         # API with auto-reload, Swagger UI at http://localhost:8000/docs
poetry run bridge cli --help  # CLI commands
```

## Tasks

Project tasks are [poethepoet](https://poethepoet.natn.io/) tasks: run them with `poetry run poe <task>`,
or `poetry run poe` to list them.

| Task                  | What it does                                                                                    |
|-----------------------|-------------------------------------------------------------------------------------------------|
| `fmt`                 | Fix imports, lint issues and formatting (Ruff + Black)                                          |
| `lint`                | Check linting and formatting without changing files (what CI runs)                              |
| `coverage-report`     | Run the tests with coverage, write an HTML report to `htmlcov/` and open it                     |
| `cosmic-ray-report`   | Run [Cosmic Ray](https://cosmic-ray.readthedocs.io/) mutation testing and write an HTML report |
| `gen-biotools-models` | Regenerate the Pydantic models from the bio.tools JSON Schema                                   |
| `gen-github-models`   | Regenerate the Pydantic models from GitHub's JSON response schemas                              |
| `gen-diagrams`        | Generate the architecture diagrams for the API reference (needs [D2](https://d2lang.com/))      |
| `gen-docs`            | Build the Sphinx docs into `docs/build`                                                         |

## Tests

```sh
poetry run pytest
```

The unit tests in `tests/unit` don't need a `.env` file or any tokens.

Mutation testing (`cosmic-ray-report`) makes small changes to the code and checks that some test fails for each one,
which shows where the tests don't really check behaviour. It reruns the test suite for every mutation, so it takes a while.
Locally it uses `cosmic-ray.local.toml`; with the `CI` environment variable set it uses `cosmic-ray.ci.toml`.

## Documentation

```sh
poetry run poe gen-diagrams
poetry run poe gen-docs
python -m http.server --directory docs/build  # then open http://localhost:8000
```

- Run `gen-diagrams` first, since the API reference includes the diagrams it generates.
- `gen-docs` treats Sphinx warnings as errors: it lists all of them, then fails, both locally and in CI.
  Most come from docstrings, for example a list without a blank line before it.
- The process diagrams are [Mermaid](https://mermaid.js.org/) files in `docs/source/api_reference/_process_diagrams/`.
  They render in the browser, so editing the `.mmd` file is all it takes.

## Dependencies

```sh
poetry add <package>               # runtime
poetry add --group dev <package>   # development
poetry add --group docs <package>  # documentation
```
