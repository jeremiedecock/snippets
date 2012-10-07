CC = g++

# Boost::random doesn't requires to link a library
CFLAGS = 
LIBS = 

.PHONY : all clean init

all : rand_normal rand_uniform_int rand_uniform_real

rand_normal : rand_normal.cc
	$(CC) -o $@ $(CFLAGS) $(LIBS) $<

rand_uniform_int : rand_uniform_int.cc
	$(CC) -o $@ $(CFLAGS) $(LIBS) $<

rand_uniform_real : rand_uniform_real.cc
	$(CC) -o $@ $(CFLAGS) $(LIBS) $<

clean :
	rm rand_normal rand_uniform_int rand_uniform_real 2> /dev/null

init : clean

