/* 
 * Exec: exec an application.
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc execlp.c
 * See "man 3 exec" for more info
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char * argv[])
{
    execlp("ls", "ls", "-l", "./", NULL);

    /* execlp() only returns on error */
    perror("execlp");
    exit(EXIT_FAILURE);
}
