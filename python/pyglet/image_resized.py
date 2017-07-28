#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://stackoverflow.com/questions/24788003/how-do-you-resize-an-image-in-python-using-pyglet

import pyglet

window = pyglet.window.Window()

#image = pyglet.resource.image('image.png')
image = pyglet.resource.image('image.jpeg')

print(image.width)
print(image.height)

image.width = 250
image.height = 300

#image.width  = image.width  // 4
#image.height = image.height // 4

@window.event
def on_draw():
    window.clear()
    image.blit(0, 0)

pyglet.app.run()
