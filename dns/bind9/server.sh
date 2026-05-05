#!/bin/bash

# Port 5353 is the standard mDNS (Multicast DNS) port, used by avahi-daemon on most Linux distributions.
# I am therefore using port 3535 instead.

podman run \
  --rm \
  --name bind9 \
  -p 3535:53/udp \
  -p 3535:53/tcp \
  --cap-add=NET_ADMIN \
  -v ./named.conf:/etc/bind/named.conf:ro \
  -v ./db.jdhp.org:/etc/bind/db.jdhp.org:ro \
  localhost/bind9:latest
