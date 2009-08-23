collisionMask : collisionMask.o
	g++ -o collisionMask `pkg-config --libs openscenegraph` collisionMask.o ../../bullet_lib/libbulletdynamics.a ../../bullet_lib/libbulletcollision.a ../../bullet_lib/libbulletmath.a

collisionMask.o : collisionMask.cc
	g++ -c -Wall -I../../bullet_src/ collisionMask.cc

clean :
	rm *.o
	rm collisionMask
