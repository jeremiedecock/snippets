// See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/DXF_Extrusion
//     https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_the_2D_Subsystem#import_dxf

rotate_extrude(convexity=10)
	import(file="2d_shape.dxf", layer="root");
