/* 
 * Signal: ANSI C signal handling.
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc signal1.c
 * See "man 2 signal" for more info
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

void handler1(int signal) {
    printf("Signal %d received.\n", signal);
}

int main(int argc, char * argv[])
{
    if(signal(SIGINT, handler1) == SIG_ERR) {
        perror("signal");
    }

    pause();

    printf("Bye\n");

    return 0;
}
