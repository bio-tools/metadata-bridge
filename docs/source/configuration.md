# Configuration

The bridge reads its settings from environment variables, or from a `.env` file in the directory you run it from.
To start, copy the example file and fill in your tokens:

```sh
cp .env.example .env
```

`.env` is git-ignored. Never commit it.

## Tokens

| Variable            | Needed for                                                                                         |
|---------------------|----------------------------------------------------------------------------------------------------|
| `GITHUB_TOKEN`      | Everything: reading repositories, and forking, pushing, and opening PRs and issues (bio.tools → GitHub) |
| `HUGGINGFACE_TOKEN` | Generating a description from the README when a repository has none (GitHub → bio.tools)         |

`GITHUB_TOKEN` must be a **classic** personal access token (starting with `ghp_`);
fine-grained tokens (`github_pat_...`) are rejected with "Invalid GitHub token format".
Give it the `public_repo` scope, or `repo` to work with private repositories
([create one](https://github.com/settings/tokens)).
The bridge forks repositories into the account that owns the token,
so for a shared service consider a dedicated bot account.

`HUGGINGFACE_TOKEN` must start with `hf_` and needs permission to call Inference Providers
([create one](https://huggingface.co/settings/tokens)).

## Other settings

- `LOG_LEVEL` is optional and defaults to `INFO`; `DEBUG` helps while developing.
- The service endpoints (`GITHUB_API_URL`, `BIOTOOLS_API_URL`, `EUROPE_PMC_API_URL`, ...) default to the public instances.
  Only change them to point the bridge at a different instance.

## Things to know

- A variable set in your shell takes precedence over the same variable in `.env`.
- Only use variable names from `.env.example`: an unknown key in `.env` makes the bridge fail at startup.
- Settings are read once at startup, and the API's auto-reload only watches Python files,
  so restart `bridge api` after editing `.env`.
- With Docker, pass the file with `--env-file .env` (see the [Deployment guide](deployment_guide.md#docker)).
