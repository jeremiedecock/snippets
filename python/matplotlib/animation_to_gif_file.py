#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2017 Jérémie DECOCK (http://www.jdhp.org)

"""
Animation

Makes an animation and save it in a file

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

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()

x = np.arange(0, 2*np.pi, 0.01)
line, = ax.plot(x, np.sin(x))

def update(i):
    line.set_ydata(np.sin(x + i/10.0))  # update the data
    return line,


# Init only required for blitting to give a clean slate.
def init():
    line.set_ydata(np.ma.array(x, mask=True))
    return line,

# https://matplotlib.org/1.2.1/api/animation_api.html#matplotlib.animation.FuncAnimation
# Makes an animation by repeatedly calling a function func, passing in (optional) arguments in fargs.
anim = animation.FuncAnimation(fig, update, np.arange(1, 100), init_func=init,
                               interval=25, blit=True)

anim.save('animation.gif', writer='imagemagick', fps=60)

#plt.show()
