#!/bin/sh

podman build -t claude-code-cli:latest -f claude.containerfile .
