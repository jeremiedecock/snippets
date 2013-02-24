/* 
 * Exec: exec an application.
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc execvp.c
 * See "man 3 exec" for more info
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char * argv[])
{
    char * exec_argv[] = { "ls", "-l", "./", NULL };

    execvp("ls", exec_argv);

    /* execvp() only returns on error */
    perror("execvp");
    exit(EXIT_FAILURE);
}
