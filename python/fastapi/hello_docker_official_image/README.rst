FastAPI with Docker
===================

Documentation: https://fastapi.tiangolo.com/deployment/docker/

FastAPI official docker image: https://fastapi.tiangolo.com/de/deployment/server-workers/

Usage
=====

Build the docker image::

    docker build -t fast-api-hello-official-docker-image .

Run the docker container::

    docker run -d --name fast-api-hello-official-docker-container -p 80:80 fast-api-hello-official-docker-image

Then open your browser at http://127.0.0.1 to test it.

To see the automatic interactive API documentation (provided by Swagger UI), open your browser at: http://127.0.0.1/docs

To see the alternative automatic documentation (provided by ReDoc), open your browser at: http://127.0.0.1/redoc

Stop the docker container::

    docker stop fast-api-hello-official-docker-container

Watch logs::

    docker logs fast-api-hello-official-docker-container
