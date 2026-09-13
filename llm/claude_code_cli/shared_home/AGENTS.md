# AGENTS.md

This file provides guidance to coding agents (Claude Code, Codex CLI, Gemini CLI, …) when working with code in this repository.

## What this repository is

Three shell/container files that package the Claude Code CLI into a rootless Podman container. There is no application code, no test suite, and no build system beyond `podman build`.

Note that the packaged CLI is the *subject* of this repository, not necessarily the agent reading this file. If you are an agent running via `run.sh`, you are executing **inside the very image defined here**: editing `claude.containerfile` changes nothing for the current session — the image must be rebuilt and a new container started to take effect.

## Commands

```sh
./build.sh                                   # podman build -t claude-code-cli:latest
./build.sh --update                          # same, but force the Claude Code CLI layer to re-run
./run.sh [claude args...]                    # run the CLI with $PWD bind-mounted at /workspace
./run.sh --claude-volume-name my-vol [args]  # use a different state volume (must precede claude args)
```

`run.sh` parses only `--claude-volume-name` (both `--opt value` and `--opt=value` forms) and stops at the first unrecognized argument, forwarding the rest verbatim to `claude`.

## How the pieces fit together

**State persistence.** All CLI state (OAuth token in `.credentials.json`, `.claude.json`, settings, history) is consolidated under a single directory via `CLAUDE_CONFIG_DIR=/home/user/.claude`, which `run.sh` backs with a named Podman volume (`claude-home` by default). The container is `--rm`, so anything written outside that volume or outside the `/workspace` bind mount is lost on exit.

**UID/GID alignment.** `run.sh`'s `--userns=keep-id:uid=1000,gid=1000` maps the invoking host user onto container UID/GID 1000, so files created in the bind-mounted `/workspace` stay owned by the host user. The `CONTAINER_UID`/`CONTAINER_GID` values in `run.sh` must match the `ARG` defaults in `claude.containerfile`; changing one without the other breaks write access to both `/workspace` and the state volume.

**CLI version pinning.** `DISABLE_AUTOUPDATER=1` — the CLI version is fixed by the image, since in-container auto-updates would vanish with the container. Updating the CLI means re-running the `curl … install.sh` layer, which is why it sits last and is gated by `ARG CACHEBUST`: passing a new value invalidates only that layer, leaving the apt layer cached. `./build.sh` passes `CACHEBUST=0` so ordinary rebuilds reuse the cached CLI; `./build.sh --update` passes the current timestamp to pull a newer CLI release. Updating the CLI is therefore always an explicit request, never a side effect of rebuilding.

## Conventions

- Both `build.sh` and `run.sh` are `/bin/bash` and use bash idioms (`[[ ]]`); keep new scripts on bash rather than reintroducing a `/bin/sh` variant.
- The image stays deliberately small (`debian:stable-slim`, `--no-install-recommends`). Tooling installed for in-container agent use: `gh`, `git`, `make`, `neovim`, `npm`, `pipx`, `python3-pip`, `ripgrep`. Add to that list only when a tool is actually needed at runtime.
- The container runs as non-root `user`; keep it that way and pre-create any new mount point with the right ownership before the `USER user` switch.
- `EDITOR`/`VISUAL` are set to `nvim` so terminal agents that shell out to an editor for long prompts work out of the box.

## Agent instruction files

`AGENTS.md` is the single source of truth. `CLAUDE.md` is a symlink to it — edit `AGENTS.md` only. If another agent needs its own filename (e.g. `GEMINI.md`), add a symlink rather than a copy.
