#!/usr/bin/env python3

from pydantic import BaseModel

class Foo(BaseModel):
    bar: int

foo = Foo(bar=1)

print(foo.model_dump())