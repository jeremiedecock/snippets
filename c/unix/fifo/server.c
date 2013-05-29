#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

#define BUFFSIZE 10

int main(int argc, char ** argv) {

    // MKFIFO
    
    char * fifo_path = "pipe";
    mkfifo(fifo_path, 0666);

    // OPEN
    
    int fd = open(fifo_path, O_RDONLY);
    if(fd==-1) {
        perror("open fifo");
        exit(1);
    }

    // READ
    
    char buff[BUFFSIZE];
    int n = read(fd, buff, BUFFSIZE);
    while(n>0) {
        write(1, buff, n);
        n = read(fd, buff, BUFFSIZE);
    }

    printf("EOF\n");
    close(fd);

    unlink(fifo_path);

    return 0;
}

