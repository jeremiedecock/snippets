/* 
 * Pause: wait for signal.
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc pause.c
 * See "man 2 pause" for more info
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char * argv[])
{
    printf("Before pause (pid=%ld)\n", (long) getpid());

    int res = pause();

    printf("After pause (returned value is %d)\n", res);

    exit(EXIT_SUCCESS);
}
