# Hello

## Build the Flask app and run Nginx

```sh
docker-compose up
```

Then open a web browser and load page http://localhost:8080/


## Deploy on a server with Ansible

Add the destination host in the `hosts` file, then type:

```sh
./ansible_playbook.yml -i hosts
```

