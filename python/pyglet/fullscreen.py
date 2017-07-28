#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyglet

window = pyglet.window.Window(fullscreen=True)

label = pyglet.text.Label('Press ESC to quit',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

@window.event
def on_draw():
    window.clear()
    label.draw()

pyglet.app.run()
