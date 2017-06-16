#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

"""
Draw geometric shapes

See:

- https://matplotlib.org/examples/shapes_and_collections/artist_reference.html
- https://matplotlib.org/api/patches_api.html
- http://matthiaseisen.com/matplotlib/shapes/
- https://matplotlib.org/users/artists.html

TODO:

- Fancy Arrows:

    - http://matthiaseisen.com/matplotlib/shapes/arrow/
    - http://matplotlib.org/examples/pylab_examples/fancyarrow_demo.html

- Text with Fancy Box:

    - https://matplotlib.org/api/patches_api.html#matplotlib.patches.BoxStyle
    - http://matplotlib.org/examples/pylab_examples/fancybox_demo2.html

- Path Patch: https://matplotlib.org/api/path_api.html#module-matplotlib.path
- Transform:

    - https://matplotlib.org/users/transforms_tutorial.html
    - https://stackoverflow.com/questions/4285103/matplotlib-rotating-a-patch
"""

import numpy as np
import matplotlib.pyplot as plt
import math

import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.path as mpath
import itertools

TITLE_FONT_SIZE = 9

fig, axis_array = plt.subplots(nrows=4,
                               ncols=5,
                               squeeze=False,   # <- Always make a 2D array, whatever nrows and ncols
                               figsize=(12.5, 6))

axs = axis_array.flat

for ax in axs:
    ax.axis('equal')      # same scale on X and Y
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_axis_off()

fill_color = "red"
line_color = "blue"
line_width = 2.
line_style = 'dashed'     # 'solid' (default), 'dashed', 'dashdot', 'dotted'   see: http://matplotlib.org/examples/lines_bars_and_markers/linestyles.html
join_style = "miter"      # 'miter', 'round', 'bevel'                          see: http://matplotlib.org/examples/api/joinstyle.html
fill = True               # True or False
fill_pattern = "/"        # "/", "\\", '-', '+', 'x', 'o', 'O', '.', '*'
alpha = 0.5

it = itertools.count()

# DRAW A LINE #################################################################

ax = axs[next(it)]

p1_x = -4
p1_y = -3

p2_x = 0
p2_y = 3

p3_x = 4
p3_y = -3

line = mlines.Line2D((p1_x, p2_x, p3_x),
                     (p1_y, p2_y, p3_y),
                     # COMMON OPTIONS:
                     alpha=alpha,
                     lw=line_width,
                     linestyle=line_style,
                     color=line_color)
ax.add_line(line)
ax.set_title("matplotlib.patches.Line2D", fontsize=TITLE_FONT_SIZE)

# DRAW AN ARROW ###############################################################

ax = axs[next(it)]

pt_start_x = -4.
pt_start_y = -3.

length_x = 8.
length_y = 6.

width = 3.

patch = mpatches.Arrow(x=pt_start_x,
                       y=pt_start_y,
                       dx=length_x,
                       dy=length_y,
                       width=width,
                       # COMMON OPTIONS:
                       alpha=alpha,
                       fill=fill,
                       facecolor=fill_color,
                       hatch=fill_pattern,
                       ec=line_color,
                       lw=line_width,
                       joinstyle=join_style,
                       linestyle=line_style)

ax.add_patch(patch)
ax.set_title("matplotlib.patches.Arrow", fontsize=TITLE_FONT_SIZE)

# DRAW A RECTANGLE ############################################################

ax = axs[next(it)]

lower_left_point = (-4., -3.)
width = 8
height = 6
angle = 0.

patch = mpatches.Rectangle(lower_left_point,
                           width=width,
                           height=height,
                           angle=angle, 
                           # COMMON OPTIONS:
                           alpha=alpha,
                           fill=fill,
                           facecolor=fill_color,
                           hatch=fill_pattern,
                           ec=line_color,
                           lw=line_width,
                           joinstyle=join_style,
                           linestyle=line_style)

ax.add_patch(patch)
ax.set_title("matplotlib.patches.Rectangle", fontsize=TITLE_FONT_SIZE)

# DRAW A FANCY BBOX PATCH #####################################################

ax = axs[next(it)]

lower_left_point = (-4., -3.)
width = 8
height = 6
box_style = 'darrow'       # 'circle', 'darrow', 'larrow', 'rarrow', 'round', 'round4', 'roundtooth', 'sawtooth', 'square'
bbox_transmuter = None
mutation_scale = 1.0       # a value with which attributes of boxstyle (e.g., pad) will be scaled. default=1.
mutation_aspect = None     # The height of the rectangle will be squeezed by this value before the mutation and the mutated box will be stretched by the inverse of it. default=None.

patch = mpatches.FancyBboxPatch(xy=lower_left_point,
                                width=width,
                                height=height,
                                boxstyle=box_style,
                                bbox_transmuter=bbox_transmuter,
                                mutation_scale=mutation_scale,
                                mutation_aspect=mutation_aspect,
                                # COMMON OPTIONS:
                                alpha=alpha,
                                fill=fill,
                                facecolor=fill_color,
                                hatch=fill_pattern,
                                ec=line_color,
                                lw=line_width,
                                joinstyle=join_style,
                                linestyle=line_style)

ax.add_patch(patch)
ax.set_title("matplotlib.patches.FancyBboxPatch\nDArrow", fontsize=TITLE_FONT_SIZE)

# DRAW A FANCY BBOX PATCH #####################################################

ax = axs[next(it)]

lower_left_point = (-4., -3.)
width = 8
height = 6
box_style = 'larrow'       # 'circle', 'darrow', 'larrow', 'rarrow', 'round', 'round4', 'roundtooth', 'sawtooth', 'square'
bbox_transmuter = None
mutation_scale = 1.0       # a value with which attributes of boxstyle (e.g., pad) will be scaled. default=1.
mutation_aspect = None     # The height of the rectangle will be squeezed by this value before the mutation and the mutated box will be stretched by the inverse of it. default=None.

patch = mpatches.FancyBboxPatch(xy=lower_left_point,
                                width=width,
                                height=height,
                                boxstyle=box_style,
                                bbox_transmuter=bbox_transmuter,
                                mutation_scale=mutation_scale,
                                mutation_aspect=mutation_aspect,
                                # COMMON OPTIONS:
                                alpha=alpha,
                                fill=fill,
                                facecolor=fill_color,
                                hatch=fill_pattern,
                                ec=line_color,
                                lw=line_width,
                                joinstyle=join_style,
                                linestyle=line_style)

ax.add_patch(patch)
ax.set_title("matplotlib.patches.FancyBboxPatch\nLArrow", fontsize=TITLE_FONT_SIZE)

# DRAW A FANCY BBOX PATCH #####################################################

ax = axs[next(it)]

lower_left_point = (-4., -3.)
width = 8
height = 6
box_style = 'rarrow'       # 'circle', 'darrow', 'larrow', 'rarrow', 'round', 'round4', 'roundtooth', 'sawtooth', 'square'
bbox_transmuter = None
mutation_scale = 1.0       # a value with which attributes of boxstyle (e.g., pad) will be scaled. default=1.
mutation_aspect = None     # The height of the rectangle will be squeezed by this value before the mutation and the mutated box will be stretched by the inverse of it. default=None.

patch = mpatches.FancyBboxPatch(xy=lower_left_point,
                                width=width,
                                height=height,
                                boxstyle=box_style,
                                bbox_transmuter=bbox_transmuter,
                                mutation_scale=mutation_scale,
                                mutation_aspect=mutation_aspect,
                                # COMMON OPTIONS:
                                alpha=alpha,
                                fill=fill,
                                facecolor=fill_color,
                                hatch=fill_pattern,
                                ec=line_color,
                                lw=line_width,
                                joinstyle=join_style,
                                linestyle=line_style)

ax.add_patch(patch)
ax.set_title("matplotlib.patches.FancyBboxPatch\nRArrow", fontsize=TITLE_FONT_SIZE)

# DRAW A FANCY BBOX PATCH #####################################################

ax = axs[next(it)]

lower_left_point = (-4., -3.)
width = 8
height = 6
box_style = mpatches.BoxStyle.Round(pad=0.3, rounding_size=2.)
bbox_transmuter = None
mutation_scale = 1.0       # a value with which attributes of boxstyle (e.g., pad) will be scaled. default=1.
mutation_aspect = None     # The height of the rectangle will be squeezed by this value before the mutation and the mutated box will be stretched by the inverse of it. default=None.

patch = mpatches.FancyBboxPatch(xy=lower_left_point,
                                width=width,
                                height=height,
                                boxstyle=box_style,
                                bbox_transmuter=bbox_transmuter,
                                mutation_scale=mutation_scale,
                                mutation_aspect=mutation_aspect,
                                # COMMON OPTIONS:
                                alpha=alpha,
                                fill=fill,
                                facecolor=fill_color,
                                hatch=fill_pattern,
                                ec=line_color,
                                lw=line_width,
                                joinstyle=join_style,
                                linestyle=line_style)

ax.add_patch(patch)
ax.set_title("matplotlib.patches.FancyBboxPatch\nRound", fontsize=TITLE_FONT_SIZE)

# DRAW A FANCY BBOX PATCH #####################################################

ax = axs[next(it)]

lower_left_point = (-4., -3.)
width = 8
height = 6
box_style = mpatches.BoxStyle.Round4(pad=0.3, rounding_size=1.)
bbox_transmuter = None
mutation_scale = 1.0       # a value with which attributes of boxstyle (e.g., pad) will be scaled. default=1.
mutation_aspect = None     # The height of the rectangle will be squeezed by this value before the mutation and the mutated box will be stretched by the inverse of it. default=None.

patch = mpatches.FancyBboxPatch(xy=lower_left_point,
                                width=width,
                                height=height,
                                boxstyle=box_style,
                                bbox_transmuter=bbox_transmuter,
                                mutation_scale=mutation_scale,
                                mutation_aspect=mutation_aspect,
                                # COMMON OPTIONS:
                                alpha=alpha,
                                fill=fill,
                                facecolor=fill_color,
                                hatch=fill_pattern,
                                ec=line_color,
                                lw=line_width,
                                joinstyle=join_style,
                                linestyle=line_style)

ax.add_patch(patch)
ax.set_title("matplotlib.patches.FancyBboxPatch\nRound4", fontsize=TITLE_FONT_SIZE)

# DRAW A FANCY BBOX PATCH #####################################################

ax = axs[next(it)]

lower_left_point = (-4., -3.)
width = 8
height = 6
box_style = mpatches.BoxStyle.Roundtooth(pad=0.3, tooth_size=0.5)
bbox_transmuter = None
mutation_scale = 1.0       # a value with which attributes of boxstyle (e.g., pad) will be scaled. default=1.
mutation_aspect = None     # The height of the rectangle will be squeezed by this value before the mutation and the mutated box will be stretched by the inverse of it. default=None.

patch = mpatches.FancyBboxPatch(xy=lower_left_point,
                                width=width,
                                height=height,
                                boxstyle=box_style,
                                bbox_transmuter=bbox_transmuter,
                                mutation_scale=mutation_scale,
                                mutation_aspect=mutation_aspect,
                                # COMMON OPTIONS:
                                alpha=alpha,
                                fill=fill,
                                facecolor=fill_color,
                                hatch=fill_pattern,
                                ec=line_color,
                                lw=line_width,
                                joinstyle=join_style,
                                linestyle='solid')

ax.add_patch(patch)
ax.set_title("matplotlib.patches.FancyBboxPatch\nRoundtooth", fontsize=TITLE_FONT_SIZE)

# DRAW A FANCY BBOX PATCH #####################################################

ax = axs[next(it)]

lower_left_point = (-4., -3.)
width = 8
height = 6
box_style = mpatches.BoxStyle.Sawtooth(pad=0.3, tooth_size=0.5)
bbox_transmuter = None
mutation_scale = 1.0       # a value with which attributes of boxstyle (e.g., pad) will be scaled. default=1.
mutation_aspect = None     # The height of the rectangle will be squeezed by this value before the mutation and the mutated box will be stretched by the inverse of it. default=None.

patch = mpatches.FancyBboxPatch(xy=lower_left_point,
                                width=width,
                                height=height,
                                boxstyle=box_style,
                                bbox_transmuter=bbox_transmuter,
                                mutation_scale=mutation_scale,
                                mutation_aspect=mutation_aspect,
                                # COMMON OPTIONS:
                                alpha=alpha,
                                fill=fill,
                                facecolor=fill_color,
                                hatch=fill_pattern,
                                ec=line_color,
                                lw=line_width,
                                joinstyle=join_style,
                                linestyle='solid')

ax.add_patch(patch)
ax.set_title("matplotlib.patches.FancyBboxPatch\nSawtooth", fontsize=TITLE_FONT_SIZE)

# DRAW A POLYGON ##############################################################

ax = axs[next(it)]

points = np.array([[-1., 0.],    # a numpy array with shape Nx2
                   [-3., 0.],
                   [-3., -2.]])
closed = False

patch = mpatches.Polygon(xy=points,
                         closed=closed,
                         # COMMON OPTIONS:
                         alpha=alpha,
                         fill=fill,
                         facecolor=fill_color,
                         hatch=fill_pattern,
                         ec=line_color,
                         lw=line_width,
                         joinstyle=join_style,
                         linestyle='solid')

ax.add_patch(patch)

###

points = np.array([[1., 0.],    # a numpy array with shape Nx2
                   [3., 0.],
                   [3., 2.]])
closed = True

patch = mpatches.Polygon(xy=points,
                         closed=closed,
                         # COMMON OPTIONS:
                         alpha=alpha,
                         fill=fill,
                         facecolor=fill_color,
                         hatch=fill_pattern,
                         ec=line_color,
                         lw=line_width,
                         joinstyle=join_style,
                         linestyle='solid')

ax.add_patch(patch)

ax.set_title("matplotlib.patches.Polygon", fontsize=TITLE_FONT_SIZE)

# DRAW A REGULAR POLYGON ######################################################

ax = axs[next(it)]

center = (-2.5, 2.5)
num_vertices = 3
radius = 2.               # the distance from the center to each of the vertices
orientation_rad = 0.      # rotates the polygon (in radians)

patch = mpatches.RegularPolygon(xy=center,
                                numVertices=num_vertices,
                                radius=radius,
                                orientation=orientation_rad,
                                # COMMON OPTIONS:
                                alpha=alpha,
                                fill=fill,
                                facecolor=fill_color,
                                hatch=fill_pattern,
                                ec=line_color,
                                lw=line_width,
                                joinstyle=join_style,
                                linestyle='solid')

ax.add_patch(patch)

###

center = (2.5, 2.5)
num_vertices = 4
radius = 2.                       # the distance from the center to each of the vertices
orientation_rad = math.pi/2.      # rotates the polygon (in radians)

patch = mpatches.RegularPolygon(xy=center,
                                numVertices=num_vertices,
                                radius=radius,
                                orientation=orientation_rad,
                                # COMMON OPTIONS:
                                alpha=alpha,
                                fill=fill,
                                facecolor=fill_color,
                                hatch=fill_pattern,
                                ec=line_color,
                                lw=line_width,
                                joinstyle=join_style,
                                linestyle='solid')

ax.add_patch(patch)

###

center = (2.5, -2.5)
num_vertices = 5
radius = 2.               # the distance from the center to each of the vertices
orientation_rad = 0.      # rotates the polygon (in radians)

patch = mpatches.RegularPolygon(xy=center,
                                numVertices=num_vertices,
                                radius=radius,
                                orientation=orientation_rad,
                                # COMMON OPTIONS:
                                alpha=alpha,
                                fill=fill,
                                facecolor=fill_color,
                                hatch=fill_pattern,
                                ec=line_color,
                                lw=line_width,
                                joinstyle=join_style,
                                linestyle='solid')

ax.add_patch(patch)

###

center = (-2.5, -2.5)
num_vertices = 6
radius = 2.               # the distance from the center to each of the vertices
orientation_rad = 0.      # rotates the polygon (in radians)

patch = mpatches.RegularPolygon(xy=center,
                                numVertices=num_vertices,
                                radius=radius,
                                orientation=orientation_rad,
                                # COMMON OPTIONS:
                                alpha=alpha,
                                fill=fill,
                                facecolor=fill_color,
                                hatch=fill_pattern,
                                ec=line_color,
                                lw=line_width,
                                joinstyle=join_style,
                                linestyle='solid')

ax.add_patch(patch)

ax.set_title("matplotlib.patches.RegularPolygon", fontsize=TITLE_FONT_SIZE)

# DRAW A CIRCLE ###############################################################

ax = axs[next(it)]

center = (0., 0.)         # center of the circle
radius = 4.               # radius of the circle

patch = mpatches.Circle(xy=center,
                        radius=radius,
                        # COMMON OPTIONS:
                        alpha=alpha,
                        fill=fill,
                        facecolor=fill_color,
                        hatch=fill_pattern,
                        ec=line_color,
                        lw=line_width,
                        linestyle=line_style)

ax.add_patch(patch)
ax.set_title("matplotlib.patches.Circle", fontsize=TITLE_FONT_SIZE)

# DRAW AN ELLIPSE #############################################################

ax = axs[next(it)]

center = (0., 0.)         # center of the circle
width = 8
height = 6
angle = 0.

patch = mpatches.Ellipse(xy=center,
                         width=width,
                         height=height,
                         angle=angle,
                         # COMMON OPTIONS:
                         alpha=alpha,
                         fill=fill,
                         facecolor=fill_color,
                         hatch=fill_pattern,
                         ec=line_color,
                         lw=line_width,
                         linestyle=line_style)

ax.add_patch(patch)
ax.set_title("matplotlib.patches.Ellipse", fontsize=TITLE_FONT_SIZE)

# DRAW A WEDGE ################################################################

ax = axs[next(it)]

center = (0., 0.)         # center of the circle
radius = 3.
theta1 = -125.
theta2 = 125.
width = None

patch = mpatches.Wedge(center=center,
                       r=radius,
                       theta1=theta1,
                       theta2=theta2,
                       width=width,
                       # COMMON OPTIONS:
                       alpha=alpha,
                       fill=fill,
                       facecolor=fill_color,
                       hatch=fill_pattern,
                       ec=line_color,
                       lw=line_width,
                       joinstyle=join_style,
                       linestyle=line_style)

ax.add_patch(patch)
ax.set_title("matplotlib.patches.Wedge\n(width=None)", fontsize=TITLE_FONT_SIZE)

# DRAW A WEDGE ################################################################

ax = axs[next(it)]

center = (0., 0.)         # center of the circle
radius = 3.
theta1 = -125.
theta2 = 125.
width = 1.

patch = mpatches.Wedge(center=center,
                       r=radius,
                       theta1=theta1,
                       theta2=theta2,
                       width=width,
                       # COMMON OPTIONS:
                       alpha=alpha,
                       fill=fill,
                       facecolor=fill_color,
                       hatch=fill_pattern,
                       ec=line_color,
                       lw=line_width,
                       joinstyle=join_style,
                       linestyle=line_style)

ax.add_patch(patch)
ax.set_title("matplotlib.patches.Wedge\n(width=1)", fontsize=TITLE_FONT_SIZE)

# DRAW AN ARC #################################################################

ax = axs[next(it)]

center = (0., 0.)         # center of ellipse
width = 4.                # length of horizontal axis
height = 2.               # length of vertical axis
rotation = 45.            # rotation in degrees (anti-clockwise)
start_angle = -125.       # starting angle of the arc in degrees
end_angle = 95.           # ending angle of the arc in degrees

patch = mpatches.Arc(xy=center,
                     width=width,
                     height=height,
                     angle=rotation,
                     theta1=start_angle,
                     theta2=end_angle,
                     # COMMON OPTIONS:
                     alpha=alpha,
                     hatch=fill_pattern,
                     ec=line_color,
                     lw=line_width,
                     joinstyle=join_style,
                     linestyle=line_style)

ax.add_patch(patch)
ax.set_title("matplotlib.patches.Arc", fontsize=TITLE_FONT_SIZE)

# DRAW A PATH PATCH ###########################################################

# See: https://matplotlib.org/api/path_api.html#module-matplotlib.path

ax = axs[next(it)]

path = mpath.Path
path_data = [
                (path.MOVETO, (1.58, -2.57)),
                (path.CURVE4, (0.35, -1.1)),
                (path.CURVE4, (-1.75, 2.0)),
                (path.CURVE4, (0.375, 2.0)),
                (path.LINETO, (0.85, 1.15)),
                (path.CURVE4, (2.2, 3.2)),
                (path.CURVE4, (3, 0.05)),
                (path.CURVE4, (2.0, -0.5)),
                (path.CLOSEPOLY, (1.58, -2.57)),
            ]

codes, verts = zip(*path_data)

path = mpath.Path(verts, codes)
patch = mpatches.PathPatch(path,
                           # COMMON OPTIONS:
                           alpha=alpha,
                           fill=fill,
                           facecolor=fill_color,
                           hatch=fill_pattern,
                           ec=line_color,
                           lw=line_width,
                           joinstyle=join_style,
                           linestyle=line_style)

ax.add_patch(patch)

# plot control points and connecting lines

x, y = zip(*path.vertices)
line, = ax.plot(x, y, 'go-', alpha=0.5, markersize=3)

ax.set_title("matplotlib.patches.Path", fontsize=TITLE_FONT_SIZE)


# DISPLAY TEXT ################################################################

ax = axs[next(it)]

line = mlines.Line2D((-1, 1), (0, 0), alpha=0.5, lw=1, linestyle="dotted", color="green")
ax.add_line(line)

line = mlines.Line2D((0, 0), (-1, 1), alpha=0.5, lw=1, linestyle="dotted", color="green")
ax.add_line(line)

text = "Hello"
fontsize = 32.
with_dash = False

ax.text(x=0.,
        y=0.,
        s=text,
        fontsize=fontsize,
        alpha=alpha,
        color="blue",
        horizontalalignment='center',
        verticalalignment='center',
        withdash=with_dash)

ax.set_title("Axes.text", fontsize=TITLE_FONT_SIZE)

# SAVE FILE ###################################################################

plt.tight_layout()
plt.savefig("draw_geometric_shapes.png")

# DISPLAY FIGURES #############################################################

plt.show()
