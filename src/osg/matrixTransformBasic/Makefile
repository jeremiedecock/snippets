CC = g++

CFLAGS = -Wall -pedantic -g -c
LIBS = `pkg-config --libs openscenegraph`

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
