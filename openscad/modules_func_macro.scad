// See http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#Modules

module hole(distance, rot, size) {
     rotate(a = rot, v = [1, 0, 0]) {
         translate([0, distance, 0]) {
             cylinder(r = size, h = 100, center = true);
         }
     }
}

hole(0, 90, 10);
hole(0, 180, 10);