# USAGE: blender --background --python blender_background_hello.py

# See http://wiki.blender.org/index.php/Doc:2.6/Manual/Extensions/Python

import bpy

print('Prints the names of all objects belonging to the Blender scene with name "Scene":')
for object in bpy.data.scenes['Scene'].objects:
    print(object.name)
