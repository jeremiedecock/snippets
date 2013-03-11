/* 
 * Kill: send a signal to a process.
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc kill_term.c
 * See "man 2 kill" for more info
 *
 */

#include <signal.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char * argv[])
{
    if(argc!=2) {
        fprintf(stderr, "Usage: %s PID\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    pid_t pid = atol(argv[1]);

    // Il est preferable d'utiliser les constantes symboliques (ici SIGTERM)
    // plutot que les numeros de signaux (variables d'un systeme a l'autre).
    // Pour Gnu/Linux, les constantes symboliques sont definies dans le header
    // "/usr/include/i386-linux-gnu/bits/signum.h".
    int kill_result = kill(pid, SIGTERM);

    if(kill_result != 0) {
        perror("KILL FAILURE");
    }

    exit(kill_result);
}
