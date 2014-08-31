// See http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#Modifier_Characters
// Ignore this subtree for the normal rendering process and draw it in transparent gray (all transformations are still applied to the nodes in this tree).
// Because the marked subtree is completely ignored, it might have unexpected effects in case it's used for example with the first object in a difference(). In that case this object will be rendered in transparent gray, but it will not be the base for the difference()!
// Usage:
//   % { ... }

difference() {
	cylinder (h = 12, r=5, center = true, $fn=100);
	// first object that will subtracted
	rotate ([90,0,0]) cylinder (h = 15, r=1, center = true, $fn=100);
	// second object that will be subtracted
	%rotate ([0,90,0]) cylinder (h = 15, r=3, center = true, $fn=100);
}