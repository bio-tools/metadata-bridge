# Installation

The bridge needs Python 3.12 or newer and `git` on the `PATH`
(it uses git to clone repositories and check wikis).

## From PyPI

```sh
pip install metadata-bridge
```

or, to keep it isolated from other tools:

```sh
pipx install metadata-bridge
```

Check it works:

```sh
bridge --version
bridge --help
```

Then set up your tokens as described in [Configuration](configuration.md).

## With Docker

See the [Deployment guide](deployment_guide.md#docker).

## From source

To work on the bridge itself, follow the [Developer guide](dev_guide.md).
