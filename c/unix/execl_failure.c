/* 
 * Exec: exec an application.
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc execl.c
 * See "man 3 exec" for more info
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char * argv[])
{
    execl("/bin/ls", "ls", "-l ./", NULL);

    /* execl() only returns on error */
    perror("execl");
    exit(EXIT_FAILURE);
}
