##Exepcted:
#$CC -fPIC -c classes.cc
#$CC -fPIC -I/usr/include/python2.7 -c python_wrapper.cc
#$CC -shared -o cppclasses.so classes.o python_wrapper.o -lboost_python

CC = g++
LIB = cppclasses.so
OBJS = $(patsubst %.cc,%.o,$(wildcard *.cc))

CFLAGS = -fPIC `pkg-config --cflags python`
LIBS = -shared -lboost_python

.PHONY : all clean init

all : $(LIB)

%.o : %.cc
	$(CC) $(CFLAGS) -o $@ -c $<

$(LIB) : $(OBJS)
	$(CC) -o $@ $^ $(LIBS)

clean :
	@rm *.o 2> /dev/null

init : clean
	rm $(LIB) 2> /dev/null

