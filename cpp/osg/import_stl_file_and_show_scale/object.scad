difference() {

    // Create an object of 10mm height and 5mm width / depth
    cube([5, 5, 10], center=true);

    // The first object that will subtracted
    #rotate([90,0,0]) cylinder(h=7, r=1, center=true, $fn=100);

    // The second object that will be subtracted
    #rotate([0,90,0]) cylinder(h=7, r=2, center=true, $fn=100);

}
