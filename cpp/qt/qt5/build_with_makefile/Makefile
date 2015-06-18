CC = g++
EXEC = hello
OBJS = $(patsubst %.cc,%.o,$(wildcard *.cc))

CFLAGS = `pkg-config --cflags Qt5Widgets`
LIBS = `pkg-config --libs Qt5Widgets`

.PHONY : all clean init

all : $(EXEC)

%.o : %.cc
	# The -fPIC flag seems to be required for Qt5...
	$(CC) -fPIC $(CFLAGS) -o $@ -c $<

$(EXEC) : $(OBJS)
	$(CC) -o $@ $^ $(LIBS)

clean :
	rm *.o

init : clean
	rm $(EXEC)
