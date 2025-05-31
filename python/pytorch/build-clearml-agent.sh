#!/bin/sh

podman build -t clearml-agent:latest -f clearml-agent.containerfile .
