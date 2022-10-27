# Hello

## Build the Flask app and run Nginx

```sh
docker-compose up
```

Then open a web browser and load page http://localhost:8080/

## Publish the image on DockerHub

```sh
docker login
docker build -t jdhp/hello-flask:latest .
docker push jdhp/hello-flask:latest
```