# Deployment with Docker Compose and Ansible

The deployment process follows guidance from the official FastAPI documentation: [FastAPI Deployment with Docker](https://fastapi.tiangolo.com/deployment/docker/).

For additional resources, see:
- [YouTube: FastAPI Deployment Tutorial](https://www.youtube.com/watch?v=7N5O62FjGDc&list=WL&index=6)
- [Dev.to: Deploying FastAPI and Other Apps with HTTPS via Traefik](https://dev.to/tiangolo/deploying-fastapi-and-other-apps-with-https-powered-by-traefik-5dik)

You can also refer to the official FastAPI Docker image documentation here: [FastAPI Docker Image and Server Workers](https://fastapi.tiangolo.com/de/deployment/server-workers/).


## Development Environment

For detailed instructions on installing, configuring, and running this project locally (with or without Docker or Docker Compose), please refer to the `README.rst` file located in the `src` directory of this project.


## Production Environment

### Deploying on a Server with Ansible

Add the target host to the `hosts.ini` file.
Then, run the following command:

```sh
./ansible_playbooks/ansible_playbook.yml -i ansible_playbooks/hosts
```

To test the deployment, open a web browser and navigate to:
- https://hello.jdhp.org/
- https://hello.jdhp.org/heroes/

To view the Traefik dashboard, visit: https://traefik.hello.jdhp.org/.

For the automatic interactive API documentation (provided by Swagger UI), visit: https://hello.jdhp.org/docs.

For the alternative automatic documentation (provided by ReDoc), visit: https://hello.jdhp.org/redoc.

The frontedn can be accessed at: https://nginx.hello.jdhp.org/

To check logs (from the remote host terminal as `root`), use:

```sh
docker logs fastapi-hello -f
```


### Deploy Manually on a Server (Without Ansible)

Copy the project to the remote server.
If using Ansible, you can disable the `docker_network` and `docker_compose` tasks in the playbook, then execute it as described below.

Then Connect to the remote server (as `root`) and run the following commands:

```sh
cd /srv/hello
docker network create traefik-public
docker-compose -f docker-compose.traefik.yml up -d
docker-compose -f docker-compose.yml up -d
```

After deployment, open a web browser at https://hello.jdhp.org/ and https://traefik.hello.jdhp.org/.

Check logs (from the remote host terminal as `root`):

```sh
docker logs hello_traefik_1 -f
docker logs fastapi-hello -f
docker logs hello_streamlit_1 -f
docker logs hello_panel_1 -f
docker logs hello_gradio_1 -f
```

To eventually remove the webapp (from the remote host terminal as `root`):

```sh
cd /srv/hello
docker-compose -f docker-compose.traefik.yml down
docker-compose -f docker-compose.yml down
docker network rm traefik-public
docker system prune
docker rmi fastapi_hello hello_panel hello_streamlit hello_gradio hello_nginx traefik
cd /srv
rm -rf /srv/hello
```
