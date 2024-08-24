# This Dockerfile is inspired by the official FastAPI Dockerfile: https://fastapi.tiangolo.com/deployment/docker/

FROM python:3.11-slim

WORKDIR /app

COPY . /app
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN pip install .

# Set the database URL as an environment variable (can be overriden with `docker run -e SQLITE_DATABASE_URL=...`)
ENV SQLITE_DATABASE_URL="sqlite:////var/lib/heroes/heroes.sqlite"

EXPOSE 80

CMD ["fastapi", "run", "heroes/main.py", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]