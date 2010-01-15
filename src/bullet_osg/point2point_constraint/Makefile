point2pointConstraint : point2pointConstraint.o
	g++ -o point2pointConstraint `pkg-config --libs openscenegraph` point2pointConstraint.o ../../bullet_lib/libbulletdynamics.a ../../bullet_lib/libbulletcollision.a ../../bullet_lib/libbulletmath.a

point2pointConstraint.o : point2pointConstraint.cc
	g++ -c -Wall -I../../bullet_src/ point2pointConstraint.cc

clean :
	rm *.o
	rm point2pointConstraint
