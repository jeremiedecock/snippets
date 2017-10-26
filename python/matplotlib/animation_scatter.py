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
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)

scat = ax.scatter([], [])

def update(i):
    if i < 30 or i > 60:
        # 1 point
        scat.set_edgecolors(['b'])
        scat.set_sizes([abs(math.sin(i/6.) * 50) + 5])
        scat.set_offsets([[math.cos(i/20.0), math.sin(i/20.0)]])
    else:
        # 2 points
        scat.set_edgecolors(['r', 'r'])
        scat.set_sizes([abs(math.sin(i/6.) * 50) + 5,
                        abs(math.sin(i/6.) * 50) + 5])
        scat.set_offsets([[math.cos((i-10)/20.0), math.sin((i-10)/20.0)],
                          [math.cos(i/20.0), math.sin(i/20.0)]])

# https://matplotlib.org/1.2.1/api/animation_api.html#matplotlib.animation.FuncAnimation
# Makes an animation by repeatedly calling a function func, passing in (optional) arguments in fargs.
anim = animation.FuncAnimation(fig, update, interval=25)

plt.show()
