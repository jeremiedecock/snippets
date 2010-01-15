hingeConstraint : hingeConstraint.o
	g++ -o hingeConstraint `pkg-config --libs openscenegraph` hingeConstraint.o ../../bullet_lib/libbulletdynamics.a ../../bullet_lib/libbulletcollision.a ../../bullet_lib/libbulletmath.a

hingeConstraint.o : hingeConstraint.cc
	g++ -c -Wall -I../../bullet_src/ hingeConstraint.cc

clean :
	rm *.o
	rm hingeConstraint
