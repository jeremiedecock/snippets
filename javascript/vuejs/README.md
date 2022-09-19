# How to create and run a new snippet

## Copy the "hello" directory

```sh
cp -r hello foo
cd foo
```

## Run the server

```sh
docker-compose up
```

Open the browser and load page http://localhost:8001/

Then change the snippet source code on the host ; changes are taken into account instantaneously (no needs to run npm commands)!

## Remove the server before leaving

```sh
docker-compose rm
```