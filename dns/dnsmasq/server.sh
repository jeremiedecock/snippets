#!/bin/bash

# Port 5353 is the standard mDNS (Multicast DNS) port, used by avahi-daemon on most Linux distributions.
# I am therefore using port 3535 instead.

podman run \
  --rm \
  --name dnsmasq \
  -p 3535:53/udp \
  -p 3535:53/tcp \
  --cap-add=NET_ADMIN \
  -v ./dnsmasq.conf:/etc/dnsmasq.conf:ro \
  localhost/dnsmasq:latest \
  --no-daemon \
  --conf-file=/etc/dnsmasq.conf
