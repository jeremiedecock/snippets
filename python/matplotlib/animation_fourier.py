#!/usr/bin/env python3

import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
ax = plt.axes(xlim=(-7, 7), ylim=(-5, 5))
line, = ax.plot([], [], "o-", lw=2)

ax.axvline(0, color="gray", lw=1)
ax.axhline(0, color="gray", lw=1)

def init():
    line.set_data([], [])
    return line,

def update(frame):
    t = float(frame)/10.
    e = math.e
    
    z1 =      2.  * e ** (1j * t)
    z2 = z1 + 1.  * e ** (1j * 2. * t)
    z3 = z2 - 0.5 * e ** (1j * 3. * t)
    
    x = [0, z1.real, z2.real, z3.real]
    y = [0, z1.imag, z2.imag, z3.imag]
    line.set_data(x, y)
    return line,

ani = animation.FuncAnimation(fig, func=update, init_func=init, frames=62, interval=50, blit=True)

#ani.save('fourier.mp4')
ani.save('animation_fourier.gif', writer='imagemagick', fps=20)

## Set up formatting for the movie files
#Writer = animation.writers['ffmpeg']
#writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
#anim.save('fourier.mp4', writer=writer)

plt.show()
