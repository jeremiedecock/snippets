/* 
 * Fork: fork the process multiple times.
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc fork_loop2.c
 * See "man 2 fork" for more info
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char * argv[])
{

    int i;
    for(i=0 ; i<5 ; i++) {

        pid_t pid = fork();

        if(pid == -1) {  // ERROR
            perror("fork");
            exit(EXIT_FAILURE);
        }

        if(pid == 0) {   // CHILD

            printf("start %ld\n", (long) getpid());
            sleep(3);
            printf("exit %ld\n",  (long) getpid());
            exit(EXIT_SUCCESS);

        }

    }
        
    // PARENT
    // Wait the end of all children process
    int status;
    pid_t pid;

    while((pid = wait(&status)) != -1) {
        if(WIFEXITED(status)) {
            printf("PROCESS %ld: EXITED (%d)\n", (long) pid, WEXITSTATUS(status));
        } else if(WIFSIGNALED(status)) {
            printf("PROCESS %ld: SIGNALED (%d)\n", (long) pid, WTERMSIG(status));
            //if(WCOREDUMP(status)) {
            //    printf("COREDUMP\n");
            //} else {
            //    printf("NO COREDUMP\n");
            //}
        }
    }
    
}
