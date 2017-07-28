#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyglet

window = pyglet.window.Window()

#image = pyglet.resource.image('image.png')
image = pyglet.resource.image('image.jpeg')

@window.event
def on_draw():
    window.clear()
    image.blit(0, 0)

pyglet.app.run()
