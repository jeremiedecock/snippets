/* 
 * Exec: exec an application.
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc execve.c
 * See "man 3 exec" for more info
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char * argv[])
{
    char * exec_argv[] = { "ls", "-l", "./", NULL };
    char * exec_envp[] = { NULL };

    execve("/bin/ls", exec_argv, exec_envp);

    /* execve() only returns on error */
    perror("execve");
    exit(EXIT_FAILURE);
}
