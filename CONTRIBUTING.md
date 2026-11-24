# Contributing guidelines

See the [Developer guide](https://bio-tools.github.io/metadata-bridge/dev_guide.html) for setup, running the API/CLI, tests and docs.

## Ground rules

- One clear purpose per PR: small, reviewable diffs
- No secrets in code: use env vars / `.env` locally; CI secrets are restricted
- Never edit auto-generated files by hand (see [Generated code](#generated-code))

## Branching & PRs

We keep two permanent branches and short-lived topic branches.

### Branch roles

| Branch | Purpose        | Rules                                                                                |
|--------|----------------|--------------------------------------------------------------------------------------|
| `main` | Release branch | Only merge from `dev` or `hotfix/*` (emergency). Tag release                         |
| `dev`  | Development    | All feature/bug PRs target dev. Keep green (working, buildable, test-passing state). |

### Topic branches

| Branch name       | Purpose     | Branch from | Merge into                                | Notes                                                                |
|-------------------|-------------|-------------|-------------------------------------------|----------------------------------------------------------------------|
| `feat/<slug>`     | Feature     | `dev`       | `dev`                                     | New features, enhancements                                           |
| `fix/<slug>`      | Bugfix      | `dev`       | `dev`                                     | Bug fixes, small changes                                             |
| `docs/<slug>`     | Docs        | `dev`       | `dev`                                     | Docs only updates                                                    |
| `chore/<slug>`    | Chore/Infra | `dev`       | `dev`                                     | Repo plumbing: tooling, CI/CD, dependencies, packaging, repo hygiene |
| `refactor/<slug>` | Refactor    | `dev`       | `dev`                                     | Code structure changes, no behavior changes                          |
| `test/<slug>`     | Tests       | `dev`       | `dev`                                     | Adding or updating tests                                             |
| `hotfix/<slug>`   | Hotfix      | `main`      | `main` and then back-merge `main` → `dev` | Emergency fixes                                                      |
| `exp/<slug>`      | Experiment  | `dev`       | `dev` or close                            | Prototypes, may be discarded                                         |

### Release flow

1. Bump the version with `poetry version <patch|minor|major>` and update `CHANGELOG.md` on `dev`.
2. Open a PR from `dev` to `main`; after review, merge it (squash or merge commit).
3. Tag `main` with `vX.Y.Z` and push the tag: the release workflow publishes to PyPI and creates the GitHub release.
4. Back-merge `main` into `dev`.

### Rebasing & merges

- Rebase topic branches on `dev` before opening/refreshing PRs.
- Use "Squash and merge" or "Merge commit" for PRs.

### PR checklist

- [ ] Rebased on latest `dev`
- [ ] Passes all pre-commit hooks (`poetry run poe fmt` and `poetry run poe lint`)
- [ ] Docs updated if needed
- [ ] Tests added/updated if needed
- [ ] Linked to an issue if applicable: Closes #ISSUE_NUMBER

## Code style

| Topic      | Standard                                        |
|------------|-------------------------------------------------|
| Python     | ≥ 3.12                                          |
| Lint       | Ruff (`ruff.toml`)                              |
| Format     | Black (`black.toml`, line length 120)           |
| Imports    | Ruff isort (first party = `bridge`)             |
| Docstrings | Required top-level docstring per package/module |
| Style      | NumPy                                           |
| Types      | Prefer precise hints                            |


## Generated code

| File                                                                           | Generated from                                                                                                                                                                                       | Regenerate with           |
|--------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------|
| `src/bridge/core/biotools.py`                                                  | The bio.tools JSON Schema                                                                                                                                                                            | `poe gen-biotools-models` |
| `src/bridge/core/github_repo.py`, `src/bridge/core/github_latest_release.py`   | GitHub's [repo](https://docs.github.com/en/rest/repos/repos#get-a-repository) and [latest release](https://docs.github.com/en/rest/releases/releases#get-the-latest-release) response schemas | `poe gen-github-models`   |

If a schema or generator changes, regenerate and commit the result.

## CI behavior

| Workflow                                 | Runs on                                        | Does                                                                                 |
|------------------------------------------|------------------------------------------------|--------------------------------------------------------------------------------------|
| Lint & unit tests (`tests.yml`)          | PRs, pushes to `dev`/`main`                    | `poe lint`, then `pytest` with coverage                                              |
| Build & Deploy Docs (`docs.yml`)         | PRs, pushes to `dev`/`main`, manual            | `poe gen-diagrams` + `poe gen-docs`; deploys to GitHub Pages only from the deploy branch |
| Release (`release.yml`)                  | `vX.Y.Z` tags                                  | Checks the tag matches `pyproject.toml`, builds, publishes to PyPI, creates a GitHub release |
| Dependabot                               | Weekly                                         | Grouped update PRs for Python dependencies and GitHub Actions, targeting `dev`       |

The docs deploy branch is the `DOCS_DEPLOY_BRANCH` repository variable
(Settings → Secrets and variables → Actions → Variables), defaulting to `dev`. PRs never deploy.
Publishing to PyPI uses trusted publishing through the `pypi` environment.
Don't commit built docs or diagrams.


## Design boundaries

| Layer       | Responsibility                                           | Examples                                                    |
|-------------|----------------------------------------------------------|-------------------------------------------------------------|
| `core`      | Pydantic domain models                                   | Data models for repos, schemas                              |
| `services`  | All interactions with external systems (APIs, git, LLMs) | API clients, ingestors, git wrappers, LLM interfaces        |
| `builders`  | Composition of models in `core` (using `services`)       | Transformers for building models from raw data              |
| `pipelines` | End-to-end flows for goals                              | Extracting metadata from a repo, suggesting file changes    |
| `adapters`  | CLI (typer) and API (fastapi) surfaces                   | Routers, commands, request models                           |
| `bootstrap` | Wiring and dependency injection                          | Registering composers for models, wiring goals to pipelines |
| `handlers`  | Orchestrators for (API/CLI) entrypoints for each goal    | Creating PRs, extracting metadata                           |


## Commit messages

Use clear, action-oriented subjects. Conventional commits encouraged.

| Good                                                  | Bad           |
|-------------------------------------------------------|---------------|
| `fix: handle 422 from GitHub PR API`                  | `fix stuff`   |
| `feat: add CLI command to extract metadata from repo` | `add code`    |
| `docs: update contributing guidelines`                | `update docs` |
