// See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_the_2D_Subsystem
//     http://www.openscad.org/cheatsheet/

// Press F6 to render and export to DXF

// Export to DXF from command line: openscad -o 2d_shapes.dxf 2d_shapes.scad

translate([0,  0])  square(size=10, center=true);
translate([0, 20]) square([7,15], center=true);
translate([0, 40]) circle(d=10, $fn=100);       // diameter
translate([0, 60]) circle(10, $fn=100);         // radius
translate([0, 80]) polygon([[0,0], [10,10], [0,5], [-10,10]]);
