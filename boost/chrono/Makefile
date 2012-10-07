CC = g++

CFLAGS = 
LIBS = -lboost_chrono -lboost_system

.PHONY : all clean init

all : chrono

chrono : chrono.cc
	$(CC) -o $@ $(CFLAGS) $< $(LIBS)

clean :
	rm chrono 2> /dev/null

init : clean

