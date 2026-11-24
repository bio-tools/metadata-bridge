# User guide

The bridge works in two directions:

- **GitHub → bio.tools**: extract bio.tools metadata (JSON) from a GitHub repository,
  optionally merged with an existing bio.tools entry.
- **bio.tools → GitHub**: propose improvements to a GitHub repository based on its bio.tools entry,
  as a pull request (README badges, description, citation, license, topics, ...) and optionally issues.

See [Installation](install.md) to get the `bridge` command, and set at least `GITHUB_TOKEN`
(environment variable or `.env` file, see `.env.example`).
Generating descriptions from READMEs with an LLM also needs `HUGGINGFACE_TOKEN`.

## Command line

### GitHub → bio.tools

```bash
bridge cli github-to-biotools extract OWNER REPO [--biotools-id ID]
```

Prints the extracted bio.tools metadata as JSON.
Pass `--biotools-id` when the tool already has a bio.tools entry, so the existing record is used as the base.

### bio.tools → GitHub

```bash
bridge cli biotools-to-github update BIOTOOLS_ID OWNER REPO [--allow-issues | --no-allow-issues]
```

Forks `OWNER/REPO` into the account that owns `GITHUB_TOKEN` (or reuses an existing fork),
commits the proposed changes on a new branch and opens a pull request against the original repository.
With `--allow-issues`, suggestions that can't be expressed as file changes are opened as issues.

## REST API

Start the API with `bridge api` (see the [Deployment guide](deployment_guide.md) for running it as a service).
The interactive docs are at `/docs`.

| Endpoint                   | Body                                                     | Does                         |
|----------------------------|----------------------------------------------------------|------------------------------|
| `POST /github-to-biotools` | `{"owner", "repo", "biotools_id"?}`                      | Returns bio.tools metadata   |
| `POST /biotools-to-github` | `{"biotools_id", "owner", "repo", "allow_issues"?}`      | Opens a PR (and issues)      |

Example:

```bash
curl -X POST http://localhost:8000/github-to-biotools \
  -H "Content-Type: application/json" \
  -d '{"owner": "bio-tools", "repo": "metadata-bridge"}'
```

## Python

The same operations are available from Python.
Both functions are async, take the metadata schema and repository type,
and the rest as keyword arguments:

```python
import asyncio

from bridge import create_pr_issues_from_meta, extract_meta_from_repo

# GitHub → bio.tools: returns the bio.tools metadata as a JSON string
metadata_json = asyncio.run(
    extract_meta_from_repo(
        schema="biotools",
        repo_type="github",
        owner="OWNER",
        repo="REPO",
        identifier=None,  # or an existing bio.tools ID
    )
)

# bio.tools → GitHub: returns {"pr": {...}, "issues": [...]} for whatever was created
result = asyncio.run(
    create_pr_issues_from_meta(
        schema="biotools",
        repo_type="github",
        identifier="BIOTOOLS_ID",
        owner="OWNER",
        repo="REPO",
        allow_issues=True,
    )
)
```

See the [API reference](api_reference/index_user) for the full signatures.

## What gets mapped

### GitHub → bio.tools

| bio.tools field  | Taken from GitHub                                                                       |
|------------------|-----------------------------------------------------------------------------------------|
| `biotoolsID`     | Repository name, adjusted to be unique on bio.tools                                     |
| `name`           | Repository name                                                                         |
| `description`    | Repository description, or generated from the README with an LLM when there is none     |
| `homepage`       | Repository homepage, falling back to the repository URL                                 |
| `link`           | Repository URL                                                                          |
| `documentation`  | Wiki, GitHub Pages and code of conduct                                                  |
| `language`       | Repository languages                                                                    |
| `license`        | Detected license                                                                        |
| `version`        | Latest release tag                                                                      |
| `maturity`       | Archived status, stars, forks and watchers                                              |
| `publication`    | References in `CITATION.cff`                                                            |
| `topic`          | Repository topics, matched to EDAM topics                                               |
| `function`       | Function annotations in the README                                                      |

When you pass an existing bio.tools ID, its record is the starting point,
and values already in bio.tools are kept wherever GitHub has nothing to add.

### bio.tools → GitHub

Changes that can be made as files are proposed in **one pull request**:

| File           | What changes                                                                         |
|----------------|--------------------------------------------------------------------------------------|
| `README.md`    | Adds bio.tools, bridge and tool-type badges; the rest of the README is kept as is    |
| `CITATION.cff` | Created or extended from the bio.tools publications                                  |
| `LICENSE.txt`  | The full SPDX text of the bio.tools license, when GitHub has none or a different one |

Other differences are opened as **issues** instead (only with `--allow-issues`),
since most of them are repository settings that a pull request can't change:
name, description, homepage, topics (from EDAM topics and operations), version (release tags)
and function annotations in the README.
