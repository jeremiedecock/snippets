fallingCube : fallingCube.o
	g++ -o fallingCube `pkg-config --libs openscenegraph` fallingCube.o ../../bullet_lib/libbulletdynamics.a ../../bullet_lib/libbulletcollision.a ../../bullet_lib/libbulletmath.a

fallingCube.o : fallingCube.cc
	g++ -c -Wall -I../../bullet_src/ fallingCube.cc

clean :
	rm *.o
	rm fallingCube
