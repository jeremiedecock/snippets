/* 
 * Alarm: set an alarm clock for delivery of a signal.
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc alarm.c
 * See "man 2 alarm" for more info
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char * argv[])
{
    alarm(3);
    pause();

    printf("Bye\n");

    exit(EXIT_SUCCESS);
}

