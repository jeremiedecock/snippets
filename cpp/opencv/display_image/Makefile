CC = g++

EXEC = display_img
OBJS = $(patsubst %.cc,%.o,$(wildcard *.cc))

CFLAGS = `pkg-config --cflags opencv`
LIBS = `pkg-config --libs opencv`

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

