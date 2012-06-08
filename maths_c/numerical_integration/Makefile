CC = gcc
AR = ar

EXEC = numerical_integration
LIB = numerical_integration.a
OBJS = $(patsubst %.c,%.o,$(wildcard *.c))

CFLAGS = 
LIBS = -lm

.PHONY : all clean init

all : $(EXEC)

%.o : %.c
	$(CC) $(CFLAGS) -o $@ -c $<

$(LIB) : $(OBJS)
	$(AR) crs $@ $^

$(EXEC) : $(LIB)
	$(CC) -o $@ $^ $(LIBS)

clean :
	@rm *.o 2> /dev/null

init : clean
	rm $(EXEC) $(LIB) 2> /dev/null

