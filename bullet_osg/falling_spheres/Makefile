fallingSpheres : fallingSpheres.o
	g++ -o fallingSpheres `pkg-config --libs openscenegraph` fallingSpheres.o ../../bullet_lib/libbulletdynamics.a ../../bullet_lib/libbulletcollision.a ../../bullet_lib/libbulletmath.a

fallingSpheres.o : fallingSpheres.cc
	g++ -c -Wall -I../../bullet_src/ fallingSpheres.cc

clean :
	rm *.o
	rm fallingSpheres
