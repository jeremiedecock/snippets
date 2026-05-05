#!/bin/bash

# Port 5353 is the standard mDNS (Multicast DNS) port, used by avahi-daemon on most Linux distributions.
# I am therefore using port 3535 instead.

dig @127.0.0.1 -p 3535 foo.jdhp.org
