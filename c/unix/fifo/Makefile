CC = gcc

CFLAGS = -Wall
LIBS = 

.PHONY : all clean init

all : server client

server : server.c
	$(CC) -o $@ $(CFLAGS) $< $(LIBS)

client : client.c
	$(CC) -o $@ $(CFLAGS) $< $(LIBS)

clean :
	rm server client 2> /dev/null

init : clean

