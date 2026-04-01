# Copilot Instructions

## Overview

This repository packages [GitHub Copilot CLI](https://github.com/features/copilot/cli/) inside a **rootless Podman container**. The container image is built from `Containerfile` (Debian slim), and the CLI binary plus all auth/settings are stored in a persistent named Podman volume (`github-copilot-cli-home`) mounted as the container's home directory.

## Workflow

```sh
./build.sh   # Build the container image (podman build)
./init.sh    # Install Copilot CLI into the named volume (run once, re-run to upgrade)
./run.sh     # Start an interactive Copilot session with the current directory as /workspace
```

## Architecture

- **`Containerfile`** – Debian slim base; installs `curl`, `git`, `ripgrep`; creates `user` (uid/gid 1000); sets `PATH` to include `~/.local/bin` so the `copilot` binary is reachable in non-login shells.
- **`init.sh`** – Runs `curl -fsSL https://gh.io/copilot-install | bash` inside a throwaway container to install the CLI into the named volume.
- **`run.sh`** – Mounts the host CWD as `/workspace` and the named volume as `/home/user`, then exec's `copilot`.
- **Named volume `github-copilot-cli-home`** – Persists the CLI binary, GitHub auth tokens, and Copilot settings across container runs.

## Key Conventions

- **`--userns=keep-id:uid=1000,gid=1000`** is used in both `init.sh` and `run.sh` so files written to the bind-mounted `/workspace` are owned by the host user rather than root.
- The container user is always `uid=1000 / gid=1000` (`user`). The `CONTAINER_UID` / `CONTAINER_GID` variables in each script must stay in sync with the `ARG` values in `Containerfile`.
- `PATH` is set via `ENV` (not `.bashrc`) in the `Containerfile` because the `CMD` uses exec form and never sources shell profiles.
- All scripts use `#!/bin/sh` (POSIX sh, not bash).
