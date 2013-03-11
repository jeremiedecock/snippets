/* 
 * Raise: send a signal to the caller.
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc raise.c
 * See "man 3 raise" for more info
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

int main(int argc, char * argv[])
{
    if(argc!=2) {
        fprintf(stderr, "Usage: %s SIGNUMBER\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    int signal = atoi(argv[1]);

    raise(signal);

    exit(EXIT_SUCCESS);
}
