// Raspicam

// Copyright (c) 2014, Jérémie Decock (jd.jdhp@gmail.com)


// BODY /////////////////////////////////////

module body(board_width, board_height, board_depth, board_corner_radius, screw_hole_radius, screw_hole_spacing, screw_hole_depth, num_screw_holes, camera_screw_holes_radius, camera_screw_holes_spacing_x, camera_screw_holes_spacing_y, camera_holes_width, hinge_radius_in, hinge_radius_out, hinge_slot_length) {
    difference() {
        union() {
            difference() {
                body_main_board(board_width, board_height, board_depth, board_corner_radius);

                #union() {
                    translate([-board_width/2 + 10, 0, 0]){
                        body_screw_holes(screw_hole_radius, screw_hole_spacing, screw_hole_depth, num_screw_holes);
                    }

                    translate([board_width/2 - camera_screw_holes_spacing_x/2 - 10, 0, 0]){
                        body_camera_screw_holes(camera_screw_holes_radius, camera_screw_holes_spacing_x, camera_screw_holes_spacing_y, screw_hole_depth);
                        translate([-camera_screw_holes_spacing_x/2, 0, 0]){
                            body_camera_holes(camera_holes_width, screw_hole_depth);
                        }
                    }
                }
            }
            translate([-board_width/2, 0, hinge_radius_out - board_depth/2]) {
                rotate(a=[90,0,0]) {
                    body_hinge(hinge_radius_in, hinge_radius_out, board_height);
                }
            }
        }
        #translate([-board_width/2, 0, hinge_radius_out - board_depth/2]) {
            cube([hinge_radius_out * 2 + 2, hinge_slot_length, hinge_radius_out * 2 + 2], center=true);
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
		translate([i*spacing, 0, 0]) {        
			cylinder(r=radius, h=depth, center=true);
		}
	}
}

module body_camera_screw_holes(radius, spacing_x, spacing_y, depth) {
	$fn=50;
	
	for (i = [-1, 1]) {    
        for (j = [-1, 1]) {    
            translate([i*spacing_x/2, j*spacing_y/2, 0]) {        
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
        #cylinder(r=radius_in, h=length+10, center=true, $fn=50);
    }
}


// HINGE SCREW //////////////////////////////

module hinge_screw(radius, head_radius, length, head_length) {
    cylinder(r=head_radius, h=head_length, $fn=8);
    translate([0, 0, head_length/2]) cylinder(r=radius, h=length, $fn=50);

    translate([15, 0, 0]) {
        difference() {
            cylinder(r=head_radius, h=head_length, $fn=8);
            #translate([0, 0, head_length/2]) cylinder(r=radius, h=length, $fn=50);
        }
    }
}


// FEET /////////////////////////////////////

module feet(board_width, board_height, board_depth, board_corner_radius, screw_holes_radius, screw_holes_spacing_x, screw_holes_spacing_y, screw_hole_depth, hinge_length, hinge_radius_in, hinge_radius_out, hinge_shelf_width, ventilation_holes_radius) {
    difference() {
        feet_main_board(board_width, board_height, board_depth, board_corner_radius);
        #feet_screw_holes(screw_holes_radius, screw_holes_spacing_x, screw_holes_spacing_y, screw_hole_depth);
        #feet_ventilation_holes(ventilation_holes_radius, screw_hole_depth);
    }

    translate([board_width/2 + hinge_shelf_width/2, 0, 0]) {
        cube([hinge_shelf_width, hinge_length, board_depth], center=true);
    }

    translate([board_width/2 + hinge_shelf_width, 0, hinge_radius_out - board_depth/2]) {
        rotate(a=[90,0,0]) {
            feet_hinge(radius_in=hinge_radius_in, radius_out=hinge_radius_out, length=hinge_length);
        }
    }
}

module feet_screw_holes(radius, spacing_x, spacing_y, depth) {
	$fn=50;
	
	for (i = [-1, 1]) {    
        for (j = [-1, 1]) {    
            translate([i*spacing_x/2, j*spacing_y/2, 0]) {        
                cylinder(r=radius, h=depth, center=true);
            }
        }
	}
}

module feet_ventilation_holes(radius, depth) {
	$fn=50;
	
    translate([0, 0, 0]) {        
        cylinder(r=radius, h=depth, center=true);
    }
}

module feet_main_board(width, height, depth, radius) {
	$fn=50;
	//minkowski()
	//{
		cube([width, height, depth], center=true);
	//	cylinder(r=radius, h=depth, center=true);
	//}
}

module feet_hinge(radius_in, radius_out, length) {
    difference() {
        cylinder(r=radius_out, h=length, center=true, $fn=50);
        #cylinder(r=radius_in, h=length+10, center=true, $fn=50);
    }
}


/////////////////////////////////////////////

assign(feet_board_width=98,
       feet_board_height=65,
       feet_board_depth=3,
       feet_board_corner_radius=3,
       feet_screw_holes_radius=1.5,
       feet_screw_holes_spacing_x=70,
       feet_screw_holes_spacing_y=30,
       feet_screw_hole_depth=10,
       feet_hinge_shelf_width=20,
       feet_ventilation_holes_radius=3,
       body_board_width=100,
       body_board_height=40,
       body_board_depth=3,
       body_board_corner_radius=3,
       body_screw_hole_radius=1.5,
       body_screw_hole_spacing=5,
       body_screw_hole_depth=10,
       body_num_screw_holes=9,
       body_camera_screw_holes_radius=1,
       body_camera_screw_holes_spacing_x=12,
       body_camera_screw_holes_spacing_y=20,
       body_camera_holes_width=8,
       hinge_radius=1.5,
       hinge_head_radius=4.6,
       hinge_head_length=5) {

    color([0,0,1]) {
        translate([0, 50, body_board_depth/2]) {
            body(board_width=body_board_width, board_height=body_board_height, board_depth=body_board_depth, board_corner_radius=body_board_corner_radius, screw_hole_radius=body_screw_hole_radius, screw_hole_spacing=body_screw_hole_spacing, screw_hole_depth=body_screw_hole_depth, num_screw_holes=body_num_screw_holes, camera_screw_holes_radius=body_camera_screw_holes_radius, camera_screw_holes_spacing_x=body_camera_screw_holes_spacing_x, camera_screw_holes_spacing_y=body_camera_screw_holes_spacing_y, camera_holes_width=body_camera_holes_width, hinge_radius_in=hinge_radius + 0.5, hinge_radius_out=hinge_radius + 0.5 + feet_board_depth, hinge_slot_length=body_board_height / 3 + 1);
        }
    }

    color([1,0,0]) {
        translate([0, -50, feet_board_depth/2]) {
            feet(board_width=feet_board_width, board_height=feet_board_height, board_depth=feet_board_depth, board_corner_radius=feet_board_corner_radius, screw_holes_radius=feet_screw_holes_radius, screw_holes_spacing_x=feet_screw_holes_spacing_x, screw_holes_spacing_y=feet_screw_holes_spacing_y, screw_hole_depth=feet_screw_hole_depth, hinge_length=body_board_height/3, hinge_radius_in=hinge_radius + 0.5, hinge_radius_out=hinge_radius + 0.5 + feet_board_depth, hinge_shelf_width=feet_hinge_shelf_width, ventilation_holes_radius=feet_ventilation_holes_radius);
        }
    }

    color([0,1,0]) {
        translate([-50, 0, 0]) {
            hinge_screw(radius=hinge_radius, head_radius=hinge_head_radius, length=body_board_height + 1 + hinge_head_length, head_length=hinge_head_length);
        }
    }
}

