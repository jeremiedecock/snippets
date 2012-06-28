CC = g++

EXEC = random
OBJS = $(patsubst %.cc,%.o,$(wildcard *.cc))

CFLAGS = `pkg-config --cflags eigen3`
LIBS =

.PHONY : all clean init

all : $(EXEC)

%.o : %.cc
	$(CC) $(CFLAGS) -o $@ -c $<

$(EXEC) : $(OBJS)
	$(CC) -o $@ $^ $(LIBS)

clean :
	@rm *.o 2> /dev/null

init : clean
	rm $(EXEC) 2> /dev/null

