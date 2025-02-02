FROM python:3.12-slim

WORKDIR /app

COPY requirements-minimal.txt /app
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements-minimal.txt
