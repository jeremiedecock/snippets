#!/bin/bash

# Port 5353 is the standard mDNS (Multicast DNS) port, used by avahi-daemon on most Linux distributions.
# I am therefore using port 3535 instead.

podman run \
  --rm \
  --name unbound \
  -p 3535:53/udp \
  -p 3535:53/tcp \
  --cap-add=NET_ADMIN \
  -v ./unbound.conf:/etc/unbound/unbound.conf:ro \
  localhost/unbound:latest
