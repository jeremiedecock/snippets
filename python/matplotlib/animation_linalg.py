#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2017 Jérémie DECOCK (http://www.jdhp.org)

"""
Animation

Makes an animation

See:
- https://matplotlib.org/api/animation_api.html
- http://matplotlib.org/gallery/animation/basic_example_writer_sgskip.html
- http://matplotlib.org/examples/animation/simple_anim.html
- https://matplotlib.org/api/_as_gen/matplotlib.animation.Animation.save.html
- https://matplotlib.org/examples/animation/moviewriter.html
- https://matplotlib.org/1.2.1/api/animation_api.html
- http://louistiao.me/posts/notebooks/save-matplotlib-animations-as-gifs/
- http://louistiao.me/posts/notebooks/embedding-matplotlib-animations-in-jupyter-notebooks/
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots(figsize=(6.0, 6.0))
ax.axis('equal')              # Same scale on x and y
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)

x = np.linspace(-10, 10, 21)
y = np.linspace(-10, 10, 21)
X, Y  = np.meshgrid(x, y)

Xs = np.array([X.ravel(), Y.ravel()])

scat = ax.scatter(Xs[0], Xs[1])

Ms = np.eye(2)
#Me = np.eye(2) * 2.
angle = math.radians(180)
Me = np.array([[math.cos(angle), -math.sin(angle)],
               [math.sin(angle), math.cos(angle)]])

NFRAMES = 100
m1 = np.linspace(Ms[0,0], Me[0,0], NFRAMES)
m2 = np.linspace(Ms[0,1], Me[0,1], NFRAMES)
m3 = np.linspace(Ms[1,0], Me[1,0], NFRAMES)
m4 = np.linspace(Ms[1,1], Me[1,1], NFRAMES)

def update(i):
    angle = math.radians(i)
    Mi = np.array([[math.cos(angle), -math.sin(angle)],
                   [math.sin(angle), math.cos(angle)]])
    #Mi = np.array([[m1[i%NFRAMES], m2[i%NFRAMES]], [m3[i%NFRAMES], m4[i%NFRAMES]]])
    Xi = np.dot(Mi, Xs)
    scat.set_offsets(Xi.T)

# https://matplotlib.org/1.2.1/api/animation_api.html#matplotlib.animation.FuncAnimation
# Makes an animation by repeatedly calling a function func, passing in (optional) arguments in fargs.
anim = animation.FuncAnimation(fig, update, interval=25)

plt.show()
