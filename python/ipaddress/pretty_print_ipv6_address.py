#!/usr/bin/env python3

import ipaddress

IPV6_ADDRESS = "fe80::96c6:92ff:fea9:f4b1"

print( " : ".join([" ".join([".".join(f'{ipaddress.IPv6Address(IPV6_ADDRESS):_b}'.split("_")[i:i+2]) for i in range(0,32,2)][j:j+2]) for j in range(0,16,2)]) )
