/* 
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc string2.c
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char * argv[])
{
    /* ERROR: str is a constant string (in .rodata section, see objdump -s ...)
     * and cannot be modified */
    //{
    //    char * str = "hello";
    //    str[0] = 'H';
    //    printf("%s\n", str);
    //}

    /* OK: the "proper" way to do it, str is dynamically allocated ("hello" is
     * in .rodata section, see objdump -s ...) */
    {
        char * str = strdup("hello");
        str[0] = 'H';
        printf("%s\n", str);
    }

    /* OK: "hello" is in .text section (see objdump -s ...) but here str is
     * an "automatic" variable -> it is allocated in the stack */
    //{
    //    char str[] = "hello";
    //    str[0] = 'H';
    //    printf("%s\n", str);
    //}

    exit(EXIT_SUCCESS);
}

