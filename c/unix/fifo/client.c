#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

#define BUFFSIZE 10

int main(int argc, char ** argv) {

    // OPEN
    
    char * fifo_path = "pipe";

    int fd = open(fifo_path, O_WRONLY);
    if(fd==-1) {
        perror("open fifo");
        exit(1);
    }

    // READ
    
    char buff[BUFFSIZE];
    int n = read(0, buff, BUFFSIZE);
    while(n>0) {
        write(fd, buff, n);
        n = read(0, buff, BUFFSIZE);
    }

    printf("EOF\n");
    close(fd);

    return 0;
}

