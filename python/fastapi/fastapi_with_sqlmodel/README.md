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
If needed, update ansible variables in `ansible_playbooks/ansible_playbook.yml` (FQDN, ...).
Then, run the following command:

```sh
./ansible_playbooks/ansible_playbook.yml -i ansible_playbooks/hosts.ini
```

To test the deployment, open a web browser and navigate to https://api.heroes.jdhp.org/heroes/.

To view the Traefik dashboard, visit: https://traefik.jdhp.org/.

For the automatic interactive API documentation (provided by Swagger UI), visit: https://api.heroes.jdhp.org/docs/.

For the alternative automatic documentation (provided by ReDoc), visit: https://api.heroes.jdhp.org/redoc/.

The frontend can be accessed at: https://heroes.jdhp.org/

To check logs (from the remote host terminal as `root`), use:

```sh
docker logs docker_heroes-api_1 -f
docker logs docker_heroes-frontend_1 -f
docker logs traefik_traefik_1 -f
```

To eventually remove the application (from the remote host terminal as `root`):

```sh
cd /srv/heroes
docker-compose -f docker/docker-compose-app.yml down
docker system prune
docker rmi docker_heroes-api
cd /srv
rm -rf /srv/heroes
```
