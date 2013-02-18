/* 
 * Rand
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc rand2.c
 * See "man 3 rand" for more info
 *
 */

#include <stdio.h>
#include <stdlib.h>                // srand() et rand() sont définies dans stdlib.h
#include <time.h>                  // time() est défini dans time.h

int main(int argc, char * argv[])
{
    srand(time(NULL));             // initialise le générateur

    int i;
    for(i = 0 ; i < 10 ; i++) {
        printf("%u\n", rand());    // tire un nombre entier entre 0 et RAND_MAX
    }

    return 0;
}
