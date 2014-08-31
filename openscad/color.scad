// See http://en.wikibooks.org/wiki/OpenSCAD_User_Manual

// Changing the colors only works in Preview mode (F5). Render mode (F6) does not currently support color.

color([1,0,0]) cube([2,3,4]);
translate([3,0,0])
color([0,1,0]) cube([2,3,4]);
translate([6,0,0])
color([0,0,1]) cube([2,3,4]);

