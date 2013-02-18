/* 
 * Fork: fork the process multiple times.
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc fork_loop.c
 *        ./a.out | dot -Tpng > test.png
 *
 * See "man 2 fork" for more info
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char * argv[])
{
    fprintf(stdout, "digraph G {\n");
    fflush(stdout);

    pid_t parent_pid = getpid();

    int i;
    for(i=0 ; i<5 ; i++) {

        pid_t proc_id = fork();

        if(proc_id == -1) {  // ERROR
            perror("fork");
            exit(EXIT_FAILURE);
        }

        if(proc_id == 0) {   // CHILD

            fprintf(stdout, "\t%ld -> %ld;\n", (long) getppid(), (long) getpid());
            //exit(EXIT_SUCCESS);

        }
        
        // PARENT
        while(wait(NULL) != -1);

    }
    
    if(getpid() == parent_pid) {
        fprintf(stdout, "}\n");
    }
}
