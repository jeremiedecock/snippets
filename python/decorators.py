#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def foo(f):
    print("decorating", f.__name__)
    print()
    return f

# Equivalent to:
#
# def bar():
#     ...
# 
# bar = foo(bar)

@foo
def bar():
    print("hello")

bar()
