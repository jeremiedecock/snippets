// See http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#CSG_Modeling

intersection() {
	cylinder (h=20, r=5, center=true, $fn=100);
	rotate ([90,0,0]) cylinder (h=20, r=4.5, center=true, $fn=100);
}