CC = g++

CFLAGS = -I../../../lib/bullet/src/ -Wall -pedantic -g -c
LIBS = `pkg-config --libs openscenegraph` -lm ../../../lib/bullet/lib/libbulletdynamics.a ../../../lib/bullet/lib/libbulletcollision.a ../../../lib/bullet/lib/libbulletmath.a

EXEC_NAME = demo
OBJECTS = $(patsubst %.cc,%.o,$(wildcard *.cc))

.PHONY: $(EXEC_NAME) clean

$(EXEC_NAME): $(OBJECTS)
	echo $(OBJECTS)
	$(CC) -o $(EXEC_NAME) $(OBJECTS) $(LIBS)

%.o : %.cc
	$(CC) $(CFLAGS) $<

clean:
	rm -f $(OBJECTS)
	rm -f $(EXEC_NAME)
