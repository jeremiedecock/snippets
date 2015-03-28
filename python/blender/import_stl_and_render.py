# A minimal example of render of the default scene.
# The blender default scene contain a cube, a lamp and a camera.

# USAGE: blender empty.blend --background --python import_stl_and_render.py

# See http://wiki.blender.org/index.php/Doc:2.6/Manual/Extensions/Python

import bpy

# Import the STL file
bpy.ops.import_mesh.stl(filepath="test.stl")
#bpy.ops.import_mesh.stl(filepath="test.stl", filter_glob="*.stl",  files=[{"name1":"test1.stl", "name2":"test2.stl"}], directory="")

# Alias
render = bpy.context.scene.render

# Set render resolution
render.resolution_x = 800
render.resolution_y = 600

# Set Scenes output filename 
render.filepath = 'out.png'

# Render Scene and store the scene 
bpy.ops.render.render(write_still=True)
