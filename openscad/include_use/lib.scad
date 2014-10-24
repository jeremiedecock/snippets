// See http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Include_Statement

module pipe(r1, r2, h) {
    difference() {
        cylinder(r=r1, h=h, center=true);
        cylinder(r=r2, h=h+1, center=true);
    }
}

// Following commands are called with "include" but not with "use"

echo("Printed with include but not with use");

pipe(4, 2, 100);
