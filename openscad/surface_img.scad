// See http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#Surface

scale([1, 1, 0.1]) {
  surface(file = "jdhp_org.png", center = true, invert = true);
}