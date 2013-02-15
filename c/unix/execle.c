/* 
 * Exec: exec an application.
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc execle.c
 * See "man 3 exec" for more info
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char * argv[])
{
    char * exec_envp[] = { NULL };

    execle("/bin/ls", "ls", "-l", "./", NULL, exec_envp);

    /* execle() only returns on error */
    perror("execle");
    exit(EXIT_FAILURE);
}
