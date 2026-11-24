# Developer guide

This guide explains how to set up a local development environment for bridge, 
run the CLI/API, and maintain code quality using the existing tooling.


## Prepare your environment

You need Python 3.12 (or higher) and Poetry.
If you don't have Poetry installed, you can install it by following the [instructions](https://python-poetry.org/docs/#installation)
or by running the following command:

```sh
pipx install poetry
```

Clone the repository and enter the project directory:

```sh
git clone https://github.com/bio-tools/metadata-bridge.git
cd metadata-bridge
```

## Install dependencies

Create and activate the virtual environment:

```sh
poetry install
```

Or install only specific groups:

```bash
poetry install --with dev  # install development dependencies
poetry install --with docs  # install documentation dependencies
```

## Enable pre-commit hooks

Pre-commit is installed automatically with the development dependencies.
To activate hooks in your local clone:

```bash
poetry install --with dev
poetry run pre-commit install --hook-type pre-commit --hook-type pre-push
```

What happens automatically:

| hook | stage      | description                                                              |
|------|------------|--------------------------------------------------------------------------|
| fmt  | pre-commit | Automatically fixes imports, formatting, and lint issues (Ruff + Black)  |
| lint | pre-push   | Checks that the codebase is clean and properly formatted before pushing. |

You can also run the same checks manually (very much encouraged):

```bash
poetry run poe [hook]
```

## Set up your `.env` file

The bridge reads its configuration from environment variables, or from a `.env` file in the directory you run it from.
Copy the example file in the project root and fill in your tokens:

```sh
cp .env.example .env
```

`.env` is git-ignored, so your tokens stay local. Never commit it.

| Variable            | Needed for                                                                                       | Where to get it                                                                                                                                                                  |
|---------------------|--------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `GITHUB_TOKEN`      | Calling the GitHub API, and forking, pushing, and opening PRs and issues (bio.tools → GitHub)   | A **classic** personal access token (it must start with `ghp_`) with the `public_repo` scope, or `repo` for private repositories: [create one](https://github.com/settings/tokens) |
| `HUGGINGFACE_TOKEN` | Generating a description from the README with an LLM when a repository has none (GitHub → bio.tools) | A token (it must start with `hf_`) with permission to call Inference Providers: [create one](https://huggingface.co/settings/tokens)                                             |
| `LOG_LEVEL`         | Optional, defaults to `INFO` (`DEBUG` is useful while developing)                                 |                                                                                                                                                                                  |

The remaining variables (`GITHUB_API_URL`, `BIOTOOLS_API_URL`, `EUROPE_PMC_API_URL`, ...) are service endpoints.
They default to the public instances and only need changing if you point the bridge at a different one,
so you can leave them as they are in `.env.example`.

A few things to know:

- Run `bridge` from the project root, so it finds `.env`.
  A variable that is set in your shell takes precedence over the same variable in `.env`.
- Only use variable names from `.env.example`.
  An unknown key in `.env` makes the bridge fail at startup with a validation error.
- Settings are read once at startup, and the API's auto-reload only watches Python files,
  so restart `bridge api` after editing `.env`.
- The unit tests don't need a `.env` file or any tokens.

## Run locally

Before running the API or CLI, set up your `.env` file as described above.

### API

To run the API server with auto-reload:

```sh
poetry run bridge api
```
You can access the Swagger UI at [localhost:8000/docs](http://localhost:8000/docs).

### CLI

To see available commands:

```sh
poetry run bridge cli --help
```

### Helper scripts

Various helper scripts are available under the `scripts/` directory.

| script                | description                                                |
|-----------------------|------------------------------------------------------------|
| `gen-biotools-models` | Generate Pydantic models from the bio.tools JSON Schema    |
| `gen-github-models`   | Generate Pydantic models from GitHub JSON response schemas |

You can run them using Poetry:

```bash
poetry run poe [script]
```

Run `poetry run poe` without arguments to list every available task.

## Documentation

There are two scripts relevant to documentation generation:

| script                | description                                              |
|-----------------------|----------------------------------------------------------|
| `gen-diagrams`        | Generate architecture diagrams used by the documentation |
| `gen-docs`            | Generate Sphinx documentation                            |

You can run them using Poetry:

```bash
poetry run poe [script]
```

The `gen-diagrams` script requires [D2](https://d2lang.com/) to be installed. 
You can install it by following their [instructions](https://github.com/terrastruct/d2/blob/master/docs/INSTALL.md).

To view the documentation locally, run:

```bash
open docs/build/index.html  # on macOS
python -m http.server --directory docs/build  # any OS
```

If you run the latter command, you can access the documentation at [localhost:8000](http://localhost:8000).


## Dependencies

We use Poetry to manage dependencies.

Add runtime dependencies with:

```bash
poetry add [package]
```

Add development dependencies with:

```bash
poetry add --group dev [package]
```

Add documentation dependencies with:

```bash
poetry add --group docs [package]
```

## Contributing guidelines

Please refer to the [CONTRIBUTING.md](https://github.com/bio-tools/metadata-bridge/blob/dev/CONTRIBUTING.md) file for guidelines on contributing to this project.
