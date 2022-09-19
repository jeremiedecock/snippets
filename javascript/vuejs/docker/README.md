Usage example (dev):

```
cd hello
docker build -t vue-hello .
docker run --rm -it -p 8002:8002 vue-hello
```

Usage example (prod):

```
cd hello
docker build -t vue-hello .
docker run --rm -it -p 3000:3000 vue-hello
```

C.f. https://www.reddit.com/r/docker/comments/ve6slx/comment/ictj7cd/