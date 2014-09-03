// Raspicam

// Copyright (c) 2014, Jérémie Decock (jd.jdhp@gmail.com)


// BODY /////////////////////////////////////

module body(board_width, board_height, board_depth, board_corner_radius, screw_hole_radius, screw_hole_spacing, screw_hole_depth, num_screw_holes, camera_screw_holes_radius, camera_screw_holes_spacing_x, camera_screw_holes_spacing_y, camera_holes_width, hinge_radius_in, hinge_radius_out) {
    difference() {
        union() {
            difference() {
                translate([0, board_width/2, 0]){
                    rotate(a=[0,0,90]){
                        body_main_board(board_width, board_height, board_depth, board_corner_radius);
                    }
                }

                union() {
                    translate([0, board_width - num_screw_holes * screw_hole_spacing - 12.5, 0]){
                    //translate([0, 0, 0]){
                        body_screw_holes(screw_hole_radius, screw_hole_spacing, screw_hole_depth, num_screw_holes);
                    }

                    translate([-camera_screw_holes_spacing_x/2, 10, 0]){
                        body_camera_screw_holes(camera_screw_holes_radius, camera_screw_holes_spacing_x, camera_screw_holes_spacing_y, screw_hole_depth);
                    }
                    
                    translate([0, camera_screw_holes_spacing_y + 10, 0]){
                        body_camera_holes(camera_holes_width, screw_hole_depth);
                    }
                }
            }
            translate([0, board_width, hinge_radius_out - board_depth/2]) {
                rotate(a=[0,90,0]) {
                    body_hinge(hinge_radius_in, hinge_radius_out, board_height);
                }
            }
        }
        translate([0, board_width, hinge_radius_out - board_depth/2]) {
            cube([board_height / 3 + 1, hinge_radius_out * 2 + 2, hinge_radius_out * 2 + 2], center=true);
        }
    }
}

module body_main_board(width, height, depth, radius) {
	$fn=50;
	//minkowski()
	//{
		cube([width, height, depth], center=true);
    //	cylinder(r=radius, h=depth, center=true);
    //}
}

module body_screw_holes(radius, spacing, depth, num) {
	$fn=50;
	
	for (i = [1:num]) {    
		translate([0, i*spacing, 0]) {        
			cylinder(r=radius, h=depth, center=true);
		}
	}
}

module body_camera_screw_holes(radius, spacing_x, spacing_y, depth) {
	$fn=50;
	
	for (i = [0:1]) {    
        for (j = [0:1]) {    
            translate([i*spacing_x, j*spacing_y, 0]) {        
                cylinder(r=radius, h=depth, center=true);
            }
        }
	}
}

module body_camera_holes(width, depth) {
    cube([width, width, depth], center=true);
}

module body_hinge(radius_in, radius_out, length) {
    difference() {
        cylinder(r=radius_out, h=length, center=true, $fn=50);
        translate([0, 0, 0]) {
            cylinder(r=radius_in, h=length+10, center=true, $fn=50);
        }
    }
}

// HINGE SCREW //////////////////////////////

module hinge_screw(radius, head_radius, length, head_length) {
    cylinder(r=head_radius, h=head_length, $fn=8);
    translate([0, 0, 0]) {
        cylinder(r=radius, h=length, $fn=50);
    }
}

// FEET /////////////////////////////////////
module feet(width, height, depth, radius) {
	$fn=50;
	//minkowski()
	//{
		cube([width, height, depth]);
	//	cylinder(r=radius, h=depth, center=true);
	//}
}


color([1,0,0]) translate([0, -100, 0]) feet(98, 65, 3, 3);

color([0,0,1]) translate([0, 0, 0]) body(board_width=100, board_height=40, board_depth=3, board_corner_radius=3, screw_hole_radius=1.5, screw_hole_spacing=5, screw_hole_depth=10, num_screw_holes=9, camera_screw_holes_radius=1, camera_screw_holes_spacing_x=20, camera_screw_holes_spacing_y=12, camera_holes_width=8, hinge_radius_in=1.6, hinge_radius_out=4.6);

color([0,1,0]) translate([-50, 0, 0]) hinge_screw(radius=1.5, head_radius=3, length=65, head_length=5);

