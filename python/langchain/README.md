# Construire l'image Podman

```
podman build -t langchain-hello-world .
```

# Exécuter le conteneur

```
podman run --rm -it -v $(pwd):/app langchain-dev
```
# Documentation

- https://python.langchain.com/docs/introduction/
- https://python.langchain.com/docs/tutorials/llm_chain/
- https://python.langchain.com/docs/integrations/chat/huggingface/
