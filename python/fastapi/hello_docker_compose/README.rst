FastAPI with Docker
===================

Documentation: https://fastapi.tiangolo.com/deployment/docker/

Usage
=====

Build and run the docker container::

    docker-compose up -d

Then open your browser at http://127.0.0.1 or http://127.0.0.1/items/5?q=somequery to test it.

To see the automatic interactive API documentation (provided by Swagger UI), open your browser at: http://127.0.0.1/docs

To see the alternative automatic documentation (provided by ReDoc), open your browser at: http://127.0.0.1/redoc

Watch logs::

    docker-compose logs

Stop and removing the docker container::

    docker-compose down

Or to just stop (but not remove) the docker container::

    docker-compose stop
