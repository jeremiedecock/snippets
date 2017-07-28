#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://bitbucket.org/pyglet/pyglet/src/8f6f713700dce9e2f6aeacb63b4d34d18c887c28/examples/image_display.py?at=default&fileviewer=file-view-default

import pyglet
from pyglet.gl import *

window = pyglet.window.Window(visible=False, resizable=True)

#filename = 'image.png'
filename = 'image.jpeg'

@window.event
def on_draw():
    background.blit_tiled(0, 0, 0, window.width, window.height)
    img.blit(window.width // 2, window.height // 2, 0)

img = pyglet.image.load(filename).get_texture(rectangle=True)
img.anchor_x = img.width // 2
img.anchor_y = img.height // 2

checks = pyglet.image.create(32, 32, pyglet.image.CheckerImagePattern())
background = pyglet.image.TileableTexture.create_for_image(checks)

# Enable alpha blending, required for image.blit.
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

window.width = img.width
window.height = img.height
window.set_visible()

pyglet.app.run()
