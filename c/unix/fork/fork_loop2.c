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

        pid_t proc_id = fork();

        if(proc_id == -1) {  // ERROR
            perror("fork");
            exit(EXIT_FAILURE);
        }

        if(proc_id == 0) {   // CHILD

            printf("start %ld\n", (long) getpid());
            sleep(3);
            printf("exit %ld\n",  (long) getpid());
            exit(EXIT_SUCCESS);

        }

    }
        
    // PARENT
    while(wait(NULL) != -1);
    
}
