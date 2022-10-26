# Hello

## Build the Flask app and run Nginx

```sh
docker-compose up
```

Then open a web browser and load page http://127.0.0.1/api/


## Deploy on a server with Ansible

Add the destination host in the `hosts` file, then type:

```sh
./ansible_playbook.yml -i hosts
```


## Remove the webapp

From the host terminal (as root):

```sh
cd /srv/flask_example_app
docker-compose down
docker rmi flask_example_app_nginx flask_example_app_flask
cd ..
rm -rf flask_example_app
```