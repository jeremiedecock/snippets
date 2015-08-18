// Src: http://www.thingiverse.com/thing:11243/#files

/*************
* Examples *
*************/
// To render an example, remove the comments
pi = 3.1415926536;
e = 2.718281828;
// function to convert degrees to radians
function d2r(theta) = theta*360/(2*pi);

/* Cartesian equations */
/* Sine wave */
//pi = 3.14159;
//function _f(x) = 20*sin((1/4)*x);
//function f(x) = _f(d2r(x));
//linear_extrude(height=5)
//	2dgraph([-50, 50], 3, steps=50);

/* Parabola */
//function f(x) = pow(x, 2)/20;
//linear_extrude(height=5)
//	2dgraph([-50, 50], 3, steps=40);

/* Ellipsoid - use a cartesion equation for a half ellipse, then rotate extrude it */
//function f(x) = sqrt((2500-pow(x, 2))/3);
//rotate_extrude(convexity=10, $fn=100) 
//	rotate([0, 0, -90]) 2dgraph([-50, 50], 3, steps=100);

/* Blancmange curve (an approximation)
works best to export to dxf first, then extrude that.
the 2d render takes a long time at this resolution */
//function blancmange(x, n) = abs(round(pow(2, n)*x)-pow(2, n)*x)/pow(2, n); 
//function f(x) = blancmange(x, 0) + blancmange(x, 1) + blancmange(x, 2) + blancmange(x, 3) + blancmange(x, 4) + blancmange(x, 5) + blancmange(x, 6);
////scale([100, 100, 100]) linear_extrude(height=0.125) import_dxf("blancmange.dxf");
//2dgraph([0, 1], 0.02, steps=480);

/* Polar equations */
/* Rose curve */
//function r(theta) = cos(4*theta);
//scale([20, 20, 20]) linear_extrude(height=0.15)
//	2dgraph([0, 720], 0.1, steps=160, polar=true);

/* Archimedes spiral */
//function r(theta) = theta/2*pi;
//scale([0.02, 0.02, 0.02]) linear_extrude(height=150)
//	2dgraph([0, 360*3], 50, steps=100, polar=true);

/* Golden spiral */
//function r(theta) = pow(e, 0.0053468*theta);
//linear_extrude(height=50)
//	2dgraph([0, 7*180], 1, steps=300, polar=true);

/* Parametric equations */
/* 9-pointed star */
//function x(t) = cos(t);
//function y(t) = sin(t);
//scale([10, 10, 10]) linear_extrude(height=0.25)
//	2dgraph([10, 1450], 0.1, steps=9, parametric=true);

/* Squiggly */
//function _x(t) = sin(t)*cos(t) + sin(2*t)*cos(2*t) + sin(3*t)*cos(3*t) + sin(4*t)*cos(4*t);
//function _y(t) = sin(t)*cos(2*t) + sin(3*t)*cos(4*t) + sin(5*t)*cos(6*t) + sin(7*t)*cos(8*t);
//function x(t) = _x(d2r(t));
//function y(t) = _y(d2r(t));
//scale([20, 10, 20]) linear_extrude(height=0.15) 
//	2dgraph([0, 3*pi], 0.06, steps=400, parametric=true);

/* Butterfly curve! */
//function _x(t) = sin(t)*(pow(e, cos(t))-2*cos(4*t)-pow(sin(t/12), 5));
//function _y(t) = cos(t)*(pow(e, cos(t))-2*cos(4*t)-pow(sin(t/12), 5));
//function x(t) = _x(d2r(t));
//function y(t) = _y(d2r(t));
////scale([20, 20, 20]) linear_extrude(height=0.125) import_dxf("butterflycurve.dxf");
//2dgraph([0, 22*pi], 0.06, steps=2000, parametric=true);

/*********************
* End of examples *
*********************/

// These functions are here to help get the slope of each segment, and use that to find points for a correctly oriented polygon
function diffx(x1, y1, x2, y2, th) = cos(atan((y2-y1)/(x2-x1)) + 90)*(th/2);
function diffy(x1, y1, x2, y2, th) = sin(atan((y2-y1)/(x2-x1)) + 90)*(th/2);
function point1(x1, y1, x2, y2, th) = [x1-diffx(x1, y1, x2, y2, th), y1-diffy(x1, y1, x2, y2, th)];
function point2(x1, y1, x2, y2, th) = [x2-diffx(x1, y1, x2, y2, th), y2-diffy(x1, y1, x2, y2, th)];
function point3(x1, y1, x2, y2, th) = [x2+diffx(x1, y1, x2, y2, th), y2+diffy(x1, y1, x2, y2, th)];
function point4(x1, y1, x2, y2, th) = [x1+diffx(x1, y1, x2, y2, th), y1+diffy(x1, y1, x2, y2, th)];
function polarX(theta) = cos(theta)*r(theta);
function polarY(theta) = sin(theta)*r(theta);

module nextPolygon(x1, y1, x2, y2, x3, y3, th) {
	if((x2 > x1 && x2-diffx(x2, y2, x3, y3, th) < x2-diffx(x1, y1, x2, y2, th) || (x2 <= x1 && x2-diffx(x2, y2, x3, y3, th) > x2-diffx(x1, y1, x2, y2, th)))) {
		polygon(
			points = [
				point1(x1, y1, x2, y2, th),
				point2(x1, y1, x2, y2, th),
				// This point connects this segment to the next
				point4(x2, y2, x3, y3, th),
				point3(x1, y1, x2, y2, th),
				point4(x1, y1, x2, y2, th)
			],
			paths = [[0,1,2,3,4]]
		);
	}
	else if((x2 > x1 && x2-diffx(x2, y2, x3, y3, th) > x2-diffx(x1, y1, x2, y2, th) || (x2 <= x1 && x2-diffx(x2, y2, x3, y3, th) < x2-diffx(x1, y1, x2, y2, th)))) {
		polygon(
			points = [
				point1(x1, y1, x2, y2, th),
				point2(x1, y1, x2, y2, th),
				// This point connects this segment to the next
				point1(x2, y2, x3, y3, th),
				point3(x1, y1, x2, y2, th),
				point4(x1, y1, x2, y2, th)
			],
			paths = [[0,1,2,3,4]]
		);
	}
	else {
		polygon(
			points = [
				point1(x1, y1, x2, y2, th),
				point2(x1, y1, x2, y2, th),
				point3(x1, y1, x2, y2, th),
				point4(x1, y1, x2, y2, th)
			],
			paths = [[0,1,2,3]]
		);
	}
}

module 2dgraph(bounds=[-10,10], th=2, steps=10, polar=false, parametric=false) {
	step = (bounds[1]-bounds[0])/steps;
	union() {
		for(i = [bounds[0]:step:bounds[1]-step]) {
			if(polar) {
				nextPolygon(polarX(i), polarY(i), polarX(i+step), polarY(i+step), polarX(i+2*step), polarY(i+2*step), th);
			}
			else if(parametric) {
				nextPolygon(x(i), y(i), x(i+step), y(i+step), x(i+2*step), y(i+2*step), th);
			}
			else {
				nextPolygon(i, f(i), i+step, f(i+step), i+2*step, f(i+2*step), th);
			}
		}
	}
}
