fallingSphere : fallingSphere.o
	g++ -o fallingSphere `pkg-config --libs openscenegraph` fallingSphere.o ../../bullet_lib/libbulletdynamics.a ../../bullet_lib/libbulletcollision.a ../../bullet_lib/libbulletmath.a

fallingSphere.o : fallingSphere.cc
	g++ -c -Wall -I../../bullet_src/ fallingSphere.cc

clean :
	rm *.o
	rm fallingSphere
