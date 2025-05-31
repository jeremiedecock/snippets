FROM python:3.12-slim

# Git and SSH are required for ClearML Agent
RUN apt update -y && apt install -y --no-install-recommends git ssh && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir clearml-agent

COPY clearml.conf /root/clearml.conf

WORKDIR /app
