/* 
 * Pipes + fork.
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc pipe.c
 * See "man 2 fork" for more info
 * See "man 2 pipe" for more info
 *
 */

#define BUFFER_SIZE 64

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

int main(int argc, char * argv[])
{

    int pipe_desc[2];

    // create a pipe
    if(pipe(pipe_desc) == -1) {
        perror("pipe");
        exit(EXIT_FAILURE);
    }

    // fork the processus
    pid_t pid = fork();
    if(pid == -1) {
        perror("fork");
        exit(EXIT_FAILURE);
    }

    if(pid == 0) {         // CHILD
        close(pipe_desc[0]);          // close the read descriptor    

        char * msg = "hello";
        write(pipe_desc[1], msg, strlen(msg));

        close(pipe_desc[1]);          // close the write descriptor (EOF)
        exit(0);
    }

    // PARENT
    close(pipe_desc[1]);              // close the write descriptor   

    char buffer[BUFFER_SIZE];
    int n_read = read(pipe_desc[0], buffer, BUFFER_SIZE);
    while(n_read != 0) {
        write(1, buffer, n_read);     // print the message on stdout
        n_read = read(pipe_desc[0], buffer, BUFFER_SIZE);
    }

    close(pipe_desc[0]);              // close the read descriptor    

    wait(NULL);                       // wait the child (useless ?)

}
