CC = g++

# Boost::graph doesn't require to link a library
CFLAGS = 
LIBS = 

.PHONY : all clean init

all : hello

chrono : hello.cc
	$(CC) -o $@ $(CFLAGS) $(LIBS) $<

clean :
	rm hello 2> /dev/null

init : clean

