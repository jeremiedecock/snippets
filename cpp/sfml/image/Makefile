CC = g++

EXEC = image
OBJS = $(patsubst %.cc,%.o,$(wildcard *.cc))

CFLAGS = 
LIBS = -lsfml-graphics -lsfml-window -lsfml-system

.PHONY : all clean init

all : $(EXEC)

%.o : %.cc
	$(CC) $(CFLAGS) -o $@ -c $<

$(EXEC) : $(OBJS)
	$(CC) -o $@ $^ $(LIBS)

clean :
	@rm *.o new_image.png 2> /dev/null

init : clean
	rm $(EXEC) 2> /dev/null

