# Codex CLI container

This project builds a small Debian-based container image containing the
[Codex CLI](https://github.com/openai/codex), along with common development
tools. It is intended to be used with Podman, keeping Codex credentials in a
named volume and mounting the current project only when Codex is run.

## Build the image

Build the image from this directory:

```sh
podman build -t codex-cli:latest -f codex.containerfile .
```

The container is configured for UID and GID `1000`. If your local user has
different IDs, pass matching build arguments and update the same values in
`init.sh` and `run.sh` before using them:

```sh
podman build \
  --build-arg CONTAINER_UID="$(id -u)" \
  --build-arg CONTAINER_GID="$(id -g)" \
  -t codex-cli:latest \
  -f codex.containerfile .
```

## Sign in to Codex

Make the helper executable if necessary, then run it:

```sh
chmod +x init.sh run.sh
./init.sh
```

The command starts Codex’s device-authentication flow. Follow the URL and
code printed in the terminal to sign in to your Codex account. Credentials are
stored in Podman’s `codex-home` named volume, so they remain available after
the temporary login container exits.

## Use Codex in a project

From the directory you want Codex to work in, invoke this repository’s run
script:

```sh
/path/to/this-repository/run.sh
```

Or, if this repository is also the project you want to work on:

```sh
./run.sh
```

`run.sh` bind-mounts the current directory at `/workspace` in the container
and starts an interactive Codex session there. Changes Codex makes to files in
`/workspace` are therefore written directly to your local project. The
container is removed when Codex exits; the `codex-home` volume retains your
login for future sessions.

To sign in again, rerun `./init.sh`.
