#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The simplest snippet

See http://jinja.pocoo.org/docs/2.9/intro/
"""

from jinja2 import Template

template = Template('Hello {{ name }}!')
res_str = template.render(name='John Doe')

print(res_str)
