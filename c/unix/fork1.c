/* 
 * Fork: fork the process and display resulting PID and PPID.
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc fork1.c
 * See "man 2 fork" for more info
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char * argv[])
{
    pid_t proc_id = fork();

    if(proc_id == -1) {

        // Error...
        fprintf(stderr, "Fork failure\n");
        exit(1);

    }

    // Reached by both process (parent and child)
    fprintf(stdout, "Hello form process %ld\n", (long) getpid());

    if(proc_id == 0) {

        // Reached by child process only
        fprintf(stdout, "CHILD : PID=%ld, Parent PID=%ld\n", (long) getpid(), (long) getppid());

    } else {

        // Reached by parent process only
        fprintf(stdout, "PARENT : PID=%ld, Parent PID=%ld, Child PID (fork return)=%ld\n", (long) getpid(), (long) getppid(), (long) proc_id);

    }

    // Reached by both process (parent and child)
    fprintf(stdout, "Goodbye form process %ld\n", (long) getpid());
    
}
