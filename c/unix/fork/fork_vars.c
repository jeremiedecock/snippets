/* 
 * Fork: show that child's and parent's variables are independent.
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc fork_vars.c
 * See "man 2 fork" for more info
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int global_var = 3;

int main(int argc, char * argv[])
{
    int local_var = 3;

    pid_t proc_id = fork();

    if(proc_id == -1) {

        // Error...
        fprintf(stderr, "Fork failure\n");
        exit(1);

    } else if(proc_id == 0) {

        // Child process
        
        global_var++;
        local_var++;

        fprintf(stdout, "Child (PID=%ld): global_var=%d local_var=%d\n", (long) getpid(), global_var, local_var);

        exit(0);

    } else {

        // Parent process

        global_var--;
        local_var--;

        fprintf(stdout, "Parent (PID=%ld): global_var=%d local_var=%d\n", (long) getpid(), global_var, local_var);

        // Wait the end of the child process
        wait(NULL);
        exit(0);
    }
}
