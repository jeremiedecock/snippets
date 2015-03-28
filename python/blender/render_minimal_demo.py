# A minimal example of render of the default scene.
# The blender default scene contain a cube, a lamp and a camera.

# USAGE: blender --background --python render_minimal_demo.py

# See http://wiki.blender.org/index.php/Doc:2.6/Manual/Extensions/Python

import bpy

# Alias
render = bpy.context.scene.render

# Set render resolution
render.resolution_x = 800
render.resolution_y = 600

# Set Scenes output filename 
render.filepath = 'out.png'

# Render Scene and store the scene 
bpy.ops.render.render(write_still=True)
