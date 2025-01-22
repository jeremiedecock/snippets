# Construire l'image Podman

```
podman build -t langchain-hello-world .
```

# Exécuter le conteneur

```
podman run --rm -it -v $(pwd):/app langchain-dev
```
