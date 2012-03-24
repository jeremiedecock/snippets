CC = g++
EXEC = hello
OBJS = hello.o

LIBS = `pkg-config --libs QtGui`
CFLAGS = `pkg-config --cflags QtGui`

.PHONY : all clean init

all : $(EXEC)

%.o : %.cc
	$(CC) $(CFLAGS) -o $@ -c $<

$(EXEC) : $(OBJS)
	$(CC) -o $@ $< $(LIBS)

clean :
	rm *.o

init : clean
	rm $(EXEC)
