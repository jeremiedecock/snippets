// See http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#hull
// and http://reprapide.fr/tutoriel-openscad-hull-et-minkowski

$fn=50;

hull() {
   translate([0,20,0]) cube(4);
   sphere(12);
}

