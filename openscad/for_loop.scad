// See http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Conditional_and_Iterator_Functions

for (i = [1:3])
{
	translate([0, i*100, 0])
	{
		sphere(30);
	}
}