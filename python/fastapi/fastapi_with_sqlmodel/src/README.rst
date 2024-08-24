.. |ProjectName| replace:: Heroes
.. |ProjectWebSiteURL| replace:: https://gitlab.com/jdhp-dev/snippets/-/tree/master/python/fastapi/fastapi_with_sqlmodel
.. |ProjectOnlineDocumentationURL| replace:: https://gitlab.com/jdhp-dev/snippets/-/tree/master/python/fastapi/fastapi_with_sqlmodel
.. |ProjectOnlineAPIDocumentationURL| replace:: https://gitlab.com/jdhp-dev/snippets/-/tree/master/python/fastapi/fastapi_with_sqlmodel
.. |ProjectIssueTrackerURL| replace:: https://gitlab.com/jdhp-dev/snippets/-/tree/master/python/fastapi/fastapi_with_sqlmodel
.. |PythonPackageName| replace:: heroes
.. |ProjectShortDesc| replace:: A simple FastAPI webapp with SQLModel
.. |ProjectGitForgePath| replace:: jdhp-dev
.. |ProjectGitForgeRepositoryName| replace:: snippets

====
|ProjectName|
====

Copyright (c) 2024 Jérémie Decock (www.jdhp.org)

* Web site: |ProjectWebSiteURL|
* Online documentation: |ProjectOnlineDocumentationURL|
* Source code: |ProjectWebSiteURL|
* Issue tracker: |ProjectIssueTrackerURL|


Table of Contents
=================

.. contents:: 
   :depth: 2

Description
===========

|ProjectShortDesc|

Note:

    This project is still in beta stage, so the API is not finalized yet.


Dependencies
============

C.f. requirements.txt


.. _install:

Development environment
=======================

Install (on Posix systems i.e. Linux, MacOSX, WSL, ...)
-------------------------------------------------------

From the ``src`` directory, run::

    python3 -m venv env
    source env/bin/activate
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements-dev.txt


Run the FastAPI backend in "development" mode (auto reload, etc.)
-----------------------------------------------------------------

From the ``src`` directory, run::

    fastapi dev heroes/main.py

or equivalently::

    uvicorn heroes.main:app --reload

Then open a web browser at http://127.0.0.1:8000/ or http://127.0.0.1:8000/heroes/ to test it.

To see the automatic interactive API documentation (provided by Swagger UI), open your browser at: http://127.0.0.1:8000/docs.

To see the alternative automatic documentation (provided by ReDoc), open your browser at: http://127.0.0.1:8000/redoc.

See https://fastapi.tiangolo.com/tutorial/first-steps/ for more information.


Run the FastAPI backend in "production" mode (a bit faster)
-----------------------------------------------------------

From the ``src`` directory, run::

    fastapi run heroes/main.py

or equivalently::

    uvicorn heroes.main:app

See https://fastapi.tiangolo.com/tutorial/first-steps/ for more information.


Build and run the Python Docker image
-------------------------------------

.. warning::

   The following commands have to be run from the root directory of this project (**not** from the ``src`` directory).

Build the docker image (from the root directory of this project)::

    docker build -t heroes_backend:latest -f ./docker/fastapi.dockerfile ./src

Run an example from the docker container (from the root directory of this project)::

    docker run --rm --name heroes_container -p 8000:80 heroes_backend

Run an example from the docker container with a persistent volume (from the root directory of this project)::

    docker run --rm --name heroes_container -p 8000:80 -v heroes-database:/var/lib/heroes/ -e SQLITE_DATABASE_URL="sqlite:////var/lib/heroes/heroes.sqlite" heroes_backend

or equivalently, if you want to specify the database directory on the host file system (e.g. to inspect the database with an external tool like ``sqlite3``)::

    docker run --rm --name heroes_container -p 8000:80 -v /tmp/heroes:/var/lib/heroes/ -e SQLITE_DATABASE_URL="sqlite:////var/lib/heroes/heroes.sqlite" heroes_backend

Then open a web browser at http://localhost:8000/ or http://localhost:8000/heroes/ to test it.

To see the automatic interactive API documentation (provided by Swagger UI), open your browser at: http://127.0.0.1:8000/docs.

To see the alternative automatic documentation (provided by ReDoc), open your browser at: http://127.0.0.1:8000/redoc.

If needed, the content of the docker image can be inspected with the following command::

    docker run -it heroes_backend bash

The content of a docker container can also be inspected while it is running with the following command::

    docker exec -it heroes_container bash


Build and run the Python Docker image with Docker Compose
---------------------------------------------------------

To build and run the Python Docker image with Docker Compose, run the following commands from the root directory of this project::

    docker network create traefik-public
    APPLICATION_DATABASE_PATH=/tmp/heroes docker-compose -f docker/docker-compose-app.yml -f docker/docker-compose-app.override.yml up

Then open a web browser at http://localhost/ or http://localhost/heroes/ to test it.

To see the automatic interactive API documentation (provided by Swagger UI), open your browser at: http://localhost/docs.

To see the alternative automatic documentation (provided by ReDoc), open your browser at: http://localhost/redoc.

Check logs::

    docker logs docker_backend_1 -f
    docker logs docker_nginx_1 -f

Stop::

    APPLICATION_DATABASE_PATH=/tmp/heroes docker-compose -f docker/docker-compose-app.yml -f docker/docker-compose-app.override.yml down
    docker network rm traefik-public
    docker system prune
    docker rmi docker_backend


Production environment
======================

Refer to the ``README.md`` file in the root directory of this project for information on how to deploy this project in a production environment.
