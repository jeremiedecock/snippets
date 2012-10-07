CC = g++

CFLAGS = 
LIBS = -lboost_program_options

.PHONY : all clean init

all : hello

hello : hello.cc
	$(CC) -o $@ $(CFLAGS) $< $(LIBS)

clean :
	rm hello 2> /dev/null

init : clean

