/* 
 * Fork + exec: fork the process and run a program.
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc fork_execl.c
 * See "man 2 fork" for more info
 * See "man 3 exec" for more info
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
        perror("fork");
        exit(EXIT_FAILURE);

    }

    if(proc_id == 0) {  // CHILD

        execl("/bin/cat", "cat", "/proc/loadavg", NULL);

        /* execl() only returns on error */
        perror("execl");
        exit(EXIT_FAILURE);

    } else {            // PARENT

        wait(NULL);

    }
    
}
