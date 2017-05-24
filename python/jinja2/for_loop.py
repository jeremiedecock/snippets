#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The for loop

See http://jinja.pocoo.org/
"""

from jinja2 import Template

template_str = '''
{% for item in seq -%}
{{ item }};
{%- endfor %}
'''

template = Template(template_str)
res_str = template.render(seq=['apple', 'banana', 'grapes'])

print(res_str)
