sphere(30);
translate([100, 0, 0]) cube(60, center=true);
translate([200, 0, 0]) cylinder(r=30,  h=50, center=true);
translate([300, 0, 0]) cylinder(r1=30, r2=10, h=50, $fn=20);
translate([400, 0, 0]) cylinder(r1=30, r2=0,  h=50);
