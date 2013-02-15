/* 
 * Exec: exec an application.
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc execv.c
 * See "man 3 exec" for more info
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char * argv[])
{
    char * exec_argv[] = { "ls", "-l", "./", NULL };

    execv("/bin/ls", exec_argv);

    /* execv() only returns on error */
    perror("execv");
    exit(EXIT_FAILURE);
}
