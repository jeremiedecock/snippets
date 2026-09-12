FROM debian:stable-slim

ARG CONTAINER_UID=1000
ARG CONTAINER_GID=1000

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    gh \
    git \
    make \
    neovim \
    npm \
    pipx \
    python3-pip \
    ripgrep \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN groupadd --gid "${CONTAINER_GID}" user \
 && useradd \
      --uid "${CONTAINER_UID}" \
      --gid "${CONTAINER_GID}" \
      --no-log-init \
      --shell /bin/bash \
      --create-home \
      user \
 && mkdir -p /workspace \
 && chown user:user /workspace

# Switch to the non-root user
USER user

# - PATH: make `claude` available in all processes (CMD uses exec form, so ~/.bashrc is never sourced)
# - EDITOR: use Neovim for editing long prompts from terminal agents such as Codex CLI
# - CLAUDE_CONFIG_DIR: keep ALL Claude Code state (OAuth token in .credentials.json,
#   .claude.json, settings, history...) in a single directory, bind-mounted from the host.
#   C.f. https://code.claude.com/docs/en/devcontainer.md#persist-authentication-and-settings-across-rebuilds
# - DISABLE_AUTOUPDATER: the CLI version is managed by the image (run `./claude.sh --build`
#   to update); auto-updates would be lost when the container exits anyway
ENV HOME=/home/user \
    PATH="/home/user/.local/bin:${PATH}" \
    LANG=C.UTF-8 \
    EDITOR=nvim \
    VISUAL=nvim \
    CLAUDE_CONFIG_DIR=/home/user/.claude \
    DISABLE_AUTOUPDATER=1

# Pre-create the mount point so that it belongs to 'user'
RUN mkdir -p "${HOME}/.local" "${HOME}/.claude"

# Install Claude Code CLI into the image (~/.local/bin/claude).
# CACHEBUST is set to the current date by `./claude.sh --build` to force this
# layer to re-run (i.e. update Claude Code) without rebuilding the layers above.
ARG CACHEBUST=0
RUN echo "cachebust=${CACHEBUST}" \
 && curl -fsSL https://claude.ai/install.sh | bash

WORKDIR /workspace

CMD ["claude"]
