/* 
 * Rand
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc rand1.c
 * See "man 3 rand" for more info
 *
 */

#include <stdio.h>
#include <stdlib.h>                  // srand() et rand() sont définies dans stdlib.h
#include <time.h>                    // time() est défini dans time.h

int main(int argc, char * argv[])
{
    srand(time(NULL));               // initialise le générateur

    int i;
    for(i = 0 ; i < 100 ; i++) {
        printf("%u ", rand() % 6);  // tire un nombre *entier* entre 0 et 5 (inclus)
    }

    printf("\n");

    return 0;
}
