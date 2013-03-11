/* 
 * Kill: send a signal to a process.
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc kill.c
 * See "man 2 kill" for more info
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

int main(int argc, char * argv[])
{
    if(argc!=3) {
        fprintf(stderr, "Usage: %s PID SIGNUMBER\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    pid_t pid = atol(argv[1]);
    int signal = atoi(argv[2]);

    printf("Send the signal %d to %ld.\n", signal, (long) pid);

    int kill_result = kill(pid, signal);

    if(kill_result != 0) {
        perror("KILL FAILURE");
    }

    exit(kill_result);
}
