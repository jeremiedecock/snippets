# Build context is the repository root:
#   podman build -f containers/backend.Containerfile -t <image> .
FROM docker.io/library/python:3.14-slim

WORKDIR /app

COPY backend/src/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/src/ ./

EXPOSE 8000
# Overridden in the Deployment, which appends --root-path.
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
