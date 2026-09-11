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

ENV HOME=/home/user \
    NPM_CONFIG_PREFIX=/home/user/.local \
    PATH="/home/user/.local/bin:${PATH}" \
    LANG=C.UTF-8

# Install Codex
RUN mkdir -p "${HOME}/.local" "${HOME}/.codex" \
 && npm install --global @openai/codex \
 && codex --version

WORKDIR /workspace

CMD ["codex"]
