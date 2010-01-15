fallingCapsules : fallingCapsules.o
	g++ -o fallingCapsules `pkg-config --libs openscenegraph` fallingCapsules.o ../../bullet_lib/libbulletdynamics.a ../../bullet_lib/libbulletcollision.a ../../bullet_lib/libbulletmath.a

fallingCapsules.o : fallingCapsules.cc
	g++ -c -Wall -I../../bullet_src/ fallingCapsules.cc

clean :
	rm *.o
	rm fallingCapsules
