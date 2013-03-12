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

int main(int argc, char * argv[])
{
    if(signal(SIGINT, SIG_IGN) == SIG_ERR) {
        perror("signal");
    }

    pause();

    printf("Bye\n");

    return 0;
}
