// See http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#Modifier_Characters
// Ignore the rest of the design and use this subtree as design root.
// Usage
//   ! { ... }


difference() {
	cube(10, center = true);
	translate([0, 0, 5]) {
		!rotate([90, 0, 0]) {
			#cylinder(r = 2, h = 20, center = true, $fn = 40);
		}
	}
}