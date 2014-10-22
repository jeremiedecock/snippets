CC = gcc
EXEC = hello
OBJS = $(patsubst %.c,%.o,$(wildcard *.c))

CFLAGS = 
LIBS = 

.PHONY : all clean init

all : $(EXEC)

%.o : %.c
	$(CC) $(CFLAGS) -o $@ -c $<

$(EXEC) : $(OBJS)
	$(CC) -o $@ $^ $(LIBS)

clean :
	rm *.o

init : clean
	rm $(EXEC)
