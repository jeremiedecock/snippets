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
    pid_t proc_id;

    proc_id = fork();

    if(proc_id == -1) {

        // Error...
        fprintf(stderr, "Fork failure\n");
        exit(1);

    }

    fprintf(stdout, "Print1 : PID=%ld, PPID=%ld, FORK_RETURN=%ld\n", (long) getpid(), (long) getppid(), (long) proc_id);
    
    if(proc_id == 0) {

        // Child process
        fprintf(stdout, "Print2 (child) : PID=%ld, PPID=%ld\n", (long) getpid(), (long) getppid());
        //exit(0);

    }

    fprintf(stdout, "Print3 : PID=%ld, PPID=%ld, FORK_RETURN=%ld\n", (long) getpid(), (long) getppid(), (long) proc_id);

    exit(0);
}
