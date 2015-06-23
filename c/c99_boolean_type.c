/*
 * Copyright (c) 2015 Jérémie DECOCK <jd.jdhp@gmail.com> (www.jdhp.org)
 */

#include <stdio.h>
#include <stdbool.h>

/*
 * Test ANSI C99 "bool" type and "true/false" macros.
 */
    
int main(int argv, char ** argc) {
    
    bool var = false;

    // ANSI C99/C11 don't include an extra printf conversion specifier for bool...
    printf("%s\n", var ? "true" : "false");

    var = true;

    printf("%s\n", var ? "true" : "false");

    return 0;
}
