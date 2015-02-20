CC = g++

CFLAGS = `pkg-config --cflags bullet` -Wall -pedantic -g -c
LIBS = -lm `pkg-config --libs bullet`

EXEC_NAME = demo
OBJECTS = $(patsubst %.cc,%.o,$(wildcard *.cc))

.PHONY: $(EXEC_NAME) clean

$(EXEC_NAME): $(OBJECTS)
	$(CC) -o $(EXEC_NAME) $(OBJECTS) $(LIBS)

%.o : %.cc
	$(CC) $(CFLAGS) $<

clean:
	rm -f $(OBJECTS)

init:
	rm -f $(EXEC_NAME)
	rm res.dat
	rm res.pdf
