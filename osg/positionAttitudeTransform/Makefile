positionAttitudeTransform : positionAttitudeTransform.o
	g++ -o positionAttitudeTransform `pkg-config --libs openscenegraph` positionAttitudeTransform.o

positionAttitudeTransform.o : positionAttitudeTransform.cc
	g++ -c -Wall positionAttitudeTransform.cc

clean :
	rm *.o
	rm positionAttitudeTransform
