/* 
 * Fork: fork the process and display resulting PID and PPID.
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc fork2.c
 * See "man 2 fork" for more info
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char * argv[])
{
    pid_t proc_id = fork();

    if(proc_id == -1) {       // ERROR

        perror("fork");
        exit(EXIT_FAILURE);

    } else if(proc_id == 0) { // CHILD

        fprintf(stdout, "CHILD : PID=%ld\n", (long) getpid());
        sleep(30);
        exit(EXIT_SUCCESS);

    } else {                  // PARENT

        // Wait the end of the child process
        int status;
        wait(&status);
        if(WIFEXITED(status)) {
            printf("EXITED: %d\n", WEXITSTATUS(status));
        } else if(WIFSIGNALED(status)) {
            printf("SIGNALED: %d\n", WTERMSIG(status));
            //if(WCOREDUMP(status)) {
            //    printf("COREDUMP\n");
            //} else {
            //    printf("NO COREDUMP\n");
            //}
        }

        exit(EXIT_SUCCESS);
    }
}
