linearMotor : linearMotor.o
	g++ -o linearMotor `pkg-config --libs openscenegraph` linearMotor.o ../../bullet_lib/libbulletdynamics.a ../../bullet_lib/libbulletcollision.a ../../bullet_lib/libbulletmath.a

linearMotor.o : linearMotor.cc
	g++ -c -Wall -I../../bullet_src/ linearMotor.cc

clean :
	rm *.o
	rm linearMotor
