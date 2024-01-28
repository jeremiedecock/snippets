FastAPI with Docker Compose and Ansible
=======================================

Documentation: https://fastapi.tiangolo.com/deployment/docker/

See:
- https://www.youtube.com/watch?v=7N5O62FjGDc&list=WL&index=6
- https://dev.to/tiangolo/deploying-fastapi-and-other-apps-with-https-powered-by-traefik-5dik

FastAPI official docker image: https://fastapi.tiangolo.com/de/deployment/server-workers/

Usage
=====

Test on localhost
-----------------

Start::

    docker network create traefik-public
    docker-compose -f docker-compose.yml up -d

Check::

    docker logs fastapi_example_app_backend -f

Stop::

    docker-compose -f docker-compose.yml down
    docker network rm traefik-public
    docker system prune
    docker rmi sql_sqlalchemy_05_timeseries_docker-compose_ansible_traefik_https_dashboard_api-token_backend


Deploy on a server manually (i.e. without Ansible)
--------------------------------------------------

Copy the project to the remote network (e.g. comment the `docker_network` and `docker_compose` tasks in the playbook then play it as described below),
then connect to the remote server (as root) and type::

    cd /srv/fastapi_example_app
    docker network create traefik-public
    docker-compose -f docker-compose.traefik.yml up -d
    docker-compose -f docker-compose.yml up -d


Deploy on a server with Ansible
-------------------------------

Add the destination host in the `hosts` file, then type::

    ./ansible_playbook.yml -i hosts

Open a web browser at https://hello.jdhp.org/ and https://traefik.hello.jdhp.org/.

Open a wab browser at https://hello.jdhp.org/docs to see the API documentation or to debug.


Check logs
----------

From the remote host terminal (as root)::

    docker logs fastapi_example_app_traefik_1 -f
    docker logs fastapi_example_app_backend -f


Remove the webapp
-----------------

From the remote host terminal (as root)::

    cd /srv/fastapi_example_app
    docker-compose -f docker-compose.traefik.yml down
    docker-compose -f docker-compose.yml down
    docker network rm traefik-public
    docker system prune
    docker rmi fastapi_example_app_backend
    cd /srv
    rm -rf /srv/fastapi_example_app
