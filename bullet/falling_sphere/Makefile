BasicDemo : BasicDemo.o main.o
	g++ -o BasicDemo BasicDemo.o ../../bullet_lib/libbulletdynamics.a ../../bullet_lib/libbulletcollision.a ../../bullet_lib/libbulletmath.a ../../opengl_lib/libbulletopenglsupport.a -L/usr/X11R6/lib -lGL -lGLU -lglut -lX11 -lXmu -lXi -lm

BasicDemo.o : BasicDemo.cpp
	g++ -c -Wall -I../../bullet_src/ -I../../opengl_src/ BasicDemo.cpp

main.o : main.cpp
	g++ -c -Wall -I../../bullet_src/ -I../../opengl_src/ main.cpp

clean :
	rm *.o
	rm BasicDemo
