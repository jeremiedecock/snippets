#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cppclasses

hello = cppclasses.Hello()
hello.greet()

helloMartin = cppclasses.Hello("Martin")
helloMartin.greet()

#help(cppclasses)
