#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

"""
Animation

Makes an animation by repeatedly calling a function

See:
- https://matplotlib.org/gallery/animation/dynamic_image2.html
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

fig = plt.figure()

def f(x, y):
    return np.sin(x) + np.cos(y)

x = np.linspace(0, 2 * np.pi, 120)
y = np.linspace(0, 2 * np.pi, 100).reshape(-1, 1)

# ims is a list of lists, each row is a list of artists to draw in the
# current frame; here we are just animating one artist, the image, in
# each frame
ims = []
for i in range(60):
    x += np.pi / 15.
    y += np.pi / 20.
    im = plt.imshow(f(x, y), animated=True)
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                repeat_delay=1000)

# ani.save('dynamic_images.mp4')

plt.show()
