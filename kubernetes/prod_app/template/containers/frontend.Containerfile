# Build context is the repository root:
#   podman build -f containers/frontend.Containerfile -t <image> .
#
# The unprivileged nginx image: runs as UID 101 and listens on 8080, so the
# Pod needs no root and no NET_BIND_SERVICE capability.
FROM docker.io/nginxinc/nginx-unprivileged:stable-alpine

COPY frontend/src/ /usr/share/nginx/html/

EXPOSE 8080
