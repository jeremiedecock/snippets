# Mistral Vibe CLI in a rootless Podman container

This demo shows how to install and run [Mistral Vibe CLI](https://docs.mistral.ai/mistral-vibe/introduction/quickstart)
inside a rootless Podman container, while keeping the host working directory writable by the
current user without permission issues.

## How it works

- The container runs as a non-root user (`uid=1000`, `gid=1000`).
- `--userns=keep-id` maps the container user to your host user, so files written inside
  `/workspace` (mounted from `.`) are owned by you on the host.
- Mistral Vibe CLI and its authentication data are stored in a single persistent named volume
  (`mistral-vibe-home`), mounted as the container's home directory.

## Files

| File | Description |
|------|-------------|
| `Containerfile` | Defines the container image (Debian slim + build tools) |
| `build.sh` | Builds the image |
| `init.sh` | Installs Mistral Vibe CLI into the persistent home volume (run once) |
| `run.sh` | Starts an interactive Mistral Vibe session in the current directory |

## Requirements

- [Podman](https://podman.io/) (rootless mode)

## Usage

### 1. Build the image

```sh
./build.sh
```

### 2. Initialize (run once)

Install Mistral Vibe CLI into the persistent named volume:

```sh
./init.sh
```

This runs `curl -LsSf https://mistral.ai/vibe/install.sh | bash` inside a temporary container
and stores the result in the `mistral-vibe-home` Podman volume. Your authentication data
and Mistral Vibe settings will also be persisted in this volume across sessions.

> Re-run `init.sh` whenever you want to update Mistral Vibe CLI to the latest version.

### 3. Run

```sh
./run.sh
```

This mounts the current directory as `/workspace` and launches `vibe` interactively.
Any files created or modified by Mistral Vibe CLI will be owned by your host user.

## Volumes

| Volume | Mount point | Content |
|--------|-------------|---------|
| `mistral-vibe-home` | `/home/user` | Mistral Vibe CLI binary, authentication, settings |
