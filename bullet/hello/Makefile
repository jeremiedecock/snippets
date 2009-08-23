hello : hello.o
	g++ -o hello hello.o ../../bullet_lib/libbulletdynamics.a ../../bullet_lib/libbulletcollision.a ../../bullet_lib/libbulletmath.a

hello.o : hello.cc
	g++ -c -Wall -I../../bullet_src/ hello.cc

clean :
	rm *.o
	rm hello
