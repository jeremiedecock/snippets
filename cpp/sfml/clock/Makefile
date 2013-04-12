CC = g++

EXEC = clock
OBJS = $(patsubst %.cc,%.o,$(wildcard *.cc))

CFLAGS = 
LIBS = -lsfml-system

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

