// See http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#minkowski
// and http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#.24fa.2C_.24fs_and_.24fn

$fn=50;
minkowski()
{
 cube([10,10,1]);
 cylinder(r=2,h=1);
}