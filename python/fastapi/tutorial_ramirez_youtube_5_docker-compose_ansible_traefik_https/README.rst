FastAPI with Docker Compose and Ansible
=======================================

Documentation: https://fastapi.tiangolo.com/deployment/docker/

See:
- https://www.youtube.com/watch?v=7N5O62FjGDc&list=WL&index=6
- https://dev.to/tiangolo/deploying-fastapi-and-other-apps-with-https-powered-by-traefik-5dik

FastAPI official docker image: https://fastapi.tiangolo.com/de/deployment/server-workers/


Development environment
=======================

Install (on Posix systems i.e. Linux, MacOSX, WSL, ...)
-------------------------------------------------------

From the project source code::

    python3 -m venv env
    source env/bin/activate
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt


Run (without Docker)
--------------------

Run::

    uvicorn app.main:app --reload

Then open a web browser at http://127.0.0.1:8000/ or http://127.0.0.1:8000/items/5?q=somequery to test it.

To see the automatic interactive API documentation (provided by Swagger UI), open your browser at: http://127.0.0.1:8000/docs.

To see the alternative automatic documentation (provided by ReDoc), open your browser at: http://127.0.0.1:8000/redoc.


Build and run the Python Docker image
-------------------------------------

Build the docker image (from the project source code)::

    docker build -t fastapi_hello:latest .

Run an example from the docker container (from the project source code)::

    docker run -p 8000:80 fastapi_hello

Then open a web browser at http://localhost:8000/ or http://localhost:8000/items/5?q=somequery to test it.

To see the automatic interactive API documentation (provided by Swagger UI), open your browser at: http://127.0.0.1:8000/docs.

To see the alternative automatic documentation (provided by ReDoc), open your browser at: http://127.0.0.1:8000/redoc.


Build and run the Python Docker image with Docker Compose
---------------------------------------------------------

Start::

    docker network create traefik-public
    docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d

Then open a web browser at http://localhost/ or http://localhost/items/5?q=somequery to test it.

To see the automatic interactive API documentation (provided by Swagger UI), open your browser at: http://localhost/docs.

To see the alternative automatic documentation (provided by ReDoc), open your browser at: http://localhost/redoc.

Check logs::

    docker logs fast-api-hello -f

Stop::

    docker-compose -f docker-compose.yml down
    docker system prune
    docker rmi fastapi_hello


Production environment
======================

Deploy on a server with Ansible
-------------------------------

Add the destination host in the `hosts` file, then type::

    ./ansible_playbooks/ansible_playbook.yml -i ansible_playbooks/hosts

Then open a web browser at https://hello.jdhp.org/ or https://hello.jdhp.org/items/5?q=somequery to test it.

To see the automatic interactive API documentation (provided by Swagger UI), open your browser at: https://hello.jdhp.org/docs.

To see the alternative automatic documentation (provided by ReDoc), open your browser at: https://hello.jdhp.org/redoc.

Check logs (from the remote host terminal, as root)::

    docker logs fastapi-hello -f


Deploy on a server manually (i.e. without Ansible)
--------------------------------------------------

Copy the project to the remote network (e.g. comment the `docker_network` and `docker_compose` tasks in the playbook then play it as described below),
then connect to the remote server (as root) and type::

    cd /srv/hello
    docker network create traefik-public
    docker-compose -f docker-compose.traefik.yml up -d
    docker-compose -f docker-compose.yml up -d

Open a web browser at https://hello.jdhp.org/ and https://traefik.hello.jdhp.org/.

Check logs (from the remote host terminal, as root)::

    docker logs hello_traefik_1 -f
    docker logs fastapi-hello -f

If eventually you want to remove the webapp (from the remote host terminal, as root)::

    cd /srv/hello
    docker-compose -f docker-compose.traefik.yml down
    docker-compose -f docker-compose.yml down
    docker network rm traefik-public
    docker system prune
    docker rmi fastapi_hello
    cd /srv
    rm -rf /srv/hello
