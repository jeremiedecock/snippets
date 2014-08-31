// See http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#Assign_Statement

assign (x = 10, y = 20, z = 30)
{
	cube([x, y, z], center = true);
}