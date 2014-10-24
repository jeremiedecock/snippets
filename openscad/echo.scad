// See http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#Echo_Statements
//     http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#String_Functions

// preview: F5
// compile and render: F6

var1 = "world";
var2 = 2;

echo("Hello", var1, var2);
echo(str("Hello ", var1, " ", var2));

