FastAPI with Docker Compose and Ansible
=======================================

Documentation: https://fastapi.tiangolo.com/deployment/docker/

See:
- https://www.youtube.com/watch?v=7N5O62FjGDc&list=WL&index=6
- https://dev.to/tiangolo/deploying-fastapi-and-other-apps-with-https-powered-by-traefik-5dik


Usage
=====

Test on localhost
-----------------

TODO...


Deploy on a server manually (i.e. without Ansible)
--------------------------------------------------

Copy the project to the remote network (e.g. comment the `docker_network` and `docker_compose` tasks in the playbook then play it as described below),
then connect to the remote server (as root) and type::

    cd /srv/fastapi_example_app
    docker network create traefik-public
    docker-compose -f docker-compose.traefik.yml up -d
    docker-compose -f docker-compose.yml up -d

Then open http://vps-f8e7667b.vps.ovh.net/ in a browser.


Deploy on a server with Ansible
-------------------------------

Add the destination host in the `hosts` file, then type::

    ./ansible_playbook.yml -i hosts

Then open http://vps-f8e7667b.vps.ovh.net/ in a browser.


Check logs
----------

From the remote host terminal (as root)::

    docker logs fastapi_example_app_traefik_1 -f
    docker logs fastapi_example_app_backend_1 -f


Remove the webapp
-----------------

From the remote host terminal (as root)::

    cd /srv/fastapi_example_app
    docker-compose -f docker-compose.traefik.yml down
    docker-compose -f docker-compose.yml down
    docker network rm traefik-public
    docker system prune
    docker rmi ...
    cd /srv
    rm -rf /srv/fastapi_example_app
