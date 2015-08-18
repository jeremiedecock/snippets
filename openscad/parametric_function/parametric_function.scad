// OpenSCAD parametric graph example

// See the "Examples" section in "lib/2dgraphing.scad"

// See also: http://makerhome.blogspot.fr/2014/01/day-133-broken-heart.html
//           http://makerhome.blogspot.fr/2014/01/day-150-trefoil-torus-knots.html
//           http://makerhome.blogspot.fr/
//           http://makerhome.blogspot.fr/search?updated-max=2014-06-21T19:09:00-07:00&max-results=31&start=53&by-date=false

include <lib/2dgraphing.scad>

// Parameters
line_height = 0.25;
line_thickness = 0.1;
number_of_steps = 9;

// Define the parametric curve
function x(t) = cos(t);
function y(t) = sin(t);

// Make the graph and extrude it
scale([10, 10, 10]) linear_extrude(height = line_height)
    2dgraph([10, 1450], line_thickness, steps=number_of_steps, parametric=true);
