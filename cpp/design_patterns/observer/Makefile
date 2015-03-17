CC = g++

CFLAGS = -std=c++11 -Wall -pedantic -g -c
LIBS = 

EXEC_NAME = demo
OBJECTS = $(patsubst %.cpp,%.o,$(wildcard *.cpp))

.PHONY: $(EXEC_NAME) clean

$(EXEC_NAME): $(OBJECTS)
	$(CC) -o $(EXEC_NAME) $(OBJECTS) $(LIBS)

%.o : %.cpp
	$(CC) $(CFLAGS) $<

clean:
	rm -f $(OBJECTS)

init : clean
	rm -f $(EXEC_NAME)
