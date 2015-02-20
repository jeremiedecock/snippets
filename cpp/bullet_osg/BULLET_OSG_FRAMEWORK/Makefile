CC = g++

CFLAGS  = `pkg-config --cflags bullet openscenegraph eigen3` -Wall -pedantic
LDFLAGS = `pkg-config --libs bullet openscenegraph eigen3`

EXEC_NAME = demo
SRC = $(wildcard *.cc)
OBJ = $(SRC:.cc=.o)

.PHONY: $(EXEC_NAME) clean

$(EXEC_NAME): $(OBJ)
	$(CC) $(LDFLAGS) -o $@ $^

%.o : %.cc
	$(CC) $(CFLAGS) -o $@ -c $<

clean:
	rm -f $(OBJ)

init : clean
	rm -f $(EXEC_NAME)
