CC = g++

CFLAGS = -I../../include/bullet/ -Wall -pedantic -g -c
LIBS = -lm ../../lib/libbulletdynamics.a ../../lib/libbulletcollision.a ../../lib/libbulletmath.a

EXEC_NAME = demo
OBJECTS = $(patsubst %.cc,%.o,$(wildcard *.cc))

.PHONY: $(EXEC_NAME) clean

$(EXEC_NAME): $(OBJECTS)
	$(CC) -o $(EXEC_NAME) $(OBJECTS) $(LIBS)

%.o : %.cc
	$(CC) $(CFLAGS) $<

clean:
	rm -f $(OBJECTS)
	rm -f $(EXEC_NAME)
