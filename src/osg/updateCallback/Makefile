updateCallback : updateCallback.o
	g++ -o updateCallback `pkg-config --libs openscenegraph` updateCallback.o

updateCallback.o : updateCallback.cc
	g++ -c -Wall updateCallback.cc

clean :
	rm *.o
	rm updateCallback
