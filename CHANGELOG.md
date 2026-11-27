# Changelog

All notable changes to this project are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `bridge --version` and a version on the API's OpenAPI schema.
- Release workflow publishing to PyPI on `vX.Y.Z` tags, plus Dependabot.
- Dockerfile for running the API, a deployment guide, an installation page and a user guide.
- `bridge api --no-reload` to turn off hot reload.
- User guide sections on using the bridge from Python and on which fields get mapped in each direction.
- `.env` setup instructions in the developer guide, and the changelog in the docs.

### Changed
- Moved from `bio-tools/biohackathon2025` to `bio-tools/metadata-bridge`; the package is published as `metadata-bridge`.
- Dev helpers (`lint`, `fmt`, `gen-*`, ...) are now poe tasks: `poetry run poe <task>`.
- The "bridge" README badge links to the new docs site; old badges are replaced instead of duplicated.
- Docs are only deployed from the deploy branch (`DOCS_DEPLOY_BRANCH`, default `dev`); PRs just build them.
- `pydantic`, `pyyaml` and `packaging` are declared as dependencies; unused `requests` is dropped.
- The docs build fails on Sphinx warnings instead of hiding them.
- Per-field mapping diagrams were removed from the docs; the general process diagrams remain.
- The unused `gen-process-diagrams` task was removed (Mermaid diagrams render in the browser).

### Fixed
- Badge logos are bundled in the package, so they work when installed from PyPI.
- The API reference shows the real signatures and docstrings of `extract_meta_from_repo` and `create_pr_issues_from_meta`.
- Docstring formatting errors and missing links in the developer API reference.

## 0.1.0

Initial version developed during the ELIXIR BioHackathon Europe 2025 (project 5).
