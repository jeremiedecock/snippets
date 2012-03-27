##Exepcted:
#$CC -fPIC -c func.cc
#$CC -fPIC -I/usr/include/python2.7 -c python_wrapper.cc
#$CC -shared -o cppfunc.so func.o python_wrapper.o -lboost_python

CC = g++
LIB = cppfunc.so
OBJS = func.o python_wrapper.o

CFLAGS = -fPIC `pkg-config --cflags python`
LIBS = -shared -lboost_python

.PHONY : all clean init

all : $(LIB)

%.o : %.cc
	$(CC) $(CFLAGS) -o $@ -c $<

$(LIB) : $(OBJS)
	$(CC) -o $@ $^ $(LIBS)

clean :
	rm *.o

init : clean
	rm $(LIB)

