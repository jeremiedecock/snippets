FROM python:3.12-slim

# Git and SSH are required for cloning repositories
RUN apt update -y && apt install -y --no-install-recommends git ssh && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir clearml clearml-agent
