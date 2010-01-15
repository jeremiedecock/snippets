fallingCubes : fallingCubes.o
	g++ -o fallingCubes `pkg-config --libs openscenegraph` fallingCubes.o ../../bullet_lib/libbulletdynamics.a ../../bullet_lib/libbulletcollision.a ../../bullet_lib/libbulletmath.a

fallingCubes.o : fallingCubes.cc
	g++ -c -Wall -I../../bullet_src/ fallingCubes.cc

clean :
	rm *.o
	rm fallingCubes
