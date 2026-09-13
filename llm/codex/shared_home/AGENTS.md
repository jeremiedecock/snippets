# AGENTS.md

This file provides guidance to coding agents (Codex CLI, Claude Code, Gemini CLI, …) when working with code in this repository.

## What this repository is

This repository packages the Codex CLI into a rootless Podman container. It consists mainly of three helper scripts, one Containerfile, and a small Neovim configuration. There is no application code, no test suite, and no build system beyond `podman build`.

The packaged CLI is the *subject* of this repository, not necessarily the agent reading this file. If you are an agent running via `run.sh`, you are executing **inside the very image defined here**: editing `codex.containerfile` changes nothing for the current session — the image must be rebuilt and a new container started to take effect.

## Commands

```sh
./build.sh                   # build localhost/codex-cli:latest
./init.sh                    # authenticate Codex and persist credentials
./run.sh [codex args...]     # run Codex with $PWD mounted at /workspace
```

`run.sh` does not parse repository-specific options; it forwards every argument verbatim to `codex`. `init.sh` starts Codex's device-authentication flow. Both scripts force `cli_auth_credentials_store="file"` because the container does not expose a host keychain.

## How the pieces fit together

**State persistence.** `init.sh` and `run.sh` mount the `codex-home` named Podman volume at `/home/user/.codex`. This persists the file-based credentials created by `codex login --device-auth`, along with Codex configuration, skills, and session data. The containers use `--rm`, so anything written outside that volume or the `/workspace` bind mount is lost when the container exits.

**Workspace mounting.** `run.sh` bind-mounts the invoking directory (`.`) at `/workspace`, which is also the image's working directory. The script is therefore intended to be invoked from the project that Codex should edit; invoking this repository's copy directly makes this repository the workspace.

**UID/GID alignment.** Both runtime scripts use `--userns=keep-id:uid=1000,gid=1000`, mapping the invoking host user onto container UID/GID 1000 so files created in `/workspace` remain owned by the host user. The `CONTAINER_UID`/`CONTAINER_GID` values in `init.sh` and `run.sh` must match the `ARG` defaults in `codex.containerfile`; changing only one side can break write access to the workspace or state volume.

**CLI installation and updates.** `codex.containerfile` installs the unversioned `@openai/codex` npm package in its final image layer and verifies it with `codex --version`. Podman may reuse that layer during an ordinary rebuild. There is currently no `build.sh --update` option or cache-busting argument; changing update behavior requires keeping `build.sh` and the final Containerfile layer consistent.

**Editor configuration.** `VISUAL` and `EDITOR` are set to `nvim`. The image copies `nvim/init.lua` into the non-root user's configuration and builds a French Neovim spell file from Debian's Hunspell dictionary.

## Conventions

- `init.sh` and `run.sh` use `/bin/bash`; `build.sh` is a minimal `/bin/sh` wrapper. Preserve the existing shell choice unless a script gains features that require Bash.
- Keep the image deliberately small (`debian:stable-slim`, `--no-install-recommends`). Runtime tooling currently includes `curl`, `gh`, `git`, `hunspell-fr-classical`, `make`, `neovim`, `npm`, `pipx`, `python3-pip`, and `ripgrep`. Add packages only when they are actually needed inside the container.
- Keep the container running as the non-root `user`. Create new mount points before the `USER user` switch and give them the correct ownership.
- Keep `CONTAINER_UID` and `CONTAINER_GID` synchronized across `codex.containerfile`, `init.sh`, and `run.sh`.
- Preserve the separation between authentication (`init.sh`) and normal interactive use (`run.sh`).
- Do not assume an image rebuild changes the currently running container; validate image-level changes only after rebuilding and starting a fresh container.

## Agent instruction files

`AGENTS.md` is the single source of truth and is the filename Codex reads natively. Edit this file directly. If another agent requires a tool-specific filename (for example `CLAUDE.md` or `GEMINI.md`), add a symlink to `AGENTS.md` rather than copying its contents.
