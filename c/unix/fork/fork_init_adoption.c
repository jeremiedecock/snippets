/* 
 * Fork_init_adoption: show what happen when the parent process terminate
 * before the child process.
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc fork_init_adoption.c
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

    if(proc_id == 0) {   // CHILD

        fprintf(stdout, "CHILD  : Parent PID=%ld\n", (long) getppid());
        fprintf(stdout, "CHILD  : sleep...\n");
        sleep(2);
        fprintf(stdout, "CHILD  : wake up...\n");
        fprintf(stdout, "CHILD  : Parent PID=%ld (init)\n", (long) getppid());
        exit(0);

    } else {             // PARENT

        sleep(1);
        fprintf(stdout, "PARENT : goodbye\n");
        exit(0);

    }
}
